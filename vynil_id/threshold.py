# import the necessary packages
from gc import get_threshold
import cv2
import numpy as np
from matplotlib import pyplot as plt
from utils.geo_tools import *
from utils.cv2_tools import *
import os
import copy
import itertools


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
            #image = resize_image(image)
            lines_h, lines_v = hough_lines_threshold(image)
            lines_h_pairs = (itertools.combinations(lines_h, 2))
            lines_v_pairs = (itertools.combinations(lines_v,2))
            unsorted_quads = []
            for line_h in lines_h_pairs:
                for line_v in lines_v_pairs:
                    unsorted_quad = pair_lines_to_quads(line_h, line_v)
                    print(unsorted_quad)
                    unsorted_quads.append(unsorted_quad)
            cv2.destroyAllWindows()
