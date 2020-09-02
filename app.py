from flask import Flask, request, make_response
from flex import scheduleCronJobToLookForFlexJobs
app = Flask(__name__)

"""
Should execute job search, and return list of accepted offers
"""
@app.route("/findJobs", methods=["GET"])
def findJobsRoute():
    username = request.args.get("username")
    password = request.args.get("password")
    if (username and password):
        return(scheduleCronJobToLookForFlexJobs(username, password))
    else:
        return make_response("Need username and password", 400)

@app.route("/", methods=["GET"])
def index():
    return "Flex utility server running"