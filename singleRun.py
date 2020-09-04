from sys import argv
from flex import logInfo, findJobs
import datetime

if __name__ == "__main__":
    username = argv[1]
    password = argv[2]
    desiredStartTime = int(argv[3])
    desiredEndTime = int(argv[4])
    desiredLocations= argv[5].split(",")
    logInfo(f"Starting job finder at {datetime.datetime.now()}")
    findJobs(username, password, desiredStartTime, desiredEndTime, desiredLocations)
    logInfo(f"Job finder run complete")