from django.shortcuts import render, redirect, reverse
from django.http import  HttpResponse

from common.models import Goods,Types

def loadinfo(request):
    context = {}
    lists = Types.objects.filter(pid=0)
    context['typelist'] = lists
    return context

def index(request):
    context = loadinfo(request)
    if 'shoplist' not in request.session:
        request.session['shoplist'] = {}
    return render(request, "web/cart.html", context)

def add(request, gid):
    #获取要放入购物车的商品信息
    goods = Goods.objects.get(id = gid)
    shop = goods.toDict()
    shop['m'] = int(request.POST.get('m', 1))
    #从session获取购物车信息，没有默认空字典
    shoplist = request.session.get('shoplist', {})
    #判断此商品是否在购物车中
    if gid in shoplist:
        #商品数量加
        shoplist[gid]['m'] += shop['m']
    else:
        #新商品添加
        shoplist[gid] = shop
    #将购物车信息放回到session
    request.session['shoplist'] = shoplist
    #重定向到浏览购物车页
    return redirect(reverse('cart_index'))

def delete(request, gid):
    shoplist = request.session['shoplist']
    del shoplist[gid]
    request.session['shoplist'] = shoplist
    return redirect(reverse('cart_index'))

def clear(request):
    context = loadinfo(request)
    request.session['shoplist'] = {}
    return render(request, "web/cart.html", context)

def change(request):
    shoplist = request.session['shoplist']
    #获取信息
    shopid = request.GET.get('gid', '0')
    num = int(request.GET['num'])
    if num < 1:
        num = 1
    shoplist[shopid]['m'] = num
    request.session['shoplist'] = shoplist
    return redirect(reverse('cart_index'))