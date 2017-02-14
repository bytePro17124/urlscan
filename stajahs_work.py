# ****************************************************************************
#
#  PROGRAM THAT COLLECTS INFORMATION FROM WEB PAGE FOR DATABASE INSERTION
#
#  Description: CS 3200 Assignment 3 -
#               Python program reads the OU Engineering web site 
#               'https://www.ohio.edu/engineering/about/people' and collects
#               all the names and email addresses. The data collected is
#               inserted into a table in an SQLite3 database. The table
#               fields include: ID, First Name, Last Name, Email Address
#               All exceptions (sqlite3.Error) are collected.
#               A single command line argument is expected for the name of
#               the database.
#
#  Student Author: Stajah Hoeflich | sh024615@ohio.edu
#  Sun Feb 12 21:33:58 2017
#
# ****************************************************************************
import urllib.request	
import sqlite3
import sys
import os
import re
import ssl


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....open_page
# PURPOSE:.....reads the full string of text of the html data of a webpage
#              and returns the string, in this case the page that is read is
#              hard-coded - https://www.ohio.edu/engineering/about/people
# PARAMETERS:..none
# RETURNS:.....string of entire webpage html
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def open_page():
	try:
		link = 'https://www.ohio.edu/engineering/about/people'
		response = urllib.request.urlopen(link)
		webpage = response.read().decode(resource.headers.get_content_charset())


	except Exception as e:
		ctx = ssl.create_default_context()
		ctx.check_hostname = False
		ctx.verify_mode = ssl.CERT_NONE

		req = urllib.request.Request('https://www.ohio.edu/engineering/about/people')
		response = urllib.request.urlopen(req, context = ctx)
		webpage = response.read().decode(response.headers.get_content_charset())	
		print("Be aware that the following error has occurred:\n", e,
			  "\nThis program will still function but this error may have "
			  "security consequences.")
		return webpage

	else:
		return webpage


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....no_file_input_by_user
# PURPOSE:.....get name of database and appends the sys.argv tuple
# PARAMETERS:..none
# RETURNS:.....none
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def no_file_input_by_user():
	filename = input('What is the filename of the database: ')
	sys.argv.append(filename)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....get_correct_db
# PURPOSE:.....if there is a problem opening the provided database file
#              for reasons such as the file doesn't exist, or the user
#              typed it in wrong, then the program will keep asking for a
#              valid database filename and insert it into the sys.argv tuple
# PARAMETERS:..none
# RETURNS:.....None
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def get_correct_db():
    while (not os.path.isfile(sys.argv[1])):
        database = input('The database filename you entered does not exist '
                         'in this path. Please enter a correct file name: ')
        if os.path.isfile(database):
            sys.argv.insert(1, database)
            del sys.argv[2]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....get_database
# PURPOSE:.....if the user did not input a command line argument for the
#              database filename, the program will ask for it
# PARAMETERS:..none
# RETURNS:.....a string which is the name of the database that the user
#              wants to use to create a new table and insert the staff
#              member information
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def get_database():
    while len(sys.argv) < 2:
        if len(sys.argv) == 1:
            no_file_input_by_user()

    if (not os.path.isfile(sys.argv[1])):
        get_correct_db()
    return (sys.argv[1])


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....connect_to_database
# PURPOSE:.....connects to a valid, pre-existing database  
# PARAMETERS:..string which is the filename of a database
# RETURNS:.....None
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def connect_to_database(db_filename):
    try:
        connection = sqlite3.connect(db_filename)
        return connection
    except Error as e:
        print('Connection to database error: ', e)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....create_directory
# PURPOSE:.....
# PARAMETERS:..connection to a prexisting database
# RETURNS:.....None
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def create_directory(connection):
	cursor = connection.cursor()
	cursor.execute("""create table staff_members (ID integer primary key,
	            	  FirstName text,
	            	  LastName text,
					  EmailAddress text)""")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....insert_entry
# PURPOSE:.....
# PARAMETERS:..
# RETURNS:.....
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def insert_entry(connection, entry):
	cursor = connection.cursor()
	cursor.execute('''INSERT INTO staff_members(FirstName,LastName,EmailAddress)
		           VALUES(?,?,?) ''', entry)
	

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....page_str_space_adjust
# PURPOSE:.....collects info from a web page and inserts into database
# PARAMETERS:..none
# RETURNS:.....none
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def page_str_space_adjust(text):
	text = re.sub('\<a href="profiles.cfm\?profile=.*"\>', 'TRIGGER1', text)
	print (type(text))
	return text


def parse(each_entry):
	first = re.split(' ', each_entry)
	print(*first, '\n')
	

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....main
# PURPOSE:.....collects info from a web page and inserts into database
# PARAMETERS:..none
# RETURNS:.....none
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def main():
	page_str = str(open_page())
	db_connection = connect_to_database(get_database())

	create_directory(db_connection)


	page_str_triggers = page_str_space_adjust(page_str) 
	split_page_lst = page_str_triggers.split('TRIGGER1')
	split_page_lst.pop(0)
	print(split_page_lst[])


	for each_entry in split_page_lst:
		entry = parse(each_entry)
		# insert_entry(db_connection, entry)


	db_connection.commit()

	
	for row in db_connection.execute('SELECT * FROM staff_members'):
		print(row)


	db_connection.close()

	




if __name__ == "__main__":
    main()
