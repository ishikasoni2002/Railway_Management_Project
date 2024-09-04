from Database_Layer.connection import conn, cur
import Business_Layer.helper as helper
import json


def create_tables_if_not_exists():
    cur.execute('CREATE TABLE IF NOT EXISTS Trains('
                'TRAIN_NUMBER INTEGER NOT NULL PRIMARY KEY,'
                'TRAIN_NAME TEXT UNIQUE,  TRAIN_FARE INTEGER, '
                'TC_ASSIGNED TEXT, START_TIME INTEGER, END_TIME INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS Train_Route('
                'TRAIN_NUMBER INTEGER NOT NULL PRIMARY KEY,'
                'ROUTE JSON, PLATFORM JSON, ARRIVAL_TIME JSON, '
                'DEPARTURE_TIME JSON)')

    cur.execute('CREATE TABLE IF NOT EXISTS AdminUsers('
                'ID INTEGER PRIMARY KEY NOT NULL, '
                'USERNAMES TEXT, PASSWORDS TEXT)')

    conn.commit()


#admin User functions
def get_admin_users():
    cur.execute('SELECT * FROM AdminUsers ').fetchall()


def check_if_admin_table_empty():
    return cur.execute('select * from AdminUsers').fetchall() == []


def insert_first_admin_into_AdminUsers(username, hashed_password):
    if not check_if_admin_table_empty():
        return
    cur.execute('INSERT INTO AdminUsers VALUES(null, ?, ?)', (username, hashed_password))
    conn.commit()


def get_admin_details_from_username(username):
    return cur.execute('SELECT * FROM AdminUsers WHERE USERNAMES = ?', (username,)).fetchall()


#************************************************************************


#Login User Credentials
def get_hashed_password(username):
    return cur.execute('SELECT PASSWORDS FROM AdminUsers where '
                       'USERNAMES = ?', (username,)).fetchall()[0][0]


def duplicate_usernames(username):
    return cur.execute('SELECT * FROM AdminUsers WHERE '
                       'Usernames = ?', (username,)).fetchall()


def insert_new_admin(username, password):
    password = helper.generate_hash(password)
    cur.execute('Insert into AdminUsers VALUES(null, ?, ?)', (username, password))
    conn.commit()


def check_if_train_exists(train_number):
    return cur.execute('SELECT * FROM Trains WHERE train_number = ?', (train_number,)).fetchall() != []


def show_all_trains():
    return cur.execute('SELECT * FROM Trains').fetchall()


def get_train_details(train_number):
    return cur.execute('SELECT * FROM Trains WHERE train_number = ?', (train_number,)).fetchall()


def get_train_details_using_name(train_name):
    return cur.execute('SELECT * FROM Trains WHERE train_name = ?', (train_name,)).fetchall()


def delete_train(train_number):
    cur.execute('DELETE FROM Trains WHERE TRAIN_NUMBER =?', (train_number,))
    cur.execute('DELETE FROM Train_Route WHERE TRAIN_NUMBER =?', (train_number,))
    conn.commit()


def get_all_route_details():
    return cur.execute('SELECT * FROM Train_Route').fetchall()


def get_route_details(train_number):
    return cur.execute('SELECT ROUTE, PLATFORM, ARRIVAL_TIME FROM Train_Route WHERE train_number = ?', (train_number,)).fetchone()


def insert_train_data(train_details):
    train_number = train_details['train_no']
    train_name = train_details['train_name']
    train_fare = train_details['train_fare']
    tc_assigned = train_details['tc_assigned']
    train_start_time = train_details['starting_station_time']
    train_end_time = train_details['ending_station_time']
    train_route = json.dumps(train_details['route'])
    platform_numbers = json.dumps(train_details['platform_number'])
    arrival_time = json.dumps(train_details['arrival_time'])
    departure_time = json.dumps(train_details['departure_time'])
    cur.execute('INSERT INTO Trains VALUES(?,?,?,?,?,?)',
                (train_number, train_name, train_fare, tc_assigned, train_start_time, train_end_time))
    cur.execute('INSERT INTO Train_Route VALUES(?,?,?,?,?)',
                (train_number, train_route, platform_numbers, arrival_time, departure_time))

    conn.commit()


def update_train_fare(new_fare, train_no):
    print('hereeeeee')
    cur.execute('UPDATE Trains SET TRAIN_FARE =? WHERE TRAIN_NUMBER = ?', (new_fare, train_no))
    conn.commit()


def update_tc_assigned(train_number, new_tc):
    # IF TABLE DOES NOT EXISTS THROW ERROR
    if not check_if_train_exists(train_number):
        print('Train not found! ')
        return
    cur.execute('UPDATE Trains SET TC_ASSIGNED =? WHERE TRAIN_NUMBER = ?', (new_tc, train_number))
    conn.commit()


def get_time_details_of_start_and_end():
    return cur.execute('SELECT TRAIN_NUMBER, START_TIME, END_TIME FROM Trains').fetchall()


def update_station_platform(train_number, platform):
    if not check_if_train_exists(train_number):
        return
    cur.execute('UPDATE Train_Route SET PLATFORM = ? WHERE TRAIN_NUMBER = ?',
                (platform, train_number))
    conn.commit()


def close_connection():
    cur.close()
    conn.close()
