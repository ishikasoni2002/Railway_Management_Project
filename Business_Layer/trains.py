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
            list_of_routes = json.loads(res[0])
            list_of_platforms = json.loads(res[1])
            list_of_arrival_time = json.loads(res[2])
            print(f"The Route of the Train {train_number} is as follows: ")
            for index in range(len(list_of_routes)):
                print(f"The train will arrive on {list_of_routes[index]} at platform 0{list_of_platforms[index]} at {helper.convert_minutes_to_time(list_of_arrival_time[index])}")

        else:
            print('Train does not exists!')

    def show_platform_number(self, train_number, station):
        train_exists = utils.get_train_details(train_number)
        if not train_exists:
            print('Train does not exist! ')
            return

        train_details = utils.get_route_details(train_number)
        route = train_details[0]
        platforms = train_details[1]
        stations = helper.json_string_to_list(route)
        platforms = helper.json_string_to_list(platforms)

        for index in range(len(stations)):
            if stations[index].strip('"') == station:
                print(f'The platform for {station} of train number {train_number} is: ', platforms[index])
                break
        else:
            print('Station does not exists! ')

    def check_fare(self, train_number, from_station, to_station):
        train_details_if_exists = utils.get_train_details(train_number)
        if train_details_if_exists:
            train_route = utils.get_route_details(train_number)[0]
            train_route = helper.json_string_to_list(train_route)
            train_route = [route.strip(' ').strip('"') for route in train_route]
            from_index = -1
            to_index = -1

            for index in range(len(train_route)):
                if train_route[index].strip('"').lower().capitalize() == from_station:
                    from_index = index
                if train_route[index].strip('"').lower().capitalize() == to_station:
                    to_index = index
            if from_index != -1 and to_index != -1 and from_index <= to_index:
                train_fare = train_details_if_exists[0][2]

                total_stations = to_index - from_index
                if total_stations == 0:
                    print('You are on the station itself')
                elif total_stations > 0:
                    print((train_fare / (len(train_route) - 1)) * total_stations)

            else:
                print("Enter valid stations and in correct format")

        else:
            print('Train does not exists!')

    def show_train_using_stations(self, from_station, to_station):
        Trains = []
        all_route_details = utils.get_all_route_details()

        train_numbers = [route[0] for route in all_route_details]
        stations = [json.loads(route[1]) for route in all_route_details]

        for index, station_route in enumerate(stations):
            try:
                from_index = station_route.index(from_station)
                to_index = station_route.index(to_station)

                if from_index < to_index:
                    Trains.append(train_numbers[index])
            except ValueError:
                continue

        return Trains
