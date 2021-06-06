import os
import sys
from musicPlayer.db.songs import FetchSongs
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class fetchSongInfo:
    def __init__(self, username):
        self.username = username
        self.fetchObj = FetchSongs()
        self.successResponse = False
        self.message = ""
        self.songs = None
    

    def getUserSongs(self):
        res = self.fetchObj.getAllSongsUploadedByUser(self.username)
        if res:
            self.message = "Fetched all songs of user" 
            self.successResponse = True
            self.songs = res
            logging.info(self.message)
        elif res == []:
            self.message = "User didn't have any songs associated with it"
        else:
            self.message = "Something went wrong !!"