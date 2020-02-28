# 直通车
- [java关键字](#javakeyvalue)
- [java中的随机数](#javarandom)
- [object](#object)
- [String](#string)


# <span id="string">String</span>

- String.fromt()

| 标识|说明 | 实例 | 结果 |
| --- | --- | --- | --- |
| 0X | 整数占位符 | ("%03d", 23) | 023 |
| X.Y | 小数占位符 | ("%3.2f", 9.9) | 009.9 |

# <span id="object">object(160-173)</span>
- 所有类的超类(所有类默认继承该类)
    * 因此可以持有所有类但是对其中内容的操作还是要知道该对象的原始类型
- 该类的成员函数
    * Equals()
        - 检测一个对象是否等于另一个对像，在Object比较的使两个对像是否有相同的引用，对于大多数类来说没有什么意义(重写该方法)
    * hashCode()
        - 对像导出一个整型值的散列码
        - 数组计算散列码：static int hashCode(type[] array)
    * toString()
        - 返回表示对象值的字符串
    * getName()
        -返回这个类的名字
    * clone()
        - 创建一个对象的副本
    * getSuperClass()
        - 以class对像的形式返回这个类的超类信息

# <span id="javakeyvalue">java关键字</span>
- native
- final
    * 修饰变量->常量
    * 修饰函数->子类不可重写
    * 修饰类->该类不可被继承

# <span id="javarandom">java中的随机数</span>
```java
//使用Random类
//生成对象Randomer
Random randomer = new Random();
//获取随机数(int\double\boolean\long\float)
int dataInt = randomer.nextInt();
boolean dataBoolean = randomer.nextBoolean();
```
