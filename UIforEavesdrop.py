
from unicurses import *
from Eavesdrop import pysharkSniffer
def Main():
    stdscr = initscr()
    start_color()
    use_default_colors()
    init_pair(1,COLOR_CYAN,-1)
    running = True
    while (running):
     #  addstr(pysharkSniffer.out_string, color_pair(1) + A_BOLD)
       key = getch();
       keypad(stdscr,True)
       if (key == ord(' ')):
           running = False
           break

    endwin()
    return 0




if __name__ == '__main__':
    Main()

