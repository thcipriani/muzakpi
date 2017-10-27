#!/usr/bin/env python

import os
import subprocess

from flask import Flask, request, render_template, flash, redirect, url_for

HOME = os.path.join('/home', 'pi')
BASE_PATH = os.path.realpath(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(BASE_PATH, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_PATH)

# This is the secret from the flask docs. This seems dumb, BUT!!! it's only on
# a local network so ¯\_(ツ)_/¯
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/bookmarklet')
def bookmarklet():
    return render_template('bookmark.html')

@app.route('/')
def index():
    return render_template('add.html')

@app.route('/getAndTag', methods=['POST'])
def get_and_tag():
    title = request.form['title']
    artist = request.form['artist']
    url = request.form['url']

    if not title or not artist or not url:
        flash('You did it wrong')
        return redirect(url_for('index'))

    file_name = os.path.join(
        HOME,
        'Music',
        '{} - {}.%(ext)s'.format(artist, title)
    )

    final_file = file_name % {'ext': 'mp3'}

    try:
        subprocess.check_call(['youtube-dl', '--extract-audio', '--audio-format', 'mp3', url, '--output', file_name])
        subprocess.check_call(['id3tag', '--artist={}'.format(artist), '--song={}'.format(title), final_file])
        subprocess.check_call(['sudo', 'mopidyctl', 'local', 'scan'])
    except:
        flash('an error occurred!')
        return redirect(url_for('index'))

    flash('SUCCESS!! Added "{} - {}" to library!'.format(artist, title))
    return redirect(url_for('index'))

@app.route('/download')
def download():
    page = request.args.get('page')
    return render_template('add.html', page=page)
