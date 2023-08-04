from datetime import datetime, timedelta
from fastapi import Security, HTTPException, status, Depends
from sqlmodel import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from user.service import service_get_by_username
from dependencies import get_db
import jwt


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"])
    secret_key = "BackendDanny"

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            "exp": datetime.utcnow() + timedelta(hours=8),
            "iat": datetime.utcnow(),
            "sub": user_id,
        }

        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="expired signature"
            )

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
            )

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    def get_current_user(self, auth: HTTPAuthorizationCredentials = Security(security),db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentianls",
        )
        username = self.decode_token(auth.credentials)
        if username is None:
            raise credentials_exception
        user = service_get_by_username(db,username=username)

        if user is None:
            raise credentials_exception
        
        return user
