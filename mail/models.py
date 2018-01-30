from django.db import models
from mylib.utils import str_to_datetime
# Create your models here.

class Domain(models.Model):
    '''邮件域'''
    domain = models.CharField(verbose_name='邮件域名', max_length=255,unique=True, primary_key=True)
    description = models.TextField(verbose_name='说明',null=True)
    disclaimer = models.TextField(verbose_name='免责声明',null=True)
    aliases = models.IntegerField(verbose_name='别名',default=0)
    mailboxes = models.IntegerField(verbose_name='邮箱',default=0)
    maxquota = models.BigIntegerField(verbose_name='最大限制',default=0)
    quota = models.BigIntegerField(verbose_name='限制',default=0)
    transport = models.CharField(verbose_name='传输器', max_length=255,default='dovecot')
    backupmx = models.BooleanField(verbose_name='备份mx',default=False)
    settings = models.TextField(verbose_name='设置',null=True)
    created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    modified = models.DateTimeField(verbose_name='修改时间时间')
    expired = models.DateTimeField(verbose_name='过期时间时间')
    active = models.BooleanField(verbose_name="是否启用",default=True)

    class Meta:
        db_table = 'domain'
        app_label = 'm23'

class MailBox(models.Model):
    '''用户邮箱'''
    username = models.CharField(verbose_name='用户名', max_length=255,unique=True, primary_key=True)
    password = models.CharField(verbose_name='密码', max_length=255)
    name = models.CharField(verbose_name='姓名', max_length=255)
    language = models.CharField(verbose_name='姓名', max_length=5,default='zh_CN')
    storagebasedirectory = models.CharField(verbose_name='存储目录', max_length=255,default='/home/data/vmail')
    storagenode = models.CharField(verbose_name='存储节点', max_length=255,default='vmail1')
    maildir = models.CharField(verbose_name='邮箱目录', max_length=255)
    quota = models.BigIntegerField(verbose_name='限制',default=0)
    domain = models.CharField(verbose_name='邮件域名', max_length=255,db_index=True)
    transport = models.CharField(verbose_name='传输器', max_length=255)
    department = models.CharField(verbose_name='部门', max_length=255)
    rank = models.CharField(verbose_name='', max_length=255,default='normal')
    employeeid = models.CharField(verbose_name='用户ID', max_length=255)
    isadmin = models.BooleanField(verbose_name="是否管理员",default=False)
    isglobaladmin = models.BooleanField(verbose_name="是否",default=False)
    enablesmtp = models.BooleanField(verbose_name="是否",default=True)
    enablesmtpsecured = models.BooleanField(verbose_name="是否",default=True)
    enablepop3 = models.BooleanField(verbose_name="是否",default=True)
    enablepop3secured = models.BooleanField(verbose_name="是否",default=True)
    enableimap = models.BooleanField(verbose_name="是否",default=True)
    enableimapsecured = models.BooleanField(verbose_name="是否",default=True)
    enabledeliver = models.BooleanField(verbose_name="是否",default=True)
    enablelda = models.BooleanField(verbose_name="是否",default=True)
    enablemanagesieve = models.BooleanField(verbose_name="是否",default=True)
    enablemanagesievesecured = models.BooleanField(verbose_name="是否",default=True)
    enablesieve = models.BooleanField(verbose_name="是否",default=True)
    enablesievesecured = models.BooleanField(verbose_name="是否",default=True)
    enableinternal = models.BooleanField(verbose_name="是否",default=True)
    enabledoveadm = models.BooleanField(verbose_name="是否",default=True)
#    enablelib-storage = models.BooleanField(verbose_name="是否",default=True)
#    enableindexer-worker = models.BooleanField(verbose_name="是否",default=True)
    enablelmtp = models.BooleanField(verbose_name="是否",default=True)
    enabledsync = models.BooleanField(verbose_name="是否",default=True)
    enablesogo = models.BooleanField(verbose_name="是否",default=True)
    allow_nets = models.TextField(verbose_name='说明',null=True)
    lastlogindate = models.DateTimeField(verbose_name='最后登录时间', auto_now_add=True)
    lastloginipv4 = models.IntegerField(verbose_name='别名',default=0)
    lastloginprotocol = models.CharField(verbose_name='', max_length=255)
    disclaimer = models.TextField(verbose_name='免责声明',null=True)
    allowedsenders = models.TextField(verbose_name='免责声明',null=True)
    rejectedsenders = models.TextField(verbose_name='免责声明',null=True)
    allowedrecipients = models.TextField(verbose_name='免责声明',null=True)
    rejectedrecipients = models.TextField(verbose_name='免责声明',null=True)
    settings = models.TextField(verbose_name='设置',null=True)
    passwordlastchange = models.DateTimeField(verbose_name='修改时间时间')
    created = models.DateTimeField(verbose_name='修改时间时间',auto_now_add=True)
    modified = models.DateTimeField(verbose_name='修改时间时间')
    expired = models.DateTimeField(verbose_name='过期时间时间')
    active = models.BooleanField(verbose_name="是否启用",default=True)
    local_part = models.CharField(verbose_name='邮箱前缀', max_length=255)

    class Meta:
        db_table = 'mailbox'
        app_label = 'm23'

class Forwardings(models.Model):
    '''用户邮箱转发'''
    address = models.CharField(verbose_name='地址', max_length=255)
    forwarding = models.CharField(verbose_name='', max_length=255)
    domain = models.CharField(verbose_name='邮件域名', max_length=255)
    dest_domain = models.CharField(verbose_name='邮件域名', max_length=255)
    is_list = models.BooleanField(verbose_name="是否启用",default=False)
    is_forwarding = models.BooleanField(verbose_name="是否启用",default=False)
    is_alias = models.BooleanField(verbose_name="是否启用",default=False)
    active = models.BooleanField(verbose_name="是否启用",default=True)

    class Meta:
        db_table = 'forwardings'
        unique_together=("address","forwarding")
        app_label = 'm23'

class UserQuota(models.Model):
    '''用户邮箱容量'''
    username = models.CharField(verbose_name='地址', max_length=255)
    bytes = models.BigIntegerField(verbose_name='使用容量')
    messages = models.BigIntegerField(verbose_name='邮件数')
    domain = models.CharField(verbose_name='域名', max_length=255)

    class Meta:
        db_table = 'used_quota'
        app_label = 'm23'

class Alias(models.Model):
    '''邮件组别名'''
    address = models.CharField(verbose_name='地址', max_length=255, primary_key=True)
    name = models.CharField(verbose_name='地址', max_length=255)
    accesspolicy = models.CharField(verbose_name='地址', max_length=255)
    domain = models.CharField(verbose_name='域名', max_length=255)
    created = models.DateTimeField(verbose_name='修改时间时间',auto_now_add=True)
    modified = models.DateTimeField(verbose_name='修改时间时间',default=str_to_datetime('1970-01-01 01:01:01'))
    expired = models.DateTimeField(verbose_name='过期时间时间',default=str_to_datetime('9999-12-31 00:00:00'))
    active = models.BooleanField(verbose_name="是否启用",default=True)

    class Meta:
        db_table = 'alias'
        app_label = 'm23'