import Business_Layer.helper
from Business_Layer.authentication import Authentication
import Business_Layer.validations as validation
from Business_Layer.trains import Train
import Presentation_Layer.input_helper as inp_helper
from Business_Layer.admins import Admin
from Business_Layer.helper import get_all_route_details

# object creation
auth = Authentication()
train = Train()
admin = Admin()

#initiating all tables
auth.initiate_all_tables()

# Dialoges
welcome_menu = """
_______________________________________________________________________________
 Welcome to Railway Management System
 What role are you trying to access:
    1. Login as Admin.
    2. Login as Guest.
    3. Exit
_______________________________________________________________________________
"""

admin_dialog = '''
_______________________________________________________________________________
What do you wish to do:
1. Create new Admin
2. Delete an existing Admin
3. Add New Train 
4. Remove Any Train
5. Update Train Fare 
6. Update Platform Number of a particular train for a particular station
7. Update TC Assigned
8. Show All Trains
9. Search Using Train number
10. Search Using Train Name 
11. Search using stations 
12. Show Route Of the train
13. Show platform number of a particular train at particular station
14. Show Fare
15. Back
_______________________________________________________________________________
'''

guest_dialog = '''
_______________________________________________________________________________
1. Show all trains
2. Search Using Train number
3. Search Using Train Name 
4. Search using stations 
5. Show Route Of the train
6. Show platform number of a particular train at particular station
7. Show Fare
8. Back
_______________________________________________________________________________
'''

# start
user_input = input(welcome_menu)


user_role = 'Guest'





def main_menu(user_input):
    global user_role

    while True:
        if user_input == '1':
            while True:
                username = input('Enter Username: ')
                password = input('Enter Password: ')

                is_username_valid = validation.check_username_and_password_format('username', username)
                is_password_valid = validation.check_username_and_password_format('password', password)

                if is_username_valid and is_password_valid:
                    user_role = auth.login_admin(username, password)
                    if user_role == 'Admin':
                        return user_role
                    else:
                        try_again = input(
                            'Admin login failed! Press enter to try again, press n to continue as guest: ')
                        if try_again == 'n':
                            return user_role

                else:
                    print('Check Your Username and Password Again! ')


        elif user_input == '2':
            return user_role

        elif user_input == '3':
            print('Terminating...')
            Business_Layer.helper.call_close_connection()
            exit()

        else:
            print('Enter Valid Choice! ')

        user_input = input(welcome_menu)


main_menu(user_input)


def guest_func():
    global user_input

    user_input = input(guest_dialog)
    while True:

        if user_input == '1':  # show all Trains
            train.show_all_trains()

        elif user_input == '2':  # search using train number
            train_no = input("Enter train number: ")
            if train_no.isdigit():
                train_no = int(train_no)
                train.search_by_train_number(train_no)
            else:
                if not train_no:
                    print('No input was provided!')
                else:
                    print("Provide only digits in the train number")

        elif user_input == '3':  # searching using train name
            train_name = input("Enter train name: ")
            if train_name.isalpha():
                train.search_by_train_name(train_name)
            else:
                if not train_name:
                    print('No input was provided!')
                else:
                    print("Provide Proper Name! ")

        elif user_input == '4':  # searching train using from stations and to station

            while True:
                from_station = input('Enter the From Station: ')
                if not from_station.isalpha():
                    print('Enter Valid Name! ')

                else:
                    from_station = from_station.lower().capitalize()
                    break

            while True:
                to_station = input('Enter the To Station: ')
                if not to_station.isalpha():
                    print('Enter Valid Name! ')

                else:
                    to_station = to_station.lower().capitalize()
                    break

            list_of_trains = train.show_train_using_stations(from_station, to_station)
            if not list_of_trains:
                print('No trains with the available route! ')

            else:
                print("The Following are the trains with the same route! ")
                for train_number in list_of_trains:
                    print(f"Train number: {train_number}")

        elif user_input == '5':  # show route
            train_no = input("Enter train number : ")
            if train_no.isdigit():
                train_no = int(train_no)
                train.show_route(train_no)
            else:
                if not train_no:
                    print('No input was provided!')
                else:
                    print("Provide only digits in the train number")

        elif user_input == '6':  # Show platform number of a particular train at particular station
            train_no = input("Enter the train number : ")
            if train_no.isdigit():
                train_no = int(train_no)
                station = input('Enter Station : ').lower().capitalize()
                if station.isalpha() and station.isalnum():
                    train.show_platform_number(train_no, station)  # todo Not implemented properly
                else:
                    if not station:
                        print('No input was provided!')
                    else:
                        print("Stations should also have a station name, not just numbers")

            else:
                if not train_no:
                    print('No input was provided!')
                else:
                    print("Provide only digits in the train number")


        elif user_input == '7':  #checking train fare

            train_no = input("Enter train number : ")

            if train_no.isdigit():
                train_no = int(train_no)
                starting_station = input("Enter starting station : ").lower().capitalize()
                ending_station = input("Enter Ending Station : ").lower().capitalize()

                if (starting_station.isalpha() and starting_station.isalnum() and
                        ending_station.isalpha() and ending_station.isalnum()):
                    train_fare = train.check_fare(train_no, starting_station, ending_station)
                    if train_fare:
                        print(train_fare)
                else:

                    print("Stations should also have a proper station name")
            else:
                if not train_no:
                    print('No input was provided!')
                else:
                    print("Provide only digits in the train number")

        elif user_input == '8':
            user_input = input(welcome_menu)
            main_menu(user_input)
        else:
            print("Enter Valid Choice!")

        user_input = input(guest_dialog)


def admin_func():
    user_input = input(admin_dialog)
    while True:

        if user_input == '1':
            pass
        elif user_input == '2':
            pass
        if user_input == '3':  #add new Train
            train_details = inp_helper.get_train_details()
            try:
                admin.add_new_train(train_details)
            except RuntimeError:
                print('Add minimum of 2 stations for the train !\n')
                continue

        elif user_input == '4':  #remove Train
            train_number = inp_helper.get_int('Enter Train_number: ', 'Please enter integer value only! ')
            admin.remove_train(train_number)
            print("Train successfully deleted")

        elif user_input == '5':  #update train fare
            train_number = inp_helper.get_int('Enter Train_number: ', 'Please enter integer value only! ')
            train_fare = inp_helper.get_int('Enter new train fare: ', 'Please enter integer value only! ')
            admin.update_train_fare(train_number, train_fare)


        elif user_input == '6':  #update station platform
            train_number = inp_helper.get_int('Enter Train_number: ', 'Please enter integer value only! ')
            station = input('Enter station name: ')
            if not station.isalpha():
                print('Enter Valid Name! ')
                break
            else:
                station = station.lower().capitalize()

            while True:
                platform = input('Enter platform number: ')
                if platform.isdigit():
                    platform = int(platform)
                    admin.update_train_platform(train_number, station, platform)
                    break
                else:
                    print('Please enter digits only! ')


        elif user_input == '7':  #update tc

            train_number = inp_helper.get_int('Enter Train_number: ', 'Please enter integer value only! ')
            while True:
                new_tc = input('Enter Name of Tc you wish to assign : ')
                if not new_tc.isalpha():
                    print('TC must have a name')
                    continue
                else:
                    break
            new_tc = new_tc.lower().capitalize()
            admin.update_tc_assigned(train_number, new_tc)
            print(f"{new_tc} is assigned as new TC ")

        elif user_input == '8':
            train.show_all_trains()

        elif user_input == '9':  #search by train number
            train_no = input("Enter train number: ")
            if train_no.isdigit():
                train_no = int(train_no)
                train.search_by_train_number(train_no)
            else:
                if not train_no:
                    print('No input was provided!')
                else:
                    print("Provide only digits in the train number")

        elif user_input == '10':  #search by train name
            train_name = input("Enter train name: ")
            if train_name.isalpha():
                train.search_by_train_name(train_name)
            else:
                if not train_name:
                    print('No input was provided!')
                else:
                    print("Provide Proper Name! ")

        elif user_input == '11':  #search using stations
            while True:
                from_station = input('Enter the From Station: ')
                if not from_station.isalpha():
                    print('Enter Valid Name! ')

                else:
                    from_station = from_station.lower().capitalize()
                    break

            while True:
                to_station = input('Enter the To Station: ')
                if not to_station.isalpha():
                    print('Enter Valid Name! ')

                else:
                    to_station = to_station.lower().capitalize()
                    break

            list_of_trains = train.show_train_using_stations(from_station, to_station)
            if not list_of_trains:
                print('No trains with the available route! ')
            else:
                print("The Following are the trains with the same route! ")
                for train_number in list_of_trains:
                    print(f"Train number: {train_number}")

        elif user_input == '12':

            train_no = input("Enter train number : ")
            if train_no.isdigit():
                train_no = int(train_no)
                train.show_route(train_no)
            else:
                if not train_no:
                    print('No input was provided!')
                else:
                    print("Provide only digits in the train number")

        elif user_input == '13':
            train.show_all_trains()
            train_no = input("Enter train number : ")
            if train_no.isdigit():
                train_no = int(train_no)
                station = input('Enter Station : ')
                if station.isalpha() and station.isalnum():
                    train.show_platform_number(train_no, station)  # todo Not implemented properly
                else:
                    if not station:
                        print('No input was provided!')
                    else:
                        print("Stations should also have a station name, not just numbers")
            else:
                if not train_no:
                    print('No input was provided!')
                else:
                    print("Provide only digits in the train number")

        elif user_input == '14':
            train_no = input("Enter train number : ")

            if train_no.isdigit():
                train_no = int(train_no)
                starting_station = input("Enter starting station : ").lower().capitalize()
                ending_station = input("Enter Ending Station : ").lower().capitalize()

                if (starting_station.isalpha() and starting_station.isalnum() and
                        ending_station.isalpha() and ending_station.isalnum()):
                    train_fare = train.check_fare(train_no, starting_station, ending_station)
                    if train_fare:
                        print(train_fare)
                else:

                    print("Stations should also have a proper station name")
            else:
                if not train_no:
                    print('No input was provided!')
                else:
                    print("Provide only digits in the train number")

        elif user_input == '15':
            user_input = input(welcome_menu)
            main_menu(user_input)

        else:
            print("Enter Valid Choice! ")

        user_input = input(admin_dialog)


if user_role == 'Guest':
    guest_func()
else:
    admin_func()
