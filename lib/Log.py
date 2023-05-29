from datetime import datetime
import requests

class Log:
    @staticmethod 
    def info(message: str, flexClass):
        if(flexClass.notifications['info']):
            requests.post("https://ntfy.sh/" + flexClass.ntfyChannel, data = message.encode(encoding="utf-8"))

        if(flexClass.logging['info']):
            print(f'['+str(datetime.now())+'] INFO: '+message, flush=True)

    @staticmethod 
    def success(message: str, flexClass):
        if(flexClass.notifications['error']):
            requests.post("https://ntfy.sh/" + flexClass.ntfyChannel, data = message.encode(encoding="utf-8"))

        if(flexClass.logging['success']):
            print(f'\n['+str(datetime.now())+'] SUCCESS: '+message+'\n', flush=True)

    @staticmethod 
    def notice(message: str, flexClass):
        if(flexClass.notifications['error']):
            requests.post("https://ntfy.sh/" + flexClass.ntfyChannel, data = message.encode(encoding="utf-8"))

        if(flexClass.logging['notice']):
            print(f'['+str(datetime.now())+'] NOTICE: '+message, flush=True)

    @staticmethod
    def error(message: str, flexClass):
        if(flexClass.notifications['error']):
            requests.post("https://ntfy.sh/" + flexClass.ntfyChannel, data = message.encode(encoding="utf-8"))

        if(flexClass.logging['error']):
            print(f'['+str(datetime.now())+'] ERROR: {message}', flush=True)

    @staticmethod
    def ntfy(message: str, flexClass):
        if(flexClass.ntfyChannel != ""):
            requests.post("https://ntfy.sh/" + channel, data=message.encode(encoding='utf-8'))

