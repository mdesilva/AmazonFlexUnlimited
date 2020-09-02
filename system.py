import subprocess
from subprocess import PIPE

fileContent = "[Unit]\nDescription=Amazon Flex Service\n\n[Service]\nExecStart=/usr/bin/python3 service.py\nWorkingDirectory=/home/mdesilva/flexutility\n\n[Install]\nWantedBy=multi-user.target"



def registerService(username, password):
