import p_hashing
from mercari_listing import get_mercari_search_results, get_mercari_listings
import threshold
import os
import cv2



def main(connect = False, verbose = False):
    if connect == True:
        get_mercari_listings(get_mercari_search_results())

    directory = 'raw_data/mercari_images'
    for filename in os.listdir(directory):
       f = os.path.join(directory, filename)
    # checking if it is a file
       if os.path.isfile(f):
           image = cv2.imread(f)
    ## get all candidates
    ## get phash of all candidates
    ## compare to all pre calculated phashes

if __name__ == '__main__':
    main(verbose=True)
