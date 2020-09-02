from flex import findJobs, logInfo
import time
import datetime

if __name__ == "__main__":
    while True:
        logInfo(f"Starting job finder at {datetime.datetime.now()}")
        findJobs("thushara70@ymail.com", "manuja98", 7, 13)
        logInfo(f"Too many requests. Resuming in 1 hour...Timestamp: {datetime.datetime.now()}")
        time.sleep(3600)