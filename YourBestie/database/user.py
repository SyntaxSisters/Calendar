import hashlib
import hmac
from os import urandom
import sqlalchemy
class user:
    HASH_ITERATIONS:int = 250000
    HASH_ALGORITHM:str = "sha256"
    __username:str
    __password:bytes
    __salt:bytes
    __hashed_password:bytes

    __autheticated:bool = False

    def __init__(self, username:str, password:bytes, salt:bytes, hashed_password:bytes):
        self.__username = username
        self.__password = password
        self.__salt = salt
        self.__hashed_password = hashed_password
        if self.authenticate():
            self.load_user_data()

    def load_user_data(self):

        pass

    @staticmethod
    def create_user(username:str, password:bytes):
        salt = urandom(16)
        hashed_password = hashlib.pbkdf2_hmac(user.HASH_ALGORITHM,password,salt,user.HASH_ITERATIONS)
        created = user(username,password,salt,hashed_password)
        

    @staticmethod
    def login_user(username:str, password:bytes):
        pass

    def authenticate(self):
        result = hmac.compare_digest(self.__hashed_password,
        hashlib.pbkdf2_hmac(user.HASH_ALGORITHM,self.__password,self.__salt,user.HASH_ITERATIONS))
        self.__autheticated = result
        return result