########################################################################################
# Programmer:          Matthew Jay Early
# File Created:        2017-02-13
# Program Description: This program runs in Python3 console and will scan a website
#                      for Emails and associated Names, exporting them to an SQLite3
#                      database.
########################################################################################

import sqllite3                               # for database work
import urllib.request                         # for urlopen
import re                                     # for regular expressiosn
import sys                                    # for the command line argument


def pass_to_database(fname_lname, email, _database):
    sql_create_contactdb_table = """ CREATE TABLE IF NOT EXISTS contactdb (
                                        id integer PRIMARY KEY,
                                        firstname text NOT NULL,
                                        lastname text NOT NULL,
                                        emailaddress text NOT NULL
                                    ); """

    # create a database connection
    conn = create_connection(_database)
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)
        # create tasks table
        create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")

    with conn:
        # create a new project
        # contact = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30')
        # contact = (firstname,lastname,email)
        contact = prepare_contact_for_db(fname_lname, email)

        project_id = create_project(conn, contact)

        
            
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
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

def prepare_contact_for_db():
    #make a list of firstname, lastname, email
    #and return it


def transfer_contacts_to_sqlitedb(_url, _database):
    f = urllib.request.urlopen(_url)   # open the url
    s = f.read().decode('utf-8')               # read in and convert bytes 
                                               # to string
    # searches for phone numbers - not needed
    #re.findall(r"\+\d{2}\s?0?\d{10}",s)

    # search for first and last name
    first_last_names = re.findall(r"[A-Z]{1}[A-Za-z-]+\xa0[A-Z]{1}[A-Za-z-]+",s) #\xa0 is &nbsp; 

    # searches for email addresses
    email_addresses = re.findall(r"[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,4}",s)  

    pass_to_database(first_last_names, email_addresses, _database)



def main(argv):

    if len(argv) > 1:
        print('Too many arguments')                     #print proper format of arguments
        print('emailscrape.py <db_name>')               #print proper format of arguments
        sys.exit()

    url_to_check = "https://www.ohio.edu/engineering/about/people"

    transfer_contacts_to_sqlitedb(url_to_check, argv[0])

    print("Work Complete.")





if __name__ == "__main__":
    main(sys.argv[1:])