from subprocess import PIPE
import subprocess 

def startService(username):
    subprocess.run(f"sudo systemctl start flex@{username}", shell=True)

def stopService(username):
    subprocess.run(f"sudo systemctl stop flex@{username}", shell=True)

def getLogs(username):
    journalOutput = subprocess.run(f"journalctl -u flex@{username} -n 100", shell=True, stdout=PIPE)
    return journalOutput.stdout