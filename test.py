import math
import PIL.Image, PIL.ImageTk
try:
    import Tkinter as tk # for Python2
except:
    import tkinter as tk # for Python3
import config as cfg
import Board as bd
import callbacks as clb
from pymouse import PyMouse
m = PyMouse()
from pykeyboard import PyKeyboard
k = PyKeyboard()

x0, y0 = None, None

def tests():
    global x0, y0
    sizes, xoff, yoff = cfg.win.geometry().split("+")
    w, h = sizes.split("x")
    xoff, yoff = float(xoff), float(yoff)
    w, h = float(w), float(h)
    x0 = xoff #934
    y0 = yoff

    print("xoff=",str(xoff),"should be 2212")
    print(m.position()) #2212
    m.move(x0, y0 + cfg.YTOP)
    #m.move(x0 + x1, y0 + cfg.YTOP + y1)
    #cfg.canvasmain.after(1000, cfg.win.update())
    #m.move(x0 + x2, y0 + cfg.YTOP + y2)
    #cfg.canvasmain.after(1000, cfg.win.update())

    drag((0, 0, -1), (3, 3, 0))

    cfg.canvasmain.after(500, cfg.win.update())

    #k.press_keys([k.alt_l_key, k.tab_key])

    k.tap_key(k.return_key)

    cfg.canvasmain.after(500, cfg.win.update())
    #clbk = clb.Callbacks()
    #clbk.buttonConfirm()
    click((2, 2, 0))
    return
    drag((0, 1, -1), (3, 2, 0))

    #k.press_keys([k.alt_l_key, k.tab_key])

    #x,y = m.position()


def drag(rowcoltab1, rowcoltab2):
    x1, y1 = cfg.board.off_to_pixel(rowcoltab1)
    x2, y2 = cfg.board.off_to_pixel(rowcoltab2)
    m.press(x0 + x1, y0 + cfg.YTOP + y1)
    cfg.canvasmain.after(1000, cfg.win.update())
    m.move(x0 + x2, y0 + cfg.YTOP + y2)
    cfg.canvasmain.after(500, cfg.win.update())
    m.release(x0 + x2, y0 + cfg.YTOP + y2)

def click(rowcoltab):
    x, y = cfg.board.off_to_pixel(rowcoltab)
    m.click(x, y, 1)