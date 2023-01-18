from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from QASystem.utils.Jwt import *
import jwt


class JWTQueryParamsAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.META.get('HTTP_TOKEN')
            print(token)
            if not token:
                raise AuthenticationFailed("登录后才能访问")
        except Exception as ex:
            raise AuthenticationFailed("登录后才能访问")
        try:
            payload = decode_token(token)
            return payload
        except jwt.exceptions.ExpiredSignatureError:
            error = "token已失效"
            raise AuthenticationFailed({"code": 401, "error": error})
        except jwt.exceptions.DecodeError:
            error = "token已认证失败"
            raise AuthenticationFailed({"code": 401, "error": error})
        except jwt.exceptions.InvalidTokenError:
            error = "非法的token"
            raise AuthenticationFailed({"code": 401, "error": error})
