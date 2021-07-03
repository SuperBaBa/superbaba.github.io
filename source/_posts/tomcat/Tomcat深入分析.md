---
title: Tomcat的简介
date: 2021-07-03 13:48:22
tags: 
  - Tomcat
  - Java Web
---
# 1. Tomcat的简介

## web概念

1. 软件架构
2. 资源分类
   1. 静态资源：所有用户访问后得到结果都是一样，可以直接被浏览器解析
   2. 动态资源：每个用户访问都是不一样的，需要进行
3. 网络通信三要素
   1. IP地址
   2. 端口号：应用程序在计算机上的唯一标识。0-65536
   3. 传输协议
      * TPC协议：三次握手
      * UDP协议

## web服务器

1. 服务器
2. 服务器软件：接收用户请求
3. web服务器软件：接收用户请求，处理器扭曲做出相应
4. 常见web服务器
   * webLogic
   * webSphere
   * JBoss
   * Tomcat：Apache基金组织
   <!--more-->
# 2. Tomcat的架构

## HTTP工作原理

HTTP协议是浏览器与服务器之间的数据传输协议，作为应用层协议，HTTP是基于TCP/IP协议，因此传输数据包都是由TCP/IP协议进行传输，HTTP只是定义了数据包的封装格式。

## HTTP服务器请求处理

浏览器发送个服务端一个HTTP格式请求，HTTP服务器接收到请求后，需要调用服务端程序

## Servlet容器工作流程

HTTP服务器不直接调用Servlet，而且将请求交给Servlet容器，具体步骤如下：

1. 客户端请求资源，HTTP服务器凤凰组昂成一个ServletRequest队形
2. 然后调用Servlet容器的`service`方法
3. Servlet容器拿到请求后，根据`URL和Servlet的映射关系`找到相应的Servlet
4. 加载Servlet，使用反射创建这个Servlet，并调动`init`方法初始化
5. 调用Servlet的`service`方法用来处理请求

## Tomcat的两个核心功能

1. 处理Socket连接，负责网络字节流与Request和Response对象的转化
2. 加载和管理Servlet，以及具体处理Request请求

两个核心组件连接器`Connector`和`Container`来分别做两件事情。

## 连接器 - coyote

coyote是Tomcat的连接器框架名称，是Tomcat服务器提供的客户端访问外部接口，客户端通过coyote月服务器建立连接、发送请求并接受响应。

**coyote封装了底层网络通信**，并未Catalina容器提供了统一的接口，是Catalina容器月具体的请求协议及IO操作方式完全解耦。Coyote将Socket输入封装为Request对象，交由Catalina容器进行处理，处理完后，Catalina通过Coyote提供的Response对象将结果写入到输出流。

Coyote负责接受请求并进行封装响应，作为独立的模块只负责具体的协议解析和IO相关操作，与Servlet规范实现没有直接关系，因此Request和Response对象也并未实现Servlet规范的对应接口。

**一个容器支持多个连接器**

## IO模型与协议

在Coyote中，Tomcat支持多种I/O模型和应用层协议，在Tomcat 8.5/9.0版本起，移除了对`BIO`的支持。

| **IO模型** | 描述                                              |
| :--------- | ------------------------------------------------- |
| NIO        | 非阻塞I/O，采用Java NIO类库实现                   |
| NIO2       | 异步I/O，采用JDK 7的NIO2类库实现                  |
| APR        | 采用Apache可移植运行库实现，是C/C++编写的本地库， |

Tomcat支持的应用层协议：

| 应用层协议 | 描述                                                         |
| ---------- | ------------------------------------------------------------ |
| HTTP/1.1   | 大部分web应用采用的访问协议                                  |
| AJP        | 在用于和Apache Web服务器集成，已实现对静态资源优化及集群部署 |
| HTTP/2     | HTTP 2.0大幅提升Web性能，下一代HTTP协议，自8.5及9.0版本后支持 |

## Tomcat启动流程

1. 启动tomcat，运行bin/startup.bat（如果是linux环境，则需要调用bin/startup.sh），在startup.bat脚本中，调用了catalina.bat脚本
2. 在`catalina.bat`脚本中进行了`JAVA_OPTS`参数的配置，然后调用了`org.apache.catalina.startup.Bootstrap`类中的`main`方法
3. 在`Bootstrap`的`main`方法中调用了`init`方法，用于初始化`Catalina`类并调用`setParentClassLoader()`方法设置其**类加载器**
4. 在`Bootstrap`的`main`方法中调用了`load`方法，然后分别调用三个方法`setAwait(true)`、`load(args)`、`start()`
   * `setAwait(true)`方法，用于设置`Catalina`对象是阻塞的
   * `load(args)`方法，调用`Catalina`对象`load()`方法，使用流去加载Catalina配置，如`conf/server.xml`，然后由交付于`Digester`对象进行拆解xml，`Server`对象就是在解析中进行初始化的
   * `start()`方法，调用`Server`对象的`start()`方法，并同步代码执行`Lifecycle`、`LifecycleBase`的方法实现。

![tomcat_sequence_chart](http://images.marcus659.com/blog/tomcat_sequence_chart.png)

### Lifecycle接口定义

在Tomcat中的所有组件均存在**初始化**、**启动**、**停止**等生命周期方法，所以在Tomcat设计时，便基于生命周期管理抽象出一个`Lifecycle`接口，而组件Server、Service、Container、Executor、Connector都实现了`Lifecycle`接口，其中部分方法有使用**模板设计模式**抽取出公共逻辑，进行复用。

1. `init()`：初始化组件
2. `start()`：启动组件
3. `stop()`：停止组件
4. `destroy()`：销毁组件

![StandardEngine](https://images.marcus659.com/blog/tomcat_standard_engine.png)

## Tomcat请求处理流程

# 3. Tomcat服务器配置

# 4. Tomcat的管理配置

# 5. Tomcat集群

## tomcat集群简介

tomcat集群是由多个tomcat进程，通过`ngnix`进行反向代理，使用`轮询`、`权重`、`ip_hash`的方式去进行负载策略，

## session共享(保持)问题

1. ip_hash策略

   同一个ip的hash值肯定是相同的，顾可以使用此类方式将用户请求负载到之前有session的那个tomcat进程上。

2. session复制

   session复制可以在小型集群中进行session复制，官方建议此方案适用于四及四个以下tomcat集群



