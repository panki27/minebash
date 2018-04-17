#!/usr/bin/python
import readline, random

UNKNOWN = 0


width, height = 9, 9
#put logic for program param here
playfield = [[0 for x in range(width)] for y in range(height)]

headline = '.'
midline = '|'
tailline = '\''

def setup_playfield(w, h):
#do this only once
    for i in range(w):
        global headline, midline, tailline
        headline += '---.'
        midline += '---|'
        tailline += '---\''    

def print_playfield(playfield):
    print headline
    for index, row in enumerate(playfield):
        rowstring = '|'
        for cell in row:
            rowstring+='[ ]|'
        print rowstring
        if(index < len(row)-1):
            print midline
    print(tailline)

def main():
    setup_playfield(width, height)
    print_playfield(playfield)

if __name__ == "__main__":
    main()