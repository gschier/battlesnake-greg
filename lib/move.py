import copy
import math
import random

from pprint import pprint
from lib.constants import constants

moves = {
    0: {
        1: 'down',
        -1: 'up'
    },
    1: {0: 'right'},
    -1: {0: 'left'}
}


def _count_moves(gs, start, count=0):
    points = _get_surrounding_points(gs, start)

    if count == 0:
        gs = copy.deepcopy(gs)

    # Just so it's not too slow
    if count > 100:
        return count

    best_count = 0
    for point in points:
        if _is_on_board(gs, point) and not _is_snake(gs, point):
            # Add new position to snake
            snake = _get_snake(gs, constants.SNAKE_NAME)
            snake['coords'].insert(0, point)

            # Mark position on board
            gs['board'][point[0]][point[1]] = {
                'state': 'body',
                'snake': snake['name']
            }

            c = _count_moves(gs, point, count + 1)
            if c > best_count:
                best_count = c

    return count + best_count


def _calc_distance(a, b):
    x_2 = (b[0] - a[0]) ** 2
    y_2 = (b[1] - a[1]) ** 2

    return math.sqrt(math.fabs(y_2 + x_2))


def _remove_diagonals(vector):
    if random.randint(0, 1) == 0:
        # Choose x
        if vector[0] != 0:
            vector[1] = 0
    else:
        # Choose y
        if vector[1] != 0:
            vector[0] = 0

    return vector


def _make_direction_vector(point):
    x = point[0]
    y = point[1]

    if x > 0:
        x = 1
    elif x < 0:
        x = -1

    if y > 0:
        y = 1
    elif y < 0:
        y = -1

    return [x, y]


def _make_point(point, vector):
    x = point[0] + vector[0]
    y = point[1] + vector[1]
    return [x, y]


def _make_move_from_points(a, b):
    x = b[0] - a[0]
    y = b[1] - a[1]
    vector = _make_direction_vector([x, y])
    move = _remove_diagonals(vector)
    return move


def _has_just_eaten(snake):
    return snake['coords'][-1] == snake['coords'][-2]


def _is_on_board(gs, point):
    if point[0] < 0 or point[1] < 0:
        return False

    if point[0] > len(gs['board']) - 1 or point[1] > len(gs['board'][0]) - 1:
        return False

    return True


def _is_snake(gs, point):
    for snake in gs['snakes']:
        if _has_just_eaten(snake):
            # Don't ignore tail if has just eaten
            body = snake['coords'][:]
        else:
            body = snake['coords'][:-1]

        if point in body:
            return True

    return False


def _get_surrounding_points(gs, point):
    points = [
        [point[0] + 1, point[1]],
        [point[0] - 1, point[1]],
        [point[0], point[1] + 1],
        [point[0], point[1] - 1]
    ]

    return points


def _get_safe_points(gs, start, min_moves=None):
    points = _get_surrounding_points(gs, start)
    safe_points = []
    for point in points:
        num_moves = _count_moves(gs, point)
        if min_moves > 0 and num_moves < min_moves:
            continue
        if not _is_on_board(gs, point):
            continue
        if _is_snake(gs, point):
            continue

        safe_points.append(point)

    if min_moves > 0 and len(safe_points) == 0:
        # If no safe points found, try again with less precision
        return _get_safe_points(gs, start, min_moves / 2)

    return safe_points


def _get_move(vector):
    return moves[vector[0]][vector[1]]


def _get_snake(gs, snake_name):
    for snake in gs['snakes']:
        if snake['name'] == snake_name:
            return snake
    return None


def _get_closest_food(gs, point):
    closest = None

    for food in gs['food']:
        if not closest:
            closest = food
        elif _calc_distance(point, food) < _calc_distance(point, closest):
            closest = food

    return closest


def _chase_tail(gs, snake, head):
    tail = snake['coords'][-1]
    desired_move = _make_move_from_points(head, tail)
    desired_point = _make_point(head, desired_move)

    safe_points = _get_safe_points(gs, head, min_moves=0)

    print 'SAFE POINTS', safe_points

    if desired_point not in safe_points:
        safe_point = random.choice(safe_points)
        return _make_move_from_points(head, safe_point)
    else:
        return desired_move


def _stay_safe(gs, snake, head):
    tail = snake['coords'][-1]

    # TODO: Choose food that's closest to your own body (Stay tight)
    food = _get_closest_food(gs, head)
    food_distance = _calc_distance(food, head)
    if food_distance < 3 or random.randint(0, 15) == 0:
        dest = food
    else:
        dest = tail

    # Get a direction vector (might be diagonal)
    move = _make_move_from_points(head, dest)
    next_point = _make_point(head, move)

    my_length = len(snake['coords'])
    safe_points = _get_safe_points(gs, head, min_moves=(my_length * 2))

    print 'SNAKE', snake['coords']
    print 'HEAD', head
    print 'SAFE POINTS', safe_points

    if len(safe_points) and next_point not in safe_points:
        next_point = random.choice(safe_points)
        move = _make_move_from_points(head, next_point)

    return move


def next(gs):
    snake = _get_snake(gs, constants.SNAKE_NAME)
    print '----------------------------------------------------------'

    # Get the closest food
    head = snake['coords'][0]

    move = _stay_safe(gs, snake, head)
    # move = _chase_tail(gs, snake, head)
    print 'MOVE', move

    return {
        'move': _get_move(move),
        'taunt': None
    }


# Keep linter quiet
pprint('')
