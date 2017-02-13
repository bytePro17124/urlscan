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



def transfer_contacts_to_sqlitedb():
    f = urllib.request.urlopen(url_to_check)   # open the url
    s = f.read().decode('utf-8')               # read in and convert bytes 
                                               # to string
    # searches for phone numbers - not needed
    #re.findall(r"\+\d{2}\s?0?\d{10}",s)

    # search for first and last name
    re.finall(r"[]+&nbsp+[]",s)

    # searches for email addresses
    re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",s)  



def main(argv):

    url_to_check = "https://www.ohio.edu/engineering/about/people"

    transfer_contacts_to_sqlitedb(url_to_check)




if __name__ == "__main__":
    main(sys.argv[1:])