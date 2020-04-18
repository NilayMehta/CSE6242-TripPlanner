import flask
from flask import request, jsonify
import mlrose
import requests

app = flask.Flask(__name__)
app.config["DEBUG"] = True

my_API_key = "AIzaSyC0krOZZt0doCgSlAL0m75wxnq1GCIu5Tg"

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
