"""
全局拦截指定请求方式及请求中间件
"""
import re

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from application import settings


class RequestInterceptMiddleware(MiddlewareMixin):
    """
    用于全局拦截指定请求方式及请求中间件
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.intercept_white_list = getattr(settings, 'INTERCEPT_WHITE_LIST',
                                            ['/api/login/','/api-auth/login/', '/api-auth/logout/', '/token/', 'token/refresh/'])
        self.intercept_method = getattr(settings, 'INTERCEPT_METHOD', ['POST', 'DELETE', 'PUT'])
        self.intercept_msg = getattr(settings, 'INTERCEPT_MSG', '演示模式，不允许操作!')

    def check_path(self, path):
        for white_regex in self.intercept_white_list:
            if re.search(white_regex, path):
                return True
        return False

    def process_request(self, request):
        if request.method.upper() in self.intercept_method and not self.check_path(request.path):
            pass
            std_data = {
                "code": 400,
                "data": {},
                "msg": self.intercept_msg,
            }
            return JsonResponse(data=std_data)
