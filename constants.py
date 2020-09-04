headers = {
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

FlexLocations = {
     "2": "UNY1",
     "721061b3-a4f1-4244-99b3-a453c9cb864e": "C077",
     "acf06702-57ba-47f3-a34f-19e536a69fc0": "C506"
}