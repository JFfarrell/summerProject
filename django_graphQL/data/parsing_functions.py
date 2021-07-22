# function to find and append the irish name for the stop
def agus_ainm(row, first_list, filtered_list):
    if row['stop_id'] in filtered_list:
        item = first_list[filtered_list.index(row['stop_id'])]
        return item[1]


# function to find and match the row with its correct customer facing route number
def route_finder(row):
    id_strings = row['trip_id'].split('-')
    return id_strings[1]


# function to create id column values
def create_id(row):
    return row["shape_id"] + "_" + row["stop_num"]


# function for isolating the stop number for each row
def stop_finder(row):
    stop_string = row['stop_name'].split(' ')
    if stop_string[-1].isdigit:
        return stop_string[-1]
    else:
        return "No stop number."


def route_direction(row):
    trip_string = row['trip_id']
    direction = trip_string[-1]
    if direction == "O":
        return "outbound"
    if direction == "I":
        return "inbound"


# and one more to change the trip_id to a shape_id as we have no need of unique trip info here
# this whole process has been about removing duplicated "shape" data, so unique trips don't help
def trip_to_shape_id(row):
    id_string = row['trip_id'].split('.')
    shape_id = id_string[2] + '.' + id_string[3] + '.' + id_string[4]
    return shape_id


def stops(row, df):
    current_route = row['route_num']
    stops_df = df[df['route_num'] == current_route]
    outbound_stops = stops_df[stops_df['direction'] == "outbound"]
    inbound_stops = stops_df[stops_df['direction'] == "inbound"]
    outbound_stops = outbound_stops["stop_num"].unique().tolist()
    inbound_stops = inbound_stops["stop_num"].unique().tolist()

    if row["direction"] == "outbound":
        stops = outbound_stops
    if row["direction"] == "inbound":
        stops = inbound_stops

    if len(stops) == 0:
        stops = "None"
    else:
        stops = ", ".join(stops)
    return stops


def name(row, df):
    current_route = row['route_num']
    current = df[df['route_num'] == current_route]
    inbound_names = current[current["direction"] == "inbound"]
    outbound_names = current[current["direction"] == "outbound"]
    inbound_names = inbound_names['stop_name'].tolist()
    outbound_names = outbound_names['stop_name'].tolist()

    if row["direction"] == "outbound":
        names = outbound_names
    if row["direction"] == "inbound":
        names = inbound_names

    if len(names) == 0:
        names = "None"

    else:
        names_modified = []
        for item in names:
            names_modified.append(item.split(",")[0])
        names = names_modified
        names = ([str(x) for x in names])
        names = ", ".join(names)
    return names


def coordinates(row, df):
    current_route = row['route_num']
    current = df[df['route_num'] == current_route]
    inbound_coords = current[current["direction"] == "inbound"]
    outbound_coords = current[current["direction"] == "outbound"]
    inbound_coords = inbound_coords['lat_long'].tolist()
    outbound_coords = outbound_coords['lat_long'].tolist()

    if row["direction"] == "outbound":
        coords = outbound_coords
    if row["direction"] == "inbound":
        coords = inbound_coords

    if len(inbound_coords) == 0:
        coords = "None"
    else:
        coords = ([str(x) for x in coords])
        coords = ", ".join(coords)
    return coords


def combine_coords(row, df):
    return str(row["latitude"]) + ", " + str(row["longitude"])


def unique_id(row):
    return row["route_num"] + "_" + row["direction"]


def route_nums(row):
    return row["route_num"]
