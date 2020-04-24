#!/bin/bash

# get the current prices
python3 get_crypto_prices.py > assets.csv

# load the prices into sqlite and fix the sell orders
# I am making the sell orders negative so I can just
# add up the columns
sqlite3 crypto.sqlite < load_current_prices.sql
sqlite3 crypto.sqlite < load_data.sql
sqlite3 crypto.sqlite < fix_sell_orders.sql

# Report is a view that does some of the calulations 
# export the report data into a file
sqlite3 crypto.sqlite "select * from Report" > report

# use sed to replace the '|' with a space
sed -i -e 's/|/ /g' report

#output the report. Use awk to format the columns
echo ""
awk 'BEGIN { printf "%-6s %-14s %-11s %-13s %-9s %-10s %-8s\n", "Asset", "Current Price", "Break Even", "Curr Amount", "Total $", "Current $", "Prof/Loss"
             printf "%-6s %-14s %-11s %-13s %-9s %-10s %-8s\n", "-----", "-------------", "----------", "-----------", "-------", "---------", "--------" }
           { printf "%-6s %-14s %-11s %-13s %-9s %-10s %-8s\n", $1, $2, $3, $4, $5, $6, $7 }' report 
echo "-----------------------------------------------------------------------------"

# cut the last three columns and total the amount below the data
cut -d' ' -f5,6,7 report | awk '{t+=$1;s+=$2;p+=$3} END {printf "%44s %10.2f %9.2f %11.2f\n", "Total:",t, s,p}'
echo ""