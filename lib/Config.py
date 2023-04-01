import os
import json
from datetime import datetime

class Config:
    """
    A class that handles the configuration settings for the application.
    
    Attributes:
    -----------
    parent_dir: str
        The absolute path of the parent directory of the current file.
    config_path: str
        The path to the `config.json` file in the parent directory.
    config_data: dict
        A dictionary that stores the configuration settings.
        
    Methods:
    --------
    checkUserPassIsSet(self) -> None:
        Checks if the username and password fields are set in the `config.json` file.
        If they are not set, prompts the user to enter their username and password
        and updates the `config.json` file. If they are set, calls the `setUserPass` method.
    
    setUserPass(self) -> None:
        Prompts the user to decide whether to change the account logged in.
        If the user chooses to change the account, prompts the user to enter their username and password
        and updates the `config.json` file with the user's input.
    
    setTimeRange(self) -> None:
        Prompts the user to decide whether to change their desired time range.
        If the user chooses to change the range, prompts the user to enter their desired starting and ending times
        and updates the `config.json` file with the user's input. Validates that the entered times are in the correct format
        and that the starting time is before the ending time. If not, prompts the user to enter a valid time range.
    """
    def __init__(self):
        self.parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.config_path = os.path.join(self.parent_dir, 'config.json')
        self.config_data = None
        self.checkUserPassIsSet()
        
    def checkUserPassIsSet(self):
        with open(self.config_path, 'r') as file:
            config = json.load(file)
            
        if config['username'] == "" or config['password'] == "":
            username = input('Enter your username: ')
            password = input('Enter your password: ')
            
            with open(self.config_path, 'r') as file:
                config = json.load(file)
                
            config['username'] = username
            config['password'] = password

            with open(self.config_path, 'w') as file:
                json.dump(config, file, indent=2)

        else:
            self.setUserPass()
    
    def setUserPass(self):
        while True:
            try:
                change_username_password = input('Do you want to change the account logged? (y/n): ')
                if change_username_password.lower() not in ['y', 'n']:
                    raise ValueError('Please enter y or n.')
                break
            except ValueError as e:
                print(str(e))

        if change_username_password.lower() == 'y':
            
            username = input('Enter your username: ')
            password = input('Enter your password: ')

            with open(self.config_path, 'r') as file:
                config = json.load(file)
                
            config['username'] = username
            config['password'] = password

            with open(self.config_path, 'w') as file:
                json.dump(config, file, indent=2)
            
        else:
            return
            
    def setTimeRange(self):
        while True:
            try:
                change_time = input('Do you want to change your desired time range (y/n): ')
                if change_time.lower() not in ['y', 'n']:
                    raise ValueError('Please enter y or n.')
                break
            except ValueError as e:
                print(str(e))

        if change_time.lower() == 'y':
            
            while True:
                try:
                    starting_time = datetime.strptime(input('Enter your desired starting time (format HH:MM): '), '%H:%M').time()
                except ValueError:
                    print('Invalid time format. Please enter a valid time in the format HH:MM.')
                    continue
                break
            
            while True:
                try:
                    ending_time = datetime.strptime(input('Enter your desired ending time (format HH:MM): '), '%H:%M').time()
                except ValueError:
                    print('Invalid time format. Please enter a valid time in the format HH:MM.')
                    continue
                
                if starting_time >= ending_time:
                    print('Starting time cannot be greater than or equal to ending time. Please enter a valid time range.')
                    continue
                
                break
            
            with open(self.config_path, 'r') as file:
                config = json.load(file)
                
            config['desiredStartTime'] = starting_time.strftime('%H:%M')
            config['desiredEndTime'] = ending_time.strftime('%H:%M')

            with open(self.config_path, 'w') as file:
                json.dump(config, file, indent=2)
        
        else:
            return

