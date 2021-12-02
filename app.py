from lib.FlexUnlimited import FlexUnlimited, __getFilters
import os


if __name__ == "__main__":
  print("***Amazon Flex Unlimited v2*** \n")

  username, password = os.environ['AMZNFLEXUSERNAME'], os.environ["AMZNFLEXPWD"]
  (minBlockRate, arrivalBuffer, desiredWarehouses, desiredStartHour, desiredEndHour, retryLimit, twilioAcctSid,
   twilioAuthToken, twilioFromNumber, twilioToNumber) = __getFilters('filters.json')
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
