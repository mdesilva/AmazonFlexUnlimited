from flex import findJobs, logInfo
from db import getUser
import time
import datetime
from sys import argv

if __name__ == "__main__":
    resetTimeInSeconds = 1800
    username = argv[1]
    user = getUser(username)
    password = user.get("password")
    desiredStartTime = user.get("desiredStartTime")
    desiredEndTime = user.get("desiredEndTime")
    currentMinute = datetime.datetime.now().minute 
    #Wait until hour is approaching before starting job finder, as most jobs are found every half hour
    if (currentMinute != 59):
        timeToWait = 59 - currentMinute
        logInfo(f"Waiting for {timeToWait} minutes before starting job finder.")
        time.sleep(timeToWait * 60)
    while True:
        logInfo(f"Starting job finder at {datetime.datetime.now()} for {username}")
        findJobs(username, password, desiredStartTime, desiredEndTime)
        logInfo(f"Too many requests. Resuming in {resetTimeInSeconds / 60} minutes...Timestamp: {datetime.datetime.now()}")
        time.sleep(resetTimeInSeconds)
