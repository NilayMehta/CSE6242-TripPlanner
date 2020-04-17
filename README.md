# CSE6242-TripPlanner
To run make sure you have packages specified in the requirments.txt file. If you do not use the following pip command to install files
```
pip install -r requirements.txt
```
<h2>TSP API</h2>
To run the api use the following command

```
python api_TSP.py
```

This will open a server on http://127.0.0.1:5000/<br />

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
