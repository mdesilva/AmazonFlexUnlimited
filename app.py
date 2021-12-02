from lib.FlexUnlimited import FlexUnlimited
from getpass import getpass

if __name__ == "__main__":
  print("***Amazon Flex Unlimited v2*** \n")
  username = input("Amazon Flex Username: ")
  password = getpass("Amazon Flex Password: ")
  desiredWarehouses = input("List of desired warehouses to pick jobs from (comma-separated, no spaces)"
                            "Enter 'none' to opt out of this filter: ").split(",")
  desiredStartHour = input("Desired start hour in military (24hr) format. "
                           "Enter 'none' to opt out of this filter: ")
  desiredEndHour = input("Desired end hour in military (24hr) format. Enter 'none' to opt out of this filter: ")
  retryLimit = int(input("Retry limit (number of refreshes): "))
  minBlockRate = float(input('Minimum amount in dollars to accept a job. Enter 0 to opt out of this filter: '))
  arrivalBuffer = float(input("Amount of time in hours (e.g. 1.5 for 1 hour and 30 minutes) between current time "
                              "and start time of a block. Enter 0 to opt out of this filter: "))
  sendAcceptSMS = input('Do you have a twilio account and want to have an SMS message with details of accepted offers '
                        'sent to you? Enter "yes" or "no": ')

  if len(desiredWarehouses) == 1 and desiredWarehouses[0].lower() == 'none':
    desiredWarehouses = None

  if desiredStartHour.lower() == 'none':
    desiredStartHour = None
  else:
    desiredStartHour = int(desiredStartHour)

  if desiredEndHour.lower() == 'none':
    desiredEndHour = None
  else:
    desiredEndHour = int(desiredEndHour)

  if sendAcceptSMS.lower() == 'yes':
    twilioAcctSid = input("Enter your twilio account SID")
    twilioAuthToken = input("Enter your twilio Auth Token")
    twilioFromNumber = input('Enter the twilio phone number to send to your personal number')
    twilioToNumber = input('Enter your personal number')
  else:
    twilioAcctSid, twilioAuthToken, twilioFromNumber, twilioToNumber = None, None, None, None
  print("\n")
  flexUnlimited = FlexUnlimited(
    username=username,
    password=password,
    desiredWarehouses=desiredWarehouses,
    minBlockRate=minBlockRate,
    arrivalBuffer=arrivalBuffer,
    desiredStartHour=desiredStartHour,
    desiredEndHour=desiredEndHour,
    retryLimit=retryLimit,
    twilioAcctSid=twilioAcctSid,
    twilioAuthToken=twilioAuthToken,
    twilioFromNumber=twilioFromNumber,
    twilioToNumber=twilioToNumber
  )
  flexUnlimited.run()
