import ctypes

from os.path import join, dirname, abspath

_pdcurses = join(dirname(abspath(__file__)), 'pdcurses')
_dll = ctypes.cdll.LoadLibrary(_pdcurses)

def beep():
  _dll.beep()

def color_pair(n):
    return n << PDC_COLOR_SHIFT & A_COLOR

def curs_set(visibility):
  return _dll.curs_set(visibility)

def echo():
  _dll.echo()

def endwin():
  _dll.endwin()

def flash():
  _dll.flash()

class MEVENT(ctypes.Structure):
  _fields_ = [
    ('id', ctypes.c_short),
    ('x', ctypes.c_int),
    ('y', ctypes.c_int),
    ('z', ctypes.c_int),
    ('bstate', ctypes.c_ulong)
  ]

def getmouse():
  mevent = MEVENT()
  _dll.nc_getmouse(ctypes.byref(mevent))
  return (mevent.id, mevent.x, mevent.y, mevent.z, mevent.bstate)

def init_pair(pair_number, fg, bg):
  return _dll.init_pair(pair_number, fg, bg)

def initscr():
  return Window(_dll.initscr())

def mouseinterval(interval):
  return _dll.mouseinterval(interval)

def mousemask(newmask):
  oldmask = ctypes.c_int()
  availmask = _dll.mousemask(newmask, ctypes.byref(oldmask))
  return (availmask, oldmask.value)

def noecho():
  _dll.noecho()

def pair_number(n):
    return (n & A_COLOR) >> PDC_COLOR_SHIFT

def start_color():
  _dll.start_color()

class Window:
  def __init__(self, window):
    self.window = window

  def addch(self, *args):
    '''[y, x], ch[, attr])'''
    if len(args) == 1:
      _dll.waddch(self.window, args[0])
    elif len(args) == 2:
      _dll.waddch(self.window, args[0] | args[1])
    elif len(args) == 3:
      _dll.mvwaddch(self.window, args[0], args[1], args[2])
    elif len(args) == 4:
      _dll.mvwaddch(self.window, args[0], args[1], args[2] | args[3])
    else:
      raise TypeError('addch requires 1 to 4 arguments')

  def addnstr(self, *args):
    '''[y, x], str, n[, attr]'''
    y, x, attr = None, None, None
    if len(args) == 2:
      str, n = args
    elif len(args) == 3:
      str, n, attr = args
    elif len(args) == 4:
      y, x, str, n = args
    elif len(args) == 5:
      y, x, str, n, attr = args
    else:
      raise TypeError('addnstr requires 2 to 5 arguments')
    if attr is not None:
      old_attr = _dll.getattrs(self.window)
      _dll.wattrset(self.window, attr)
    if y is not None and x is not None:
      _dll.mvwaddnstr(self.window, y, x, str, n)
    else:
      _dll.waddnstr(self.window, str, n)
    if attr is not None:
      _dll.wattrset(self.window, old_attr)

  def addstr(self, *args):
    '''[y, x], str[, attr]'''
    y, x, attr = None, None, None
    if len(args) == 1:
      str = args[0]
    elif len(args) == 2:
      str, attr = args
    elif len(args) == 3:
      y, x, str = args
    elif len(args) == 4:
      y, x, str, attr = args
    else:
      raise TypeError('addstr requires 1 to 4 arguments')
    if attr is not None:
      old_attr = _dll.getattrs(self.window)
      _dll.wattrset(self.window, attr)
    if y is not None and x is not None:
      _dll.mvwaddstr(self.window, y, x, str)
    else:
      _dll.waddstr(self.window, str)
    if attr is not None:
      _dll.wattrset(self.window, old_attr)

  def box(self, *args):
    '''[vertch, horch]'''
    if len(args) == 0:
      vertch, horch = 0, 0
    elif len(args) == 2:
      vertch, horch = args
    else:
      raise TypeError('box requires 0 or 2 arguments')
    _dll.box(self.window, vertch, horch)

  def clear(self):
    _dll.wclear(self.window)

  def getch(self, *args):
    '''[y, x]'''
    if len(args) == 0:
      return _dll.wgetch(self.window)
    elif len(args) == 2:
      return _dll.mvwgetch(self.window, args[0], args[1])
    else:
      raise TypeError('getch requires 0 or 2 arguments')

  def keypad(self, yes):
    _dll.keypad(self.window, yes)

  def refresh(self):
    _dll.wrefresh(self.window)

A_ATTRIBUTES = 0xffff0000
A_NORMAL = 0
A_UNDERLINE = 0x00100000
A_REVERSE = 0x00200000
A_BLINK = 0x00400000
A_DIM = A_NORMAL
A_BOLD = 0x00800000
A_STANDOUT = A_REVERSE | A_BOLD
A_ALTCHARSET = 0x00010000
A_INVIS = 0x00080000
A_RIGHTLINE = 0x00020000
A_LEFTLINE = 0x00040000
A_PROTECT = A_UNDERLINE | A_LEFTLINE | A_RIGHTLINE
A_CHARTEXT = 0x0000ffff
A_COLOR = 0xff000000

PDC_ATTR_SHIFT = 19
PDC_COLOR_SHIFT = 24

COLOR_BLACK = 0
COLOR_RED = 4
COLOR_GREEN = 2
COLOR_YELLOW = COLOR_RED | COLOR_GREEN
COLOR_BLUE = 1
COLOR_MAGENTA = COLOR_RED | COLOR_BLUE
COLOR_CYAN = COLOR_BLUE | COLOR_GREEN
COLOR_WHITE = 7

BUTTON1_RELEASED = 0x00000001
BUTTON1_PRESSED = 0x00000002
BUTTON1_CLICKED = 0x00000004
BUTTON1_DOUBLE_CLICKED = 0x00000008
BUTTON1_TRIPLE_CLICKED = 0x00000010

BUTTON2_RELEASED = 0x00000020
BUTTON2_PRESSED = 0x00000040
BUTTON2_CLICKED = 0x00000080
BUTTON2_DOUBLE_CLICKED = 0x00000100
BUTTON2_TRIPLE_CLICKED = 0x00000200

BUTTON3_RELEASED = 0x00000400
BUTTON3_PRESSED = 0x00000800
BUTTON3_CLICKED = 0x00001000
BUTTON3_DOUBLE_CLICKED = 0x00002000
BUTTON3_TRIPLE_CLICKED = 0x00004000

BUTTON4_RELEASED = 0x00008000
BUTTON4_PRESSED = 0x00010000
BUTTON4_CLICKED = 0x00020000
BUTTON4_DOUBLE_CLICKED = 0x00040000
BUTTON4_TRIPLE_CLICKED = 0x00080000

BUTTON_SHIFT = 0x04000000
BUTTON_CTRL = 0x08000000
BUTTON_ALT = 0x10000000

ALL_MOUSE_EVENTS = 0x1fffffff
REPORT_MOUSE_POSITION = 0x20000000

KEY_MOUSE = 0x21b

def ACS_PICK(w, n):
    return ord(w) | A_ALTCHARSET

ACS_ULCORNER = ACS_PICK('l', '+')
ACS_LLCORNER = ACS_PICK('m', '+')
ACS_URCORNER = ACS_PICK('k', '+')
ACS_LRCORNER = ACS_PICK('j', '+')
ACS_RTEE = ACS_PICK('u', '+')
ACS_LTEE = ACS_PICK('t', '+')
ACS_BTEE = ACS_PICK('v', '+')
ACS_TTEE = ACS_PICK('w', '+')
ACS_HLINE = ACS_PICK('q', '-')
ACS_VLINE = ACS_PICK('x', '|')
ACS_PLUS = ACS_PICK('n', '+')

