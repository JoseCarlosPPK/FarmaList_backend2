from ... import app
from .. import BASE_API
from flask import request, jsonify
from ...models import Usuario
from flask_jwt_extended import JWTManager, create_access_token, set_access_cookies, get_jwt, get_jwt_identity
from datetime import datetime, timezone, timedelta
import os
from dotenv import dotenv_values

PATH_ENV = os.path.join(os.path.dirname(__file__), '.env')
# Lee y guarda en un dict las variables de entorno
config = dotenv_values(PATH_ENV)

# https://flask-jwt-extended.readthedocs.io/en/stable/index.html

# Setup the Flask-JWT-Extended extension

# Here you can globally configure all the ways you want to allow JWTs to
# be sent to your web application. By default, this will be only headers.
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]

# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
app.config["JWT_COOKIE_SECURE"] = False

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

app.config["JWT_SECRET_KEY"] = config["JWT_SECRET_KEY"] 
jwt = JWTManager(app)
###############################################################################

@app.post(f"{BASE_API}/auth")
def api_auth():
   username = request.json.get("username", None)
   password = request.json.get("password", None)

   user = Usuario.query.filter_by(nombre=username).first()

   if user and user.check_password(password):
      token = create_access_token(identity=username)
      response = jsonify({"token": token})
      set_access_cookies(response, token)

      return response, 201
   
   return jsonify({"msg": "Bad username or password"}), 401

# https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens.html#implicit-refreshing-with-cookies
# Using an `after_request` callback, we refresh any token that is within X
# minutes of expiring
@app.after_request
def refresh_expiring_jwt(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response
