# 安卓手机安装Klipper

## 1.安装debian系统
1. 下载F-Droid app,搜索Termux安装Termux\Termux:boot\AnLinux
2. 打开Termux执行命令：
    1. 更新：pkg update
    2. 安装ssh: pkg install openssh
    3. 在电脑控制台连接手机：ssh -p 8022 u0_a127@192.168.0.6 \\debain ssh -p 22 root@192.168.8.122
        1. 查看用户：whoami
        2. 查看IP：ifconfig
3. 安装debian系统
    1. pkg install wget openssl-tool proot -y
    2. wget https://ghproxy.com/https://raw.githubusercontent.com/EXALAB/AnLinux-Resources/master/Scripts/Installer/Debian/debian.sh
        1. wget https://raw.githubusercontent.com/EXALAB/AnLinux-Resources/master/Scripts/Installer/Debian/debian.sh
    3. nano debian.sh
    4. 对应的行修改为：wget https://ghproxy.com/https://raw.githubusercontent.com/EXALAB/AnLinux-Resources/master/Scripts/Installer/Debian/debian.sh
    5. bash debian.sh
    6. ./debian.sh
    6.
    6. apt install nginx
    7. logout
4. pkg install tsu //获取sudo
5. sudo ./start-debian.sh//进入debian
6. apt install sudo
7. useradd -m -s /bin/bash klipper
8. sudo passwd klipper
9. sudo usermod klipper -a -G sudo
10. su klipper//切换到klipper用户
11. cd ~//进入根目录
12. sudo apt install git -y//安装git
13. git clone https://gitee.com/miroky/kiauh.git//下载脚本
14. ./kiauh/kiauh.sh//使用Klipper的安装脚本
15. sudo apt install vim -y
16. vi startklipper.sh//常见启动klipper的脚本
    1.  
    ```shell
    cd /home/klipper/KlipperScreen
    /etc/init.d/nginx start
    DISPLAY=localhost:0 /home/klipper/.KlipperScreen-env/bin/python /home/klipper/KlipperScreen/screen.py -c /home/klipper/klipper_config/KlipperScreen.conf&
    /home/klipper/klippy-env/bin/python /home/klipper/klipper/klippy/klippy.py /home/klipper/klipper_config/printer.cfg -I /tmp/printer -l /home/klipper/klipper_logs/klippy.log -a /tmp/klippy_uds&
    /home/klipper/moonraker-env/bin/python /home/klipper/moonraker/moonraker/moonraker.py -l /home/klipper/klipper_logs/moonraker.log -c /home/klipper/klipper_config/moonraker.conf

    /etc/init.d/nginx start
    /home/klipper/klippy-env/bin/python /home/klipper/klipper/klippy/klippy.py /home/klipper/printer_data/config/printer.cfg -I /home/klipper/printer_data/comms/klippy.serial -l /home/klipper/printer_data/logs/klippy.log -a /home/klipper/printer_data/comms/klippy.sock&
    /home/klipper/moonraker-env/bin/python /home/klipper/moonraker/moonraker/moonraker.py -l /home/klipper/printer_data/logs/moonraker.log -c /home/klipper/printer_data/config/moonraker.conf
    ```

17. 将startklipper.sh转变为可执行的文件：sudo chmod +x ./startklipper.sh
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
        2.1 
         #修改源文件
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

# 内核编译

1. 解压内核文件，并进入该文件夹后打开终端
2. 解压交叉编译工具
3. 配置变量:配置交叉编译工具的bin文件夹路径，即替换下面PATH对应的值
4. 执行下列命令
```
#编译命令参考
export ARCH=arm64
export SUBARCH=arm64
export HEADER_ARCH=arm64
PATH="/home/username/toolchains/aarch64-linux-android-4.9/bin:/home/username/toolchains/arm-linux-androideabi-4.9/bin:${PATH}"
```
5. 执行命令： rm -rf out   \\删除输出文件（第一次编译可以不执行，因为还没有输出文件）
6. 执行命令： make O=out clean && make mrproper  \\设置输出文件到指定目录
7. 配置配置文件路径：make O=out ARCH=arm64 mokee_santoni_defconfig \\mokee_santoni_defconfig ===> 配置文件名字：./arch/arm64/configs目录下
8. 执行编译：make -j$(nproc --all) O=out ARCH=arm64 CROSS_COMPILE=aarch64-linux-android- CROSS_COMPILE_ARM32=arm-linux-androideabi-
9. 在./out/arm64/boot找到此文件：Image.gz-dtb
10. 解压测试步骤中的boot.img，解压成功后会有一个kernel.gz文件
11. 将文件Image.gz-dtb重命名为kernel.gz，两个文件的大小不能相差太大，替换解压出来的kernel.gz文件
12. 打包会boot.img,如果需要签名则签名，然后在刷入手机看看是否异常,没问题则继续
13. cd out \\进入out文件夹
14. 执行配置命令： make menuconfig
15. 在USB support中设置串口,最好看视频操作(时间点：23:30)
    1. Device Drivers ---> USB support ---> USB Serial Converter support ---> USB Winchiphead CH341...
    2. 保存退出
16. cd .. \\退出到上一级目录
17. 再次执行编译：make -j$(nproc --all) O=out ARCH=arm64 CROSS_COMPILE=aarch64-linux-android- CROSS_COMPILE_ARM32=arm-linux-androideabi-
18. 按照前面的方法将boot.img刷入手机




nmcli d wifi connect 烤鸭别鸡冻 password dixin305


nohup ./frpc -c frpc.toml >/dev/null 2>&1 &
