from django.conf.urls import url
from cmdb_api import views

urlpatterns = [
    url(r'^v1/asset$', views.asset_api),
]
