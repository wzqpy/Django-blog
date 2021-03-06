"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from BBS import settings
from django.views.static import serve
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('artlike/', views.artlike),
    path('comment/', views.comment),
    path('backend/', views.backend),
    path('backend_add/', views.backend_add_article),

    # media配置:
    re_path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),

    # 个人站点的跳转
    # ^匹配字符串的开头 $匹配字符串的末尾。  小写w 匹配数字字母下划线， + （重复 >=1 次） {a+b,（abbb)}）,*匹配0个或多个的表达式。
    re_path('^(?P<username>\w+)/(?P<condition>tag|category|archive)/(?P<param>.*)/$', views.home_site),
    # home_site(reqeust,username="yuan",condition="tag",param="python")

    # 个人站点url
    re_path('^(?P<username>\w+)/$', views.home_site),  # home_site(reqeust,username="yuan")
    # 文章详情的跳转  \d	匹配任意数字，等价于 [0-9].    + （重复 >=1 次）
    re_path('^(?P<username>\w+)/articles/(?P<article_id>\d+)/$', views.article)

]
