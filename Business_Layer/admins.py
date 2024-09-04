import json

import Database_Layer.db_utils as utils
import Business_Layer.helper as helper


class Admin:

    def add_new_train(self, train_details):
        if utils.get_train_details(train_details['train_no']):
            print('Train Number already exists! ')
            return
        if len(train_details['route']) < 2 :
            raise RuntimeError('Add minimum of 2 stations !')

        start_time_in_minutes = train_details['starting_station_time']
        end_time_in_minutes = train_details['ending_station_time']
        data_of_route = [train_details['route'], train_details['platform_number'],
                         train_details['arrival_time'], train_details['departure_time']]
        flag = helper.check_train_clash(start_time_in_minutes, end_time_in_minutes, data_of_route)

        if flag:
            print('There is a clashing with another Train! ')
        elif start_time_in_minutes >= end_time_in_minutes:
            print('Start time of the train should be less than end time !')
        elif end_time_in_minutes-start_time_in_minutes > 60*12 :
            print('Train cannot have a journey of more than 12 hours!')
        else:
            utils.insert_train_data(train_details)

    def remove_train(self, train_number):
        utils.delete_train(train_number)

    def update_train_fare(self, train_number, new_fare):
        if utils.get_train_details(train_number):
            utils.update_train_fare(train_number, new_fare)
            print('Train Fare updated! ')
        else:
            print('Train does not exists!')

    def update_train_platform(self, train_number, station, platform):
        if not utils.get_train_details(train_number):
            print('No such train exists! ')
            return
        train_details = utils.get_route_details(train_number)

        route_details = json.loads(json.dumps(train_details[0]))
        platform_details = json.loads(json.dumps(train_details[1]))
        route_details = route_details.strip('[').strip(']').split(',')
        platform_details = platform_details.strip('[').strip(']').split(',')
        #
        # route_details = json.loads(train_details[0][0])  #list
        # platform_details = json.loads(train_details[0][1])  #list
        print(route_details, type(route_details[0]), train_details, type(train_details), platform_details, type(platform_details))

        for index in range(len(route_details)):
            if route_details[index] == station:
                platform_details[index] = platform
                print(platform_details[index])
                platform_details = json.dumps(platform_details)
                print(platform_details, type(platform_details))
                utils.update_station_platform(train_number, platform_details)
                break

    def update_tc_assigned(self, train_number, new_tc):
        utils.update_tc_assigned(train_number, new_tc)
