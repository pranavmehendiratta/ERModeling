
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Create an item entry and fill in item.dat
"""






"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.

"""
def parseJson(json_file, userSet, catSet):
    users = 0
    #For every json file, open in append mode
    fp1 = open("AuctionItem.dat", "a+")
    
    fp3 = open("BidsInfo.dat", "a+")
    fp4 = open("Categories.dat", "a+")

    #GLOBAL dictionary of user IDs
    #userSet = set() 

    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file

        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
				
            """
            #get all the parameters
            id = item.get("ItemID")
            name = item.get("Name")
            categories = item.get("Category")
            buy = item.get("Buy_Price")
            first_bid = item.get("First_Bid")
            numBids = item.get("Number_of_Bids")
            curr = item.get("Currently")
            
            location = item.get("Location").replace("\"", "\\\"")
            country = item.get("Country")
            started = transformDttm(item.get("Started"))
            ends = transformDttm(item.get("Ends"))

            sellerObject = item.get("Seller")
            sellerID = sellerObject.get("UserID")
            rating = sellerObject.get("Rating")
            description = item.get("Description")

            #get the item information and add it to.dat
       
            #+ buy + columnSeparator + first_bid + columnSeparator + started + columnSeparator)
            if(buy is None):
                buy = '\"NULL\"'

            if(description is None):
                description = '\"NULL\"'
                

            newStr = (id + columnSeparator + name.replace("\"", "\\\"") + columnSeparator + curr + columnSeparator +
                    sellerID + columnSeparator + transformDollar(buy) 
                    + columnSeparator  + transformDollar(first_bid) + columnSeparator + 
                    item.get("Number_of_Bids") + columnSeparator + transformDttm(started)
                     + columnSeparator + transformDttm(ends) + columnSeparator + description.replace("\"", "\\\""))

            #newStr = name.replace("\"", "\\\"")

            if(location is None):
            	location = '\"NULL\"'

            if(country is None):
            	country = '\"NULL\"'

            #Record the auction item and the seller info
            fp1.write(newStr)
            fp1.write('\n')


            if(sellerID not in userSet):
                userSet[sellerID] = [location, country, rating]
            else:
            	if(userSet[sellerID][0] == 'NULL' and location is not None):
            		userSet[sellerID][0] = location
           

            

            #Add data from bids to bidder table
            bids = item.get("Bids")

            if bids != None:
                for bid in bids:



                    bidder = bid.get("Bid").get("Bidder")

                    bidderID = bidder.get("UserID")
                    bidderLoc = bidder.get("Location")
                    bidderCountry = bidder.get("Country")

                    if(bidderLoc is None):
                        bidderLoc = '\"NULL\"'

                    if(bidderCountry is None):
                        bidderCountry = '\"NULL\"'

                    #item ID, user ID
                    bid_info = (id + columnSeparator + bidderID + columnSeparator
                                    + transformDollar(bid.get("Bid").get("Amount")) + 
                                    columnSeparator + transformDttm(bid.get("Bid").get("Time")) )

                    fp3.write(bid_info)
                    fp3.write('\n') #Record the bid 

                    #Record the bidder in user table
                    BidderData = (bidderID + columnSeparator + bidderLoc.replace("\"", "\\\"") + 
                                columnSeparator + bidderCountry + columnSeparator 
                                    + bidder.get("Rating") )

                    
       

                    if(bidderID not in userSet):
                        userSet[bidderID] = [bidderLoc, bidderCountry, bidder.get("Rating")]
                    else:
                    	if(userSet[bidderID][0] == 'NULL' and bidderLoc is not None):
                    		userSet[bidderID][0] = bidderLoc
                        

            #Write the categories to the schema
            categories = item.get("Category")
            if categories != None:
                for catStr in categories:
                	if(id not in catSet):
                		catSet[id] = [catStr]
                	else:
                	  	#Add the category if not present in there
                	  	if(catStr not in catSet[id]):
                	  		catSet[id].append(catStr)




"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument



    userSet = dict()
    catSet = dict()
    for f in argv[1:]:
        if isJson(f):
            parseJson(f, userSet, catSet)
            print "Success parsing " + f
    print(len(userSet))

    fp = open("UserInfo.dat", "w+")
    for k,v in userSet.items():
    	sellerID = k
    	location = v[0]
    	country = v[1]
    	rating = v[2]
        SellerData = (sellerID + columnSeparator + location + columnSeparator + country + columnSeparator + rating)
        fp.write(SellerData + '\n')

    fp.close()
    fp2 = open("Categories.dat", "w+")
    for k,v in catSet.items():
    	id = k
    	for category in v:
    		catStr = id + columnSeparator + category
    		fp2.write(catStr + '\n')

    fp2.close()



if __name__ == '__main__':
    main(sys.argv)
