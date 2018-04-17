#!/usr/bin/python
import readline, random

NOTHING = 0
MINE = -1
FLAG = -2
UNKNOWN = -3


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
    if playfield[col][row] != MINE:
        for x in range(col-1, col+2):
            if x >= 0 and x < len(playfield)-1:
                for y in range(row-1, row+2):
                    if y >= 0 and y < len(playfield[0])-1:
                        if(playfield[x][y] == MINE):
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
    for rowindex, row in enumerate(playfield):
        for colindex, cell in enumerate(row):
            playfield[colindex][rowindex] = calculate_hint(colindex, rowindex)

def print_playfield(playfield):
    print headline
    for index, row in enumerate(playfield):
        rowstring = '|'
        for cell in row:
            # did we find a hint?
            if cell >= 0:
                rowstring += '[' + str(cell) + ']|'
            elif cell == UNKNOWN:
                rowstring+='[#]|'
            elif cell == MINE:
                rowstring+='[X]|'
        print rowstring
        if(index < len(row)-1):
            print midline
    print tailline

def main():
    setup_strings(width)
    #print_playfield(playfield)
    #TODO: user input
    #generate mines:
    setup_playfield(width, height)
    print_playfield(playfield)
if __name__ == "__main__":
    main()