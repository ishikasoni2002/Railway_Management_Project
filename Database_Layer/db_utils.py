from Database_Layer.connection import conn, cur
import Business_Layer.Helper as helper
import json


def create_tables_if_not_exists():
    cur.execute('CREATE TABLE IF NOT EXISTS Trains('
                'TRAIN_NUMBER INTEGER NOT NULL PRIMARY KEY,'
                'TRAIN_NAME TEXT,  TRAIN_FARE INTEGER, '
                'TC_ASSIGNED TEXT, START_TIME INTEGER, END_TIME INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS Train_Route('
                'TRAIN_NUMBER INTEGER NOT NULL PRIMARY KEY,'
                'ROUTE JSON, PLATFORM JSON, ARRIVAL_TIME JSON, '
                'DEPARTURE_TIME JSON)')

    cur.execute('CREATE TABLE IF NOT EXISTS AdminUsers('
                'ID INTEGER PRIMARY KEY NOT NULL, '
                'USERNAMES TEXT, PASSWORDS TEXT)')

    conn.commit()


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


def get_train_details(train_number):
    return cur.execute('SELECT * FROM Trains WHERE train_number = ?', (train_number,)).fetchall()


# def show_route(train_number):
#     return cur.execute('SELECT ROUTE FROM Trains WHERE train_number = ?', (train_number,)).fetchall()


def get_all_route_details():
    return cur.execute('SELECT * FROM Train_Route').fetchall()
def get_route_details(train_number):
    return cur.execute('SELECT ROUTE, PLATFORM FROM Train_Route WHERE train_number = ?', (train_number,)).fetchall()


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


def delete_train(train_number):
    cur.execute('DELETE FROM Trains WHERE TRAIN_NUMBER =?', (train_number,))
    cur.execute('DELETE FROM Train_Route WHERE TRAIN_NUMBER =?', (train_number,))
    conn.commit()
    print("Train Does not exist anymore")


def update_train_fare(new_fare, train_no):
    # IF TABLE DOES NOT EXISTS THROW ERROR
    cur.execute('UPDATE Trains SET TRAIN_FARE =? WHERE TRAIN_NUMBER = ?', (new_fare, train_no))
    conn.commit()
    print("Train Fare Updated! ")


def update_tc_assigned(train_no, new_tc):
    # IF TABLE DOES NOT EXISTS THROW ERROR
    cur.execute('UPDATE Trains SET TC_ASSIGNED =? WHERE TRAIN_NUMBER = ?', (new_tc, train_no))
    conn.commit()
    new_tc = new_tc.capitalize()
    print(f"{new_tc} is assigned as new TC ")


def get_time_details_of_start_and_end():
    return cur.execute('SELECT TRAIN_NUMBER, START_TIME, END_TIME FROM Trains').fetchall()

def show_all_trains():
    return cur.execute('SELECT * FROM Trains').fetchall()
