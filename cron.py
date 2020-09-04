from crontab import CronTab

cron = CronTab(user=True)

def scheduleJob():
    job = cron.new(command='python3 /home/mdesilva/flexunlimited/singleRun.py thushara70@ymail.com manuja98 7 13 >> /home/mdesilva/flexunlimited/logs/log.txt ', comment="ThusharaFlexService")
    job.minute.every(1)
    cron.write()

scheduleJob()