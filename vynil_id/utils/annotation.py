import cv2
import os
import time
import cv2_tools
import numpy as np
import json

MERCARI_IMAGES = 'raw_data/mercari_images'

#TO DO
# Save to file
# Only open non annotated files
# Double click clear all
# Single rclick clear last drawn


class Annotater(object):
    def __init__(self, image_path):
        self.original_image = cv2.imread(image_path)
        self.clone = self.original_image.copy()
        self.image_path = image_path

        window = cv2.namedWindow('image')
        cv2.moveWindow('image', 40,30)
        cv2.setMouseCallback('image', self.extract_coordinates)

        # Bounding box reference points
        self.image_coordinates = [[]]

    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.clone,(x,y),2,(0,0,255),-1)
            self.image_coordinates[-1].append((x,y))
            cv2.imshow("image",self.clone)


        elif event == cv2.EVENT_MBUTTONDOWN:
            self.reshape_to_quad()
            self.draw_quad()
            self.image_coordinates.append([])

        # Clear last drawn quad on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()
            if len(self.image_coordinates)>1:
                if len(self.image_coordinates[-1])==0:
                    self.image_coordinates.pop()
                self.image_coordinates.pop()
                self.draw_quads()
            else:
                self.image_coordinates = [[]]

            cv2.imshow("image",self.clone)



    def reshape_to_quad(self, idx = -1):
        self.image_coordinates[idx] = np.stack(self.image_coordinates[idx], axis=0).reshape((-1,1,2)).astype(np.int32)
        if len(self.image_coordinates[idx]) > 4:
            self.image_coordinates[idx] = self.reduce_polygon_to_q()
        pass

    def draw_quad(self, internal = True, idx = -1):
        ##draw hull on image and show

        cv2.drawContours(self.clone, [self.image_coordinates[idx]], 0, (0,255,0), 3)
        cv2.imshow("image", self.clone)
        if internal == False:
            cv2.waitKey(2000)
        pass

    def draw_quads(self):
        for i in range(len(self.image_coordinates)):
            self.draw_quad(idx = i)

    def reduce_polygon_to_q(self):
        return cv2_tools.contour_to_quad(self.image_coordinates[-1])

    def get_coords(self):
        return self.image_coordinates

    def get_contour(self):
        return

    def get_image(self):
        return self.clone

    def save_json(self, location: str):
        json.dump(self.annotations, location, sort_keys=True, indent=4)

if __name__ == '__main__':


    for filename in os.listdir(MERCARI_IMAGES):

        f = os.path.join(MERCARI_IMAGES, filename)
        anno_dict= {}
        annotater_widget = Annotater(f)
        key = 113
        while True:
            cv2.imshow('image', annotater_widget.get_image())
            key_ = cv2.waitKey(0)
        # Close program with keyboard 'q'
            print(f'{key}, {key_}')
            if key_ == ord('q') and key_ != key:
                annotater_widget.draw_quad(internal=False)
                coords = annotater_widget.get_coords()
                print(coords)
                cv2.destroyAllWindows()
                break

            key = key_
