from pymodm import fields, MongoModel
from pymodm.connection import connect
import json
import musicPlayer.db.connect as db_con
import uuid
from musicPlayer.config.config import SECRET_KEY
from cryptography.fernet import Fernet
from datetime import datetime


class users(MongoModel):
    # schema
    username = fields.CharField(primary_key=True)
    firstname = fields.CharField(blank=True)
    lastname = fields.CharField(blank=True)
    password = fields.CharField()
    created_at = fields.DateTimeField()
    token = fields.CharField()


class InsertUser():
    '''
    class to insert data into Users collection
    '''
    def __init__(self):
        self.key = SECRET_KEY
        self.fernet = Fernet(self.key)
        
    def insert_into_db(self,username,password, firstname,lastname):
        encrypted_password = self.fernet.encrypt(password.encode()).decode('ascii')
        # encrypted_password = hash(str(uuid.uuid5(uuid.NAMESPACE_OID, password)))
        data = users(
            username=str(username),
            firstname=str(firstname), 
            lastname=str(lastname),
            password=str(encrypted_password),
            created_at=datetime.now(),
            token=str(self.key.decode('ascii'))
        ).save()
        print('inserted user data for username : {}'.format(username))


class fetchUserDetails():
    def __init__(self):
        pass

    def checkIfuserNameExists(self, username):
        try:
            res = users.objects.raw({"_id": str(username)}).values()
            return next(res)
        except StopIteration:
            print("User doesn't exists")
            return {}
        except Exception as e:
            return None
    
    def checkUserCredentials(self, username, password):
        try:
            res = self.checkIfuserNameExists(username)
            if res:
                key = res['token'].encode('ascii')
                fernet = Fernet(key)
                decrypted_password = fernet.decrypt(res['password'].encode('ascii')).decode('ascii')
                if decrypted_password == password:
                    return res
                else:
                    return {}
            else:
                return {}
        except StopIteration:
            return {}
        except Exception as e:
            print(str(e))
            return None

if __name__ == "__main__":
    obj = InsertUser()
    obj.insert_into_db("test", "first", "name", "21313")