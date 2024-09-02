import Database_Layer.db_utils as utils
import json
import Business_Layer.Helper as helper
class Train:


    def show_all_trains(self):
        list_of_trains = utils.show_all_trains()
        print('The List Of trains is as follows: \n')
        for train_detail in list_of_trains:
            print(f'Train Number: {train_detail[0]}, Train Name: {train_detail[1]}')

    def search_by_train_number(self, train_number):
        res = utils.get_train_details(train_number)
        if res:
            start_time= helper.convert_minutes_to_time(res[0][4])
            end_time= helper.convert_minutes_to_time(res[0][5])
            total_days= 0
            rem_time=0
            minutes=int()
            time=0
            if res[0][5]>24:
                total_days = (res[0][5]//60)//24
                rem_time = (res[0][4])//60 + (res[0][5])//60 - (24*total_days)
                time = (res[0][4])//60 + rem_time
                minutes= (res[0][4])%60
                print(minutes)
                if time>24:
                    total_days+=1
                    time = time-24

            print(f'\nThe Train Number is {res[0][0]}\n'
                  f'The Train Name is {res[0][1]}\n'
                  f'The Train Fare is {res[0][2]}\n'
                  f'The TC Assigned is {res[0][3]}\n'
                  f'The Train Journey Starts at {start_time}\n'
                  f'The Train Journey Ends after {total_days} days at {time} :: {minutes} \n'
                  )
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
        train_exists=utils.get_train_details(train_number)
        if train_exists:
            train_details = utils.get_route_details(train_number)
            stations = json.loads(train_details[0][0])
            platforms = json.loads(train_details[0][1])

            index = 0
            for index in range(len(stations)):
                if stations[index] == station:
                    print(f'The platform for {station} of train number {train_number} is: ', platforms[index])
                    break
            else:
                print('Station does not exists! ')

        else:
            print('Train does not exist!')



    def check_fare(self, train_number, from_station , to_station):
        is_train_existing = utils.get_train_details(train_number)
        print(is_train_existing)
        if is_train_existing:
            # print(utils.get_route_details(train_number))
            train_route = utils.get_route_details(train_number)[0][0]
            train_route = json.loads(train_route)
            from_index = -1
            to_index = -1

            for index in range(len(train_route)):
                if train_route[index] == from_station:
                    from_index = index
                if train_route[index] == to_station:
                    to_index = index
            if from_index != -1 and to_index != -1 and from_index <= to_index:
                train_fare =  is_train_existing[0][2]

                total_stations = to_index - from_index
                if total_stations == 0:
                    print('You are on the station itself')
                elif total_stations>0:
                    print ((train_fare / (len(train_route) - 1)) * total_stations)
                    return (train_fare / (len(train_route) - 1)) * total_stations


            else:
                print("Enter valid stations and in correct format")

        else:
                print('Train does not exists!')









