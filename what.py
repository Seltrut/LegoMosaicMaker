import rebrick
import json
import sqlite3
import numpy as np
import math

if __name__ == "__main__":
   x = math.ceil(3.4)
   print(x)
   print(type(x))
#    API_KEY = "9ae6321fbe86b420e884560f124ce1bd"
#    # piece_id = 98138 # 98138 is flat dots
#    # piece_id = 85861 # 85861 us dots that can still connect with hole?
#    piece_id = 6141 # 85861 us dots that can still connect

#    rebrick.init(API_KEY)


# #    response = rebrick.lego.get_part_colors(piece_id)
# #    response = rebrick.lego.get_part(614125)
#    response = rebrick.lego.get_part_color(part_id=piece_id, color_id=1055)
#    result = json.loads(response.read())
#    print(result)
#    # # #print out elements
# #    for res in result['results']:
# #       print(res)
