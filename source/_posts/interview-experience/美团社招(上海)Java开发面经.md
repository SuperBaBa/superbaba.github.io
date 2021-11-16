---
title: 美团社招(上海)Java开发面经
date: 2021-06-12 12:48:22
tags: 
  - Java
  - 面经
categories:
  - 面经
---
[TOC]
# 美团社招(上海)Java开发面经

先搞个前提，各位同学可以根据自身情况仅做参考，本人非计算机专业，学历一般吧，工作目前两年左右，因为工作日实在没有时间，所以和HR约定的是视频面试。

招聘的岗位描述：Java开发工程师，但可能需要学习Go语言，非业务开发部门

地点：上海市长宁区北新泾地铁站附近吧，一年之后极有可能搬到杨浦区

### 技术一面

1. 项目相关的一些问题，主要是阐述了下项目是什么业务场景，解决什么问题，在进行项目描述过程汇总面试官比较关注的貌似是**并发量**和**业务总量**

2. 因为我在项目中使用了很多的ES作为持久层，所以面试官就针对我熟悉的中间件进行了提问

   * ES在写入时它是怎么完成一次写入操作的？

     此处我给出了两种层面的回答
     
     > 1. 架构层面
     >
     >    在架构层面，由于ES分为了`master`、`client`、`data`、`ingest`四种角色，每次写入和读取的HTTP请求都会先落到client角色的节点上，然后再**负载**到各个data节点上，完成写入和读取的操作后又将响应给应用程序。其中需要注意的是`data`节点在进行查询时，是由多个分片进行查询后，在内存中拼接而成的，所系查询时也需要很大的内存，
     >
     > 2. 持久化操作层面
     >
     >    这层面的话就只是在写入操作上进行了藐视，首先是数据请求到达了data节点进行存储，存储时刷盘存在了两种方式，`buffer`刷入磁盘和`translog`进行存储
   <!--more-->  
   * ES集群写入是怎么优化的
   
3. 关于`HashMap`源码方面的理解，主要是存储运算过程

   * HashMap的容量为什么是2的n次方幂
   * HashMap线程不安全会有哪些影响
   * HashMap的resize过程是怎么样的
   * 对于其他集合框架的了解

   关于这个HashMap，我之前有专门研究过两天源码，笔记放着同学们自行拿取[HashMap源码学习笔记](https://blog.csdn.net/qq_26125865/article/details/115221949?spm=1001.2014.3001.5501)

4.  JVM堆内存模型相关问题

   ![jvm_memory_region](http://images.marcus659.com/blog/jvm_memory_region.jpg)

   * 新建对象内存分配过程(没太答上来)

     > 这里应该会涉及到**指针碰撞**、**空闲列表**、**并发安全(CAS机制和分配缓冲)**

   * 堆内存中的GC分类，我在回答时分为了youngGC和FullGC

   * 出现GC时什么情况下会有阻塞用户线程的情况

   * GC算法进行标记的时候，**可达性分析算法中，根可达算法(GC Roots)有哪些根**

     作为 GC Roots 的对象包括下面几种:

     > 1. 虚拟机栈（栈帧中的本地变量表）中引用的对象；各个线程调用方法堆栈中使用到的参数、局部变量、临时变量等。 
     > 2. 方法区中类静态属性引用的对象；java 类的引用类型静态变量。 
     > 3. 方法区中常量引用的对象；比如：字符串常量池里的引用。 
     > 4. 本地方法栈中 JNI（即一般说的 Native 方法）引用的对象。 
     > 5. JVM 的内部引用（class 对象、异常对象 NullPointException、OutofMemoryError，系统类加载器）。（非重点） 
     > 6. 所有被同步锁(synchronized 关键)持有的对象。（非重点） 
     > 7. JVM 内部的 JMXBean、JVMTI 中注册的回调、本地代码缓存等（非重点） 
     > 8. JVM 实现中的“临时性”对象，跨代引用的对象

5. Spring框架是如何解决循环依赖的问题

6. SpringMVC框架中Filter和Interceptor有什么区别，平时会怎么使用它们

7. ThreadLocal的实现原理，为什么能保证线程安全

8. 设计模式，手写一个静态工厂模式

   > 之前另一个面试手写过三种单例模式，这些设计模式考的都还挺简单的，目前我自己掌握的有
   >
   > 三种创建模式：
   >
   > 单例、工厂、原形
   >
   > 四种行为模式：
   >
   > 模板、策略、监听(写的不多，要百度才能手写出来)、责任链

9. 一个业务场景的算法选择，**字典树算法**

   给出的业务场景：目前有一堆单词，给定开头的前缀，如`ab`找出这对单词中以`ab`开头的单词。这个没有手写，但是之前在业务上自己用过，放这里方便大家参考

   ```java
   public static void initTrie(Set<String> sensitiveWords) {
       words = new HashMap(sensitiveWords.size());
       Map temp;
       Map<String, String> temp2;
       //遍历传入的敏感词集合，构建字典树
       for (String word : sensitiveWords) {
           temp = words;
           //将每个词转为字符数组，每个字符都是一个状态，构建有限状态集合
           for (char character : word.toCharArray()) {
               //先查看字典树内是否存在这个状态
               Object var1 = temp.get(character);
               if (var1 != null) {
                   //如果存在，则指向下一个节点
                   temp = (Map) var1;
               } else {
                   //如果不存在则进行创建节点
                   temp2 = new HashMap();
                   temp2.put("isEnd", "0");
                   //放置该字符，并标记其状态
                   temp.put(character, temp2);
                   //指向下一个节点
                   temp = temp2;
               }
               if (word.charAt(word.length() - 1) == character) {
                   temp.put("isEnd", "1");
               }
           }
       }
       System.out.println(words);
   }
   
   public static boolean contains(String text, int matchType) {
       int i = 0;
       while (i == text.length() - 1) {
           text.substring(i);
       }
       return false;
   }
   
   public static void main(String[] args) {
       initTrie(new HashSet<>(Arrays.asList("搓搓手", "扣扣脚", "深深懒腰")));
       System.out.println(contains("搓手",1));
   }
   ```

   

### 反问环节

1. 团队代码规范是否严苛，是否有注释

   A：代码注释可能不会特别多，但是对于变量的命名有绝对的CodeReview标准，代码仓库也是自研，如果代码不是太规范标准的话，将不能编译

2. 招人团队属于哪个业务线，如果一起奋斗的话，会在哪个模块

   A：主要是负责公司自研的`代码仓库`，只有部分命令传输模块使用的是开源组件，其他均为公司自研，非业务方面，并且能够看到公司所有的代码







