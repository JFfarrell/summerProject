The customers app is repsonsible for the creation of the bus_routes schema in our database.

The graphQL interface for this django app is found at http://127.0.0.1:8000/.

The application contains the following files and directories:

`migrations/`
Contains a record of migrations applied by Django to the customers schema.

`admin.py`
Creates functionality for this app at localhost:8000/admin (login required).

`apps.py`
Creates the application customers.

`models.py`
Creates the Customers model class.

`schema.py`
This provides functionality for the provision of graphQL mutations and queries. One query
and three mutations are provided. They are listed here:

### Queries
-resolve_all_customers: returns all data of all customers

NOTE: Future creation of selective queries to be made!!

### Mutations
-create_customer: Add an additional entrant to the schema.

-update_customer: Alter an existing entrants data. Id is a required parameter.

-delete_customer: Remove a previous included entrant.

`urls.py`
Url routing provided for our app, directing to our graphQL portal.

`views.py`
Provision available for page "views" for our app. None currently implemented.