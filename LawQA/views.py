
from drf_yasg2.openapi import *
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from QASystem.utils import CodeList
from QASystem.utils.Jwt import decode_token
from QASystem.utils.ResponseRes import HttpResponseRes
from StudentQA.models import QuestionRecord
from QASystem.utils import law_qa

ask_body = Schema(type=TYPE_OBJECT, properties={
    'question': Schema(description='当前用户的问题内容', type=TYPE_STRING),
})
resp = {200: Response(description='success', examples={'code': 200, 'msg': "成功", "res": ""})}
header = [Parameter(name='token', in_='header', description='用户登录后获得的token', type=TYPE_STRING, required=True)]


@swagger_auto_schema(
    method='POST',
    operation_description="法律问答",
    responses=resp,
    request_body=ask_body,
    manual_parameters=header
)
@api_view(['POST'])
def law_ask(request):
    json_body = request.data
    question = json_body['question']
    token = request.META.get('HTTP_TOKEN')
    payload = decode_token(token)
    user_id = payload['id']
    print(question)
    '''todo 调用算法api'''
    es = law_qa.ES()
    answer = es.get_law(question)
    print(question + ": "+answer)
    if not answer:
        return HttpResponseRes(CodeList.StatusCode.No_Content.value, "未找到答案，请检查您的问题", "")
    record = QuestionRecord.objects.create(user_id=user_id, question_text=question, answer_text=answer)
    return HttpResponseRes(CodeList.StatusCode.OK.value, "提问成功", {'question_id': record.id, 'answers': answer})
