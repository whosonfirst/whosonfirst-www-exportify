#!/usr/bin/env python

import os
import sys
import logging
import json

import flask
import werkzeug
import werkzeug.security
from flask_cors import cross_origin

import mapzen.whosonfirst.validate
import mapzen.whosonfirst.export

app = flask.Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.before_request
def init():

    vld_args = {
        'derive': False,
    }

    g.flask.exporter = mapzen.whosonfirst.export.base()
    g.flask.validator = mapzen.whosonfirst.validator.validator(**vld_args)

@app.route("/", methods=["POST"])
def index():

    raw = flask.request.data

    try:
        data = json.loads(raw)
    except Exception, e:
        logging.error(e)
        flask.abort(400)

    try:
        report = g.flask.validator.validate_feature(data)

        if not report.ok():
            flask.abort(400)

    except Exception, e:
        logging.error(e)
        flask.abort(500)

    feature = None

    try:
        feature = g.flask.exporter.export_feature(data)
    except Exception, e:
        logging.error(e)
        flask.abort(500)

    if not feature:
        flask.abort(400)

    flask.jsonify(feature)

if __name__ == '__main__':

    import optparse
    import ConfigParser

    opt_parser = optparse.OptionParser()

    opt_parser.add_option('-p', '--port', dest='port', action='store', default=7777, help='')
    opt_parser.add_option('-c', '--config', dest='config', action='store', default=None, help='')
    opt_parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Be chatty (default is false)')

    options, args = opt_parser.parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    cfg = ConfigParser.ConfigParser()
    cfg.read(options.config)

    os.environ['EXPORTIFY_SEARCH_HOST'] = cfg.get('search', 'host')
    os.environ['EXPORTIFY_SEARCH_PORT'] = cfg.get('search', 'port')
    os.environ['EXPORTIFY_SEARCH_INDEX'] = cfg.get('search', 'index')

    port = int(options.port)

    # Seriously do not ever run this with 'debug=True' no matter
    # how tempting. It is a bad idea. It will make you sad.

    app.run(port=port)

