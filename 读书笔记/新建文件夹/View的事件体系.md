# View的事件体系
## View的基础知识
### 什么是View
- View是Android中所有控件的基（单View或者VIewGroup）

### View的位置参数
- 分别是左上角和右下角的（left,top）和（right,bottom），可以get相关参数
- 通过两坐标可以获得控件的宽高
- Android3.0添加了其他参数：x,  y, translationX, translationY
-  View平移是，left,top不变，变化的是额外添加的四个参数

### MotionEvent和TouchSlop
1. MotionEvent
- 事件类型：
- ACTION_DOWN
- ACTION_MOVE
- ACTION_UP
- 获取事件发生坐标：通过MotionEvent的getX()/getY ()和getRawX()/getRawY (),前者是相对于当前View,后者是相对于屏幕

2. TouchSlop
- 滑动的最小距离：8dp

### VelocityTracker/GestureDetector/Scroller
1. VelocituTracker
- 速度追踪，追踪手指在滑动过程中的速度
- 首先在View的onTouchEvent事件中进行追踪
```java
VelocityTracker velocityTracker = VelocitTracker.obation();
velocityTracker.addMovement(event);
```

- 接着就可以获取速度了

```java
//获取速度之前必须先计算速度
//1000为单位时间（单位：ms）即像素每1000ms
velocityTracker.computeCurrentVelocity(1000);
int xVelocity = velocityTracker.getXVelocity();
int yVelocity = velocityTracker.getYVelocity();
```
- 不需要是就清除回收内存
```java
velocityTracker.clear();
velocityTracker.recycle();
```
2. GestureDetector
- 手势检测：用于辅助检测用户单击、滑动、长按、双击等行为。
- 使用
    1. 创建GestureDetector对象并实现OnGestureListener接口
    2. 