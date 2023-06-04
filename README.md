# Amazon Flex Unlimited SUPERCHARGED
This work is based on the work done by @mdesilva. The original Amazon Flex Unlimited repository can be found at [https://github.com/mdesilva/AmazonFlexUnlimited](https://github.com/mdesilva/AmazonFlexUnlimited).

SUPERCHARGED currently adds the following functionality to the script:

## ntfy.sh Notifications
Through the free Android and iOS-app ntfy, the script now provides push notifications.

Set "ntfyChannel" in config.json to the ntfy.sh topic you have created in your app, and your notifications will be delivered there.

## Choose which notifications to receive, and which messages to print
It is possible to customize which notifications to receive and what messaages to have printed in the terminal.

Modify the "notifications" entry in config.json for notifications, or "logging" for what to be printed.

The different categorizations contain the following messages:
- Notice: On block search started, block search stopped.
- Info: For every attempt, tells you if it found a listing and how many seconds to sleep before attempting again.
- Success: On block acceptance.
- Error: On errors and captchas. 

## Run infinitely
Set "retryLimit" to 0 in config.json to make the script run infinitely.
It only exits if it encounters a CAPTCHA.

## Detect CAPTCHA
Starting 2023, Amazon now asks suspected bot-users to confirm that they are human through completing a CAPTCHA in the Flex app. If the script encounters this, it will send you an ntfy notification and exit the script entirely.

## Randomized refresh interval
"refreshInterval" in config.js has been split into two:

1. "refreshIntervalMin"
2. "refreshIntervalMax"

These are both floats, and the sleep-time between two attempts is found by selecting a random number between the min and max values.

## Stop script at certain time
You can force the script to stop at a certain hour and minute by setting the "stopRunAt" setting in config.json to the desired time.

E.g. if you want it to stop at 5:22PM, change "stopRunAt" from false to "17:22".

If you do not want the script to stop at a certain time, set "stopRunAt" to false.

## Start script at certain time
You can start the script and not have it start until a certain hour and minute by setting the "startRunAt" setting in config.json to the desired time.

E.g. if you want it to start at 5:22PM, change "startRunAt" from false to "17:22".

If you want the script to start immediately, set "startRunAt" to false.


## Rate limit parameters
The default rate limit prevention mechanism consists of a 30 minute pause the first time rate limit is encountered, then 30 * the amount of times a rate limit has been encountered. When this has been multiplied 4 times (30 * 4 = 120), it goes back to 30 minutes.

Change "rateLimit.increment" for the amount of minutes, "rateLimit.maxTimesIncrement" for the max amount of times to multiply increment before going back to increment * 1.

## Experimental: Method to filter desired warehouses
The way this script originally chose whether a certain offer should be considered was by sending the id's of the desired warehouses to the getOffer endpoint. Instead, it is possible to fetch all offers, but only accept the ones with the correct warehouse id.

Set "filterForWarehouse" to false to enable the new method. It does not yet have any actual influence on the functionality of the script, but in the future it will be able to provide you with an overview of available and unaccepted offers encountered by the script during its run.

# Original README.md
This is the original README.md from @mdesilva.
# Flex Unlimited #
## Automate searching and accepting Amazon Flex Driver jobs ##

This is an attempt to automate picking up Amazon Flex driver jobs. I attempted to automate this process for a client and it worked well. The only setup caveat is that you have to run the program on a machine connected to the Internet by wire; wireless isn't fast enough to compete with the dumb clickers that Flex drivers are fooled into paying for (https://www.cnbc.com/2020/02/09/amazon-flex-drivers-use-bots-to-get-more-work.html). These clickers require the drivers to stare at their phones all day long and watch the clicker 'ghost' click the "Refresh" button to search for jobs, but at a rate of 1000x of what they can do with their thumbs. This is stupid software that only the unknowledgeable will fall for; true software automates an entire process without any continous human intervention, know-how, or awareness. My ultimate goal was for any Amazon Flex driver to only pick up their phone to actually DO the jobs this program accepted on their behalf; they would never have to search for jobs again. 

**Note**: I reverse-engineered the Amazon Flex API by running Charles Proxy on my iPhone whilst doing a variety of things on the Flex app (e.g logging in, searching for jobs, accepting a job, declining a job). You can do the same if you need to update the reverse engineered API in this program.

**Disclaimer 1**: Run this program at your own risk. I am not responsible for Flex account termination or penalties imposed by Amazon as a result of using this program. 

**Disclaimer 2**: I tried to run this on a AWS server and it didn't work, possibly because Flex blocks all incoming connections from data centers to prevent large scale automation. But perhaps it'll work out of data centers not owned by AWS. 

## Usage ##

0. You MUST have python 3 installed. Versions below 3 will not work.  
1. Clone the repo to the machine you will be using to run the program (machine should be connected to Internet by wire for best results).
2. Install dependencies using **pip**: `pip install -r requirements.txt`.
3. Set `username` and `password` in **config.json**.
4. Modify the remainder of **config.json** to meet your job search requirements. It already comes with some defaults. Fill out `desiredWarehouses` if you would like to restrict your job search to certain warehouses. If you choose this option, 
`desiredWarehouses` must be a list of strings of **internal warehouse ids**. Otherwise, leave `desiredWarehouses` as an empty list.
5. Fill out the `desiredWeekdays` filter in **config.json** if you would like to restrict your job search to certain days of the week. Otherwise, you may leave `desiredWeekdays` as an empty list. `desiredWeekdays` must be a list of strings (case insensitive) corresponding to days of the week (i.e. "Sun", "monday", etc.). Each string must include at least the first three letters of the day.

To determine the internal warehouse ids of warehouses you are eligible for, run the following command:
`python3 app.py getAllServiceAreas` OR `python3 app.py --w`

Here you will get a table of all the service areas (warehouses) that you are eligible for. The left column states the service area name, and the right column is the internal warehouse id used by Amazon. Copy all the service area ids you want to restrict your search to as strings into the **desiredWarehouses** field into the config.json. 

e.g
```
{
...
"desiredWarehouses": ["9c332725-c1be-405f-87c5-e7def58595f6", "5fa41ec8-44ae-4e91-8e48-7be008d72e8a"]],
...
}
```
5. Optionally, setup SMS notifications of Amazon Flex job acceptances by filling out the `twilio` parameters in  **config.json**.
6. Run `python app.py`. Alternatively, try `python3 app.py`.

## Troubleshooting ##

- Unable to authenticate to Amazon Flex. Please try completing the two step verification challenge at (url)

Click on the url and complete the two step verification challenge. After you get to a page that says:

_Looking for Something?
We're sorry. The Web address you entered is not a functioning page on our site_

You have **successfully completed the two step verification challenge**. Go back to your terminal and re-run the program.
