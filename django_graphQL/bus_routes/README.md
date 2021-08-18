The bus_routes app is repsonsible for the creation of the bus_routes schema in our database.

The graphQL interface for this django app is found at http://127.0.0.1:8000.

The application contains the following files and directories:

`route_models/`
Linear regression models for bus route predictions.
- Inputs for the prediction: Hour, Day, Month, Rain & Temperature.
- Outputs of the prediction: Journey Time.

`migrations/`
Contains a record of migrations applied by Django to the bus_routes schema.

`weather/`
Data parsing function for provision of current weather information to be sent to the front-end.

`admin.py`
Creates functionality for this app at localhost:8000/admin (login required).

`apps.py`
Creates the application bus_routes.

`models.py`
Creates the BusRoute model class.

`types.py`
Contains graphene object types

`schema.py`
Creates a BusRoute object that can be queried by graphQL. Querys housed here are as follows:

- resolve_unique_stops: returns every unique stop

- resolve_unique_routes: returns every unique route
![route1in](https://user-images.githubusercontent.com/71881578/126664189-0173cf28-a8f2-45e9-b0b3-b1d0119149a1.PNG)
![route1out](https://user-images.githubusercontent.com/71881578/126664199-8751caf9-cad0-4f65-9133-de88ebc01493.PNG)

- resolve_all_bus_routes: catch all. returns all data for all routes, no parameters required.
![allQ](https://user-images.githubusercontent.com/71881578/125189397-ce744a00-e22f-11eb-9914-c4a44b18ce2f.PNG)

- resolve_weather
This query returns a dictionary of hourly weather data for the next 24hrs.
The key for each dictionary entry follows the following format: "day from current day" + "-" + "hour"
Only 3 weather data items are included as this is all we require so far, this can be changed easily in the future if required
![image](https://user-images.githubusercontent.com/25707613/129356397-3ef299c8-0564-43af-a81e-11b7270a6bfd.PNG)

`tests.py`
Space for unittesting. No unittests currently applied.

`urls.py`
Url routing provided for our app, directing to our graphQL portal.

`views.py`
Provision available for page "views" for our app. None currently implemented.
