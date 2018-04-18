#!/usr/bin/env python2
import readline, random, io, sys

import curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()

NOTHING = 0
MINE = -1
FLAG = -2
UNKNOWN = -3
FLAG_MINE = -4

CURSOR_POSITION=[0,0]
FIELDS_CLEARED = 0

width, height = 9, 9
MINECOUNT = 10
#put logic for program param here
playfield = [[UNKNOWN for x in range(width)] for y in range(height)]

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

def setup_playfield(w, h):
#do this only once [AFTER THE FIRST GUESS] 
    #randomly distribute mines across the field
    global playfield
    minesleft = MINECOUNT
    while minesleft > 0:
        for rowindex, row in enumerate(playfield):
            for colindex, cell in enumerate(row):
                if  minesleft > 0 and playfield[colindex][rowindex] != MINE:
                    if random.random() < 0.1:
                        minesleft -= 1
                        playfield[colindex][rowindex] = MINE
                else:
                    break
    #now that's done, we'll have to calculate the hint numbers
    #for rowindex, row in enumerate(playfield):
    #    for colindex, cell in enumerate(row):
    #        playfield[colindex][rowindex] = calculate_hint(colindex, rowindex)

def gameover(win):
    stdscr.clear()
    if not win:
        stdscr.addstr(0, 0, '                               ________________')
        stdscr.addstr(1, 0, '                          ____/ (  (    )   )  \___')
        stdscr.addstr(2, 0, '                         /( (  (  )   _    ))  )   )\ ')
        stdscr.addstr(3, 0, '                       ((     (   )(    )  )   (   )  )')
        stdscr.addstr(4, 0, '                     ((/  ( _(   )   (   _) ) (  () )  )')
        stdscr.addstr(5, 0, '                    ( (  ( (_)   ((    (   )  .((_ ) .  )_')
        stdscr.addstr(6, 0, '                   ( (  )    (      (  )    )   ) . ) (   )')
        stdscr.addstr(7, 0, '                  (  (   (  (   ) (  _  ( _) ).  ) . ) ) ( )')
        stdscr.addstr(8, 0, '                  ( (  (   ) (  )   (  ))     ) _)(   )  )  )')
        stdscr.addstr(9, 0, '                 ( (  ( \ ) (    (_  ( ) ( )  )   ) )  )) ( )')
        stdscr.addstr(10, 0, '                  (  (   (  (   (_ ( ) ( _    )  ) (  )  )   )')
        stdscr.addstr(11, 0, '                 ( (  ( (  (  )     (_  )  ) )  _)   ) _( ( )')
        stdscr.addstr(12, 0, '                  ((  (   )(    (     _    )   _) _(_ (  (_ )')
        stdscr.addstr(13, 0, '                   (_((__(_(__(( ( ( |  ) ) ) )_))__))_)___)')
        stdscr.addstr(14, 0, '                   ((__)        \\||lll|l||///          \_))')
        stdscr.addstr(15, 0, '                            (   /(/ (  )  ) )\   )')
        stdscr.addstr(16, 0, '                          (    ( ( ( | | ) ) )\   )')
        stdscr.addstr(17, 0, '                           (   /(| / ( )) ) ) )) )')
        stdscr.addstr(18, 0, '                         (     ( ((((_(|)_)))))     )')
        stdscr.addstr(19, 0, '                          (      ||\(|(|)|/||     )')
        stdscr.addstr(20, 0, '                        (        |(||(||)||||        )')
        stdscr.addstr(21, 0, '                          (     //|/l|||)|\\ \     )')
        stdscr.addstr(22, 0, '                        (/ / //  /|//||||\\  \ \  \ _)')        
        stdscr.addstr(23, 0, '                           You lose! Press q to quit.')
    else:
        stdscr.addstr(0, 0, 'You win! Press q to quit.')
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            sys.exit(0)

def print_playfield(playfield):
    currentline = 0
    stdscr.addstr(currentline, 0, headline)
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
            if cell >= 0:
                rowstring += str(cell)
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
        stdscr.addstr(currentline, 0, rowstring)
        currentline +=1
        if(rowindex < len(row)-1):
            stdscr.addstr(currentline, 0, midline)
            currentline +=1
            #print midline
    #print currentline
    #print tailline
    stdscr.addstr(currentline, 0, tailline)
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
    global playfield
    #playfield[y][x] = playfield[y][x]
    if playfield[y][x] == MINE:
        playfield[y][x] = FLAG_MINE
    elif playfield[y][x] == UNKNOWN:
        playfield[y][x] = FLAG
    elif playfield[y][x] == FLAG_MINE:
        playfield[y][x] = MINE
    elif playfield[y][x] == FLAG:
        playfield[y][x] = UNKNOWN

def handle_input(k):
    global CURSOR_POSITION
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
        hit(CURSOR_POSITION[0], CURSOR_POSITION[1])      

def main(stdscr):
    stdscr.clear()
    setup_strings(width)
    #generate mines:
    setup_playfield(width, height)
    #print_playfield(playfield)
    #TODO: user input
    while(True):
        print_playfield(playfield)
        key = stdscr.getch()
        handle_input(key)
        check_score()
        stdscr.refresh()
        #stdscr.getkey()
if __name__ == "__main__":
    curses.wrapper(main)
    #finally:
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
