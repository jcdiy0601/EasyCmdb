from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class UserProfileManager(BaseUserManager):
    """用户表"""
    def create_user(self, email, name, phone, password=None):
        if not email:
            raise ValueError('用户必须有一个email地址')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self.db)
        return user

    def create_superuser(self, email, name, phone, password):
        user = self.create_user(email, name, phone, password)
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='邮箱', unique=True)
    name = models.CharField(verbose_name='姓名', max_length=64)
    phone = models.CharField(verbose_name='电话', max_length=11, unique=True)
    is_active = models.BooleanField(verbose_name='是否可登录', default=True)
    is_admin = models.BooleanField(verbose_name='是否为管理员', default=False)

    class Meta:
        verbose_name_plural = '用户表'
        permissions = (
            ('can_show_user', '可以访问用户管理页面'),
            ('can_show_add_user', '可以访问添加用户页面'),
            ('can_add_user', '可以添加用户'),
            ('can_delete_user', '可以删除用户'),
            ('can_show_edit_user', '可以访问用户编辑页面'),
            ('can_edit_user', '可以编辑用户'),
            ('can_show_change_pass_user', '可以访问重置密码页面'),
            ('can_change_pass_user', '可以重置密码'),
            ('can_show_change_permission_user', '可以访问修改用户权限页面'),
            ('can_change_permission_user', '可以修改用户权限'),
        )

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        # __unicode__ on Python 2
        return self.email

    # def has_perm(self, perm, obj=None):
    #     # Does the user have a specific permission?
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     # Does the user have permissions to view the app `app_label`?
    #     # Simplest possible answer: Yes, always
    #     return True

    @property
    def is_staff(self):
        # Is the user a member of staff?
        # Simplest possible answer: All admins are staff
        return self.is_admin


class BusinessUnit(models.Model):
    """业务线表"""
    name = models.CharField(verbose_name='业务线名称', max_length=64, unique=True)
    contact = models.ForeignKey(verbose_name='所属业务联系人', to='UserProfile', related_name='c')
    manager = models.ForeignKey(verbose_name='所属系统管理员', to='UserProfile', related_name='m')

    class Meta:
        verbose_name_plural = '业务线表'
        permissions = (
            ('can_show_business_unit', '可以访问业务线管理页面'),
            ('can_update_business_unit', '可以更新业务线'),
            ('can_delete_business_unit', '可以删除业务线'),
            ('can_show_add_business_unit', '可以访问添加业务线页面'),
            ('can_add_business_unit', '可以添加业务线'),
        )

    def __str__(self):
        return self.name


class IDC(models.Model):
    """IDC表"""
    name = models.CharField(verbose_name='机房', max_length=64)
    floor = models.IntegerField(verbose_name='楼层', default=1)

    class Meta:
        unique_together = (
            ('name', 'floor'),
        )
        verbose_name_plural = 'IDC表'
        permissions = (
            ('can_show_idc', '可以访问IDC管理页面'),
            ('can_update_idc', '可以更新IDC'),
            ('can_delete_idc', '可以删除IDC'),
            ('can_show_add_idc', '可以访问添加IDC页面'),
            ('can_add_idc', '可以添加IDC'),
        )

    def __str__(self):
        return self.name


class Tag(models.Model):
    """标签表"""
    name = models.CharField(verbose_name='标签名称', max_length=64, unique=True)
    creator = models.ForeignKey(verbose_name='所属创建人', to='UserProfile')
    create_date = models.DateField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = '标签表'
        permissions = (
            ('can_show_tag', '可以访问标签管理页面'),
            ('can_update_tag', '可以更新标签'),
            ('can_delete_tag', '可以删除标签'),
            ('can_show_add_tag', '可以访问添加标签页面'),
            ('can_add_tag', '可以添加标签'),
        )

    def __str__(self):
        return self.name


class Asset(models.Model):
    """资产表"""
    asset_type_choices = (
        ('hardwareserver', '硬件服务器'),
        ('softwareserver', '软件服务器'),
        ('networkdevice', '网络设备'),
        ('securitydevice', '安全设备'),
    )
    asset_type = models.CharField(verbose_name='资产类型', choices=asset_type_choices, max_length=64, default='softwareserver')
    asset_status_choices = (
        ('online', '在线'),
        ('offline', '离线'),
        ('putaway', '上架'),
        ('removeoff', '下架')
    )
    asset_status = models.CharField(verbose_name='资产状态', choices=asset_status_choices, max_length=64, default='online')
    cabinet_num = models.CharField(verbose_name='机柜号', max_length=32, null=True, blank=True)
    cabinet_order = models.CharField(verbose_name='机柜中序号', max_length=32, null=True, blank=True)
    idc = models.ForeignKey(verbose_name='所属IDC机房', to='IDC', null=True, blank=True)
    business_unit = models.ForeignKey(verbose_name='所属业务线', to='BusinessUnit', null=True, blank=True)
    tag = models.ManyToManyField(verbose_name='所属标签', to='Tag', blank=True)
    purchasing_company = models.CharField(verbose_name='采购公司', max_length=64, null=True, blank=True)
    auto = models.BooleanField(verbose_name='是否为自动采集', default=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    latest_date = models.DateField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name_plural = '资产表'
        permissions = (
            ('can_show_asset', '可以访问资产管理页面'),
            ('can_update_asset', '可以更新资产'),
            ('can_delete_asset', '可以删除资产'),
            ('can_show_asset_detail', '可以访问资产详情页面'),
            ('can_change_speed_asset_detail', '可以编辑硬盘转速'),
            ('can_show_add_asset', '可以访问添加资产页面'),
            ('can_show_add_hardware_server', '可以访问添加硬件服务器资产页面'),
            ('can_show_add_software_server', '可以访问添加软件件服务器资产页面'),
            ('can_show_add_network_device', '可以访问添加网络设备资产页面'),
            ('can_show_add_security_device', '可以访问添加安全设备资产页面'),
            ('can_show_hand_add_software_server', '可以访问添加手工录入软件服务器资产页面'),
            ('can_add_hardware_server', '可以添加硬件服务器资产'),
            ('can_add_software_server', '可以添加软件服务器资产'),
            ('can_add_network_device', '可以添加网络设备资产'),
            ('can_add_security_device', '可以添加安全设备资产'),
            ('can_hand_add_software_server', '可以添加手工录入软件服务器资产'),
            ('can_show_edit_asset', '可以访问资产编辑页面'),
            ('can_edit_asset', '可以编辑资产')
        )

    def __str__(self):
        return str(self.id)


class HardwareServer(models.Model):
    """硬件服务器表"""
    asset = models.OneToOneField(verbose_name='所属资产', to='Asset', on_delete=models.CASCADE)
    hostname = models.CharField(verbose_name='主机名', max_length=128, null=True, blank=True)
    sn = models.CharField(verbose_name='SN号', max_length=64, unique=True)
    manager_ip = models.GenericIPAddressField(verbose_name='管理IP', unique=True)
    fast_server_number = models.CharField(verbose_name='快速服务号', max_length=64, null=True, blank=True)
    manufacturer_choices = (
        ('dell', '戴尔'),
    )
    manufacturer = models.CharField(verbose_name='厂商', max_length=64, choices=manufacturer_choices, default='dell')
    model = models.CharField(verbose_name='型号', max_length=64, null=True, blank=True)
    os_version = models.CharField(verbose_name='系统版本', max_length=64, null=True, blank=True)
    memo = models.CharField(verbose_name='备注', max_length=128, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    latest_date = models.DateField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name_plural = '硬件服务器表'

    def __str__(self):
        return self.hostname


class SoftwareServer(models.Model):
    """软件服务器表"""
    asset = models.OneToOneField(verbose_name='所属资产', to='Asset', on_delete=models.CASCADE)
    hostname = models.CharField(verbose_name='主机名', max_length=128, unique=True)
    os_version = models.CharField(verbose_name='系统版本', max_length=64, null=True, blank=True)
    memo = models.CharField(verbose_name='备注', max_length=128, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    latest_date = models.DateField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name_plural = '软件服务器表'

    def __str__(self):
        return self.hostname


class NetworkDevice(models.Model):
    """网络设备表"""
    asset = models.OneToOneField(verbose_name='所属资产', to='Asset', on_delete=models.CASCADE)
    device_name = models.CharField(verbose_name='设备名称', max_length=64, null=True, blank=True)
    device_type_choices = (
        ('switch', '交换机'),
        ('firewall', '防火墙'),
    )
    device_type = models.CharField(verbose_name='设备类型', max_length=64, choices=device_type_choices, default='switch')
    sn = models.CharField(verbose_name='SN号', max_length=64, unique=True)
    manager_ip = models.GenericIPAddressField(verbose_name='管理IP', unique=True)
    manufacturer_choices = (
        ('h3c', '华三'),
        ('juniper', '瞻博'),
    )
    manufacturer = models.CharField(verbose_name='厂商', max_length=64, choices=manufacturer_choices, default='h3c')
    model = models.CharField(verbose_name='型号', max_length=64, null=True, blank=True)
    port_number = models.IntegerField(verbose_name='接口数', null=True, blank=True)
    basic_info = models.TextField(verbose_name='基本信息', null=True, blank=True)
    memo = models.CharField(verbose_name='备注', max_length=128, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    latest_date = models.DateField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name_plural = '网络设备表'

    def __str__(self):
        return self.device_name


class SecurityDevice(models.Model):
    """安全设备表"""
    asset = models.OneToOneField(verbose_name='所属资产', to='Asset', on_delete=models.CASCADE)
    device_name = models.CharField(verbose_name='设备名称', max_length=64, null=True, blank=True)
    device_type_choices = (
        ('waf', 'WAF'),
        ('ads', 'ADS'),
        ('ips', 'IPS'),
    )
    device_type = models.CharField(verbose_name='设备类型', max_length=64, choices=device_type_choices, default='waf')
    sn = models.CharField(verbose_name='SN号', max_length=64, unique=True)
    manager_ip = models.GenericIPAddressField(verbose_name='管理IP', unique=True)
    manufacturer_choices = (
        ('nsfocus', '绿盟'),
    )
    manufacturer = models.CharField(verbose_name='厂商', max_length=64, choices=manufacturer_choices, default='h3c')
    model = models.CharField(verbose_name='型号', max_length=64, null=True, blank=True)
    port_number = models.IntegerField(verbose_name='接口数', null=True, blank=True)
    memo = models.CharField(verbose_name='备注', max_length=128, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    latest_date = models.DateField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name_plural = '安全设备表'

    def __str__(self):
        return self.device_name


class CPU(models.Model):
    """CPU组件表"""
    asset = models.OneToOneField(verbose_name='所属资产', to='Asset', on_delete=models.CASCADE)
    cpu_model = models.CharField(verbose_name='CPU型号', max_length=128, null=True, blank=True)
    cpu_physical_count = models.IntegerField(verbose_name='CPU物理个数', null=True, blank=True)
    cpu_count = models.IntegerField(verbose_name='CPU逻辑个数', null=True, blank=True)
    memo = models.CharField(verbose_name='备注', max_length=128, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    latest_date = models.DateField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name_plural = "CPU组件表"

    def __str__(self):
        return self.cpu_model


class RAM(models.Model):
    """内存组件表"""
    asset = models.ForeignKey(verbose_name='所属资产', to='Asset', on_delete=models.CASCADE)
    slot = models.CharField(verbose_name='插槽', max_length=64, null=True, blank=True)
    sn = models.CharField(verbose_name='SN号', max_length=128, null=True, blank=True)
    manufacturer = models.CharField(verbose_name='厂商', max_length=64, null=True, blank=True)
    model = models.CharField(verbose_name='型号', max_length=128, null=True, blank=True)
    speed = models.IntegerField(verbose_name='频率', null=True, blank=True)
    total_capacity = models.IntegerField(verbose_name='内存总大小(MB)', blank=True, null=True)
    capacity = models.IntegerField(verbose_name='内存大小(MB)', null=True, blank=True)
    memo = models.CharField(verbose_name='备注', max_length=128, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    latest_date = models.DateField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name_plural = "内存组件表"

    def __str__(self):
        if self.slot:
            return '%s:%s:%s' % (self.asset_id, self.slot, self.capacity)
        else:
            return '%s:%s' % (self.asset_id, self.total_capacity)


class Disk(models.Model):
    """硬盘组件表"""

    asset = models.ForeignKey(verbose_name='所属资产', to='Asset', on_delete=models.CASCADE)
    slot = models.CharField(verbose_name='插槽', max_length=64, null=True, blank=True)
    sn = models.CharField(verbose_name='SN号', max_length=128, null=True, blank=True)
    manufacturer = models.CharField(verbose_name='厂商', max_length=64, null=True, blank=True)
    model = models.CharField(verbose_name='型号', max_length=128, null=True, blank=True)
    speed = models.IntegerField(verbose_name='转速', default=10)
    total_capacity = models.FloatField(verbose_name='磁盘总大小(GB)', null=True, blank=True)
    capacity = models.FloatField(verbose_name='磁盘大小GB', null=True, blank=True)
    memo = models.CharField(verbose_name='备注', max_length=128, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    latest_date = models.DateField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name_plural = '硬盘组件表'

    def __str__(self):
        if self.slot:
            return '%s:%s:%s' % (self.asset_id, self.slot, self.capacity)
        else:
            return '%s:%s' % (self.asset_id, self.total_capacity)


class NIC(models.Model):
    """网卡组件表"""
    asset = models.ForeignKey(verbose_name='所属资产', to='Asset', on_delete=models.CASCADE)
    slot = models.CharField(verbose_name='插槽', max_length=64, null=True, blank=True)
    name = models.CharField(verbose_name='网卡名称', max_length=128, null=True, blank=True)
    macaddress = models.CharField(verbose_name='MAC', max_length=64, unique=True)
    ipaddress = models.GenericIPAddressField(verbose_name='IP', null=True, blank=True)
    memo = models.CharField(verbose_name='备注', max_length=128, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    latest_date = models.DateField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name_plural = '网卡组件表'

    def __str__(self):
        if self.slot:
            return '%s:%s:%s' % (self.asset_id, self.slot, self.macaddress)
        else:
            return '%s:%s' % (self.asset_id, self.macaddress)


class AssetRecord(models.Model):
    """资产变更记录表,creator为空时，表示是资产汇报的数据。"""
    asset = models.ForeignKey(verbose_name='所属资产', to='Asset', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='变更内容', null=True)
    creator = models.ForeignKey(verbose_name='变更来源', to='UserProfile', null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = "资产变更记录表"

    def __str__(self):
        return "%s-%s-%s" % (self.asset.idc.name, self.asset.cabinet_num, self.asset.cabinet_order)


class ErrorLog(models.Model):
    """错误日志,如：agent采集数据错误 或 运行错误"""
    asset = models.ForeignKey(verbose_name='所属资产', to='Asset', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(verbose_name='标题', max_length=64)
    content = models.TextField(verbose_name='内容')
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = '错误日志表'

    def __str__(self):
        return self.title
