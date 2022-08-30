from dis import dis, disco
from logging import PercentStyle
from this import d
import imagehash
import os
from PIL import Image
import pickle
import threshold
import cv2
import numpy as np
import pandas as pd

##Turn that for filename in dir do function into function that accepts function and params as param
PHASH_LOCATION = 'vynil_id/data/phashs.dat'
DISCOGS_IMAGE_DIRECTORY = 'raw_data/discogs_images'
MERCARI_IMAGE_DIRECTORY = 'raw_data/mercari_images'
MERCARI_ANNOTATED = 'vynil_id/data/annotated_mercari.csv'
DISCOGS_NAMES = 'vynil_id/data/discogs_names.csv'

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
    with open(PHASH_LOCATION, 'wb') as f:
        pickle.dump(hashs, f)

def load_phash(directory):
    with open(directory, 'rb') as filename:
        hashs = pickle.load(filename)
    return hashs

def phash_candidates(candidates):
    hashs = []
    for candidate in candidates:
        hash = phash(candidate)
        hashs.append(hash)
    return hashs

def check_against_library(candidate_hashs, library_hashs):
    distances = []
    for candidate_hash in candidate_hashs:
        for discogs_id, library_hash in library_hashs.items():
            distance = candidate_hash-library_hash
            distances.append((distance, discogs_id))
    return distances

def get_prediction(candidates, library_hashs):
    distances = check_against_library(phash_candidates(candidates), library_hashs)
    #print(distances)
    distance, discogs_id = zip(*distances)
    idx = np.argmin(distance)
    prediction = discogs_id[idx]
    print(prediction)
    return prediction

def phash(image):
    hash = imagehash.average_hash(image)
    return(hash)

if __name__ == '__main__':
    phash_collection(directory=DISCOGS_IMAGE_DIRECTORY)
    library_hashs = load_phash(PHASH_LOCATION)

    i = 0
    annotated_mercari_df = pd.read_csv(MERCARI_ANNOTATED, sep=',')
    discogs_names_df = pd.read_csv(DISCOGS_NAMES, sep=',')
    discogs_names_df.discogs_id.astype(int)
    records = pd.merge(annotated_mercari_df, discogs_names_df, how = 'left', left_on=['class'], right_on=['name'])
    records = records.set_index('file_name').drop(columns='name')

    files = []
    for file in os.listdir(MERCARI_IMAGE_DIRECTORY):
        if file in records.index.values:
            files.append(file)

    preds = []
    files = files[:10]
    len(file)
    correct_num = 0
    for file in files:
        f = os.path.join(MERCARI_IMAGE_DIRECTORY, file)
        if os.path.isfile(f):
            image = cv2.imread(f) ##image = Image.open(f)

            candidates = threshold.messy_threshold(image)

            candidates_pil = [Image.fromarray(cv2.cvtColor(candidate, cv2.COLOR_BGR2RGB)) for candidate in candidates]
            prediction = get_prediction(candidates, library_hashs)
            preds.append((file,prediction))

    preds_df = pd.DataFrame(preds, columns=['file_name','prediction_id']).set_index('file_name')
    preds_df['prediction_id'] = preds_df.astype({'prediction_id':'int64'})
    records = records.join(preds_df, how='left')

    records['correct'] = np.where(records['discogs_id'] == records['prediction_id'], True, False)
    print(records['correct'].value_counts())
    records.to_csv('vynil_id/data/phash_classification.csv')
