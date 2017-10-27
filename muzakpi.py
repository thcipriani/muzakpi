#!/usr/bin/env python

import copy
import json
import logging
import math
import random
import time

import dothat.backlight as bl
import dothat.lcd as lcd
import dothat.touch as touch
import requests


JSON_PAYLOAD = {
    'jsonrpc': '2.0',
    'id': '1',
}


JSON_ENDPOINT = 'http://localhost:6680/mopidy/rpc'


logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger()


class YouTuber(object):
    """
    Flask app for adding tracks via youtube
    """
    pass


class LcdScreen(object):
    """
    Abstraction for the lcd screen.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        lcd.clear()
        bl.set_graph(0.0)
        bl.off()

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

    def _parse_track(self, track_info):
        """
        Attempt to parse the json output of the modipy rpc track object.
        """
        result = track_info.get('result')
        if result is None:
            return None, None
        main_artist = result.get('artists', [{'name': 'Unknown Aritst'}])[0].get('name')
        title = result.get('name', 'Unknown Title')
        return main_artist, title

    @property
    def current_track(self):
        return self._parse_track(current_track())

    @property
    def artist(self):
        artist, _ = self.current_track()
        return artist

    @property
    def title(self):
        _, title = self.current_track()
        return title

    @touch.on(touch.RIGHT)
    def next_track(self):
        LOG.debug('TOUCHED RIGHT!!!!!!!!!!!!!!!')
        next_track()

    @touch.on(touch.LEFT)
    def next_track(self):
        LOG.debug('TOUCHED LEFT!!!!!!!!!!!!!!!')
        previous_track()

    @touch.on(touch.BUTTON)
    def next_track(self):
        LOG.debug('BUTTON TOUCHED!!!!!!!!!!!!!!!')
        play_pause()

    @touch.on(touch.CANCEL)
    def next_track(self):
        LOG.debug('CANCEL TOUCHED!!!!!!!!!!!!!!!')


def current_track():
    return _rpc_call()


def next_track():
    return _rpc_call(method='core.playback.next')


def previous_track():
    return _rpc_call(method='core.playback.previous')


def play_pause():
    if is_playing():
        return _rpc_call(method='core.playback.pause')

    return _rpc_call(method='core.playback.play')


def is_playing():
    state = _rpc_call(method='core.playback.get_state')
    return state.get('result') == 'playing'


def _rpc_call(method='core.playback.get_current_track'):
    payload = copy.deepcopy(JSON_PAYLOAD)
    payload['method'] = method
    r = requests.post(JSON_ENDPOINT, data=json.dumps(payload))
    r.raise_for_status()
    return r.json()


def main():
    lcd_screen = LcdScreen()
    controls = Control()
    x = 0
    while True:
        if not is_playing():
            lcd_screen.reset()

        else:
            artist, title = controls.current_track
            LOG.debug('Aritst: {}\nTitle: {}\nX: {}'.format(artist, title, x))

            lcd_screen.random_color(x)
            lcd_screen.show_track(artist, title)

            x += 10
            if x >= 360:
                x = 0
        time.sleep(2)

if __name__ == '__main__':
    main()
