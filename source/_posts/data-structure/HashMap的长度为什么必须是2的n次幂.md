---
title: HashMap的长度为什么必须是2的n次方
date: 2021-06-12 12:48:22
tags: Java
categories:
  - Java基础
  - 集合框架
---
首先我们看下`HashMap`中的源码当中那里奠定了长度是**2的n次方**，并且是靠近`cap`这个值`最近的2的n次方`

```java
static final int tableSizeFor(int cap) {
    // 首先cap-1使得n的最后一位和cap最后一位绝对不一样
    int n = cap - 1;
    // 向右无符号的移动了1位，并使用或运算使n的所有有1的位上全部是1
    n |= n >>> 1;
    // 向右无符号移动2位，使用或运算将低位填充为1
    n |= n >>> 2;
    // 同理可得
    n |= n >>> 4;
    n |= n >>> 8;
    n |= n >>> 16;
    // 已经向右移动多个位，最终 00011111 = 31 那么 +1 既成为了2的n次方
    return (n < 0) ? 1 : (n >= MAXIMUM_CAPACITY) ? MAXIMUM_CAPACITY : n + 1;
}
```

由上方代码可以看出，上方的方法是**将`cap`无符号的向右移动，再启动期间，使用`|`运算保证低位全部是1。**

看起来有点复杂，那咱们举个例子：
<!--more-->

1. 首先我们传入`cap`初始值为17
2. 经过`int n = cap -1 `也就是17-1后`n = 16`
3. 将n进行如下的**位移动和逻辑运算**，最后得到`n = 31`
4. 返回是根据三目运算符，得值返回值是`n + 1 = 32`，正好是 **2的5次方**

![image-20211116152759541](https://images.marcus659.com/typora/hashmap-calculate01.png)

通过上方的容量计算，我们已经确定在HashMap中`capacity `一定是**2的n次方**。

在进行取模运算时，为什么我们必须要使用位运算进行取模

- `&`运算速度快，至少比`%`取模运算快

- 能保证索引值肯定在 capacity 中，不会超出数组长度，`(n - 1) & hash`，当为2的n次方时，会满足一个公式：`(n - 1) & hash = hash % n`

![hashmap-calculate02.png](https://img-blog.csdnimg.cn/20210629011049948.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzI2MTI1ODY1,size_16,color_FFFFFF,t_70#pic_center)

两种运算效率差别到底有多少，这里可以直接做个测试：

```java
public static void main(String[] args) {
    int times = Integer.MAX_VALUE;
    /* 此处计算2^31-1次9999整数对1024的取模，使用的数学计算
     * 多次执行放大时间
     */
    long currentTimeMillis = System.currentTimeMillis();
    int a = 0;
    for (long i = 0; i < times; i++) {
        a = 9999 % 1024;
    }
    long currentTimeMillis2 = System.currentTimeMillis();
    /* 此处计算2^31-1次9999整数对1024的取模，使用的位运算
     * 因为要求 hash&(n-1) 中n必须为2的n次方，这里取1024
     */
    int b = 0;
    for (long i = 0; i < times; i++) {
        b = 9999 & (1024 - 1);
    }

    long currentTimeMillis3 = System.currentTimeMillis();
    System.out.println(a + "," + b);//最后的结果应该是一样的
    System.out.println("数学计算耗时: " + (currentTimeMillis2 - currentTimeMillis));// 1839ms
    System.out.println("位运算耗时: " + (currentTimeMillis3 - currentTimeMillis2));// 852ms
}
```



那么当我们在HashMap初始化时，如果指定非2的n次方整数为初始化容量`initialCapacity`，那么会不会致使HashMap中的数组变更

```java
public HashMap(int initialCapacity, float loadFactor) {
    if (initialCapacity < 0)
        throw new IllegalArgumentException("Illegal initial capacity: " +
                                           initialCapacity);
    if (initialCapacity > MAXIMUM_CAPACITY)
        initialCapacity = MAXIMUM_CAPACITY;
    if (loadFactor <= 0 || Float.isNaN(loadFactor))
        throw new IllegalArgumentException("Illegal load factor: " +
                                           loadFactor);
    this.loadFactor = loadFactor;
    // 此处可以看到下一次扩容的值已经经过转换，是2的n次方，并且只有在put时才会有Entry数组的创建
    this.threshold = tableSizeFor(initialCapacity);
}
```

由上面的源码咱们可以看到，HashMap的容量经过了tableSizeFor方法处理，能保证容量永远都是2次幂。