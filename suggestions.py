import geopy.distance
import math
import pandas as pd
import ast

dataset = pd.read_csv('assets/final_dataset_sorted.csv')

def compileMemberInfo(memberInfo):
    catagory_mapping = {'tourist': ['tourist_attraction'], 'museum': ['museum', 'art_gallery'],
                        'amusement_park': ['amusement_park'], 'natural': ['natural_feature', 'campground'],
                         'tour': ['travel_agency'], 'zoo': ['zoo', 'aquarium'],
                        'casino': ['casino'], 'food': ['restaurant', 'cafe', 'bar']}
    negative_categories = []
    positive_categories = []

    for member_idx in memberInfo:
        prefs = memberInfo[member_idx]['pref']
        member_pos_cats = []
        member_neg_cats = []
        for catagory in prefs:
            if prefs[catagory] == 1:
                relevant_categories = catagory_mapping[catagory]
                for each in relevant_categories:
                    member_pos_cats.append(each)
            elif prefs[catagory] == -1:
                relevant_categories = catagory_mapping[catagory]
                for each in relevant_categories:
                    member_neg_cats.append(each)

        positive_categories.append(member_pos_cats)
        negative_categories.append(member_neg_cats)

    return (positive_categories, negative_categories)


def limit_travel_radius(initial_coords, maximum_distance, data):
    list_index=[]
    for i in range (len(data)):
        # coords_data = (dataset.iloc[i].lat, dataset.iloc[i].lng)
        coords_data = (data.iloc[i].lat, data.iloc[i].lng)
        if geopy.distance.distance(initial_coords, coords_data).miles > maximum_distance:
            list_index.append(i)
    data_new = data.drop(list_index)
    data_new = data_new.sort_values(by=['number'],ascending=False)
    data_new = data_new.reset_index()
    data_new = data_new.drop(["index"],axis=1)
    return data_new

def combine_preferences(categories_list):
    preferences={}
    for i in range(len(categories_list)):
        for cat in categories_list[i]:
            if cat not in preferences:
                preferences[cat]=1
            else:
                preferences[cat]+=1
    return preferences


def relevance_score(data, negative_preferences, positive_preferences):
    # max_nb_rating = int(dataset.iloc[0].number)
    max_nb_rating = int(data.iloc[0].number)

    list_score = []

    for i in range(len(data)):
        neg = 1
        pos = 1
        nb_rating = int(data.iloc[i].number)
        if nb_rating == 0:
            score = 0
        else:
            rating = data.iloc[i].rating
            list_categories = ast.literal_eval(data.categories[i])
            for cat in list_categories:
                if cat in negative_preferences:
                    neg += negative_preferences[cat]
                if cat in positive_preferences:
                    pos += positive_preferences[cat]

            score = ((math.log(nb_rating) / math.log(max_nb_rating)) * (rating / 5)) ** (neg / pos)
        list_score.append(score)

    data["relevance_score"] = list_score
    data = data[["place_name", "relevance_score", "place_id", "categories", "number", "rating", "address", "lat", "lng",
                 "photos", 'photo_url']]
    data = data.sort_values(by=['relevance_score'], ascending=False)
    data = data.reset_index()
    data = data.drop(["index"], axis=1)
    return data

def output_dataset(initial_coords, maximum_distance, negative_categories, positive_categories, suggestion_count):
    data = limit_travel_radius(initial_coords, maximum_distance, dataset)
    negative_preferences= combine_preferences(negative_categories)
    positive_preferences = combine_preferences(positive_categories)
    data = relevance_score(data,negative_preferences, positive_preferences)
    data = data.head(suggestion_count)
    return data

def test():
    coords_miami = (25.761681, -80.191788)
    maximum_distance = 400
    negative_categories = [[ "aquarium", "zoo","spa"],["movie_theater","cafe","casino"],["zoo","city_hall","bar"]]
    positive_categories = [[ "movie_theater","museum","bar"],["bar", "bowling_alley", "cafe"],["art_gallery","museum","aquarium"]]

    ex_output = output_dataset(coords_miami, maximum_distance, negative_categories, positive_categories)
    return ex_output
