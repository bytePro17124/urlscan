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

def export_to_sqlite3(fname_lname, email, _database):

    ## OPEN DATABASE
    sql_create_contactdb_table = ''' CREATE TABLE IF NOT EXISTS contactdb (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        firstname text NOT NULL,
                                        lastname text NOT NULL,
                                        emailaddress text NOT NULL
                                    ); '''
        # create a database connection

    conn = sqlite3.connect(_database)

    c = conn.cursor()
    
    try:
        c.execute('''CREATE TABLE fresh_email_contacts\
                 (ID integer PRIMARY KEY, FirstName text, LastName text, Email text)''')
    except sqlite.error:
        print("problem initializing the database")


    exports = prepare_contact_for_db(fname_lname, email)
    
    for e in exports:
        c.execute("INSERT INTO fresh_email_contacts VALUES (?,?,?)", (e[0],e[1],e[2]))

    conn.commit()

    conn.close()

    # conn = create_connection(database)
    # if conn is not None:
    #     # create projects table
    #     create_table(conn, sql_create_projects_table)
    #     # create tasks table
    #     create_table(conn, sql_create_tasks_table)
    # else:
    #     print("Error! cannot create the database connection.")

    # with conn:
    #     # create a new project
    #     project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30')
    #     project_id = create_project(conn, project)

    #     # tasks
    #     task_1 = ('Analyze the requirements', 1, 1, project_id, '2015-01-01', '2015-01-02')
    #     task_2 = ('Confirm the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')

    #     # create tasks
    #     create_task(conn, task_1)
    #     create_task(conn, task_2)

# def create_connection(db_file):
#     try:
#         conn = sqlite3.connect(db_file)
#         return conn
#     except Exception as e:
#         print(e)
#     return None

# def create_table(conn, create_table_sql):
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Exception as e:
#         print(e)

# def create_project(conn, project):
#     sql = ''' INSERT INTO projects(name,begin_date,end_date)
#               VALUES(?,?,?) '''
#     cur = conn.cursor()
#     cur.execute(sql, project)
#     return cur.lastrowid


## prepare_contact_for_db Changes The Imported firstandlastnames and emailaddresses 
## Data Into a List of Lists
## In preparation for export to database.
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
    export_to_sqlite3(first_last_names, email_addresses, _database)




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