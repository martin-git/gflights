import urllib
import json
import itertools
import smtplib

# Set some variables

keyfile = 'key1.txt'

listofstartdates = ["2016-12-18", "2016-12-19"]

listofenddates = ["2017-01-18", "2017-01-19"]

minprice = []
flightsfound = []


def read_key(keyfile):
    with open(keyfile, "r") as myfile:
        apikey = myfile.read().replace('\n', '')
    return apikey

def main():
    apikey=read_key(keyfile)
    print(apikey)




main()


# def checkprice(startdate,enddate,minprice):
#
# 	url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=%s" % apikey
#
# 	request = {
# 	"request": {
# 	"slice": [
# 	{
# 	"origin": "AKL",
# 	"destination": "MOW",
# 	"date": startdate
# 	},
# 	{
# 	"origin": "MOW",
# 	"destination": "AKL",
# 	"date": enddate
# 	}
# 	],
# 	"passengers": {
# 	"adultCount": 2,
# 	"infantInLapCount": 0,
# 	"infantInSeatCount": 0,
# 	"childCount": 0,
# 	"seniorCount": 0
# 	},
# 	"solutions": 500,
# 	"maxPrice": minprice,
# 	"refundable": False
# 	}
# 	}
#
# 	jsonreq = json.dumps(request, encoding = 'utf-8')
#
# 	try:
# 		req = urllib2.Request(url, jsonreq, {'Content-Type': 'application/json'})
# 		flight = urllib2.urlopen(req)
# 		response = flight.read()
# 		result = json.loads(response)
# 		flight.close()
#
# 		try :
# 			for i in result['trips']['tripOption']:
# 				#return "Found " + i['saleTotal'] +  "  (from " + startdate + " to " + enddate + ")\n"
# 				return (i['saleTotal'], "(from " + startdate + " to " + enddate + ")")
# 		except:
# 			return ""
# 			#return "Nothing found for that price (from " + startdate + " to " + enddate + ")"
# 	except urllib2.HTTPError, err:
# 		if err.code == 403:
# 			print "API requsts limit exceeded!"
#
# # Main loop:
#
# for dates in itertools.product(listofstartdates, listofenddates): flightsfound.append(checkprice(dates[0],dates[1],minprice))
#
# try:
# 	# Output prices starting with lowest, after a bit of filtering
# 	flightsfound = ''.join(["Price: %s %s \n" % (x[0],x[1]) for x in sorted([x for x in flightsfound if x != ""], key=lambda tup: tup[0])])
# except:
# 	# A bit a a debugging
# 	flightsfound = "Something went wrong"
# 	print flightsfound
#
#
# # Optional email report with 3 best results:
# message = """From: From Flight Bot <sergey@server.com>
# To: To Person <sergey@server.com>
# Subject: Daily flight search results
#
# {flightsfound}
#
# """.format(flightsfound=flightsfound)
#
# smtpObj = smtplib.SMTP('mail.server.com')
# smtpObj.sendmail("sergey@server.com", ["sergey@server.com"], message)
