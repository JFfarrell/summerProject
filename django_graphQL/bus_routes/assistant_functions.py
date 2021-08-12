def to_timestamp(time_in_seconds):
    arrival_second = str(int(time_in_seconds % 60))
    remainder = time_in_seconds // 60
    arrival_minute = str(int(remainder % 60))
    arrival_hour = str(int(remainder // 60))

    # eliminate single digits in timestamp
    if len(arrival_hour) == 1:
        arrival_hour = f"0{arrival_hour}"
    if len(arrival_minute) == 1:
        arrival_minute = f"0{arrival_minute}"
    if len(arrival_second) == 1:
        arrival_second = f"0{arrival_second}"
    arrival_time = arrival_hour + ":" + arrival_minute + ":" + arrival_second
    return arrival_time


def timestamp_to_seconds(time_list):
    ftr = [3600, 60, 1]
    times_in_seconds = []

    for time in time_list:
        time_units = time.split(':')
        total_secs = (int(time_units[0]) * ftr[2]) + (int(time_units[1]) * ftr[1]) + (int(time_units[0]) * ftr[0])
        times_in_seconds.append(total_secs)

    times_in_seconds.sort()
    return times_in_seconds