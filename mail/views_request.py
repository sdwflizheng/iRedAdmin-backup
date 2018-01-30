#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.conf import settings
import simplejson as json

from .models import Domain,MailBox,UserQuota,Alias,Forwardings
from mylib.utils import filesizeformat

@login_required
def domain(request):
    """        
    所有的数据,用于bootstrap-table
    """

    #得到偏移量
    pageIndex= int(request.GET.get('offset',0))
    #得到查询个数
    pageSize = int(request.GET.get('limit',10))
    #增加状态后解决清空，搜索的limit为搜索的值
    if pageSize < 10:
        pageSize = 10

    #得到搜索字段
    search_key = request.GET.get('search')
    #得到搜索类型，html中自定义
    search_type = request.GET.get('search_type')

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

    if search_key=="" or search_key == None:
        #获取所有记录
        data['total'] = Domain.objects.all().count()
        #判断起始查询如果是ALL,表示显示全部
        if pageSize != -1:
            ormdata = Domain.objects.all().order_by(order_by)[pageIndex:pageIndex + pageSize]
        else:
            ormdata = Domain.objects.all().order_by(order_by)
    else:
        #拼接搜索
        key = "domain like '%%" +search_key + "%%'"

        #获取所有记录        
        data['total'] = Domain.objects.filter(Q(domain__contains=search_key)).count()
        #判断起始查询如果是ALL,表示显示全部
        if pageSize != -1:
            ormdata = Domain.objects.filter(Q(domain__contains=search_key)).order_by(order_by)[pageIndex:pageSize]
        else:
            ormdata = Domain.objects.filter(Q(domain__contains=search_key)).order_by(order_by)   

    for i in ormdata:
        
        users = MailBox.objects.filter(domain=i.domain).count()
        
        data['rows'].append({"domain": i.domain,
                             "active": i.active,
                             "users":users
                             })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)

@login_required
def mailbox(request):
    """        
    所有的数据,用于bootstrap-table
    """

    #得到偏移量
    pageIndex= int(request.GET.get('offset',0))
    #得到查询个数
    pageSize = int(request.GET.get('limit',10))
    #增加状态后解决清空，搜索的limit为搜索的值
    if pageSize < 10:
        pageSize = 10

    #得到搜索字段
    search_key = request.GET.get('search')
    #得到搜索类型，html中自定义
    search_type = request.GET.get('search_type')

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

    if search_key=="" or search_key == None:
        #获取所有记录
        data['total'] = MailBox.objects.all().count()
        #判断起始查询如果是ALL,表示显示全部
        if pageSize != -1:
            ormdata = MailBox.objects.all().order_by(order_by)[pageIndex:pageIndex + pageSize]
        else:
            ormdata = MailBox.objects.all().order_by(order_by)
    else:
        #拼接搜索
        key = "username like '%%" + search_key + "%%' or name like '%%" + search_key + "%%'"

        #获取所有记录        
        data['total'] = MailBox.objects.filter(Q(username__contains=search_key)|Q(name__contains=search_key)).count()
        #判断起始查询如果是ALL,表示显示全部
        if pageSize != -1:
            ormdata = MailBox.objects.filter(Q(username__contains=search_key)|Q(name__contains=search_key)).order_by(order_by)[pageIndex:pageSize]
        else:
            ormdata = MailBox.objects.filter(Q(username__contains=search_key)|Q(name__contains=search_key)).order_by(order_by)   

    for i in ormdata:
        
        if i.quota==0:
            quota='无限制'
        else:
            quota = filesizeformat(i.quota,baseMB=True)

        try:
            mailbox_useinfo = UserQuota.objects.filter(username=i.username).values('bytes','messages')[0]
            usequota = mailbox_useinfo['bytes']
            messages = mailbox_useinfo['messages']

            usequota = filesizeformat(usequota)
        except:
            #未使用邮箱用户
            usequota = 0
            messages = 0

        data['rows'].append({"username": i.username,
                             "name": i.name,
                             "domain": i.domain,
                             "quota": quota,
                             "active": i.active,
                             "usequota":usequota,
                             "messages":messages
                             })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)



@login_required
def group(request):
    """        
    所有的数据,用于bootstrap-table
    """

    #得到偏移量
    pageIndex= int(request.GET.get('offset',0))
    #得到查询个数
    pageSize = int(request.GET.get('limit',10))
    #增加状态后解决清空，搜索的limit为搜索的值
    if pageSize < 10:
        pageSize = 10

    #得到搜索字段
    search_key = request.GET.get('search')
    #得到搜索类型，html中自定义
    search_type = request.GET.get('search_type')

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

    if search_key=="" or search_key == None:
        #获取所有记录
        data['total'] = Alias.objects.all().count()
        #判断起始查询如果是ALL,表示显示全部
        if pageSize != -1:
            ormdata = Alias.objects.all().order_by(order_by)[pageIndex:pageIndex + pageSize]
        else:
            ormdata = Alias.objects.all().order_by(order_by)
    else:
        #拼接搜索
        key = "address like '%%" + search_key + "%%' or name like '%%" + search_key + "%%'"

        #获取所有记录        
        data['total'] = Alias.objects.filter(Q(address__contains=search_key)|Q(name__contains=search_key)).count()
        #判断起始查询如果是ALL,表示显示全部
        if pageSize != -1:
            ormdata = Alias.objects.filter(Q(address__contains=search_key)|Q(name__contains=search_key)).order_by(order_by)[pageIndex:pageSize]
        else:
            ormdata = Alias.objects.filter(Q(address__contains=search_key)|Q(name__contains=search_key)).order_by(order_by)   

    for i in ormdata:
        
        users = Forwardings.objects.filter(address=i.address,domain=i.domain).values('forwarding')[0]

        data['rows'].append({"address": i.address,
                             "name": i.name,
                             "domain": i.domain,
                             "active": i.active,
                             "users":users['forwarding'].replace(',','</br>')
                             })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)

@login_required
def searchmailbox(request):
    """        
    所有的数据,用于bootstrap-table
    """

    #得到排序字段
    address = request.GET.get('q')

    ormdata = MailBox.objects.filter(Q(username__contains=address))
    data = []
    for i in ormdata:

        data.append({"id": i.username,
                             "text": i.username
                             })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data,safe=False)