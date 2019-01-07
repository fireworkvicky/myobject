from django.shortcuts import redirect, reverse
import re

class ShopMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #网站前台登录用户判断
        urllist = ['/myadmin/login','/myadmin/dologin','/myadmin/logout', '/myadmin/verify']
        path = request.path
        if re.match("^/orders", path) or re.match("^/vip", path):
            if "vipuser" not in request.session:
                return redirect(reverse("login"))
        if re.match("/myadmin", path) and (path not in urllist):
            if "adminuser" not in request.session:
                return redirect(reverse('myadmin_login'))
        response = self.get_response(request)
        return response
