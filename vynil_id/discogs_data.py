from curses import raw
import json
from urllib import request, response
from urllib.parse import parse_qsl
from urllib.parse import urlparse
import requests
from PIL import Image
from io import BytesIO
import re
import discogs_client
from os import makedirs
import time


TEST_LABEL_ID = '728017' ##acid wax

DISCOGS_RELEASE_URL = 'https://api.discogs.com/releases/'
# Enter your user token to get images
d = discogs_client.Client('ExampleApplication/0.1' ,  user_token="puQrtnEjrKmMyUteBXrItifKdglTROLzMCGGfbem")

def get_discogs_cover_image(discogs_id):
    """Function returning the cover image of the album"""
    # Change the 0 to get other images associated with the album

    #returns the images of albums that have an image associated with it
    if d.release(discogs_id).images is not None:
        cover = d.release(discogs_id).images[0]
        cover_url = list(cover.values())[1]
        response = requests.get(cover_url)
        cover_img = Image.open(BytesIO(response.content))

        return cover_img
    pass

def get_discogs_release_data(discogs_id):
    """Get's release data in JSON form"""
    params = {'id':discogs_id}

    response = requests.get(DISCOGS_RELEASE_URL+params['id'])
    json_data = response.json()
    return json_data

def get_discogs_artist_name(discogs_id):
    """Function returning the album name of the album"""
    if d.release(discogs_id).artists[0].name is not None:
        artist_name = d.release(discogs_id).artists[0].name
        return artist_name
    pass


def get_discogs_album_name(discogs_id):
    """Function returning the album name of the album"""
    if d.release(discogs_id).title is not None:
        album = d.release(discogs_id).title
        return album
    pass

def get_discogs_album_names(discogs_label_id = False, ids = False, save = False):
    if discogs_label_id:
        ids = get_discogs_album_name(discogs_label_id)
    elif ids == False:
        return 'No Album or ID listed'
    # returns the images from the label discogs has a request limit of 60 per minute

    for id in ids:
        album_name = get_discogs_album_name(id)
        print(album_name)
    pass

# def get_discogs_album_name(json_data):
#     """Function returning the name of the album"""
#     album_name = json_data['title']
#     return album_name

def get_discogs_url(json_data):
    """Function returning the url for the album"""
    album_url = json_data['uri']
    return album_url

def get_discogs_lowest_price(json_data):
    """Function returning the lowest price on discogs in $"""
    lowest_price = json_data['lowest_price']
    return lowest_price

def get_release_id_from_labels(discogs_label_id):
    """Function returning a list of album ids from a label"""

    # Dictionary for all the records released by the label

    page_number = len(d.label(discogs_label_id).releases)/50

    label_results = {}
    for i in range(int(page_number)+2):
        label = d.label(discogs_label_id).releases.page(i)
        label_results[i] = label

    # List of lists of values from the dictionary
    label_results_list = []

    res_val = label_results.values()
    for value in res_val:
        str(value)
        label_results_list.append(value)

    # Singular list of Release id and title
    fin_list = [l for sl in label_results_list for l in sl]

    #list of release ids
    release_id_from_label = []

    for i in fin_list:
        match = re.search( '\s+([^\s]+)' ,str(i))
        if match:
            release_id_from_label.append(match.group().strip())

    return release_id_from_label

def get_discogs_album_covers(discogs_label_id = False, ids = False, save = False):
    if discogs_label_id:
        ids = get_release_id_from_labels(discogs_label_id)
    elif ids == False:
        return 'No label or ID listed'
    # returns the images from the label discogs has a request limit of 60 per minute

    for id in ids:
        time.sleep(5)
        image = get_discogs_cover_image(id)
        if save == True and image:
            image.save('raw_data/discogs_images/'+ id + '.jpg', "JPEG", quality=80, optimize=True, progressive=True)
    pass


#class to get Album names and cover images
def get_discogs_album_names_and_cover_images(discogs_label_id = False, ids = False, save = False):
    if discogs_label_id:
        ids = get_discogs_album_name(discogs_label_id)
    elif ids == False:
        return 'No Album or ID listed'
    # returns the images from the label discogs has a request limit of 60 per minute

    for id in ids:
        image = get_discogs_cover_image(id)
        artist_name = get_discogs_artist_name(id)
        album_name = get_discogs_album_name(id)
        print(image)
        print(artist_name)
        print(album_name)
        if save == True and image:
            raw_data = 'raw_data/discogs_images/'
            album_name_path = raw_data+artist_name+' - '+album_name
            # makedirs(album_name_path, exist_ok=True)
            # image.save(album_name_path + '/' + artist_name + ' - ' + album_name + ' - ' + id + '.jpg', "JPEG", quality=80, optimize=True, progressive=True)
            image.save(artist_name + ' - ' + album_name + ' - ' + id + '.jpg', "JPEG", quality=80, optimize=True, progressive=True)
    pass


# if __name__ == '__main__':
#     # ids = get_release_id_from_labels(TEST_LABEL_ID)
#     with open('vynil_id/data/discogs_targets.txt') as f:
#         line = f.readline()
#         ids = line.split(',')
#     get_discogs_album_covers(discogs_label_id = False, ids = ids, save=True)


# Get Image inside the album name.
if __name__ == '__main__':
    # ids = get_release_id_from_labels(TEST_LABEL_ID)
    with open('vynil_id/data/discogs_targets.txt') as f:
        line = f.readline()
        ids = line.split(',')
    get_discogs_album_names_and_cover_images(discogs_label_id = False, ids = ids, save=True)
