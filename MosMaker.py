import cv2
import numpy as np
import os
from LegoDBHelper import LegoDBHelper
from color_helper import ColorHelper
from panel import Panel
from piece import Piece
import math


pieces_in_order = []

## Determines the closes lego color for the piece available to the given color
def find_closest_color(available_colors, avg_color):
    colors = np.array(available_colors)
    color = np.array(avg_color)
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    key = color_dict[tuple(smallest_distance[0])]
    if key not in pieces_dict:
        pieces_dict[key] = 1
    else:
        pieces_dict[key] = pieces_dict[key] + 1
    pieces_in_order.append(key)
    return smallest_distance[0] 

## Converts a list of hex codes to a list of BGR color tupes
def hex_to_rgb_list(bricks):
    color_dict = {ColorHelper.hex_to_bgr(brick['HEX_CD']):brick['LEGO_ID'] for brick in bricks}
    colors =  list(color_dict.keys())
    return colors, color_dict

## saves the directions when the directions was just one image
@DeprecationWarning
def save_direction_pieces(img, dir_name):
    print('saving pieces')
    pieces = []
    directory = f'./{dir_name} directions'
    if not os.path.exists(directory):
        os.mkdir(directory)
    os.chdir(directory)
    interval = 200 #THis is arbitrary, it
    for i in range(0, img.shape[0], interval):
        for j in range(0,img.shape[1], interval):
            piece = img[i:i+interval, j:j+interval]
            pieces.append(piece)
            cv2.imwrite(f'{dir_name} {int(i/interval)}x{int(j/interval)}.png', piece)

#   Retrieve piece data from the DB
lego_db_helper = LegoDBHelper()
bricks = lego_db_helper.get_by_piece_id(6141)

colors, color_dict = hex_to_rgb_list(bricks)
print('###########################')
print(color_dict)
print('###########################')

filename = 'toonlink'
img = cv2.imread(f'./pics/{filename}.png')

cv2.imshow('celeste', img)


height = img.shape[0]
width  = img.shape[1]

interval = 5
color_map = [[0] * int(width / interval)] * int(height/interval)

pieces_dict={}

####new stuff
x_panel_count = math.ceil(width / 16 / interval)
y_panel_count = math.ceil(height/ 16 / interval)
mosaic = [[Panel() for j in range(x_panel_count)] for i in range(y_panel_count)]


for x in range(0, int(height/interval)):
    for y in range(0, int(width/interval)):
        pos_x = x * interval
        pos_y = y * interval
        next_x = pos_x + interval
        next_y = pos_y + interval

        pixel = img[pos_x:next_x, pos_y:next_y]

        panel_x = int(x/16)
        panel_y = int(y/16)
        piece_color = find_closest_color(colors, np.average(pixel, axis=(0,1)))
        piece_id = color_dict[tuple(piece_color)]
        piece = Piece(lego_id=piece_id, color=piece_color)

        mosaic[panel_x][panel_y].color_dot(y%16, x%16, piece)
####### END OF NEW STUFF

for x in range(len(mosaic)):
    for y in range(len(mosaic[0])):
        mosaic[y][x].display(x, y)
cv2.waitKey(0)