from datetime import datetime

from lib.Log import Log


class Offer:

    def __init__(self, offerResponseObject: object) -> None:
        self.id = offerResponseObject.get("offerId")
        self.expirationDate = datetime.fromtimestamp(offerResponseObject.get("expirationDate"))
        self.location = offerResponseObject.get('serviceAreaId')
        self.blockRate = float(offerResponseObject.get('rateInfo').get('priceAmount'))
        self.endTime = datetime.fromtimestamp(offerResponseObject.get('endTime'))
        self.hidden = offerResponseObject.get("hidden")
        self.ratePerHour = self.blockRate / ((self.endTime - self.expirationDate).seconds / 3600)
        self.weekday = self.expirationDate.weekday()
    
    def toString(self) -> str:
        blockDuration = (self.endTime - self.expirationDate).seconds / 3600

        body = 'Location: ' + self.location + '\n'
        body += 'Date: ' + str(self.expirationDate.month) + '/' + str(self.expirationDate.day) + '\n'
        body += 'Pay: ' + str(self.blockRate) + '\n'
        body += 'Pay rate per hour: ' + str(self.ratePerHour) + '\n'
        body += 'Block Duration: ' + str(blockDuration) + f'{"hour" if blockDuration == 1 else "hours"}\n'

        if not self.expirationDate.minute:
            body += 'Start time: ' + str(self.expirationDate.hour) + '00\n'
        elif self.expirationDate.minute < 10:
            body += 'Start time: ' + str(self.expirationDate.hour) + '0' + str(self.expirationDate.minute) + '\n'
        else:
            body += 'Start time: ' + str(self.expirationDate.hour) + str(self.expirationDate.minute) + '\n'

        if not self.endTime.minute:
            body += 'End time: ' + str(self.endTime.hour) + '00\n'
        elif self.endTime.minute < 10:
            body += 'End time: ' + str(self.endTime.hour) + '0' + str(self.endTime.minute) + '\n'
        else:
            body += 'End time: ' + str(self.endTime.hour) + str(self.endTime.minute) + '\n'

        return body
