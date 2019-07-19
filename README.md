# whosonfirst-www-exportify

Expose the `py-mapzen-whosonfirst-export` functionality as an HTTP endpoint.

## Description

This allows you `POST` a Who's On First (WOF) GeoJSON document to a local HTTP
server and have it "exportified" which means that it's ready to be included in a
commit or pull request in a
[https://github.com/whosonfirst-data](whosonfirst-data) repository.

When a WOF record is "exportified" a number of derived properties are
automatically updated (for example `wof:belongsto`, `src:geom_hash` and
`wof:lastmodified`) and the document is formatted according to the WOF style
guide (specifically that GeoJSON properties but _not_ geometries be indented).

This package is just a small Flask application build on top of the
[py-mapzen-whosonfirst-export](https://github.com/whosonfirst/py-mapzen-whosonfirst-export)
library and is used by the
[docker-whosonfirst-exportify](https://github.com/whosonfirst/docker-whosonfirst-exportify)
container but you can also use it as a standalone HTTP server if you want to.

## Example

```
$> ./www/server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
INFO:werkzeug: * Running on http://127.0.0.1:7777/ (Press CTRL+C to quit)
INFO:werkzeug:127.0.0.1 - - [17/Jul/2019 08:11:05] "POST / HTTP/1.1" 200 -
```			

```
$> curl -s -X POST -H "Content-Type: application/json" -d @101736545.geojson localhost:7777 | jq '.properties["wof:name"]'
"Montreal"
```

## See also

* https://github.com/whosonfirst/py-mapzen-whosonfirst-validator
* https://github.com/whosonfirst/py-mapzen-whosonfirst-export
* https://github.com/whosonfirst/docker-whosonfirst-exportify
* https://flask.palletsprojects.com/
