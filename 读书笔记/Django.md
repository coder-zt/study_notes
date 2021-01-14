# 第一章 Django建站基础
- 创建一个项目及一个网站
    
    * django-admin startproject [项目名称]

- 一个页面或多个页面相当于一个App，因此先要创建App
    
    * python manage.py startapp [appName]
     
- 将整个服务器程序运行起来

    * python manage.py runserver [port]

# 第二章 Django配置信息

## 基本配置信息

- 配置信息主要由项目的settings.py实现，主要配置有项目路径、密钥配置、域名访问权限、App列表、配置静态资源、配置模板文件、数据库配置、中间件和缓存配置。

## 静态资源

- STATIC_URL = '/static/'
- 包括CSS文件、JavaScript文件以及图片等资源文件
- 静态资源在每个App的static文件夹下

- 配置根目录下的静态文件夹-STATCFILE_DIRS
- STATICFILES_DIRS = [os.path.join(BASE_DIR, 'public_static')]
    * http://127.0.0.1:81/static/public_avater.png //虽然文件夹名称市public_static但路径中是static
    * http://127.0.0.1:81/static/avater.png
- 前者必须配置且不能为空，或者则不用

- STATIC_ROOT
    * 方便服务部署，存放整个项目的静态文件-生产部署
    * STATIC_ROOT = os.path.join(BASE_DIR, 'all_static')

## 模板路径

- 模板及MTV中的T，是一些Html文件，它在文档中写了一些关键变量的指示符，通过解析出这些变量然后赋值做成动态的网页
- 在每个app中的templates中和根目录中也有一个templates文件存放一些公共的模板,如html的head部分
- 配置
    * setting -> TEMPLATES
    * BACKEND:解析指示符的引擎
    * DIRS:模板路径
    * APP_DIRS:是否在App里查找模板文件
    * OPTIONS:一些设置.一般不用修改

## 数据库配置
- Django除了支持PostgreSQL、Sqlite3、MySQL和Oracle之外，还支持SQLServer和MongoDB的连接。

    ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'danjgo_db',
                'USER': 'root',
                'PASSWORD': '123456',
                'HOST': '127.0.0.1',
                'POST': '3306',
            },
            'my_sqlite': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
    ```

- 因为mysql 8.0版本修改了密码的验证方式，所以会报错 ---> django.db.utils.OperationalError:
- 修改为低版本的方式
- 登录mysql
- use mysql;
- alter user 'root'@'localhost' identified with mysql_native_password by '123456';
- flush privileges;
- 查看
-  select user,plugin from user where user='root';
- 数据库必须创建一个新的数据库（已经有的会报错）

# 中间件

- 当Django接收到用户请求时，Django首先经过中间件处理请求信息，执行相关的处理，然后将处理结果返回给用户
- 中间件介绍：
    * SecurityMiddleware：内置的安全机制，保护用户与网站的通信安全。
    * SessionMiddleware：会话Session功能。
    * LocaleMiddleware：支持中文语言。//添加了会报错
    * CommonMiddleware：处理请求信息，规范化请求内容。
    * CsrfViewMiddleware：开启CSRF防护功能。
    * AuthenticationMiddleware：开启内置的用户认证系统。
    * MessageMiddleware：开启内置的信息提示功能。
    * XFrameOptionsMiddleware：防止恶意程序点击劫持。

```python
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]  
```

# 第三章 编写URL规则


## 1.编写URL规则

- 一个url的完整路径是由根目录的urls.py和App中的urls.py共同决定的，前者将分发到每个App中“appName/”,再由或者分发到指定的处理函数中

    ```python
    # 根目录
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('index.urls')), # 分发到app的urls.py中
    ]
    # app
    urlpatterns = [
        path('', views.index),# 分发到具体的方法中
    ]
    ```

## 2. 带变量的URL

- 变量类型
    * 字符类型:匹配任何非空字符串，但不含斜杠。如果没有指定类型，默认使用该类型。
    * 整型:匹配0和正整数。
    * slug:可理解为注释、后缀或附属等概念，常作为URL的解释性字符。
    * uuid:匹配一个uuid格式的对象。
    ```python
        path('<year>/<int:month>/<slug:day>', views.getDate),
        # 利用正则表达式来匹配路径 (?P<variableName>'re表达式')
        re_path('(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2}).html', views.getDate),
    ```

## 3.设置参数的name
- 将url以型的方式保存为变量name,然后利用{% 'name' param1 param2 %} | html中生成新的url,可以作为锚点
```python
    # urls.py
    re_path('(?P<year>[0-9]{4})/(?P<month>[0-9]{2}).html', views.getYear, name="myyear"),
    # views.py
    def getYear(request, year, month):
        return render(request, 'myyear.html')
    
    # myyear.html
    '''
    <!DOCTYPE html>
    <html lang="zh-CN">
        <head>
            <meta charset="UTF-8"/>
            <title>Title</title>
        </head>
        <body>
            <div><a href="/2018.html">2018 old Archive</a></div>
            <div><a href="{% url 'myyear' 2018 12%} | >{% url 'myyear' 2018 12%} | Archive</a></div>
        </body>
    </html>
    '''
```
## 4. 设置额外的参数

- urls分发至views的函数是可以传递一个字典参数给views的方法，而且字典参数会作为函数的参数传入
- views中render函数参数，直接可以将字典参数中的数据传递给html中
- html中邦定数据使用“{{paramName}}”

```python
    # urls.py
    re_path('(?P<year>[0-9]{4})/(?P<month>[0-9]{2}).html', views.getYear,{'day': 211}, name="myyear")

    # views.py
    def getYear(request, year, month, day):
        return render(request, 'myyear.html', {'month': 22, 'day': day})
    # myyear.html
    '''
    <!DOCTYPE html>
    <html lang="zh-CN">
        <head>
            <meta charset="UTF-8"/>
            <title>Title</title>
        </head>
        <body>
            <div><a href="/2018.html">2018 {{month}} - {{day}} old Archive</a></div>
         <div><a href="{% url 'myyear' 2018 12 %} | >{% url 'myyear' 2018 12%} | Archive</a></div>
        </body>
    </html>
    '''
```

# 第四章 探索视图

- 视图（View）是Django的MTV架构模式的V部分
- 主要负责处理用户请求和生成相应的响应内容，然后在页面或其他类型文档中显示。
- 也可以理解为视图是MVC架构里面的C部分（控制器），主要处理功能和业务上的逻辑。

## 1.构建网页内容

- 响应类型

响应类型 | 说明
|---|---|
HttpResponse('Hello world) | HTTP状态码200，请求已成功被服务器接收
HttpResponseRedirect('/admin/') | HTTP状态码302，重定向Admin站点的URL
HttpResponsePermanentRedirect('/admin/') | HTTP状态码301，永久重定向Admin站点的URL
HttpResponseBadRequest('BadRequest') | HTTP状态码400，访问的页面不存在或者请求错误
HttpResponseNotFound(NotFound') | HTTP状态码404，网页不存在或网页的URL失效
HttpResponseForbidden('NotFound') | HTTP状态码403，没有访问权限
HttpResponseNotAllowed('NotAllowed') | HTTP状态码405，不允许使用该请求方式
HttpResponseServerError('ServerError') | HTTP状态码500，服务器内容错误

- render()函数
    * 必要参数： request、template_name
    * request：浏览器向服务器发送的请求对象，包含用户信息、请求内容和请求方式等。
    * template_name：HTML模板文件名，用于生成HTML网页。
    * context：对HTML模板的变量赋值，以字典格式表示，默认情况下是一个空字典。
    * content_type：响应数据的数据格式，一般情况下使用默认值即可。
    * status：HTTP状态码，默认为200。
    * using：设置HTML模板转换生成HTML网页的模板引擎。

- redirect()函数
    * 用于实现请求重定向，重定向的链接以字符串的形式表示，链接的地址信息可以支持相对路径和绝对路径。

```python
# render（）的使用
return render(resquest, 'index.html', context={"title": "首页"}， status=500)
# 重定向首爷（相对路径）
return redirect('/')
# 重定向首爷（绝对路径）
return redirect('http://127:0.0.1:8000')
```

## 2. 数据可视化

- 与模型（Model）实现数据交互（操作数据库）。
- 读取数据库中的数据进行显示
- 视图相当于一个处理中心，负责接收用户请求，然后根据请求信息读取并处理后台数据，最后生成HTML网页返回给用户。

1. 生成数据容器（在数据库中创建数据表）
```python
#  1.在models,py创建数据对象
class Product(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 50)
    type = models.CharField(max_length = 20)

# 2.创建数据表
# a.根据models.py中的数据对象生成相关的py文件，用于创建数据表
> python manage.py makemigrations
# b.创建数据表
> python manage.py migrate
```

2. 查询数据并渲染html

```python
# 在views.py 中model.py进行交付
def showProduct(request):
    # 查询数据
    typeList = models.Product.objects.values('type').distinct()
    nameList = models.Product.objects.values('name', 'type')
    # 利用数据创建字典
    context = {'title':'首页'，'typeList':typeList, 'nameList':nameList}
    return render(request, 'index.html', context = context, status=200)
    # 使用locals()代替字典
    title = "首页"
    return render(request, 'index.html', context = locals(), status=200)
```

```html
<!-- 创建html模板，供模板引擎解析并填充数据 -->
<!DOCTYPE html>
<html lang="zh-CN">
    <head>
        <meta charset="UTF-8"/>
        <!-- 变量标识符：{{ }} -->
        <title>{{ title }}</title>
    </head>
    <body>
        <ul>
         <!-- 列表渲染：{% for i in list %} | -->
            {% for type in typeList%} |             <li>
                <!-- 字典访问 -->
                <h3>{{ type.type }}</h3>
                    {% for name innameList %} |                         <!-- 条件渲染：{{% if condition%} |  -->
                        {% if name.type == type.type } |                         <span>{{ name.name }}</span>
                        <!-- 条件渲染结束 -->
                        {% edif %} |                     {% endfor } |             </li>
            <!-- 列表渲染结束 -->
            {% endor %} |         </ul>
    </body>
</html>
```
## 3. 获取请求信息

- 所有views.py中的函数都有默认参数--->request，可以通过它获取请求端的信息，然后做出响应

- request的常用属性

属性 | 说明 | 实例
| --- | --- | --- |
COOKIES | 获取客户端(浏览器) Cookie信息 | data = request.COOKIES
FILES | 字典对象，包含所有的上载文件。该字典有三个键: filename为 上传文件的文件名:content-type为上传文件的类型:content为上传文件的原始内容 | file = request.FILES
 GET | 获取GET请求的请求参数，以字典形式存储 | //如{'name': 'TOM'} request.GET.get(name')
 META | 获取客户端的请求头信息，以字典形式存储 | //获取客户端的IP地址 request.META. get('REMOTE_ADDR)
 POST | 获取POST请求的请求参数，以字典形式存储 | //如{'name': 'TOM'}request.POST.get'name')
method | 获取该请求的请求方式(GET或POST请求) | data = request.method
path | 获取当前请求的URL地址 | path = request.path
user | 获取当前请求的用户信息 | //获取用户名name = request.user.username

```python
def methodIsGet(request):
    typeList = models.Product.objects.values('type').distinct()
    nameList = models.Product.objects.values('name', 'type')
    title = request.GET.get('name')
    print(request.method)
    print(request.GET.get('name'))
    return render(request, 'index.html', context = locals(), status=200)
```

## 4.通用视图

- 类别：
    * TemplateView直接返回HTML模板，但无法将数据库的数据展示出来。
    * ListView能将数据库的数据传递给HTML模板，通常获取某个表的所有数据。
    * DetailView能将数据库的数据传递给HTML模板，通常获取数据表的单条数据

- ListView实例
```python
# views.py
class ProductList(ListView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nameList'] =  models.Product.objects.values('name', 'type')
        print("context==============")
        print(context)
        print(kwargs)
        print("context==============")
        return context

    def get_queryset(self):
        print(self.kwargs['id'])
        print(self.kwargs['name'])
        print(self.kwargs)
        print(self.request.method)
        return models.Product.objects.values('type').distinct()

    # urls.py
    path('index/<id>.html', views.ProductList.as_view(), {'name':'phone'})
```

# 第五章 深入模板

- Django作为Web框架，需要一种很便利的方法去动态地生成HTML网页。而模板就是为了方便生成Html

- 模板
    * HTML的部分代码
    * 一些特殊的语法

## 1. 变量与标签

- 变量是模板中最基本的组成单位，**模板变量**是由**视图函数**生成的
- {{ variable }} 绑定变量，也可是字典或对象通过"."访问
- {% %} 标签标识符，其种类如下：

    标签 | 描述
    | :-:| :-|
    {% for %} | 遍历输出变量的内容，变量类型应为列表或数据对象
    {% if %} | 对变量进行条件判断
    {% csrf toen %} | 生成csrf token的标签，用于防护跨站请求伪造攻击
    {% url %} | 引用路由配置的地址，生成相应的URL地址
    {% with %} | 将变量名重新命名
    {% load %} | 加载导入Django的标签库
    {% stati %} | 读取静态资源的文件内容
    {% extends xx %} | 模板继承，xxx为模板 文件名，使当前模板继承xxx模板
    {% block xxx %} | 重写父类模板的代码

- for循环的相关变量

    变量 | 描述
    | ---- | --- |
    forloop.counter | 获取当前循环的索引，从1开始计算
    forloop.counter0 | 获取当前循环的索引，从0开始计算
    forloop.revcounter | 索引从最大数开始递减，直到索引到1位置
    forloop.revcounter0 | 索引从最大数开始递减，直到索引到0位置
    forloop.first | 当遍历的元素为第一项时为真
    forloop.last | 当遍历的元素为最后。项时为真
    forloop.parentloop | 在嵌套的for循环中，获取上层for循环的forloop

## 2. 模板继承

- 减少模板之间重复的代码。
- 在base.html中要重写的部分用 {% block xxx %}{% endblock %}标记并名称为xxx
- 继承改base.html {% extends 'base.html' %}
- {% block xxx %}{% endblock %}中加入新html,进而产生新的html

```
<!-- base.html -->
< !DOCTYPE html> 
<html>
    <head> 
        <meta charset=" UTF-8”>
        <title>{{ title }}</title> 
    </head>
    <body> 
        {% block body %} {% endblock %}
    </body>
</html>

<!-- child.html -->
{% extends "base. html" %}
    {% block body %}
    <a href=" {% url'index' %}" target=" blank" >首页</a>
    <h1>Hello Django</h1>
    {% endblock %}

```
## 3.自定义过滤器

- 使用过滤器
    * 多个过滤器： {{ variable|filter|lower }}
    * 过滤器只能传一个参数 ： {{ variable|filter:arg }}

- 内置过滤器

    内置过滤器 | 使用形式 | 说明
    |--- | ---|---|
    add | { value \| add: "2"}} | 将value的值增加2
    addslashes | {{ value \| addslashes } | 在value中的引号前增加反斜线
    capfirst | {{ value \|capfirst }} | value的第个字符转化成大写形式
    cut | {{ value \|cut:arg}} | 从value中删除所有arg的值。如果value是"String with spaces", arg是" "，那么输出"Stringwithspaces"
    date | {{ value \| date:"D d M Y" } | 将日期格式数据按照给定的格式输出
    default | {{ value \| default: "nothing" }} | 如果value的意义是False,那么输出值为过滤器设定的默认值
    default if none | {{ value \| default_ if_none:"nothing"}} | 如果value的意义是None,那么输出值为过滤器设定的默认值
    dictsort | {{ value \| dictsort:"name"}} | 如果value的值是一个列表，里面的元素是字典，那么返回值按照每个字典的关键字排序
    dictsortreversed | {{ value \| dictsortreversed:"name"}} | 如果value的值是一个列表，里面的元素是字典，每个字典的关键字反序排行
    divisibleby | {{ value \| divisibleby:arg}} | 如果valuc能够被arg整除，那么返回值将是True
    escape | {{ value \| escape} } | 控制HTML转义，替换value中的某些HTML特殊字符
    escapejs | {{ value \| escapejs }} | 替换value中的某些字符，以适应JavaScript和JSON格式
    filesizeformat | {{ value \| filesizeformat }} | 格式化value,使其成为易读的文件大小，例如13KB、4.1MB等
    first | {{ value \| first }} | 返回列表中的第一个Item，例如，如果value是列表['a','b','c']，那么输出将是'a'
    floatformat | {{ value \| floatformat }}或{{valuelfloatformat:arg}} | 对数据进行四舍五入处理，参数arg是保留小数位，可以是正数或负数，如{{valuefloatformat:"2" }}是保留两| 位小数。若无参数arg,默认保留1位小数，如{{valuefloatformat}}
    get_digit | {{ value \| get_digit"arg"}} | 如果value是123456789，arg是2， 那么输出的是8
    iriencode | {{ value \| iriencode}} | 如果value中有非ASCI字符，那么将其转化成URL中适合的编码
    join | {{ value \| join:"arg"}} | 使用指定的字符串连接一个list,作用如同Python的strjoin(ist)
    last | {{ value \| last }} | 返回列表中的最后一个Item
    length | {{ value \| length }} | 返回value的长度
    length is | {{value \| length_is:"arg"}} | 如果value的长度等于arg,例如: value是['a','b','c'], arg是3， 那么返回True
    linebreaks | {{value \| linebreaks}} | value中的"\n"将被<br/>替代，并且将整个value使用<p>包围起来，从而适合HTML的格式
    linebreaksbr | {{value \| linebreaksbr}} | value中的"\n"将被<br/>替代
    linenumbers | {{value \| linenumbers}} | 为显示的文本添加行数
    ljust | {{value \| rjust} | 以左对齐方式显示value
    center | {{value \| center}} | 以居中对齐方式显示value
    rjust | {{value \| rjust}} | 以右对齐方式显示value
    lower | {{value \| lower}} | 将一个字符串转换成小写形式
    make list | {{value \| make_list}} | 将value转换成list。例如value是Joel,输出[u'J',u'o',u'e',u'l'];如果value是 123,那么输出是[1,2.3]
    pluralize | {{value \| pluralze}或{{value \| pluralize:" es" }或{{value \| pluralize:"y,ies}} | 将value返回英文复数形式
    random | {{value \| random}} | 从给定的list中返回一个任意的Item
    removetags | {{value \| removetags:"tag1 tag2 tag..."}} | 删除value中tagl tag2...的标签
    safe | {{value \| safe}} | 关闭HTML转义，告诉Django这段代码是安全的，不必转义
    safeseq | {{value \| safeseq }} | 与上述safe基本相同，但有一点不同:safe针对字符串，而safeseq针对多 个字符串组成的sequence
    slice | {{some_list \| slice:":2"}} | 与Python语法中的slice相同，":2” 表示截取前两个字符，此过滤器可用于中文或英文
    slugify | {{value \| slugify}} | 将value转换成小写形式，同时删除所有分单词字符，并将空格变成横线。例如:value是Joel is a slug,那么输出的将是joel-is-a-slug
    striptags | {{value \| striptags}} | 删除value中的所有HTML标签
    time | {{value \| time:" H:i"}或{{value \| time}} | 格式化时间输出，如果time后 面没有格式化参数，那么输出按照默认设置的进行
    truncatewords | {{value \| truncatewords:2}} | 将value进行单词截取处理，参数2代表截取前两个单词，此过滤器只可用于英文截取。如value是Joel is a slug那么输出将是: Joel is
    upper | {{value \| upper}} | 转换一个字符串为大写形式
    urlencode | {{value \| urlencode}} | 将字符串进行URLEncode处理
    urlize | {{value \| urlize}} | 将一个字符串中的URL转化成可点击的形式。如果value 是Check out www.baidu.com,那么输出的将是: Check out <a href="http://www.baidu.com" >www.baidu. com</a>
    wordcount | {{value \| wordcount}} | 返回字符串中单词的数目
    wordwrap | {{value \| wordwrap:5}} | 按照指定长度的分割字符串
    timesince | {{value \| timesince:arg}} | 返回参数arg到value的天数和小时数。如果arg是一个日期实例，表示2006-06-01午夜，而value表示2006- -06- 01早上8点，那么输出结果返回“8 hours”
    timeuntil | {{value \| timeuntil}} | 返回value距离当前日期的天数和小时数

- 自定义过滤器
1. 创建过滤器的目录和文件--->在根目录下或APP目录下创建文件夹并创建初始化文件和templatetags文件夹（名字不能变），然后再该目录下创建过滤程序文件和初始化文件

    ```
    <!-- 文件结构 -->
    user_define
        |- __init__.py
        |_ templatetags
            |- __init__.py
            |_ myfliter.py
    ```

2. 再过滤文件中写过滤器函数
    ```python
    from django import template
    # 声明一个模板对象，注册过滤器
    register = template.Library()
    # 声明并定义过滤器
    @register.filter
    def myplace(value, args):
        old = args.split('：')[0]
        new = args.split('：')[1]
        return value.replace(old, new)
    ```

3. 再设置配置文件中注册改文件夹
    ```python
    # setting.py
    # App列表
    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'index',
        'user',
        'user_define'
    ]
    ```

4. 再静态文件中使用改过滤器
    ```
    <!-- 加载过滤器 -->
    {% load myfliter %}
    <!-- 使用过滤器 -->
    <title>{{ title | myplace:"首：使用了过滤器" }}</title>
    ```

# 第六章 模型与数据库
   
- Django对各种数据库提供了很好的支持，包括：PostgreSQL、MySQL、SQLite和Oracle。
- 为这些数据库提供了统一的调用API，这些API统称为ORM框架。
- 通过使用Django内置的ORM框架可以实现数据库连接和读写操作。
- 再数据库中自动生成的其他数据表是Django内置功能所使用的数据表，分别是会话session、用户认证管理和Admin日志记录等。
## 1. 构建模型
1. 再model.py中声明数据表对象（一个对象对应一张表）
2. 使用manage.py创建数据表

```python
# models.py
from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 50)
    type = models.CharField(max_length = 20)

# 创建产品类型数据表
class ProductType(models.Model):
    id = models.AutoField(primary_key = True)
    typeName = models.CharField(max_length = 20)
    
#创建产品信息数据表
class ProductInfo(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50)
    weight = models.CharField(max_length = 20)
    size = models.CharField(max_length = 20)
    type_id = models.ForeignKey(ProductType, on_delete = models.CASCADE) 

# cmd
# makemigrations指令用于将index所定义的模型生成0001_initial.py文件，该文件存放在index的migrations文件夹
>python manage.py makemigrations
# migrate指令根据脚本代码在目标数据库中生成相对应的数据表。
>python manage.py migrate

```

- 表字段数据类型及说明

表字段 | 说明
| --- | --- |
models.AutoField | 默认会生成一个名为id的字段并为int类型
models.CharField | 字符串类型
models. BooleanField | 布尔类型
models. ComaSeparatedIntegerField | 用逗号分割的整数类型
models. DateField | 日期(date) 类型
models.DateTimeField | 日期(datetime) 类型
models.Decimal | 十进制小数类型
models. EmailField | 字符串类型(正则表达式邮箱)
models. FloatField | 浮点类型
models.IntegerField | 整数类型
models. BigIntegerField | 长整数类型
models.IPAddressField | 字符串类型(IPv4正则表达式)
models.GenericIPAddressField | 字符串类型，参数protocol可以是: both、 IPv4和ipv6，验证IP地址
models.NullBooleanField | 允许为空的布尔类型
models.PositiveIntegerFiel | 正整数的整数类型
models.PositiveSmallIntegerField | 小正整数类型
models. SlugField | 包含字母、数字、下画线和连字符的字符串，常用于URL
models.SmallIntegerField | 小整数类型，取值范围(-32,768~+32,767)
models.TextField | 长文本类型
models.TimeField | 时间类型，显示时分秒HH:MM[:ss[ .uwuu]]
models.URLField | 字符串，地址为正则表达式
models. BinaryField | 二进制数据类型

- 表字段参数及说明

参数 | 说明
| --- | --- |
Null | 如为True,字段是否可以为空
Blank | 如为True,设置在Admin站点管理中添加数据时可允许空值
Default | 设置默认值
primary_key | 如为True,将字段设置成主键
db_column | 设置数据库中的字段名称
Unique | 如为True,将字段设置成唯一属性， 默认为False
db_index | 如为True,为字段添加数据库索引
verbose_name | 在Admin站点管理设置字段的显示名称
related name | 关联对象反向引用描述符，用于多表查询，可解决一个数据表有两个外键同时指向另一个数据表而出现重名的问题

## 2.数据表的关系

- 一对一的关系
    * 使用OneToOneField构建
        ``` python
        # 学生表
        class Student(models.Model):
            id = models.IntegerField(primary_key = True)
            name = models.CharField(max_length = 20)
            stuIndex = models.CharField(Unique = True)

        # 学生详细信息表
        class Student(models.Model):
            id = models.IntegerField(primary_key = True)
            # 设置该表与学生表为一对一的关系
            student = models.OneToOneField(Student, on_delete = models.CASEADE)
            origin = models.CharField(max_length = 20)
            brithday = models.DateField(Unique = True)
            # True为男，False为女
            stuSex = models.BooleanField()
        ```

- 一对多的关系
    * 使用ForeignKey构建
        ``` python
        # 部门表
        class Department(models.Model):
            id = models.IntegerField(primary_key = True)
            # 设置该表与学生表为一对一的关系
            s = models.ForeignKey(Student, on_delete = models.CASEADE)
            name = models.CharField(max_length = 20)
            # 是否所属团委
            isOffice = models.BooleanField()
        ```

- 多对多的关系
    * 使用ManyToManyField构建
        ``` python
        # 课程表表
        class Course(models.Model):
            id = models.IntegerField(primary_key = True)
            # 设置该表与学生表为一对一的关系
            student = models.ManyToManyField(Student, on_delete = models.CASEADE)
            name = models.CharField(max_length = 20)
            # 学分
            creidt = models.FolatField()
        ```

## 3. 数据表的读写

- 数据库的读写操作主要对数据进行增、删、改、查。
- 使用shell模式（启动命令行和执行脚本），该模式主要为方便开发人员开发和调试程序。输入python manage.py shell指令即可开启。

- 读写操作
    - 增
        ```python
        # 方法一
        p = Product()
        p.id = 1
        p.name = '小米'
        p.type = '手机'
        p.save()

        # 方法二
        p = Product.objects.create(id = '1', name='小米', type='手机')
        
        # 方法二
        p = Product(id = '1', name='小米', type='手机')
        p.save()
        ```
    - 删

         ```python
            # 删除单条数据
            Proudct.objects.get(id = 0).delete()
            # 删除多条数据
            Proudct.objects.filter(id = 0).delete()
            # 删除所有数据
            Proudct.objects.all().delete()
        ```
    - 改
        - 更新，查询数据后再重新赋最后保存

            ```python
            # 单条数据更新
            p = Proudct.objects.get(id = 0)
            p.name = '雷军_小米'
            p.save()
            # 使用Api
            Proudct.objects.get(id = 0).update(name='雷军_小米')
            # 更新多条数据
            Proudct.objects.filter(id = 0).update(name='雷军_小米')
            # 更新所有数据
            Proudct.objects.update(name='雷军_小米')
            ```
    - 查
        - 查询条件get：查询字段必须是 **主键或者唯一约束的字段**，并且查询的数据**必须存在**，如果查询的字段有重复值或者查询的数据不存在，程序都会抛出异常信息。
        - 查询条件filter：查询字段没有限制，只要该字段是数据表的某一字段即可。查询结果以列表的形式返回，如果查询结果为空（查询的数据在数据库中找不到），就返回空列表。
        
            ```python
            # 全表查询
            products = Proudct.objects.all()
            products[1].name

            # 查询前5条数据
            products = Proudct.objects.all()[:5]

            # 查询某个字段(列表-字典)
            products = Proudct.objects.values('name')
            products[1]['name']

            # 查询某个字段(列表-元组)
            products = Proudct.objects.values_list('name')
            
            # 查询单条数据
            product = Proudct.objects.get(id = 0)

            # 查询多条数据
            Proudct.objects.filter(id = 0)

            # 查询多条数据（多条件）
            Proudct.objects.filter(id = 0， name = '小米')

            # 实现OR操作，需要引入Q
            from django.db.models import Q
            products = Product.objects.filter(Q(id = 1)|Q(name = '小米'))

            # 使用count()统计数量
            count = Product.objects.filter(id = 0).count()

            # 去重查询,根据values()中的值判断去重
            products = Product.objects.values('name').filter(name = '小米').distinct()

            # 对查询结果进行排序（‘-’降序）
            products = Product.objects.order_by('-id')
            # 聚合查询
            # annotate相当于SQL中的GROUP BY,对values()中的参数进行分组，默认为主键
            from django.db.models import Sum,Count
            p = Product.objects.values('name').annotate(Sum('id')) 

            # aggregate(n.集合；聚集)将某个字段计算然后返回计算结果
            from django.db.models import Count
            p = Product.objects.aggregate(id_count = Count('id'))
            ```

    - 使用大于、不等于和模糊查询的匹配方法

        匹配符 | 使用 | 说明
        | --- | --- | --- |
        __exact | filter(name__exact='荣耀) | 精确等于，如SQL的like'荣耀'
        __iexact | filter(name__iexact='荣耀') | 精确等于并忽略大小写
        __contains | filter(name__contains='荣耀') | 模糊匹配，如SQL的like'%荣 耀%'
        __icontains | filter(name__icontains='荣耀) | 模糊匹配，忽略大小写
        __gt | filter(id__gt=5) | 大于
        __gte | filter(id__gte= 5) | 大于等于
        __lt | filter(id__lt=5) | 小于
        __lte | filter(id__lte=5) | 小于等于
        __in | filter(id__in=[1,2,3]) | 判断是否在列表内
        __startswith | filter(name__startswith='荣耀) | 以...开头
        __istartswith | filter(name__istartswith= '荣耀) | 以...开头并忽略大小写
        __endswith | filter(name__endswith='荣耀') | 以..结尾
        __iendswith | filter(name__iendswith='荣耀') | 以...结尾并忽略大小写
        __range | filter(name__range='荣耀') | 在...范围内
        __year | filter(date__year=2018) | 日期字段的年份
        __month | filter(date__month=12) | 日期字段的月份
        __day | filter(date__day=30) | 日期字段的天数
        __isnull | filter(name__isnull=True/False) | 判断是否为空


        ```python
        # 查询id <= 4
        p = Prouduct.objects.filter(id__lte = 4)
        ```
## 多表查询

- 正向查询与反向查询
    - 正向查询：查询主体和查询的数据一致，及同一个数据表
    - 反向查询：查询主体和查询的数据针对不同数据表

    ```python
    # 查询主体为ProductType
    p = ProductType.objects.filter(id = 0)
    # 正向查询
    P[0].typeName
    # 反向查询，及用上面的数据去查另一张表ProductInfo
    p[0].productinfo_set.values('name') 
    ```
- 使用select_related方法实现
    ```python
    # productinfo 查询主体的外键，可以使用它访问另一张表
    # values('name', 'producttype__name') 查询输出的字段，productinfo__表示访问另一张表的字段名称
    ProductType.objects.select_related('productinfo').values('name', 'productinfo__name')
    # 添加筛选条件，productinfo__表示访问另一张表的字段名称
    ProductType.objects.select_related().values('name', 'productinfo__name').all)()

    ProductType.objects.select_related().values('name', 'productinfo__name').filter(id = 1)
    ```

# 第7章 表单和模型

- 表单是搜集用户数据信息的各种表单元素的集合
- 作用是实现网页上的数据交互，用户在网站输入数据信息，然后提交到网站服务器端进行处理（如数据录入和用户登录、注册等）。

- 用户表单是Web开发的一项基本功能，Django的表单功能由Form类实现，主要分为两种：
    - django.forms.Form：是一个基础的表单功能
    - django.forms.ModelForm：后者是在前者的基础上结合模型所生成的数据表单。

## 1.初识表单

- 表单的组成元素
    - action: 提交地址;为空，则默认当前的URL
    - method： GET/POST
    - input: 数据输入
    - submit： 提交数据
```html
< !DOCTYPE html>
<html>
    <body>
        #表单
        <form action="" method="post" >
            First name: </br>
            <input type="text" name=" firstname" value=" Mickey"><\br>
            Last name:</br> 
            <input type="text" name="las tname" value="Mouse" >
            </br></br>
            <input type='submit' value='Submit' >
        </form>
        #表单
    </body>
</html>
```
- django中表单的简单使用
1. 创建表单类
    ```python
    from django import forms
    from .models import *

    class BookInfoForm(forms.Form):
        name = forms.CharField(max_length = 20, label="书名")
        author = forms.CharField(max_length = 20, label="作者")
        public = forms.CharField(max_length = 20, label="出版社")
        # 生成多选框
        choices_list = [(1, "科幻"), (2, "漫画"),(3, "军事"),(4, "传记")]
        typeName = forms.ChoiceField(choices = choices_list, label = "类型")
    ``` 
2. 再html中创建表单
    ```html
    <!DOCTYPE html>
    <html lang="zh-CN">
        <head>
            <meta charset="UTF-8"/>
            <title>Title</title>
        </head>
        <body>
            {% if book.errors %}
            <p> 数据出错，出错信息： {{ book.error }}</p>
            {% else %}
                <form action="" method="GET">
                    {% csrf_token %}
                    <table>
                        {{ book.as_table }}
                    </table>
                </form>
                <input type="submit"  value="提交" />
            {% endif %}
        </body>
    </html>
    ```
3. 再views中获取表单对象并渲染生成html返回
    ```python
    def recordBookInfo(request):
        book = BookInfoForm()
        return render(request, 'book_form.html', locals())
    ```

## 2. 表单的定义
    

