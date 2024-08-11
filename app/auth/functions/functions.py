import jwt
import os
import datetime
import bcrypt
class AuthFunctions:
    def decode_jwt(self, jwt_token: str):
        decoded_jwt = jwt.decode(str.encode(jwt_token), os.getenv('JWT_SECRET'), "HS256")

        return decoded_jwt

    def get_access_token(self, user_id):
        payload = {
            "user_id": str(user_id),
            "expires_at": str(datetime.datetime.now() + datetime.timedelta(hours=1))
        }

        access_token = jwt.encode(
            payload=payload,
            key=os.getenv('JWT_SECRET')
        )

        return access_token

    def is_password_correct(self, password, hashed_password):
        is_password_correct = bcrypt.checkpw(
            password=str.encode(password),
            hashed_password=hashed_password
        )

        return is_password_correct
