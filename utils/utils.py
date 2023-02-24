import jwt
from rest_framework.request import Request
from .exceptions import JWTnotFound


def jwt_decode(request: Request, secret: str):
    encoded_jwt = request.headers.get('Authorization').split('Bearer ')[1]
    decoded_jwt = jwt.decode(encoded_jwt, secret, algorithms=["HS256"])
    return decoded_jwt
