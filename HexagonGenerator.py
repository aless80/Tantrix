import math
from config import * #todo

class HexagonGenerator(object):
    """Returns a hexagon generator for hexagons of the specified size. odd-q offset"""
    def __init__(self, edge_length):
        self.edge_length = edge_length
    @property
    def col_width(self):
        return self.edge_length * 3
    @property
    def row_height(self):
        return math.sin(math.pi / 3) * self.edge_length
    def __call__(self, row, col, offset=(0,0)):
        x = offset[0] + col * 0.5    * self.col_width + HEX_SIZE / 2
        y = offset[1] + (2 * row + (col % 2)) * self.row_height
        y -= 1 * ((col + 1) % 2) #fix even columns by one pixel
        for angle in range(0, 420, 60):
            x += math.cos(math.radians(angle)) * self.edge_length
            y += math.sin(math.radians(angle)) * self.edge_length
            yield x
            yield y
    def topleft_pixel(self, row, col):
        print("---")
        x = col * 0.5    * self.col_width+20
        y = (2 * row + (col % 2)) * self.row_height
        #top left pixel
        topleft=(x + math.cos(math.radians(240)) * self.edge_length,
            y + math.sin(math.radians(0)) * self.edge_length)
        return topleft



def isrotation(s1, s2):
         return len(s1)==len(s2) and s1 in 2*s2

def isrot(src, dest):
    # Make sure they have the same size
    #if len(src) != len(dest):
    #    return False
    # Rotate through the letters in src
    for ix in range(len(src)):
        # Compare the end of src with the beginning of dest
        # and the beginning of src with the end of dest
        if dest.startswith(src[ix:]) and dest.endswith(src[:ix]):
            return True
    return False