# coding:utf-8
from django.conf.urls import url
from .. import views, views_request

app_name = 'mymenu'

urlpatterns = [
    # Resource asset url

    url(r'^index/$', views.MenuListView.as_view()),
    url(r'^add$', views.MenuAddView.as_view()),
    url(r'^edit$', views.MenuEditView.as_view()),
    url(r'^del$', views.MenuDelView.as_view()),

    url(r'^list/$', views_request.menu),
    url(r'^groupmenuztree/$', views_request.groupmenuztree),
    url(r'^usermenuztree/$', views_request.usermenuztree),
    url(r'^menuztree/$', views_request.menuztree),

]

