from bottle import route, run

@route("/")
def index():
    return "hello world"

# NOTE: host and port should come from config
run(host="0.0.0.0", port=8080)
