# -*- coding: utf-8 -*-
#
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.encoding import filepath_to_uri
from collections import OrderedDict
import base64
import os
import string
import logging
import datetime
import time
import hashlib
from email.utils import formatdate
import calendar
import threading
import uuid
import random 
import requests 
import simplejson as json
import ftplib
import socket

def get_logger(name=None):
    return logging.getLogger('%s' % name)


def timesince(dt, since='', default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days, 5 hours.
    """

    if since is '':
        since = datetime.datetime.utcnow()

    if since is None:
        return default

    diff = since - dt

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        if period:
            return "%d %s" % (period, singular if period == 1 else plural)
    return default

_STRPTIME_LOCK = threading.Lock()

_GMT_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
_ISO8601_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"


def to_unixtime(time_string, format_string):
    time_string = time_string.decode("ascii")
    with _STRPTIME_LOCK:
        return int(calendar.timegm(time.strptime(time_string, format_string)))


def http_date(timeval=None):
    """返回符合HTTP标准的GMT时间字符串，用strftime的格式表示就是"%a, %d %b %Y %H:%M:%S GMT"。
    但不能使用strftime，因为strftime的结果是和locale相关的。
    """
    return formatdate(timeval, usegmt=True)


def http_to_unixtime(time_string):
    """把HTTP Date格式的字符串转换为UNIX时间（自1970年1月1日UTC零点的秒数）。

    HTTP Date形如 `Sat, 05 Dec 2015 11:10:29 GMT` 。
    """
    return to_unixtime(time_string, _GMT_FORMAT)


def iso8601_to_unixtime(time_string):
    """把ISO8601时间字符串（形如，2012-02-24T06:07:48.000Z）转换为UNIX时间，精确到秒。"""
    return to_unixtime(time_string, _ISO8601_FORMAT)

def capacity_convert(size, expect='auto', rate=1000):
    """
    :param size: '100MB', '1G'
    :param expect: 'K, M, G, T
    :param rate: Default 1000, may be 1024
    :return:
    """
    rate_mapping = (
        ('K', rate),
        ('KB', rate),
        ('M', rate**2),
        ('MB', rate**2),
        ('G', rate**3),
        ('GB', rate**3),
        ('T', rate**4),
        ('TB', rate**4),
    )

    rate_mapping = OrderedDict(rate_mapping)

    std_size = 0  # To KB
    for unit in rate_mapping:
        if size.endswith(unit):
            try:
                std_size = float(size.strip(unit).strip()) * rate_mapping[unit]
            except ValueError:
                pass

    if expect == 'auto':
        for unit, rate_ in rate_mapping.items():
            if rate > std_size/rate_ > 1:
                expect = unit
                break
    expect_size = std_size / rate_mapping[expect]
    return expect_size, expect

def filesizeformat(value, baseMB=False):
    """Format the value like a 'human-readable' file size (i.e. 13 KB,
    4.1 MB, 102 bytes, etc).  Per default decimal prefixes are used (mega,
    giga etc.), if the second parameter is set to `True` the binary
    prefixes are (mebi, gibi).
    """
    try:
        bytes = float(value)
    except:
        return 0

    if baseMB is True:
        bytes = bytes * 1024 * 1024

    base = 1024

    if bytes == 0:
        return '0'

    ret = '0'
    if bytes < base:
        ret = '%d Bytes' % (bytes)
    elif bytes < base * base:
        ret = '%d KB' % (bytes / base)
    elif bytes < base * base * base:
        ret = '%d MB' % (bytes / (base * base))
    elif bytes < base * base * base * base:
        if bytes % (base * base * base) == 0:
            ret = '%d GB' % (bytes / (base * base * base))
        else:
            ret = "%d MB" % (bytes / (base * base))
    else:
        ret = '%.1f TB' % (bytes / (base * base * base * base))

    return ret

def sum_capacity(cap_list):
    total = 0
    for cap in cap_list:
        size, _ = capacity_convert(cap, expect='K')
        total += size
    total = '{} K'.format(total)
    return capacity_convert(total, expect='auto')


def str_to_md5(strs):  
    m=hashlib.md5()  
    m.update(strs.encode("utf8"))  
    return m.hexdigest()

def int_random():
    """使用uuid生产随机数,返回128位整数"""
    u = uuid.uuid1()
    return u.int

def hex_random():
    """使用uuid生产随机数,返回32位十六进制"""
    u = uuid.uuid1()
    return u.hex
 
def iso8601_to_time(time_string):
    """把ISO8601时间字符串（形如，2012-02-24T06:07:48.000Z）转换为UNIX时间，精确到秒。"""
    return time_string.strftime('%Y-%m-%d %H:%M:%S')

def str_to_datetime(string):
    """字符串 2017-10-21 00:00:00 格式化为datetime"""
    return datetime.datetime.strptime(string,"%Y-%m-%d %H:%M:%S")


def sumplus(*args):
    """求和"""
    r = 0.0
    for n in args:
        r += float(n)
    return "%.2f" % r

def sumplusInt(*args):
    """求和"""
    r = 0
    for n in args:
        r += int(n)
    return r

class ImageStorage(FileSystemStorage): 
    """
    图片上传
    """ 
    
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):  
        #初始化  
        super(ImageStorage, self).__init__(location, base_url)  
  
    #重写 _save方法          
    def _save(self, name, content):  
        
        #文件扩展名  
        ext = os.path.splitext(name)[1]  
        #文件目录  
        d = os.path.dirname(name)  
        #定义文件名，年月日时分秒随机数
        year = time.strftime('%Y')
        month = time.strftime('%m')
        fn = time.strftime('%Y%m%d%H%M%S')  
        fn = fn + str(hex_random())
        #重写合成文件名  
        name = os.path.join('images', year,month, d, fn + ext)  
        #调用父类方法  
        return super(ImageStorage, self)._save(name, content)
       
def htmlfilesave(name, content, gameid):  
    """
    保存文件,返回url地址
    """
    
    #文件扩展名  
    ext = os.path.splitext(name)[1]  
 
    #定义文件名，年月日时分秒随机数
    year = time.strftime('%Y')
    month = time.strftime('%m')
    fn = time.strftime('%Y%m%d%H%M%S')  
    fn = fn + str(hex_random())
    #重写合成文件名  
    name = os.path.join('html', year,month, gameid, fn + ext) 
    #完整的文件路径 
    full_name = os.path.join(settings.MEDIA_ROOT, name)
    #得到url
    url = filepath_to_uri(os.path.join(settings.MEDIA_URL, name))

    directory = os.path.dirname(full_name)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except FileNotFoundError:
            pass

    if not os.path.isdir(directory):
        raise IOError("%s exists and is not a directory." % directory)

    #写入文件
    #open(full_name,'w', encoding='utf8').writelines(content.replace(settings.HTML_HREF_REPLACE_KEY, app_url))
    open(full_name,'w', encoding='utf8').writelines(content)

    return url

def writefile(content, apk_url, ext='html'):  
    """
    写文件，返回文件路径
    """
    ext = '.' + ext

    fn = time.strftime('%Y%m%d%H%M%S')  
    fn = fn + str(hex_random())
    #重写合成文件名  
    name = os.path.join('cdnfile', fn + ext) 
    #完整的文件路径 
    full_name = os.path.join(settings.MEDIA_ROOT, name)

    directory = os.path.dirname(full_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    #写入文件
    open(full_name,'w', encoding='utf8').writelines(content.replace(settings.HTML_HREF_REPLACE_KEY, apk_url))

    return full_name

def ftpupload(host, port, username, password, upload_dir, upload_file, rmfile=False):
    """上传文件到ftp"""
    
    timeout = 10
    ftp = ftplib.FTP()
    filename = os.path.basename(upload_file)
    try:
        #连接ftp
        ftp.connect(host=host, port=port, timeout=timeout)
    except (socket.error, socket.gaierror):
        return  False, "连接FTP失败 %s" % host
  
    try:
        #登录
        ftp.login(username, password)
    except ftplib.error_perm:
        return  False, "ftp用户名或密码错误"
    
    try:
        #切换到操作目录
        ftp.cwd(upload_dir)
    except:
        #切换目录失败,目录不存在
        #创建目录
        ftp.mkd(upload_dir)
        #切换目录
        ftp.cwd(upload_dir)
    
    fd=open(upload_file,'rb')
    #上传文件
    ftp.storbinary('STOR %s' % filename, fd)
    
    fd.close()
    ftp.quit()  

    #删除文件
    if rmfile:
        os.remove(upload_file)

    #返回写入的ftp地址
    url = filepath_to_uri(os.path.join('/', upload_dir, filename))

    return True,url 


class ExcelStorage(FileSystemStorage): 
    """
    excel文件上传
    """ 
    
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):  
        #初始化  
        super(ExcelStorage, self).__init__(location, base_url)  
  
    #重写 _save方法          
    def _save(self, name, content):  
        
        #文件扩展名  
        ext = os.path.splitext(name)[1]  
        #文件目录  
        d = os.path.dirname(name)  
        #定义文件名，年月日时分秒随机数
        year = time.strftime('%Y')
        month = time.strftime('%m')
        fn = time.strftime('%Y%m%d%H%M%S')  
        #fn = fn + str(hex_random())
        #重写合成文件名  
        name = os.path.join('excel', year,month, d, fn + ext)  
        #调用父类方法  
        return super(ExcelStorage, self)._save(name, content)
