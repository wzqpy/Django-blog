from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from django.http import JsonResponse
from blog.Myforms import UserForm
from blog.models import UserInfo
import json
from blog import models
from django.db.models import Count


# Create your views here.


def index(request):
    '''
    首页视图 ,文章查询，排序，时间倒序
    :param request:
    :return:
    '''

    article_list = models.Article.objects.all().order_by('-create_time')

    return render(request, "index.html", {"article_list": article_list})


def login(request):
    '''
    登录视图
    :param request:
    :return:
    '''
    if request.method == 'POST':

        response = {'user': None, 'msg': None}
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')

        print(user, pwd)

        user = auth.authenticate(username=user, password=pwd)
        print(222, user)
        if user:
            auth.login(request, user)  # request.user== 当前登录对象
            response["user"] = user.username
            print(111, response)
        else:
            response["msg"] = "用户名或者密码错误!"

        return HttpResponse(json.dumps({'response': response}))
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

        response = {'user': None, 'msg': None}
        if form.is_valid():
            response['user'] = form.cleaned_data.get('user')

            # 数据入表 注意名字要和forms里面的一样
            user = form.cleaned_data.get("user")
            print("user", user)
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            telephone = form.cleaned_data.get("telephone")
            avatar_obj = request.FILES.get("avatar")  # 存头像文件

            extra = {}
            if avatar_obj:
                extra["avatar"] = avatar_obj

            UserInfo.objects.create_user(username=user, password=pwd, email=email, telephone=telephone, **extra)

        else:
            print(form.cleaned_data)
            print(form.errors)
            response["msg"] = form.errors

        return JsonResponse(response)

    # 没有登录，生成一个UserForm模板传给html
    form = UserForm()
    return render(request, 'register.html', {'form': form})


def logout(request):
    """
    注销视图 自带的auth组件判断
    :param request:
    :return:
    """
    auth.logout(request)  # request.session.flush()--冲洗
    # logout不需要配置视图
    return redirect("/login/")


def home_site(requset, username, **kwargs):
    '''
    个人博客站点（基于ORM查询数据）
    :param requset:
    :return:
    '''
    print(requset, username)
    user = UserInfo.objects.filter(username=username).first()
    # 判断用户是否存在!,返回错误页面，或者渲染个人站点
    if not user:
        return render(requset, "errorPage.html.html")

    # user 与blog是外键关联
    blog = user.blog

    # 文章分类 对应筛选出2个值
    cate_list = models.Category.objects.filter(blog=blog).values("pk").annotate(c=Count("article__title")).values_list(
        "title", "c")
    #标签分类 对应筛选出2个值
    tag_list = models.Tag.objects.filter(blog=blog).values("pk").annotate(c=Count("article")).values_list("title", "c")
    #时间分类 对应筛选出2个值
    date_list = models.Article.objects.filter(user=user).extra(
        select={"y_m_date": "date_format(create_time,'%%Y/%%m')"}).values("y_m_date").annotate(
        c=Count("nid")).values_list("y_m_date", "c")

    # 当前用户或者当前站点对应所有文章,排序，时间最新在最前面
    # airticle 与user表示外键关联
    article_list = models.Article.objects.filter(user=user).order_by('-create_time')

    # kwargs是个字典 ，condition和param 有名分组 从url 捕获
    if kwargs:
        condition = kwargs.get("condition")
        param = kwargs.get("param")

        # 分类文章查询 连表查询
        if condition == "category":  # 文章分类
            article_list = article_list.filter(category__title=param)
        elif condition == "tag":  # 标签分类
            article_list = article_list.filter(tags__title=param)
        else:
            year, month = param.split("/")  # 分隔    时间分类
            print(year,month)
            #  需要在setting里面设置  时区改为   USE_TZ = False
            article_list = article_list.filter(create_time__year=year, create_time__month=month)
            print(article_list)

    # 传入表
    return render(requset, "blog_site.html",
                  {"username": username, "blog": blog, "article_list": article_list, 'user': user,
                   "cate_list": cate_list, "date_list": date_list, "tag_list": tag_list})
