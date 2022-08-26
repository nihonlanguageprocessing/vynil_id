import cv2
import numpy as np
from utils.geo_tools import *

def reduce_contours(contours, eps=0.010):
    '''returns a list of all simplified contours'''
    reduced_contours = []

    ## reduce all contours
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        reduced_contour = cv2.approxPolyDP(contour, eps * peri, True)
        reduced_contours.append(reduced_contour)

    return reduced_contours

def oct_contours(contours):
    '''returns a list of all octagonal contours'''
    return contours

def get_contours(image,min_size = 6000):
    '''return a list of all contours larger than min_size area'''
    image_filtered = filter_(image)
    image_filtered = clahe(image_filtered, 5, (3, 3))


    img_blur = cv2.blur(image_filtered, (10, 10))
    img_th = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 51, 2)

    contours,_ = cv2.findContours(img_th,
                                           cv2.RETR_CCOMP,
                                            cv2.CHAIN_APPROX_SIMPLE)

    ## Getting rid of small contours
    contours = [contour for contour in contours if cv2.contourArea(contour) >= min_size]
    return contours

def get_hulls(contours):
    '''return a list of convex hulls for each contour'''
    hulls = []
    for i in range(len(contours)):
        # creating convex hull object for each contour
        hulls.append(cv2.convexHull(contours[i], False))
    return hulls

def clahe(image, clip_limit=2.0, grid_size=(8,8)):
    '''applies CLAHE on a single channel  image'''
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
    return clahe.apply(image)

def squarish(contours):
    '''returns squarish contours'''
    squarish_contours = []
    for contour in contours:
        dists = point_distances(contour)
        avg_length = np.average(dists)
        diff = np.sum(np.abs(dists - avg_length))
        ratio = diff / sum(dists)

        if  ratio <= 0.075:
            squarish_contours.append(contour)

    return squarish_contours

def unwarp(image, contour, verbose=False):
    '''unwarps an image based on quadrilateral contours'''
    h, w = image.shape[:2]
    # use cv2.getPerspectiveTransform() to get M, the transform matrix, and Minv, the inverse
    size = int(500)
    source = orient_quad(contour.squeeze(axis=1).astype(np.float32))


    dest = np.float32([(size, 0),
                  (size, size),
                  (0, size),
                  (0, 0)])



    M = cv2.getPerspectiveTransform(source, dest)
    # use cv2.warpPerspective() to warp your image to a top-down view
    warped = cv2.warpPerspective(image, M, (w, h), flags=cv2.INTER_LINEAR)
    crop_warped = warped[0:size, 0:size].copy()
    crop_warped = np.flip(crop_warped, axis=1)
    if verbose:
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
        f.subplots_adjust(hspace=.2, wspace=.05)
        ax1.imshow(image)

        ax1.set_title('Original Image', fontsize=30)
        ax2.imshow(cv2.flip(crop_warped, 1))
        ax2.set_title('Unwarped Image', fontsize=30)
        plt.show()
    else:
        return crop_warped, M

def filter(image):
    pass


def filter_(image):
    '''currently not using'''
    color = image[0][0]
    hsv = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2HSV)
    lower = np.array([0, 0, 120])
    upper = np.array([180, 38, 255])
    #lower = color - 60
    #upper = color + 60
    print(lower)
    print(upper)
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(image,image, mask=mask)
    r, g, b = cv2.split(result)

    f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(20, 10))
    f.subplots_adjust(hspace=.2, wspace=.05)
    ax1.imshow(result)
    ax2.imshow(r)
    ax3.imshow(g)
    ax4.imshow(b)

    plt.show()
    g = clahe(g, 5, (3, 3))
    return g

def resize_image(image):
    width = 300
    height = int(width / image.shape[1] *  image.shape[0])
    dim = (width, height)

    # resize image
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return resized
