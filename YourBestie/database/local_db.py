import hmac
import secrets

from sqlalchemy import Engine, create_engine


class database:
    user_logins:dict[str,tuple[bytes,bytes]]
    user_tokens:dict[str,bytes]
    engine:Engine
    def __init__(self):
        self.user_logins = {}
        self.user_tokens = {}
        self.engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

    def authenticate_user(self, username:str, password_hash:bytes):
        found = self.user_logins.get(username, None)

        if found is None:
            return None

        matches = hmac.compare_digest(password_hash,found[1])
        if matches:
            token = secrets.token_bytes()
            self.user_tokens[username] = token
            return token
        return None

    def get_events_for_user(self,username:str, token:str):
        pass

    def create_new_user(self,username:str,salt:bytes,password_hash:bytes):
        pass

    def get_user_salt(self, username:str):
        found = self.user_logins.get(username, None)
        if found is not None:
            return found[0]
        else:
            return None