from django.shortcuts import render, render_to_response
from django.template import RequestContext

# Create your views here.

def page_not_found(request):
    """
    全局404错误处理函数
    """
    response = render_to_response("404.html", {})
    return response
 
def page_error(request):
    """
    全局500错误处理函数
    """
    response = render_to_response("500.html", {})
    return response


def permission_denied(request):
    """
    全局403错误处理函数
    """
    response = render_to_response("403.html", {})
    return response