## 2.18

### 项目初始化
1. 创建项目
2. 使用git管理自己的代码
3. 创建相应的文件夹
    - 适配器文件夹---adapters
    - 工具类文件夹---utils
    - fragment文件夹---fragments
    - 逻辑相关文件夹---presenters
    - 接口文件夹---interfaces
    - 自定义控件文件夹
### 喜马拉雅SDK
1. 下载SDK
2. 根据官方给的demo配置自己的项目
3. 加载第三方库
4. 测试是否继集成SDK成功
---
## 2.19

### 编写自己的日志打印工具类
### 下载第三方开源框架MagicIndicator
- 下载第三方开源框架后先运行其中DEMO
    * 修改grade文件和properties，保持于自己程序同步，减少加载时间
    * 安装软件查看demo样式
## 2.24
### 将MagicIndicator集成到自己的项目中(p6)
- 添加依赖
    ```java
    implementation 'com.github.hackware1993:MagicIndicator:1.5.0'
    ```
- 添加控件
    ```xml
      <net.lucode.hackware.magicindicator.MagicIndicator
        android:id="@+id/main_indicator"
        android:layout_width="match_parent"
        android:layout_height="40dp"
        tools:ignore="MissingConstraints" />
    ```
- 寻找控件并设置相关属性和适配器
    ```java
     mMagicIndicator = findViewById(R.id.main_indicator);
        mMagicIndicator.setBackgroundColor(this.getResources().getColor(R.color.main_color));
        //创建适配器
        mMagicIndicatorAdapter = new IndicatorAdapter(this);
        CommonNavigator commonNavigator = new CommonNavigator(this);
        commonNavigator.setAdapter(mMagicIndicatorAdapter);

    ```
- Indicator适配器
    * 标题数量
    * 标题样式
    * 标题下划线样式
### 绑定MagicIndicator与ViewPager(p7)
- ViewPager
    * 它的适配器为PagerAdapter,且FragmentAdapter是它的子类，可以使Fragment作为容器的子元素
    * FragmentAdapter
        - 返回Item数量
        - 根据当前位置返回对应子元素(Fragment)
        - 在上面为了返回相应的Fragment创建FragmentCreator类
- FragmentCreator类
    * 建立了Map<index, Fragment>用于存储Fragment，对此进行缓存，提高软件效率
    * 当前缓存Map中如果没有相应的Fragment则创建并且放到缓存map中
- 创建Fragment
    * 由于三个Fragment的属性相似，因此使三个Fragment继承父类BaseFragment
    * BaseFragment
        - 继承与Fragment
        - onCreateView(LayoutInflater layoutInflater, ViewGroup container, Bunle savedInstanceState)
            - 调用抽象函数，获得View
        - 拥有一抽象函数，返回View
        - 三个子类
            * 重写抽象函数，创建各自的View


### tab与ViewPager的联动(p8)(有待进一步理解)
- 为了实现联动，那么当点击tab会调用click事件更换ViewPager里的内容
    * 了解接口的使用
## 2.19
### indicator和搜索按钮的布局(p9)
- 使tab的item平均分布 - commonNavigator.setAdjustMode(true);
- 编辑布局文件，加入搜索按钮
### 获取推荐内容数据(p10)
- 根据SDK获取猜你喜欢的数据，验证适合成功
    ```java
    /**
     * 获取推荐内容，--猜你喜欢
     */
    private void getRecommendData() {
        //封装数据
        Map<String, String> map = new HashMap<String, String>();
        map.put(DTransferConstants.LIKE_COUNT, Constants.RECOMMEND_COUNT + "");
        CommonRequest.getGuessLikeAlbum(map, new IDataCallBack<GussLikeAlbumList>() {
            @Override
            public void onSuccess(GussLikeAlbumList gussLikeAlbumList) {
                //数据获取成功
                if (gussLikeAlbumList != null) {
                    List<Album> albums = gussLikeAlbumList.getAlbumList();
                    if (albums != null) {
                        LogUtil.d(TAG, "SIZE ---> " + albums.size());
                    }
                }
            }
            @Override
            public void onError(int i, String s) {
                //数据获取失败
                LogUtil.d(TAG,"error --> " + i);
                LogUtil.d(TAG,"errorMsg --> " + s);
            }
        });
    }
    ```
### 获取推荐内容数据UI展示设计(p11)
- 使用RecyclerView
- 使用Picasso(图片加载)

### 推荐内容数据UI展示设计优化（p12)
- 修改ImageView的填充方式
    * android:scaleType="fitXY"
- 修改RecyclerView滑动到末端的阴影显示
    * android:overScrollMode="never"
- 修改RecyclerView作为的间隙
    ```java
    //RecyclerView控件
     mRecommendRv.addItemDecoration(new RecyclerView.ItemDecoration() {
            @Override
            public void getItemOffsets(@NonNull Rect outRect, @NonNull View view, @NonNull RecyclerView parent, @NonNull RecyclerView.State state) {
                outRect.top = UIUtil.dip2px(view.getContext(), 5);
                outRect.bottom =UIUtil.dip2px(view.getContext(), 5);
                outRect.left =UIUtil.dip2px(view.getContext(), 5);
                outRect.right =UIUtil.dip2px(view.getContext(), 5);
            }
        });
    ```
- 修改RecyclerView每个Item的背景-圆角矩形
    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <shape xmlns:android="http://schemas.android.com/apk/res/android">
        <size android:width="350dp"
            android:height="75dp"/>
        <solid  android:color="#ffffff"/>
        <corners android:radius="4dp"/>
    </shape
    ```
- 修改图片的边框为圆角矩形-自定义View
    ```java
    public class RoundRectIamgeView extends AppCompatImageView{
        private float roundRatio = 0.2f;
        private Path path;
        public RoundRectIamgeView(Context context, AttributeSet attrs){
            super(context, attrs);
        }

        @Override
        protected void onDraw(Canvas canvas) {
            if(path == null){
                path = new Path();
                path.addRoundRect(new RectF(0,0,getWidth(), getHeight()), roundRatio*getWidth(), roundRatio*getHeight(), Path.Direction.CW);
            }
            canvas.save();
            canvas.clipPath(path);
            super.onDraw(canvas);
            canvas.restore();
        }
    }
    ```
### 推荐内容代码重构（p13)
- 在原始项目中，我们将网络请求推荐歌曲和更新UI全部写在了RecommendFargment.java中,导致程序结构复杂，使得数据与UI混合在一起，减少了请求数据的复用性，因此将数据独立出来
- 利用接口将二者之间建立联系
    * 数据请求接口-IRecommendPresenter
        - getRecommendList()\\\请求数据列表
        - registerViewCallback(IRecommendViewCallback callback)\\\注册UI的回调函数
        - unRegisterViewCallback(IRecommendViewCallback callback)
        \\\取消已注册的UI回调函数
    * 请求后，UI获取数据接口-IRecommendViewCallback
        - onRecommendListLoaded(List\<Album> result)\\\获取数据成功后UI的回调函数
    * RecommendFragment实现接口IRecommendViewCallback---RecommendPresenter实现接口IRecommendPressenter
        - RF通过IRP注册自己位IRP中的成员(IRVC)，并调用IRP的函数getRecommendList()获取数据，数据获取成功后，IRP使用成员(IRVC)调用onRecommendListLoaded()函数，通知RF已经获取数据成功。
- 获取RecommendPresenter对象-单例模式（设计模式）
    * 单例模式是指控制程序只能获取一个
### UILoader（p14）
- 当请求数据时，当数据请求未结束之前，页面应该没有数据显示，所以应该将当前页面显示正在加载。。。
- 当请求数据成功后，将数据用RecyclerView展示出来，即数据展示页面
- 若请求的数据为空，显示数据为空页面
- 若因为没有网络导致请求失败，我们应该显示网络无效，且还可以点重试
- 由于以上四种情况，我们需要构建UILoader，根据实际情况加载UI
- UILoader
    * 继承自FrameLayout-它继承ViewGroup，也就是一个View
        - 通过addView向其中加入View
        - 它的展示方式是层叠的展示每个View
        - 因此我们把四种情况的View通过addView()加入其中，并控制每个View的setVisibility()控制是否显示该View
    * 如何控制每个View的显示情况
        - 使用枚举
            ```java
            public  enum  UIStatus{
                LOADING, SUCCESS, NETWORK_ERROR, EMPTY, NONE
            }
            ```
        - 初始化
            ```java
            public UIStatus mCurrentStatus = UIStatus.NONE;
                private void init() {
                switchUIByCurrentStatus();
            }
            ```
        - 控制UI
            * 提供给外部控制UI的函数，根据请求的情况不同，设置当前程序的状态，并通过Hlander在主线程更新UI
            ```java
             public void updateStatus(UIStatus status){
                mCurrentStatus = status;
                //更新UI一定要到主线程
                BaseApplication.getsHandler().post(new Runnable() {
                        @Override
                    public void run() {
                            LogUtil.d(TAG, "当前所在线程的名称--->" + Thread.currentThread().getName());
                        switchUIByCurrentStatus();
                    }
                });
            }
            ```
        - 控制每个View
            * 根据当前程序状态设置每个View的可见性
            ```java
                private void switchUIByCurrentStatus() {
                    //加载中
                    if (mLoadingView == null) {
                        mLoadingView = getLoadingView();
                        addView(mLoadingView);
                    }
                    //根据状态设值是否可见
                    mLoadingView.setVisibility(mCurrentStatus == UIStatus.LOADING ? VISIBLE : GONE);

                    //成功
                    if (mSuccessView == null) {
                        mSuccessView = getSuccessView(this);
                        addView(mSuccessView);
                    }
                    //根据状态设值是否可见
                    mSuccessView.setVisibility(mCurrentStatus == UIStatus.SUCCESS ? VISIBLE : GONE);

                    //网络错误
                    if (mNetworkErrorView == null) {
                        mNetworkErrorView = getNetworkErrorView();
                        addView(mNetworkErrorView);
                    }
                    //根据状态设值是否可见
                    mNetworkErrorView.setVisibility(mCurrentStatus == UIStatus.NETWORK_ERROR ? VISIBLE : GONE);

                    //数据为空
                    if (mEmptyView == null) {
                        mEmptyView = getEmptyView();
                        addView(mEmptyView);
                    }
                    //根据状态设值是否可见
                    mEmptyView.setVisibility(mCurrentStatus == UIStatus.EMPTY ? VISIBLE : GONE);
                }
            ```
    - 创建每种情况的View
        * 加载layout文件创建View
            - LayoutInflater-将layout文件转换为View
            - 通过from()获取该对象
            - inflate()转换为view
            ```java
                private View getEmptyView() {
                    return LayoutInflater.from(getContext()).inflate(R.layout.fragment_empty_view, this, false);
                }
            ```
### UILoader-错误页面优化（p15）
* 重写错误页面的layout
* 实现View的点击事件
    - 设计接口
    ```java
        public interface OnRetryClickListener{
            void onRetryClick();
        }
    ```
    - 设置该监听器
    ```java
        public void  setOnRetryClickListener(OnRetryClickListener listener){
            this.mRetryClickListener = listener;
        }
    ```
    - 调用接口
        ```java
            private View getNetworkErrorView() {
                View networkErrorView =  LayoutInflater.from(getContext()).inflate(R.layout.fragment_networkerror_view, this, false);
                networkErrorView.findViewById(R.id.network_error_icon).setOnClickListener(new OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        //重新获取数据
                        if (mRetryClickListener != null) {
                            mRetryClickListener.onRetryClick();
                        }
                    }
                });
                return networkErrorView;
            }
        ```
    - 在所需的地点实现该接口
        ```java
        
            mUILoader.setOnRetryClickListener(this);

            @Override
            public void onRetryClick() {
                //网络不佳后的重试
                if (mRecommendPresenter != null) {
                    mRecommendPresenter.getRecommendList();
                }
            }
        ```
---
进——>视频数：15/138; 内存量：946.6mb/5.4g>>>17.12% + 559.3（24）
---

### UILoader的加载页面设计（p16）
- 重新编写fargment_loading_view.xml文件
- 加载中的图片为自定义控件
    - 继承自ImageView
    
### UILoader的内容为空设计(p17)
- 重新编写fargment_empty_view.xml文件

### 推荐页面跳转到详情页面（p18)
- 新建详细页面
    - 编写基类统一activity
    - 设置状态栏透明
    - 设置状态栏的可见性
    ```java
        getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION);
        getWindow().setStatusBarColor(Color.TRANSPARENT);
    ```
- 设计点击Item事件接口
- 设置接口函数（传入实现该接口得对象）
- 接口函数为点击后传入点击对象得tag作为索引
- 当Item被点击时，调用传入对象得接口函数
- 在推荐页面中实现该接口
### 详情页面加载图片和设置标题(p19)
- 定义详细数据接口
    - 注册或取消详细页面UI的回调函数
    - 下拉刷新
    - 上拉加载更多
    - 获取该歌单下的曲目
- 实现该接口
    - 该类设计为单例模式-懒汉式
    - 添加函数-设置内部的数据即通过它从推荐首页传入数据
- 定义获取数据成功回调接口
    * 获取详细数据后
    * 获取该歌单的曲目后
- 详情页面实现该接口
- 推荐页面在跳转前获取详情数据的实例设值当前点击的Item的数据
- 详情页面初始化时获取单例数据请求对象并注册UI回调函数
- 当注册UI回调时，判断Album数据是否存在，存在即调用回调对象的AlbumLoaded通知UI更新
- UI回调函数更新UI
- 编写详细数据的layout文件

### app图标和清单文件警告(p20)
- 设置app图标-android:icon="@mipmap/logo"
- 警告原因:sdk超过26之后需要添加- <action android:name="android.intent.action.VIEW"\/>

### 图片的高斯模糊毛玻璃效果（p21）
- 工具类-实现图片模糊
    ```java
    package com.zhangtao.himalaya.utils;

    import android.content.Context;
    import android.graphics.Bitmap;
    import android.graphics.drawable.BitmapDrawable;
    import android.renderscript.Allocation;
    import android.renderscript.Element;
    import android.renderscript.RenderScript;
    import android.renderscript.ScriptIntrinsicBlur;
    import android.widget.ImageView;

    /**
    * 设置图片的毛玻璃效果
    */
    public class ImageBlur {

        public static void makeBlur(ImageView imageview, Context context) {
            BitmapDrawable drawable = (BitmapDrawable) imageview.getDrawable();
            Bitmap bitmap = drawable.getBitmap();
            Bitmap blurred = blurRenderScript(bitmap, 13, context); //second parametre is radius max:25
            imageview.setImageBitmap(blurred); //radius decide blur amount
        }


        private static Bitmap blurRenderScript(Bitmap smallBitmap, int radius, Context context) {
            smallBitmap = RGB565toARGB888(smallBitmap);
            Bitmap bitmap = Bitmap.createBitmap(smallBitmap.getWidth(), smallBitmap.getHeight(), Bitmap.Config.ARGB_8888);
            RenderScript renderScript = RenderScript.create(context);
            Allocation blurInput = Allocation.createFromBitmap(renderScript, smallBitmap);
            Allocation blurOutput = Allocation.createFromBitmap(renderScript, bitmap);
            ScriptIntrinsicBlur blur = ScriptIntrinsicBlur.create(renderScript, Element.U8_4(renderScript));
            blur.setInput(blurInput);
            blur.setRadius(radius); // radius must be 0 < r <= 25
            blur.forEach(blurOutput);
            blurOutput.copyTo(bitmap);
            renderScript.destroy();
            return bitmap;

        }

        private static Bitmap RGB565toARGB888(Bitmap img) {
            int numPixels = img.getWidth() * img.getHeight();
            int[] pixels = new int[numPixels];

            //Get JPEG pixels.  Each int is the color values for one pixel.
            img.getPixels(pixels, 0, img.getWidth(), 0, 0, img.getWidth(), img.getHeight());

            //Create a Bitmap of the appropriate format.
            Bitmap result = Bitmap.createBitmap(img.getWidth(), img.getHeight(), Bitmap.Config.ARGB_8888);

            //Set RGB pixels.
            result.setPixels(pixels, 0, result.getWidth(), 0, 0, result.getWidth(), result.getHeight());
            return result;
        }
    }
    ```
- 由于Picasso加载图片是异步的所以要判断加载图片是否成功，因此new Picasso的Callback
    ```java
    //毛玻璃效果
        if (mLargeCover != null) {
            Picasso.with(this).load(album.getCoverUrlLarge()).into(mLargeCover, new Callback() {
                @Override
                public void onSuccess() {

                    Drawable drawable = mLargeCover.getDrawable();
                    if(drawable != null){//判断该控件是否已存在
                        ImageBlur.makeBlur(mLargeCover, DetailActivity.this);
                    }
                }

                @Override
                public void onError() {
                    LogUtil.d(TAG, "onError...");
                }
            });
        }
    ```
### 使用drawable实现订阅按钮(p22)
- 编辑详情页面的layout
- 使用drawable实现订阅按钮
    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <shape xmlns:android="http://schemas.android.com/apk/res/android">
    <size android:width="75dp"
        android:height="30dp"/>

        <solid  android:color="#f97254"/>

        <corners android:radius="15dp"/>
    </shape>
    ```
- TextView中的文字居中- android:gravity="center"

### 再写详情内容的布局（p23)
- 再写详情内容layout

### 获取专辑的详细内容（p24)
- 查看SDK文档

