"""myobject URL Configuration

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
#from django.contrib import admin
#from django.urls import path
from django.conf.urls import url
from web.views import index,cart,orders,vip

urlpatterns = [
    #path('admin/', admin.site.urls),
    url(r'^$', index.index, name="index"),
    url(r'^list$', index.lists, name="list"),
    url(r'^list/(?P<pIndex>[0-9]+)$', index.lists, name="list"),
    url(r'^detail/(?P<gid>[0-9]+)$', index.detail, name="detail"),

    url(r'^login$', index.login, name="login"),
    url(r'^dologin$', index.dologin, name="dologin"),
    url(r'^logout$', index.logout, name="logout"),

    url(r'^cart$', cart.index, name="cart_index"),
    url(r'^cart/add/(?P<gid>[0-9]+)$', cart.add, name="cart_add"),
    url(r'^cart/del/(?P<gid>[0-9]+)$', cart.delete, name="cart_del"),
    url(r'^cart/clear$', cart.clear, name="cart_clear"),
    url(r'^cart/change$', cart.change, name="cart_change"),
    url(r'^orders/add$', orders.add, name="orders_add"),
    url(r'^orders/confirm$', orders.confirm, name="orders_confirm"),
    url(r'^orders/insert$', orders.insert, name="orders_insert"),

    url(r'^vip/orders$', vip.viporders, name="vip_orders"),
    url(r'^vip/odstate$', vip.odstate, name="vip_odstate"),

]
