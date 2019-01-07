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
from django.conf.urls import  url
from myadmin.views import index,users,type,goods


urlpatterns = [
    #path('admin/', admin.site.urls),
    url(r'^$', index.index, name='myadmin_index'),
    url(r'^users$',users.index, name='myadmin_users_index'),
    url(r'^users/add$', users.add, name='myadmin_users_add'),
    url(r'^users/insert$', users.insert, name='myadmin_users_insert'),
    url(r'^users/del/(?P<uid>[0-9]+)$', users.delete, name='myadmin_users_del'),
    url(r'^users/edit/(?P<uid>[0-9]+)$', users.edit, name='myadmin_users_edit'),
    url(r'^users/update/(?P<uid>[0-9]+)$', users.update, name='myadmin_users_update'),
    url(r'^login$', index.login, name='myadmin_login'),
    url(r'^dologin$', index.dologin, name='myadmin_dologin'),
    url(r'^logout$', index.logout, name='myadmin_logout'),
    url(r'^verify$', index.verify, name='myadmin_verify'),
    url(r'^type$', type.index, name='myadmin_type_index'),
    url(r'^type/add/(?P<tid>[0-9]+)$', type.add, name='myadmin_type_add'),
    url(r'^type/insert$', type.insert, name='myadmin_type_insert'),
    url(r'^type/del/(?P<tid>[0-9]+)$', type.delete, name='myadmin_type_del'),
    url(r'^type/edit/(?P<tid>[0-9]+)$', type.edit, name='myadmin_type_edit'),
    url(r'^type/update/(?P<tid>[0-9]+)$', type.update, name='myadmin_type_update'),
    url(r'^goods$', goods.index, name='myadmin_goods_index'),
    url(r'^goods/add$', goods.add, name='myadmin_goods_add'),
    url(r'^goods/insert$', goods.insert, name='myadmin_goods_insert'),
    url(r'^goods/del/(?P<gid>[0-9]+)$', goods.delete, name='myadmin_goods_delete'),
    url(r'^goods/edit/(?P<gid>[0-9]+)$', goods.edit, name='myadmin_goods_edit'),
    url(r'^goods/update/(?P<gid>[0-9]+)$', goods.update, name='myadmin_goods_update'),


]
