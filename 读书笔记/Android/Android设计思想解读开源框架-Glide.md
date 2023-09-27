# Glide 原理分析(p386)

## 1.1 基本用法(p386)

- Picasso 比 Glide 更加简洁和轻量，Glide 比 Picasso 功能更为丰富。

```java
// 使用glide加载一张网络图片
    viewBinding.btnGet.click {
        val url = "http://cn.bing.com/az/hprichbg/rb/Dongdaemun_ZH-CN10736487148_1920x1080.jpg"
        Glide.with(this).load(url).into(viewBinding.acivImage)
    }
```

1. 首先是 with 接收 Context 参数，例如 Activity\Fragment\ApplicationContext,使得图片加载过程会与 Context 的生命周期一样长
2. 再者是 load(),可以接收图片的很多来源，例如：括网络图片、本地图片、应用资源、二进制流、Uri 对象等等
3. 最后就是 into(),将图片资源放入到对应的 ImageView 中

## 1.2 扩展内容

```java
//占位图
.placeholder()
// 注：再此测试加载网络图片会发现加载图片很快，是因为Glide已经缓存下该图片

// 禁用Glide的缓存功能
.diskCacheStrategy(DiskCacheStrategy.NONE)
// 异常占位图
.error()

// 指定图片格式:Glide可以自动判断图片格式，可以加载GIF动图
.asBitmap()
// 如果传入静态图片会加载报错
.asGif()

// 指定加载图片大小
.override(100,100)
```

# 1.3 从源码的角度理解 Glide 的执行流程

- 如何阅读源码

  > 抽丝剥茧、点到即止。应该认准一个功能点，然后去分析这个功能点是如何实现的。但只要去追寻主体的实现逻辑即可，千万不要试图去搞懂每一行代码都是什么意思，那样很容易会陷入到思维黑洞当中，而且越陷越深。因为这些庞大的系统都不是由一个人写出来的，每一行代码都想搞明白，就会感觉自己是在盲人摸象，永远也研究不透。如果只是去分析主体的实现逻辑，那么就有比较明确的目的性，这样阅读源码会更加轻松，也更加有成效。

- 源码下载

> https://github.com/bumptech/glide/tree/v3.7.0

- 开始阅读

1.  with():RequestManager

    该函数可以传入 Context、Activity、Fragment 等等参数，当传入的 Context 是 Application 时，直接通过 getApplicationManager()来获取 RequestManager;如果是其他类型则会向当前的 Activity 添加一个隐藏的 Fragment，并且创建 RequestManager。前后区别是前者的生命周期就是这个应用程序的生命周期，而后者就是 Activity 的生命周期，所以需要添加一个隐藏的 Fragment 来获取到生命周期的变化

    ```java

        /**
         * 使用RequestManagerFragment创建RequestManager,使得RequestManager可以获取到
         * Activity的生命周期变化
         */
        RequestManager fragmentGet(Context context, android.app.FragmentManager fm) {
            RequestManagerFragment current = getRequestManagerFragment(fm);
            RequestManager requestManager = current.getRequestManager();
            if (requestManager == null) {
                // 创建RequestManager
                requestManager = new RequestManager(context, current.getLifecycle(), current.getRequestManagerTreeNode());
                current.setRequestManager(requestManager);
            }
            return requestManager;
        }

        /**
          * 创建RequestManagerFragment，添加到activity中
         */
        RequestManagerFragment getRequestManagerFragment(final android.app.FragmentManager fm) {
            RequestManagerFragment current = (RequestManagerFragment) fm.findFragmentByTag(FRAGMENT_TAG);
            if (current == null) {
                current = pendingRequestManagerFragments.get(fm);
                if (current == null) {
                    current = new RequestManagerFragment();
                    pendingRequestManagerFragments.put(fm, current);
                    fm.beginTransaction().add(current, FRAGMENT_TAG).commitAllowingStateLoss();
                    handler.obtainMessage(ID_REMOVE_FRAGMENT_MANAGER, fm).sendToTarget();
                }
            }
            return current;
        }
    ```

2.  RequestManager.<strong>load()</strong>:DrawableTypeRequest\<String>(p411)

    load()只有一行代码：(DrawableTypeRequest<String>) fromString().load(string);，fromString()通过调用 loadGeneric(String.class)方法，生成传入参数对应的 ModelLoader，并使用该 ModelLoader 创建了 DrawableTypeRequest

    Q:optionsApplier.apply()的作用?

    ```java

    public DrawableTypeRequest<String> load(String string) {
        return (DrawableTypeRequest<String>) fromString().load(string);
    }

    public DrawableTypeRequest<String> fromString() {
        return loadGeneric(String.class);
    }

    private <T> DrawableTypeRequest<T> loadGeneric(Class<T> modelClass) {
        ModelLoader<T, InputStream> streamModelLoader = Glide.buildStreamModelLoader(modelClass, context);
        ModelLoader<T, ParcelFileDescriptor> fileDescriptorModelLoader =
                Glide.buildFileDescriptorModelLoader(modelClass, context);
        if (modelClass != null && streamModelLoader == null && fileDescriptorModelLoader == null) {
            throw new IllegalArgumentException("Unknown type " + modelClass + ". You must provide a Model of a type for"
                    + " which there is a registered ModelLoader, if you are using a custom model, you must first call"
                    + " Glide#register with a ModelLoaderFactory for your custom model class");
        }

        return optionsApplier.apply(
                new DrawableTypeRequest<T>(modelClass, streamModelLoader, fileDescriptorModelLoader, context,
                        glide, requestTracker, lifecycle, optionsApplier));
    }
    ```

    DrawableTypeRequest 继续调用 load()方法，而自身没有 load()方法，而是在其父类
    DrawableTypeRequestBuilder 中,DrawableTypeRequest 中有 asGif()、asBitmap()、downloadOnly(),则会转化成目标类型 <font color="red">TypeRequest</font>对象

    ```java
        public BitmapTypeRequest<ModelType> asBitmap() {
             return optionsApplier.apply(new BitmapTypeRequest<ModelType>(this, streamModelLoader,
                     fileDescriptorModelLoader, optionsApplier));
         }

         public GifTypeRequest<ModelType> asGif() {
             return optionsApplier.apply(new GifTypeRequest<ModelType>(this, streamModelLoader, optionsApplier));
         }

         public <Y extends Target<File>> Y downloadOnly(Y target) {
             return getDownloadOnlyRequest().downloadOnly(target);
         }

         public FutureTarget<File> downloadOnly(int width, int height) {
             return getDownloadOnlyRequest().downloadOnly(width, height);
         }

         private GenericTranscodeRequest<ModelType, InputStream, File> getDownloadOnlyRequest() {
             return optionsApplier.apply(new GenericTranscodeRequest<ModelType, InputStream, File>(File.class, this,
                     streamModelLoader, InputStream.class, File.class, optionsApplier));
         }
    ```

    调用父类的 load()则会返回 DrawableTypeRequestBuilder(),而第三步调用的 into()就是该对象的方法，因此到此 load()部分结束，在 DrawableTypeRequestBuilder 提供了很多 api,例如
    placeholder()方法、error()方法、diskCacheStrategy()方法、override()方法等等，丰富了加载图片的功能。

    Q: 分析这些 API 的具体实现？

3.  DrawableRequestBuilder.<strong>into()</strong>:Target\<GlideDrawable>(p429)

    与 DrawableTypeRequest 相同，into()的具体实现也是在其父类中，先只关注最后一行，其调用了重载方法 into(),但是参数类型是 Target,所以具体关注<strong>glide.buildImageViewTarget(view, transcodeClass)</strong>

    ```java
        public Target<TranscodeType> into(ImageView view) {
            Util.assertMainThread();
            if (view == null) {
                throw new IllegalArgumentException("You must pass in a non null View");
            }

            if (!isTransformationSet && view.getScaleType() != null) {
                switch (view.getScaleType()) {
                    case CENTER_CROP:
                        applyCenterCrop();
                        break;
                    case FIT_CENTER:
                    case FIT_START:
                    case FIT_END:
                        applyFitCenter();
                        break;
                    //$CASES-OMITTED$
                    default:
                        // Do nothing.
                }
            }

            return into(glide.buildImageViewTarget(view, transcodeClass));
        }

    ```

    ```java
        <R> Target<R> buildImageViewTarget(ImageView imageView, Class<R> transcodedClass) {
            return imageViewTargetFactory.buildTarget(imageView, transcodedClass);
        }

        public class ImageViewTargetFactory {

            @SuppressWarnings("unchecked")
            public <Z> Target<Z> buildTarget(ImageView view, Class<Z> clazz) {
                if (GlideDrawable.class.isAssignableFrom(clazz)) {
                    return (Target<Z>) new GlideDrawableImageViewTarget(view);
                } else if (Bitmap.class.equals(clazz)) {
                    return (Target<Z>) new BitmapImageViewTarget(view);
                } else if (Drawable.class.isAssignableFrom(clazz)) {
                    return (Target<Z>) new DrawableImageViewTarget(view);
                } else {
                    throw new IllegalArgumentException("Unhandled class: " + clazz
                            + ", try .as*(Class).transcode(ResourceTranscoder)");
                }
            }

        }
    ```

    在 DrawableRequestBuilder 初始化中，transcodedClass 参数默认是 GlideDrawable.class，因此这里会返回<strong>GlideDrawableImageViewTarget</strong>,如果调用 asBitmap,则这个参数将是 Bitmap.class,返回 BitmapImageViewTarget，接着就是 into 的另一个重载方法<Y extends Target\<TranscodeType>> Y into(Y target)

    ```java
      public <Y extends Target<TranscodeType>> Y into(Y target) {
        Util.assertMainThread();
        if (target == null) {
        throw new IllegalArgumentException("You must pass in a non null Target");
        }
        if (!isModelSet) {
        throw new IllegalArgumentException("You must first set a model (try #load())");
        }

        Request previous = target.getRequest();

        if (previous != null) {
        previous.clear();
        requestTracker.removeRequest(previous);
        previous.recycle();
        }

        Request request = buildRequest(target);
        target.setRequest(request);
        lifecycle.addListener(target);
        requestTracker.runRequest(request);

        return target;
    }
    ```

    在该 into()主要创建了 Request,并调用 runRequest 来请求数据

    Request 的创建过程：

    Request 的请求过程：

    Responsible for starting loads and managing active and cached resources.

    负责启动加载并管理活动资源和缓存资源

## 从 Engine 的 load()看 glide 的网络加载过程

- 包名：com.bumptech.glide.load.engine

1. Engine

   1. load()

   ```java
       // 根据参数获取EngineKey，然后去内存中查找对应的Resource,没有则使用线程加载数据
       EngineKey key = keyFactory.buildKey(...);
       EngineResource<?> memoryResource;
       synchronized (this) {
       memoryResource = loadFromMemory(key, isMemoryCacheable, startTime);

       if (memoryResource == null) {
           // 使用线程加载数据
           return waitForExistingOrStartNewJob(...);
       }
       }
       cb.onResourceReady(emoryResource, DataSource.MEMORY_CACHE, false)
       return null;
   ```

   2. waitForExistingOrStartNewJob()

   ```java
     private <R> LoadStatus waitForExistingOrStartNewJob(...) {
       // 检查是否有对应的加载数据的线程，有则直接返回
       EngineJob<?> current = jobs.get(key, onlyRetrieveFromCache);
       if (current != null) {
       current.addCallback(cb, callbackExecutor);
       if (VERBOSE_IS_LOGGABLE) {
           logWithTimeAndKey("Added to existing load", startTime, key);
       }
       return new LoadStatus(cb, current);
       }

   // 线程池
   EngineJob<R> engineJob = engineJobFactory.build(...);
   // 线程
   DecodeJob<R> decodeJob =
       decodeJobFactory.build(...);

   jobs.put(key, engineJob);

   engineJob.addCallback(cb, callbackExecutor);
   // 执行decodeJob线程
   engineJob.start(decodeJob);

   if (VERBOSE_IS_LOGGABLE) {
     logWithTimeAndKey("Started new load", startTime, key);
   }
   return new LoadStatus(cb, engineJob);
   }

   ```

2. EngineJob

   1. start()

   ```java
   // 使用对应的线程池来执行decodeJob,重点就在DecodeJob的run()
     public synchronized void start(DecodeJob<R> decodeJob) {
        this.decodeJob = decodeJob;
        GlideExecutor executor =
            decodeJob.willDecodeFromCache() ? diskCacheExecutor : getActiveSourceExecutor();
        executor.execute(decodeJob);
   }
   ```

3. DecodeJob

   1. run()

   ```java
        @Override
       public void run() {
           GlideTrace.beginSectionFormat("DecodeJob#run(reason=%s, model=%s)", runReason, model);
           DataFetcher<?> localFetcher = currentFetcher;
           try {
           // 执行加载任务
           runWrapped();
           } catch (CallbackException e) {
           throw e;
           } catch (Throwable t) {
               ...
           } finally {
           if (localFetcher != null) {
               localFetcher.cleanup();
           }
           GlideTrace.endSection();
           }
       }
   ```

   2. runWrapped()

   ```java
        // runReason = RunReason.INITIALIZE;
     private void runWrapped() {
       switch (runReason) {
       case INITIALIZE:
            // stage = Stage.DATA_CACHE
            // currentGenerator = new DataCacheGenerator(decodeHelper, this)
           stage = getNextStage(Stage.INITIALIZE);
           currentGenerator = getNextGenerator();
           runGenerators();
           break;
       case SWITCH_TO_SOURCE_SERVICE:
           runGenerators();
           break;
       case DECODE_DATA:
           decodeFromRetrievedData();
           break;
       default:
           throw new IllegalStateException("Unrecognized run reason: " + runReason);
       }
   }
   ```

   3. runGenerators()

   ```java
     private void runGenerators() {
        currentThread = Thread.currentThread();
        startFetchTime = LogTime.getLogTime();
        boolean isStarted = false;
        while (!isCancelled
            && currentGenerator != null
            && !(isStarted = currentGenerator.startNext())) {
        stage = getNextStage(stage);
        currentGenerator = getNextGenerator();

        if (stage == Stage.SOURCE) {
            reschedule(RunReason.SWITCH_TO_SOURCE_SERVICE);
            return;
        }
        }
        // We've run out of stages and generators, give up.
        if ((stage == Stage.FINISHED || isCancelled) && !isStarted) {
            notifyFailed();
        }
    }

   ```

   ```java
        // 初始阶段
        runReason = RunReason.INITIALIZE
        stage = Stage.INITIALIZE
        // 执行runWrapped()
        runWrapped()
        stage = Stage.RESOURCE_CACHE
        currentGenerator =new ResourceCacheGenerator()
        // 执行runGenerators()
        runGenerators()
        // 第一次循环：currentGenerator(ResourceCacheGenerator).startNext()：如果能找到本地的缓存则结束本次数据加载
        // 本地缓存中没有找到对应的数据
        stage = Stage.DATA_CACHE
        currentGenerator = new DataCacheGenerator()
        // 第二次循环：currentGenerator(DataCacheGenerator).startNext()：同样是在本地缓存中查找数据
        // 本地缓存中没有找到对应的数据
        stage = Stage.SOURCE
        currentGenerator = new SourceGenerator()
        // 第二次循环：currentGenerator(SourceGenerator).startNext()：

   ```

   DECODE_DATA

   MultiModelLoader

, randStr: String, ticket: String
