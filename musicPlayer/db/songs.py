from pymodm import fields, MongoModel, ReferenceField
from pymodm.connection import connect
import json
import musicPlayer.db.connect as db_con
from musicPlayer.db.users import users
from datetime import datetime

class songs(MongoModel):
    # schema
    _id = fields.ObjectIdField(primary_key=True)
    title = fields.CharField()
    artist = fields.ListField(blank=True)
    uploadedOn = fields.DateTimeField(blank=True)
    uploadedBy = fields.ReferenceField(users, on_delete=ReferenceField.CASCADE)


class InsertSong:
    
    def __init__(self):
        pass


    def insert_to_db(self, title, artistInfo, uploadedBy):
        uploadedOn = datetime.now()
        data = songs(
            title=str(title),
            artist=artistInfo,
            uploadedOn=uploadedOn,
            uploadedBy=uploadedBy
        ).save()

        print('inserted song data for username : {}'.format(uploadedBy))


class FetchSongs:
    def __init__(self):
        pass

    
    def getAllSongsUploadedByUser(self, username):
        try:
            res = songs.objects.raw({'uploadedBy': username}).values()
            return list(res)
        except StopIteration:
            return []
        except Exception as e:
            print(str(e))
            return None


