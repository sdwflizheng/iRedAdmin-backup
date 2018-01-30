# coding:utf-8
from django.conf.urls import url
from .. import views, views_request

app_name = 'mail'

urlpatterns = [
    # Resource asset url

    url(r'^domain/$', views.DomainListView.as_view()),
    url(r'^add/domain$', views.DomainAddView.as_view()),
    #url(r'^edit/domain$', views.DomainEditView.as_view()),
    url(r'^del/domain$', views.DomainDelView.as_view()),
    url(r'^user/$', views.UserListView.as_view()),
    url(r'^add/user$', views.UserAddView.as_view()),
    url(r'^edit/user$', views.UserEditView.as_view()),
    url(r'^del/user$', views.UserDelView.as_view()),
    url(r'^makestatus$', views.MakeStatusView.as_view()),
    url(r'^makepassword$', views.MakePasswordView.as_view()),
    url(r'^group/$', views.GroupListView.as_view()),
    url(r'^add/group$', views.GroupAddView.as_view()),
    url(r'^edit/group$', views.GroupEditView.as_view()),
    url(r'^del/group$', views.GroupDelView.as_view()),

    url(r'^list/domain$', views_request.domain),
    url(r'^list/mailbox$', views_request.mailbox),
    url(r'^list/group$', views_request.group),
    url(r'^search/user$', views_request.searchmailbox),

]

