import PIL.Image
import math

win = None
canvasmain = None
canvastop = None
canvasbottom = None

SPRITE = PIL.Image.open("./img/tantrix_sprite.png")
SPRITE_WIDTH = 180
SPRITE_HEIGHT = 156

colors = tuple(['ryybrb','byybrr','yrrbby','bgrbrg','rbbryy','yrbybr','rbbyry','ybbryr','rbyryb','byyrbr','yrrbyb','brryby','yrrybb','ryybbr','rggryy','yrrygg','ryygrg','gyyrgr','yrrgyg','grrygy','yggrry','gyygrr','gyyrrg','bggbrr','brrggb','grrgbb','grrbgb','rbbggr','brrgbg','rbbrgg','yggryr','gyrgry','rggyry','rgyryg','yrgygr','bggrbr','rbbgrg','gbbrgr','grbgbr','bgrbrg','rggbrb','rbgrgb','gbbyyg','ybgygb','bggyyb','yggbyb','ybbygg','bggbyy','gyygbb','bgybyg','gybgby','bggyby','byygbg','gyybgb','ybbgyg','gbbygy'])

directions = [[0, 1, -1],[+1,0, -1],[+1, -1,0],[0, -1, 1],[-1,0, 1],[-1, 1,0] ]
PLAYERCOLORS = ["red","blue","yellow","green"]
COLS = 10


HEX_SIZE = 20
HEX_HEIGHT = math.sin(math.radians(120)) * HEX_SIZE * 2
HEX_SIDE = math.cos(math.radians(60)) * HEX_SIZE
#COLS = 10
CANVAS_HEIGHT = math.ceil(HEX_HEIGHT * COLS)
ROWS = int(math.ceil(float(CANVAS_HEIGHT)/HEX_SIZE/2)) + 1
CANVAS_WIDTH = HEX_SIDE+(HEX_SIZE * 2 - HEX_SIDE) * COLS




def isrotation(s1, s2):
     return len(s1)==len(s2) and s1 in 2*s2

def isrot(src, dest):
  # Make sure they have the same size
  #if len(src) != len(dest):
  #  return False
  # Rotate through the letters in src
  for ix in range(len(src)):
    # Compare the end of src with the beginning of dest
    # and the beginning of src with the end of dest
    if dest.startswith(src[ix:]) and dest.endswith(src[:ix]):
      return True
  return False

