class ColorHelper:
    
    def hex_to_bgr(hex_cd):
        # print(hex_cd)
        rgb =  tuple(int(hex_cd[i:i+2], 16) for i in (0, 2, 4))
        bgr =  ColorHelper.rgb_to_bgr(rgb)
        return bgr
    
    def rgb_to_bgr(color):
        red = color[0]
        green = color[1]
        blue = color[2]
        return (blue, green, red)