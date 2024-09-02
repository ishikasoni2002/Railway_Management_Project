import bcrypt
import Database_Layer.db_utils as utils
import json


def generate_hash(password):
    pw_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw_bytes, salt)
    return hashed


def check_train_clash(start_time_in_minutes, end_time_in_minutes, data_of_route):
    train_route = data_of_route[0]
    route_specific_platforms = data_of_route[1]
    route_specific_arrival_time = data_of_route[2]
    route_specific_departure_time = data_of_route[3]

    time_detail = utils.get_time_details_of_start_and_end()
    start_time = time_detail[0][1]
    end_time = time_detail[0][2]

    for time in time_detail:
        if ((start_time <= time[1] and time[1] <= end_time) or
                (time[2] <= end_time and time[2] >= start_time)):  # can clash
            route_table_details = utils.get_all_route_details()

            for train_details in route_table_details:
                stations = json.loads(train_details[1])
                platforms = json.loads(train_details[2])
                arrival_time = json.loads(train_details[3])

                for index in range(len(stations)):
                    for index_of_new_entry in range(len(train_route)):
                        if stations[index] == train_route[index_of_new_entry]:
                            if arrival_time[index] == route_specific_arrival_time[index_of_new_entry]:
                                if platforms[index] == route_specific_platforms[index_of_new_entry]:
                                    return True
            else:
                return False

    else:
        return False


def convert_minutes_to_time(minutes):
    hours = minutes // 60
    min_time = minutes % 60
    time = f'{hours} :: {min_time}'
    return time


def call_close_connection():
    utils.close_connection()

