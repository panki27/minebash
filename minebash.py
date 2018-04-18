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

CURSOR_POSITION=[0,0]

width, height = 9, 9
minecount = 20
#put logic for program param here
playfield = [[-3 for x in range(width)] for y in range(height)]

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
            if x >= 0 and x < len(playfield)-1:
                for y in range(row-1, row+2):
                    if y >= 0 and y < len(playfield[0])-1:
                        if(playfield[y][x] == MINE):
                            hint+=1
    else:
        hint = MINE
    return hint

def setup_playfield(w, h):
#do this only once [AFTER THE FIRST GUESS] 
    #randomly distribute mines across the field
    global playfield
    global minecount
    while minecount > 0:
        for rowindex, row in enumerate(playfield):
            for colindex, cell in enumerate(row):
                if (minecount > 0) and cell != MINE:
                    if random.random() < 0.1:
                        minecount -= 1
                        playfield[colindex][rowindex] = MINE
                else:
                    break
    #now that's done, we'll have to calculate the hint numbers
    #for rowindex, row in enumerate(playfield):
    #    for colindex, cell in enumerate(row):
    #        playfield[colindex][rowindex] = calculate_hint(colindex, rowindex)

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
            elif cell == UNKNOWN:
                rowstring+= '#'
            elif cell == MINE:
		rowstring += 'X'
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
    stdscr.addstr(currentline, 0, tailline)
    currentline +=1
    #print tailline

def hit(x, y):
    global playfield
    if playfield[y][x] == UNKNOWN:
        hint = calculate_hint(x, y)
        playfield[y][x] = hint

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
        stdscr.refresh()
        #stdscr.getkey()
if __name__ == "__main__":
    curses.wrapper(main)
    #finally:
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
