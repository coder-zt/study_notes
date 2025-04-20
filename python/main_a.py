content = '''
    toolDeps = [
            channel            : "com.leon.channel:helper:2.0.3",                            // vasDolly多渠道打包获取渠道信息
            ok2curl            : "com.github.mrmike:ok2curl:0.6.0",
            liteAdapter        : "com.github.yu1tiao:LiteAdapter:1.1.4",
            toastUtil          : 'com.hjq:toast:8.6',
            startup            : 'com.rousetime.android:android-startup:1.0.6',
            xlog               : "com.elvishew:xlog:1.6.1",
            utilCode           : "com.blankj:utilcodex:1.31.1",
            mmkv               : "com.tencent:mmkv-static:1.1.1",
            timber             : "com.jakewharton.timber:timber:4.7.1",
            agentweb           : "com.just.agentweb:agentweb:4.1.3",

            wm_router          : "com.sankuai.waimai.router:router:1.2.0",
            wm_router_compiler : "com.sankuai.waimai.router:compiler:1.2.0",

            kefu_sdk           : "com.easemob:kefu-sdk-lite:1.3.3.0",

            zxing              : "com.google.zxing:core:3.3.3",
            barcodescanner     : "me.dm7.barcodescanner:zxing:1.9.13",

//            rxdownload        : "com.github.ssseasonnn:RxDownload:1.1.3",
//            rxdownload_manager : "com.github.ssseasonnn.RxDownload:rxdownload4-manager:1.1.3",
//            rxdownload_notification : "com.github.ssseasonnn.RxDownload:rxdownload4-notification:1.1.3",
//            rxdownload_recorder : "com.github.ssseasonnn.RxDownload:rxdownload4-recorder:1.1.3",

            okdownload         : "com.liulishuo.okdownload:okdownload:1.0.7",
            okdownload_sqlite  : "com.liulishuo.okdownload:sqlite:1.0.7",
            okdownload_http    : "com.liulishuo.okdownload:okhttp:1.0.7",

            findbugsAnnotations: "com.google.code.findbugs:annotations:3.0.1",

            litepal            : "org.litepal.guolindev:core:3.2.3",

            gifDrawable        : "pl.droidsonroids.gif:android-gif-drawable:1.2.19",
            svgaPlayer        : "com.github.yyued:SVGAPlayer-Android:2.5.12",

            notchfit           : "com.wcl.notchfit:notchfit:1.4.2",             //  刘海适配工具
            fastJson           : "com.alibaba:fastjson:1.2.76",
            agcp               : "com.huawei.hms:scan:2.12.0.300"
    ]
'''

res = content.split("\n")
print(len(res))
for r in res:
    if len(r) <= 0:
        continue
    if ":" not in r:
        continue
    print(r)
    lineRes = r.split(":")
    packName  = lineRes[0]
    packPath  = lineRes[1]
    print(packName + "<<<<:>>>>" + packPath)