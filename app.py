from flask import Flask, request, make_response
from system import startService, stopService, getLogs
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Flex utility server running"

@app.route("/start", methods=["POST"])
def startServiceRoute():
    username = request.form["username"]
    try:
        startService(username)
        return make_response("Service started", 200)
    except Exception as e:
        print(e)
        return make_response("An error occurred when starting the service", 500)

@app.route("/stop", methods=["POST"])
def stopServiceRoute():
    username = request.form["username"]
    try:
        stopService(username)
        return make_response("Service stopped", 200)
    except Exception as e:
        print(e)
        return make_response("An error occurred when stopping the service", 500)

@app.route("/logs", methods=["GET"])
def getLogsRoute():
    username = request.args.get("username")
    try:
        return make_response(getLogs(username), 200)
    except Exception as e:
        print(e)
        return make_response("An error occurred.", 500)
        