from pymodm import fields, MongoModel
from pymodm.connection import connect
import json
import musicPlayer.db.connect as db_con
import uuid
from cryptography.fernet import Fernet


class users(MongoModel):
    # schema
    username = fields.CharField(primary_key=True)
    firstname = fields.CharField()
    lastname = fields.CharField()
    password = fields.CharField()


class InsertUser():
    '''
    class to insert data into aocr collection
    '''
    def __init__(self):
        pass

    def insert_into_db(self,username,password, firstname,lastname):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(password.encode())
        # encrypted_password = hash(str(uuid.uuid5(uuid.NAMESPACE_OID, password)))
        data = users(
            username=str(username),
            firstname=str(firstname), 
            lastname=str(lastname),
            password=str(encrypted_password)
        ).save()
        print('inserted user data for username : {}'.format(username))


class fetchUserDetails:
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
                key = Fernet.generate_key()
                fernet = Fernet(key)

                print(type(res['password'].encode()))
                print(fernet.decrypt(res['password'].encode()))
                decrypted_password = fernet.decrypt(bytes(res['password'].encode())).decode()
                print(decrypted_password, password)
                if decrypted_password == password:
                    print("Here")
                    return True
                else:
                    print("not match")
                    return False
            else:
                return {}
        except StopIteration:
            return {}
        except Exception as e:
            print(str(e))
            print('fsdf')
            return None

if __name__ == "__main__":
    obj = InsertUser()
    obj.insert_into_db("test", "first", "name", "21313")