from datetime import datetime


class Offer:
    def __init__(self, offer_information: object) -> None:
        self.id             = offer_information.get("offerId")
        self.expirationDate = datetime.fromtimestamp(offer_information.get("expirationDate"))
        self.startTime      = datetime.fromtimestamp(offer_information.get("startTime"))
        self.location       = offer_information.get('serviceAreaId')
        self.blockRate      = float(offer_information.get('rateInfo').get('priceAmount'))
        self.endTime        = datetime.fromtimestamp(offer_information.get('endTime'))
        self.hidden         = offer_information.get("hidden")
        self.ratePerHour    = self.blockRate / ((self.endTime - self.startTime).seconds / 3600)
        self.weekday        = self.expirationDate.weekday()
    
    def __srt__(self) -> str:
        blockDuration = (self.endTime - self.startTime).seconds / 3600

        body = (
            f'Location:       {self.location}\n'
            f'Date:           {self.startTime.strftime("%m/%d")}\n'
            f'Total Pay:      {self.blockRate}\n'
            f'Hourly Rate:    {self.ratePerHour}\n'
            f'Block Duration: {blockDuration} hour(s)\n'
            f'Start Time:     {self.startTime.strftime("%H:%M")}\n'
            f'End Time:       {self.endTime.strftime("%H:%M")}\n'
        )

        return body
