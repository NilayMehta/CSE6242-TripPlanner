# CSE6242 Final Project - TripPlanner

## Description

Trip Planner is all about creating the perfect road trip. Our application collects and analyzes each group member's preferences to create the perfect itinerary for your next trip. Get started with planning your next road trip now!

A video demo of our application can be found here! 
https://youtu.be/Ih7Qt_MlxKY

This is a Flask project that runs on Python 3 with standard HTML and JS packages. As a overview of the files within the package,
here is a breakdown of important files and their function:

App.py

This file contains the majority of the functional logic for routing within the web app. It initializes and stores data 
regarding the group and itinerary, handles the logic for processing and passing data between web pages, and routes from one
web page to the next. This is also the file we run in order to start the web app.

Forms.py

This file contains Form objects represent and store the data collected from the various information gathering stages of our application.

Util.py

This file has various utility functions that are useful in various parts of the computation within the project such as 
data processing like parsing suggestions, conversions between metric and empirical units, catagory and voting suggestion spits, etc.

Suggestions.py

This file handles takes in the processed category preferences for the group and performs the data processing and calculations 
necessary to compute relevancy scores within our dataset. We take the top ranked destinations and pass this data onto the Voting
page for each member of the group to rank.

TSP.py

Once we have the votes of all the members, we process the data and using the preferences to being building the ideal 
itinerary for our group. This involves building a distance matrix based on driving time, initializing and running our TSP genetic
algorithm, adn converting the results into a usable format for our front end. 

Templates Directory and Associated Files

This directory contains all of our front end code that ingests the data from the back end and programmatically scales to 
display each part of the web app.


## Installation/Execution

In order to set up our project, please download our repository. Once you have have the project downloaded or cloned please follow the following steps (Please ensure that Python 3 is installed on your local machine):

1. Change directory into project

`cd CSE6242-TripPlanner/`

2. Set up a Vitrual Environment 

`run 'python3 -m venv venv'`

3. Activate Virtual Environment

OSX: `source venv/bin/activate`

WIndows: `'venv\Scripts\activate'`

4. Install dependencies

`pip install -r requirements.txt`

5. Run Application

`python app.py`

The application should now be operational! 

IMPORTANT: As a last step, please download and install this extension:
https://chrome.google.com/webstore/detail/moesif-orign-cors-changer/digfbfaphojjndkpccljibejjbppifbc?hl=en-US
Once it is installed, please enable it before using our App. On the map page of our application, 
we need to make external calls to Google's Maps API, and this extension resolves any potential browser issues that might 
occur during that process.

To speed things up, we have prepopulated some of the form fields like group 
information("Group Name", "Number of members", etc.) to make it quicker for the tester to use the application! 
It can be accessed at http://127.0.0.1:5000/
