from django.conf.urls import url
from cmdb_web.views import asset_view
from cmdb_web.views import idc_view
from cmdb_web.views import business_unit_view
from cmdb_web.views import tag_view
from cmdb_web.views import user_view
from cmdb_web.views import affiliation_view
from cmdb_web.views import ip_view
from cmdb_web.views import dashboard_view

urlpatterns = [
    # 资产
    url(r'^asset.html$', asset_view.asset_page, name='asset'),
    url(r'^asset_json.html$', asset_view.asset_json, name='asset_json'),
    url(r'^update_asset_json.html$', asset_view.update_asset_json, name='update_asset_json'),
    url(r'^delete_asset_json.html$', asset_view.delete_asset_json, name='delete_asset_json'),
    url(r'^asset_detail_(?P<asset_type>\w+)_(?P<asset_id>\d+).html$', asset_view.asset_detail, name='asset_detail'),
    url(r'^asset_detail_update_speed.html$', asset_view.asset_detail_update_speed, name='asset_detail_update_speed'),
    url(r'^asset_add.html$', asset_view.asset_add, name='asset_add'),
    url(r'^asset_add_hardware_server.html$', asset_view.asset_add_hardware_server, name='asset_add_hardware_server'),
    url(r'^asset_add_software_server.html$', asset_view.asset_add_software_server, name='asset_add_software_server'),
    url(r'^asset_add_network_device.html$', asset_view.asset_add_network_device, name='asset_add_network_device'),
    url(r'^asset_add_security_device.html$', asset_view.asset_add_security_device, name='asset_add_security_device'),
    url(r'^asset_hand_add_software_server.html$', asset_view.asset_hand_add_software_server, name='asset_hand_add_software_server'),
    url(r'^asset_edit_(?P<asset_type>\w+)_(?P<asset_id>\d+).html$', asset_view.asset_edit, name='asset_edit'),
    # IDC
    url(r'^idc.html$', idc_view.idc_page, name='idc'),
    url(r'^idc_json.html$', idc_view.idc_json, name='idc_json'),
    url(r'^update_idc_json.html$', idc_view.update_idc_json, name='update_idc_json'),
    url(r'^delete_idc_json.html$', idc_view.delete_idc_json, name='delete_idc_json'),
    url(r'^idc_add.html$', idc_view.idc_add, name='idc_add'),
    # 业务线
    url(r'^business_unit.html$', business_unit_view.business_unit_page, name='business_unit'),
    url(r'^business_unit_json.html$', business_unit_view.business_unit_json, name='business_unit_json'),
    url(r'^update_business_unit_json.html$', business_unit_view.update_business_unit_json,
        name='update_business_unit_json'),
    url(r'^delete_business_unit_json.html$', business_unit_view.delete_business_unit_json,
        name='delete_business_unit_json'),
    url(r'^business_unit_add.html$', business_unit_view.business_unit_add, name='business_unit_add'),
    # 标签管理
    url(r'^tag.html$', tag_view.tag_page, name='tag'),
    url(r'^tag_json.html$', tag_view.tag_json, name='tag_json'),
    url(r'^update_tag_json.html$', tag_view.update_tag_json, name='update_tag_json'),
    url(r'^delete_tag_json.html$', tag_view.delete_tag_json, name='delete_tag_json'),
    url(r'^tag_add.html$', tag_view.tag_add, name='tag_add'),
    # 用户管理
    url(r'^user.html$', user_view.user_page, name='user'),
    url(r'^user_json.html$', user_view.user_json, name='user_json'),
    url(r'^delete_user_json.html$', user_view.delete_user_json, name='delete_user_json'),
    url(r'^user_add.html$', user_view.user_add, name='user_add'),
    url(r'^user_edit_(?P<user_id>\d+).html$', user_view.user_edit, name='user_edit'),
    url(r'^user_change_pass_(?P<user_id>\d+).html$', user_view.user_change_pass, name='user_change_pass'),
    url(r'^user_change_permission_(?P<user_id>\d+).html$', user_view.user_change_permission, name='user_change_permission'),
    # 查询归属主机
    url(r'^show_all_affiliation.html', affiliation_view.show_all_affiliation, name='show_all_affiliation'),
    url(r'^search_affiliation.html', affiliation_view.search_affiliation, name='search_affiliation'),
    # 查询可用ip地址
    url(r'^search_ip.html', ip_view.search_ip, name='search_ip'),
    url(r'^search_ip_json.html', ip_view.search_ip_json, name='search_ip_json'),
    # chart
    url(r'^dashboard_chart1.html', dashboard_view.chart1, name='chart1'),
    url(r'^dashboard_chart2.html', dashboard_view.chart2, name='chart2'),
]
