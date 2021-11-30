from FlexUnlimited import FlexUnlimited
from getpass import getpass

if __name__ == "__main__":
    print("***Amazon Flex Unlimited v2*** \n")
    username = input("Amazon Flex Username: ")
    password = getpass("Amazon Flex Password: ")
    desiredWarehouses = input("List of desired warehouses to pick jobs from (comma-separated, no spaces): ").split(",")
    desiredStartHour = int(input("Desired start hour in military (24hr) format: "))
    desiredEndHour = int(input("Desired end hour in military (24hr) format: "))
    retryLimit = int(input("Retry limit (number of refreshes): "))
    print("\n")
    flexUnlimited = FlexUnlimited(
        username=username,
        password=password,
        desiredWarehouses=desiredWarehouses,
        desiredStartHour=desiredStartHour,
        desiredEndHour=desiredEndHour,
        retryLimit=retryLimit
        )
    flexUnlimited.run()
    
