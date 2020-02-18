# 四大组件之Activity

## AndroisManifest.xml文件
- 软件的配置文件，主要设置软件图标，名称,主题等
- 注册Activity \<activity>\</activity>
- 设置软件入口
- 意图过滤\<intent-filter>\</intent-filter>
- 添加权限\<uses-permission/>

## 意图
- 显式意图实现程序跳转->应用内部
    * 跳转前
        1. 声明意图
        2. 传入参数
        3. 跳转
        4. 注销该页面-finshed();
        ```java
        Intent intent = new Intent(activity_main_login.this,activity_sec_admin.class);
        intent.putExtar("key","value");
        startActivity(intent);
        finish();
        ```
    * 跳转后
        1. 获取意图-getIntent()
        2. 获取数据-getStringExtar("key", "defualt")至此多种类型数据的获取
        ```java
        Intent intent = getIntent();
        String data = intent.getStringExtar("key","defualt_value");
        ```
    * 主要应用于应用内的程序跳转
- 隐式意图实现跳转->各应用之间
    * 不直接指定activity的名字而利用意图过滤器进行跳转
    * \<action>动作名称
    * \<categroy>种类
    * 对Intent设置动作和增加种类而实现的跳转
        ```java
        intent = new Intent();
        intent.setAction("com.zhangtao.androidlearndemo.intent");
        intent.addCategory(Intent.CATEGORY_DEFAULT);
        intent.putExtra("mode", "隐式");
        startActivity(intent);
        ```
- 引用型无默认值因为没有值时返回null

## 传递参数
- 普通>>>见上文
- 传递对象
    1. 对象需要实现Parceable接口->实现了对象序列化以便于传输
    2. 向普通方式一样传递一个实例化对象 
- 传递数据
    1. 数据按照Manifest文件中的data的方式编辑数据格式
    2. 在意图中增加传递的数据
        ```java
        requestPermission();//动态申请相关权限
        Intent intent = new Intent();
        intent.setAction(Intent.ACTION_CALL);
        intent.addCategory(Intent.CATEGORY_DEFAULT);
        Uri uri = Uri.parse("tel:10086");
        intent.setData(uri);
        startActivity(intent);
        ```
- 实现数据的传输和接收
    - 1. 编写意图过滤器中的\<data android:scheme =""\/>
    - 2. 向上面一样编写意图
    - 3. 接收数据->getData()->@return Uri
        ```java
        //Uri.prase("info:信息内容")
         result = intent.getData().toString().split(":")[1];
        ```
## 数据回传
1. 跳转函数：startActivityForResult(意图, 请求码);
    ```java
    public void returnData(View view) {
        Intent intent = new Intent(activity_sec_Activity.this, activity_thr_intent.class);
        intent.putExtra("mode", "数据回传");
        startActivityForResult(intent, REQUESR_CODE);
    }
    ```
2. 重写函数：onActivityResult(int requestCode, int resultCode, @Nullable Intent data)
    * 根据请求码、结果码及获取的数据进行相应处理
    ```java
     @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if(requestCode== REQUESR_CODE && resultCode == 2){
            Toast.makeText(this, data.getStringExtra("return"), Toast.LENGTH_SHORT).show();
        }
    }
    ```
3. 跳转页面：setResult(结果码， 意图);//意图中添加数据
    ```java
    private void returnData() {
    tvResult.setOnClickListener(new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            Intent intent = new Intent();
            intent.putExtra("return", "回传数据");
            setResult(2, intent);
            finish();
        }
    });
    }
    ```
4. 调用第三回应用（相机）接收返回数据
    ```java
    //调用相机应用
    public void takePhoto(View view) {
        Intent intent = new Intent("android.media.action.IMAGE_CAPTURE");
        intent.addCategory(Intent.CATEGORY_DEFAULT);
        startActivityForResult(intent, TAKEPHOTO_CODE);
    }
    //动态申请权限
        ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CALL_PHONE, Manifest.permission.CAMERA}, 1);
    //根据请求码和结果码获取数据
        if(requestCode == 2 && resultCode == RESULT_OK){
        Bundle extras = data.getExtras();
        Bitmap mImageBitmap = (Bitmap) extras.get("data");
        llView.setBackground(new BitmapDrawable(mImageBitmap));
    ```
## 关于权限
1. android 6 以后不仅要在Manifest文件中写上权限声明还要动态申请权限
2. 调用申请函数：ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CALL_PHONE, Manifest.permission.CAMERA}, 1);
3. 重写函数->查询权限获取情况，对权限获取失败的进一步处理，引导用户打开权限
    - public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults)
    ```java
    //调用函数申请相关权限
    ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CALL_PHONE, Manifest.permission.CAMERA}, 1);
    //查询权限获取情况
    @Override//(重写函数)
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }
    ```

## 生命周期
1. 应用开始和结束时的调用
- onCreate-创建视图，加载数据

- onDestroy-保存数据

2. 在中途退出应用时会调用onStop而再次回到应用调用onStrat
- 它们会被调用取决于页面是否还可见
- onStrat-再次回到应用的处理

- onStop-中途退出应用的处理
3. 在页面跳转时，会调用onPause()\onResume()
- 它们会被调用取决于页面是否可以获取焦点
- onPause-页面失去焦点

- onResume-页面获取焦点
4. 在切换横竖屏时，页面时销毁在创建
- 第一种方式-一直处于横屏
    * android:SrceenOrientation="landscape"
- 第二种方式-主要用于经常切换横竖屏
    * android:configChanges="kryboardHidden|screenSize|orientation"

## 启动模式

### 任务栈
- 利用栈来保存任务界面等
```
android:launchMode="standard|singleTop|singleTask|singleInstance"
```
- standard - 创建新的任务，符合栈的特点：先进后出

- singleTop - 如果该任务在栈顶则不在创建新的任务

- singTask - 如果该任务已创建则不会在创建，若不在栈顶这将上面的任务出栈直到自己为栈顶-页面资源比较大

- singleInstance - 会单独创建一个任务栈,在调用该页面，不会新建而是提前到其他任务前面 - 有道取词、launcher
