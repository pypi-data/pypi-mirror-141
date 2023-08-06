import mysql.connector

print_stat = False
DB = ""
cursor = ""

def DB(user_password="", hostname="localhost", username="root"):
    print("try to connect")
    try:
        Database = mysql.connector.connect(
            host = hostname,
            user = username,
            password = user_password
        )
    except:
        if print_stat:
            print("Could not connect to Database")
        return "unable to connect"

    if print_stat:
        print("Connection established")
    DB = Database
    return Database

def new_cursor():
    global cursor
    try:
        cursor = DB.cursor()
    except:
        if print_stat:
            print("Error while creating cursor on DB: " + str(DB))
        if DB == "":
            if print_stat:
                print("no database set")
        return "Error while creating cursor on DB: " + str(DB)
        

    if print_stat:
            print("Succesfully created cursor on DB: " + str(DB))
    return cursor

def new_DB(Name):
    global cursor
    command = "CREATE DATABASE " + str(Name)
    try:
        cursor.execute(command)
    except:
        if print_stat:
            print("Error while creating new DB: " + str(Name))
        if cursor == "":
            if print_stat:
                print("no cursor set")
                new_cursor()
                new_DB(Name)
        return "Error while creating new DB: " + str(Name)
    if print_stat:
        print("Suzccesfully created new database: " + str(Name))
    return
