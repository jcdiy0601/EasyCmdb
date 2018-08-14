from django.conf.urls import url
from cmdb_api import views

urlpatterns = [
    url(r'^v1/asset$', views.asset_api),
    url(r'^v1/softwareserver$', views.softwareserver_api),
    url(r'^v1/softwareserver_basic_info$', views.softwareserver_basic_info_api),
    # url(r'^v1/monitor$', views.monitor_api),
]
