# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 22:40:54 2019

@author: PaulJ
"""


class Snake():
    pass


import pgzrun
import random
import time

FONT_COLOR = (255, 255, 255)
SNAKE_SPRITE_SIZE = 64
WIDTH_IN_SPRITES = 12  # was 25, made smaller for testing
HEIGHT_IN_SPRITES = 12
WIDTH = SNAKE_SPRITE_SIZE * WIDTH_IN_SPRITES  # 1600
HEIGHT = SNAKE_SPRITE_SIZE * HEIGHT_IN_SPRITES  # 768
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
CENTER = (CENTER_X, CENTER_Y)
HEAD = 0
# TAIL = -1
START_EDGE_SPRITE_MARGIN = 4
START_EDGE_APPLE_MARGIN = 1
CRASH_EDGE_MARGIN = 0  # pixels
SNAKE_MOVE_ACCEL = 0.05  # 5% increase in speed after eating apple
NORTH = 'north'
SOUTH = 'south'
WEST = 'west'
EAST = 'east'
DIRECTIONS = [NORTH, SOUTH, EAST, WEST]
OPP_DIR = {NORTH: SOUTH,
           SOUTH: NORTH,
           EAST: WEST,
           WEST: EAST}
X_MOVE = {'north': 0,
          'south': 0,
          'east': SNAKE_SPRITE_SIZE,
          'west': -SNAKE_SPRITE_SIZE}
Y_MOVE = {'north': -SNAKE_SPRITE_SIZE,
          'south': SNAKE_SPRITE_SIZE,
          'east': 0,
          'west': 0}
HS_FILENAME = (r'C:\Users\PaulJ\Data\Computers & Internet\Python\Games\S' +
               'nake\high-scores.txt')
MAX_SCORES_TO_KEEP = 5

# snake_head = Actor('snake_head')
# snake_body = Actor('snake_body')
# snake_tail = Actor('snake_tail')

scores = []




def initiate():
    global snake_length, tail, turn_direction, snake, apple, game_over, score
    global start_time, high_score_updated, snake_move_duration
    snake_length = 2
    tail = snake_length - 1
    turn_direction = False
    snake_move_duration = 0.5
    high_score_updated = False
    snake_head_direction = random.choice(DIRECTIONS)
    start_pos_x = int((random.randint(START_EDGE_SPRITE_MARGIN,
                                      WIDTH_IN_SPRITES -
                                      START_EDGE_SPRITE_MARGIN - 1) + 0.5) *
                      SNAKE_SPRITE_SIZE)
    start_pos_y = int((random.randint(START_EDGE_SPRITE_MARGIN,
                                      HEIGHT_IN_SPRITES -
                                      START_EDGE_SPRITE_MARGIN - 1) + 0.5) *
                      SNAKE_SPRITE_SIZE)
    print('snake: start_pos_x:', start_pos_x, ', start_pos_y:', start_pos_y)
    snake = [{'actor': Actor('snake_head_' + snake_head_direction),
              'pos': (start_pos_x, start_pos_y),
              'dir': snake_head_direction,
              'dir-tail': OPP_DIR[snake_head_direction]}]
    snake[HEAD]['actor'].pos = snake[HEAD]['pos']
    snake.append({'actor': Actor('snake_tail_' + snake[HEAD]['dir']),
                  'pos': (snake[HEAD]['pos'][0] - X_MOVE[snake[HEAD]['dir']],
                          snake[HEAD]['pos'][1] - Y_MOVE[snake[HEAD]['dir']]),
                  'dir': snake[HEAD]['dir'],
                  'dir-head': snake_head_direction})

    with open(HS_FILENAME, 'r') as file:
        line = file.readline()
        high_scores = line.split()
        high_scores_ints = []
        for a_score in high_scores:
            try:
                high_scores_ints.append(int(a_score))
            except ValueError:
                print('Some scores in high score file are invalid, ignoring')

    game_over = False
    score = 0
    start_time = time.time()


def new_apple():
    global apple
    apple = Actor('apple')
    ok_apple_position = False
    while not ok_apple_position:
        ok_apple_position = True

        apple_start_pos_x = int(
            (random.randint(START_EDGE_APPLE_MARGIN,
                            WIDTH_IN_SPRITES - START_EDGE_APPLE_MARGIN - 1)
             + 0.5) * SNAKE_SPRITE_SIZE)
        apple_start_pos_y = int(
            (random.randint(START_EDGE_APPLE_MARGIN,
                            HEIGHT_IN_SPRITES - START_EDGE_APPLE_MARGIN - 1)
             + 0.5) * SNAKE_SPRITE_SIZE)

        for a_snake_part in snake:
            snake_part_pos_x = a_snake_part['pos'][0]
            snake_part_pos_y = a_snake_part['pos'][1]
            if (apple_start_pos_x == snake_part_pos_x and
                    apple_start_pos_y == snake_part_pos_y):
                ok_apple_position = False
                break
    apple.pos = (apple_start_pos_x, apple_start_pos_y)
    print('apple: start_pos_x:', start_pos_x, ', start_pos_y:', start_pos_y)


def draw_snake():
    global snake
    tail = len(snake)-1
    # print('\ndraw_snake-start: snake:\n', snake)

    snake[HEAD]['actor'] = Actor(
        '_'.join(['snake_head', snake[HEAD]['dir']]))
    snake[HEAD]['actor'].pos = snake[HEAD]['pos']
    snake[HEAD]['actor'].draw()

    snake[tail]['dir'] = (
        NORTH if (snake[tail-1]['pos'][1] - snake[tail]['pos'][1] ==
                  -SNAKE_SPRITE_SIZE)
        else SOUTH if (snake[tail-1]['pos'][1] - snake[tail]['pos'][1] ==
                       SNAKE_SPRITE_SIZE)
        else EAST if (snake[tail-1]['pos'][0] - snake[tail]['pos'][0] ==
                      SNAKE_SPRITE_SIZE)
        else WEST)
    snake[tail]['dir-head'] = snake[tail]['dir']
    snake[tail]['actor'] = Actor('_'.join(['snake_tail', snake[tail]['dir']]))
    snake[tail]['actor'].pos = snake[tail]['pos']
    snake[tail]['actor'].draw()

    for snake_part_no, _ in enumerate(snake[1: -1], 1):
        this_snake_part_pos = snake[snake_part_no]['pos']
        print('\nsnake_part_no:', snake_part_no)
        temp_snake_part = {'pos': this_snake_part_pos}
        snake[snake_part_no] = find_connecting_snake_part(
            snake[snake_part_no-1],
            temp_snake_part,
            snake[snake_part_no+1])
        snake[snake_part_no]['pos'] = this_snake_part_pos
        snake[snake_part_no]['actor'].pos = snake[snake_part_no]['pos']
        snake[snake_part_no]['actor'].draw()
    # print('\ndraw_snake-end: snake:\n', snake)


def grow_snake():
    global snake
    # head_dir = snake[HEAD]['dir']
    old_head_pos = snake[HEAD]['pos']
    snake[HEAD]['pos'] = (old_head_pos[0] + X_MOVE[snake[HEAD]['dir']],
                          old_head_pos[1] + Y_MOVE[snake[HEAD]['dir']])

    # First determine which piece to insert
    temp_snake_part = {'pos': old_head_pos}
    new_snake_part = find_connecting_snake_part(snake[HEAD],
                                                temp_snake_part,
                                                snake[1])
    new_snake_part['pos'] = old_head_pos
    snake.insert(1, new_snake_part)
    # print('\ngrow_snake-end: snake:', snake)


def find_connecting_snake_part(pre_snake_part,
                               this_snake_part,
                               post_snake_part):
    pre_snake_pos = pre_snake_part['pos']
    this_snake_pos = this_snake_part['pos']
    post_snake_pos = post_snake_part['pos']
    print('\npre_snake_pos:', pre_snake_pos,
          '\nthis_snake_pos:', this_snake_pos,
          '\npost_snake_pos:', post_snake_pos)
    pre_snake_part_dir = (
        SOUTH if (pre_snake_pos[1] - this_snake_pos[1] == -SNAKE_SPRITE_SIZE)
        else NORTH if (pre_snake_pos[1] - this_snake_pos[1] ==
                       SNAKE_SPRITE_SIZE)
        else WEST if (pre_snake_pos[0] - this_snake_pos[0] ==
                      SNAKE_SPRITE_SIZE)
        else EAST)
    post_snake_part_dir = (
        NORTH if (this_snake_pos[1] - post_snake_pos[1] == -SNAKE_SPRITE_SIZE)
        else SOUTH if (this_snake_pos[1] - post_snake_pos[1] ==
                       SNAKE_SPRITE_SIZE)
        else EAST if (this_snake_pos[0] - post_snake_pos[0] ==
                      SNAKE_SPRITE_SIZE)
        else WEST)

    # pre_snake_part_dir = pre_snake_part['dir-tail']
    # post_snake_part_dir = post_snake_part['dir-head']
    print('pre_snake_part_dir:', pre_snake_part_dir,
          '\npost_snake_part_dir:', post_snake_part_dir)
    if pre_snake_part_dir == OPP_DIR[post_snake_part_dir]:
        actor_file = ('snake_body_horiz'
                      if pre_snake_part_dir in ['east', 'west']
                      else 'snake_body_vert')
    elif (pre_snake_part_dir in [EAST, NORTH] and
          post_snake_part_dir in [EAST, NORTH]):
        actor_file = 'snake_body_1_30_turn'
    elif (pre_snake_part_dir in [EAST, SOUTH] and
          post_snake_part_dir in [EAST, SOUTH]):
        actor_file = 'snake_body_4_30_turn'
    elif (pre_snake_part_dir in [WEST, SOUTH] and
          post_snake_part_dir in [WEST, SOUTH]):
        actor_file = 'snake_body_7_30_turn'
    elif (pre_snake_part_dir in [WEST, NORTH] and
          post_snake_part_dir in [WEST, NORTH]):
        actor_file = 'snake_body_10_30_turn'
    else:
        actor_file = 'apple'  # to show logic errors

    return {'actor': Actor(actor_file),
            'dir':   post_snake_part_dir,
            'dir-head': OPP_DIR[pre_snake_part_dir],
            'dir-tail': OPP_DIR[post_snake_part_dir]}


def update_snake():  # Not sure if this is needed
    global snake, tail
    pass


def move_snake():
    global snake, turn_direction
    print('move_snake, turn_direction:', turn_direction)
    # print('\nmove_snake-start: snake:\n', snake)
    for snake_part_no_index, _ in enumerate(snake[-1:0:-1]):
        snake_part_no = len(snake) - snake_part_no_index - 1
        snake[snake_part_no]['pos'] = snake[snake_part_no-1]['pos']
    snake[HEAD]['dir'] = (turn_direction if turn_direction
                          else snake[HEAD]['dir'])
    snake[HEAD]['dir-tail'] = OPP_DIR[snake[HEAD]['dir']]
    snake[HEAD]['pos'] = (snake[HEAD]['pos'][0] + X_MOVE[snake[HEAD]['dir']],
                          snake[HEAD]['pos'][1] + Y_MOVE[snake[HEAD]['dir']])
    turn_direction = False
    # print('\nmove_snake-end: snake:\n', snake)
    draw_snake()
    print('end move_snake')



def apple_hit():
    global score, apple, snake_length, snake_move_duration
    print('\neat the apple\n')
    score += 1
    snake_length += 1
    grow_snake()
    snake_move_duration = snake_move_duration * (1 - SNAKE_MOVE_ACCEL)
    apple = None
    new_apple()


def handle_game_over():
    display_message('GAME OVER!', 'Try again.')
    if not high_score_updated:
        update_high_scores()
    # while not keyboard.SPACE:
    #     time.sleep(1)
    #     print('foo')
    # exit()


def display_message(heading_text, sub_heading_text):
    screen.draw.text(heading_text,
                     fontsize=60,
                     center=(CENTER_X, CENTER_Y/2),
                     color='yellow')
    screen.draw.text(sub_heading_text,
                     fontsize=30,
                     center=(CENTER_X, CENTER_Y/2 + 30),
                     color='yellow')


def update_high_scores():
    global scores, high_score_updated, high_scores, high_scores_ints
    scores = []
    with open(HS_FILENAME, 'r') as file:
        line = file.readline()
        high_scores = line.split()
        high_scores_ints = []
        # print('high_scores_ints:', high_scores_ints)
        for a_score in high_scores:
            try:
                high_scores_ints.append(int(a_score))
            except ValueError:
                print('Some scores in high score file are invalid, ignoring')
        high_scores_ints.append(score)
        # print('high_scores_ints:', high_scores_ints)
        high_scores_ints.sort(reverse=True)
        # print('high_scores_ints:', high_scores_ints)
        high_scores_ints = high_scores_ints[:MAX_SCORES_TO_KEEP]
        # print('high_scores_ints:', high_scores_ints)
        high_scores = ' '.join(list(map(str, high_scores_ints)))
        # print('new high scores:', high_scores)
    with open(HS_FILENAME, 'w') as file:
        file.write(high_scores)
    high_score_updated = True


def display_high_scores():
    screen.draw.text('HIGH SCORES',
                     fontsize=30,
                     center=(CENTER_X, HEIGHT * 5 / 8),
                     color='yellow')
    y = HEIGHT * 5 / 8 + 25
    for position, high_score in enumerate(high_scores_ints, 1):
        screen.draw.text(str(position) + '.  ' + str(high_score),
                         center=(CENTER_X - 10, y),
                         color='yellow')
        y += 25
        position += 1


def draw():  # Called whenever screen needs to be refreshed
    if not game_over:
        screen.fill('black')
        # update_snake()
        draw_snake()
        apple.draw()
        screen.draw.text('Score: ' + str(score), ((WIDTH / 2 - 40), 5),
                         color='yellow')
    elif high_score_updated:
        display_high_scores()


def update():  # Called once per frame (60), parameter is seconds
    global game_over, score, number_of_updates, turn_direction, start_time
    if game_over:
        handle_game_over()
        return
    # print(snake[HEAD]['actor'].top, snake[HEAD]['actor'].bottom,
    #       snake[HEAD]['actor'].left, snake[HEAD]['actor'].right)
    if (snake[HEAD]['actor'].top < CRASH_EDGE_MARGIN or
            snake[HEAD]['actor'].bottom > (HEIGHT - CRASH_EDGE_MARGIN) or
            snake[HEAD]['actor'].left < CRASH_EDGE_MARGIN or
            snake[HEAD]['actor'].right > (WIDTH - CRASH_EDGE_MARGIN)):
        print('ran into a wall. direction: ', snake[HEAD]['dir'])
        game_over = True
    for snake_part_no, _ in enumerate(snake[4:], 4):
        if snake[HEAD]['actor'].collidepoint(
                (snake[snake_part_no]['actor'].x,
                 snake[snake_part_no]['actor'].y)):
            print('ran into other part of snake. Part:', snake_part_no)
            game_over = True
    if snake[HEAD]['actor'].collidepoint(apple.x, apple.y):
        apple_hit()
    if keyboard.left:
        turn_direction = ('west' if snake[HEAD]['dir'] in ['north', 'south']
                          else False)
    elif keyboard.right:
        turn_direction = ('east' if snake[HEAD]['dir'] in ['north', 'south']
                          else False)
    elif keyboard.up:
        turn_direction = ('north' if snake[HEAD]['dir'] in ['east', 'west']
                          else False)
    elif keyboard.down:
        turn_direction = ('south' if snake[HEAD]['dir'] in ['east', 'west']
                          else False)
    elapsed_time = time.time() - start_time
    if elapsed_time > snake_move_duration:
        move_snake()
        start_time = time.time()

initiate()
# clock.schedule(handle_game_over, 10.0)

pgzrun.go()
