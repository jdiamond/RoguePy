import test_helper
import roguepy.curseswrapper as curses

if __name__ == '__main__':
    w = curses.initscr()
    curses.noecho()
    curses.cbreak()
    w.keypad(1)
    curses.start_color()
    try:
        curses.mousemask(curses.BUTTON1_RELEASED)
        curses.mouseinterval(0)
        try:
            # Hide the cursor.
            curses.curs_set(0)
        except:
            # Raises an exception on Mac OS X.
            pass
        w.clear()
        curses.init_pair(1, curses.COLOR_RED, 0)
        w.box()
        w.addstr(1, 1, 'Click to move', curses.A_REVERSE)
        x = 5
        y = 5
        w.addch(y, x, ord('@'), curses.color_pair(1) | curses.A_BOLD)
        w.refresh()
        maxyx = w.getmaxyx()
        maxx = maxyx[1] - 2
        maxy = maxyx[0] - 2
        while True:
            ch = w.getch()
            w.addch(y, x, ord(' '))
            if ch == curses.KEY_MOUSE:
                mevent = curses.getmouse()
                w.addstr(1, 1, repr(mevent))
                if mevent[1] < x: x = max(1, min(maxx, x - 1))
                elif mevent[1] > x: x = max(1, min(maxx, x + 1))
                if mevent[2] < y: y = max(1, min(maxy, y - 1))
                elif mevent[2] > y: y = max(1, min(maxy, y + 1))
            elif ch == 27: break
            elif ch == ord('h'): x = max(1, min(maxx, x - 1))
            elif ch == ord('l'): x = max(1, min(maxx, x + 1))
            elif ch == ord('j'): y = max(1, min(maxy, y + 1))
            elif ch == ord('k'): y = max(1, min(maxy, y - 1))
            else:
                curses.flash()
            w.addch(y, x, ord('@'), curses.color_pair(1) | curses.A_BOLD)
            w.refresh()
    finally:
        w.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
