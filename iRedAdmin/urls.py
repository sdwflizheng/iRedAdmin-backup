"""adAdmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings

from index.views import IndexView

urlpatterns = [

    url(r'^$', IndexView.as_view()),
    url(r'^', include('login.urls.views_urls')),
    #用户、组、权限
    url(r'^myauth/', include('myauth.urls.views_urls')),
    #菜单
    url(r'^mymenu/', include('mymenu.urls.views_urls')),
    #邮箱
    url(r'^mail/', include('mail.urls.views_urls')),
    # url(r'^login/', LoginView.as_view()),
    # url(r'^logout/', logout),
] 


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
