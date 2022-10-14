
# 使用octoPrint
0. 安装软件OctoPrint For Android
1. 使用ssh登录移动端
2. su(switch user) 切换当前用户,默认切换为root ==> :/data/data/com.termux/files/home #
3. cd /data/data/com.octo4a/files 进入octoPrint的files文件夹
4. ls -la (ls:list directory contents ==> 列出目前工作目录所含之文件及子目录)
- 4.1 -a 显示所有文件及目录 (. 开头的隐藏文件也会列出)
- 4.2 -l 除文件名称外，亦将文件型态、权限、拥有者、文件大小等资讯详细列出

# 使用TCP-UART
0. 安装软件TCPUART
1. sudo ./start-debian-org.sh 进入debian
2. su klipper 切换为klipper用户
3. socat -d -d pty,link=/tmp/tcpserial,raw,echo=0,waitslave tcp:localhost:8080 创建虚拟设备，开启 TCP 数据转发
4. cat /tmp/tcpserial