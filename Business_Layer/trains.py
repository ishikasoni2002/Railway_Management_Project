import Database_Layer.db_utils as utils
import json
import Business_Layer.helper as helper


class Train:

    def show_all_trains(self):
        list_of_trains = utils.show_all_trains()
        if list_of_trains:
            print('The List Of Trains is as follows: \n')
            for train_detail in list_of_trains:
                print(f'Train Number: {train_detail[0]}, Train Name: {train_detail[1]}')
        else:
            print('No Trains exist! ')

    def search_by_train_number(self, train_number):
        train_details = utils.get_train_details(train_number)
        if train_details:
            helper.print_train_details(train_details)
        else:
            print('Train does not exists! ')

    def search_by_train_name(self, train_name):
        train_details = utils.get_train_details_using_name(train_name)
        if train_details:
            helper.print_train_details(train_details)
        else:
            print('Train does not exists! ')

    def show_route(self, train_number):
        train_details = utils.get_train_details(train_number)

        if train_details:
            res = utils.get_route_details(train_number)
            print(res[0][0])
        else:
            print('Train does not exists!')

    def show_platform_number(self, train_number, station):
        # todo yet to implement
        train_exists = utils.get_train_details(train_number)
        if train_exists:
            train_details = utils.get_route_details(train_number)
            print(train_details)
            print(train_details[0], type(train_details[0]))

            stations = json.loads(json.dumps(train_details[0]))
            platforms = json.loads(json.dumps(train_details[1]))
            stations = stations.strip('[').strip(']').split(',')
            platforms = platforms.strip('[').strip(']').split(',')

            for index in range(len(stations)):
                if stations[index].strip("'") == station:
                    print(f'The platform for {station} of train number {train_number} is: ', platforms[index])
                    break
            else:
                print('Station does not exists! ')

        else:
            print('Train does not exist!')

    def check_fare(self, train_number, from_station, to_station):
        train_details_if_exists = utils.get_train_details(train_number)
        if train_details_if_exists:
            train_route = utils.get_route_details(train_number)[0]
            train_route = json.loads(json.dumps(train_route))
            train_route = train_route.strip('[').strip(']').split(',')
            train_route = [route.strip(' ').strip("'") for route in train_route]
            from_index = -1
            to_index = -1

            for index in range(len(train_route)):
                if train_route[index].strip("'").lower().capitalize() == from_station:
                    from_index = index
                if train_route[index].strip("'").lower().capitalize() == to_station:
                    to_index = index
            if from_index != -1 and to_index != -1 and from_index <= to_index:
                train_fare = train_details_if_exists[0][2]

                total_stations = to_index - from_index
                if total_stations == 0:
                    print('You are on the station itself')
                elif total_stations > 0:
                    return (train_fare / (len(train_route) - 1)) * total_stations

            else:
                print("Enter valid stations and in correct format")

        else:
            print('Train does not exists!')
