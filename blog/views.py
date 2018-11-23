from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
from django.http import JsonResponse
from blog.Myforms import UserForm
from blog.models import UserInfo
import json
# Create your views here.


def index(request):
    '''
    首页视图
    :param request:
    :return:
    '''

    return render(request, 'index.html')


def login(request):
    '''
    登录视图
    :param request:
    :return:
    '''
    if request.method == 'POST':

        response = {'user':None,'msg':None}
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        print(user,pwd)

        user = auth.authenticate(username=user, password=pwd)
        print(222,user)
        if user:
            auth.login(request, user)  # request.user== 当前登录对象
            response["user"] = user.username
            print(111,response)
        else:
            response["msg"] = "用户名或者密码错误!"

        return HttpResponse(json.dumps({'response':response}))
        # return JsonResponse(response)   #ajax 交互数据


    return render(request, 'login.html')


def register(request):
    '''
    注册视图
    :param request:
    :return:
    '''

    if request.is_ajax():
        print(request.POST)
        form = UserForm(request.POST)

        response = {'user':None,'msg':None}
        if form.is_valid():
            response['user'] = form.cleaned_data.get('user')

            #数据入表 注意名字要和forms里面的一样
            user = form.cleaned_data.get("user")
            print("user", user)
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avatar_obj = request.FILES.get("avatar")  # 存头像文件

            extra = {}
            if avatar_obj:
                extra["avatar"] = avatar_obj

            UserInfo.objects.create_user(username=user, password=pwd, email=email, **extra)

        else:
            print(form.cleaned_data)
            print(form.errors)
            response["msg"] = form.errors

        return JsonResponse(response)

    # 没有登录，生成一个模板传给html
    form = UserForm()
    return render(request, 'register.html',{'form':form})




