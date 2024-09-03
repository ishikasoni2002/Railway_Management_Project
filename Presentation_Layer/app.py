from Business_Layer.authentication import Authentication
import Business_Layer.validations as validation
from Business_Layer.trains import Train
import Presentation_Layer.input_helper as inp_helper
from Business_Layer.admins import Admin

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
1. Add New Train 
2. Remove Any Train
3. Update Train Fare 
4. Update Platform Number of a particular train for a particular station
5. Update TC Assigned
6. Search a Train 
7. Show Route Of the train
8. Show platform number of a particular train at particular station
9. Show Fare
10. Exit
_______________________________________________________________________________
'''

guest_dialog = '''
_______________________________________________________________________________
1. Show all trains
2. Search using stations
3. Search a Train 
4. Show Route Of the train
5. Show platform number of a particular train at particular station
6. Show Fare
7. Exit
_______________________________________________________________________________
'''

#start
user_input = input(welcome_menu)
user_role = 'Guest'


# if user_input == '1':
#     while True:
#
#         username = input('''Enter new Username:
#                     The Username format should consist of:
#                     At least one digit,
#                     At least one Uppercase Letter,
#                     At least one Lowercase Letter,
#                     Minimum of 5 characters''')
#
#         flag_username = validation.check_username_and_password_format('username', username)
#
#         if flag_username:
#             is_unique = auth.is_unique_username(username)
#             if is_unique:
#                 break
#             else:
#                 print('This Username already exists. Please try again with different username!')
#         else:
#             print("Please Enter Valid Format Username to Sign up!\n")
#
#     while True:
#
#         password = input('''Enter your password:
#                     The Username format should consist of:
#                     At least one digit,
#                     At least one Uppercase Letter,
#                     At least one Lowercase Letter,
#                     At least One Special Character,
#                     Minimum of 8 characters''')
#
#         flag_password = validation.check_username_and_password_format('password', password)
#
#         if flag_password:
#             break
#         else:
#             print("Please Enter Valid Format Password to Sign up!\n")
#
#     while True:
#         root_password = input('Enter Root Password to Sign up as Admin: ')
#         root_is_valid = auth.check_root_password(root_password)
#         if root_is_valid:
#             auth.signup_new_admin(username, password)
#             print('\nSuccessfully Signed up! Please Login with your new Credentials')
#             break
#         else:
#             try_again = input('Invalid Root Password! \nTo discontinue press "n".')
#             if try_again == 'n':
#                 break

def main_menu():
    while True:
        if user_input == '1':

            while True:
                username = input('Enter Username: ')
                is_username_valid = validation.check_username_and_password_format('username', username)

                password = input('Enter Password: ')
                is_password_valid = validation.check_username_and_password_format('password', password)

                if is_username_valid and is_password_valid:
                    user_role = auth.login_admin(username, password)
                    if user_role == 'Admin':
                        return user_role
                        break
                    else:
                        try_again = input('Enter "n" to exit and continue as guest! ')
                        if try_again == 'n':
                            return user_role
                            break

                else:
                    print('Check Your Username and Password Again! ')

        elif user_input == '2':
            break

        elif user_input == '3':
            print('Terminating...')
            exit()

        else:
            print('Enter Valid Choice! ')

        user_input = input(welcome_menu)


# GUEST FUNCTIONS
# 1. Show all trains
# 7. Search using stations
#
# 2. Search a Train  using train number
# 3.  searching a train using train name
# 2. Show Route Of the train
# 3. Show platform number of a particular train at particular station
# 4. Show Fare
#
# 5. Exit


if user_role == 'Guest':
    user_input = input(guest_dialog)
    while user_input != '8':

        if user_input == '1':  #show all Trains
            train.show_all_trains()

        elif user_input == '2':  #search using train number
            train_no = input("Enter train number: ")
            if train_no.isdigit():
                train_no = int(train_no)
                train.search_by_train_number(train_no)
            else:
                if not train_no:
                    print('No input was provided!')
                else:
                    print("Provide only digits in the train number")

        elif user_input == '3':  #searching using train name
            train_name = input("Enter train name: ")
            if train_name.isalpha():
                train.search_by_train_name(train_name)
            else:
                if not train_name:
                    print('No input was provided!')
                else:
                    print("Provide Proper Name! ")

        elif user_input == '4': #searching using stations to station from station
            pass

        elif user_input == '5': #show route
            train_no = input("Enter train number")
            if train_no.isdigit():
                train_no = int(train_no)
                train.show_route(train_no)
            else:
                if not train_no:
                    print('No input was provided!')
                else:
                    print("Provide only digits in the train number")

        elif user_input == '6': #Show platform number of a particular train at particular station
            train_no = input("Enter train number")
            if train_no.isdigit():
                train_no = int(train_no)
                station = input('Enter Station')
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










        # elif user_input == '3':  #search using train name
        #     train_no = input("Enter train number")
        #     if train_no.isdigit():
        #         train_no = int(train_no)
        #         train.show_route(train_no)
        #     else:
        #         if not train_no:
        #             print('No input was provided!')
        #         else:
        #             print("Provide only digits in the train number")

        # elif user_input == '3':
        #     train.show_all_trains()
        #     train_no = input("Enter train number")
        #     if train_no.isdigit():
        #         train_no = int(train_no)
        #         station = input('Enter Station')
        #         if station.isalpha() and station.isalnum():
        #             train.show_platform_number(train_no, station)  #todo Not implemented properly
        #         else:
        #             if not station:
        #                 print('No input was provided!')
        #             else:
        #                 print("Stations should also have a station name, not just numbers")
        #
        #     else:
        #         if not train_no:
        #             print('No input was provided!')
        #         else:
        #             print("Provide only digits in the train number")

        elif user_input == '7':

            train_no = input("Enter train number")

            if train_no.isdigit():
                train_no = int(train_no)
                starting_station = input("Enter starting station").lower().capitalize()
                ending_station = input("Enter Ending Station").lower().capitalize()

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
            break
        else:
            print("Enter Valid Choice!")

        user_input = input(guest_dialog)


# ADMIN FUNCTIONS
else:
    user_input = input(admin_dialog)
    while user_input != '10':

        if user_input == '1':
            train_details = inp_helper.get_train_details()
            admin.add_new_train(train_details)

        elif user_input == '2':
            train_number = inp_helper.get_int('Enter Train_number', 'Please enter integer value only! ')
            admin.remove_train(train_number)
            print("Train successfully deleted")

        elif user_input == '3':
            train_number = inp_helper.get_int('Enter Train_number', 'Please enter integer value only! ')
            train_fare = inp_helper.get_int('Enter new train fare: ', 'Please enter integer value only! ')
            admin.update_train_fare(train_number, train_fare)
            print("Train Fare Updated! ")

        elif user_input == '4':
            train_number = inp_helper.get_int('Enter Train_number', 'Please enter integer value only! ')
            station = input('Enter station name: ')
            platform = input('Enter platform number: ')
            admin.update_train_platform(train_number, station, platform)

        elif user_input == '5':

            train_number = inp_helper.get_int('Enter Train_number', 'Please enter integer value only! ')
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

        elif user_input == '6':
            train.show_all_trains()
            train_no = input("Enter train number")
            if train_no.isdigit():
                train_no = int(train_no)
                train.search_by_train_number(train_no)
            else:
                if not train_no:
                    print('No input was provided!')
                else:
                    print("Provide only digits in the train number")


        elif user_input == '7':
            train.show_all_trains()
            train_no = input("Enter train number")
            if train_no.isdigit():
                train_no = int(train_no)
                train.show_route(train_no)
            else:
                if not train_no:
                    print('No input was provided!')
                else:
                    print("Provide only digits in the train number")

        elif user_input == '8':
            train.show_all_trains()
            train_no = input("Enter train number")
            if train_no.isdigit():
                train_no = int(train_no)
                station = input('Enter Station')
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


        elif user_input == '9':
            train.show_all_trains()
            train_no = input("Enter train number")

            if train_no.isdigit():
                train_no = int(train_no)
                starting_station = input("Enter starting station").lower().capitalize()
                ending_station = input("Enter Ending Station").lower().capitalize()

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



        elif user_input == '10':
            break

        else:
            print("Enter Valid Choice!")

        user_input = input(admin_dialog)
