#!/bin/sh
rm -rf Project.db
rm -rf AuctionItems.dat
rm -rf BidsInfo.dat
rm -rf Categories.dat
rm -rf UserInfo.dat
rm -rf Sells.dat
rm -rf Category.dat
python skeleton_parser.py ebay_data/items*
sqlite3 Project.db < create.sql 
sqlite3 Project.db < load.txt
