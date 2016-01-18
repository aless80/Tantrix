"""
install python-dev
sudo apt-get install python3-pil
sudo apt-get install python3-imaging-tk

http://variable-scope.com/posts/hexagon-tilings-with-python
http://www.raywenderlich.com/1223/python-tutorial-how-to-generate-game-deck-
with-python-imaging-library

http://www.redblobgames.com/grids/hexagons/
"""
import math
import PIL.Image, PIL.ImageTk
#import aggdraw.Draw, aggdraw.Brush, aggdraw.Pen
try:
  import Tkinter as tk # for Python2
except:
  import tkinter as tk # for Python3
import random


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
    x = offset[0] + col * 0.5  * self.col_width + HEX_SIZE / 2
    y = offset[1] + (2 * row + (col % 2)) * self.row_height
    y -= 1 * ((col + 1) % 2) #fix even columns by one pixel
    for angle in range(0, 420, 60):
      x += math.cos(math.radians(angle)) * self.edge_length
      y += math.sin(math.radians(angle)) * self.edge_length
      yield x
      yield y
  def topleft_pixel(self, row, col):
    print("---")
    x = col * 0.5  * self.col_width+20
    y = (2 * row + (col % 2)) * self.row_height
    #top left pixel
    topleft=(x + math.cos(math.radians(240)) * self.edge_length,
      y + math.sin(math.radians(0)) * self.edge_length)
    return topleft



class Board(object):
  def pixel_to_off_canvastopbottom(self, x, y):
    col = math.floor(float(x) / (HEX_SIZE * 2))
    return (0, col)
  def pixel_to_off(self,x, y):
    q = x * 2/3 / HEX_SIZE
    r = (-x / 3 + math.sqrt(3)/3 * y) / HEX_SIZE
    #print("self.cube_round in cube= " +str(self.cube_round((q, -q-r, r))))
    cube = (q, -q-r, r)
    cuberound = self.cube_round(cube)
    offset = self.cube_to_off(cuberound)
    return offset
  def pixel_to_hex(self, x, y):
    q = x * 2/3 / HEX_SIZE
    r = (-x / 3 + math.sqrt(3)/3 * y) / HEX_SIZE
    #print("self.cube_round in cube= " +str(self.cube_round((q, -q-r, r))))
    return self.hex_round((q, r))
    #return self.cube_to_hex(self.cube_round((q, -q-r, r)))
  def hex_round(self, hex):
    return self.cube_to_hex(self.cube_round(self.hex_to_cube(hex)))
  def cube_to_off(self,cube):
    """Convert cube to odd-q offset"""
    row = cube[0]
    col = cube[2] + (cube[0] - (cube[0]%2)) / 2
    return (row, col)
  def off_to_cube(self, row, col):
    # convert odd-q offset to cube
    x = row
    z = col - (x - (x%2)) / 2
    y = -x-z
    return (x,y,z)
  def cube_to_hex(self, hex):
    """Convert cube coordinates to axial"""
    q = hex[0]
    r = hex[1]
    return (q, r)
  def hex_to_cube(self, h): # axial
      x = h[1]
      z = h[0]
      y = -x-z
      return (x, y, z) #return Cube(x, y, z)
  def cube_round(self, h):
      rx = round(h[0])
      ry = round(h[1])
      rz = round(h[2])
      x_diff = abs(rx - h[0])
      y_diff = abs(ry - h[1])
      z_diff = abs(rz - h[2])
      if x_diff > y_diff and x_diff > z_diff:
          rx = -ry-rz
      elif y_diff > z_diff:
          ry = -rx-rz
      else:
          rz = -rx-ry
      return ((rx, ry, rz)) #return (Cube(rx, ry, rz))
  def __init__(self):
    global win, canvasmain, canvastop, canvasbottom, hexagon_generator, board, deck
    global btn1, btn2, btnTry, btnConf
    win = tk.Tk()
    canvasmain = tk.Canvas(win, height= CANVAS_HEIGHT, width = CANVAS_WIDTH, background='lightgrey', name="canvasmain")
    canvastop = tk.Canvas(win, height= HEX_HEIGHT, width = CANVAS_WIDTH, background='lightgrey',name="canvastop")
    canvasbottom = tk.Canvas(win, height= HEX_HEIGHT, width = CANVAS_WIDTH, background='lightgrey',name="canvasbottom")
    w = CANVAS_WIDTH + 5
    h = CANVAS_HEIGHT + HEX_HEIGHT * 2 + 5
    ws = win.winfo_screenwidth()    #width of the screen
    hs = win.winfo_screenheight()       #height of the screen
    x = ws - w / 2; y = hs - h / 2    #x and y coord for the Tk root window
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #Create hexagons on main canvas
    hexagon_generator = HexagonGenerator(HEX_SIZE)
    for row in range(ROWS):
      for col in range(COLS):
        pts = list(hexagon_generator(row, col))
        canvasmain.create_line(pts, width =2)
    #Append canvases
    canvastop.grid(row = 0, column = 0)#,expand="-in")
    canvasmain.grid(row = 1, column = 0, rowspan = 5)#,expand="-ipadx")
    canvasbottom.grid(row = 6, column = 0)#,expand="-padx")
    #Button1
    btn1 = tk.Button(win, text="Refill\nhand",  bg="yellow", padx=5, name = "btn1")
    #Add canvastop to tags, so button click will be processed by canvastop!
    #bindtags = list(btn1.bindtags())
    #bindtags.insert(1, canvastop)
    #btn1.bindtags(tuple(bindtags))
    btn1.bind('<ButtonRelease-1>',buttonClick)
    btn1.grid(row=0, column=1,columnspan=1)
    #Button2
    btn2 = tk.Button(win, text="Refill\nhand",  bg="red",
                   padx=5, name = "btn2") #, height=int(round(HEX_HEIGHT))-1
    #Add canvasbpttom to tags, so button click will be processed by canvasbottom!
    #bindtags = list(btn1.bindtags())
    #bindtags.insert(1, canvasbottom)
    #btn2.bindtags(tuple(bindtags))
    btn2.bind('<ButtonRelease-1>',buttonClick)
    btn2.grid(row=6, column=1,columnspan=1)
    #Confirm button
    btnConf = tk.Button(win, text="Confirm\nmove",  bg="cyan",
                      padx=5, name = "btnConf")
    #bindtags = list(btnConf.bindtags())
    #bindtags.insert(1, canvasmain)
    #btnConf.bindtags(tuple(bindtags))
    btnConf.bind('<ButtonRelease-1>',buttonClick)
    btnConf.grid(row=2, column=1,columnspan=1)
    #.. button
    btnTry = tk.Button(win, text="Try\nthings",  bg="grey", padx=5, name = "btnTry")
    #bindtags = list(btnConf.bindtags())
    #bindtags.insert(1, canvasmain)
    #btnTry.bindtags(tuple(bindtags))
    btnTry.bind('<ButtonRelease-1>',buttonClick)
    btnTry.grid(row=3, column=1,columnspan=1)
    #btnTry(state="disabled")
    #Update window
    win.update()
    wh=win.winfo_height() #update before asking size!
    win.geometry(str(canvasmain.winfo_width() + 100) + "x" + str(int(round(CANVAS_HEIGHT + 2 * HEX_HEIGHT))))
    win.update()
  def get_neighbors(self, row, col=False):
    """Find neighbors of a hexagon in the main canvas"""
    if type(row) == list or type(row) == tuple:
      row, col,bin = row
    row, col = int(row),int(col)
    #Convert to cube coordinates, then add directions to cube coordinate
    neigh = []
    cube = list(self.off_to_cube(row, col))
    for dir in directions:
      c = map(lambda x, y : x + y, cube, dir)
      off = self.cube_to_off(c)
      #Get rowcolcanv
      rowcolcanv = off
      rowcolcanv += (".canvasmain",)
      #Find if there is a tile on rowcolcanv
      ind = deck.get_index_from_rowcolcanv(rowcolcanv)
      if ind is not None:
        neigh.append(ind)
    return neigh #list of ind where tile is present [(0,0),..]
  def get_neighboring_colors(self, row, col = False):
    """Return the neighboring colors as a list of (color,ind)"""
    if type(row) != int:
      row, col,bin = row
    neigh = self.get_neighbors(row, col) #[(0,0),..]
    color_dirindex_neighIndex = []
    if len(neigh) > 0:
      for n in neigh:   #(0,0)
        wholecolor = deck.tiles[n].color
        #here get direction and right color
        rowcolcanv = deck.positions[n]
        cube = self.off_to_cube(rowcolcanv[0],rowcolcanv[1])
        home = board.off_to_cube(row, col)
        founddir = map(lambda dest, hom : dest-hom,cube,home)
        dirindex = directions.index(founddir)
        color = wholecolor[(dirindex + 3) % 6]
        color_dirindex_neighIndex.append(tuple([color,dirindex,n]))
    return color_dirindex_neighIndex #[('b',1),('color',directionIndex),]


class Deck(object):
  def __init__(self):
    self.tiles = []       #this contains tile in PhotoImage format
    self.positions = []   #(row, col,str(canvas))
    self.itemids = []     #itemid= canvas.create_image()
    self.undealt =range(1, 57) #1:56
    self.dealt = [] #1:56
  def get_index_from_tile_number(self, num):
    return self.dealt.index(num)
  def get_index_from_rowcolcanv(self, rowcolcanv):
    try:
      return self.positions.index(tuple(rowcolcanv))
    except:
      return None
  def get_tile_number_from_rowcolcanv(self, rowcolcanv):
    pass #self.getTileNumberFromIndex(self.get_index_from_rowcolcanv(rowcolcanv))
  def get_tile_number_from_index(self, ind):
    pass #self.dealt[ind]
    
  def remove(self, row, col, canvas):
    ind = self.get_index_from_rowcolcanv((row, col, str(canvas)))
    itemid = self.itemids[ind]
    #Delete it
    canvas.delete(itemid)
    #Update properties
    pos = self.positions.pop(ind)
    tile = self.tiles.pop(ind)
    self.itemids.pop(ind)
    #NB: remove tile from deck dealt. leaving undealt as is
    num = deck.dealt.pop(ind)
    return (pos,num,tile)
  def is_occupied(self, rowcolcanv):
    """Return whether an hexagon is already occupied:
    deck.isOccupied(rowcolcanv)    """
    return rowcolcanv in self.positions
  def movable(self, row1, col1, canvas1, row2, col2, canvas2):
    if TRYING:
      return True
    #Ignore movement when:
    if self.is_occupied((row2, col2, str(canvas2))):
      #Return False if destination is already occupied
      print('Destination tile is occupied: ' + str((row2, col2, str(canvas2))))
      return False
    if canvas2 == canvasmain:
      #Movement to main canvas.
      #Ok if there are no tiles on canvas
      if ".canvasmain" not in [p[2] for p in self.positions]: #todo: later on maybe check score
                                # or something that is populated when the first tile is placed
        return True
      #Check if tile matches colors
      ind1 = self.get_index_from_rowcolcanv((row1, col1, str(canvas1)))
      tile = deck.tiles[ind1]
      #NB The following does not allow you to move the same tile one position away.
      #That should not be of any use though so ok
      ok = tile.tile_match_colors(tuple([row2, col2, str(canvas2)]))
      if not ok:
        print('No color matching')
        return ok
    elif canvas1 != canvasmain and canvas1 != canvas2:
      #Return False if trying to move from bottom to top or vice versa
      print('trying to move from bottom to top or vice versa')
      return False
    elif canvas1 == canvasmain and canvas2 != canvasmain:
      #Return False if trying to move from canvasmain to top or bottom
      print('trying to move from canvasmain to top or bottom')
      return False
    return True

  def move(self, row1, col1, canvas1, row2, col2, canvas2):
    if not self.movable(row1, col1, canvas1, row2, col2, canvas2):
      print("You cannot move the tile as it is to this hexagon")
      return 0
    #Remove tile. properties get updated
    (posold,num,tile)= self.remove(row1,col1,canvas1)
    #Place tile on new place
    itemid = tile.place(row2,col2,canvas2,tile.tile)
    #Update storage
    self.tiles.append(tile)
    self.positions.append((row2,col2,str(canvas2)))
    self.itemids.append(itemid)
    deck.dealt.append(num)
    #Update window
    win.update()
    return 1
  def rotate(self, rowcolcanv):
    global win
    #Find the index
    try:
      ind= self.get_index_from_rowcolcanv(tuple(rowcolcanv))
      print('found at ' + str(ind))
    except:
      print('not found: ' + str(rowcolcanv) +' in')
      print(self.positions)
      return
    #Check if color would match
    if str(rowcolcanv[2]) == ".canvasmain":
      if not self.tiles[ind].tile_match_colors(rowcolcanv, -60):
        print("You cannot rotate the tile")
        return
    #Spawn the rotated tile
    tile = Tile(self.dealt[ind], self.tiles[ind].angle-60)
    #Update tiles list
    self.tiles[ind] = tile
    #Place the tile
    canvas = win.children[rowcolcanv[2][1:]]
    itemid = tile.place(rowcolcanv[0],rowcolcanv[1],canvas,tile.tile)
    self.itemids[ind] = itemid
    print(tile)
  def deal(self, row, col, canv, num='random'):
    #Random tile if num is not set
    if num =='random':
      ran = random.randrange(0, len(self.undealt)) #0:55
    num= self.undealt.pop(ran)   #1:56
    #Get tile as PhotoImage
    tileobj = Tile(num)
    tile = tileobj.tile
    #Store tile instance
    self.tiles.append(tileobj)
    #Place on canvas
    itemid = tileobj.place(row, col,canv,tile)
    #print('itemid=' + str(itemid))
    self.itemids.append(itemid)
    #store dealt/undealt tile numbers
    self.dealt.append(num)
    self.positions.append((row, col,str(canv)))
  def get_tiles_in_deck(self, canvas):
    count = 0
    row = []
    col = []
    for pos in self.positions:
      r, q, c = pos
      if str(c) == str(canvas):
        row.append(r)
        col.append(q)
        count +=1
    yield count
    yield row
    yield col


  def refill_deck(self, canv):
    #Check how many tiles there are
    count, row, col = self.get_tiles_in_deck(canv)
    if count == 6:
      return 0
    #Flush existing tiles to left
    for i in range(0, len(col)):
      if col[i] > i:
        deck.move(0, col[i], canv, 0, i, canv)
    #Refill deck
    for i in range(count, 6):
      self.deal(0, i, canv)
    return 1

class Tile(object):
  def __init__(self, num, angle=0):
    """tile object containing a tile in PhotoImage format"""
    global board
    #tile is a PhotoImage (required by Canvas' create_image) and its number
    tilePIL = SPRITE.crop((SPRITE_WIDTH * (num - 1), 4,
           SPRITE_WIDTH * num - 2,SPRITE_HEIGHT)).resize((HEX_SIZE * 2, int(HEX_HEIGHT)))
    if angle != 0:
      tilePIL = tilePIL.rotate(angle, expand = 0)
    self.tile = PIL.ImageTk.PhotoImage(tilePIL)
    self.color = colors[num-1]
    self.angle = angle
  def __str__(self):
    return 'tile color and angle: ' +self.getColor() +' ' + str(self.angle) +' '
  def getColor(self):
    basecolor = self.color
    n = self.angle/60
    return basecolor[n:] + basecolor[:n]

  def tile_match_colors(self, rowcolcanv, angle=0):
    #No color matching when user is trying things
    if TRYING == True:
      print("TRYING is True, so no color check")
      return True
    #Get neighboring colors
    neighcolors = board.get_neighboring_colors(rowcolcanv)
    #Angle
    basecolor = self.getColor()
    n = angle/60
    tilecolor = basecolor[n:] + basecolor[:n]
    for nc in neighcolors:
      if tilecolor[nc[1]] != nc[0]:
        print("neighbors: " + str(board.get_neighbors(rowcolcanv)))
        print("tilecolor = " + str(tilecolor) + " " + str(nc[1]) + " " + nc[0])
        #NB cannot move tile one tile away because current tile is present. I do not see any case in which that is what i want
        return False
    return True

  def tile_pixels(self, row, col, canv):
    """Given row, col and canvas, return the pixel coordinates of the center
    of the corresponding hexagon

    if canvas.find_withtag(tk.CURRENT):
        #canvas.itemconfig(tk.CURRENT, fill="blue")
        canvas.update_idletasks()
        canvas.after(200)
        canvas.itemconfig(CURRENT, fill="red")
        """
    #I need the coordinates on the canvas
    if str(canv) == ".canvasmain":
      x = HEX_SIZE + (HEX_SIZE  + HEX_SIDE) * row
      y = HEX_HEIGHT / 2 + HEX_HEIGHT * col + HEX_HEIGHT / 2 * (row % 2)
    else: #bottom or top canvases
      x = HEX_SIZE + ((HEX_SIZE * 2) * col)
      y = HEX_HEIGHT / 2
    yield x
    yield y

  def place(self, row, col, canv,tile):
    """Place image from tile instance on canvas. No update .positions. Return the itemid."""
    #Get the pixels
    tilex,tiley = self.tile_pixels(row, col, canv)
    itemid = canv.create_image(tilex, tiley, image = tile)
    #Update positions - not needed!
    #Update window
    win.update()
    return itemid


class Hand(object):
  def __init__(self,canv):
    #Choose a color for the player
    avail_colors = PLAYERCOLORS
    ran = random.randrange(0, len(PLAYERCOLORS))
    self.playercolor = PLAYERCOLORS.pop(ran)
    #todo Color the corresponding button
    self.playercolor

    for i in range(0, 6): #todo maybe use the new refill_deck
      deck.deal(0, i, canv)
  def refill(self, canv):
    pass


PLAYERCOLORS = ["red","blue","yellow","green"]
TRYING = False
SPRITE = PIL.Image.open("./img/tantrix_sprite.png")
SPRITE_WIDTH = 180
SPRITE_HEIGHT = 156

HEX_SIZE = 30
HEX_HEIGHT = math.sin(math.radians(120)) * HEX_SIZE * 2
HEX_SIDE = math.cos(math.radians(60)) * HEX_SIZE
COLS = 10
CANVAS_HEIGHT = HEX_HEIGHT * COLS
ROWS = int(math.ceil(float(CANVAS_HEIGHT)/HEX_SIZE/2)) + 1
CANVAS_WIDTH = HEX_SIDE+(HEX_SIZE * 2 - HEX_SIDE) * COLS

#old ones
#CANVAS_WIDTH=HEX_SIDE+(HEX_SIZE * 2 - HEX_SIDE) * 8
#CANVAS_HEIGHT=HEX_HEIGHT * 6
#ROWS=int(math.ceil(float(CANVAS_HEIGHT)/HEX_SIZE/2))+1
#COLS=12


colors = tuple(['ryybrb','byybrr','yrrbby','bgrbrg','rbbryy','yrbybr','rbbyry','ybbryr','rbyryb','byyrbr','yrrbyb','brryby','yrrybb','ryybbr','rggryy','yrrygg','ryygrg','gyyrgr','yrrgyg','grrygy','yggrry','gyygrr','gyyrrg','bggbrr','brrggb','grrgbb','grrbgb','rbbggr','brrgbg','rbbrgg','yggryr','gyrgry','rggyry','rgyryg','yrgygr','bggrbr','rbbgrg','gbbrgr','grbgbr','bgrbrg','rggbrb','rbgrgb','gbbyyg','ybgygb','bggyyb','yggbyb','ybbygg','bggbyy','gyygbb','bgybyg','gybgby','bggyby','byygbg','gyybgb','ybbgyg','gbbygy'])
directions = [[0, 1, -1],[+1,0, -1],[+1, -1,0],[0, -1, 1],[-1,0, 1],[-1, 1,0] ]
hexagon_generator = False
win = False
canvasmain = False
canvastop = False
canvasbottom = False
board = False
deck = False
hand1 = False
hand2 = False
clicked_rowcolcanv = None

btnTry = False

def main():
  global win, canvasmain, hexagon_generator, canvastop, canvasbottom, board, deck
  board = Board()
  #Deal deck
  deck = Deck()
  hand1 = Hand(canvastop)
  hand2 = Hand(canvasbottom)
  #Check for duplicates. It should never happen
  dupl = set([x for x in deck.dealt if deck.dealt.count(x) > 1])
  if len(dupl) > 0:
    raise UserWarning("Duplicates in deck.dealt!!!")
  #Bindings
  canvasmain.bind('<ButtonPress-1>', clickCallback) #type 4
  #<Double-Button-1>?
  canvastop.bind('<ButtonPress-1>', clickCallback) #type 4
  canvasbottom.bind('<ButtonPress-1>', clickCallback) #type 4
  canvasmain.bind('<B1-Motion>', clickCallback) #drag
  canvastop.bind('<B1-Motion>', clickCallback) #drag
  canvasbottom.bind('<B1-Motion>', clickCallback) #drag
  canvasmain.bind('<ButtonRelease-1>', clickCallback) #release
  canvastop.bind('<ButtonRelease-1>', clickCallback) #release
  canvasbottom.bind('<ButtonRelease-1>', clickCallback) #release
  canvasmain.bind('<ButtonPress-3>', clickB3Callback)
  #canvas.bind('<Return>', clickCallback)
  #canvas.bind('<Key>', clickCallback)
  #canvas.bind('<MouseWheel>', wheel)
  win.mainloop()


def print_event(event, msg= ' '):
  print(msg)
  x, y = event.x, event.y
  hex = board.pixel_to_hex(x,y)
  cube = board.pixel_to_off(x, y)
  print('cube (if in canvasmain!) = ' + str(cube))
  print('hex = ' + str(hex))
  rowcolcanv=onClickRelease(event)
  neigh= board.get_neighbors(rowcolcanv)
  print('neigh = ' + str(neigh))
  neighcolors = board.get_neighboring_colors(rowcolcanv)
  print('neighcolors = ' + str(neighcolors))

def buttonClick(event):
  print('buttonClick')
  #Buttons
  if event.widget._name[0:3] == "btn":
    if event.state == 272:  #release click
      if event.widget._name == "btn1":
        deck.refill_deck(canvastop)
      elif event.widget._name == "btn2":
        deck.refill_deck(canvasbottom)
      elif event.widget._name == "btnConf":
        print("Confirmed! todo")
        pass
      elif event.widget._name == "btnTry":
        global TRYING
        TRYING = not TRYING
        clr={False:"grey", True:"cyan"}
        btnTry.configure(background = clr[TRYING])
        print('widget = ' + str(event.widget))
        print("TRYING = " + str(TRYING))
    return

def clickEmptyHexagon(event):
  print_event(event,' \nclickEmptyHexagon')

def clickB3Callback(event):
  print_event(event, ' \nclickB3Callback')

def clickCallback(event):
  print('\nclickCallback')
  global clicked_rowcolcanv
  x, y = event.x, event.y
  #logs
  if 0:
    print(' widget = ' + str(event.widget))
    print(' type = ' + str(event.type))
    print(' state = ' + str(event.state))
    print(' num = ' + str(event.num))
    print(' delta =' + str(event.delta))
    print('x, y = {}, {}'.format(x, y))
    print(" x_root, y_root = ",str((event.x_root, event.y_root)))
  #with this I change to the canvas' coordinates: x = canvas.canvasx(event.x)
  #print canvas.find_closest(x, y)
  #http://epydoc.sourceforge.net/stdlib/Tkinter.Event-class.html
  #NB: move while dragging is type=6 (clickCallback) state=272
  #NB: click                  type=4 (BPress) state=16
  #NB: release click          type=5 (BRelea) state=272
  #
  if event.type == '4' and event.state == 16: #click
    rowcolcanv=onClickRelease(event)
    ind = deck.get_index_from_rowcolcanv(rowcolcanv)
    if ind is None:
      clicked_rowcolcanv = None
      return
    clicked_rowcolcanv = rowcolcanv
    #wait ..
  elif event.type == '5' and event.state == 272: #release click
    #previously clicked on empty hexagon
    if clicked_rowcolcanv is None:
      clickEmptyHexagon(event)
      return
    rowcolcanv=onClickRelease(event)  #todo here I could use simpler onClickRelease
    print('rowcolcanv=      ' + str(rowcolcanv))
    print('clicked_rowcolcanv=' + str(clicked_rowcolcanv))
    if len(rowcolcanv) == 0:
      return
    if rowcolcanv == clicked_rowcolcanv: #released on same tile => rotate it
      #Rotate
      deck.rotate(rowcolcanv)
    elif rowcolcanv != clicked_rowcolcanv: #released elsewhere => drop tile there.
      #previously clicked on empty hexagon
      if clicked_rowcolcanv is None:
        return
      #move tile if place is not occupied already:
      canvas_origin, canvas_dest = win.children[clicked_rowcolcanv[2][1:]], win.children[rowcolcanv[2][1:]]
      deck.move(clicked_rowcolcanv[0],clicked_rowcolcanv[1],canvas_origin, rowcolcanv[0],rowcolcanv[1],canvas_dest)
    #Reset the coordinates of the canvas where the button down was pressed
    clicked_rowcolcanv=None
  else :
    print('\n !event not supported \n')
  print('')

def onClickRelease(event):
  x, y = event.x, event.y
  if x <= 0 or x >= event.widget.winfo_reqwidth():
    print('x outside the original widget')
    return tuple()
  elif x < event.widget.winfo_reqwidth():
    print('x is inside the original widget')
  else:
    print('cannot be determined where x is vs original widget')
    return tuple()
  #event.x and event.y
  ytop= canvastop.winfo_reqheight()
  ymain= ytop + canvasmain.winfo_reqheight()
  ybottom=ymain + canvasbottom.winfo_reqheight()
  if str(event.widget) == ".canvastop":
    yrel = y
  elif str(event.widget) == ".canvasmain":
    yrel = y + ytop
  elif str(event.widget) == ".canvasbottom":
    yrel = y + ymain
  else:
    return tuple()
    raise UserWarning("onClickRelease: cannot determine yrel")

  if yrel <= 0 or yrel >= ybottom:
    print('x outside the original widget')
    return tuple()
  elif yrel <= ytop:
    print('x inside canvastop')
    rowcolcanv = list(board.pixel_to_off_canvastopbottom(x,y))
    rowcolcanv.append(".canvastop")
  elif yrel <= ymain:
    print('x inside canvas')
    rowcolcanv = list(board.pixel_to_off(x,yrel-ytop))
    rowcolcanv.append(".canvasmain")
  elif yrel <= ybottom:
    print('x inside canvasbottom')
    rowcolcanv = list(board.pixel_to_off_canvastopbottom(x,yrel-ymain))
    rowcolcanv.append(".canvasbottom")
  else:
    raise UserWarning("onClickRelease: cannot destination canvas")
    return tuple()
  return rowcolcanv

def onClick2(event):
  #Find rowcolcanv ie offset and canvas
  x, y = event.x, event.y
  if str(event.widget) == ".canvasmain":
    print("board.pixel_to_off= " + str(board.pixel_to_off(x,y))) #wrong for canvastop, eg 1.3 becomes 1,4
    rowcolcanv = list(board.pixel_to_off(x,y))
  elif str(event.widget) == ".canvastop" or str(event.widget) == ".canvasbottom":
    print("board.pixel_to_off_canvastopbottom= " + str(board.pixel_to_off_canvastopbottom(x,y)))
    rowcolcanv = list(board.pixel_to_off_canvastopbottom(x,y))
  else:
    print('\n clickCallback did not find the canvas! event.widget is :')
    print(str(event.widget))
  rowcolcanv.append(str(event.widget))
  return rowcolcanv


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

print("tantrix.py")
print(__name__)
if __name__ == "__main__":
  main()

"""TO DO
use axial coordinates to get the correct neighbors
"""

def test():
  if canvasmain.find_withtag(tk.CURRENT):
    #canvas.itemconfig(tk.CURRENT, fill="blue")
    canvasmain.update_idletasks()
    canvasmain.after(200)
    #canvas.itemconfig(tk.CURRENT, fill="red")