import json
import requests

# Set some variables

deplist = ["2016-12-5"] # list of departure dates

retlist = ["2017-01-18"] # list of return dates

origin = "MEX" # IATA designator of origin airport

destination = "INN" # IATA designator of destination airport

nAdults = 1 # number of adult passangers

nChildren = 0 # number of child passangers

maxStops = 2 # maximum number of stops

permittedCarrier = [] # Only flights using these carriers will be returned (list of 2-letter IATA airline designators)

prohibitedCarrier = [] # Flights using these carriers will be ignored (list of 2-letter IATA airline designators)

saleCountry = "MX" # IATA country code representing the point of sale

ticketingCountry = "MX" # IATA country code representing the point of ticketing

nSolutions = 100 # maximum number of results (max = 500)

keyfile = 'key1.txt' # file containing api key

# IATA Codes: https://en.wikipedia.org/wiki/International_Air_Transport_Association_code



def read_key(keyfile):
    with open(keyfile, "r") as myfile:
        apikey = myfile.read().replace('\n', '')
    return apikey


def readable(data):
    print(json.dumps(data, indent=4, sort_keys=True))


def print_offers(result):

    for trip in result["trips"]["tripOption"]: # trip = single trip in "tripOption"
        print(trip["saleTotal"])
        Slice = 0
        for s in trip["slice"]: # loop over slices s
            Slice = Slice + 1
            print("   Slice %s" % Slice)
            for flight in s["segment"]:
                flight_number = flight["flight"]["number"]
                flight_carrier = flight["flight"]["carrier"]
                flight_origin = flight['leg'][0]['origin']
                flight_departureTime = flight['leg'][0]['departureTime']
                flight_destination = flight['leg'][0]['destination']
                flight_arrivalTime = flight['leg'][0]['arrivalTime']
                flight_mileage = flight['leg'][0]['mileage']

                print("      %s%s %s %s %s %s %s mileage" % (flight_carrier, flight_number, flight_origin, flight_departureTime, flight_destination, flight_arrivalTime,flight_mileage))


def checkprice(url, saleCountry, ticketingCountry, nSolutions, dep, ret, origin, destination, nAdults, nChildren,
               maxStops, permittedCarrier, prohibitedCarrier):

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

    try:
        r = requests.post(url, data=jsonreq, headers={"Content-Type": "application/json"})
        result = r.json()
        r.raise_for_status()

    except requests.exceptions.HTTPError as e:
        print ("Error: " + str(e))

    return result
        # jede tripOption hat: saleTotal, id,  2 slices (hin und retur flug)!!


def main():

    url="https://www.googleapis.com/qpxExpress/v1/trips/search?key="+read_key(keyfile)

    for dep, ret in zip(deplist,retlist):
        print(dep," to ",ret)
        result = checkprice(url, saleCountry, ticketingCountry, nSolutions, dep, ret, origin, destination, nAdults, nChildren,
                   maxStops, permittedCarrier, prohibitedCarrier)
        print_offers(result)

main()
