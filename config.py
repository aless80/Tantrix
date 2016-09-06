import PIL.Image
import math
import random

win = None
canvas = None
wroom = None
wroominstance = None

#SPRITE = PIL.Image.open("./img/tantrix_sprite.png")
import os.path

script_dir = os.path.dirname(os.path.abspath(__file__))
SPRITE  = PIL.Image.open(os.path.join(script_dir, "./img/sprite_smaller.png"))
#SPRITE = PIL.Image.open("./img/sprite_smaller.png")
#SPRITE_WIDTH = 180
#SPRITE_HEIGHT = 156
SPRITE_WIDTH = 2004 / 2
SPRITE_HEIGHT = 1736 / 2

hexagon_generator = None
colors = tuple(['ryybrb','byybrr','yrrbby','rybrby','ryyrbb','yrbybr','rbbyry','ybbryr','rybrby','byyrbr',
                'yrrbyb','brryby','ybbyrr','ryybbr','rggryy','yggyrr','ryygrg','gyyrgr','yrrgyg','grrygy',
                'yggrry','gyygrr','gyyrrg','bggbrr','bggrrb','gbbgrr','grrbgb','rggbbr','brrgbg','rggrbb',
                'yggryr','grygyr','rggyry','rgyryg','ygryrg','bggrbr','rbbgrg','gbbrgr','grbgbr','brgbgr',
                'rggbrb','rbgrgb','yggbby','ybgygb','bggyyb','yggbyb','yggybb','bggbyy','gyygbb','bygbgy',
                'gbygyb','bggyby','byygbg','gyybgb','ybbgyg','gbbygy'])

PLAYERCOLORS = ["red", "blue", "yellow", "green", "#ff8533", "#00E5FF", "#FEF760", "lightgreen"]
playercolor = "red" #TODO: this is needed when no server. Open a dialog instead
opponentcolor = None
gameinprogress = False

COLS = 10
HEX_SIZE = 20 #half width of the bottom side

HEX_HEIGHT = math.sin(math.radians(120)) * HEX_SIZE * 2
HEX_COS = math.cos(math.radians(60)) * HEX_SIZE
HEX_WIDTH = (HEX_SIZE + HEX_COS) * 2
BUFFER = 1
YTOPPL1 = 20
YTOPMAINCANVAS = YTOPPL1 + HEX_HEIGHT + BUFFER
CANVAS_HEIGHT = math.ceil(HEX_HEIGHT * COLS)
YBOTTOMMAINCANVAS = YTOPPL1 + CANVAS_HEIGHT + HEX_HEIGHT * 1.5 - BUFFER * 2 #It ends in the middle of botton tiles!
YBOTTOMPL2 = YBOTTOMMAINCANVAS + HEX_HEIGHT - YTOPPL1
YBOTTOMWINDOW = YBOTTOMMAINCANVAS + HEX_HEIGHT + YTOPPL1


ROWS = int(math.ceil(float(CANVAS_HEIGHT) / HEX_SIZE / 2)) + 1
CANVAS_WIDTH = HEX_COS + (HEX_SIZE * 2 - HEX_COS) * COLS




import Board as bd
board = bd.Board()

TRYING = True
#board = False
deck = False
hand1 = False #TODO I can probably remove hand1 hand2
hand2 = False
turnUpDown = 1
playerIsTabUp = True
scores = [0, 0]
scores_loop = [0, 0]
shifts = [0, 0]

gui_instance = None
gameid = None
player_num = None
name = ""
opponentname = "" #TODO
rndgen = random.Random()


from PodSixNet.Connection import ConnectionListener, connection
connection = connection

connectionID = None   #eg ('127.0.0.1', 35240)
players = []
queue = None
solitaire = False
history = []

