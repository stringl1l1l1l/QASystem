from enum import Enum


class StatusCode(Enum):
    OK = 200
    '''请求正常处理完毕'''

    No_Content = 204
    '''请求成功处理，没有实体的主体返回'''

    Partial_Content = 206
    '''GET范围请求已成功处理'''

    Moved_Permanently = 301
    '''永久重定向，资源已永久分配新URI'''

    Found = 302
    '''临时重定向，资源已临时分配新URI'''

    Not_Modified = 304
    '''发送的附带条件请求未满足'''

    Temporary_Redirect = 307
    '''临时重定向，POST不会变成GET'''

    Bad_Request = 400
    '''请求报文语法错误或参数错误'''

    Unauthorized = 401
    '''需要通过HTTP认证，或认证失败'''

    Forbidden = 403
    '''请求资源被拒绝'''

    Not_Found = 404
    '''未找到资源'''

    Permission_Deny = 405

    Internal_Server_Error = 500
    '''服务器故障或Web应用故障'''

    Service_Unavailable = 503
    '''服务器超负载或停机维护'''
