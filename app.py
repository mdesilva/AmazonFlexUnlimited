from FlexJobFinder import FlexJobFinder
from getpass import getpass

if __name__ == "__main__":
    print("***Amazon Flex Unlimited v2*** \n")
    username = input("Amazon Flex Username: ")
    password = getpass.getpass("Amazon Flex Password: ")
    desiredWarehouses = input("List of desired warehouses to pick jobs from (comma-separated, no spaces): ").split(",")
    desiredStartHour = input("Desired start hour in military (24hr) format: ")
    desiredEndHour = input("Desired end hour in military (24hr) format: ")
    retryLimit = input("Retry limit (number of refreshes): ")
    jobFinder = FlexJobFinder(
        username=username,
        password=password,
        desiredWarehouses=desiredWarehouses,
        desiredStartHour=desiredStartHour,
        desiredEndHour=desiredEndHour,
        retryLimit=retryLimit
        )
    jobFinder.run()
    
