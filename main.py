import logging
import os
import secrets
from flask import Flask, request, jsonify, g
from authlib.integrations.flask_client import OAuth
from sqlalchemy import create_engine
import config

from repository import Users, Courses, Students, StudentCourses
from service import AuthService

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

oauth = OAuth(app)
google_oauth = oauth.register(
    name = "google",
    client_id = config.GOOGLE_CLIENT_ID,
    client_secret = config.GOOGLE_CLIENT_SECRET,
    api_base_url = "https://www.googleapis.com/oauth2/v1/",
    userinfo_endpoint = "https://www.googleapis.com/oauth2/v1/userinfo",
    client_kwargs = {"scope": "openid email profile"},
    server_metadata_url=config.GOOGLE_DISCOVERY_URL
)

@app.before_request
def load_user_identities():
    authorization_header = request.headers.get("Authorization")
    g.users = users
    g.courses = courses
    g.students = students
    g.student_courses = student_courses
    g.auth_service = auth_service
    g.google_oauth = google_oauth

    if authorization_header:
        token = authorization_header.replace('Bearer ', '', 1)
        g.user = auth_service.authenticate_token(token)
        if not g.user:
            return jsonify({"error": "Unauthorized"}), 401
    else:
        return jsonify({"error": "Unauthorized"}), 401

connection_string = (
    f"mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PASSWD}"
)

SQL_ENGINE = create_engine(connection_string)
users = Users(SQL_ENGINE)
courses = Courses(SQL_ENGINE)
students = Students(SQL_ENGINE)
student_courses = StudentCourses(SQL_ENGINE)
auth_service = AuthService(logging, config.JWT_SECRET, users)

from controllers import auth_bp, course_bp, student_bp  # pylint: disable=wrong-import-position, unused-import, cyclic-import

app.register_bluseprint(auth_bp, url_prefix="/auth")
app.register_bluseprint(course_bp, url_prefix="/courses")
app.register_bluseprint(student_bp, url_prefix="/students")

if __name__ == "__main__":
    app.run(debug=True, host="5000")
