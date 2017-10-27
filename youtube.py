#!/usr/bin/env python

import subprocess

from flask import Flask, request
app = Flask('Youtuber')

@app.route('/bookmarklet')
def bookmarklet():
    return '''
<!doctype html>
<html>
<head>
    <meta charset="utf8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>YouTube Downloader</title>
</head>
<body>
<h1>Youtube Downloader</h1>
<p>
Bookmark  this page, click Edit... to edit the bookmark, and copy the text below into the URL field
</p>
<textarea style="width: 100%; height: 200px;">
javascript:location.href='{}download?page='+encodeURIComponent(location.href)
</textarea>
</body>
</html>
    '''.format(request.url_root)

@app.route('/')
def grab():
    return '''
<!doctype html>
<html>
<head>
    <meta charset="utf8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>YouTube Downloader</title>
</head>
<body>
<h1>Youtube Downloader</h1>
<form method="post" action="getAndTag">
<p>
<label for="artist">Arist</label>
<input type=text name=artist id=artist>
</p>
<p>
<label for="title">Title</label>
<input type=text name=title id=title>
</p>
<p>
<label for="url">URL</label>
<input name=url id=url type=text placeholder="youtube url">
</p>
<p>
<input type=submit>
</p>
</form>
</body>
</html>'''

@app.route('/getAndTag', methods=['POST'])
def get_and_tag():
    title = request.form['title']
    artist = request.form['artist']
    url = request.form['url']

    file_name = '/home/pi/Music/{}_{}.mp3'.format(artist, title)

    subprocess.check_call(['youtube-dl', '--extract-audio', '--audio-format', 'mp3', url, '--output', file_name])
    subprocess.check_call(['id3tag', '--artist={}'.format(artist), '--song={}'.format(title), file_name])
    subprocess.check_call(['sudo', 'mopidyctl', 'local', 'scan'])
    return "OK..."

@app.route('/download')
def download():
    page = request.args.get('page')
    if 'youtube' not in page and 'vimeo' not in page:
        return 'I only work for youtube type things'
    return '''
<!doctype html>
<html>
<head>
    <meta charset="utf8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>YouTube Downloader</title>
</head>
<body>
<h1>Youtube Downloader</h1>
<form method="post" action="getAndTag">
<p>
<label for="artist">Arist</label>
<input type=text name=artist id=artist>
</p>
<p>
<label for="title">Title</label>
<input type=text name=title id=title>
</p>
<input name=url id=url type=hidden value="{}">
<p>
<input type=submit>
</p>
</form>
</body>
</html>'''.format(page)

