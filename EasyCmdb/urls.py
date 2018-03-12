from django.conf.urls import url
from django.contrib import admin
from EasyCmdb import views
from django.conf.urls import include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login.html$', views.acclogin, name='acclogin'),
    url(r'^logout.html$', views.acclogout, name='acclogout'),
    url(r'^$', views.index, name='index'),
    url(r'^cmdb_web/', include('cmdb_web.urls')),
    url(r'^cmdb_api/', include('cmdb_api.urls')),
    url(r'^user_info.html$', views.user_info, name='user_info'),
]
