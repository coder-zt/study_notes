
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

# 编译内核
- https://www.bilibili.com/video/BV1vt4y1w7Rb/
## ROM推荐(00:00 - 06:18)
- TWRP文件下载：https://onfix.cn
- MoKee下载
    https://download.mokeedev.com/
    https://github.com/MoKee

- crdroid下载
    https://crdroid.net/downloads
    https://github.com/crdroidandroid

- lineageos下载
    https://download.lineageos.org/
    https://github.com/LineageOS

## 编译前的测试工作(06:18-10:39)

- 内核解包打包工具下载
    https://github.com/Vaimibao/Boot-Recoveryimg-Un-Repack-Tool

1.使用解压打包工具：Boot-Recoveryimg-Un-Repack-Tool -> xiyan.bat
    1. 解压刷机包文件 ===>boot.img
    2. 直接打包（如果文件大小不一致，需要签名，文件大小应该一致）
    3. 刷入手机测试是否能正常开机

# 编译环境搭建(10:39-16:50)

- VMware安装Ubuntu(桌面版)

- 换源：在软件更新器中设置（可选）

- 编译环境安装：sudo apt-get install -y build-essential kernel-package libncurses5-dev bzip2

    ```s
    - sudo apt-get install kernel-package 报错：没有可用的软件包 kernel-package，但是它被其它的软件包引用了。处理

    1. 源的问题，需要新增一个新的源
    2. 修改源文件
        2.1 vim /etc/apt/sources.list #修改源文件
        2.2 deb http://cz.archive.ubuntu.com/ubuntu focal main universe # 添加新源，添加到新的一行
    3. 更新数据
        3.1 sudo apt-get update
        3.2 sudo apt-get upgrade
    4. 重新安装
        4.1 sudo apt-get install kernel-package
    ```
- 交叉编译工具(https://android.googlesource.com/platform/prebuilts/gcc/linux-x86/)

1. 分别下载32位和64位(最好是最新的版本)
- https://android.googlesource.com/platform/prebuilts/gcc/linux-x86/aarch64/aarch64-linux-android-4.9/+/refs/tags/android-10.0.0_r47
- https://android.googlesource.com/platform/prebuilts/gcc/linux-x86/arm/arm-linux-androideabi-4.9/+/refs/tags/android-10.0.0_r47


- 将文件复制ubuntu系统下
