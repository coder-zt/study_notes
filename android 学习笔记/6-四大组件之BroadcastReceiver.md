# 四大组件之BroadcastReceiver

- 向其他应用广播信息，方便各应用做出相应策略

## 广播接收者

### 电量监听demo
1. 创建广播接收者类继承于BroadcastReceiver
2. 设置监听的频道
    1. 创建intentFilter对象
    2. 在此对象上添加动作
3. 创建广播接受对象
4. 注册广播（动态注册）
    ```java
    //设置监听
    IntentFilter intentFilter = new IntentFilter();
    intentFilter.addAction(Intent.ACTION_BATTERY_CHANGED);
    BroadcastReceiver broadcastReceiver = new BatteryLevelReceiver();
    //注册广播接收器
    this.registerReceiver(broadcastReceiver, intentFilter);

    /**
     * 1.创建广播->继承于BroadcastReceiver
     */
    private class BatteryLevelReceiver extends BroadcastReceiver{

        @Override
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            Log.d(TAG, "电量变化了！---》" + action);
        }
    }
    ```
### 静态注册
1. 编写继承BroadcastRevecier的类
2. 在Manifest文件中注册该广播
3. 由于系统为了提供用户体验，不推荐静态注册，官方也减少的能静态注册的广播
4. 尽量采用动态注册
```
<receiver android:name=".broadcastReceive" >
    <intent-filter>
        <action android:name="android.intent.action.BOOT_COMPLETED" />
    </intent-filter>
</receiver>
```

### 发送广播
1. 新建意图
2. 设置动作
3. 存放数据
4. 设置组件（指定广播接受器）
5. 发送广播
    ```java
        public void sendbroadcast(View view) {
        Intent intent = new Intent();
        intent.setAction("this.is.a.broadcast");
        intent.setComponent(new ComponentName("com.zhangtao.androidlearndemo","com.zhangtao.androidlearndemo.broadcastReceive"));
        intent.putExtra("data", "武汉加油");
        Log.d(TAG, "马上发送广播");
        sendBroadcast(intent);
    }
    ```


