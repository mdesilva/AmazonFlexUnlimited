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



