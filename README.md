## iredAdmin

    是用python3编写的iredmail后台管理平台,前端框架使用bootstrap,由于是后台管理建议浏览器使用firefox、chrome，如果使用IE建议IE10以上
	
	版本 v1.0 2018年1月30日 第一版

	
## 软件环境(基础)
    1) python3
	2) django 1.10+

## 安装(基于关闭selinux部署)

## 安装mysql
        # yum install mysql mysql-server mysql-devel -y

## 安装python3
        # yum install zlib-devel openssl-devel sqlite-devel bzip2-devel readline-devel  ncurses-devel
        安装python3
        # wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
        # tar zvxf Python-3.6.4.tgz
        # cd Python-3.6.4
        # ./configure --prefix=/usr/local/python3
        # make
        # make install

## 安装平台需要的python模块
        # /usr/local/python3/bin/pip3 install django django-mysql django-cors-headers simplejson uwsgi mysqlclient requests

## 创建iredadmin数据库，权限用户
	启动mysql
	# /etc/init.d/mysqld start
	进入mysql，创建数据库,创建用户
	mysql> CREATE DATABASE `iredadmin` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
	mysql> grant all on iredadmin.* to iredadmin@localhost identified by '123456';
	mysql> flush privileges;

## 项目部署
    # mkdir -p /home/data/www
    # git clone https://gitee.com/devop/iRedAdmin.git
    # cd iRedAdmin
    修改配置文件 iRedAdmin/settings.ini，将其中的数据库配置修改

## 导入管路员(可以自己创建) 用户名admin 密码123456
    #/usr/local/python3/bin/python3 manage.py loaddata data.json

## 截图
* 
![login](http://gitee.com/devop/iRedAdmin/raw/master/screen/2018-01-30T06-18-35.520Z.png)
![main](http://gitee.com/devop/iRedAdmin/raw/master/screen/2018-01-30T06-19-29.650Z.png)
![user](http://gitee.com/devop/iRedAdmin/raw/master/screen/2018-01-30T06-21-34.824Z.png)
![use1r](http://gitee.com/devop/iRedAdmin/raw/master/screen/2018-01-30T06-22-17.039Z.png)

## 有问题反馈
在使用中有任何问题，欢迎反馈给我，可以用以下联系方式跟我交流

* 邮件(249545020#qq.com, 把#换成@)
* QQ: 249545020

## 授权
    BSD license

## 捐助开发者
在兴趣的驱动下,写一个`免费`的东西，有欣喜，也还有汗水，希望你喜欢我的作品，同时也能支持一下。
当然，有钱捧个钱场（右上角的爱心标志，支持支付宝和PayPal捐助），没钱捧个人场，谢谢各位。

## 关于作者

```javascript
  var 17fengmi = {
    nickName  : "炎舞皇",
    site : "http://17fengmi.com"
  }
```