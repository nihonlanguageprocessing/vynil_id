import cv2
import os
import time
import cv2_tools
import numpy as np

MERCARI_IMAGES = 'raw_data/mercari_images'

class Annotater(object):
    def __init__(self, image_path):
        self.original_image = cv2.imread(image_path)
        self.clone = self.original_image.copy()

        window = cv2.namedWindow('image')
        cv2.moveWindow('image', 40,30)
        cv2.setMouseCallback('image', self.extract_coordinates)

        # Bounding box reference points
        self.image_coordinates = []

    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates.append((x,y))
            #print(self.image_coordinates)

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()

    def draw_quad(self):
        if len(self.image_coordinates) > 4:
             self.image_coordinates = np.stack(self.image_coordinates, axis=0).reshape((-1,1,2)).astype(np.int32)
             self.image_coordinates = self.reduce_polygon_to_q()
        ##draw hull on image and show
        else:
            self.image_coordinates = np.stack(self.image_coordinates, axis=0).reshape((-1,1,2)).astype(np.int32)

        cv2.drawContours(self.clone, [self.image_coordinates], 0, (0,255,0), 3)
        cv2.imshow("image", self.clone)
        cv2.waitKey(2000)
        pass

    def reduce_polygon_to_q(self):
        print('hello :)')
        return cv2_tools.contour_to_quad(self.image_coordinates)


    def get_coords(self):
        return self.image_coordinates

    def show_image(self):
        return self.clone



if __name__ == '__main__':


    for filename in os.listdir(MERCARI_IMAGES):
        f = os.path.join(MERCARI_IMAGES, filename)
        annotater_widget = Annotater(f)
        key = 113
        while True:
            cv2.imshow('image', annotater_widget.show_image())
            key_ = cv2.waitKey(0)
        # Close program with keyboard 'q'
            print(f'{key}, {key_}')
            if key_ == ord('q') and key_ != key:
                annotater_widget.draw_quad()
                cv2.waitKey(2000)
                coords = annotater_widget.get_coords()
                print(coords)
                #time.sleep(2)
                cv2.destroyAllWindows()
                break

            key = key_
