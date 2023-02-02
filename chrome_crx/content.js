

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    console.log("content.js")
    if (request.action == "getText");
    {
        // var result = document.all[0].body; // innerText
        sendResponse({ "title": document.title, "result": document.all[0].outerHTML });
        createAndDownloadFile("ceshi.html", document.all[0].outerHTML)

        for (var img in document.images) {
            console.log("imgs:" + document.images[img].src);
            download(document.images[img].src, document.images[img].alt)
        }
    }
});

/**
 * 创建并下载文件
 * @param  {String} fileName 文件名
 * @param  {String} content  文件内容
 */
function createAndDownloadFile(fileName, content) {
    var aTag = document.createElement('a');
    var blob = new Blob([content]);
    aTag.download = fileName;
    aTag.href = URL.createObjectURL(blob);
    aTag.click();
    URL.revokeObjectURL(blob);
}

function download(url, name) {
    const aLink = document.createElement('a')
    aLink.download = name
    aLink.href = url
    aLink.dispatchEvent(new MouseEvent('click', {}))
}

chrome.webRequest.onBeforeRequest.addListener(
    function (details) {
        console.log("onBeforeRequest")
        for (var i = 0, headerLen = details.requestHeaders.length;
            i < headerLen; ++i) {
        }
        return { requestHeaders: details.requestHeaders };
    },
    {
        urls: [
            "<all_urls>"
        ]
    },
    [
        "blocking",
        "requestHeaders"
    ]
);