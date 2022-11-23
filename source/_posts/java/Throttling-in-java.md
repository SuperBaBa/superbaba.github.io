---
title: 限流
comments: true
date: 2022-07-15 12:15:50
categories: java
---

# 固定窗口算法

固定窗口算法又叫计数器算法，是一种简单方便的限流算法。主要通过一个支持原子操作的计数器来累计 1 秒内的请求次数，当 1 秒内计数达到限流阈值时触发拒绝策略。每过 1 秒，计数器重置为 0 开始重新计数。

临界突变
![临界突变问题](https://images.marcus659.com/typora/fixed-window-critical-mutation.png)


# 滑动窗口算法
```java
package com.wdbyte.rate.limiter;

import java.time.LocalTime;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * 滑动窗口限流工具类
 *
 * @author https://www.wdbyte.com
 */
public class RateLimiterSlidingWindow {
    /**
     * 阈值
     */
    private int qps = 2;
    /**
     * 时间窗口总大小（毫秒）
     */
    private long windowSize = 1000;
    /**
     * 多少个子窗口
     */
    private Integer windowCount = 10;
    /**
     * 窗口列表
     */
    private WindowInfo[] windowArray = new WindowInfo[windowCount];

    public RateLimiterSlidingWindow(int qps) {
        this.qps = qps;
        long currentTimeMillis = System.currentTimeMillis();
        for (int i = 0; i < windowArray.length; i++) {
            windowArray[i] = new WindowInfo(currentTimeMillis, new AtomicInteger(0));
        }
    }

    /**
     * 1. 计算当前时间窗口
     * 2. 更新当前窗口计数 & 重置过期窗口计数
     * 3. 当前 QPS 是否超过限制
     *
     * @return
     */
    public synchronized boolean tryAcquire() {
        long currentTimeMillis = System.currentTimeMillis();
        // 1. 计算当前时间窗口
        int currentIndex = (int)(currentTimeMillis % windowSize / (windowSize / windowCount));
        // 2.  更新当前窗口计数 & 重置过期窗口计数
        int sum = 0;
        for (int i = 0; i < windowArray.length; i++) {
            WindowInfo windowInfo = windowArray[i];
            if ((currentTimeMillis - windowInfo.getTime()) > windowSize) {
                windowInfo.getNumber().set(0);
                windowInfo.setTime(currentTimeMillis);
            }
            if (currentIndex == i && windowInfo.getNumber().get() < qps) {
                windowInfo.getNumber().incrementAndGet();
            }
            sum = sum + windowInfo.getNumber().get();
        }
        // 3. 当前 QPS 是否超过限制
        return sum <= qps;
    }

    private class WindowInfo {
        // 窗口开始时间
        private Long time;
        // 计数器
        private AtomicInteger number;

        public WindowInfo(long time, AtomicInteger number) {
            this.time = time;
            this.number = number;
        }
        // get...set...
    }
}
```
