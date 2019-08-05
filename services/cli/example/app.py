from bottle import route, run

@route("/")
def index():
    return "hello world"

run(host="localhost", port=8080)
