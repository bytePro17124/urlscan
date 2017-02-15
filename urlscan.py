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

	# create a database connection
	try:
		conn = sqlite3.connect(_database)
	except sqlite3.Error as e:
		print("Connection to database error: %s" % e)

	# fire up a cursor
	c = conn.cursor()

	# use the curosr to create a starting table
	try:
		c.execute('''CREATE TABLE fresh_email_contacts
					(ID integer PRIMARY KEY, FirstName text,
					LastName text, Email text)''')
	except sqlite3.Error:
		print("problem initializing the database")

	# turn our data source into a proper list of lists ready to export
	db_ready_list = prepare_contact_for_db(fname_lname, email)

	for e in db_ready_list:
		c.execute('''INSERT INTO fresh_email_contacts
					(FirstName,LastName,Email) VALUES (?,?,?)''',\
					(e[0],e[1],e[2]))

	conn.commit()

	conn.close()

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
	print("  \\0/")
	print("   |     NEW EMAILS!")
	print("  / \\")
	print("Work Complete. See your sqlite3 database file, %s" % argv[0])




if __name__ == "__main__":
	main(sys.argv[1:])
