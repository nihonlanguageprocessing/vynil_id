import cv2
import os
import time
import cv2_tools
import numpy as np
import json

MERCARI_IMAGES = 'raw_data/mercari_images'
JSON_FILE = 'raw_data/coords.json'

#TO DO
# Save to file
# Only open non annotated files

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
        ## On left click: start clicking (x,y) coordinates
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.clone,(x,y),2,(0,0,255),-1)
            self.image_coordinates[-1].append((x,y))
            cv2.imshow("image",self.clone)


        ## On middle click: draw quad and append those coordinates
        elif event == cv2.EVENT_MBUTTONDOWN:
            self.reshape_to_quad()
            self.draw_quad()
            self.image_coordinates.append([])

        ## On right click: Clear last drawn quad or working quad.
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
        print(self.image_coordinates[idx])
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
        print(self.image_coordinates)
        if len(self.image_coordinates[-1]) == 0:
            self.image_coordinates.pop()

        #new_coords = []
        #for coord in self.image_coordinates:
        #    print(isinstance(coord, list))

        self.image_coordinates = [coord.tolist() for coord in self.image_coordinates if not (isinstance(coord, list))]
        return self.image_coordinates


    def get_contour(self):
        return

    def get_image(self):
        return self.clone

    def save_json(self, location: str):
        json.dump(self.annotations, location, sort_keys=True, indent=4)


def get_json(json_file_path: str) -> json:
    with open(json_file_path, 'r') as json_file:
        try:
            data = json.load(json_file)
        except:
            print('Excepting')
            data = {}
    return data

def update_json(json_file_path: str, old_coords: json) -> None:
    with open(JSON_FILE, 'w') as json_file:

        json.dump(data, json_file, sort_keys=True, indent=2)
    #https://stackoverflow.com/questions/13249415/how-to-implement-custom-indentation-when-pretty-printing-with-the-json-module


if __name__ == '__main__':
    ## Get filenames from the directory that haven't already been reviewed
    data = get_json(JSON_FILE)
    filenames = [filename for filename in os.listdir(MERCARI_IMAGES) if filename not in data.keys()]

    i = 0
    while i < len(filenames):
        path = os.path.join(MERCARI_IMAGES, filenames[i])
        annotater_widget = Annotater(path)
        key = 113 # q
        while True:
            cv2.imshow('image', annotater_widget.get_image())
            key_ = cv2.waitKey(0)

             # Close program with keyboard 'q'
            if key_ == ord('q') and key_ != key:

                coords = annotater_widget.get_coords()
                data.update({filenames[i], coords})
                update_json(JSON_FILE, data)


                cv2.destroyAllWindows()
                break

            key = key_
        i+=1
