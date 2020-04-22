#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash, url_for
import copy
from werkzeug.utils import redirect

import TSP
import suggestions
import util
import forms
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np

app = Flask(__name__)

app_data = {
    "name":         "Trip Planner",
    "transition":  "Lets get started",
    "html_title":   "Trip Planner App",
    "project_name": "CSE 6242 - Trip Planner"
}

group_form_data = {}

app.secret_key = 'big oof'

memberIndex = 0
memberInfo = {}

dataVar = None

votingResults = {}

memberPreferencesInit = {'tourist':0, 'museum':0, 'amusement_park':0, 'natural':0,
                         'tour':0, 'zoo':0, 'casino':0,'food':0}

N_COUNT = 20

@app.route('/')
def index():
    global memberIndex
    global memberInfo
    memberInfo = {}
    memberIndex = 0
    return render_template('index.html', app_data=app_data)

@app.route('/voting')
def voting():
    return render_template('groupindividualname.html', app_data=app_data)

@app.route('/grouplanding',  methods=('GET', 'POST'))
def grouplanding():
    global group_form_data
    global N_COUNT
    form = forms.GroupForm()
    if form.validate_on_submit():
        print('success')
        group_form_data['groupName'] = form.groupName.data
        group_form_data['groupSize'] = int(form.groupSize.data)
        group_form_data['startCity'] = form.startCity.data
        group_form_data['distance'] = int(form.distance.data)
        group_form_data['duration'] = int(form.duration.data)
        group_form_data['driveTime'] = float(form.driveTime.data)
        days = group_form_data['duration']
        if days <=2:
            N_COUNT = 12
        elif days == 3:
            N_COUNT = 16
        else:
            N_COUNT = 20
        print("N_COUNT:", N_COUNT)
        print(group_form_data)
        return render_template('groupindividualname.html', app_data=app_data, group_data=group_form_data, getStarted = True)
    print('no success')
    return render_template('grouplanding.html', app_data=app_data, form=form)


@app.route('/getstarted',  methods=('GET', 'POST'))
def getstarted():
    global memberIndex
    global memberInfo
    print(group_form_data)
    print(memberIndex)
    form = forms.Individual()
    if form.validate_on_submit():
        print('success')
        if memberIndex not in memberInfo:
            memberInfo[memberIndex] = {}
        memberInfo[memberIndex]['name'] = form.memberName.data
        memberInfo[memberIndex]['pref'] = copy.deepcopy(memberPreferencesInit)
        print(memberInfo)
        print(memberIndex)
        if memberIndex < group_form_data['groupSize']:
            return render_template('initPreferences.html', app_data=app_data, group_data=group_form_data, getStarted = False, memberIndex=memberIndex, memberInfo=memberInfo, dataVar=dataVar)

    return render_template('groupindividualname.html', app_data=app_data, group_data=group_form_data, getStarted = False, form=form, memberIndex=memberIndex)

@app.route('/nextMember', methods=('GET', 'POST'))
def preferenceGather():
    # TODO get preferences and add them to data
    # also add checks to make sure we dont keep going on forever and terminate at last member
    global memberIndex
    global memberInfo
    global group_form_data
    print(memberIndex)
    memberIndex += 1
    print(memberIndex)
    print(group_form_data)
    form = forms.Individual()
    if memberIndex < group_form_data['groupSize']:
        return render_template('groupindividualname.html', app_data=app_data, group_data=group_form_data, getStarted=False, form=form,
                           memberIndex=memberIndex)

    # After collecting all preferences, what do we do

    print('---- FINAL -----')
    print('memberInfo')
    print(memberInfo)

    positive_categories, negative_categories = suggestions.compileMemberInfo(memberInfo)

    max_distance = int(group_form_data['distance'])
    geolocator = Nominatim(user_agent='myapplication')
    location = geolocator.geocode(group_form_data['startCity'])
    lat = float(location.raw['lat'])
    lon = float(location.raw['lon'])
    coords = (lat, lon)

    memberIndex = 0

    print('positive_categories')
    print(positive_categories)

    print('negative_categories')
    print(negative_categories)

    filtered_dataset = suggestions.output_dataset(coords, max_distance, negative_categories, positive_categories, N_COUNT)
    filtered_dataset['categories'] = filtered_dataset['categories'].apply(util.parseCategories)
    # filtered_dataset['photo_url'] = filtered_dataset['place_id'].apply(util.getPlaceImageURL)
    filtered_dataset.to_csv('assets/suggestions/top20.csv', index=False)

    # filtered_dataset = pd.read_csv('assets/suggestions/top20.csv')
    # filtered_dataset['categories'] = filtered_dataset['categories'].apply(util.parseCategories)


    return render_template('voting.html', app_data=app_data, group_data=group_form_data, getStarted=False,
                           form=form, memberIndex=memberIndex, memberInfo=memberInfo,
                           tables=[filtered_dataset.to_html(classes='data', header="true")], suggestions=filtered_dataset)


@app.route('/test', methods=('GET', 'POST'))
def test():
    form = forms.ContactForm()
    if form.validate_on_submit():
        print('success')
        return render_template('groupindividualname.html', app_data=app_data)
    print('no success')
    return render_template('testForm.html', app_data=app_data, form=form)

@app.route('/testVoting', methods=['GET', 'POST'])
def testVoting():
    global memberIndex
    global votingResults

    values = []
    for idx in range(N_COUNT):
        values.append(request.form[str(idx)])

    print('values', values)

    votingResults[memberIndex] = values
    memberIndex += 1

    print('votingResults', votingResults)

    filtered_dataset = pd.read_csv('assets/suggestions/top20.csv')
    filtered_dataset['categories'] = filtered_dataset['categories'].apply(util.parseCategories)

    if memberIndex >= group_form_data['groupSize']:
        print("----------  start  ----------")
        ballot_arr = np.zeros(N_COUNT).astype(int)
        ballot_match = []
        for member_idx in votingResults:
            ballot_arr = ballot_arr + np.array(votingResults[member_idx]).astype(int)

        print("ballot_arr", ballot_arr)

        placeIds = filtered_dataset['place_id'].to_numpy()
        for place_idx, placeId in enumerate(placeIds):
            ballot_match.append((placeId, ballot_arr[place_idx]))

        sorted_ballots = sorted(ballot_match, key=lambda x: -x[1])

        print("sorted_ballots", sorted_ballots)

        sorted_placeIds = []
        for pair in sorted_ballots:
            sorted_placeIds.append(pair[0])

        print("final sorted_placeIds", sorted_placeIds)

        final_itin = TSP.TSP(sorted_placeIds, group_form_data['duration'], group_form_data['driveTime'])

        print(final_itin)

        return render_template('/index.html', app_data=app_data)

    return render_template('voting.html', app_data=app_data, group_data=group_form_data, memberIndex=memberIndex, memberInfo=memberInfo,
                           tables=[filtered_dataset.to_html(classes='data', header="true")],
                           suggestions=filtered_dataset)


@app.route('/setPref/pos/<pref>', methods=('GET', 'POST'))
def setPrefTouristPos(pref):
    form = forms.Individual()
    global memberInfo
    memberInfo[memberIndex]['pref'][pref] = 1
    print(memberInfo)
    return render_template('initPreferences.html', app_data=app_data, group_data=group_form_data, getStarted = False, memberIndex=memberIndex, memberInfo=memberInfo, dataVar=dataVar)

@app.route('/setPref/neg/<pref>', methods=('GET', 'POST'))
def setPrefTouristNeg(pref):
    form = forms.Individual()
    global memberInfo
    memberInfo[memberIndex]['pref'][pref] = -1
    print(memberInfo)
    return render_template('initPreferences.html', app_data=app_data, group_data=group_form_data, getStarted = False, memberIndex=memberIndex, memberInfo=memberInfo, dataVar=dataVar)

@app.route('/setPref/neutral/<pref>', methods=('GET', 'POST'))
def setPrefTouristNeutral(pref):
    form = forms.Individual()
    global memberInfo
    memberInfo[memberIndex]['pref'][pref] = 0
    print(memberInfo)
    return render_template('initPreferences.html', app_data=app_data, group_data=group_form_data, getStarted = False, memberIndex=memberIndex, memberInfo=memberInfo, dataVar=dataVar)


# ------- PRODUCTION CONFIG -------
#if __name__ == '__main__':
#    app.run()



# ------- DEVELOPMENT CONFIG -------
if __name__ == '__main__':
    app.run(debug=True)