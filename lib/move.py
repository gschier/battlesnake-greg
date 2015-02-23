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

    for point in points:
        if _is_on_board(gs, point) and not _is_snake(gs, point):
            count = count + 1

            # Add new position to snake
            snake = _get_snake(gs, constants.SNAKE_NAME)
            snake['coords'].insert(0, point)

            # Mark position on board
            gs['board'][point[0]][point[1]] = {
                'state': 'body',
                'snake': snake['name']
            }

            count = _count_moves(gs, point, count)

    return count


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


def _is_on_board(gs, point):
    if point[0] < 0 or point[1] < 0:
        return False

    if point[0] > len(gs['board']) - 1 or point[1] > len(gs['board'][0]) - 1:
        return False

    return True


def _is_snake(gs, point):
    for snake in gs['snakes']:
        # Ignore tails
        if point in snake['coords'][:-1]:
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


def _get_safe_points(gs, point, min_moves=None):
    points = _get_surrounding_points(gs, point)
    safe_points = []
    for point in points:
        num_moves = _count_moves(gs, point)
        if min_moves and num_moves < min_moves:
            print point, 'only has', num_moves, 'moves'
            continue
        if not _is_on_board(gs, point):
            print point, 'isnt on board'
            continue
        if _is_snake(gs, point):
            print point, 'is snake'
            continue

        safe_points.append(point)

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


def next(gs):
    snake = _get_snake(gs, constants.SNAKE_NAME)

    # Get the closest food
    head = snake['coords'][0]
    tail = snake['coords'][-1]

    # TODO: Choose food that's closest to your own body (Stay tight)
    food = _get_closest_food(gs, head)

    if _calc_distance(food, head) < len(gs['board']) / 4 or random.randint(0, 15) == 0:
        dest = food
    else:
        dest = tail

    print '--------------------------------------------------'
    print 'CURRENT HEAD', head
    print 'CLOSEST FOOD', food, _calc_distance(food, head)
    print 'CLOSEST DEST', dest

    # Get a direction vector ot the food (may be diagonal)
    move = _make_move_from_points(head, dest)
    next_point = _make_point(head, move)
    print 'NEXT POINT  ', next_point

    my_length = len(snake['coords'])
    safe_points = _get_safe_points(gs, head, min_moves=(my_length * 1.2))
    if len(safe_points) == 0:
        safe_points = _get_safe_points(gs, head, min_moves=my_length / 2)
        if len(safe_points) == 0:
            safe_points = _get_safe_points(gs, head, min_moves=10)
            if len(safe_points) == 0:
                safe_points = _get_safe_points(gs, head, min_moves=0)

    print 'SAFE POINTS ', safe_points
    if next_point not in safe_points:
        next_point = random.choice(safe_points)
        print 'SAFE POINT  ', next_point
        move = _make_move_from_points(head, next_point)

    print 'MOVE        ', move

    return {
        'move': _get_move(move),
        'taunt': None
    }


# Keep linter quiet
pprint('')
