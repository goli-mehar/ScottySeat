from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone, dateformat
from scottyseats.models import RoomModel
from django.db import transaction
from django.utils import timezone
import random
import json
import time
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
import os
import math
from datetime import datetime
import sys
sys.path.insert(0,'../../ScottySeat/Application')
from main import CV



distance_threshold = 200
mapwidth = 800
mapheight = 500
persepctiveRatio = 250/490
started = False
objmodel = CV()
halfcircleseatratio = 12.5

def get_global_json_dumps_serializer(request):
    room_information = RoomModel.objects.select_for_update().all().filter(roomnumber=request.roomname)[0]
    room_map = {
        'roomname': room_information.roomname,
        'tablecount': room_information.tablecount,
        'seatscount': room_information.seatscount,
        'seatsposition': room_information.seatsposition,
        'tablesposition':room_information.tablesposition,
        'peoplecount': room_information.peoplecount,
        'peopleposition': room_information.peopleposition,
        'occupancy':room_information.occupancy,
    }
    allthe = {'room':room_map}
    global lastresponse
    lastresponse = allthe
    response_json = json.dumps(allthe)
    response = HttpResponse(response_json, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response

def straighten(x, y):
    # return [x,y]
    divideRatio = 1/2
    offsetRatio = 1/4
    top = 300/mapwidth
    bottom = 600/mapwidth
    # divideRatio = 1
    # offsetRatio = 1
    # top = 0
    # bottom = 1
    e = ((1-persepctiveRatio) * mapheight)/2
    mide = (1-divideRatio) * e
    e = ((mapwidth - y)/mapwidth) * e
    f = (mapwidth/(mapwidth - 2*e)) * y
    newf = ((f - top*mapwidth)/((bottom-top)*mapwidth))*mapwidth
    if (newf >= mapwidth): newf = mapwidth
    if (newf <= 0): newf = 0
    ifmid = -1 if (x >= mapheight/2) else 1
    newx = ((x - e)/(mapheight - 2*e))*mapheight + ifmid * mide * offsetRatio
    if (newx <= e): return (0, newf)
    if (newx >= (mapheight - e)): return (mapheight, newf)
    return [newx, newf]

# def straighten(x, y):
#     e = ((1-persepctiveRatio) * mapheight)/2
#     e = ((mapwidth - y)/mapwidth) * e
#     if (x <= e): return (0, y)
#     if (x >= (mapheight - e)): return (mapheight, y)
#     newx = ((x - e)/(mapheight - 2*e))*mapheight
#     f = (mapwidth/(mapwidth - 2*e)) * y
#     if (f >= mapwidth): f = mapwidth
#     return (newx, f)
# def straighten(x, y):
#     divideRatio = 1/2
#     e = ((1-persepctiveRatio) * mapheight)/2
#     mide = ((1-divideRatio)**2) * e
#     e = ((mapwidth - y)/mapwidth) * e
#     f = (mapwidth/(mapwidth - 2*e)) * y
#     if (f >= mapwidth): f = mapwidth
#     ifmid = -1 if (x >= mapheight/2) else 1
#     newx = ((x - e)/(mapheight - 2*e))*mapheight 
#     if (newx <= 0): return (0, f)
#     if (newx >= mapheight): return (mapheight, f)
#     return (newx, f)


@csrf_exempt 
def show_map(request):
    now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    print("Starting Parsing Time =", now)
    #if not started:
        #ob
    objmodel.run()
    my_list = [];
    columns = [] # To store column names
    seatcount = 0
    personcount = 0
    occupied = 0
    seats = []
    person_or_chair = []
    tables = []
    seatts_in_tables = []
    roomlist = []
    with open('../../Scottyseat/b3/scottyseats/data/data.txt') as f:
        lines = f.readlines()
        # for line in lines:
        #     line = line.strip()
        #     temp_seats = line.split(' ')[1:3]
        for line in lines:
            line = line.strip()
            object_id = line.split(' ')[0]
            if object_id == '0' or object_id == '56':
            # columns.append(line.split(' '))
            # print(columns)
                temp_seats = line.split(' ')[1:3]
                # print(temp_seats)
                # print(straighten(float(temp_seats[0])*mapheight, float(temp_seats[1]))*mapwidth)
                seats.append(straighten(float(temp_seats[0])*mapheight, float(temp_seats[1])*mapwidth))
                # seats.append((float(temp_seats[0])*mapheight, float(temp_seats[1])*mapwidth))
                # seats.append(temp_seats)
                person_or_chair.append(object_id)
            if object_id == '60':
                print(line)
                temp_tables = line.split(' ')[1:3]
                four_corners = []
                table_width = line.split(' ')[3]
                table_height = line.split(' ')[4]
                table_left_bottom = straighten((float(temp_tables[0]) - float(table_width)/2)*mapheight, (float(temp_tables[1]) + float(table_height)/2)*mapwidth)
                table_right_top = straighten((float(temp_tables[0]) + float(table_width)/2)*mapheight, (float(temp_tables[1]) - float(table_height)/2)*mapwidth)
                # table_adjust_for_left_bottom = straighten((float(temp_tables[0]) + float(table_width)/2)*mapheight, (float(temp_tables[1]) - float(table_height)/2)*mapwidth)
                table_adjust_for_left_bottom = straighten((float(temp_tables[0]) + float(table_width)/2)*mapheight, (float(temp_tables[1]) + float(table_height)/2)*mapwidth)
                # table_center = straighten(float(temp_tables[0])*mapheight, float(temp_tables[1])*mapwidth)
                print(table_left_bottom)
                print(table_right_top)
                tables.append((table_left_bottom[0], table_left_bottom[1], table_adjust_for_left_bottom[0] - table_left_bottom[0], table_left_bottom[1] - table_right_top[1]))
    print(seats)

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
            print(closest_chair_distance)
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





    # new_item = RoomModel(roomname='defaultroom', tablecount=len(tables), tablesposition=tables, seatsposition=seats, seatscount=seatscount, tablesposition=tables, peoplecount = personcount, occupancy = available_or_not, w = mapwidth, h = mapheight)
    #     roomname     = models.CharField(max_length=15)
    #     tablecount = models.IntegerField()
    #     seatscount = models.IntegerField()
    #     seatsposition = models.TextField()
    #     tablesposition = models.TextField()
    #     peoplecount = models.IntegerField()
    #     peopleposition = models.TextField()
    #     occupancy = models.TextField()
    room_map = {
        'roomname: "wean1101"'
        'seatscount': seatcount,
        'personscount': personcount,
        'seatsposition': seats,
        'personorchair':person_or_chair,
        'occupancy':available_or_not,
        'occupied': occupied,
        'available' : seatcount - occupied,
        'w':mapwidth,
        'h':mapheight,
        'tablesposition':tables,
        'tablecount':len(tables),
    }
    roomlist.append(room_map)
    allthe = {'room':roomlist}
    global lastresponse
    lastresponse = allthe
    response_json = json.dumps(allthe)

    # response_json = json.dumps(room_map)
    print(room_map)
    response = HttpResponse(response_json, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    now1 = datetime.now()
    # current_time1 = now.strftime("%H:%M:%S")
    print("End Parsing Time =", now1)

    return response

def mainmap(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'scottyseats/map.html', context)
    return redirect(reverse('mainmap'))

def listtostr_no_repeats(stringlist):
    liststring = ""
    for t in stringlist:
        if t == stringlist[-1]:
            liststring = liststring + t
        elif t == '':
            continue
        else:
            liststring = liststring + t + ","
    return liststring
