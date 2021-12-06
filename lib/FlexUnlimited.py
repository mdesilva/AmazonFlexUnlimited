from requests.models import Response
from lib.Offer import Offer
from lib.Log import Log
import requests, time, os, sys, json
from datetime import datetime

try:
  from twilio.rest import Client
except:
  pass

class FlexUnlimited:
  allHeaders = {
    "AmazonApiRequest": {
      "x-amzn-identity-auth-domain": "api.amazon.com",
      "User-Agent": "AmazonWebView/Amazon Flex/0.0/iOS/15.2/iPhone"
    },
    "FlexCapacityRequest": {
      "Accept": "application/json",
      "x-amz-access-token": None,
      "Authorization": "RABBIT3-HMAC-SHA256 SignedHeaders=x-amz-access-token;x-amz-date, "
                       "Signature=82e65bd06035d5bba38c733ac9c48559c52c7574fb7fa1d37178e83c712483c0",
      "X-Amz-Date": None,
      "Accept-Encoding": "gzip, deflate, br",
      "x-flex-instance-id": "BEEBE19A-FF23-47C5-B1D2-21507C831580",
      "Accept-Language": "en-US",
      "Content-Type": "application/json",
      "User-Agent": "iOS/15.2 (iPhone Darwin) Model/iPhone Platform/iPhone13,3 RabbitiOS/2.88.2",
      "Connection": "keep-alive",
      "Cookie": 'session-id=147-7403990-6925948; session-id-time=2082787201l; '
                'session-token=1mGSyTQU1jEQgpSB8uEn6FFHZ1iBcFpe9V7LTPGa3GV3sWf4bgscBoRKGmZb3TQICu7PSK5q23y3o4zYYhP'
                '/BNB5kHAfMvWcqFPv/0AV7dI7desGjE78ZIh+N9Jv0KV8c3H/Xyh0OOhftvJQ5eASleRuTG5+TQIZxJRMJRp84H5Z+YI'
                '+IhWErPdxUVu8ztJiHaxn05esQRqnP83ZPxwNhA4uwaxrT2Xm; '
                'at-main="Atza|IwEBIB4i78dwxnHVELVFRFxlWdNNXzFreM2pXeOHsic9Xo54CXhW0m5juyNgKyCL6KT_9bHrQP7VUAIkxw'
                '-nT2JH12KlOuYp6nbdv-y6cDbV5kjPhvFntPyvBEYcl405QleSzBtH_HUkMtXcxeFYygt8l-KlUA8-JfEKHGD14'
                '-oluobSCd2UdlfRNROpfRJkICzo5NSijF6hXG4Ta3wjX56bkE9X014ZnVpeD5uSi8pGrLhBB85o4PKh55ELQh0fwuGIJyBcyWSpGPZb5'
                'uVODSsXQXogw7HCFEoRnZYSvR_t7GF5hm_78TluPKUoYzvw4EVfJzU"; '
                'sess-at-main="jONjae0aLTmT+yqJV5QC+PC1yiAdolAm4zRrUlcnufM="; '
                'ubid-main=131-1001797-1551209; '
                'x-main="ur180BSwQksvu@cBWH@IQejqHw6ZYkMDKkwbdOwJvEeVZWlh15tnxZdleqfq9qO0"'
    }
  }
  routes = {
    "GetOffers": "https://flex-capacity-na.amazon.com/GetOffersForProviderPost",
    "AcceptOffer": "https://flex-capacity-na.amazon.com/AcceptOffer",
    "GetAuthToken": "https://api.amazon.com/auth/register",
    "ForfeitOffer": "https://flex-capacity-na.amazon.com/schedule/blocks/"
  }

  def __init__(self) -> None:
    try:
      with open("config.json") as configFile:
        config = json.load(configFile)
        self.username = os.environ['AMZNFLEXUSERNAME']
        self.password = os.environ["AMZNFLEXPWD"]
        self.desiredWarehouses = config["desiredWarehouses"]  # list of warehouse ids
        self.minBlockRate = config["minBlockRate"]
        self.arrivalBuffer = config["arrivalBuffer"]
        self.desiredStartHour = config["desiredStartHour"]  # start hour in military time
        self.desiredEndHour = config["desiredEndHour"]  # end hour in military time
        self.retryLimit = config["retryLimit"]  # number of jobs retrieval requests to perform
        self.twilioFromNumber = config["twilioFromNumber"]
        self.twilioToNumber = config["twilioToNumber"]
        self.__retryCount = 0
        self.__acceptedOffers = []
        self.__startTimestamp = time.time()
        self.__requestHeaders = FlexUnlimited.allHeaders.get("FlexCapacityRequest")
        self.__requestHeaders["x-amz-access-token"] = self.__getFlexRequestAuthToken()

        twilioAcctSid = config["twilioAcctSid"] 
        twilioAuthToken = config["twilioAuthToken"]

        if twilioAcctSid != "" and twilioAuthToken != "" and self.twilioFromNumber != "" and self.twilioToNumber != "":
          self.twilioClient = Client(twilioAcctSid, twilioAuthToken)
        else:
          self.twilioClient = None
    except KeyError as nullKey:
      Log.error(f'{nullKey} was not set. Please setup FlexUnlimited as described in the README.')
      sys.exit()
    except FileNotFoundError:
      Log.error("Config file not found. Ensure a properly formatted 'config.json' file exists in the root directory.")
      sys.exit()


  def __getFlexRequestAuthToken(self) -> str:
    """
        Get authorization token for Flex Capacity requests
        Returns:
        An access token as a string
        """
    payload = {
      "requested_extensions": ["device_info", "customer_info"],
      "cookies": {
        "website_cookies": [],
        "domain": ".amazon.com"
      },
      "registration_data": {
        "domain": "Device",
        "app_version": "0.0",
        "device_type": "A3NWHXTQ4EBCZS",
        "os_version": "15.2",
        "device_serial": "B262D48AC3EA4671B288C20F406821B5",
        "device_model": "iPhone",
        "app_name": "Amazon Flex",
        "software_version": "1"
      },
      "auth_data": {
        "user_id_password": {
          "user_id": self.username,
          "password": self.password
        }
      },
      "user_context_map": {
        "frc": "AFgQ07+f4rZ1HkMDmsLeD9GlOFoIa9auy7p03s6CSDsZFiskgDYWhSIQyD7S8EUxSMGAGs1gf0e"
               "\/wlmnvGBZ2Jh7YkvVfXENXnwoQ12acgHysONHR\/oBMWPwNOBg+qY88UlNQ1RXNOv9fgMDJPjr5gvZJs3S5RY9RyAMg7H"
               "\/sSIEJ9j+TXIE+xnMZrT1lOpEMdQJHV53+pgcJEG2SB4kt8OraJqoZCt7A\/lyWO9RAL1gWlnhEHyEd3"
               "\/\/t8TNQBKXbjO2G9iFUQs\/s0VqVSchIVzOzT\/BRpe36iFW7XnbGU0N9Q5Y40m+M"
               "\/kxySQ3h5YWs9kl1PuLGTx3ql1ttSf7nSHLGj342KZJtK3oOjCxVrsjteGRyekpKe6Jagrssjq1QOVNIyRmU428fdl"
               "\/lWILDAnSFSMZNiOzzQ=="},
      "requested_token_type": ["bearer", "mac_dms", "website_cookies"]
    }
    try:
      response = requests.post(FlexUnlimited.routes.get("GetAuthToken"),
                               headers=FlexUnlimited.allHeaders.get("AmazonApiRequest"), json=payload).json()
      return response.get("response").get("success").get("tokens").get("bearer").get("access_token")
    except Exception as e:
      Log.error("Unable to authenticate to Amazon Flex. Please provide a valid Amazon Flex username and password.")
      sys.exit()

  @staticmethod
  def __getAmzDate() -> str:
    """
        Returns Amazon formatted timestamp as string
        """
    return datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

  def __getOffers(self) -> Response:
    """
        Get job offers.
    
        Returns:
        Offers response object
        """
    self.__requestHeaders["X-Amz-Date"] = FlexUnlimited.__getAmzDate()
    return requests.post(
      FlexUnlimited.routes.get("GetOffers"),
      headers=self.__requestHeaders,
      json={
        "serviceAreaIds": ["2"],
        "apiVersion": "V2"
      })

  def __acceptOffer(self, offer: Offer):
    self.__requestHeaders["X-Amz-Date"] = self.__getAmzDate()

    request = requests.post(
      FlexUnlimited.routes.get("AcceptOffer"),
      headers=self.__requestHeaders,
      json={"offerId": offer.id})

    if request.status_code == 200:
      self.__acceptedOffers.append(offer)
      if self.twilioClient is not None:
          self.twilioClient.messages.create(
            to=self.twilioToNumber,
            from_=self.twilioFromNumber,
            body=offer.toString())
      Log.info(f"Successfully accepted offer {offer.id}")
    else:
      Log.error(f"Unable to accept offer {offer.id}. Request returned status code {request.status_code}")

  def __processOffer(self, offer: Offer):
    offerStartHour = offer.expirationDate.hour

    if self.desiredWarehouses is not None:
      if offer.location not in self.desiredWarehouses:
        return

    if self.minBlockRate:
      if self.minBlockRate > offer.blockRate:
        return

    if self.arrivalBuffer:
      deltaTime = (offer.expirationDate - datetime.now()).seconds / 3600
      if deltaTime < self.arrivalBuffer:
        return

    if self.desiredStartHour is not None and self.desiredEndHour is not None:
      if not (self.desiredStartHour < offerStartHour < self.desiredEndHour):
        return

    self.__acceptOffer(offer)


  def run(self):
    Log.info("Starting job search...")
    while self.__retryCount < self.retryLimit:
      if not self.__retryCount % 50:
        print(self.__retryCount, 'requests attempted\n\n')

      offersResponse = self.__getOffers()
      if offersResponse.status_code == 200:
        currentOffers = offersResponse.json().get("offerList")
        currentOffers.sort(key=lambda pay: int(pay['rateInfo']['priceAmount']),
                           reverse=True)
        for offer in currentOffers:
          offerResponseObject = Offer(offerResponseObject=offer)
          self.__processOffer(offerResponseObject)
        self.__retryCount += 1
      else:
        Log.error(offersResponse.json())
        break
    Log.info("Job search cycle ending...")
    Log.info(f"Accepted {len(self.__acceptedOffers)} offers in {time.time() - self.__startTimestamp} seconds")
