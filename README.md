# whosonfirst-www-exportify

Expose the `py-mapzen-whosonfirst-export` functionality as an HTTP endpoint.

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
