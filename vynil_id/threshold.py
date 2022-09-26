# import the necessary packages
from gc import get_threshold
from math import comb
import cv2
import numpy as np
from matplotlib import pyplot as plt
from utils.geo_tools import *
from utils.cv2_tools import *
import os
import copy
import itertools
import random

MERCARI_IMAGES = 'raw_data/mercari_images'

def get_quads(contours, method='oct'):
    quads = []
    if method == 'oct':
        for contour in contours:
            oct_points = max_directional_oct(contour)
            quad = contour_to_quad(oct_points)
            quads.append(quad)
    elif method == 'red':
        eps = 0.010
        ## reduce all hulls
        for contour in contours:
            peri = cv2.arcLength(contour, True)
            reduced_contour = cv2.approxPolyDP(contour, eps * peri, True)
            quad = contour_to_quad(reduced_contour)
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


        quad_ = contour_to_quad(reduced_contour)
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

def messy_threshold(image, verbose=False):
    '''a currently very messy function'''
       #image = resize_image(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    lines_h, lines_v = hough_lines_threshold(image, verbose=True)
    image_size = image.shape
    if len(lines_h) >20:
        lines_h = random.sample(lines_h,20)
    if len(lines_v) >20:
        lines_v = random.sample(lines_v,20)
    lines_h.append(((0,0),(1,0)))
    lines_h.append(((0,0),(0,1)))
    lines_h.append(((image_size[0],image_size[1]), (image_size[0],0)))
    lines_h.append(((image_size[0],image_size[1]), (0,image_size[0])))
    lines_h_pairs = list(itertools.combinations(lines_h, 2))
    lines_v_pairs = list(itertools.combinations(lines_v,2))
    unsorted_quads = []
    i = 0
    for line_h in lines_h_pairs:
        for line_v in lines_v_pairs:
            i += 1
            unsorted_quad = pair_lines_to_quads(line_h, line_v)
            unsorted_quads.append(unsorted_quad)

    oriented_quads = []
    for unsorted_quad in unsorted_quads:
        oriented_quad = orient_quad_arbitrary(unsorted_quad)
        if oriented_quad is not None:
            oriented_quads.append(oriented_quad)

    image_size = image.shape
    min_area = image_size[0] * image_size[1] / 9
    reduced_contours = reduce_small_contours(oriented_quads, min_size=min_area)
    #cv2.drawContours(image,reduced_contours,-1,(255,0,255),4)
    contours = squarish(reduced_contours)
    print(f'H Lines: {len(lines_h)}, V Lines: {len(lines_v)}')
    print(f'Line Pairs: {i}, Unsorted: {len(unsorted_quads)}, Oriented: {len(oriented_quads)}, Reduced: {len(reduced_contours)}, Big: {len(reduced_contours)}, Square: {len(contours)}')
    l10 = math.ceil(len(contours) / 10)

    largest_contours = sorted(contours, key=cv2.contourArea)[-(l10+3):]
    if verbose == True:
        image_c = image.copy()
        cv2.drawContours(image_c,largest_contours,-1,(255,0,255),5)
        plt.figure(figsize=(8,8))
        plt.imshow(image_c)
        plt.show()
        cv2.destroyAllWindows()

    candidates = []
    for quad in largest_contours:
        candidate = unwarp(image, quad, verbose=verbose)
        candidates.append(candidate)

    return candidates

if __name__ == '__main__':

    for filename in os.listdir(MERCARI_IMAGES):
        f = os.path.join(MERCARI_IMAGES, filename)

    #checking if it is a file
        if os.path.isfile(f):
            image = cv2.imread(f)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            contours = messy_threshold(image,verbose=False)
