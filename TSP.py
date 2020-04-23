import googlemaps
import pprint
import time
import csv
import requests
import mlrose
import numpy as np
import copy

my_API_key = "AIzaSyAsehbprMSCj4Hs1aquw2yDekqQii2KUYE"

def createDistanceMatrix(places_to_visit):
    distance_matrix = []
    for i in range(len(places_to_visit)):
        for j in range(i + 1, len(places_to_visit)):
            origin = places_to_visit[i]
            dest = places_to_visit[j]
            key = (origin, dest)

            req = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=place_id:' + origin + '&destinations=place_id:' + dest + '&key=' + my_API_key
            Response = requests.get(req)
            Response = Response.json()

            pprint.pprint(Response)

            # pprint.pprint(Response["rows"][0]["elements"][0]["duration"]["value"])
            value = Response["rows"][0]["elements"][0]["duration"]["value"]  # We get the time duration is seconds
            new_element = (i, j, value)
            distance_matrix.append(new_element)
    return distance_matrix

def orderPlaces(places_to_visit, final_itin):
    for day_idx, day in enumerate(final_itin):
        for place_idx, place in enumerate(day):
            final_itin[day_idx][place_idx] = places_to_visit[place]
    return final_itin

def findDistance(v1, v2, distance_matrix):
    sm = min(v1, v2)
    lg = max(v1, v2)
    for pair in distance_matrix:
      a = pair[0]
      b = pair[1]
      smp = min(a, b)
      lgp = max(a, b)
      if sm == smp and lg == lgp:
        return pair[2]

def TSP(places_to_visit, duration, dailyDriveTime):
    print('start distance matrix')

    distance_matrix = createDistanceMatrix(places_to_visit)

    print('distance matrix done')
    print(distance_matrix)

    fitness = mlrose.TravellingSales(distances = distance_matrix)
    # We want to visit all the places of our list "places_to_visit"
    problem = mlrose.TSPOpt(length = len(places_to_visit), fitness_fn = fitness,
                                maximize=False)
    best_state, best_fitness = mlrose.genetic_alg(problem, random_state=0)

    print('melrose done')
    print('best_state', best_state)
    print('best_fitness', best_fitness)

    max_time = duration * dailyDriveTime * 60 * 60
    dailyDriveTime = dailyDriveTime * 60 * 60


    print('max_time', max_time)
    print('dailyDriveTime', dailyDriveTime)

    final_itin = []
    for day in range(duration):
        final_itin.append([])

    print('empty final itin done')
    print(final_itin)

    day = 0
    current_time = 0

    for idx, place_idx in enumerate(best_state[:-1]):
        travelTime = findDistance(best_state[idx], best_state[idx + 1], distance_matrix)
        # add to current day
        if current_time + travelTime < dailyDriveTime:
            final_itin[day].append(place_idx)
            current_time += travelTime
        # add to next day
        elif day + 1 < len(final_itin):
            day += 1
            final_itin[day].append(place_idx)
            current_time = travelTime
        # end, cant add any more destinations

        # print('At idx ', idx)
        # print('We are on day: ', day)
        # print('travel_time: ', travelTime)
        # print('current_time', current_time)

    print('Final Itin - split over days done')
    print(final_itin)

    final_itin_idxs = copy.deepcopy(final_itin)

    itin_final = orderPlaces(places_to_visit, final_itin)

    print('--- Final Itin DONE ---')
    print(itin_final)

    return itin_final, final_itin_idxs
