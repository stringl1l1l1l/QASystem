import json

from django.http import HttpResponse
from drf_yasg2.openapi import SwaggerDict


def ResponseRes(code, msg, res):
    return json.dumps({
        "code": code,
        "msg": msg,
        "res": res
    },
        ensure_ascii=False
    )


def ResponseResDict(code, msg, res):
    return {
        "code": code,
        "msg": msg,
        "res": res
    }


def HttpResponseRes(code, msg, res):
    return HttpResponse(json.dumps({
        "code": code,
        "msg": msg,
        "res": res
    },
        ensure_ascii=False
    )
    )
