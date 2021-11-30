from requests.models import Response
from lib.Offer import Offer
from lib.Log import Log
import requests
import datetime
import time
import sys

class FlexUnlimited:

    allHeaders = {
    "AmazonApiRequest": {
        "x-amzn-identity-auth-domain": "api.amazon.com",
        "User-Agent": "AmazonWebView/Amazon Flex/0.0/iOS/13.6/iPhone"
    },
    "FlexCapacityRequest": {
        "Accept": "application/json",
        "x-amz-access-token": None,
        "Authorization": "RABBIT3-HMAC-SHA256 SignedHeaders=x-amz-access-token;x-amz-date,Signature=13956353d663d0e0285b9fe033600f6aa349141b4927b8f00dc4d8688803fe22",
        "X-Amz-Date": None,
        "Accept-Encoding": "gzip, deflate, br",
        "x-flex-instance-id": "BEEBE19A-FF23-47C5-B1D2-21507C831580",
        "Accept-Language": "en-US",
        "Content-Type": "application/json",
        "User-Agent":  "iOS/13.6 (iPhone Darwin) Model/iPhone Platform/iPhone12,1 RabbitiOS/2.63.1",
        "Connection": "keep-alive",
        "Cookie": 'at-main="Atza|IwEBID6-c-dyE3qRaNz-TFhETWU5uiyXXekimNY3tVY12ai0kq1S0hluo9IaJWlGuH-7fgPyimbyvWFtPPxTjjS8aurbzzEJhAW0MsIHJYYYwZEEQIWyKsaW82olcMjKVmCZdy7hkxANRiNLioEVcwQvDPLtrVGijRoKspT1zpHULgG9Q2jxiDMxaht974DoChDYpn_6bbozrPDM_HMhENRqEW6ntnUjUNa9Siv9fxyBJma0AbMFqxFpdZAlCwjhnOTiWvc"; sess-at-main="HaUexuByh5iTAwNf0oNIlyTraGUTR1BJCf5Qc+CWuGg="; session-id=141-6691796-2206425; ubid-main=130-2521667-2032303; x-main="wP5g2jxnzyFZW1RSW66zx@tF9SegMprjUpUjp6nrMaIdSz99EUE3ZaT7UEdwli5i"'
    },
}

    routes = {
        "GetOffers": "https://flex-capacity-na.amazon.com/GetOffersForProviderPost",
        "AcceptOffer": "https://flex-capacity-na.amazon.com/AcceptOffer",
        "GetAuthToken": "https://api.amazon.com/auth/register",
        "ForfeitOffer": "https://flex-capacity-na.amazon.com/schedule/blocks/"
    }

    def __init__(self, username, password, desiredWarehouses, desiredStartHour, desiredEndHour, retryLimit) -> None:
        self.username = username
        self.password = password
        self.desiredWarehouses = desiredWarehouses #list of warehouse ids
        self.desiredStartHour = desiredStartHour #start hour in military time
        self.desiredEndHour = desiredEndHour #end hour in military time
        self.retryLimit = retryLimit #number of jobs retrieval requests to perform
        self.__retryCount = 0
        self.__acceptedOffers = []
        self.__startTimestamp = time.time()
        self.__requestHeaders = FlexUnlimited.allHeaders.get("FlexCapacityRequest")
        self.__requestHeaders["x-amz-access-token"] = self.__getFlexRequestAuthToken()


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
                "os_version": "13.6",
                "device_serial": "02BD3E1B2F1A45F59B6D1BBB4A7DD96E",
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
                "frc": "AHrt\/FkKyrMPP\/x9r3kbbMPySlIu8ikMCA9fmU5Lw5ZciJ220vhy\/zAhTPZhs1Z2Sxr0dsp9HGaMfbsboUKzZlb2eEsz1j58hiYVnCiY6U38iswsCzgrElj9D+tNOkiQDIjYdT7NExGhMIHs\/bH+gulMpPJSKoTJRuCCaIKyTjxKUvWv060XXnTLwmWZiBfJDzkWE90GFt0SZ78nCdolFEmyb0UyyUnajxqXwdRz4Ypdr2vbEl6b1PEgMu2E32cs8mMoM2aHu+ah1YeupM\/y7D4LnDS1tZiDwNh4mtolsHiJBTmsGrJWTuOZbXsm9MK6m+1UPRSNHVk2YBNtF6tWf98Yly37txZygN7sxWbe\/YH0BBOfT3SB7rcvIoz4RckX6n8dlav7TBLsCKKC0ijubkPvTRIIrlggCg=="
            },
            "requested_token_type": ["bearer", "mac_dms", "website_cookies"]
        }
        try:
            response = requests.post(FlexUnlimited.routes.get("GetAuthToken"), headers=FlexUnlimited.allHeaders.get("AmazonApiRequest"), json=payload).json()
            return response.get("response").get("success").get("tokens").get("bearer").get("access_token")
        except Exception as e:
            Log.error(e)
            Log.error("Unable to authenticate to Amazon Flex. Please provide a valid Amazon Flex username and password.")
            sys.exit()

    
    def __getAmzDate(self) -> str:
        """
        Returns Amazon formatted timestamp as string
        """
        return datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

    def __getOffers(self) -> Response:
        """
        Get job offers.
    
        Returns:
        Offers response object
        """
        self.__requestHeaders["X-Amz-Date"] = self.__getAmzDate()
        return requests.post(
            FlexUnlimited.routes.get("GetOffers"), 
            headers=self.__requestHeaders, 
            json= { 
                "serviceAreaIds": ["2"],
                "apiVersion": "V2"
            })
    
    def __acceptOffer(self, offer: Offer):
        self.__requestHeaders["X-Amz-Date"] = self.__getAmzDate()
        request = requests.post(
            FlexUnlimited.routes.get("AcceptOffer"), 
            headers=self.__requestHeaders,
            json={"offerId": offer.id})
        if (request.status_code == 200):
            self.__acceptedOffers.append(offer)
            Log.info(f"Successfully accepted offer {offer.id}")
        else:
            Log.error(f"Unable to accept offer {offer.id}. Request returned status code {request.status_code}")
        
    
    def __processOffer(self, offer: Offer):
        offerEndHour = datetime.datetime.fromtimestamp(offer.expirationDate).hour
        if (offerEndHour > self.desiredStartHour and offerEndHour < self.desiredEndHour):
            self.__acceptOffer(offer)
    
    def run(self):
        Log.info("Starting job search...")
        while(self.__retryCount < self.retryLimit):
            offersResponse = self.__getOffers()
            if (offersResponse.status_code == 200):
                for offer in offersResponse.json().get("offerList"):
                    self.__processOffer(Offer(offerResponseObject=offer))
                self.__retryCount += 1
            else:
                Log.error(offersResponse.json())
                break
        Log.info("Job search cycle ending...")
        Log.info(f"Accepted {len(self.__acceptedOffers)} offers in {time.time() - self.__startTimestamp} seconds")
        return
