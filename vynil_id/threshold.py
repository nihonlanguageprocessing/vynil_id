# import the necessary packages
from gc import get_threshold
import cv2
import numpy as np
from matplotlib import pyplot as plt
from utils.geo_tools import *
from utils.cv2_tools import *
import os


def get_quads(contours, method='oct'):
    quads = []
    if method == 'oct':
        for contour in contours:
            oct_points = max_directional_oct(contour)
            dists = point_distances(oct_points)
            indices_pairs = longest_line_indices(dists)
            quad = longest_line_intersections(oct_points, indices_pairs)
            quads.append(quad)
    elif method == 'red':
        eps = 0.010
        ## reduce all hulls
        for contour in contours:
            peri = cv2.arcLength(contour, True)
            reduced_contour = cv2.approxPolyDP(contour, eps * peri, True)
            dists = point_distances(reduced_contour)
            indices_pairs = longest_line_indices(dists)
            quad = longest_line_intersections(reduced_contour, indices_pairs)
            quads.append(quad)
    return quads


def threshold(image, verbose = False, show_candidates = False):
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contours = get_contours(image)
    hulls = get_hulls(contours)

    quads = get_quads(contours = hulls, method = 'red')
    quads = squarish(quads)

    candidates = []
    for quad in quads:
        candidate = unwarp(image, quad)
        candidates.append(candidate)
        print('hello')


    if verbose==True:
        cv2.drawContours(image,quads,-1,(0,255,255),5)
        plt.figure(figsize=(8,8))
        plt.imshow(image)
        plt.show()

    pass

if __name__ == '__main__':
    directory = 'raw_data/mercari_images'
    for filename in os.listdir(directory):
       f = os.path.join(directory, filename)
    # checking if it is a file
       if os.path.isfile(f):
           image = cv2.imread(f)
           threshold(image, verbose=True)
