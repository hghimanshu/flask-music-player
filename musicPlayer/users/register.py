import os
import sys
import logging
from musicPlayer.db.users import InsertUser, fetchUserDetails


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class RegisterUser:
    def __init__(self, username, password, firstname, lastname, *args, **kwargs):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.insertObj = InsertUser()
        self.fetchObj = fetchUserDetails()
        self.message = ""
        self.successRes = False
    

    def insertUser(self):
        userAlreadyPresent = self.fetchObj.checkIfuserNameExists(self.username)
        if userAlreadyPresent is None:
            self.message = "Something went wrong!!"
            logging.info(self.message)

        elif userAlreadyPresent == {}:
            self.message = "User doesnt exists with this username"
            logging.info(self.message)
            self.insertObj.insert_into_db(username=self.username, 
                                                password=self.password,
                                                firstname=self.firstname,
                                                lastname=self.lastname )
            self.successRes = True

        else:
            self.message = "Username already exists !!"
            logging.info(self.message)
