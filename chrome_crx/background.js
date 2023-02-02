chrome.action.onClicked.addListener((tab) => {
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ['content.js'],
    });


    // chrome.scripting.executeScript(tab.id, { file: "content.js" }, function () {
    //     sendMessage(tab.id);
    // });
    // // chrome.tabs.query可以通过回调函数获得当前页面的信息tabs
    //     chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    //     // 发送一个copy消息出去
    //     sendMessage(tabs[0].id)
    //     }); 



    console.log("tab ===> ")
    console.log(chrome.tabs)
    console.log("tab <=== ")
    if (tab.url?.startsWith("chrome://")) return undefined;
    sendMessage(tab.id)
    console.log("hello")
});


function sendMessage(tabid) {
    console.log("tabid ====> " + tabid)
    chrome.tabs.sendMessage(tabid, { action: "getText" }, function (respond) {
        console.log("sendMessage ====> " )
        console.log(respond)
        // createAndDownloadFile("ceshi.txt", respond)
        console.log("sendMessage ====> " )
        // var formatStr = respond.content;
        //此处通过http发起服务端请求,将content写入自己的数据库或文件
    });
}


// chrome.webRequest.onBeforeRequest.addListener(
//     function (details) {
//         console.log("onBeforeRequest")
//         for (var i = 0, headerLen = details.requestHeaders.length;
//             i < headerLen; ++i) {
//         }
//         return { requestHeaders: details.requestHeaders };
//     },
//     {
//         urls: [
//             "<all_urls>"
//         ]
//     },
//     [
//         "blocking",
//         "requestHeaders"
//     ]
// );
