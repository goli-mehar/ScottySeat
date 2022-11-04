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

distance_threshold = 70
mapwidth = 800
mapheight = 500
persepctiveRatio = 230/490
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
    e = ((1-persepctiveRatio) * mapheight)/2
    e = ((mapwidth - y)/mapwidth) * e
    if (x <= e): return (0, y)
    if (x >= (mapheight - e)): return (mapheight, y)
    newx = ((x - e)/(mapheight - 2*e))*mapheight
    f = (mapwidth/(mapwidth - 2*e)) * y
    if (f >= mapwidth): f = mapwidth
    return (newx, f)

@csrf_exempt 
def show_map(request):
    now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    print("Starting Parsing Time =", now)
    my_list = [];
    columns = [] # To store column names
    seatcount = 0
    personcount = 0
    occupied = 0
    seats = []
    person_or_chair = []
    with open('/Users/mink/Documents/b3/scottyseats/data/data.txt') as f:
        lines = f.readlines()
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
        	seatcount += 1
    print(available_or_not)
    room_map = {
        'seatscount': seatcount,
        'personscount': personcount,
        'seatsposition': seats,
        'personorchair':person_or_chair,
        'occupancy':available_or_not,
        'occupied': occupied,
        'available' : seatcount - occupied,
        'w':mapwidth,
        'h':mapheight,
    }
    # allthe = {'room':room_map}
    # global lastresponse
    # lastresponse = allthe
    response_json = json.dumps(room_map)
    # print(room_map)
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
