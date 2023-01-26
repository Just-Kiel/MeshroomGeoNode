# import module
from geopy.geocoders import Nominatim
import json

## return region number (as string to handle corse) from the postCode
def regionFromPostcode(postCode: int):
    firstTwoNumber = postCode//1000
    # dom tom
    if firstTwoNumber == 97:
        return str(postCode//100)
    # corse
    elif firstTwoNumber == 20:
        return "2A" if postCode < 20200 else "2B"
    else:
        return str(firstTwoNumber)

def getDepartement(GPSData):
    # Opening JSON file
    with open(GPSData, 'r') as GPSfile:
        # Reading from json file
        json_gps = json.load(GPSfile)


    # initialize Nominatim API
    geolocator = Nominatim(user_agent="getRegion")
    # Latitude & Longitude input
    Latitude = json_gps["latitude"]
    Longitude = json_gps["longitude"]
    
    location = geolocator.reverse(str(Latitude)+","+str(Longitude))

    address = location.raw['address']
    print(address)
    
    # #region = str(address["county"]).encode('utf-8').decode('latin_1') if "county" in address else str(address["state"]).encode('utf-8').decode('latin_1')

    region = str(address["county" if "county" in address else "state"]).encode('utf-8').decode('latin_1')

    return {
        "region": regionFromPostcode(int(address["postcode"])),
        "postcode": address["postcode"]
    }


    