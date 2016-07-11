#!/usr/bin/env python3
# For now, render a single frame of a @choochoobot drawing onto a canvas.
# More to come.

from PIL import Image
import random
from math import ceil

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 576
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
NUMROWS = 6
BLOCK_SIDE = int(SCREEN_HEIGHT/NUMROWS)
BLOCK_SIZE = (BLOCK_SIDE,BLOCK_SIDE)
ROWS = [BLOCK_SIDE * x for x in range(NUMROWS)]
NUMCOLS = int(SCREEN_WIDTH/BLOCK_SIDE)
FRAME_COUNT = 160

choochoo = Image.open("images/choochoo.png").resize(BLOCK_SIZE)
redcar = Image.open("images/redcar.png").resize(BLOCK_SIZE)
greencar = Image.open("images/greencar.png").resize(BLOCK_SIZE)
cactus = Image.open("images/cactus.png").resize(BLOCK_SIZE)
palm = Image.open("images/palm.png").resize(BLOCK_SIZE)
turtle = Image.open("images/turtle.png").resize(BLOCK_SIZE)
horse = Image.open("images/horse.png").resize(BLOCK_SIZE)
sun = Image.open("images/sun.png").resize(BLOCK_SIZE)
moon = Image.open("images/moon.png").resize(BLOCK_SIZE)
blank = Image.new("RGBA",BLOCK_SIZE,(0,0,0,0))

# chance the object will move (0 to 1) in the R,L,U,D directions
# objects will never move into other scenery
MOVABLES = [
    [horse, 0.25, 0.5,0.2,0.2],
    [turtle, 0.1, 0.1, 0.1, 0.1]
]

# List of random scenery
SCENERY = [cactus,cactus,palm,palm,horse,turtle]
# Rows that can contain scenery
SCENERY_ROWS = [1,2,4,5]

def main():

    # cells holds the current state of the world
    cells = [None] * NUMROWS
    for i in range(0,NUMROWS):
        cells[i] = [None] * NUMCOLS


    # generate train
    choochx = 6
    choochy = 3

    train_length = 7
    train = []

    train.append(choochoo)
    for car in range(train_length):
        cars = [redcar,greencar]
        train.append(random.choice(cars))

    # generate initial scenery
    generate_scenery(cells, SCENERY_ROWS)

    frame_number = 0

    while frame_number <= FRAME_COUNT:

        bgcolor = (255,255,255)

        render = Image.new('RGBA',SCREEN_SIZE,bgcolor)

        # draw all cells
        for i, r in enumerate(cells):
            for j, c in enumerate(r):
                if c != None:
                    render.paste(c,(j*BLOCK_SIDE, i*BLOCK_SIDE), c)

        # draw the sky
        draw_sky(render, frame_number)

        # draw the train
        draw_train(render, train, choochx, choochy)

        # scroll and move scenery
        update_scenery(cells, SCENERY_ROWS)
        
        new_filename = "slides/img" + format(frame_number,"04d") + ".png"
        print("rendering frame " + str(frame_number) + " as " + new_filename)
        render.save(new_filename)

        frame_number += 1

def draw_sky(canvas,frame):
    # how often sky moves (in frames)
    SKY_MOVE_FRAME = FRAME_COUNT/40
    sky_pos = int(frame / SKY_MOVE_FRAME) % (2 * NUMCOLS)
    sky_img = sun
    if sky_pos > NUMCOLS:
        sky_pos -= NUMCOLS
        sky_img = moon
    canvas.paste(sky_img, (sky_pos*BLOCK_SIDE, 0), sky_img)

def draw_train(canvas, train, x, y):
    bounce = random.randint(-4,4)
    for i, car in enumerate(train):
        canvas.paste(car,((x+i)*BLOCK_SIDE,y*BLOCK_SIDE+bounce),car)

def generate_scenery(cells, rows):
    for r in rows:
        for c in range(0, NUMCOLS):
            if random.randint(1,10) == 1:
                cells[r][c] = random.choice(SCENERY)


def update_scenery(cells, rows):
    # move any movable scene objects
    for r, row in enumerate(cells):
        for c, obj in enumerate(row):
            if obj != None:
                # check if movable
                for m in MOVABLES:
                    if m[0] == obj:
                        move_object(cells, rows, r, c, m)

    for r in rows:
        # move all scenery to the right
        for c in range(NUMCOLS-1, 0, -1):
            cells[r][c] = cells[r][c-1]

        # spawn new scenery
        cells[r][0] = None
        if random.randint(1,10) == 1:
            cells[r][0] = random.choice(SCENERY)

def move_object(cells, rows, r, c, move_def):
    # move only once, randomly
    moves = ["R", "L", "U", "D"]
    random.shuffle(moves)

    for m in moves:
        # move right
        if m == "R":
            if c < NUMCOLS-1 and random.random() < move_def[1] and cells[r][c+1] == None:
                cells[r][c+1] = cells[r][c]
                cells[r][c] = None
                return
        # move left?
        if m == "L":
            if c > 0 and random.random() < move_def[2] and cells[r][c-1] == None:
                cells[r][c-1] = cells[r][c]
                cells[r][c] = None
                return
        # move up?
        if m == "U":
            if r > 0 and random.random() < move_def[3] and r-1 in rows and cells[r-1][c] == None:
                cells[r-1][c] = cells[r][c]
                cells[r][c] = None
                return
        # move down?
        if m == "D":
            if r < NUMROWS-1 and random.random() < move_def[4] and r+1 in rows and cells[r+1][c] == None:
                cells[r+1][c] = cells[r][c]
                cells[r][c] = None
                return


if __name__ == "__main__":
    main()
