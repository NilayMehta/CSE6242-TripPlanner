#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash, url_for
import copy
from werkzeug.utils import redirect

import util
import forms

app = Flask(__name__)

app_data = {
    "name":         "Trip Planner",
    "transition":  "Lets get started",
    "html_title":   "Trip Planner App",
    "project_name": "CSE 6242 - Trip Planner",
    "keywords":     "flask, webapp, template, basic"
}

group_form_data = {}

app.secret_key = 'big oof'

memberIndex = 0
memberInfo = {}

dataVar = None

memberPreferencesInit = {'tourist':False, 'museum':False, 'amusement_park':False, 'natural':False, 'tour':False, 'zoo':False}


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
    form = forms.GroupForm()
    if form.validate_on_submit():
        print('success')
        group_form_data['groupName'] = form.groupName.data
        group_form_data['groupSize'] = int(form.groupSize.data)
        group_form_data['startCity'] = form.startCity.data
        group_form_data['distance'] = form.distance.data
        group_form_data['duration'] = int(form.duration.data)
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
    form = forms.Individual()
    if memberIndex < group_form_data['groupSize']:
        return render_template('groupindividualname.html', app_data=app_data, group_data=group_form_data, getStarted=False, form=form,
                           memberIndex=memberIndex)

    # After collecting all preferences, what do we do

    pref_vector = util.compileMemberInfo(memberInfo)
    print('pref_vector', pref_vector)
    start_lat_lng = (25.719375, -80.2756722)
    suggestions = util.prepareSuggestions(pref_vector, start_lat_lng, int(group_form_data['distance']))

    return render_template('voting.html', app_data=app_data, group_data=group_form_data, getStarted=False,
                           form=form, memberIndex=memberIndex, memberInfo=memberInfo)

    # if form.validate_on_submit():
    #     print('success')
    #     if memberIndex not in memberInfo:
    #         memberInfo[memberIndex] = {}
    #     memberInfo[memberIndex]['name'] = form.memberName.data
    #     print(memberInfo)
    #     return render_template('groupindividualname.html', app_data=app_data, group_data=group_form_data, getStarted = False, memberIndex=memberIndex, memberInfo=memberInfo)
    #
    # return render_template('groupindividualname.html', app_data=app_data, group_data=group_form_data, getStarted=False,
    #                        form=form)


@app.route('/test', methods=('GET', 'POST'))
def test():
    form = forms.ContactForm()
    if form.validate_on_submit():
        print('success')
        return render_template('groupindividualname.html', app_data=app_data)
    print('no success')
    return render_template('testForm.html', app_data=app_data, form=form)


@app.route('/setPref/<pref>', methods=('GET', 'POST'))
def setPrefTourist(pref):
    form = forms.Individual()
    global memberInfo
    memberInfo[memberIndex]['pref'][pref] = not memberInfo[memberIndex]['pref'][pref]
    print(memberInfo)
    return render_template('initPreferences.html', app_data=app_data, group_data=group_form_data, getStarted = False, memberIndex=memberIndex, memberInfo=memberInfo, dataVar=dataVar)


# ------- PRODUCTION CONFIG -------
#if __name__ == '__main__':
#    app.run()



# ------- DEVELOPMENT CONFIG -------
if __name__ == '__main__':
    app.run(debug=True)