from bs4 import BeautifulSoup as bs
import urllib.parse as urlparse
import itertools
from decimal import Decimal
from re import sub
import lxml
from dataclasses import dataclass
import requests
import json
## To do ##
## 1. in the config file, the 'drop' value needs to be updated every (???) at least every few days
## how do we get this from an initial call on start up?

MERCARI_SEARCH_JSON_PATH = 'vynil_id/config/mercari_search.json'
MERCARI_SEARCH_URL = 'https://api.mercari.jp/v2/entities:search'
MERCARI_DESCRIPTION_URL = 'https://api.mercari.jp/items/get'

with open(MERCARI_SEARCH_JSON_PATH, 'r') as f:
    json_data = json.load(f)
    HEADERS = json_data['headers_search']
    HEADERS_DESCRIPTION = json_data['headers_description']
    JSON_PARAMS = json_data['params']

@dataclass
class Listing:
    """ A listing of an item on Mercari with the name, product url, price (in yen), and a sold boolean. """
    name: str = None
    mercari_id: str = None
    price: int = 0
    is_sold: bool = True
    updated: int = 0 ##epoch seconds
    condition: int = 0
    free_shipping: bool = False
    description: str = ''
    buy: bool = False

    def __post__init__(self):
        if self.get_desc:
            self.desc

    def __repr__(self):
        return f'Mercari Listing name: "{self.name}"; id {self.id}'

    def __str__(self):
        return f'"{self.name}" is {"" if self.is_sold else "not"} sold @¥{self.price} ({self.id})' \
               + (f' [desc defined]' if self.desc else '')

    def __contains__(self, item):
        return item.lower() in self.name.lower()


    @property
    def purchase_url(self):
        return f'https://www.mercari.com/jp/transaction/buy/{self.id}'

    @property
    def listing_url(self):
        return f'https://www.mercari.com/jp/items/{self.id}'


def get_mercari_listings(json_data
                         , get_desc=False):
    '''Parses search result JSON data and returns a list of listings'''
    listings = []
    for listing in json_data:
        name = listing['name']
        mercari_id = listing['id']
        price = int(listing['price'])
        if listing['status'] == "ITEM_STATUS_ON_SALE":
            is_sold = 0
        free_shipping = int(listing['shippingPayerId']) - 1 ## 1 is buyer pays, 2 is seller pays
        condition = int(listing['itemConditionId'])

        if get_desc == True:
            description = get_mercari_item_description(mercari_id)
        else:
            description = ''

        listings.append(Listing(name=name,
                                mercari_id=mercari_id,
                                price=price,
                                is_sold=is_sold,
                                condition=condition,
                                free_shipping=free_shipping,
                                description=description))

        get_mercari_images(mercari_id)

    return listings


def get_mercari_item_description(mercari_id):
    """Function returning the description text for a given Mercari listing based on url"""
    params = {'id': mercari_id}


    response = requests.get(MERCARI_DESCRIPTION_URL, params=params, headers=HEADERS_DESCRIPTION)
    print(response)
    json_data = json.loads(response.text)['data']
    description = json_data['description']
    return description

def get_mercari_search_results(url=MERCARI_SEARCH_URL
                               , headers=HEADERS
                               , json_params=JSON_PARAMS
                               , items=10
                               , save=False):
    """Uses the mercariAPI to get search results based on saved parameters"""
    ### mercari.com entities::search
    json_params['pageSize'] = items
    response = requests.post(url=url, headers=headers, json=json_params)
    json_data = json.loads(response.text)['items']

    if save == True:
        with open('vynil_id/config/mercari_search_resultsANRI.json', 'w') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)

    return json_data

def get_mercari_images(mercari_id):
    '''Gets the image from a mercari listing based on mercari_id'''
    ## to get other images change the _1 to another number
    url = 'https://static.mercdn.net/item/detail/orig/photos/' + mercari_id + '_1.jpg'
    img_data = requests.get(url).content
    with open('raw_data/mercari_images/'+ mercari_id + '.jpg', 'wb') as handler:
        handler.write(img_data)
    pass

if __name__ == '__main__':
    ##Currently set to read results from file for testing
    #json_data = get_mercari_search_results(MERCARI_SEARCH_URL, HEADERS, JSON_PARAMS, items=50, save=True)
    with open('vynil_id/config/mercari_search_resultsUTADA.json', 'r') as json_file:
        json_data = json.load(json_file)
    listings = get_mercari_listings(json_data)
