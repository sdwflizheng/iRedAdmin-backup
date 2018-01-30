# coding:utf-8
from django.conf.urls import url
from .. import views, views_request

app_name = 'myauth'

urlpatterns = [
    # Resource asset url
    url(r'^user/$', views.UserListView.as_view(), name='user'),
    url(r'^user/add$', views.UserAddView.as_view(), name='useradd'),
    url(r'^user/edit$', views.UserEditView.as_view(), name='useredit'),
    url(r'^user/del$', views.UserDelView.as_view(), name='userdel'),
    url(r'^user/resetpasswd$', views.UserResetPasswdView.as_view(), name='resetpasswd'),

    url(r'^group/$', views.GroupListView.as_view()),
    url(r'^group/add$', views.GroupAddView.as_view()),
    url(r'^group/edit$', views.GroupEditView.as_view()),
    #url(r'^group/del$', views.GroupDelView.as_view()),
    url(r'^group/groupusersadd$', views.GroupUsersAddView.as_view()),

    url(r'^permission/$', views.PermissionListView.as_view()),
    url(r'^permissiongroup/add$', views.PermissionGroupAddView.as_view()),
    url(r'^permissionuser/add$', views.PermissionUserAddView.as_view()),

    #post
    url(r'^user/list$', views_request.user, name="userlist"),
    url(r'^group/list$', views_request.group),
    url(r'^permissiongroup/list$', views_request.permissiongroup),
    url(r'^permissionuser/list$', views_request.permissionuser),

]

