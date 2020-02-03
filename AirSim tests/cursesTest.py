import time
import curses

def pbar(window):
    for i in range(10):
        window.addstr(10, 10, "[" + ("=" * i) + ">" + (" " * (10 - i )) + "]")
        window.addstr(10, 10, "aids")
        window.refresh()
        time.sleep(0.5)

curses.wrapper(pbar)