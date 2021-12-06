#!/usr/bin/env python

from flask import Flask, render_template, url_for
from optparse import OptionParser
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('via.html')

if __name__ == '__main__':
    parser = OptionParser(usage='Usage: %prog [options]')
    parser.add_option('-l', '--listen', metavar='ADDRESS', dest='host', default='127.0.0.1', help='address to listen on [127.0.0.1]')
    parser.add_option('-p', '--port', metavar='PORT', dest='port', type='int', default=5000, help='port to listen on [5000]')
    # parser.add_option('-b', '--base_url', metavar='{base_url}', dest='BASE_URL', type='str', help='base_url')
    (opts, args) = parser.parse_args()
    # set options
    for k in dir(opts):
        if not k.startswith('_') and getattr(opts, k) is None:
            delattr(opts, k)
    app.config.from_object(opts)

    app.run(host=opts.host, port=opts.port, threaded=True)