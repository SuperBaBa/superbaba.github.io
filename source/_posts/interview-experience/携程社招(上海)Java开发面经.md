# 携程社招(上海)Java开发面经20210517

一面：

携程总部大楼（上海市长宁区金钟路），汽车票船票组，面试官两位(项目经理+开发工程师)

1、项目了解

此处手绘系统架构图，并表明自己负责的哪一块，我们项目中对ES和RocketMQ使用比较多

2、线程池参数（最好是自己手写过线程池）

* corePoolSize 指定了线程池里的线程数量
* maximumPoolSize 指定了线程池里的最大线程数量
* RejectPolicy 拒绝策略，当任务过多时候，如何拒绝任务
  - **AbortPolicy** 丢弃任务并抛出RejectedExecutionException异常。
  - **DiscardPolicy** 丢弃任务，但是不抛出异常。如果线程队列已满，则后续提交的任务都会被丢弃，且是静默丢弃
  - **CallerRunsPolicy** 丢弃队列最前面的任务，然后重新提交被拒绝的任务
  - **DiscardOldestPolicy** 由调用线程处理该任务
* keepAliveTime 当线程池线程数量大于corePoolSize时候，多出来的空闲线程，多长时间会被销毁。
* ThreadFactory 线程工厂，用于创建线程，一般可以用默认的
* workQueue 任务队列，用于存放提交但是尚未被执行的任务
* unit 时间单位

3、MQ的顺序消费痛点

异常后会阻塞

多个队列，分布式全局不太好处理

3、JVM内存模型

jdk1.7

jdk1.8

jvm调优参数，jstack查看其

4、并发编程

我在项目中CountDown等待所有线程**减一**结束，然后主线程获取`Future`中的结果

Volatile关键字使用

5、锁

synchronize 互斥锁

ReentrantLock 可重入锁(自旋锁)

6、MYSQL索引执行查看策略

使用`explain`查看执行策略



改个文章