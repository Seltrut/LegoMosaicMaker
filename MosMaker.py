import cv2
import numpy as np
import os
from LegoDBHelper import LegoDBHelper
from color_helper import ColorHelper
from panel import Panel
from piece import Piece
import math

pieces_in_order = []
class MosMaker():

    def __init__(self, img, piece_id: int) -> None:
        self.img = img
        self.piece_id = piece_id
        pass

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

## Converts an RGB tuple to a BGR tuple
# def rgb_to_bgr(color):
#     red = color[0]
#     green = color[1]
#     blue = color[2]
#     return (blue, green, red)

## Converts a list of hex codes to a list of BGR color tupes
def hex_to_rgb_list(bricks):
    color_dict = {ColorHelper.hex_to_bgr(brick['HEX_CD']):brick['LEGO_ID'] for brick in bricks}
    colors =  list(color_dict.keys())
    return colors, color_dict

## Converts a single hex code to a BGR tuple
# def hex_to_bgr(hex):
#     rgb =  tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
#     bgr =  rgb_to_bgr(rgb)
#     return bgr

## adds a small dot of the given color to the image at the location (x,y)
## returns the image with a dot
def add_dot(x, y, img, color):
    radius = 10
    diameter = 2 * radius
    color = (int(color[0]), int(color[1]), int(color[2]))
    center_coord = (x * diameter + radius, y * diameter + radius)
    img = cv2.circle(img, center_coord, radius, color, -1)
    return img

## Print out how many pieces of each time are needed and their lego ids, and the dimensions of the mosaic
def print_piece_info():
    #output of how many of each piece is needed
    print(pieces_dict)
    print(sum(pieces_dict.values()))
    print(lego_img.shape)


    print('PIECES IN ORDER')
    for piece in pieces_in_order:
        print(piece)

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
print(type(color_dict))
print('###########################')

filename = 'toonlink'
img = cv2.imread(f'./pics/{filename}.png')

cv2.imshow('celeste', img)


height = img.shape[0]
width  = img.shape[1]
avg_img = np.zeros((height, width, 3), np.uint8)
lego_img = np.zeros((height, width, 3), np.uint8)

interval = 5
color_map = [[0] * int(width / interval)] * int(height/interval)

pieces_dict={}
directions = np.zeros((2000, 2000, 3), np.uint8)

#Stitch together new image
for x in range(0, height, interval):
    for y in range(0,width, interval):
        next_x = x+interval
        next_y = y+interval
        pixel = img[x:next_x, y:next_y]
        lego_color = find_closest_color(colors, np.average(pixel, axis=(0,1)))
        directions = add_dot(int(y/interval), int(x/interval), directions, lego_color)
        print(lego_color)
        color_map[int(x/interval)][int(y/interval)] = color_dict[tuple(lego_color)]
        lego_img[x:next_x, y:next_y] = lego_color
        avg_img[x:next_x, y:next_y] = np.average(pixel, axis=(0,1))

####new stuff
# x_panel_count = int(width / 16 / interval)
# y_panel_count = int(height/ 16 / interval)
# mosaic = [[Panel() for j in x_panel_count] for i in y_panel_count]

# for x in range(0, int(height/interval)):
#     for y in range(0, int(width/interval)):
#         pos_x = x * interval
#         pos_y = y * intervalqui
#         next_x = pos_x+interval
#         next_y = pos_y+interval

#         pixel = img[pos_x:next_x, pos_y:next_y]

#         panel_x = int(x/16)
#         panel_y = int(y/16)
#         piece = Piece(lego_id='GET LEGO ID HERE', color=find_closest_color(colors, np.average(pixel, axis=(0,1))))
#         mosaic[panel_x][panel_y].color_dot(int(x/len(mosaic)), int(y/len(mosaic[0])), piece.color)

#         lego_color = find_closest_color(colors, np.average(pixel, axis=(0,1)))
        # directions = add_dot(int(y/interval), int(x/interval), directions, lego_color)
        # print(lego_color)
        # color_map[int(x/interval)][int(y/interval)] = color_dict[tuple(lego_color)]
        # lego_img[x:next_x, y:next_y] = lego_color
        # avg_img[x:next_x, y:next_y] = np.average(pixel, axis=(0,1))
####### END OF NEW STUFF




#Show the full direction picture
cv2.imshow('directions', directions)
save_direction_pieces(directions, filename)



cv2.imshow('avg', avg_img)
cv2.imshow('lego', lego_img)
print(color_map)
# print(len(color_map))
# for x in range(0, len(color_map)):
#     print(len(color_map[x]))

print_piece_info()
cv2.waitKey(0)