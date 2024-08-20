import re
from datetime import timezone, datetime
import jwt

class AuthService:
    def __init__(self, logger, jwt_secret, users):
        self.logger = logger
        self.secret = jwt_secret
        self.users = users

    def issue_token(self, profile):
        email = profile['email']
        name = profile['name']

        # Regex patterns to match email formats
        teacher_pattern = r"^[a-zA-Z0-9]@[^@]+\.mail\.mcu\.edu\.tw$"

        # Determine the role based on email pattern
        if re.match(teacher_pattern, email):
            role = 'teacher'
        else:
            self.logger.error(f"Invalid email format: {email}")
            raise ValueError("Invalid email format")

        # Check if the user exists or needs to be registered
        user = self.users.query_user(email)
        if not user:
            self.users.add_user(name, email, role)
            user = self.users.query_user(email)

        now = int(datetime.now(tz=timezone.utc).timestamp())
        payload = {
            "iat": now,
            "exp": now + 3600,
            "uid": user['id'],
            "email": user['email'],
            "role": user['role'],
        }

        token = jwt.encode(payload, self.secret, algorithm="HS256")
        print(token)
        return token

    def authenticate_token(self, payload):
        if not payload:
            raise ValueError("Token is empty")
        try:
            payload = jwt.decode(payload, self.secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError as e:
            self.logger.error(f"Token has expired: {e}")
            return None
        except jwt.InvalidTokenError as e:
            self.logger.error(f"Invalid token: {e}")
            return None

        user = self.users.query_user(payload['email'])
        if not user:
            self.logger.error(f"User not found: {payload['email']}")
            return None
        return user
