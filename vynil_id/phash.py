import imagehash
import os
from PIL import Image
import pickle

##Turn that for filename in dir do function into function that accepts function and params as param
PHASH_DESTINATION = 'vynil_id/data/phashs.json'

def phash_collection(directory=False, candidates=False, **kwargs):

    if directory:
        phash_directory(directory)
    elif candidates:
        phash(candidates)
    pass

def read_phash(location):
    pass

def phash_directory(directory):
    hashs = {}
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            image = Image.open(f)
            discogs_id = filename[:filename.index(".")]
            hash = phash(image)
            hashs[discogs_id] = hash
    with open(PHASH_DESTINATION, 'wb') as f:
        pickle.dump(hashs, f)

def phash_candidates(candidates):
    hashs = []
    for candidate in candidates:
        hash = phash(candidate)
        hashs.append(hash)
    return hashs

def phash(image):
    hash = imagehash.average_hash(image)
    return(hash)

if __name__ == '__main__':
    directory = 'raw_data/discogs_images'
    phash_collection(directory=directory)
