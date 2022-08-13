import numpy as np
from matplotlib import pyplot as plt
from utils import seg_intersect

def min_quad_oct(contours):
    '''From a contours, finds maxiumum points in each of 8 directions'''
    rs_hull = [np.squeeze(h,axis=1) for h in contours]
    oct_points = []
    for h in rs_hull:
        x,y=np.split(h,2,axis=1)

        ## gets the maximum point in 8 cardinal directions
        ## 4 cardinal directions
        max_e = int(max(x))
        max_w = int(min(x))
        max_n = int(max(y))
        max_s = int(min(y))

        max_e_ = [max_e, int(min(y[np.where(x == max_e)[0]]))]
        max_s_ = [int(min(x[np.where(y == max_s)[0]])), max_s]
        max_w_ = [max_w, int(min(y[np.where(x == max_w)[0]]))]
        max_n_ = [int(min(x[np.where(y == max_n)[0]])), max_n]

        ## diagonal cardinal directions
        nw = -x+y
        ne = x+y
        se = x-y
        sw = -x-y

        max_nw = int(max(nw))
        max_ne = int(max(ne))
        max_se = int(max(se))
        max_sw = int(max(sw))

        max_nw_i = np.argmax(nw == max_nw)
        max_ne_i = np.argmax(ne == max_ne)
        max_se_i = np.argmax(se == max_se)
        max_sw_i = np.argmax(sw == max_sw)

        max_nw_ = [int(x[max_nw_i]), int(y[max_nw_i])]
        max_ne_ = [int(x[max_ne_i]), int(y[max_ne_i])]
        max_se_ = [int(x[max_se_i]), int(y[max_se_i])]
        max_sw_ = [int(x[max_sw_i]), int(y[max_sw_i])]

        ## creates an onctagon that binds the hull
        oct_point = [max_w_, max_nw_, max_n_, max_ne_, max_e_, max_se_, max_s_, max_sw_]

        ## convert to contour
        oct_point = np.array(oct_point).reshape((-1,1,2)).astype(np.int32)
        oct_points.append(oct_point)

    return oct_points

def point_distances(points):
    '''get distances between sequential points
    Points should be ordered either counter or clockwise'''
    dists = []
    for i in range(-1,7):
        dists.append(np.linalg.norm(points[i]-points[i+1]))
    return dists

def longest_line_indices(dists, num_lines=4):
    '''find longest lines by index (i-1, i)'''
    ind = np.argpartition(dists, -num_lines)[-num_lines:]
    ind.sort()

    ## get pairs of points forming longest lines
    indices_pairs = []
    for i in ind:
        indices_pairs.append([(i-1) % 8, i])

    return indices_pairs

def longest_line_intersections(points, indices_pairs):
    '''Return the n-gon formed by the intersection of the
    line segments created from points as indicated by the indices_pairs'''
    ngon_points = []
    for i in range(-1,len(indices_pairs)-1):
        p1 = points[indices_pairs[i][0]][0]
        p2 = points[indices_pairs[i][1]][0]
        p3 = points[indices_pairs[i+1][0]][0]
        p4 = points[indices_pairs[i+1][1]][0]

        ngon_points.append(seg_intersect(p1,p2,p3,p4))

    ## Convert to contour
    ngon = np.stack(ngon_points, axis=0).reshape((-1,1,2)).astype(np.int32)
    return ngon
