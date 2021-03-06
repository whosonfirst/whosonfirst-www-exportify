#!/usr/bin/env python

import os
import sys
import logging
import geojson
import io

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
        flask.abort(400, "Nothing to exportify")

    try:
        data = geojson.loads(raw)
    except Exception as e:
        logging.error(e)
        flask.abort(400, "Invalid GeoJSON")

    try:
        report = flask.g.validator.validate_feature(data)
    except Exception as e:
        logging.error(e)
        flask.abort(500, "Failed to validate GeoJSON")

    if not report.ok:
        logging.info("Validation failed")

        fh = io.StringIO()
        report.print_report(fh)

        flask.abort(400, fh.getvalue())
            
    try:
        f = flask.g.exporter.export_feature(data)
        return f, 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        logging.error(e)
        flask.abort(500, "Failed to export GeoJSON")

@app.route("/ping", methods=["GET"])
def ping():
    return "PONG"

# this is so we can specify custom max_content_length settings when
# running under gunicorn: https://github.com/benoitc/gunicorn/issues/135
# for example: $> gunicorn 'server:app_with_max_content_length(2097152)'

def app_with_max_content_length(len):
    app.config['MAX_CONTENT_LENGTH'] = int(len)
    return app

if __name__ == '__main__':

    import optparse

    opt_parser = optparse.OptionParser()

    opt_parser.add_option('--host', dest='host', action='store', default='127.0.0.1', help='')
    opt_parser.add_option('--port', dest='port', action='store', default=7777, help='')
    opt_parser.add_option('--max-content-length', dest='max_content_length', action='store', default=1048576, help='')
    opt_parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Be chatty (default is false)')

    options, args = opt_parser.parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    host = options.host
    port = int(options.port)
    max_content = int(options.max_content_length)

    # https://flask.palletsprojects.com/en/1.0.x/patterns/fileuploads/
    app.config['MAX_CONTENT_LENGTH'] = max_content

    # Seriously do not ever run this with 'debug=True' no matter
    # how tempting. It is a bad idea. It will make you sad.

    app.run(host=host, port=port, debug=False)
