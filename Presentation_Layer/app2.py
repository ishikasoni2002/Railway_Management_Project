from Business_Layer.authentication import Authentication
import Business_Layer.validations as validation
from Business_Layer.trains import Train
import Presentation_Layer.input_helper as inp_helper
from Business_Layer.admins import Admin
from Database_Layer.connection import cur, conn
from Business_Layer.admin_Users import AdminUsers


auth = Authentication()
train = Train()
admin = Admin()
admin_users = AdminUsers()

auth.initiate_all_tables()

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
What do you wish to do:
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

def login():
    while True:
        username = input('Enter Username: ')
        password = input('Enter Password: ')

        is_username_valid = validation.check_username_and_password_format('username', username)
        is_password_valid = validation.check_username_and_password_format('password', password)

        if is_username_valid and is_password_valid:
            user_role = auth.login_admin(username, password)
            if user_role == 'Admin':
                return [user_role, username, password]
            else:
                try_again = input(
                    'Admin login failed! Press enter to try again, press n to continue as guest: ')
                if try_again == 'n':
                    return [user_role]

        else:
            print('Check Your Username and Password Again! ')
        still_continue = input('Press "n" to continue with other functions')
        if still_continue == 'n':
            return 'Guest'

def show_list_of_trains_using_stations(from_station, to_station):
    list_of_trains = train.show_train_using_stations(from_station, to_station)
    if not list_of_trains:
        print('No trains with the available route! ')
        return 0

    else:
        print("The Following are the trains with the same route! ")
        for train_number in list_of_trains:
            print(f"Train number: {train_number}")
        return 1



user_input = input(welcome_menu)
role = 'Guest'
def main_menu():
    while True:
        global user_input
        global role
        if user_input == '1':
            role = login()
            if role[0] == 'Admin':
                print("----You Are Logged In As Admin----")

                admin_users.set_username(role[1])
                admin_func()
            else:
                print('Log In Failed!!! ')



        elif user_input == '2':
            role = 'Guest'
            print("----You Are Logged In As Guest----")
            guest_func()

        elif user_input == '3':
            cur.close()
            conn.close()
            exit()

        else:
            print('Enter Valid Choice! ')

        user_input = input(welcome_menu)

def guest_func():
    choice = input(guest_dialog)
    while True:
        if choice == '1':
            train.show_all_trains()

        elif choice == '2':
            while True:
                train_no = input('Enter Train Number: ')
                is_train_no_valid= validation.check_train_number_format(train_no)
                if is_train_no_valid:
                    train_no = int(train_no)
                    train.search_by_train_number(train_no)
                    break
                else:
                    print("Provide only 5 digits in the train number! ")
                    still_continue = input('Press "n" to continue with other functions')
                    if still_continue == 'n':
                        break

        elif choice == '3':
            while True:
                train_name = input("Enter train name: ")
                if train_name.isalpha():
                    train.search_by_train_name(train_name)
                    break
                else:
                    print("Provide Proper Name! ")
                    still_continue = input('Press "n" to continue with other functions')
                    if still_continue == 'n':
                        break

        elif choice == '4':
            while True:
                from_station = input('Enter the From Station: ')
                to_station = input('Enter the To Station: ')
                is_valid_from_station = validation.check_station_name_format(from_station)
                is_valid_to_station = validation.check_station_name_format(to_station)

                if is_valid_from_station and is_valid_to_station:
                    from_station = from_station.lower().capitalize()
                    to_station = to_station.lower().capitalize()
                    successful = show_list_of_trains_using_stations(from_station,to_station)
                    if successful:
                        break
                    else:
                        still_continue = input('Press "n" to continue with other functions')
                        if still_continue == 'n':
                            break


        elif choice == '5':
            while True:
                train_no = input('Enter Train Number: ')
                is_train_no_valid = validation.check_train_number_format(train_no)
                if is_train_no_valid:
                    train_no = int(train_no)
                    train.show_route(train_no)
                    break
                else:
                    print("Provide only 5 digits in the train number! ")
                    still_continue = input('Press "n" to continue with other functions')
                    if still_continue == 'n':
                        break

        elif choice == '6':
            while True:
                train_no = input('Enter Train Number: ')
                station = input('Enter Station : ')

                is_train_no_valid = validation.check_train_number_format(train_no)
                is_valid_station = validation.check_station_name_format(station)

                if is_train_no_valid and is_valid_station:
                    train_no = int(train_no)
                    station = station.lower().capitalize()
                    train.show_platform_number(train_no, station)
                    break
                else:
                    print('Invalid Train Number or Train Name Format! ')
                    still_continue = input('Press "n" to continue with other functions')
                    if still_continue == 'n':
                        break

        elif choice == '7':
            while True:
                train_no = input('Enter Train Number: ')
                starting_station = input('Enter Starting Station : ')
                ending_station = input('Enter Ending Station: ')

                is_train_no_valid = validation.check_train_number_format(train_no)
                is_valid_starting_station = validation.check_station_name_format(starting_station)
                is_valid_ending_station = validation.check_station_name_format(ending_station)

                if is_train_no_valid and is_valid_starting_station and is_valid_ending_station:
                    train_no = int(train_no)
                    starting_station = starting_station.lower().capitalize()
                    ending_station = ending_station.lower().capitalize()

                    train.check_fare(train_no, starting_station, ending_station)
                    break
                else:
                    print("Please Enter in valid format!"
                          "\n1. The Train numbers should be digits."
                          "\n2. The station names should be Alphabets only and shouldn't contain spaces")
                    still_continue = input('Press "n" to continue with other functions')
                    if still_continue == 'n':
                        break

        elif choice == '8':
            return

        else:
            print('Enter Valid Choice!')
        choice = input(guest_dialog)



def admin_func():
    choice = input(admin_dialog)
    while True:

        if choice == '1':
            while True:
                username = input('Enter Username for new Admin: ')
                password = input('Enter Password for new Admin: ')

                is_username_valid = validation.check_username_and_password_format('username', username)
                is_password_valid = validation.check_username_and_password_format('password', password)

                if is_username_valid and is_password_valid:
                    new_admin_created = admin_users.create_new_admin(username, password)
                    if new_admin_created:
                        print('New Admin Created Successfully! ')
                        break
                    else:
                        print('Username Already exists! ')

                else:
                    print('Invalid Username/ Password Format! ')
                still_continue = input('Press "n" to continue with other functions')
                if still_continue == 'n':
                    break

        elif choice == '2':
            username = input('Enter The username of Admin you wish to delete! ')
            admin_users.remove_an_admin(username)



        elif choice == '8':
            train.show_all_trains()

        elif choice == '9':
            while True:
                train_no = input('Enter Train Number: ')
                is_train_no_valid= validation.check_train_number_format(train_no)
                if is_train_no_valid:
                    train_no = int(train_no)
                    train.search_by_train_number(train_no)
                    break
                else:
                    print("Provide only 5 digits in the train number! ")
                    still_continue = input('Press "n" to continue with other functions')
                    if still_continue == 'n':
                        break

        elif choice == '10':
            while True:
                train_name = input("Enter train name: ")
                if train_name.isalpha():
                    train.search_by_train_name(train_name)
                    break
                else:
                    print("Provide Proper Name! ")
                    still_continue = input('Press "n" to continue with other functions')
                    if still_continue == 'n':
                        break

        elif choice == '11':
            while True:
                from_station = input('Enter the From Station: ')
                to_station = input('Enter the To Station: ')
                is_valid_from_station = validation.check_station_name_format(from_station)
                is_valid_to_station = validation.check_station_name_format(to_station)

                if is_valid_from_station and is_valid_to_station:
                    from_station = from_station.lower().capitalize()
                    to_station = to_station.lower().capitalize()
                    successful = show_list_of_trains_using_stations(from_station,to_station)
                    if successful:
                        break
                    else:
                        still_continue = input('Press "n" to continue with other functions')
                        if still_continue == 'n':
                            break


        elif choice == '12':
            while True:
                train_no = input('Enter Train Number: ')
                is_train_no_valid = validation.check_train_number_format(train_no)
                if is_train_no_valid:
                    train_no = int(train_no)
                    train.show_route(train_no)
                    break
                else:
                    print("Provide only 5 digits in the train number! ")
                    still_continue = input('Press "n" to continue with other functions')
                    if still_continue == 'n':
                        break

        elif choice == '13':
            while True:
                train_no = input('Enter Train Number: ')
                station = input('Enter Station : ')

                is_train_no_valid = validation.check_train_number_format(train_no)
                is_valid_station = validation.check_station_name_format(station)

                if is_train_no_valid and is_valid_station:
                    train_no = int(train_no)
                    station = station.lower().capitalize()
                    train.show_platform_number(train_no, station)
                    break
                else:
                    print('Invalid Train Number or Train Name Format! ')
                    still_continue = input('Press "n" to continue with other functions')
                    if still_continue == 'n':
                        break

        elif choice == '14':
            while True:
                train_no = input('Enter Train Number: ')
                starting_station = input('Enter Starting Station : ')
                ending_station = input('Enter Ending Station: ')

                is_train_no_valid = validation.check_train_number_format(train_no)
                is_valid_starting_station = validation.check_station_name_format(starting_station)
                is_valid_ending_station = validation.check_station_name_format(ending_station)

                if is_train_no_valid and is_valid_starting_station and is_valid_ending_station:
                    train_no = int(train_no)
                    starting_station = starting_station.lower().capitalize()
                    ending_station = ending_station.lower().capitalize()

                    train.check_fare(train_no, starting_station, ending_station)
                    break
                else:
                    print("Please Enter in valid format!"
                          "\n1. The Train numbers should be digits."
                          "\n2. The station names should be Alphabets only and shouldn't contain spaces")
                    still_continue = input('Press "n" to continue with other functions')
                    if still_continue == 'n':
                        break

        elif choice == '15':
            return

        else:
            print('Enter Valid Choice!')
        choice = input(admin_dialog)



main_menu()



