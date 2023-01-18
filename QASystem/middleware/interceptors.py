import traceback

import jwt
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection
from rest_framework.views import exception_handler

from QASystem.utils.Jwt import decode_token
from QASystem.utils.ResponseRes import ResponseRes
from QASystem.utils.CodeList import StatusCode

from django.shortcuts import HttpResponseRedirect, HttpResponsePermanentRedirect


# 定义中间件类，处理全局异常
class ExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        """视图函数发生异常时调用"""
        # 直接抛出 django admin 的异常
        if str(request.path).startswith('/admin/'):
            return None
        print('----process_exception----')
        print(traceback.format_exc())
        return ResponseRes(StatusCode.Internal_Server_Error.value, "系统异常，请联系管理员", {'exception': repr(exception)})


whiteList = ('/admin/', '/doc/', '/login/', '/register/')


class RequestMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if str(request.path).startswith(whiteList):
            return None
        if str(request.path) == '/':
            return HttpResponseRedirect('/doc/')
        else:
            try:
                token = request.META.get("HTTP_TOKEN")
                # print("拦截的token:\n"+token)
            except Exception as ex:
                return HttpResponseRedirect('/login/')
            else:
                if token:
                    try:
                        payload = decode_token(token)
                        redis = get_redis_connection()
                        key = "QA:" + str(payload['id'])
                        if not redis.get(key):
                            error = "用户未登录"
                            return HttpResponse(ResponseRes(StatusCode.Unauthorized.value, "认证失败", error))
                        # print("拦截的token载荷\n"+str(payload))
                    except jwt.exceptions.ExpiredSignatureError:
                        error = "token已过期"
                        return HttpResponse(ResponseRes(StatusCode.Unauthorized.value, "认证失败", error))
                    except jwt.exceptions.DecodeError:
                        error = "token认证失败"
                        return HttpResponse(ResponseRes(StatusCode.Unauthorized.value, "认证失败", error))
                    except jwt.exceptions.InvalidTokenError:
                        error = "非法的token"
                        return HttpResponse(ResponseRes(StatusCode.Unauthorized.value, "认证失败", error))
                else:
                    return HttpResponse(ResponseRes(StatusCode.Unauthorized.value, "认证失败", "token信息为空"))
