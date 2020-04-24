#!/bin/bash

python3 get_crypto_prices.py > assets.csv
sqlite3 crypto.db < load_current_prices.sql
sqlite3 crypto.db < load_data.sql
sqlite3 crypto.db < fix_sell_orders.sql
sqlite3 crypto.db "select * from Report" > report
sed -i -e 's/|/ /g' report
#cut -d',' -f1,7 report
#cat report
echo ""
awk 'BEGIN { printf "%-6s %-14s %-11s %-13s %-9s %-10s %-8s\n", "Asset", "Current Price", "Break Even", "Curr Amount", "Total $", "Current $", "Prof/Loss"
             printf "%-6s %-14s %-11s %-13s %-9s %-10s %-8s\n", "-----", "-------------", "----------", "-----------", "-------", "---------", "--------" }
           { printf "%-6s %-14s %-11s %-13s %-9s %-10s %-8s\n", $1, $2, $3, $4, $5, $6, $7 }' report 
echo "-----------------------------------------------------------------------------"

cut -d' ' -f5,6,7 report | awk '{t+=$1;s+=$2;p+=$3} END {printf "%44s %10.2f %9.2f %11.2f\n", "Total:",t, s,p}'  

echo ""