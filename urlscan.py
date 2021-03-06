###########################################################################################
# Programmer:           Matthew Jay Early
# File Created:         2017-02-13
# Program Description:  This program runs in Python3 console and will scan a website for
#                        Emails and associated Names, exporting them to an SQLite3 database 
# Run command:          'python3 urlscan.py anyname.db'
###########################################################################################

import sqlite3                                # for database work
import urllib.request                         # for urlopen
import re                                     # for regular expressiosn
import sys                                    # for the command line argument


#  export_to_sqlite3 takes in a formatted data list and a database name and creates a
#   populated database of the name specified at program runtime
def export_to_sqlite3(_data, _database):
	try:
		conn = sqlite3.connect(_database)     # create a database connection
	except sqlite3.Error as e:
		print("Connection to database error: %s" % e)
		print("Quitting... ")
		sys.exit()

	c = conn.cursor()                         # fires up a cursor

	try:                                      # use the cursor to create a starting table
		c.execute('''CREATE TABLE fresh_email_contacts
					(ID integer PRIMARY KEY, FirstName text,
					LastName text, Email text)''')
	except sqlite3.Error as e:
		print("Problem initializing the database. Error: %s" % e)
		print("Quitting... ")
		sys.exit()

	for d in _data:                           # export our data into the table
		c.execute('''INSERT INTO fresh_email_contacts
					(FirstName,LastName,Email) VALUES (?,?,?)''',\
					(d[0],d[1],d[2]))

	conn.commit()                             # finalize our changes to the database

	conn.close()                              # close our connection to the database file


#  prepare_contact_for_db makes a list of firstname, lastname, email
#  relies on fullname being passed in sepearted by the &nbsp; characters
#    and an email passed in verbatim
#  returning format: [ (fn0,ln0,em0),(fn1,ln1,em1), ... ]
def prepare_contact_for_db(_fullname, _email):
	results = []                              # local placeholder to return
	lst = []                                    # placeholder to helpo populate results

	for e in range(len(_fullname)):
		lst = _fullname[e].split("\xa0", 2)   # splits first/last names
		lst.append(_email[e])                 # puts email addy with names
		print (lst)                           # just to test that it is working
		results.append(lst)                   # put this list of names/email into a new list

	return results                            # and return it


#  scan_site_to_db scans the website for data
#  scan_site_to_db is the controller routine for the functions: 
#   prepare_contact_for_db
#   export_to_sqlite3
def scan_site_to_db(_url, _database):
	f = urllib.request.urlopen(_url)          # open the url sepcified

	s = f.read().decode('utf-8')              # read in the site data and convert to characters
	
	# search for firstname lastname combinantion and store in a list
	# \xa0 is &nbsp; 
	first_and_last_names = re.findall(r"[A-Z]{1}[.A-Za-z-]+\s*[A-Z]*.*\xa0[A-Z]{1}[A-Za-z-]+",s)

	# search for emails
	# search for format matching after mailto: keyword
	email_addresses = re.findall(r"(?<=mailto:)[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,4}",s) 

	#  turn it into proper formatting with our other defined function
	formatted_data = prepare_contact_for_db(first_and_last_names, email_addresses)

	export_to_sqlite3(formatted_data, _database)   	#  export





#  main is the controller routine for scan_site_to_db
#  expects a database name to be specified at runtime ex: 'python3 urlscan.py anyname.db'
def main(argv):

	# checks to make sure something was passed in
	if len(argv) > 1:
		print('Too many arguments')
		print('use \'python3 urlscan.py databasename.db\'')
		sys.exit()

	# this one is pretty self-explanatory
	url_to_check = "https://www.ohio.edu/engineering/about/people"

	# begin our core routine
	scan_site_to_db(url_to_check, argv[0])

	# finished message
	print("  \\0/")
	print("   |     NEW EMAILS! PREP THE SPAM!")
	print("  / \\")
	print("Work Complete. See your sqlite3 database file, %s" % argv[0])




if __name__ == "__main__":
	main(sys.argv[1:])
