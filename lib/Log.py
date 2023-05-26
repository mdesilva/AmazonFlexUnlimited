from datetime import datetime

class Log:
    
    @staticmethod 
    def info(message: str):
        print(f'['+str(datetime.now())+'] INFO: '+message, flush=True)

    @staticmethod
    def error(message: str):
        print(f'ERROR: {message}', flush=True)
