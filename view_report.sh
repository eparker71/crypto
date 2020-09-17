#!/bin/bash

# get the lastest Cointbase Report
RPT=$(ls -t Coinbase* | head -1)

#prepare the datafile
tail -n +8 $RPT > data.csv 

# get the current prices
python3 get_crypto_prices.py > assets.csv

# load the prices into sqlite and fix the sell orders
# I am making the sell orders negative so I can just
# add up the columns
sqlite3 crypto.sqlite < load_current_prices.sql
sqlite3 crypto.sqlite < load_data.sql
sqlite3 crypto.sqlite < fix_sell_orders.sql
sqlite3 crypto.sqlite < update_tax_status.sql

# Report is a view that does some of the calulations 
# export the report data into a file
if [ $# -eq 0 ]
  then
    sqlite3 crypto.sqlite "select * from Report" > report
else
  echo $1
  sqlite3 crypto.sqlite "select * from Report where Asset = '$1' " > report
fi

# use sed to replace the '|' with a space
sed -i -e 's/|/ /g' report

#output the report. Use awk to format the columns
echo ""
awk 'BEGIN { printf "%6s %11s %11s %13s %9s %10s %11s %6s\n", "Asset ", "Cur Price  ", "Break Even ", "  Total      ", "  Cost   ", "Cur Value ", " Prof/Loss ", "Tax Stat"
             printf "%6s %11s %11s %13s %9s %10s %11s %6s\n", "------", "-----------", "-----------", "-------------", "---------", "----------", "-----------", "--------" }
           { printf "%6s %11s %11s %13s %9s %10s %11s %6s\n", $1, $3, $4, $5, $6, $7, $8, $2 }' report 
echo "--------------------------------------------------------------------------------------"

# cut the last three columns and total the amount below the data
cut -d' ' -f6,7,8 report | awk '{t+=$1;s+=$2;p+=$3} END {printf "%43s %11.2f %11.2f %9.2f\n", "Total:",t, s,p}'
echo ""
