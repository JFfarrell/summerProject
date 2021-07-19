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