import requests
import json
import datetime
import time
from sys import argv
from constants import headers, routes, FlexLocations
import subprocess
from subprocess import PIPE

def logInfo(info):
    print(info, flush=True)

def logError(errorMsg):
    print(f'ERROR: {errorMsg}', flush=True)

def getFlexHeaders(flexUser, flexPassword):
    """Returns http headers with fresh access token required to complete a Flex Capacity request"""
    flexHeaders = headers.get("FlexCapacityRequest")
    flexHeaders["x-amz-access-token"] = getAuthToken(flexUser, flexPassword) #getAuthTokenUsingCurl
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
   token = subprocess.run("/home/mdesilva/flexunlimited/auth.sh", shell=True, stdout=PIPE, stderr=PIPE)
   return token.stdout[1:-2].decode("utf-8")

def getOffers(flexHeaders):
    """
    Get job offers.
    
    Returns:
    Offers response object
    """
    flexHeaders["X-Amz-Date"] = getAmzDate() #must always be most up-to-date timestamp
    payload = {
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
    logInfo(f"Start timestamp {startTimestamp}")
    flexHeaders["X-Amz-Date"] = getAmzDate()
    request = requests.delete(f'https://flex-capacity-na.amazon.com/schedule/blocks/{startTimestamp}', headers=flexHeaders, json=payload)
    if (request.status_code == 200):
        logInfo(f"Successfully forfeited offer {offer.get('offerId')} due to {reasonForForfeit}")
        return True
    else:
        logInfo(f"Unable to forfeit offer {offer.get('offerId')}. Server returned status code {request.status_code}")
        logError(request.json())
        return False

def pruneOffersByLocation(flexHeaders, offers, desiredLocations):
    logInfo("Pruning any accepted offers by location...")
    remainingOffers = []
    for offer in offers:
        location = offer.get("serviceAreaId")
        if (location not in FlexLocations): #FlexLocations ONLY HAS THE 3 LOCATIONS WE CURRENTLY WANT. CHANGE THIS TO USE desiredLocations once we have all NYC locations
            if (not forfeitOffer(flexHeaders, offer, "unidentified location")):
                remainingOffers.append(offer)
        else:
            remainingOffers.append(offer)
    logInfo("Prune by location complete.")
    return remainingOffers

def pruneOffersByTime(flexHeaders, offers, desiredStartHour, desiredEndHour):
    logInfo("Pruning any accepted offers by time...")
    remainingOffers = []
    for offer in offers:
        endHour = datetime.datetime.fromtimestamp(offer.get("expirationDate")).hour
        if (endHour < desiredStartHour or endHour > desiredEndHour):
            if (not forfeitOffer(flexHeaders, offer, "time out of bounds")):
                remainingOffers.append(offer)
        else:
            remainingOffers.append(offer)
    logInfo("Prune by time complete.")
    return remainingOffers

def finishJobFinderCycle(flexHeaders, startTimestamp, endTimestamp, acceptedOffers, desiredStartHour, desiredEndHour):
    elapsedTime = (endTimestamp - startTimestamp)
    acceptedOffers = pruneOffersByTime(flexHeaders, acceptedOffers, desiredStartHour, desiredEndHour)
    logInfo(f"Accepted {len(acceptedOffers)} offers in {elapsedTime} seconds.")
    return 

def isValidOffer(offer, desiredStartHour, desiredEndHour):
    endHour = datetime.datetime.fromtimestamp(offer.get("expirationDate")).hour
    if (endHour < desiredStartHour or endHour > desiredEndHour):
        return False
    else:
        return True

def findJobs(username, password, desiredStartHour, desiredEndHour):
    flexHeaders = getFlexHeaders(username, password)
    retries = 0
    acceptedOffers = []
    startTimestamp = time.time()
    while(retries < 1000):
        offersResponse = getOffers(flexHeaders)
        if (offersResponse.status_code == 200):
            currentOffers = offersResponse.json().get("offerList")
            for offer in currentOffers:
                if(isValidOffer(offer, desiredStartHour, desiredEndHour)):                        
                    if (acceptOffer(flexHeaders, offer.get("offerId"))):
                        acceptedOffers.append(offer)
            retries += 1
        else:
            logError(offersResponse.json())
            return finishJobFinderCycle(flexHeaders, startTimestamp, time.time(), acceptedOffers, desiredStartHour, desiredEndHour)
    logInfo("Job search cycle ending...")
    return finishJobFinderCycle(flexHeaders, startTimestamp, time.time(), acceptedOffers, desiredStartHour, desiredEndHour)
