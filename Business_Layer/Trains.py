import Database_Layer.db_utils as utils
import json

class Train:


    def show_all_trains(self):
        list_of_trains = utils.show_all_trains()
        print('The List Of trains is as follows: ')
        for train_detail in list_of_trains:
            print(f'Train Number: {train_detail[0]}, Train Name: {train_detail[1]}')

    def search_by_train_number(self, train_number):
        res = utils.get_train_details(train_number)
        if res:
            print(res[0])
        else:
            print('Train does not exists')


    def show_route(self, train_number):
        is_train_existing = utils.get_train_details(train_number)

        if is_train_existing:
            res = utils.get_route_details(train_number)
            print(res[0][0])
        else:
            print('Train does not exists!')

    def show_platform_number(self, train_number, station):
        # todo yet to implement
        train_details = utils.get_route_details(train_number)
        stations = json.loads(train_details[0][0])
        platforms = json.loads(train_details[0][1])

        print(stations)

        index = 0
        for index in range(len(stations)):
            print(len(stations), index, stations[index])
            if stations[index] == station:
                print(f'The platform for {station} of train number {train_number} is: ', platforms[index])
                break
        else:
            print('Station does not exists! ')



    def check_fare(self, train_number, from_station , to_station):
        is_train_existing = utils.get_train_details(train_number)

        if is_train_existing:
            train_route = utils.get_route_details(train_number)[0][0]
            train_route = json.loads(train_route)
            from_index = -1
            to_index = -1

            for index in range(len(train_route)):
                if train_route[index] == from_station:
                    from_index = index
                elif train_route[index] == to_station:
                    to_index = index

            if from_index != -1 and to_index != -1 and from_index<to_index:
                train_fare = utils.get_train_details(train_number)[0][2]

                total_stations = to_index - from_index
                if total_stations == 0:
                    print('You are on the station itself')
                elif total_stations>0:
                    return (train_fare / (len(train_route) - 1)) * total_stations


            else:
                print(from_index, to_index)
                print("Enter valid stations and in correct format")

        else:
                print('Train does not exists!')









