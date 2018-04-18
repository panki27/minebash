#!/usr/bin/env python3
#TODO: Color, show controls, command line param

import readline, random, io, sys, time, os

import curses
from curses import wrapper

NOTHING = 0
MINE = -1
FLAG = -2
UNKNOWN = -3
FLAG_MINE = -4

STARTTIME = 0

SCREEN = 0

firstmove = False
FIELD_GENERATED = False

CURSOR_POSITION=[0,0]
FIELDS_CLEARED = 0

width, height = 9, 9
MINECOUNT = 10
FLAGCOUNT = 0
if len(sys.argv) > 1:
    if len(sys.argv) == 4:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        MINECOUNT = int(sys.argv[3])
    else:
        print('Specify parameters as width height minecount (for example ./minebash.py 5 5 7)')
        sys.exit(0)
playfield = [[UNKNOWN for x in range(width)] for y in range(height)]


#stdscr = curses.initscr()
#curses.noecho()
#curses.cbreak()
headline = '.'
midline = '|'
tailline = '\''

def setup_strings(colcount):
    #setup lines to print
    for i in range(colcount):
        global headline, midline, tailline
        headline += '---.'
        midline += '---|'
        tailline += '---\''

def endgame(msg=''):
 #   curses.nocbreak()
  #  stdscr.keypad(False)
   # curses.echo()
    #curses.endwin()
    if msg != '':
        print(msg)
    sys.exit(0)

def calculate_hint(col, row):
    hint = 0
    if playfield[row][col] != MINE:
        for x in range(col-1, col+2):
            if x >= 0 and x < len(playfield):
                for y in range(row-1, row+2):
                    if y >= 0 and y < len(playfield[0]):
                        if playfield[y][x] == MINE or playfield[y][x] == FLAG_MINE:
                            hint+=1
    else:
        hint = MINE
    return hint

def setup_playfield(w, h, x, y):
#do this only once [AFTER THE FIRST GUESS] -> Done
    #randomly distribute mines across the field
    global playfield, FIELD_GENERATED, STARTTIME
    minesleft = MINECOUNT
    while minesleft > 0:
        for rowindex, row in enumerate(playfield):
            for colindex, cell in enumerate(row):
                if colindex == x and rowindex == y:
                    continue
                if  minesleft > 0 and playfield[colindex][rowindex] != MINE:
                    if random.random() < 0.1:
                        minesleft -= 1
                        playfield[colindex][rowindex] = MINE
                else:
                    break
    FIELD_GENERATED = True
    STARTTIME = time.time()

def gameover(win):
    SCREEN.clear()
    if not win:
        SCREEN.addstr(0, 0, '                               ________________')
        SCREEN.addstr(1, 0, '                          ____/ (  (    )   )  \___')
        SCREEN.addstr(2, 0, '                         /( (  (  )   _    ))  )   )\ ')
        SCREEN.addstr(3, 0, '                       ((     (   )(    )  )   (   )  )')
        SCREEN.addstr(4, 0, '                     ((/  ( _(   )   (   _) ) (  () )  )')
        SCREEN.addstr(5, 0, '                    ( (  ( (_)   ((    (   )  .((_ ) .  )_')
        SCREEN.addstr(6, 0, '                   ( (  )    (      (  )    )   ) . ) (   )')
        SCREEN.addstr(7, 0, '                  (  (   (  (   ) (  _  ( _) ).  ) . ) ) ( )')
        SCREEN.addstr(8, 0, '                  ( (  (   ) (  )   (  ))     ) _)(   )  )  )')
        SCREEN.addstr(9, 0, '                 ( (  ( \ ) (    (_  ( ) ( )  )   ) )  )) ( )')
        SCREEN.addstr(10, 0, '                  (  (   (  (   (_ ( ) ( _    )  ) (  )  )   )')
        SCREEN.addstr(11, 0, '                 ( (  ( (  (  )     (_  )  ) )  _)   ) _( ( )')
        SCREEN.addstr(12, 0, '                  ((  (   )(    (     _    )   _) _(_ (  (_ )')
        SCREEN.addstr(13, 0, '                   (_((__(_(__(( ( ( |  ) ) ) )_))__))_)___)')
        SCREEN.addstr(14, 0, '                   ((__)        \\||lll|l||///          \_))')
        SCREEN.addstr(15, 0, '                            (   /(/ (  )  ) )\   )')
        SCREEN.addstr(16, 0, '                          (    ( ( ( | | ) ) )\   )')
        SCREEN.addstr(17, 0, '                           (   /(| / ( )) ) ) )) )')
        SCREEN.addstr(18, 0, '                         (     ( ((((_(|)_)))))     )')
        SCREEN.addstr(19, 0, '                          (      ||\(|(|)|/||     )')
        SCREEN.addstr(20, 0, '                        (        |(||(||)||||        )')
        SCREEN.addstr(21, 0, '                          (     //|/l|||)|\\ \     )')
        SCREEN.addstr(22, 0, '                        (/ / //  /|//||||\\  \ \  \ _)')        
        SCREEN.addstr(23, 0, '                          You lose! Press q to quit.')
    else:
        now = time.time()
        elapsed = now - STARTTIME
        mins = elapsed / 60
        secs = elapsed % 60
        winstr = 'You win! It took you {}:{} to bash the field!'.format(int(mins), str(round(secs, 2)).zfill(5))
        SCREEN.addstr(0, 0, ' /$$      /$$           /$$ /$$       /$$$$$$$                                /$$')
        SCREEN.addstr(1, 0, '| $$  /$ | $$          | $$| $$      | $$__  $$                              | $$')
        SCREEN.addstr(2, 0, '| $$ /$$$| $$  /$$$$$$ | $$| $$      | $$  \ $$  /$$$$$$  /$$$$$$$   /$$$$$$ | $$')
        SCREEN.addstr(3, 0, '| $$/$$ $$ $$ /$$__  $$| $$| $$      | $$  | $$ /$$__  $$| $$__  $$ /$$__  $$| $$')
        SCREEN.addstr(4, 0, '| $$$$_  $$$$| $$$$$$$$| $$| $$      | $$  | $$| $$  \ $$| $$  \ $$| $$$$$$$$|__/')
        SCREEN.addstr(5, 0, '| $$$/ \  $$$| $$_____/| $$| $$      | $$  | $$| $$  | $$| $$  | $$| $$_____/    ')
        SCREEN.addstr(6, 0, '| $$/   \  $$|  $$$$$$$| $$| $$      | $$$$$$$/|  $$$$$$/| $$  | $$|  $$$$$$$ /$$')
        SCREEN.addstr(7, 0, '|__/     \__/ \_______/|__/|__/      |_______/  \______/ |__/  |__/ \_______/|__/')
        SCREEN.addstr(10, 0, winstr)
        SCREEN.addstr(11,0, 'Press q to quit!')
    while True:
        key = SCREEN.getch()
        if key == ord('q'):
            endgame()
        #if key == ord('r'):
        #    os.execl(sys.executable, sys.executable, *sys.argv)

def print_playfield(playfield, screen):
    currentline = 0
    screen.addstr(currentline, 0, headline)
    currentline +=1
    #print headline
    for rowindex, row in enumerate(playfield):
        rowstring = '|'
        for colindex, cell in enumerate(row):
            # is the cell selected?
            selected = False
            if [colindex, rowindex] == CURSOR_POSITION:
                rowstring += '['
                selected = True
            else:
                rowstring += ' '
            # did we find a hint?
            if cell > 0:
                rowstring += str(cell)
            elif cell == 0:
                rowstring += ' '
            elif cell == UNKNOWN or cell == MINE:
                rowstring+= '#'
            elif cell == FLAG_MINE or cell == FLAG:
                rowstring += 'P'
            #elif cell == MINE:
            #    rowstring += 'X'
            if selected:
                rowstring += ']|'
            else:
                rowstring+=' |'
        #print rowstring
        screen.addstr(currentline, 0, rowstring)
        currentline +=1
        if(rowindex < len(row)-1):
            screen.addstr(currentline, 0, midline)
            currentline +=1
    screen.addstr(currentline, 0, tailline)
    currentline +=1
    #print tailline

def hit(x, y, recursive_call=False):
    global playfield, FIELDS_CLEARED
    if playfield[y][x] == UNKNOWN:
        hint = calculate_hint(x, y)
        playfield[y][x] = hint
        FIELDS_CLEARED += 1
        if not recursive_call and hint == NOTHING:
            for i in range(x-1, x+2):
                for j in range(y-1, y+2):
                    if i >= 0 and i < width:
                        if j >= 0 and j< height:
                            if playfield[j][i] == UNKNOWN:
                                    hint = calculate_hint(i, j)
                                    if hint > 0 and hint<3:
                                        hit(i,j, True)
                                    if hint == 0:
                                        hit(i,j)
    elif playfield[y][x] == MINE:
        gameover(False)

def check_score():
    if FIELDS_CLEARED == (width*height)-MINECOUNT:
        gameover(True)

def place_flag(x, y):
    global playfield, FLAGCOUNT
    #playfield[y][x] = playfield[y][x]
    if playfield[y][x] == MINE:
        playfield[y][x] = FLAG_MINE
        FLAGCOUNT += 1
    elif playfield[y][x] == UNKNOWN:
        playfield[y][x] = FLAG
        FLAGCOUNT += 1
    elif playfield[y][x] == FLAG_MINE:
        playfield[y][x] = MINE
        FLAGCOUNT -= 1
    elif playfield[y][x] == FLAG:
        playfield[y][x] = UNKNOWN
        FLAGCOUNT -=1

def handle_input(k):
    global CURSOR_POSITION, firstmove
    if k == curses.KEY_LEFT:
        if CURSOR_POSITION[0] > 0:
            CURSOR_POSITION[0] -=1
    elif k == curses.KEY_RIGHT:
        if CURSOR_POSITION[0] < width-1:
            CURSOR_POSITION[0] +=1    
    elif k == curses.KEY_UP:
        if CURSOR_POSITION[1] > 0:
            CURSOR_POSITION[1] -=1
    elif k == curses.KEY_DOWN:
        if CURSOR_POSITION[1] < height-1:
            CURSOR_POSITION[1] +=1
    elif k == ord('f'):
        place_flag(CURSOR_POSITION[0], CURSOR_POSITION[1])
    elif k == ord(' '):
        if not firstmove:
            firstmove = True
        else:
            hit(CURSOR_POSITION[0], CURSOR_POSITION[1])      

def print_score(screen):
    scorestr = 'Mines: {} Flags: {}'.format(MINECOUNT, FLAGCOUNT)
    screen.addstr(19 ,0,scorestr)

def main(stdscr):
    global SCREEN
    SCREEN = stdscr
    stdscr.clear()
    setup_strings(width)
    #generate mines:
    #print_playfield(playfield)
    #TODO: user input
    while(True):
        print_playfield(playfield, stdscr)
        key = stdscr.getch()
        handle_input(key)
        if (firstmove) and not (FIELD_GENERATED):
            setup_playfield(width, height, CURSOR_POSITION[0], CURSOR_POSITION[1])
            handle_input(key)
            STARTTIME = time.time()
        check_score()
        print_score(stdscr)
        stdscr.refresh()
        #stdscr.getkey()
if __name__ == "__main__":
    wrapper(main)

