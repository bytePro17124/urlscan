########################################################################################
# Programmer:          Matthew Jay Early
# File Created:        2017-02-13
# Program Description: This program runs in Python3 console and will scan a website
#                      for Emails and associated Names, exporting them to an SQLite3
#                      database.
########################################################################################

import sqlite3                                # for database work
import urllib.request                         # for urlopen
import re                                     # for regular expressiosn
import sys                                    # for the command line argument


def pass_to_database(fname_lname, email, _database):
    sql_create_contactdb_table = """ CREATE TABLE IF NOT EXISTS contactdb (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        firstname text NOT NULL,
                                        lastname text NOT NULL,
                                        emailaddress text NOT NULL
                                    ); """

    # create a database connection
    conn = create_connection(_database)

    if conn is not None:
        # create projects table
        create_table(conn, sql_create_contactdb_table)
    else:
        print("Error! cannot create the database connection.")

    with conn:
        # create a new project
        # contact = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30')
        # contact = (firstname,lastname,email)
        contact = prepare_contact_for_db(fname_lname, email)

        project_id = create_project(conn, contact)

        
            
def create_connection(_database):
    try:
        conn = sqlite3.connect(_database)
        return conn
    except Exception as e:
        print(e)
    return None

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)

def create_project(conn, contact):
    sql = ''' INSERT INTO contactdb(firstname,lastname,emailaddress)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, contact)
    return cur.lastrowid

# def create_task(conn, task):
#     sql = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
#               VALUES(?,?,?,?,?,?) '''
#     cur = conn.cursor()
#     cur.execute(sql, task)
#     return cur.lastrowid

def prepare_contact_for_db(firstandlastnames, emailaddresses):
    #make a list of firstname, lastname, email
    #and return it
    results = []
    lst = []
    for e in range(len(emailaddresses)):
        lst = firstandlastnames[e].split("\xa0", 2)
        lst.append(emailaddresses[e])
        # print (lst)  #just to test that it is working
        results.append(lst)
    print (results)


    return results



def transfer_contacts_to_sqlitedb(_url, _database):
    # open the url sepcified
    f = urllib.request.urlopen(_url)
    
    # read in teh data from the url convert bytes to characters 
    s = f.read().decode('utf-8')               
    
    # search for firstname&nbsp;lastname combinantion and store in a list
    first_last_names = re.findall(r"[A-Z]{1}[A-Za-z-]+\xa0[A-Z]{1}[A-Za-z-]+",s) #\xa0 is &nbsp; 
    # change it int a set to remove duplicates then back to a list
    set(first_last_names)
    list(first_last_names) 


    # search for emails and store in a list
    email_addresses = re.findall(r"[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,4}",s)  
    # change it into a set to remove duplicates then back to a list
    set(email_addresses)
    list(email_addresses)
    
    # pass this newfound data to our functon that works with the sqllite3 database
    # they should already be in order
    pass_to_database(first_last_names, email_addresses, _database)


def main(argv):

    if len(argv) > 1:
        print('Too many arguments')
        print('use \'urlscan.py databasename.db\'')
        sys.exit()

    url_to_check = "https://www.ohio.edu/engineering/about/people"

    transfer_contacts_to_sqlitedb(url_to_check, argv[0])

    print("Work Complete.")





if __name__ == "__main__":
    main(sys.argv[1:])