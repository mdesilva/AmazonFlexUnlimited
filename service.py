from flex import findJobs, logInfo
import time
import datetime
import sys

if __name__ == "__main__":
    resetTimeInSeconds = 1800
    username = sys.argv[1]
    password = sys.argv[2]
    desiredStartTime = int(sys.argv[3])
    desiredEndTime = int(sys.argv[4])
    desiredLocations= sys.argv[5].split(",")
    while True:
        logInfo(f"Starting job finder at {datetime.datetime.now()}")
        findJobs(username, password, desiredStartTime, desiredEndTime, desiredLocations)
        logInfo(f"Too many requests. Resuming in {resetTimeInSeconds / 60} minutes...Timestamp: {datetime.datetime.now()}")
        time.sleep(resetTimeInSeconds)