########################################################################################
# Programmer:          Matthew Jay Early
# File Created:        2017-02-13
# Program Description: This program runs in Python3 console and will scan a website
#                      for Emails and associated Names, exporting them to an SQLite3
#                      database.
########################################################################################

import sqlite3                                # for database manipulation
import urllib.request                         # for urlopen
import re                                     # for regular expressiosn
import sys                                    # for the command line argument

def pass_to_database(id_fname_lname_email, database):

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)
        # create tasks table
        create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")

    with conn:
        # create a new project
        project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30')
        project_id = create_project(conn, project)

        # tasks
        task_1 = ('Analyze the requirements', 1, 1, project_id, '2015-01-01', '2015-01-02')
        task_2 = ('Confirm the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')

        # create tasks
        create_task(conn, task_1)
        create_task(conn, task_2)

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

def create_project(conn, project):
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid

def create_task(conn, task):
    sql = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid

def transfer_contacts_to_sqlitedb(url_to_check):
    f = urllib.request.urlopen(url_to_check)   # open the url
    s = f.read().decode('utf-8')               # read in and convert bytes 
                                               # to string
    # searches for phone numbers - not needed
    #re.findall(r"\+\d{2}\s?0?\d{10}",s)

    # search for first and last name
    first_last_names = re.findall(r"[A-Za-z]+\xa0[A-Za-z]+",s)  #\xa0 is &nbsp; 

    # searches for email addresses
    email_addresses = re.findall(r"[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,4}",s)  



def main(argv):


    if len(argv) > 1:
        print('Too many arguments')                     #print proper format of arguments
        print('emailscrape.py <db_name>')               #print proper format of arguments
        sys.exit()

    db_name = argv

    id_fname_lname_email = ''

    url_link = "https://www.ohio.edu/engineering/about/people"

    transfer_contacts_to_sqlitedb(url_link)

    pass_to_database(id_fname_lname_email, db_name)


if __name__ == "__main__":
    main(sys.argv[1:])