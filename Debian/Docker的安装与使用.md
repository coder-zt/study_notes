# 安装Docker\Docker-Compose

1. docker

```shell
apt install docker.io
```

2. docker-compose

```shell
apt install docker-compose
```
# 安装容器（mysql、nginx）

1. mysql

'''yml
version: '2.0'
services:
    mysql:
        container_name: "mo-mysql"
        network_mode: "host"
        environment:
            MYSQL_ROOT_PASSWORD: "zt123456"
            MYSQL_USER: 'root'
            MYSQL_PASS: 'zt123456'
        image: "mysql:5.7.30"
        restart: always
        ports:
            - 3306:3306
        volumes:
            - "/home/mo/docker/mysql/db:/var/lib/mysql"
            - "/home/mo/docker/mysql/conf:/etc/mysql"
            - "/home/mo/docker/mysql/log:/var/log/mysql"
'''

> docker-compose up -d[守护式运行]

2. nginx

nginx.conf
```
user nginx;
worker_processes 1;

events {
    worker_connections 1024;
}

server {
       listen       81; # 监听的端口
       server_name  localhost; # 域名或ip
       location / {	# 访问路径配置
           root   /home/mo/docker/nginx/wwwroot;# 根目录
           index  index.html index.htm; # 默认首页
       }
   }
```

'''yml
version: '2.0'
services:
    mysql:
        container_name: "mo-nginx"
        network_mode: "bridge"
        image: "nginx:1.19.2-alpine"
        restart: always
        ports:
            - 81:80
            - 443:443
        volumes:
            - "/home/mo/docker/nginx/wwwroot:/usr/share/nginx/html"
            - "/home/mo/docker/nginx/conf/nginx.conf:/etc/nginx/nginx.conf"
            - "/home/mo/docker/nginx/logs:/var/log/nginx"
'''

> docker-compose up -d[守护式运行]

3. redis

'''yml
version: '2.0'
services:
    redis:
        container_name: "mo-redis"
        network_mode: "bridge"
        image: redis
        command: redis-server --requirepass zt123456
        restart: always
        ports:
            - 6379:6379
        volumes:
            - "/home/mo/docker/redis/data:/data"
'''

> docker-compose up -d[守护式运行]

# 其他
1. 进入容器

```yml
docker exec -it [docker-ID>] /bin/bash
```

2. 关闭正在运行的容器

```yml
docker stop [docker-name]
```

3.  删除停止运行的容器

```yml
docker rm [docker-ID]
```

```yml
docker run -d --name=mac-debian -p 3306:3306  mysql

docker run -p 3306:3306 -it debain-11-mysql /bin/bash

dockeer run -dt --name=sob-ubuntu ubuntu
docker exec -it sob-ubuntu /bin/bash

-d 后台 -t -i 交互式 -p 端口映射
# 资源使用信息
docker stats
```

4. docker-compose 启动 mysql 时报错

```log
WARNING: Some networks were defined but are not used by any service: vhost-net
Creating debain-11-mysql
Attaching to debain-11-mysql
debain-11-mysql | 2023-02-11 15:09:11+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 5.7.30-1debian10 started.
debain-11-mysql | 2023-02-11 15:09:11+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
debain-11-mysql | 2023-02-11 15:09:11+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 5.7.30-1debian10 started.
debain-11-mysql | 2023-02-11 15:09:11+00:00 [Note] [Entrypoint]: Initializing database files
debain-11-mysql | 2023-02-11T15:09:11.405320Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
```
