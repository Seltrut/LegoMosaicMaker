import numpy as np
import cv2
from piece import Piece

class Panel:
    
    def __init__(self) -> None:
        self.__side_len = 16
        side_pixels = self.__side_len * 50
        self.image = np.zeros((side_pixels, side_pixels, 3), np.uint8)
        self.pieces = self.create_blank_panel()
        self.unique_pieces = set()
        pass
    
    def __str__(self) -> str:
        result = ''
        for i in range(self.__side_len):
            for j in range(self.__side_len):
                result += f'{self.pieces[i][j]} / '
            result += '\n'
        return result
    
    def create_blank_panel(self) -> list[list[Piece]]:
        pieces = []
        for i in range(self.__side_len):
            row = []
            for j in range(self.__side_len):
                piece = Piece(lego_id=(i, j), hex_cd='FFFFFF')
                row.append(piece)
                self.image = self.add_dot(i, j, self.image, piece.color)
            pieces.append(row)
        return pieces

    ## Replace the piece at the given (x,y) position
    def add(self, x:int, y:int, piece:Piece) -> None:
        if self.pieces[x][y].get_lego_id() == 0:
            self.pieces[x][y] = piece
            self.image = self.add_dot(x, y, self.image, piece.color)
            # self.unique_pieces.add(piece)

    def add_dot(self, x:int, y:int, img:np.ndarray, color) -> np.ndarray:
        radius = 25
        diameter = 2 * radius
        color = (int(color[0]), int(color[1]), int(color[2]))
        center_coord = (x * diameter + radius, y * diameter + radius)
        img = cv2.circle(img, center_coord, radius, color, -1)
        return img
    
    def color_dot(self, x, y, color) -> None:
        radius = 25
        diameter = 2 * radius
        color = (int(color[0]), int(color[1]), int(color[2]))
        center_coord = (x * diameter + radius, y * diameter + radius)
        self.image = cv2.circle(self.image, center_coord, radius, color, -1)
        self.pieces[x][y].set_color(color)
    

    ## Returns the set of unique pieces
    ## If the set is empty the set is generated from the current pieces on the panel
    def get_unique_pieces(self) -> set[Piece]:
        if not self.unique_pieces:
            for row in self.pieces:
                for col in row:
                    self.unique_pieces.add(col)
        return self.unique_pieces

def test_create_panel_image(p:Panel) -> None:
    cv2.imshow('test',p.image)
    cv2.waitKey(0)
    
if __name__ == "__main__":
    p = Panel()
    d = Piece(23, 'BBAA77')
    p.color_dot(3, 4, d.color)
    print(p.pieces[3][4])
    print(p.pieces[4][4])
    # print(p)
    # p.add(1,7,Piece(lego_id=4, hex_cd='a'))
    # print(p.get_unique_pieces())
    test_create_panel_image(p)




