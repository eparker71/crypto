# crypto

This repo contains a couple of tools to help you work with the reports you get from Coinbase.

**view_report.sh** - create a profit/loss report of your Coinbase crypto account

**send_message.sh** - Sends you SMS messages based on rules you define about crypto currencies

You will need to get API keys from <https://textbelt.com/>
as well as <https://coinmarketcap.com/>

Add the keys as environmental variables:

export TEXTBELT_KEY="your key"
export CMC_PRO_API_KEY="your key"
export TEXT_NUM="your num"

*** you MUST have sqlite installed ***

# Look at the settings.py.example file
rename the file to just settings.py
Update the file as needed

# setup a python venv and run pip install 
python3 -m venv <name of your venv>
pip3 install requests

# How to use the tools

1.Goto coinbase and generate a report of your transactions
2.Download as a csv file and place it in the same directory as this project

# How to run the report

## make the report script executable
chmod +x view_report.sh

## now you can run the report 
./view_report.sh

# How to recieve text messages
message.py can be set to run as a cron job. 

Based on the rules you define in message_rules.csv and assuming you have setup the texting url and num, you will get
emails if the asset price matches any of your rules. 

example rules below

---------------------------
Asset,Direction,Limit,Comment
BTC,0,12000.00, Bitcon Above $12,000
BTC,1,9000.00, Bitcoin below $9,000

Asset is BTC (Bitcon)
Direction is either 0 (Above) or 1 (below)
Limit is the price you want to trigger the message
Comment is a place for you to add comments, it is ignored by the system

