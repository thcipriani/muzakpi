#!/usr/bin/env python

import json
import logging
import math
import random
import time

import dothat.backlight as bl
import dothat.lcd as lcd
import dothat.touch as touch
import requests


RPC_ENDPOINT = 'http://localhost:6680/mopidy/rpc'
logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger()


class LcdScreen(object):
    """
    Abstraction for the lcd screen.
    """

    def __init__(self):
        pass

    def random_color(self, x):
        bl.sweep((x % 360) / 360.0)
        bl.set_graph(abs(math.sin(x / 100.0)))
        # bl.rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def show_track(self, artist='Unknown Artist', title='Unknown Title'):
        lcd.clear()
        lcd.write('{} - {}'.format(artist, title))


class Control(object):
    """
    Abstraction for button controls
    """
    
    def __init__(self):
        pass


    @touch.on(touch.RIGHT)
    def next_track(self):
        LOG.debug('TOUCHED RIGHT!!!!!!!!!!!!!!!')
        get_next_track()


class RPCInterface(object):
    """
    Handle RPC communication.
    """


def get_track():
    """
    Call get_current_track rpc endpoint.
    """
    payload = {
        'jsonrpc': '2.0',
        'id': '1',
        'method': 'core.playback.get_current_track'
    }
    r = requests.post(RPC_ENDPOINT, data=json.dumps(payload))
    r.raise_for_status()
    return r.json()


def get_next_track():
    """
    Call next_track rpc endpoint.
    """
    payload = {
        'jsonrpc': '2.0',
        'id': '1',
        'method': 'core.playback.next'
    }
    r = requests.post(RPC_ENDPOINT, data=json.dumps(payload))
    r.raise_for_status()
    return r.json()


def parse_track(track_info):
    """
    Attempt to parse the json output of the modipy rpc track object.
    """
    result = track_info.get('result')
    main_artist = result.get('artists', [{'name': 'Unknown Aritst'}])[0].get('name')
    title = result.get('name', 'Unknown Title')
    return main_artist, title


def main():
    lcd_screen = LcdScreen()
    controls = Control()
    x = 0
    while True:
        artist, title = parse_track(get_track())
        LOG.debug('Aritst: {}\nTitle: {}\nX: {}'.format(artist, title, x))

        lcd_screen.random_color(x)
        lcd_screen.show_track(artist, title)

        x += 10
        time.sleep(2)

if __name__ == '__main__':
    main()
