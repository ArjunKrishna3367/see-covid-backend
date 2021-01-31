from uszipcode import SearchEngine
import json
search = SearchEngine(simple_zipcode=False)
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import numpy as np

def get_zip(lat,long):
    zips=search.by_coordinates(lat, long,radius=20,returns=20)
    possiblezips=[]
    otherzips=[]
    for azip in zips:
        azip=json.loads(azip.to_json())
        otherzips.append(azip)
        #print("lat: {}, north: {}, south: {}, long: {}, west: {}, east: {}, zip: {}".format(lat,azip['bounds_north'],azip['bounds_south'],long,azip['bounds_west'] ,azip['bounds_east'],azip['zipcode']))
        if lat < azip['bounds_north'] and lat > azip['bounds_south']:
            if abs(long) < abs(azip['bounds_west']) and abs(long) > abs(azip['bounds_east']):
                possiblezips.append(azip)
               
    if(len(possiblezips)>1):
        for azip in possiblezips:
            lons_lats_vect = np.column_stack(np.column_stack([tuple(l) for l in azip['polygon']])) # Reshape coordinates
            polygon = Polygon(lons_lats_vect) # create polygon
            point = Point(long, lat) # create point
           
            if polygon.contains(point):
                otherzips.remove(azip)
               
                #check that all of the nearby zip codes are adjacent to the present zip code:
                p1 = Polygon([tuple(l) for l in azip['polygon']])
                finalzips=[]
                for azip in otherzips:
                    if depth(azip['polygon']) >2:
                        p2 = Polygon([tuple(l) for l in azip['polygon'][0]])
                    else:
                        p2 = Polygon([tuple(l) for l in azip['polygon']])
                   
                    if p1.intersects(p2):
                        finalzips.append(azip)
               
                return {"zipCode": azip['zipcode'],
                "nearbyZipCodes": [i['zipcode'] for i in finalzips], 
                "nearbyCoords": [tuple([i['lat'],i['lng']]) for i in finalzips],
                "nearbyCountyNames": [i['county'] for i in finalzips]}
           
    else:
        if possiblezips[0] in otherzips:
            otherzips.remove(possiblezips[0])
   
    #check that all of the nearby zip codes are adjacent to the present zip code:
        p1= Polygon([tuple(l) for l in possiblezips[0]['polygon']])
        finalzips=[]
        for azip in otherzips:
            print("here")
            if depth(azip['polygon']) >2:
                p2 = Polygon([tuple(l) for l in azip['polygon'][0]])
            else:
                p2 = Polygon([tuple(l) for l in azip['polygon']])
            if p1.intersects(p2):
                finalzips.append(azip)
       
        return {"zipCode": possiblezips[0]['zipcode'],
                "nearbyZipCodes": [i['zipcode'] for i in finalzips], 
                "nearbyCoords": [tuple([i['lat'],i['lng']]) for i in finalzips],
                "nearbyCountyNames": [i['county'] for i in finalzips]}
    return "ERROR"

def depth (givenList):
    for i in givenList:
        if not isinstance(i,list):
            return 1
        else:
            return depth(i)+1

