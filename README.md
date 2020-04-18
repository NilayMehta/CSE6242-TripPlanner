# CSE6242-TripPlanner
I would recommend using a virutal env to run the project, but it's not required. To run it inside of a virtual env, follow these steps:
1. run 'python3 -m venv venv'
2. run 'source venv/bin/activate' to activate virtual env (this works on Mac OSX, for windows I think its 'venv\Scripts\activate')
3. run 'pip install -r requirements.txt'
4. run 'python app.py'

Without a virtual environment, all you need to do is run 
```
pip install -r requirements.txt
python app.py
```

This will open a server on http://127.0.0.1:5000/<br />

TSP stuff has been moved to util.py

TSP Readme Section from before:

To send request to TSP api you do the following:<br />
Send a GET request to the following resource<br />
http://127.0.0.1:5000/api/v1/TSP?places=<br />
where places is followed by a list of placeID for example<br />
http://127.0.0.1:5000/api/v1/TSP?places=ChIJ96XKNOZ-3YgRoPEc0B85Hqc,ChIJ98BffLK22YgRsymdIvOgjNA,ChIJgUulalN-3YgRGoTaWM2LawY,ChIJvRBCrN9-54gRGZuuaCLGrQE,ChIJyaCQzpHhwogRBdPcZI6UOyc<br /><br />

This will return a json request with a list of placeID in order under the 'request' field<br />

<h2>Checklist</h2>
- [x] TSP API
- [ ] Recommendation API
- [ ] UI Landing Page
- [ ] UI Map Page
