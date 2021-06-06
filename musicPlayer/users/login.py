import os
import sys
import logging
from typing import Tuple
from musicPlayer.db.users import InsertUser, fetchUserDetails


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class LoginUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.fetchObj = fetchUserDetails()
        self.message = ""
        self.successResponse = False
    

    def checkCreds(self):
        res = self.fetchObj.checkUserCredentials(self.username, self.password)
        if res:
            self.message = "Successfully logged in !!" 
            self.successResponse = True
            logging.info(self.message)
        elif res == {}:
            self.message = "Username / Password didn't matched"
        else:
            self.message = "Something went wrong !!"