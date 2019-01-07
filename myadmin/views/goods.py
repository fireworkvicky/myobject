from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from common.models import Types, Goods
from PIL import  Image
from datetime import datetime
import time,json,os
from django.db.models import Q
from django.core.paginator import Paginator


def index(request, pIndex):
    #获取商品类别信息
    tlist = Types.objects.extra(select={'_has':'concat(path, id)'}).order_by('_has')
    for ob in tlist:
        ob.pname = '. . .'*(ob.path.count(',')-1)

    #获取商品信息查询对象
    mod = Goods.objects
    mywhere = [] #定义一个用于存放搜索条件列表
    #获取、判断并封装keyword
    kw = request.GET.get("keyword", None)
    if kw:
        #查询商品名中只要含有关键字的都可以
        list = mod.filter(goods__contains=kw)
        mywhere.append("keyword="+kw)
    else:
        list = mod.filter()
    #获取、判断并封装商品类别typeid搜索条件
    typeid = request.GET.get('typeid','0')
    if typeid != '0':
        tids = Types.objects.filter(Q(id=typeid)|Q(pid=typeid)).values_list('id',flat=True)
        list = list.filter(typeid__in=tids)
        mywhere.append("typeid="+typeid)
    #获取、判断并封装商品状态state搜索条件
    state = request.GET.get('state','')
    if state != '':
        list = list.filter(state=state)
        mywhere.append("state="+state)
    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list, 5) #以5条每页创建分页对象
    maxpages = page.num_pages;
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range #页码数列表

    #遍历商品信息，并获取对应的商品类别名称，以typename名封装
    for vo in list2:
        ty = Types.objects.get(id=vo.typeid)
        vo.typename = ty.name
    #封装信息加载模板输出
    context = {'typelist':tlist, "goodslit":list2, 'plist':plist, 'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere,'typeid':int(typeid)}
    return render(request, "myadmin/goods/index.html", context)

def add(request):
    try:
        #判断并执行图片上传，缩放等处理
        myfile = request.FILES.get('pic', None)
        if not myfile:
            return HttpResponse("没有上传文件信息")
        #以时间戳命名一个新图片名称
        filename = str(time.time())+"."+myfile.name.split('.').pop()
        destination = open(os.path.join("./static/goods/", filename), 'wb+')
        for chunk in myfile.chunks():
            destination.write(chunk)
        destination.close()
        #执行图片缩放
        im = Image.open("./static/goods/"+filename)
        #缩放到375*375
        im.thumbnail((375,375))
        #把缩放后的图像用jpeg格式保存
        im.save("./static/goods/"+filename, 'jpeg')
        #缩放到220*220
        im.thumbnail((220,220))
        im.save("./static/goods/m_"+filename,'jpeg')
        #缩放到75*75
        im.thumbnail((75,75))
        #把缩放后的图像用jpeg格式保存
        im.save("./static/goods/s_"+filename, 'jpeg')
        #获取商品信息并执行添加
        ob = Goods()
        ob.goods = request.POST['goods']
        ob.typeid = request.POST['typeid']
        ob.company = request.POST['company']
        ob.price = request.POST['price']
        ob.store = request.POST['store']
        ob.content = request.POST['content']
        ob.picname = filename
        ob.state = 1
        ob.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info":"添加成功"}
    except Exception as err:
        print(err)
        context = {"info":"添加失败"}
    return render(request, "myadmin/info.html", context)

def delete(request, gid):
    try:
        #获取被删除商品的信息，先删除对应的图片
        ob = Goods.objects.get(id=gid)
        os.remove("./static/goods/"+ob.picname)
        os.remove("./static/goods/m_"+ob.picname)
        os.remove("./static/goods/s_"+ob.picname)
        #执行商品信息的删除
        ob.delete()
        context = {"info":"删除成功"}
    except Exception as err:
        print(err)
        context = {"info":"删除失败"}
    return render(request, "myadmin/info.html",context)

def edit(request, gid):
    try:
        #获取要编辑的商品信息
        ob = Goods.objects.get(id = gid)
        #获取商品的类别信息
        list = Types.objects.extra(select={'_has':'concat(path, id)'}).order_by('_has')
        #放置信息加载模板
        context = {"typelist":list, "goods":ob}
        return render(request, "myadmin/goods/edit.html", context)
    except Exception as err:
        print(err)
        context = {"info":"没有找到要修改的信息"}
    return render(request, "myadmin/info.html", context)

def update(request, gid):
    try:
        b = False
        oldpicname = request.POST['oldpicname']
        if None != request.FILES.get("pic"):
            myfile = request.FILES.get("pic", None)
            if not myfile:
                return HttpResponse("没有上传文件信息")
            #以时间戳命名一个新图片名称
            filename = str(time.time())+"."+myfile.name.split('.').pop()
            destination = open(os.path.join("./static/goods/", filename), 'wb+')
            for chunk in myfile.chunks():
                destination.write(chunk)
            destination.close()
            #执行图片缩放
            im = Image.open("./static/goods/"+filename)
            #缩放到375*375
            im.thumbnail((375,375))
            #把缩放后的图像用jpeg格式保存
            im.save("./static/goods/"+filename, 'jpeg')
            #缩放到220*220
            im.thumbnail((220,220))
            im.save("./static/goods/m_"+filename, 'jpeg')
            #缩放到75*75
            im.thumbnail((75,75))
            im.save("./static/goods/s_"+filename, 'jpeg')
            b = True
            picname = filename
        else:
            picname = oldpicname
        ob = Goods.objects.get(id=gid)
        ob.goods = request.POST['goods']
        ob.typeid = request.POST['typeid']
        ob.company = request.POST['company']
        ob.price = request.POST['price']
        ob.store = request.POST['store']
        ob.content = request.POST['content']
        ob.picname = picname
        ob.state = request.POST['state']
        ob.save()
        context = {"info":"修改成功"}
        if b:
            os.remove("./static/goods/m_"+oldpicname)
            os.remove("./static/goods/s_"+oldpicname)
            os.remove("./static/goods/"+oldpicname)
    except Exception as err:
        print(err)
        context = {"info":"修改失败"}
        if b:
            os.remove("./static/goods/m_"+picname)
            os.remove("./static/goods/s_"+picname)
            os.remove("./static/goods/"+picname)
    return render(request, "myadmin/info.html", context)

