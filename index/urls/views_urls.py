# coding:utf-8
from django.conf.urls import url
from .. import views

app_name = 'index'

urlpatterns = [
    # Resource asset url
    url(r'^$', views.IndexView.as_view()),

]

