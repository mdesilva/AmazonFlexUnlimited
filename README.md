# Flex Unlimited #
## Automate searching and accepting Amazon Flex Driver jobs ##

This is an attempt to automate picking up Amazon Flex driver jobs. I attempted to automate this process for a client and it worked well. The only setup caveat is that you have to run the program on a machine connected to the Internet by wire; wireless isn't fast enough to compete with the dumb clickers that Flex drivers are fooled into paying for (https://www.cnbc.com/2020/02/09/amazon-flex-drivers-use-bots-to-get-more-work.html). These clickers require the drivers to stare at their phones all day long and watch the clicker 'ghost' click the "Refresh" button to search for jobs, but at a rate of 1000x of what they can do with their thumbs. This is stupid software that only the unknowledgeable will fall for; true software automates an entire process without any continous human intervention, know-how, or awareness. My ultimate goal was for any Amazon Flex driver to only pick up their phone to actually DO the jobs this program accepted on their behalf; they would never have to search for jobs again. 

**Note**: I reverse-engineered the Amazon Flex API by running Charles Proxy on my iPhone whilst doing a variety of things on the Flex app (e.g logging in, searching for jobs, accepting a job, declining a job). You can do the same if you need to update the reverse engineered API in this program.

**Disclaimer**: I tried to run this on a AWS server and it didn't work, possibly because Flex blocks all incoming connections from data centers to prevent large scale automation. But perhaps it'll work out of data centers not owned by AWS. 

## Usage ##

1. Clone the repo to the machine you will be using to run the program (machine should be connected to Internet by wire for best results).
2. Install dependencies
3. Setup the desired Amazon Flex user account for which jobs will be searched for by running `export AMZNFLEXUSERNAME=$username` & `export AMZNFLEXPWD=$password`, where `$username` and `$password` is the Amazon Flex username and password.
4. Modify `config.json` to meet your job search requirements. It already comes with some defaults; the only field you MUST fill out is `desiredWarehouses`. `desiredWarehouses` is a list of strings of all the warehouses ids of the warehouses you'd like to search for jobs at; **these must be internal warehouse ids**. For some example warehouses, refer to the table below.

| Warehouse External ID | Warehouse Internal ID |
| --------------------- | ---------------------- |
|  UNY1 | 2 |
| C077| 721061b3-a4f1-4244-99b3-a453c9cb864e|
| C506| acf06702-57ba-47f3-a34f-19e536a69fc0|
| Elkridge MD (SMD1/VMD1) - Sub Same-Day' | 2a13b39b-2238-4cb3-aa11-99ae1ea78172 |
| Canton - (UMD1) Prime Now | 18 |
| Hanover - (DBA2) AMZL | 47d2658a-568d-4f42-84dc-55e41b39de96 |
| Hanover (DMD6) - Amazon.com | ef813098-fa34-4f76-992b-bf580626c449 |
| Hanover (DBA8) - Amazon.com | 467735da-dc81-4bfd-9a5c-4f21b82b8d0a |


If you want to only search for jobs in the **UNY1** warehouse, `desiredWarehouses` will be `[2]`. For **UNY1** **and** **C506** warehouses, `[2,acf06702-57ba-47f3-a34f-19e536a69fc0]`. For warehouses not in the table above, you'll have to snoop on requests made by the Amazon Flex app to get the internal warehouse id.

5. Optionally, setup SMS notifications of Amazon Flex job acceptances by filling out the `twilio` parameters in `config.json`.
6. Run `python app.py`.




