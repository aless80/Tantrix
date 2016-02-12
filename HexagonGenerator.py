import math
import config as cfg

class HexagonGenerator(object):
    '''Returns a hexagon generator for hexagons of the specified size. odd-q offset'''
    def __init__(self, edge_length):
        self.edge_length = edge_length

    @property
    def col_width(self):
        return self.edge_length * 3

    @property
    def row_height(self):
        return math.sin(math.pi / 3) * self.edge_length

    def __call__(self, row, col, table =0, offset = (0, 0)):
        '''Generator yielding six (I think) x,y coordinates defining the vertices of an hexagon on the main canvas'''
        if table == 0:
            x = offset[0] + row * 0.5 * self.col_width + cfg.HEX_SIZE / 2
            y = offset[1] + (2 * col + (row % 2)) * self.row_height + 2 # +2 is to give some buffer
            #HEX_HEIGHT = math.sin(math.radians(120)) * HEX_SIZE * 2
            #BUFFER = 1
            #YTOP = HEX_HEIGHT + BUFFER
            y -= ((row + 1) % 2) #fix even columns by one pixel
            for angle in range(0, 420, 60):
                x += math.cos(math.radians(angle)) * self.edge_length
                y += math.sin(math.radians(angle)) * self.edge_length
                yield x
                yield y + cfg.HEX_HEIGHT
        elif table == -1:
            x = col * self.col_width
            y = self.row_height * 2
        elif table == -2:
            x = col * self.col_width
            y = self.row_height + cfg.YBOTTOM

    def topleft_pixel(self, row, col):
        print("---")
        x = col * 0.5    * self.col_width+20
        y = (2 * row + (col % 2)) * self.row_height
        #top left pixel
        topleft=(x + math.cos(math.radians(240)) * self.edge_length,
            y + math.sin(math.radians(0)) * self.edge_length)
        return topleft
