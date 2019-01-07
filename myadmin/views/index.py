from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import reverse
from common.models import Users
import time, json

def index(request):
    return render(request, 'myadmin/index.html')
def login(request):
    return render(request, "myadmin/login.html")
def dologin(request):
    #校验验证码
    verifycode = request.session['verifycode']
    code = request.POST['code']
    if verifycode != code:
        context = {"info":"验证码错误"}
        return render(request,'myadmin/login.html', context)
    
    try:
        #根据账号获取登陆者信息
        user = Users.objects.get(username=request.POST['username'])
        #判断当前用户是否是后台管理员用户
        if user.state == 0:
            #验证密码
            import hashlib
            m = hashlib.md5()
            m.update(bytes(request.POST['password'], encoding="utf8"))
            if user.password == m.hexdigest():
                #此处登录成功，将当前登录信息放入到session中，并跳转页面
                request.session['adminuser'] = user.name
                return redirect(reverse('myadmin_index'))
            else:
                context = {"info":"登录密码错误"}
        else:
            context = {"info":"非管理员用户"}
    except:
        context = {"info":"登录账号错误"}
    return render(request, 'myadmin/login.html', context)
def logout(request):
    #清楚登录的session信息
    del request.session['adminuser']
    #跳转登录页面
    return redirect(reverse('myadmin_login'))
def verify(request):
    #引入随机函数模块
    import random
    from PIL import Image, ImageDraw, ImageFont
    #定义变量，用于画面背景色、宽、高
    bgcolor = (242,164,247)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height),bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point函数绘制噪点
    for i in range(0,100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0,255), 255, random.randrange(0,255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = "ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0"
    #随机选取4个值作为验证码
    rand_str = ""
    for i in range(0,4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    #font = ImageFont.truetype()
    font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    import io
    buf = io.BytesIO()
    #将突破保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的突破数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

