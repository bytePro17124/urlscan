import urllib.request	
import sqlite3
import sys
import os
import re
import ssl


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
		return webpage

	else:
		return webpage



def no_file_input_by_user():
	filename = input('What is the filename of the database: ')
	sys.argv.append(filename)


def get_correct_db():
    while (not os.path.isfile(sys.argv[1])):
        database = input('The database filename you entered does not exist '
                         'in this path. Please enter a correct file name: ')
        if os.path.isfile(database):
            sys.argv.insert(1, database)
            del sys.argv[2]


def get_database():
    while len(sys.argv) < 2:
        if len(sys.argv) == 1:
            no_file_input_by_user()

    if (not os.path.isfile(sys.argv[1])):
        get_correct_db()
    return (sys.argv[1])



def connect_to_database(db_filename):
    try:
        connection = sqlite3.connect(db_filename)
        return connection
    except Error as e:
        print('Connection to database error: ', e)



def create_directory(connection):
	try:
		cursor = connection.cursor()
		cursor.execute("""create table staff_members (ID integer primary key,
			  			  FirstName text,
			  			  LastName text,
			  			  EmailAddress text)""")
	except sqlite3.Error:
		cursor.executescript("drop table if exists staff_members;")



def insert_entry(connection, entry):
	try:
		cursor = connection.cursor()
		cursor.execute('''INSERT INTO staff_members(FirstName,LastName,EmailAddress)
		   			      VALUES(?,?,?) ''', entry)
	except sqlite3.Error:
		create_directory(connection)
		cursor = connection.cursor()
		cursor.execute('''INSERT INTO staff_members(FirstName,LastName,EmailAddress)
		   			      VALUES(?,?,?) ''', entry)		
	else:
		pass
	


def page_str_space_adjust(text):
	text = re.sub('\<a href="profiles.cfm\?profile=.*"\>', 'TRIGGER1', text)
	print (type(text))
	return text



def parse(each_entry):
	first = re.split(' ', each_entry)
	print(*first, '\n')
	

# main: collects info from a web page and inserts into database
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
		insert_entry(db_connection, entry)


	db_connection.commit()
	
	for row in db_connection.execute('SELECT * FROM staff_members'):
		print(row)

	db_connection.close()

	

if __name__ == "__main__":
    main()
