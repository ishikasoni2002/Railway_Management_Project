import bcrypt
import Database_Layer.db_utils as utils
import json


def generate_hash(password):
    print(password,"passwordd")
    pw_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw_bytes, salt)
    return hashed

def get_all_route_details():
    return utils.get_all_route_details()

def check_train_clash(start_time_in_minutes, end_time_in_minutes, data_of_route):
    train_route = data_of_route[0]
    route_specific_platforms = data_of_route[1]
    route_specific_arrival_time = data_of_route[2]
    route_specific_departure_time = data_of_route[3]

    time_detail = utils.get_time_details_of_start_and_end()
    if time_detail :

        index=0
        for time in time_detail:
            start_time =time_detail[index][1]
            end_time = time_detail[index][2]
            index+=1
            if ((start_time <= start_time_in_minutes and start_time_in_minutes<= end_time) or
                    (end_time_in_minutes<= end_time and end_time_in_minutes >= start_time)):  # can clash
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




def print_train_details(train_details):
    if train_details:
        start_time = convert_minutes_to_time(train_details[0][4])
        end_time = convert_minutes_to_time(train_details[0][5])

        print(f'\nThe Train Number is {train_details[0][0]}\n'
              f'The Train Name is {train_details[0][1]}\n'
              f'The Train Fare is {train_details[0][2]}\n'
              f'The TC Assigned is {train_details[0][3]}\n'
              f'The Train Journey Starts at {start_time}\n'
              f'The Train Journey starts at {start_time} and Ends at {end_time} \n'
              )
    else:
        print('Train does not exists')

def call_close_connection():
    utils.close_connection()

def get_index(li, value):
    try:
        from_index = li.index(value)
        return from_index
    except ValueError:
        return None

def json_string_to_list(train_detail):
    train_detail = json.loads(json.dumps(train_detail))
    train_detail = train_detail.strip('[').strip(']').split(',')
    return train_detail



