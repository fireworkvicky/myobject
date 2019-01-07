from django.shortcuts import render,reverse,redirect
from django.http import  HttpResponse
from common.models import Users,Goods,Types
from django.core.paginator import Paginator

def loadinfo(request):
    context = {}
    lists = Types.objects.filter(pid=0)
    context['typelist'] = lists
    return context

def index(request):
    context = loadinfo(request)
    return render(request, "web/index.html", context)

def lists(request, pIndex=1):
    context = loadinfo(request)
    #获取商品信息查询对象
    mod = Goods.objects
    mywhere = [] #定义一个用于存放搜索条件列表
    #判断添加搜索条件
    tid = int(request.GET.get('tid', 0))
    if tid > 0:
        list = mod.filter(typeid__in=Types.objects.only('id').filter(pid=tid))
        mywhere.append("tid="+str(tid))
    else:
        list = mod.filter()
    #获取、判断并封装keyword搜索
    kw = request.GET.get("keyword", None)
    if kw:
        #查询商品名中只要含有关键字的都可以
        list = list.filter(goods__contains=kw)
        mywhere.append("keyword="+kw)
    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list, 5)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)
    plist = page.page_range

    context['goodslist'] = list2
    context['plist'] = plist
    context['pIndex'] = pIndex
    context['maxpages'] = maxpages
    context['mywhere'] = mywhere
    context['tid'] = int(tid)

    return  render(request, "web/list.html", context)

def detail(request, gid):
    context = loadinfo(request)
    ob = Goods.objects.get(id=gid)
    ob.clicknum += 1
    ob.save()
    context['goods'] = ob
    return render(request, "web/detail.html", context)

def login(request):
    return render(request, "web/login.html")

def dologin(request):
    verifycode = request.session['verifycode']
    code = request.POST['code']
    if verifycode != code:
        context = {"info":"验证码错误"}
        return render(request, "web/login.html", context)
    try:
        #根据账号获取登录者信息
        user = Users.objects.get(username=request.POST['username'])
        #判断当前用户是否是后台管理员用户
        if user.state == 0 or user.state == 1:
            #验证码
            import hashlib
            m = hashlib.md5()
            m.update(bytes(request.POST['password'], encoding="utf8"))
            if user.password == m.hexdigest():
                #此处登录成功，将当前登录信息放入到session中，并跳转页面
                request.session['vipuser'] = user.toDict()
                return redirect(reverse('index'))
            else:
                context = {"info":"登录密码错误"}
        else:
            context = {"info":"此用户为非法用户"}
    except:
        context = {"info":"登录账号错误"}
    return render(request, "web/login.html", context)

def logout(request):
    #清除登录的session信息
    del request.session['vipuser']
    #跳转登录页面
    return redirect(reverse("login"))



