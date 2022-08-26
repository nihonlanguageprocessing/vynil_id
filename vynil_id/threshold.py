# import the necessary packages
from gc import get_threshold
import cv2
import numpy as np
from matplotlib import pyplot as plt
from utils.geo_tools import *
from utils.cv2_tools import *
import os
import copy


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
    image_  = copy.deepcopy(image)
    contours = get_contours(image)

    reduced_contours = []
    eps = 0.010
    ## reduce all hulls
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        reduced_contour = cv2.approxPolyDP(contour, eps * peri, True)
        print(len(reduced_contour))

        dists = point_distances(reduced_contour)
        indices_pairs = longest_line_indices(dists)
        quad_ = longest_line_intersections(reduced_contour, indices_pairs)
        quad_ = cv2.approxPolyDP(quad_, 0.010, closed=True)
        reduced_contours.append(quad_)

    cv2.drawContours(image,reduced_contours,-1,(255,255,255),5)
    plt.figure(figsize=(8,8))
    plt.imshow(image)
    plt.show()



    hulls = get_hulls(contours)
    cv2.drawContours(image,hulls,-1,(0,255,255),5)
    plt.figure(figsize=(8,8))
    plt.imshow(image)
    plt.show()


    quads = get_quads(contours = hulls, method = 'oct')
    quads = squarish(quads)

    candidates = []
    for quad in quads:
        candidate = unwarp(image, quad, verbose=False)
        candidates.append(candidate)


    if verbose==True:
        cv2.drawContours(image,quads,-1,(0,0,255),5)
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
           image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
           image = resize_image(image)
           threshold(image, verbose=False)
           cv2.destroyAllWindows()
