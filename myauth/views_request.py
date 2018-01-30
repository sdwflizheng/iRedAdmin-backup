#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from myauth.decorators import superuser_required

import simplejson as json
from .models import User, Group
from mymenu.models import Menu
from mylib.utils import iso8601_to_time

#直接使用检查是否管理员
#from django.contrib.auth.decorators import user_passes_test
#@user_passes_test(lambda u: u.is_superuser)

@login_required
@superuser_required
def user(request):
    """        
    所有用户的数据,用于bootstrap-table
    """

    #得到偏移量
    pageIndex= int(request.GET.get('offset',0))
    #得到查询个数
    pageSize = int(request.GET.get('limit',10))
    #增加状态后解决清空，搜索的limit为搜索的值
    if pageSize < 10:
        pageSize = 10

    #得到排序字段
    sort = request.GET.get('sort','id')
    #得到排序规则
    order_by_type = request.GET.get('order','asc')
    
    if order_by_type == 'asc':
        order_by = sort
    else:
        order_by = '-' + sort

    data = {}
    data['rows'] = []

    #获取所有记录
    data['total'] = User.objects.all().count()
    #判断起始查询如果是ALL,表示显示全部
    if pageSize != -1:
        ormdata = User.objects.all().order_by(order_by)[pageIndex:pageIndex + pageSize]
    else:
        ormdata = User.objects.all().order_by(order_by)
 

    for i in ormdata:
        
        #1 超级管理员 0 普通用户
        if i.is_superuser:
            is_admin = '是'
        else:
            is_admin = '否' 
            
        # 1激活 0 锁定
        if i.is_active:
            is_active = '激活'
        else:
            is_active = '锁定'

        last_login = i.last_login
        if last_login != None:
            last_login = iso8601_to_time(last_login)

        data['rows'].append({"id":i.id,
                         "name":i.name,
                         "nickname":i.nickname,
                         "email":i.email,
                         "last_login":last_login,
                         "is_superuser":is_admin,
                         "mobile":i.mobile,
                         "is_active":is_active
                         })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)

@login_required
@superuser_required
def group(request):
    """        
    所有用户的数据,用于bootstrap-table
    """

    #得到偏移量
    pageIndex= int(request.GET.get('offset',0))
    #得到查询个数
    pageSize = int(request.GET.get('limit',10))
    #增加状态后解决清空，搜索的limit为搜索的值
    if pageSize < 10:
        pageSize = 10

    #得到排序字段
    sort = request.GET.get('sort','id')
    #得到排序规则
    order_by_type = request.GET.get('order','asc')
    
    if order_by_type == 'asc':
        order_by = sort
    else:
        order_by = '-' + sort

    data = {}
    data['rows'] = []

    #获取所有记录
    data['total'] = Group.objects.all().count()
    #判断起始查询如果是ALL,表示显示全部
    if pageSize != -1:
        ormdata = Group.objects.all().order_by(order_by)[pageIndex:pageIndex + pageSize]
    else:
        ormdata = Group.objects.all().order_by(order_by)
 
    #组ID为key，用户登录名和用户姓名为value
    group_users = {}
    #获取所有用户数据
    user_ormdata = User.objects.filter(is_active=1).filter(is_superuser=0)
    for u in user_ormdata:
        groups = []
        #得到该用户所在的组
        for g in u.groups.all():
            if g.id not in group_users:
                group_users[g.id] = []
            
            group_users[g.id].append("%s(%s)" % (u.name,u.nickname))
        #groups.append(i.id for i in u.groups.all()])

    for i in ormdata:
        
        if i.id in group_users:
            data['rows'].append({"id":i.id,
                                 "name":i.name,
                                 "users":",".join(group_users[i.id])
                                })
        else:
            data['rows'].append({"id":i.id,
                                 "name":i.name,
                                 "users":""
                                })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)

@login_required
@superuser_required
def permissiongroup(request):
    """        
    所有用户的数据,用于bootstrap-table
    """

    #得到偏移量
    pageIndex= int(request.GET.get('offset',0))
    #得到查询个数
    pageSize = int(request.GET.get('limit',10))
    #增加状态后解决清空，搜索的limit为搜索的值
    if pageSize < 10:
        pageSize = 10

    #得到排序字段
    sort = request.GET.get('sort','id')
    #得到排序规则
    order_by_type = request.GET.get('order','asc')
    
    if order_by_type == 'asc':
        order_by = sort
    else:
        order_by = '-' + sort

    data = {}
    data['rows'] = []
    data['total'] = 0
    #获取所有记录
    data['total'] = Group.objects.all().count()
    #判断起始查询如果是ALL,表示显示全部
    if pageSize != -1:
        ormdata = Group.objects.all().order_by(order_by)[pageIndex:pageIndex + pageSize]
    else:
        ormdata = Group.objects.all().order_by(order_by)
 
    for i in ormdata:
        #得到组对应的所有菜单权限,返回一个list
        #menu_ids = i.get_permissions()
        menu_names = i.get_permissions_name()
        data['rows'].append({"id":i.id,
                            "name":i.name,
                            "menus":menu_names
                        })
        
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)

@login_required
@superuser_required
def permissionuser(request):
    """        
    所有用户的数据,用于bootstrap-table
    """

    #得到偏移量
    pageIndex= int(request.GET.get('offset',0))
    #得到查询个数
    pageSize = int(request.GET.get('limit',10))
    #增加状态后解决清空，搜索的limit为搜索的值
    if pageSize < 10:
        pageSize = 10

    #得到排序字段
    sort = request.GET.get('sort','id')
    #得到排序规则
    order_by_type = request.GET.get('order','asc')
    
    if order_by_type == 'asc':
        order_by = sort
    else:
        order_by = '-' + sort

    data = {}
    data['rows'] = []

    #获取所有记录
    data['total'] = User.objects.filter(is_active=1).filter(is_superuser=0).count()
    #判断起始查询如果是ALL,表示显示全部
    if pageSize != -1:
        ormdata = User.objects.filter(is_active=1).filter(is_superuser=0).order_by(order_by)[pageIndex:pageIndex + pageSize]
    else:
        ormdata = User.objects.filter(is_active=1).filter(is_superuser=0).order_by(order_by)
 
    for i in ormdata:
        #得到组对应的所有菜单权限,返回一个list
        #menu_ids = i.get_permissions()
        menu_names = i.get_permissions_name(i)
        data['rows'].append({"id":i.id,
                            "name":i.name,
                            "menus":menu_names
                        })

    return JsonResponse(data)