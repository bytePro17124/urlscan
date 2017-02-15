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

def export_to_sqlite3(_data, _database):
	# create a database connection
	try:
		conn = sqlite3.connect(_database)
	except sqlite3.Error as e:
		print("Connection to database error: %s" % e)

	# fires up a cursor
	c = conn.cursor()

	# use the curosr to create a starting table
	try:
		c.execute('''CREATE TABLE fresh_email_contacts
					(ID integer PRIMARY KEY, FirstName text,
					LastName text, Email text)''')
	except sqlite3.Error as e:
		print("Problem initializing the database. Error: %s" % e)

	# iterate through our prepared data list and put the values into the table
	for d in _data:
		c.execute('''INSERT INTO fresh_email_contacts
					(FirstName,LastName,Email) VALUES (?,?,?)''',\
					(d[0],d[1],d[2]))

	# finalize our changes to the database
	conn.commit()

	# close our connection to the database file
	conn.close()
	


def prepare_contact_for_db(_fullname, _email):
	#make a list of firstname, lastname, email

	results = []                                    # local placeholder to return
	lst = []                                        # placeholder to helpo populate results

	for e in range(len(_fullname)):
		lst = _fullname[e].split("\xa0", 2) # splits first/last names
		lst.append(_email[e])                       # puts email addy with names
		print (lst)                                 # just to test that it is working
		results.append(lst)                         # put this list of names/email into a new list

	#and return it
	return results



def scan_site_to_db(_url, _database):
	# open the url sepcified
	f = urllib.request.urlopen(_url)
	## read in the site data from the url 
	#  convert bytes to characters 
	s = f.read().decode('utf-8')               
	## search for firstname&nbsp;lastname combinantion and store in a list
	#  \xa0 is &nbsp; 
	first_and_last_names = re.findall(r"[A-Z]{1}[.A-Za-z-]+\s*[A-Z]*.*\xa0[A-Z]{1}[A-Za-z-]+",s) 
	## search for emails
	#  search for re format matching after mailto:
	email_addresses = re.findall(r"(?<=mailto:)[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,4}",s) 
	#  turn it into proper formatting
	formatted_data = prepare_contact_for_db(first_and_last_names, email_addresses)
	#  export
	export_to_sqlite3(formatted_data, _database)




def main(argv):

	# checks to make sure something was passed in
	if len(argv) > 1:
		print('Too many arguments')
		print('use \'urlscan.py databasename.db\'')
		sys.exit()

	# this one is pretty self-explanatory
	url_to_check = "https://www.ohio.edu/engineering/about/people"

	# begin our main routine
	scan_site_to_db(url_to_check, argv[0])

	# finished message
	print("  \\0/")
	print("   |     NEW EMAILS! PREP THE SPAM!")
	print("  / \\")
	print("Work Complete. See your sqlite3 database file, %s" % argv[0])




if __name__ == "__main__":
	main(sys.argv[1:])
