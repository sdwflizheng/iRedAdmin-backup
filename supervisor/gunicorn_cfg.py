##指定workers的数目，使用多少个进程来处理请求
workers = 8
#指定每个进程开启的线程数
threads = 2 
##绑定本地端口
#bind = '0.0.0.0:8081'
bind = 'unix:/home/data/www/adAdmin/logs/gunicorn.sock'
user='www'
group='www'
proc_name = 'gunicorn.adAdmin'
#切换工作目录
chdir = '/home/data/www/adAdmin'
#指定python运行环境
pythonpath='/usr/local/python3/bin'
#工作模式
#sync
#eventlet - Requires eventlet >= 0.9.7
#gevent - Requires gevent >= 0.13
#tornado - Requires tornado >= 0.2
#gthread - Python 2 requires the futures package to be installed
#gaiohttp - Requires Python 3.4 and aiohttp >= 0.21.5
worker_class = 'gevent'
worker_connections = 1000
max_requests = 1000
#超时
timeout = 30
loglevel = 'debug'
#访问日志
accesslog='/home/data/www/adAdmin/logs/gunicorn_access.log'
errorlog='/home/data/www/adAdmin/logs/gunicorn_error.log'
#pid文件
pidfile='/home/data/www/adAdmin/logs/gunicorn.pid'
#后台运行
#daemon = True

#/usr/local/python3/bin/gunicorn -c gunicorn_cfg.py gamepay.wsgi:application

#nginx配置
"""
upstream test {
  server unix:/home/data/www/gamepay/logs/gunicorn.sock;
}
server {
        listen 80;
        server_name _;

        index index.html index.htm index.jsp;
        root /home/data/www/gamepay;

        location ^~ /gamepay/ {
            proxy_pass http://test;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        }
        location ^~ /gamepayadmin/ {
            proxy_pass http://test;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        }        
                location /gamepay/uploads {
                    alias /home/data/www/gamepay/uploads;
                }

                location /gamepay/static {
                        alias /home/data/www/gamepay/static;
                }

        location ~ .*.(svn|git|cvs) {
            deny all;
        }

}
"""