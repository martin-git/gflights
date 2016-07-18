import json
import smtplib
import requests

# Set some variables

deplist = ["2016-12-18"] # list of departure dates

retlist = ["2017-01-18"] # list of return dates

origin = "MEX" # IATA designator of origin airport

destination = "INN" # IATA designator of destination airport

nAdults = 1 # number of adult passangers

nChildren = 0 # number of child passangers

maxStops = 1 # maximum number of stops

permittedCarrier = [] # Only flights using these carriers will be returned (list of 2-letter IATA airline designators)

prohibitedCarrier = [] # Flights using these carriers will be ignored (list of 2-letter IATA airline designators)

saleCountry = "MX" # IATA country code representing the point of sale

ticketingCountry = "MX" # IATA country code representing the point of ticketing

nSolutions = 50 # maximum number of results (max = 500)

keyfile = 'key1.txt' # file containing api key

# IATA Codes: https://en.wikipedia.org/wiki/International_Air_Transport_Association_code






def read_key(keyfile):
    with open(keyfile, "r") as myfile:
        apikey = myfile.read().replace('\n', '')
    return apikey

def checkprice(url, saleCountry, ticketingCountry, nSolutions, dep, ret, origin, destination, nAdults, nChildren,
               maxStops, permittedCarrier, prohibitedCarrier):

    # request = {
    #     "request": {
    #         "slice": [
    #             {
    #                 "origin": origin,
    #                 "destination": destination,
    #                 "date": dep
    #             },
    #             {
    #                 "origin": destination,
    #                 "destination": origin,
    #                 "date": ret
    #             }
    #         ],
    #         "passengers": {
    #             "adultCount": nAdults,
    #             "infantInLapCount": 0,
    #             "infantInSeatCount": 0,
    #             "childCount": 0,
    #             "seniorCount": 0
    #         },
    #         "solutions": 500,
    #         "maxPrice": "NZD5700",
    #         "refundable": False
    #     }
    # }

    request = {
        "request": {
            "passengers": {
                "kind": "qpxexpress#passengerCounts",
                "adultCount": nAdults,
                "childCount": nChildren,
                "infantInLapCount": 0,
                "infantInSeatCount": 0,
                "seniorCount": 0
            },
            "slice": [
                {   # departure flight
                    "kind": "qpxexpress#sliceInput",
                    "origin": origin,
                    "destination": destination,
                    "date": dep,
                    "maxStops": maxStops,
                    "permittedCarrier": permittedCarrier,
                    "prohibitedCarrier": prohibitedCarrier
                },
                {   # return flight
                    "kind": "qpxexpress#sliceInput",
                    "origin": destination,
                    "destination": origin,
                    "date": ret,
                    "maxStops": maxStops,
                    "permittedCarrier": permittedCarrier, # list of 2-letter IATA airline designators
                    "prohibitedCarrier": prohibitedCarrier # list of 2-letter IATA airline designators
                }
            ],
            "saleCountry": saleCountry,
            "ticketingCountry": ticketingCountry,
            "refundable": False,
            "solutions": nSolutions
        }
    }

    jsonreq = json.dumps(request)
    print(jsonreq)

    try:
        r = requests.post(url, data=jsonreq, headers={"Content-Type": "application/json"})
        print(r.json())
        result = r.json()
        r.raise_for_status()

    except requests.exceptions.HTTPError as e:
        print ("Error: " + str(e))

    for trip in result["trips"]["tripOption"]:
        print(trip["saleTotal"], "(from " + dep + " to " + ret + ")")

        # jede tripOption hat: saleTotal, id,  2 slices (hin und retur flug)!!


        # try:
        # 	req = urllib2.Request(url, jsonreq, {'Content-Type': 'application/json'})
        # 	flight = urllib2.urlopen(req)
        # 	response = flight.read()
        # 	result = json.loads(response)
        # 	flight.close()
        #
        # 	try :
        # 		for i in result['trips']['tripOption']:
        # 			#return "Found " + i['saleTotal'] +  "  (from " + startdate + " to " + enddate + ")\n"
        # 			return (i['saleTotal'], "(from " + startdate + " to " + enddate + ")")
        # 	except:
        # 		return ""
        # 		#return "Nothing found for that price (from " + startdate + " to " + enddate + ")"
        # except urllib2.HTTPError, err:
        # 	if err.code == 403:
        # 		print "API requsts limit exceeded!"


def main():

    url="https://www.googleapis.com/qpxExpress/v1/trips/search?key="+read_key(keyfile)
    print(url)

    for dep, ret in zip(deplist,retlist):
        print(dep, ret)
        checkprice(url, saleCountry, ticketingCountry, nSolutions, dep, ret, origin, destination, nAdults, nChildren,
                   maxStops, permittedCarrier, prohibitedCarrier)

main()


# def checkprice(startdate,enddate,minprice):
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
