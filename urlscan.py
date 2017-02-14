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



def prepare_contact_for_db(firstandlastnames, emailaddresses):
    #make a list of firstname, lastname, email
    #and return it
    results = []
    lst = []
    for e in range(len(firstandlastnames)):
        lst = firstandlastnames[e].split("\xa0", 2)
        lst.append(emailaddresses[e])
        print (lst)  #just to test that it is working
        results.append(lst)
    return results


def transfer_contacts_to_sqlitedb(_url, _database):
    # open the url sepcified
    f = urllib.request.urlopen(_url)
    
    # read in teh data from the url convert bytes to characters 
    s = f.read().decode('utf-8')               
    
    # search for firstname&nbsp;lastname combinantion and store in a list
    first_last_names = re.findall(r"[A-Z]{1}[.A-Za-z-]+\s*[A-Z]*.*\xa0[A-Z]{1}[A-Za-z-]+",s) #\xa0 is &nbsp; 

    # search for emails and store in a list
    email_addresses = re.findall(r"(?<=mailto:)[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,4}",s)
    # email_addresses = re.findall(r"[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,4}",mailto)
    
    # pass this newfound data to our functon that works with the sqllite3 database
    # they should already be in order
    pass_to_database(first_last_names, email_addresses, _database)




def main(argv):

    # checks to make sure something was passed in
    if len(argv) > 1:
        print('Too many arguments')
        print('use \'urlscan.py databasename.db\'')
        sys.exit()

    # this one is pretty self-explanatory
    url_to_check = "https://www.ohio.edu/engineering/about/people"

    # begin our main routine
    transfer_contacts_to_sqlitedb(url_to_check, argv[0])

    # finished message
    print("Work Complete.")








if __name__ == "__main__":
    main(sys.argv[1:])