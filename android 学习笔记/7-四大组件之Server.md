# 四大组件之Server

## 了解服务

### 什么是服务

- 用俗话说就是长期运行在后台的程序
- 它是一个组件，用于执行长期运行的任务，并且与用户没有交互
- 注册<service\>

### 为什么使用服务

- 运行一些后台任务，如下载、音乐播放等
- 进程（内存不足会杀进程）
    * 前台进程
    * 可见进程
    * 服务进程
    * 后台进程
    * 空进程

## service的周期

- onCreate
- onStartCommand
- onStart
- onDestroy

## 调用服务内部的函数

1. 创建一个内部类继承与Binder的子类调用服务的方法
2. onBind返回一个子类对象
3. 绑定服务
4. 调用服务内部方法->获取服务内部类的对象并间接调用内部的函数
5. 解除服务

## 两种开启服务的方式

| 开启方式 | 优缺点 | 生命周期 |
| :---: | :---: | :---: |
| StartService | 可以长期运行在后台，但不能通讯 | onCreate -> onStartCommend -> onDestroy
| BindService | 可以通信，但不能长期运行 | onCreate -> onBind -> onUnbind -> onDestroy

- 开启与停止

```java
  /**
     * 开启服务
     * @param view
     */
    public void startSerivce(View view) {
        Intent intent = new Intent(this, Service_First.class);
        startService(intent);
    }

    /**
     * 停止服务
     * @param view
     */
    public void stopSerivce(View view) {
        Intent intent = new Intent();
        intent.setClass(this, Service_First.class);
        stopService(intent);
    }
```

- 绑定与解除

```java

    /**
     * 绑定服务
     * @param view
     */
    public void bindSerivce(View view) {
        Intent intent = new Intent();
        intent.setClass(this, Service_First.class);
        isBindService = bindService(intent, mServiceConnection, BIND_AUTO_CREATE);
    }

    private ServiceConnection mServiceConnection = new ServiceConnection() {

        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            mRemoteBinder = (Service_First.InnerBinder)service;
            Log.d(TAG,"连接服务。。。");

        }

        @Override
        public void onServiceDisconnected(ComponentName name) {
            mRemoteBinder = null;
            Log.d(TAG,"断开服务。。。");
        }
    };
    /**
     * 解除服务
     * @param view
     */
    public void unbindSerivce(View view) {
        if(mServiceConnection != null && isBindService){
            unbindService(mServiceConnection);
           mRemoteBinder = null;
        }
    }
```

## 用接口隐藏服务内部类的实现

1. 创建调用服务内部的接口

    ```java
    public interface ICommunication {
        void callServiceInnerMenthod();
        }
    ```

2. 内部类继承自binder和接口

    ```java
    private class ICommunication extends Binder implements com.zhangtao.androidlearndemo.Interfaces.ICommunication {

        @Override
        public void callServiceInnerMenthod() {
            sayHello();
        }
    }
    ```

3. 使用接口实现调用服务内的函数

    ```java
    private ICommunication iCommunication;
    ```

---

## 银行服务案例

1. 定义接口
    - 普通用户->存钱、取钱、贷款
    - 银行工作人员->查询账户信息、冻结账户、存钱、取钱、贷款
    - 银行老板->修改账户金额、查询账户信息、冻结账户、存钱、取钱、贷款
    - 依次继承接口

2. 实现接口
    -实现对应的接口，并继承自Binder,作为返回对象
3. 在服务中利用意图动作返回接口实现
4. UI实现
    - UI实现时，当有多个重复看控件时，可用<include layout="..."\>，提高代码复用
5. 各角色的功能实现
    1. 绑定服务
        * 设置动作，添加种类，设置包名
        * 创建连接类实现ServiceConnection
            - 通过IBinder返回接口实现对象，进而调用该对象的方法
        * 调用绑定服务
    2. 通过返回实现对象的方法实现角色功能
    3. 解除邦定

## AIDL android interface definition language
- 进程间的通信

## Service的生命周期
1. 通过开启服务到关闭服务
- onCreate->onStratCommand->onDestroy
2. 开启服务后再开启服务到关闭服务(若服务未关闭，那么服务不会再创建)
- onCreate->onStratCommand->...->onStratCommand->onDestroy
3. 通过绑定服务到解除服务
- onCreate->onBind->onUnbind->onDestroy
4. 通过开启服务再绑定服务之后解除服务再关闭服务
- onCreate->onStratCommand->onBind->onUnbind->onDestroy
### 音乐播放案例
1. 实现播放器UI界面
2. 播放器接口定义
3. UI层调用方法
4. 实现UI接口
5. 实现底层逻辑层接口