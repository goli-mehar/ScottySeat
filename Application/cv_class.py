import cv2, torch,time, sys, json, requests
import numpy as np
import random
import json
import time
import os
import math
from datetime import datetime
import sys
class CV:

    SAMPLES_PER_UPDATE = 5 #How many images will be sampled in each update
    CYCLE_PERIOD = 3 #Time between each image sample
    THR_SAMPLES = 5 #How many images to threshold from after confidence

    def __init__(self):
        self.mapwidth = 800
        self.mapheight = 500
        self.persepctiveRatio = 250/490
        self.model = torch.hub.load('../Model_Development/yolov5', 'custom', path='model_weights.pt', source='local', force_reload=True)
        self.samples = []

        try:
            with open('roomconf.json', 'r') as f:
                room_info = json.loads(f.read())
        except:
            room_info = self.get_room_info()

        self.room_name = room_info["Room"]
        self.server_path = room_info["Server Path"]
        self.camera = cv2.VideoCapture(room_info["Camera Path"], cv2.CAP_AVFOUNDATION)

    def get_room_info(self):

        print("Room Configuration File Not Found")
        print("Making new file now")

        room_info = dict()

        while True:
            room_info["Room"] = input("Enter Room Name: ")
            if input("Is the Room Correct (Y/N)?") == 'Y': break

        while True:
            room_info["Camera Path"] = int(input("Enter Camera Path: "))
            if input("Is the Camera Path Correct (Y/N)?") == 'Y': break
        
        while True:
            room_info["Server Path"] = input("Enter Server Web Address: ")
            if input("Is the Server Path Correct (Y/N)?") == 'Y': break

        with open("roomconf.json", "w") as outf: 
            outf.write(json.dumps(room_info))

        print("room/server info to 'roomconf.json', Any further changes can be made directly to file")

        return room_info


    def preprocess(self, img):
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        img = clahe.apply(img)

        #img = cv.convertScaleAbs(img, alpha=alpha, beta=beta)
        #img = cv.fastNlMeansDenoising(img,None,5,10,7,21)

        return img

    def get_highest_confidence_image(self):


        #top 5 with highest confidence averges in image
        #take objects with greater than 70% confidence
        #if an object overlaps more than 50% onoy tke the higher confidnece object
        return self.samples[0]

    def straighten(self, x, y):
        divideRatio = self.persepctiveRatio
        offsetRatio = 1/4
        top = 300/self.mapwidth
        bottom = 750/self.mapwidth
        # divideRatio = 1
        # offsetRatio = 1
        # top = 0
        # bottom = 1
        e = ((1-self.persepctiveRatio) * self.mapheight)/2
        mide = (1-divideRatio) * e
        e = ((self.mapwidth - y)/self.mapwidth) * e
        f = (self.mapwidth/(self.mapwidth - 2*e)) * y
        newf = ((f - top*self.mapwidth)/((bottom-top)*self.mapwidth))*self.mapwidth
        if (newf >= self.mapwidth): newf = self.mapwidth
        if (newf <= 0): newf = 0
        ifmid = -1 if (x >= self.mapheight/2) else 1
        newx = ((x - e)/(self.mapheight - 2*e))*self.mapheight + ifmid * mide * offsetRatio
        if (newx <= e): return (0, newf)
        if (newx >= (self.mapheight - e)): return (self.mapheight, newf)
        return [newx, newf]

    def calculate_occupancy(self, sample):
        my_list = []
        columns = [] # To store column names
        seatcount = 0
        personcount = 0
        occupied = 0
        seats = []
        person_or_chair = []
        tables = []
        seatts_in_tables = []
        roomlist = []
        for obj in sample:
            object_id = obj[0]
            if object_id == '2' or object_id == '0':
                temp_seats = obj[1:3]
                # print(temp_seats)
                # print(self.straighten(float(temp_seats[0])*self.mapheight, float(temp_seats[1]))*self.mapwidth)
                seats.append(self.straighten(float(temp_seats[0])*self.mapheight, float(temp_seats[1])*self.mapwidth))
                # seats.append((float(temp_seats[0])*self.mapheight, float(temp_seats[1])*self.mapwidth))
                # seats.append(temp_seats)
                person_or_chair.append(object_id)
            if object_id == '1':
                # print(line)
                temp_tables = obj[1:3]
                four_corners = []
                table_width = obj[3]
                table_height = obj[4]
                table_left_bottom = self.straighten((float(temp_tables[0]) - float(table_width)/2)*self.mapheight, (float(temp_tables[1]) + float(table_height)/2)*self.mapwidth)
                table_right_top = self.straighten((float(temp_tables[0]) + float(table_width)/2)*self.mapheight, (float(temp_tables[1]) - float(table_height)/2)*self.mapwidth)
                # table_adjust_for_left_bottom = self.straighten((float(temp_tables[0]) + float(table_width)/2)*self.mapheight, (float(temp_tables[1]) - float(table_height)/2)*self.mapwidth)
                table_adjust_for_left_bottom = self.straighten((float(temp_tables[0]) + float(table_width)/2)*self.mapheight, (float(temp_tables[1]) + float(table_height)/2)*self.mapwidth)
                # table_center = self.straighten(float(temp_tables[0])*self.mapheight, float(temp_tables[1])*self.mapwidth)
                # print(table_left_bottom)
                # print(table_right_top)
                tables.append((table_left_bottom[0], table_left_bottom[1], table_adjust_for_left_bottom[0] - table_left_bottom[0], table_left_bottom[1] - table_right_top[1]))

        available_or_not = [True]*len(seats)
        # calculate distance and availablity
        for j in range(len(seats)):
            if person_or_chair[j] == '0':
                personcount += 1
                closest_chair_index = -1
                closest_chair_distance = float(math.inf)
                for k in range(len(seats)):
                    if person_or_chair[k] == '56' and available_or_not[k]:
                        distance = math.hypot(float(seats[k][0]) - float(seats[j][0]), float(seats[k][1]) - float(seats[j][1]))
                        if distance < closest_chair_distance:
                            closest_chair_distance = distance
                            closest_chair_index = k
                if closest_chair_distance <= distance_threshold:
                    available_or_not[closest_chair_index] = False
                    occupied += 1
                # print(closest_chair_distance)
            else:
                #check if the seat is in a table
                seatcount += 1
        for t in tables:
            in_the_table = []
            lowest_y = 0
            highest_y = float(math.inf)
            lowest_x = 0
            highest_x = float(math.inf)
            for s in range(len(seats)):
                if person_or_chair[s] == '56':
                    if seats[s][0] > t[0] and seats[s][0] < (t[2] + t[0]) and seats[s][1] < t[1] and seats[s][1] > (t[1] - t[-1]):
                        indexes = [seats[s][0] - t[0], (t[2] + t[0]) - seats[s][0],  t[1] - seats[s][1], seats[s][1] - (t[1] - t[-1])]
                        bounding = [t[0], (t[2] + t[0]), t[1], (t[1] - t[-1])]
                        minindice = indexes.index(min(indexes))
                        if minindice < 2:
                            seats[s][0] = bounding[minindice]
                        else:
                            seats[s][1] = bounding[minindice]
        room_map = {
            'seatscount': seatcount,
            'personscount': personcount,
            'seatsposition': seats,
            'personorchair':person_or_chair,#labels of the items, 
            #it's named personorchair because its named before we had a table
            'occupancy':available_or_not,
            'occupied': occupied,
            'available' : seatcount - occupied,
            'w':self.mapwidth,
            #given the self.mapwidth and height by the server so that the map will re-adjust
            # every update even if the user tried to change it on the client side
            'h':self.mapheight,
            'tablesposition':tables,
            'tablecount':len(tables),
        }
        single_room = {'Room' : self.room_name,
                       'Results' : room_map,}
        return single_room

    def convert_xyxytoxywh(self, sample, img_dim):

        results = sample.pandas().xyxy[0].values
        height, width = img_dim
        results = [res for res in results]

        adj_results = []
        for obj in reversed(results):
            cl = obj[-2]
            x1, y1, x2, y2 = obj[0:4]

            x_w = np.abs(x2-x1); y_h = np.abs(y2-y1)

            x_c = np.minimum(x1, x2) + x_w/2; y_c = np.minimum(y1, y2) + y_h/2

            x_w /= width; x_c /= width
            y_c /= height; y_h /= height

            adj_results += [[cl, x_c, y_c, x_w, y_h]]

        return adj_results

    def to_json(self, occupancy):
        pass

    def send_to_server(self, occupancy):

        json_obj = occupancy
        requests.post(url=self.server_path, json=json_obj)
