# coding:utf-8
from django.conf.urls import url
from .. import views

app_name = 'login'

urlpatterns = [
    # Resource asset url
    url(r'^login/$', views.LoginView.as_view()),
    url(r'^logout$', views.logout),

]

