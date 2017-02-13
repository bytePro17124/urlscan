########################################################################################
# Programmer:          Matthew Jay Early
# File Created:        2017-02-13
# Program Description: This program runs in Python3 console and will scan a website
#                      for Emails and associated Names, exporting them to an SQLite3
#                      database.
########################################################################################

import urllib.request                         # for urlopen
import re                                     # for regular expressiosn
import sys                                    # for the command line argument


def pass_to_database(id_fname_lname_email):



def transfer_contacts_to_sqlitedb(url_to_check):
    f = urllib.request.urlopen(url_to_check)   # open the url
    s = f.read().decode('utf-8')               # read in and convert bytes 
                                               # to string
    # searches for phone numbers - not needed
    #re.findall(r"\+\d{2}\s?0?\d{10}",s)

    # search for first and last name
    first_last_names = re.findall(r"[A-Z]{1}[A-Za-z-]+\xa0[A-Z]{1}[A-Za-z-]+",s) #\xa0 is &nbsp; 

    # searches for email addresses
    email_addresses = re.findall(r"[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,4}",s)  



def main(argv):

    url_to_check = "https://www.ohio.edu/engineering/about/people"

    transfer_contacts_to_sqlitedb(url_to_check)

    print("Work Complete.")





if __name__ == "__main__":
    main(sys.argv[1:])