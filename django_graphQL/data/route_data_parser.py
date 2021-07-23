import pandas as pd
import sqlite3
from parsing_functions import *
import warnings
warnings.filterwarnings('ignore')

print("Reading in data files...")
stop_times = pd.read_csv("files/stop_times.txt")
stops_df = pd.read_csv("files/stops.txt")
all_routes_sequences = pd.read_csv("files/route_seqs.csv")
print("all files read in.")

# I need a list of all "shapes"
all_shapes = []
all_trips = stop_times["trip_id"].tolist()
for route_id in all_trips:
    id_strings = route_id.split('.')
    shape_id = id_strings[2] + '.' + id_strings[3] + '.' + id_strings[4]
    if shape_id not in all_shapes:
        all_shapes.append(shape_id)
print("shapes list made")

# create an empty dataframe to fill from the stop_times df
# this may take some time
new_df = stop_times.iloc[0:0]
print("""
Empty data frame ready.
Appending parsed data to new dataframe.
This is the longest part of the script, please be patient.""")

remaining = len(all_shapes)
for shape_id in all_shapes:
    current_shape_df = stop_times[stop_times["trip_id"].str.contains(shape_id)]
    no_repeats = current_shape_df.drop_duplicates(subset=['stop_sequence'], keep='first')
    new_df = new_df.append(no_repeats, ignore_index=True)
    remaining -= 1
    print(f"Appended data from shapeID {shape_id}")
    print(f"{remaining} shapes left.")

new_df = new_df.drop(['arrival_time',
                      'departure_time',
                      'pickup_type',
                      'drop_off_type',
                      'shape_dist_traveled'], axis=1)
print("Excess data cleared from new dataframe.")

merged_df = pd.merge(new_df, stops_df, left_on='stop_id', right_on='stop_id', how='left')
print("stops and new df merged")

# we need some data from an extra file containing more info per each stop
db_routes_sequences = all_routes_sequences[all_routes_sequences["Operator"] == "DB"]
db_stops_filtered = db_routes_sequences[["AtcoCode", "ShortCommonName_ga"]]
print("dublin bus irish stop names filtered and ready to merge in.")


# And now we need to merge in the irish name and make some other changes
# !! warning !! some of these functions take a long time to run,

# we need a list of stops paired with their irish names to match with the dataframe
first_list = [tuple(r) for r in db_stops_filtered.to_numpy()]
filtered_list = []
for item in first_list:
    filtered_list.append(item[0])

print("Merging and altering dateframe, this may take some time...")

merged_df['ainm'] = merged_df.apply(agus_ainm, first_list=first_list, filtered_list=filtered_list, axis=1)
print("Irish names added successfully.")

merged_df['route_num'] = merged_df.apply(route_finder, axis=1)
print("Route numbers added successfully.")

merged_df['shape_id'] = merged_df.apply(trip_to_shape_id, axis=1)
print("trip id removed and replaced with shape id.")

merged_df['stop_num'] = merged_df.apply(stop_finder, axis=1)
print("stop numbers added successfully.")

merged_df["id"] = merged_df.apply(create_id, axis=1)
print("row id value created successfully.")

merged_df["direction"] = merged_df.apply(route_direction, axis=1)
print("Route direction added successfully.")

print("Data successfully merged. Altering column headers...")

merged_df.rename(columns={"stop_headsign": "destination",
                          "stop_lat": "latitude",
                          "stop_lon": "longitude"}, inplace=True)

print("Creating unique stops dataframe.")
unique_stops = merged_df.drop_duplicates(subset=['stop_num'], keep='first')
unique_stops = unique_stops[["stop_id",
                             "latitude",
                             "longitude",
                             "stop_name",
                             "ainm",
                             "stop_num"]].sort_values(by='stop_id')

print("Creating filtered dataframe, with only one instance per route.")
unique_routes = merged_df["route_num"].unique().tolist()
filtered_df = merged_df.iloc[0:0]

for db_route in unique_routes:
    current_shape_df = merged_df[merged_df["route_num"] == db_route]
    no_repeats = current_shape_df.drop_duplicates(subset=['stop_num'], keep='first')

    filtered_df = filtered_df.append(no_repeats, ignore_index=True)

filtered_df = filtered_df.drop(["trip_id", "shape_id"], axis=1)

print("Creating unique routes dataframe.")
unique_routes = merged_df.drop_duplicates(subset=['route_num', "direction"], keep='first')
unique_routes['stops'] = unique_routes.apply(stops, df=merged_df, axis=1)
unique_routes['longitudes'] = unique_routes.apply(coordinates, df=merged_df, coordinate="longitude", axis=1)
unique_routes['latitudes'] = unique_routes.apply(coordinates, df=merged_df, coordinate="latitude", axis=1)
unique_routes['names'] = unique_routes.apply(name, df=merged_df, axis=1)
unique_routes['id'] = unique_routes.apply(create_id, axis=1)


unique_routes = unique_routes[["id",
                               "route_num",
                               "stops",
                               "latitudes",
                               "longitudes",
                               "direction",
                               "destination",
                               "names"]].sort_values(by='route_num')


print("Complete. Loading to database now.")
db = sqlite3.connect("../db.sqlite3")
merged_df.to_sql("bus_routes_busroute", db, if_exists="replace", index=False)
unique_stops.to_sql("bus_routes_uniquestops", db, if_exists="replace", index=False)
unique_routes.to_sql("bus_routes_uniqueroutes", db, if_exists="replace", index=False)
filtered_df.to_sql("bus_routes_filteredroutes", db, if_exists="replace", index=False)
print("Finished. Whew, that was long...")
