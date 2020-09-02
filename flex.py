import requests
import json
import datetime
import time
from sys import argv
from constants import headers, routes
import subprocess
from subprocess import PIPE

def logInfo(info):
    print(info, flush=True)

def getFlexHeaders(flexUser, flexPassword):
    """Returns http headers with fresh access token required to complete a Flex Capacity request"""
    flexHeaders = headers.get("FlexCapacityRequest")
    flexHeaders["x-amz-access-token"] = getAuthTokenUsingCurl()
    return flexHeaders

def getAmzDate():
    """Returns Amazon formatted timestamp as string"""
    return datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

def getAuthToken(username, password):
    """
    Get authorization token for Flex Capacity requests

    Args:
    username: Flex username
    password: Flex password

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
                "user_id": username,
                "password": password
            }
        },
        "user_context_map": {
            "frc": "AHrt\/FkKyrMPP\/x9r3kbbMPySlIu8ikMCA9fmU5Lw5ZciJ220vhy\/zAhTPZhs1Z2Sxr0dsp9HGaMfbsboUKzZlb2eEsz1j58hiYVnCiY6U38iswsCzgrElj9D+tNOkiQDIjYdT7NExGhMIHs\/bH+gulMpPJSKoTJRuCCaIKyTjxKUvWv060XXnTLwmWZiBfJDzkWE90GFt0SZ78nCdolFEmyb0UyyUnajxqXwdRz4Ypdr2vbEl6b1PEgMu2E32cs8mMoM2aHu+ah1YeupM\/y7D4LnDS1tZiDwNh4mtolsHiJBTmsGrJWTuOZbXsm9MK6m+1UPRSNHVk2YBNtF6tWf98Yly37txZygN7sxWbe\/YH0BBOfT3SB7rcvIoz4RckX6n8dlav7TBLsCKKC0ijubkPvTRIIrlggCg=="
        },
        "requested_token_type": ["bearer", "mac_dms", "website_cookies"]
    }
    response = requests.post(routes.get("GetAuthToken"), headers=headers.get("AmazonApiRequest"), json=payload).json()
    return response.get("response").get("success").get("tokens").get("bearer").get("access_token")

def getAuthTokenUsingCurl():
   token = subprocess.run("./auth.sh", shell=True, stdout=PIPE, stderr=PIPE)
   return token.stdout[1:-2].decode("utf-8")

def getOffers(flexHeaders):
    """
    Get job offers.
    
    Returns:
    Offers response object
    """
    flexHeaders["X-Amz-Date"] = getAmzDate() #must always be most up-to-date timestamp
    payload = {
        "filters": {
            "timeFilter": {
                "endTime": "13:00",
                "startTime": "07:00"
            },
            "serviceAreaFilter": ["2", "721061b3-a4f1-4244-99b3-a453c9cb864e"]
        },
        "serviceAreaIds": ["2"],
        "apiVersion": "V2"
    }
    request =  requests.post(routes.get("GetOffers"), headers=flexHeaders, json=payload)
    return request

def acceptOffer(flexHeaders, id):
    """
    Try to accept offer

    Args:
    flexHeaders: Valid flex headers 
    id: offer id as string

    Returns:
    True if offer was accepted successfully, False otherwise
    """
    flexHeaders["X-Amz-Date"] = getAmzDate() #must always be most up-to-date timestamp
    payload = {
        "offerId": id
    }
    request = requests.post(routes.get("AcceptOffer"), headers=flexHeaders, json=payload)
    if (request.status_code == 200):
        logInfo(f"Successfully accepted offer {id}")
        return True
    else:
        logInfo(request.status_code)
        logInfo(f"Unable to get offer {id}")
        return False

def forfeitOffer(flexHeaders, offer, reasonForForfeit):
    startTimestamp = int(datetime.datetime.fromtimestamp(offer.get("startTime")).timestamp())
    payload = {
        "pickUpTime": startTimestamp
    }
    flexHeaders["X-Amz-Date"] = getAmzDate()
    request = requests.delete(f'{routes.get("ForfeitOffer")}{startTimestamp}', headers=flexHeaders, json=payload)
    if (request.status_code == 200):
        logInfo(f"Successfully forfeited offer {id} due to {reasonForForfeit}")
        return True
    else:
        logInfo(f"Unable to forfeit offer {id}. Server returned status code {request.status_code}")
        return False

def pruneOffersByLocation(flexHeaders, offers, desiredLocations):
    for offer in offers:
        if (offer.get("serviceAreaId") not in desiredLocations):
            forfeitOffer(flexHeaders, offer)

def pruneOffersByTime(flexHeaders, offers, desiredStartHour, desiredEndHour):
    logInfo("Pruning any accepted offers by time...")
    for offer in offers:
        endHour = datetime.datetime.fromtimestamp(offer.get("expirationDate")).hour
        if (endHour < desiredStartHour or endHour > desiredEndHour):
            forfeitOffer(flexHeaders, offer)
    logInfo("Prune by time complete.")

def findJobs(username, password, desiredStartHour, desiredEndHour):
    flexHeaders = getFlexHeaders(username, password)
    acceptedOfferCount = 0
    acceptedOffers = []
    startTimestamp = time.time()
    while(True):
        offersResponse = getOffers(flexHeaders)
        if (offersResponse.status_code == 200):
            currentOffers = offersResponse.json().get("offerList")
            for offer in currentOffers:
                if (acceptOffer(flexHeaders, offer.get("offerId"))):
                    acceptedOfferCount += 1
                    acceptedOffers.append(offer)
        else:
            endTimestamp = time.time()
            elapsedTime = (endTimestamp - startTimestamp)
            pruneOffersByTime(flexHeaders, acceptedOffers, desiredStartHour, desiredEndHour)
            return f"Accepted {acceptedOfferCount} offers in {elapsedTime} seconds."
