import traceback

import drf_yasg2
import rest_framework
from django.core.cache import cache
from django.core.exceptions import *
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from drf_yasg2.openapi import Response, Parameter, TYPE_STRING
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.serializers import Serializer
from QASystem.utils.Jwt import *
from QASystem.utils.ResponseRes import ResponseRes, ResponseResDict
from QASystem.utils.CodeList import StatusCode
import json

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import LoginUserSerializer
from django_redis import get_redis_connection

def exceptionMap(exception):
    return {"exception": repr(exception)}


resp = {200: Response(description='成功', examples={'json': ResponseResDict(200, "登录成功", {'token': ""})})}
parm = [Parameter(name='token', in_='header', description='用户登录后获得的token', type=TYPE_STRING, required=True)]


@swagger_auto_schema(
    method='POST',
    operation_description="用户登录",
    request_body=LoginUserSerializer,
    responses=resp,
)
@api_view(['POST'])
def login(request):
    try:
        # 获取body中的用户名 密码
        json_body = request.data
        username = json_body['username']
        password = json_body['password']
        # 根据用户名查询是否存在该用户
        loginUser = User.objects.get(username=username)
        if loginUser:
            # 根据用户名密码认证
            user_obj = auth.authenticate(username=username, password=password)
            if user_obj:
                # 认证成功，生成token，存入redis
                token = create_token(user_obj.id)
                redis = get_redis_connection()
                redis.set("QA:" + str(user_obj.id), user_obj.username)
                print("用户 id:" + str(user_obj.id) + " name:" + str(redis.get(user_obj.id)) + " 登录成功" + "token:" + token)
                return HttpResponse(ResponseRes(StatusCode.OK.value, "登录成功", {"user_id": user_obj.id, "token": token}))
            else:
                return HttpResponse(ResponseRes(StatusCode.Unauthorized.value, "认证失败, 请检查用户名或密码", ""))
    except ObjectDoesNotExist as odne:
        return HttpResponse(ResponseRes(StatusCode.No_Content.value, "用户不存在，请检查用户名", exceptionMap(odne)))


@swagger_auto_schema(
    method='GET',
    operation_description="用户注销",
    responses=resp,
    manual_parameters=parm
)
@api_view(['GET'])
def logout(request):
    token = request.META.get('HTTP_TOKEN')
    payload = decode_token(token)
    print("待注销用户" + str(payload))
    k = "QA:" + str(payload['id'])
    redis = get_redis_connection()
    if redis.get(k):
        redis.delete(k)
        msg = "注销成功"
        return HttpResponse(ResponseRes(StatusCode.OK.value, msg, ""))
    else:
        msg = "用户未登录"
        return HttpResponse(ResponseRes(StatusCode.Unauthorized.value, msg, ""))


@swagger_auto_schema(
    method='POST',
    operation_description="用户注册,注册后自动登录",
    responses=resp,
    request_body=LoginUserSerializer
)
@api_view(['POST'])
def register(request):
    json_body = request.data
    username = json_body['username']
    password = json_body['password']
    email = ""
    try:
        user_obj = User.objects.create_user(username, email, password)
        token = create_token(user_obj.id)
        redis = get_redis_connection()
        redis.set("QA:" + str(user_obj.id), user_obj.username)
        print("用户 id:" + str(user_obj.id) + " name:" + str(redis.get(user_obj.id)) + " 注册成功" + " token:" + token)
        return HttpResponse(ResponseRes(StatusCode.OK.value, "注册成功", {"user_id": user_obj.id, "token": token}))
    except IntegrityError as err:
        return HttpResponse(ResponseRes(StatusCode.Bad_Request.value, "用户名已存在", ""))
