from django.shortcuts import render, redirect, reverse
from django.http import  HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator

from common.models import Goods,Types,Orders,Detail,Users
from datetime import datetime

def loadinfo(request):
    context = {}
    lists = Types.objects.filter(pid=0)
    context['typelist'] = lists
    return context

def index(request, pIndex=1):
    mod = Orders.objects
    mywhere = []
    #获取，判断并封装keyword搜索
    kw = request.GET.get("keyword", None)
    if kw:
        #查询收件人和地址中只要含有关键字的都可以
        list = mod.filter(Q(linkman__contains=kw)|Q(address__contains=kw))
        mywhere.append("keyword="+kw)
    else:
        list = mod.filter()
    #获取，判断并封装订单状态state搜索条件
    state = request.GET.get('state','')
    if state != '':
        list = list.filter(state=state)
        mywhere.append("state="+state)

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

    #遍历订单信息并追加订单姓名信息
    for od in list2:
        user = Users.objects.only('name').get(id=od.uid)
        od.name = user.name
    #封装信息加载模板输出
    context = {"orderslist":list2, 'plist':plist, 'pIndex':pIndex, 'maxpages':maxpages, 'mywhere':mywhere}
    return render(request, "myadmin/orders/index.html", context)

def detail(request, oid):
    try:
        orders = Orders.objects.get(id=oid)
        if orders != None:
            user = Users.objects.only('name').get(id=orders.uid)
            orders.name = user.name
        #加载订单详情
        dlist = Detail.objects.filter(orderid=oid)
        #遍历每个商品详情，从Goods中获取对应的图片
        for og in dlist:
            og.picname = Goods.objects.only('picname').get(id=og.goodsid).picname
        #放置模板变量，加载模板并输出
        context = {'orders':orders, 'detaillist':dlist}
        return render(request, "myadmin/orders/detail.html",context)
    except Exception as err:
        print(err)
        context = {'info':'没有找到要修改的信息'}
    return render(request, "myadmin/info.html", context)

def state(request):
    try:
        oid = request.GET.get("oid",'0')
        ob = Orders.objects.get(id=oid)
        ob.state = request.GET['state']
        ob.save()
        context = {'info':'修改成功'}
    except Exception as err:
        print(err)
        context = {'info':'修改失败'}
    return render(request, "myadmin/info.html", context)


def add(request):
    context = loadinfo(request)
    ids = request.GET.get("ids",'')
    if len(ids) == 0:
        context = {"info":"请选择要结算的商品"}
        return render(request, "web/ordersinfo.html", context)
    gidlist = ids.split(',')
    #从购物车获取要结算所有商品，并放入到orderlist中，并累计总金额
    shoplist = request.session['shoplist']
    orderslist = {}
    total = 0.0
    for gid in gidlist:
        orderslist[gid] = shoplist[gid]
        total += shoplist[gid]['price']*shoplist[gid]['m']
    #将这些信息放入到session中
    request.session['orderslist'] = orderslist
    request.session['total'] = total
    return render(request, "web/ordersadd.html", context)

def confirm(request):
    context = loadinfo(request)
    return render(request, "web/ordersconfirm.html", context)

def insert(request):
    context = loadinfo(request)
    try:
        od = Orders()
        od.uid = request.session['vipuser']['id']
        od.linkman = request.POST.get('linkman')
        od.address = request.POST.get('address')
        od.code = request.POST.get('code')
        od.phone = request.POST.get('phone')
        od.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%%S")
        od.total = request.session['total']
        od.state = 0
        od.save()

        orderslist = request.session['orderslist']
        shoplist = request.session['shoplist']
        for shop in orderslist.values():
            del shoplist[str(shop['id'])]
            ov = Detail()
            ov.orderid = od.id
            ov.goodsid = shop['id']
            ov.name = shop['goods']
            ov.price = shop['price']
            ov.num = shop['m']
            ov.save()
        del request.session['orderslist']
        del request.session['total']
        request.session['shoplist'] = shoplist
        context = {"info":"订单添加成功！，订单号：" +str(od.id)}
        return render(request, "web/ordersinfo.html", context)
    except Exception as err:
        print(err)
        context = {"info":"订单添加失败，请稍后再试"}
        return render(request, "web/ordersinfo.html", context)