import numpy as np
from color_helper import ColorHelper

## Class for holding piece information
## Feels like I might need to add more data here but we'll see
class Piece():

    def __init__(self, lego_id:int=0, hex_cd:str='FFFFFF', color:np.ndarray = np.array([255, 255, 255])) -> None:
        self.lego_id = lego_id
        self.hex_cd = hex_cd
        self.color = ColorHelper.hex_to_bgr(self.hex_cd)

    def __str__(self) -> str:
        return f'id: {self.lego_id}   color: #{self.hex_cd}     color: {self.color}'
    
    def __eq__(self, __value: object) -> bool:
        return self.lego_id == __value.lego_id and self.hex_cd == __value.hex_cd
    
    def __hash__(self) -> int:
        return hash(self.lego_id)
    
    def get_lego_id(self) -> int:
        return self.lego_id
    
    def get_hex_cd(self) -> str:
        return self.hex_cd
    
    def set_lego_id(self, lego_id:int) -> None:
        self.lego_id = lego_id

    def set_hex_cd(self, hex_cd:str) -> None:
        self.hex_cd = hex_cd

    def set_color(self, color: np.ndarray) -> None:
        self.color = color
        

if __name__ == "__main__":
    p = Piece(1234, 'FFFFFF')
    print(p)
