import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta


class AuthHandler:
    users = {}
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = "SECRET"

    def get_password_hash(self, password):
        return self.pwd_context.hash(password, salt="rkllomdfhjfbnvgkfmavul")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=60),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            self.users.pop(token, None)
            raise HTTPException(status_code=440, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token")

    def create_session(self, key, id):
        self.users[key] = id

    def remove_session(self, key):
        self.users.pop(key, None)

    def get_session(self, key):
        return self.users.get(key, None)

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        self.decode_token(auth.credentials)
        return auth.credentials
