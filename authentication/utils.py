import jwt
from rest_framework_jwt.utils import jwt_payload_handler
from django.conf import settings

def create_token(user):
    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, settings.SECRET_KEY)
    return token.decode('unicode_escape')
