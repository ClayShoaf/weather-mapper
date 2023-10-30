import csv
import pygame
from datetime import datetime, timedelta
from Settings import *

# actual coodinates range from 20 to 50 for lat and 130 to 60 for lon
def get_coordinate(slat, slon, elat, elon, lon_min=60, lat_min=20):
    if int(elat) is 0 or int(elon) is 0:
        elat = slat
        elon = slon
    x1 = width - int((-slon - lon_min) * lon_scale)
    y1 = height - int((slat - lat_min) * lat_scale)
    x2 = width - int((-elon - lon_min) * lon_scale)
    y2 = height - int((elat - lat_min) * lat_scale)
    return (x1, y1), (x2, y2)

def read_file():
    with open('/home/user/testpad/Datasets/1950-2022_all_tornadoes.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader, None)
        date, slat, slon, elat, elon = 4, 15, 16, 17, 18
        for line in reader:
            yield line[date], (line[slat], line[slon]), (line[elat], line[elon])

def dict_fill():
    nader_dict = {}
    start_date = datetime(1950, 1, 1)
    end_date = datetime(2022, 12, 31)
    step = timedelta(days=1)
    
    current_date = start_date
    while current_date <= end_date:
        nader_dict[current_date.strftime("%Y-%m-%d")] = []
        current_date += step
    return nader_dict

