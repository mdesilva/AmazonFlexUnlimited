from datetime import datetime
import requests

class Log:
    
    @staticmethod 
    def info(message: str):
        print(f'['+str(datetime.now())+'] INFO: '+message, flush=True)

    @staticmethod 
    def success(message: str):
        print(f'\n['+str(datetime.now())+'] SUCCESS: '+message+'\n', flush=True)

    @staticmethod
    def error(message: str):
        print(f'ERROR: {message}', flush=True)

    @staticmethod
    def ntfy(message: str, channel: str):
        requests.post("https://ntfy.sh/" + channel, data=message.encode(encoding='utf-8'))

