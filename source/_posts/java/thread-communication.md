---
title: 线程间的通信
comments: true
date: 2022-07-07 12:15:50
categories: java
---
# 问题背景

在同一个进程中，咱们可能存在多线程对同一个东西进行修改，比如一个全局变量标识，后面的线程根据这标识。

例如当前有多个线程进行滚动查询，每次查询通信都会返回一个`lastRecordId`，也就是本次翻页查询最后一条记录的Id，下次请求需要带上这个字段才能顺利翻到下一页

# 使用Volatile关键字
`volatile`关键字多线程见可见，线程能够感知到同一个变量的变化
Arthas 是Alibaba开源的Java诊断工具。采用命令行交互模式，提供了较为丰富的功能，主要还是他是免费里面的算是好用且功能比较强大的一个JVM排查的插件。

# 使用Object类的wait()/notify()
```java
public class TestSync {
    public static void main(String[] args) {
        //定义一个锁对象
        Object lock = new Object();
        List<String>  list = new ArrayList<>();
        // 线程A
        Thread threadA = new Thread(() -> {
            synchronized (lock) {
                for (int i = 1; i <= 10; i++) {
                    list.add("abc");
                    System.out.println("线程A添加元素，此时list的size为：" + list.size());
                    try {
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    if (list.size() == 5)
                        lock.notify();//唤醒B线程
                }
            }
        });
        //线程B
        Thread threadB = new Thread(() -> {
            while (true) {
                synchronized (lock) {
                    if (list.size() != 5) {
                        try {
                            lock.wait();
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                    System.out.println("线程B收到通知，开始执行自己的业务...");
                }
            }
        });
        //需要先启动线程B
        threadB.start();
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        //再启动线程A
        threadA.start();
    }
}
```

## Dashboard

## 字节码反编译

## Thread信息捕获

## 查看JVM信息

## 堆内存快照信息分析