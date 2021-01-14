# android网络编程
## http协议(超文本传输协议)
- 基于TCP/IP
- 请求方式
    * post
    * get
    * put
    * delete
- 响应码

    | 响应码 | 类别 | 原因 |
    | :---:  | :---: | :---: |
    | 1xx | Infomational(信息性状态码) | 接收的请求正在处理 |
    | 2xx | Success(成功状态码) | 请求正常处理完毕 |
    | 3xx | Redirection(重定向状态码) | 需要进行附加操作以完成请求 |
    | 4xx | Client Error(客户端错误状态码) | 服务器无法处理请求 |
    | 5xx | Server Error(服务器错误状态码) | 服务器处理请求出错 |

- http请求格式
    * 请求行
    * 请求头
    * 空一行
    * 请求体
- http响应格式
    * 响应行
    * 响应头
    * 空一行
    * 向应体

## 使用java的api进行请求数据
```java
 new Thread(new Runnable() {
    @Override
    public void run() {
        try {
            URL url = new URL("http://localhost:9102/get/text");
            HttpURLConnection connection = (HttpURLConnection)url.openConnection();
            connection.setConnectTimeout(10000);
            connection.setRequestMethod("GET");
            connection.setRequestProperty("Accept-Encoding", " gzip, deflate");
            connection.setRequestProperty("Accept-Language", "zh-CN,zh;q=0.9,en;q=0.8");
            connection.connect();
            //响应码
            int resultCode = connection.getResponseCode();
            if(resultCode == 200){
                Map<String, List<String>> headerFields = connection.getHeaderFields();
                Set<Map.Entry<String, List<String>>> entrysets = headerFields.entrySet();
                for(Map.Entry<String, List<String>> entry : entrysets){
                    Log.d(TAG, entry.getKey() + "==" + entry.getValue());
                }
            }
            InputStream inputStream = connection.getInputStream();
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
            String lines = "";
            while(bufferedReader.read()){
                lines +=  bufferedReader.readLine();
            }
            Log.d(TAG, "content --> " +  bufferedReader.readLine());

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}).start();
```

- api27以后禁止访问明文http

    * 处理办法：修改配置-> android:usesCleartextTraffic="true"
    * 添加网络配置文件：android:networkSecurityConfig="@security_file.xml"
    * @security_file.xml
        ```xml
            <?xml version="1.0" encoding="utf-8"?>
            <network-security-config>
                <domain-config>
                    <domain includeSubdomains="true">sunofbeaches.com</domain>
                    <domain-config cleartextTrafficPermitted="true">
                        <domain includeSubdomains="true">www.sunofbeaches.com</domain>
                    </domain-config>
                </domain-config>
            </network-security-config>
        ```


## 使用java的api进行请求图片

```java
 public void requestToImg(View view) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    URL url = new URL("https://cn.bing.com/th?id=OHR.Windhorses_ZH-CN5349922758_1920x1080.jpg&rf=LaDigue_1920x1080.jpg");
                    HttpURLConnection connection = (HttpURLConnection)url.openConnection();
                    connection.setConnectTimeout(10000);
                    connection.setRequestMethod("GET");
                    connection.setRequestProperty("Accept-Encoding", " gzip, deflate");
                    connection.setRequestProperty("Accept-Language", "zh-CN,zh;q=0.9,en;q=0.8");
                    connection.connect();
                    //响应码
                    int resultCode = connection.getResponseCode();
                    if(resultCode == 200){
                        //从数据流中获取图片
                       final Bitmap resBitmap = BitmapFactory.decodeStream(connection.getInputStream());
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                               ImageView iv_show = findViewById(R.id.iv_photo);
                               iv_show.setImageBitmap(resBitmap);
                            }
                        });
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }
```

## 加载大图片处理优化


