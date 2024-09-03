import Business_Layer.validations as validation


def get_time():
    while True:
        time = input('Enter Time for the train (24 Hours Format HH : MM): ')
        is_valid_format = validation.check_time_format(time)
        if is_valid_format:
            return True
        else:
            print('Enter Valid Format!')
            return False




def get_int(msg1, msg2):
    while True:
        number = input(msg1)
        if number.isdigit():
            number = int(number)
            return number
        else:
            print(msg2)


def hours_to_minute(time):
    total_minutes = (time['Hours'] * 60) + time['Minutes']
    return total_minutes


def route_details():
    list_of_stations = []
    list_of_platforms = []
    list_of_arrival_time = []
    list_of_departure_time = []

    while True:
        while True:
            station_name = input("Enter Station Name: ")
            if station_name.isalpha() and station_name.isalnum():
                break
            else:
                print("Station Name can only Consist of Alphabets and digits! ")

        platform = get_int('Enter Platform Number: ', 'Platform should only contain digits')

        arrival_time = get_time()
        total_minutes = hours_to_minute(arrival_time)

        list_of_stations.append(station_name.lower().capitalize())
        list_of_platforms.append(platform)
        list_of_arrival_time.append(total_minutes)
        list_of_departure_time.append(total_minutes + 10)

        admin_choice = input("Do you wish to add stations? y/n: ")
        if admin_choice == 'n':
            break

    return {'list_of_stations': list_of_stations,
            'list_of_platforms': list_of_platforms,
            'list_of_arrival_time': list_of_arrival_time,
            'list_of_departure_time': list_of_departure_time
            }


def get_train_details():
    # getting train number
    while True:
        train_no = get_int('Enter Train Number', 'Train number should only contain digits')
        if train_no is None or len(str(train_no)) != 5:
            print('Please enter integer value with length = 5 ')
        else:
            break

    # getting train name
    while True:
        train_name = input("Enter Train Name: ")
        if train_name.isalpha() and train_name.isalnum():
            break
        else:
            print("Train Name can only Consist of Alphabets and digits! ")

    #getting train fare
    train_fare = get_int('Enter Train Fare', 'Fare should only contain digits')

    # getting tc assigned
    while True:
        tc_assigned = input("Enter TC Assigned: ")
        if tc_assigned.isalpha():
            tc_assigned = tc_assigned.lower().capitalize()
            break
        else:
            print("Enter TC Name Properly")

    # Getting Route details

    route_detail = route_details()
    route = route_detail['list_of_stations']
    platform_number = route_detail['list_of_platforms']
    arrival_time = route_detail['list_of_arrival_time']
    departure_time = route_detail['list_of_departure_time']

    return {
        'train_no': train_no, 'train_name': train_name, 'train_fare': train_fare,
        'tc_assigned': tc_assigned, 'starting_station_time': arrival_time[0],
        'ending_station_time': arrival_time[len(arrival_time)-1], 'route': route,
        'platform_number': platform_number,'arrival_time': arrival_time,
        'departure_time': departure_time
    }
