import math

import flask
from flask import request, jsonify
import mlrose
import requests
import numpy as np
import pandas as pd
import random
import ast
from googleplaces import GooglePlaces, types, lang


app = flask.Flask(__name__)
app.config["DEBUG"] = True

my_API_key = 'AIzaSyDiIa1mWK2UwXIGb0t-Y06Q9Ts7JyBRk2k'
google_places = GooglePlaces(my_API_key)

voting_suggestions_count = 20

# @app.route('/api/v1/TSP', methods=['GET'])
def api_tsp():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    places_to_visit = []
    if 'places' in request.args:
        temp = request.args['places']
        splitItems = temp.split(",")
        # listTemp = [int(i) for i in splitItems]
        print(request.args['places'])
        places_to_visit = splitItems
        # id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    distance_matrix=[]
    for i in range(len(places_to_visit)):
        for j in range(i+1,len(places_to_visit)):
            origin=places_to_visit[i]
            dest=places_to_visit[j]
            key=(origin,dest)

            req='https://maps.googleapis.com/maps/api/distancematrix/json?origins=place_id:'+origin+'&destinations=place_id:'+dest+'&key='+my_API_key
            Response = requests.get(req)
            Response=Response.json()

            #pprint.pprint(Response["rows"][0]["elements"][0]["duration"]["value"])
            value=Response["rows"][0]["elements"][0]["duration"]["value"] #We get the time duration is seconds
            new_element=(i,j,value)
            distance_matrix.append(new_element)
    fitness = mlrose.TravellingSales(distances = distance_matrix)
    # We want to visit all the places of our list "places_to_visit"
    problem = mlrose.TSPOpt(length = len(places_to_visit), fitness_fn = fitness,
                                maximize=False)

    best_state, best_fitness = mlrose.genetic_alg(problem, random_state = 0)
    ordered_places_to_visit=[]
    for i in best_state:
      ordered_places_to_visit.append(places_to_visit[i])
    print(places_to_visit)

    temp = {}
    temp['results'] = ordered_places_to_visit
    results.append(temp)
    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    # for book in books:
    #     if book['id'] in listTemp:
    #         results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


# Suggestions
def compileMemberInfo(memberInfo):
    pref_mapping = {'tourist': 0, 'museum': 1, 'amusement_park': 2, 'natural': 3, 'tour': 4, 'zoo': 5}
    pref_vector = [0] * 6

    for idx in memberInfo:
        for pref in memberInfo[idx]['pref']:
            if memberInfo[idx]['pref'][pref]:
                i = pref_mapping[pref]
                pref_vector[i] += 1

    return pref_vector

def prepareSuggestions(pref_vector, start_lat_lng, radius):
    pref_mapping = {0:'tourist', 1:'museum', 2:'amusement_park', 3:'natural', 4:'tour', 5:'zoo'}
    unit_vec = np.array(pref_vector) / float(sum(pref_vector))
    suggestions_split = unit_vec * voting_suggestions_count

    if sum(suggestions_split) < voting_suggestions_count:
        idx = suggestions_split.index(max(suggestions_split))
        diff = voting_suggestions_count - sum(suggestions_split)
        suggestions_split[idx] += diff

    # suggestions_split is not a vector like [5, 5, 5, 5, 0, 0] where each index is a category
    # (that corresponds to pref_mapping) and each value (ex: 5) is how many places we need to find
    # for the voting step

    print('suggestions_split', suggestions_split)

    df = read_dataset()
    closest_idx, valid_places_idxs = find_closest_places(df, start_lat_lng, radius)

    # now we have a df of all the places within our radius
    df_valid = df.loc[valid_places_idxs, :]

    matches = []

    for idx, count in enumerate(suggestions_split):
        if count > 0:
            pref = pref_mapping[idx]

            potential_matches = []

            for idx_df, row in df_valid.iterrows():
                if row[pref] == 1:
                    potential_matches.append(idx_df)

            matches.append(np.random.choice(potential_matches, int(count), replace=False))

    matches = np.array(matches)
    matches = [item for sublist in matches for item in sublist]
    np.random.shuffle(matches)

    suggestions = df_valid.loc[matches, :]

    print(suggestions)

    return suggestions


def read_dataset():
    df = pd.read_csv('assets/final_dataset_sorted.csv')
    return df

def find_closest_places(df, start_lat_lng, radius):
    lat, lng = start_lat_lng
    best_lat, best_lng, best_dist, best_idx = 0.0, 0.0, 999900, -1
    valid_places = []
    for idx, row in df.iterrows():
        r_lat = float(row['lat'])
        r_lng = float(row['lng'])
        dist = latlng2miles(lat, lng, r_lat, r_lng)
        if dist < radius:
            valid_places.append(idx)
            if dist < best_dist:
                best_lat = r_lat
                best_lng = r_lng
                best_dist = dist
                best_idx = idx

    return best_idx, valid_places


def latlng2miles(lat1, lng1, lat2, lng2):
    R = 6373.0

    l1 = math.radians(lat1)
    ln1 = math.radians(lng1)
    l2 = math.radians(lat2)
    ln2 = math.radians(lng2)

    dlon = ln2 - ln1
    dlat = l2 - l1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    if a < 0:
        a = 0
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    conv_fac = 0.621371
    miles = distance * conv_fac

    return miles

def parseCategories(x):
    c = ast.literal_eval(x)
    return c

def getPlaceImageURL(placeId):
    res = google_places.get_place(placeId)
    res.get_details()
    res.photos[0].get(maxheight=500, maxwidth=500)
    return res.photos[0].url