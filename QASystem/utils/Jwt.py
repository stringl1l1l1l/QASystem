import jwt
import datetime
from datetime import timezone
import json
key = "QASYS"

expire_hours = 2


def create_token(user_id):
    token = jwt.encode(
        {
            "id": user_id,
            "exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours=expire_hours)
        },
        key,
        algorithm="HS256"
    )
    return token


def decode_token(token):
    try:
        return jwt.decode(token, key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as ex:
        raise ex
