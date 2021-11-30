# Flex Unlimited #
## Automate searching and accepting Amazon Flex Driver jobs ##

This was a very rudimentary attempt to automate picking up Amazon Flex driver jobs. I attempted to automate this process for a client and it worked well. The only setup caveat is that you have to run the program on a machine connected to the Internet by wire; wireless isn't fast enough to compete with the dumb clickers that Flex drivers are fooled into paying for (https://www.cnbc.com/2020/02/09/amazon-flex-drivers-use-bots-to-get-more-work.html). However, I ran into the problem of not being able use a filter when searching for jobs. Due to this, the program had to naively accept all jobs whenever they became available, and then automatically decline them after it had already accepted them if it didn't fit the client's parameters. This was suspicious to Amazon and ultimately got the client banned from Flex when the program failed to decline some jobs. In addition, I didn't get the Amazon Flex server timeout workaround entirely figured out (can only poll for jobs for a variable amount of time before your polling requests are blocked).

I am no longer working on this, but if you wish to try your hand at automatically getting Flex jobs, feel free to pick up where I left off. It is far better than the boatload of insane clicker software that was built solely for this task.
These clickers require the drivers to stare at their phones all day long and watch the clicker 'ghost' click the "Refresh" button to search for jobs, but at a rate of 1000x of what they can do with their thumbs. This is stupid software that only the unknowledgeable will fall for; true software automates an entire process without any human intervention, know-how, or awareness. This program attempts to do just that; essentialy create an infinitely running cron job that searches for Flex jobs for a client that fits their exact parameters (e.g certain warehouses they want to pick up from, specific times they want to work) and accepts those jobs automatically when they are found. My ultimate goal was for any Amazon Flex driver to only pick up their phone to actually DO the jobs this program accepted on their behalf; they would never have to search for jobs again. 

**Note**: I reverse-engineered the Amazon Flex API by running Charles Proxy on my iPhone whilst doing a variety of things on the Flex app (e.g logging in, searching for jobs, accepting a job, declining a job). You can do the same if you need to update the reverse engineered API in this program.

**Disclaimer**: I tried to run this on a AWS server and it didn't work, possibly because Flex blocks all incoming connections from data centers to prevent large scale automation. But perhaps it'll work out of data centers not owned by AWS. 

## Usage ##

1. Clone the repo to the machine you will be using to run the program.
2. Install dependencies
3. Run `python app.py` and follow the prompts. For your desired warehouses that you wish to retrieve jobs from, make sure to enter the INTERNAL ID's of the warehouses. Here is an example:


| Warehouse External ID | Warehouse Internal ID |
| --------------------- | ---------------------- |
|  UNY1 | 2 |
| C077| 721061b3-a4f1-4244-99b3-a453c9cb864e|
| C506| acf06702-57ba-47f3-a34f-19e536a69fc0|


If you want to only search for jobs in the **UNY1** warehouse, you would type in `2`. For **UNY1** **and** **C506** warehouses, `2,acf06702-57ba-47f3-a34f-19e536a69fc0`. All three of these example warehouses are located in New York, I believe. For other warehouses, you'll have to snoop on requests made by Amazon Flex to get the internal warehouse id.

