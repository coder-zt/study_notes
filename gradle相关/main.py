import os
import zipfile
import time
import datetime

basePath = "/Users/edy/Downloads/new/transforms"

jar2DexPath = "/Users/edy/Android/utils/dex-tools-v2.4/d2j-jar2dex.sh"

androidProjectPath = "/Users/edy/Android/53BX/Android_53helper/app/build/intermediates"

def isIndependentFile(name):
    return name != ".DS_Store"

def addBasePath(path, name):
    return path  + "/"+ name

def getChildren(path):
    childeren = os.listdir(path)
    filterList = filter(isIndependentFile, childeren)
    pathList = []
    for i in filterList:
        pathList.append(path)
    return list(map(addBasePath, pathList, filter(isIndependentFile, childeren)))

def get_creation_time(file_path):
    creation_time = os.path.getctime(file_path)
    return creation_time

def format_time(timestamp):
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    # 将datetime对象格式化为字符串，精确到毫秒
    time_string = dt_object.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return time_string



def findDexOrJar(path, count):
    children =  getChildren(path)
    for child in children:
        if os.path.isdir(child):
            findDexOrJar(child, count)
        else:
            if child.endswith(".dex") and "mergeProjectDexDebug" in child:
                print(child)
            

findDexOrJar(androidProjectPath, 0)

pluginChildren =  getChildren(basePath)
for pluginChild in pluginChildren:
    # print("pluginChild  ===> " + pluginChild + "/debug")
    pluginDebugChild = pluginChild + "/debug"
    nextChildren = getChildren(pluginDebugChild)
    for next in nextChildren:
        # print(next)
        if str(next).endswith(".jar"):
            jarPath = next
            # print("jarPath  ===> " + jarPath)
            zipFile = zipfile.ZipFile(jarPath, "r")
            zipChildren = zipFile.namelist()
            for i in zipChildren:
                if i.startswith("com/baidu/mapapi"):
                    
                    createTime = get_creation_time(jarPath)
                    timeStr = format_time(createTime)
                    print(jarPath + " : " + timeStr)
                    
        
