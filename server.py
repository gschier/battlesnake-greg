from gevent import monkey

monkey.patch_all()

import json
import random
import sys

from bottle import request, route, run

from lib.constants import constants
from lib.move import next_move


@route('/')
def index():
    return json.dumps({
        'head': constants.SNAKE_HEAD,
        'taunt': '...zzz...'
    })


@route('/start', method='POST')
def start():
    return json.dumps({
        'name': constants.SNAKE_NAME,
        'head_url': constants.SNAKE_HEAD,
        'color': constants.SNAKE_COLOR,
        'taunt': '...zzz...'
    })


@route('/move', method='POST')
def move():
    move = next_move(request.json)

    return json.dumps(move)


@route('/end', method='POST')
def end():
    return json.dumps({})


# Expose WSGI app
port = 8081
ip = 'localhost'

if len(sys.argv) == 3:
    ip = sys.argv[1]
    port = int(sys.argv[2])

if ip == 'localhost':
    constants.SNAKE_NAME = '%s:%s' % (constants.SNAKE_NAME, port)
    constants.SNAKE_COLOR = 'rgba(%s,%s,%s,%s)' % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 100) / 100.0,
    )

run(host=ip, port=port, server='gevent')
