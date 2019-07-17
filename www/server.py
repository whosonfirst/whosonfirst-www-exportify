#!/usr/bin/env python

import os
import sys
import logging
import geojson

import flask
import flask_cors
import werkzeug
import werkzeug.security

import mapzen.whosonfirst.validator
import mapzen.whosonfirst.export

app = flask.Flask(__name__)
flask_cors.CORS(app)

logging.basicConfig(level=logging.INFO)

@app.before_request
def init():

    vld_args = {
        'derive': False,
    }

    flask.g.validator = mapzen.whosonfirst.validator.validator(**vld_args)
    flask.g.exporter = mapzen.whosonfirst.export.string()

@app.route("/", methods=["POST"])
def index():

    raw = flask.request.data

    if len(raw) == 0:
        logging.info("Nothing to parse")
        flask.abort(400)

    try:
        data = geojson.loads(raw)
    except Exception, e:
        logging.error(e)
        flask.abort(400)

    try:
        report = flask.g.validator.validate_feature(data)

        if not report.ok():
            logging.info("Validation failed")
            flask.abort(400)

    except Exception, e:
        logging.error(e)
        flask.abort(500)

    try:
        f = flask.g.exporter.export_feature(data)
        return f, 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception, e:
        logging.error(e)
        flask.abort(500)

if __name__ == '__main__':

    import optparse
    import ConfigParser

    opt_parser = optparse.OptionParser()

    opt_parser.add_option('--host', dest='host', action='store', default='127.0.0.1', help='')
    opt_parser.add_option('--port', dest='port', action='store', default=7777, help='')
    opt_parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Be chatty (default is false)')

    options, args = opt_parser.parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    host = options.host
    port = int(options.port)

    # Seriously do not ever run this with 'debug=True' no matter
    # how tempting. It is a bad idea. It will make you sad.

    app.run(host=host, port=port, debug=False)
