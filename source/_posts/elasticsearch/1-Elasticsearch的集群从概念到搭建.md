---
title: Elasticsearch集群从概念到搭建
date: 2021-11-04 12:48:22
tags: Elastcisearch
categories:
  - 文档型数据库
  - 全文搜索
  - NoSQL
---

[TOC]

# Elasticsearch从概念到搭建

Elasticsearch是一个开源的高扩展的`分布式全文搜索和分析引擎`，是整个Elastic Stack的核心。在咱们即将接触到的Elastic Stack中还有出了Elasticsearch以外的其他组件，`Logstash`和`Beats`充当了数据收集、聚合、处理非结构化数据的角色，在数据存储到Elasticsearch之前不可缺少的前置项目。Kibana使咱们存储在Elasticsearch中的各个维度数据有了可视化的功能，同时结合`X-Pack`套件，将能够获得更多扩展功能，如：ILM、Dashboard、Alarm、Aggregation 等更多大数据所需要的各类功能。

Elasticsearch的很多操作都是可以通过`RESTful API`进行调用触发，这样一来隐藏Lucene的复杂性，让全文搜索变得简单，同时也能够在各平台进行扩展时，有了更好的扩展性。

<!--more-->

**ES作为一个分布式搜索和分析引擎，解决的并不只是搜索相关问题，根据各类用例和官方解释可归纳为：**

- 在应用程序或网站中增加垂直搜索

- 存储日志、指标和安全事件的海量数据  ，同时以数据维度提供各类可视化的分析报表

- 为机器学习自动模拟实时数据提供数据捅，同时还可为算法平台提供模拟行为 

- 使用Elasticsearch作为存储引擎实现业务工作流的自动化  

- 使用Elasticsearch作为地理信息系统(GIS)管理、集成和分析空间信息  

- 使用Elasticsearch作为生物信息学研究工具存储和处理遗传数据 (非机构化并且数据量很大)

  

## 1. 高可用性

通过适合场景的设计减少系统不能提供服务的时间，集群的部署方式不仅能提供可用性更高的服务，同时也会对`数据的安全性和可用性加以保障`。为了保证在`宕机期间`，ES的数据安全和依然可用，则需要对其数据进行备份，在单个集群或单个节点中，为了提高数据的可用性，需要有`分片和副本的概念`，在进行跨集群复制，`follower cluster`也需要进行了解。

### 分片和副本

**分片**：将数据切分成多个部分，在ES中所有数据都存储于`索引(index)` 之上，但实际索引只是维护了与多个分片之间的联系，数据则是被路由到多个分片。例如一个索引有5个分片，则该索引将会有`0,1,2,3,4,这五个分片` ，起指定每个文档数据存储在哪个分片是根据路由运算公式`has(_routing)%number_of_primary_shards`指定，使数据`均匀分布`在集群当中。

**副本**：副本是`主分片` 的复制分片，可以灵活调整，提高了整个集群的`容错性` ，且需要注意的是`副本分片不能与主分片在同一个节点`。一般来说，Elasticsearch 会尽量把一个索引的不同分片存储在不同的主机上，分片的副本也尽可能存在不同的主机上，这样可以提高容错率，从而提高高可用性。

![elasticsearch-write-processes](http://images.marcus659.com/typora/elasticsearch-write-processes.png)

> 如果存在某个或某几个分片存储数据量特别大，可以使用`索引分区`既`index.routring_partition_size`， 但使用后限制有
>
> 1. 无法创建`join_feild` 关系映射
> 2. `_routing` 将成为写入数据必要传入参数

### 集群设计

### 跨集群复制



## 2. 健康状态
elasticsearch集群存在三种健康状态，单节点elasticsearch也可以算是一个集群。

+ green(绿色)：代表所有索引的主分片和副本均已分配且可用，集群是100%可用
+ yellow(黄色)：主分片已分配且全部主分片可用，但所有的副本不全部可用，可能是缺失，也有可能是某个索引的副本`未被分配`，可以通过`move` `cancel` `allocate` 命令所属的API进行分配或移动分片到指定节点，使用这里要注意`主分片和其副本绝不能在同一节点`。此时系统容错性和集群高可用被弱化。
+ red(红色)：所有的主分片不全部可用，这代表很有可能存在丢失数据的风险。
  如果只有一个单节点Elasticsearch那么属于一种yellow状态，因为没有副本。

## 3. 存储空间

多个节点的ES集群，那么相对单节点来说拥有更多的存储空间，可以设置`elasticsearch.yml` 设置`data` 和`log` 的挂载目录。

# ES集群Set up
## 节点类型
集群由多个节点构成，每一台主机则称为一台节点，在伪集群中每一个ES实例则为一个节点。
![elastic-cluster01](http://images.marcus659.com/typora/elastic-cluster01.png)
上述图中则为一个集群，其中Node-1是`主节点`，主节点有权限控制整个集群，有权限控制整个集群。每个节点都有三个分片，其中`P0 P1 P2` 代表Primary为主分片，R开头的则代表为每个主分片对应的副本分片，一共是3个主分片，每个主分片有两个对应的副本分片。

* 主节点：即 Master 节点。主节点的主要职责是和集群操作相关的内容，如创建或删除索引，跟踪哪些节点是群集的一部分，并决定哪些分片分配给相关的节点。稳定的主节点对集群的健康是非常重要的。默认情况下任何一个集群中的节点都有可能被选为主节点。索引数据和搜索查询等操作会占用大量的cpu，内存，io资源，为了确保一个集群的稳定，分离主节点和数据节点是一个比较好的选择。虽然主节点也可以协调节点，路由搜索和从客户端新增数据到数据节点，但最好不要使用这些专用的主节点。一个重要的原则是，尽可能做尽量少的工作。

* 数据节点：即 Data 节点。数据节点主要是存储索引数据的节点，主要对文档进行增删改查操作，聚合操作等。数据节点对 CPU、内存、IO 要求较高，在优化的时候需要监控数据节点的状态，当资源不够的时候，需要在集群中添加新的节点。

* 负载均衡节点：也称作 Client 节点，也称作客户端节点。当一个节点既不配置为主节点，也不配置为数据节点时，该节点只能处理路由请求，处理搜索，分发索引操作等，从本质上来说该客户节点表现为智能负载平衡器。独立的客户端节点在一个比较大的集群中是非常有用的，他协调主节点和数据节点，客户端节点加入集群可以得到集群的状态，根据集群的状态可以直接路由请求。但是过多的协调节点也会增加Master节点管理难度，增加Master节点管理集群的负担。

* 预处理节点：也称作 Ingest 节点，在索引数据之前可以先对数据做预处理操作，所有节点其实默认都是支持 Ingest 操作的，也可以专门将某个节点配置为 Ingest 节点。以上就是节点几种类型，一个节点其实可以对应不同的类型，如一个节点可以同时成为主节点和数据节点和预处理节点，但如果一个节点既不是主节点也不是数据节点，那么它就是负载均衡节点。具体的类型可以通过具体的配置文件来设置。

* 冷热节点：在Elasticsearch集群中，如果存在冷热架构那么，在数据节点上就会存在 `node.attr.box_type: hot` 、`node.attr.box_type: warm`、`node.attr.box_type: cold` 三种不同的**数据节点**，这三类数据节点可以使用不同配置的机器，从而节约集群的机器成本


**Elasticsearch处理查询请求时节点工作流程：**
1. 请求被交给主节点
2. 主节点接收请求，将请求广播到该索引在数据节点上的每个分片(shard)
3. 每个分片执行搜索请求，并将结果返回
4. 分片的Result在主节点上进行合并。排序后返回给用户
## 配置文件
Elasticsearch有很好的默认配置，更多地设置可以使用 ` Cluster update settings API ` 在集群运行中进行设置，官方指导集群设置如下：
[https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-update-settings.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-update-settings.html)
**Elasticsearch 有三个配置文件**：
* `elasticsearch.yml` elasticsearch单个实例的配置文件
* `jvm.options`  elasticsearch**JVM虚拟机内存设置**，并可以使用`bootstrap.memory_lock` 锁定虚拟内存的大小
* `log4j2.properties` elasticsearch日志设置，可以设置**慢索引**/**慢查询**日志打印

**配置文件location**：
 `ES_HOME/config` 目录下，如果想更改的话可以在**环境变量中**设置`ES_PATH_CONF=/path/to/my/config`或者**启动参数**设置`ES_PATH_CONF=/path/to/my/config ./bin/elasticsearch`

**GC日志**:
ES默认启动GC日志，被配置在`jvm.options`中，日志输出位置默认与es日志位置相同，`/path/data/log`并且最多只占用`2G`磁盘空间，每`64M` 进行一次打包。
```bash
## JDK 8 GC logging

8:-XX:+PrintGCDetails
8:-XX:+PrintGCDateStamps
8:-XX:+PrintTenuringDistribution
8:-XX:+PrintGCApplicationStoppedTime
8:-Xloggc:logs/gc.log
8:-XX:+UseGCLogFileRotation
8:-XX:NumberOfGCLogFiles=32
8:-XX:GCLogFileSize=64m

# JDK 9+ GC logging 更改路径即可改变gc日志输出位置
9-:-Xlog:gc*,gc+age=trace,safepoint:file=logs/gc.log:utctime,pid,tags:filecount=32,filesize=64m
# due to internationalization enhancements in JDK 9 Elasticsearch need to set the provider to COMPAT otherwise
# time/date parsing will break in an incompatible way for some date patterns and locals
9-:-Djava.locale.providers=COMPAT
```
# 搭建Elasticsearch7.X伪集群
**1. 下载ES**
这里我们把ES安装在服务器的`opt` 目录下
```bash
# 使用华为镜像超快！！ 并重命名未 elasticsearch7.4-x86.tar.gz（x86是系统指令架构）
$ wget -O elasticsearch7.4-x86.tar.gz https://mirrors.huaweicloud.com/elasticsearch/7.4.0/elasticsearch-7.4.0-linux-x86_64.tar.gz
# 解压
$ tar -zxvf elasticsearch7.4-x86.tar.gz
```
**2. 修改 `jvm.options` 和 `elasticsearch.yml` 配置ES**
```bash
# 进入es配置目录
$ cd /opt/elasticsearch7.4-x86/config
# 修改jvm相关参数，调整jvm堆内存大小
$ vim jvm.options
# 对es进行配置
$ vim elasticsearch.yml
```
* jvm.options配置
```bash
## 修改 IMPORTANT: JVM heap size ，内存小我就设置成这样了
-Xms512m
-Xmx512m
```
* 配置elasticsearch.yml
```yml
# 不要在该文件中设置索引相关配置
cluster.name: waybill-center # 设置集群名比较重要！
# ------------------------------------ Node ------------------------------------
node.name: es-master # 配置节点名
node.master: true # 是否有资格被选举为master，ES默认集群中第一台机器为主节点
node.data: false # 是否存储索引数据，默认 true，大集群中推荐一个角色一个类节点，不要身兼多职
node.ingest: false #默认情况下所有节点均可以做ingest节点
node.attr.box_type: hot
# ----------------------------------- Paths ------------------------------------
#path.conf: /opt/elasticsearch7.4-x86/config # 设置配置文件存储路径，默认是es根目录下的config目录
path.data: /data/es-master/data # 设置索引数据存储路径，默认是es根目录下的data目录
path.logs: /data/es-master/log # 设置日志文件存储路径，默认是es根目录下的log目录
# ----------------------------------- Memory -----------------------------------
#bootstrap.memory_lock: true # 锁住内存不进行swapping，避免系统内存不够时压制JVM虚拟内存
# ---------------------------------- Network -----------------------------------
#network.host: 192.168.0.1 # 同时设置bind_host 和 publish_host
network.bind_host: 0.0.0.0 # 设置节点绑定ip，可用于http访问
network.publish_host: 10.130.9.129 # 设置其他节点与该节点交互ip，可以使内网ip单必须是真实ip
# Set a custom port for HTTP:
http.port: 9200 # 设置对外服务http端口
transport.tcp.port: 9300 # 设置节点之间交互的tcp端口
transport.tcp.compress: true # 设置是否压缩tcp传输时的数据，默认为false
# --------------------------------- Discovery ----------------------------------
#
# Pass an initial list of hosts to perform discovery when this node is started:
# The default list of hosts is ["127.0.0.1", "[::1]"]
#
discovery.seed_hosts: ["10.130.9.129:9300", "10.130.9.129:9301","10.130.9.129:9302"]
# 集群个节点IP地址，也可以使用els、els.shuaiguoxia.com等名称，需要各节点能够解析
#
# Bootstrap the cluster using an initial set of master-eligible nodes:
#
cluster.initial_master_nodes: ["es-master"]
# 也可以如下配置，二选一
discovery.seed_hosts:
   - 192.168.1.10:9300
   - 192.168.1.11 # 端口默认是9300
   - seeds.mydomain.com # 域名解析出来多个地址，则es会尝试发现所有节点
   - [0:0:0:0:0:ffff:c0a8:10c]:9301 #IPV6 地址必须用中括号括起来
cluster.initial_master_nodes: 
   - master-node-a
   - master-node-b
   - master-node-c
   
discovery.zen.minimum_master_nodes: 2  # 为了避免脑裂，集群节点数最少为 半数+1
# For more information, consult the discovery and cluster formation module documentation.
# ---------------------------------- Gateway -----------------------------------
gateway.recover_after_nodes: 3 # 设置集群中N个节点启动时进行数据恢复，默认为1
# 是否支持跨域，是：true，在使用head插件时需要此配置,“*” 表示支持所有域名
http.cors.enabled: true
http.cors.allow-origin: "*"
```
**3. 配置ES使用自己的所带的jdk(推荐)**
* 修改 `bin` 目录下的`elasticsearch` 脚本文件
```bash
source "`dirname "$0"`"/elasticsearch-env # 这里可以看出先加载的 elasticsearch-env 脚本设置环境
# use es internal jdk
export JAVA_HOME=$ES_HOME/jdk/
export PATH=$JAVA_HOME/bin:$PATH
```
* 查看`elasticsearch-env`
```bash
#!/bin/bash

set -e -o pipefail

CDPATH=""

SCRIPT="$0"

# SCRIPT might be an arbitrarily deep series of symbolic links; loop until we
# have the concrete path
while [ -h "$SCRIPT" ] ; do
  ls=`ls -ld "$SCRIPT"`
  # Drop everything prior to ->
  link=`expr "$ls" : '.*-> \(.*\)$'`
  if expr "$link" : '/.*' > /dev/null; then
    SCRIPT="$link"
  else
    SCRIPT=`dirname "$SCRIPT"`/"$link"
  fi
done

# determine Elasticsearch home; to do this, we strip from the path until we find
# bin, and then strip bin (there is an assumption here that there is no nested
# directory under bin also named bin)
ES_HOME=`dirname "$SCRIPT"` # 这里可以看出已经设置了ES_HOME

# now make ES_HOME absolute
ES_HOME=`cd "$ES_HOME"; pwd`

while [ "`basename "$ES_HOME"`" != "bin" ]; do
  ES_HOME=`dirname "$ES_HOME"`
done
ES_HOME=`dirname "$ES_HOME"`
```
**4. 复制当前es构建其他数据节点**
* 复制当前ES目录
```bash
# 复制两份数据节点的目录
cp -r /opt/elasticsearch7.4-x86 /opt/es-data-node1 
cp -r /opt/elasticsearch7.4-x86 /opt/es-data-node2
```
* 修改两个数据节点的配置文件，先修改第一数据节点
```bash
vim /opt/es-data-node1/config/elasticsearch.yml
```
```yml
node.name: es-node1 # 配置节点名
node.ingest: false #默认情况下所有节点均可以做ingest节点
node.master: false # 是否有资格被选举为master，ES默认集群中第一台机器为主节点
node.data: true # 是否存储索引数据，默认 true
node.attr.box_type: hot
#path.conf: /opt/es-data-node1/config # 设置配置文件存储路径，默认是es根目录下的config目录
path.data: /data/es-node1/data # 设置索引数据存储路径，默认是es根目录下的data目录
path.logs: /data/es-node1/log # 设置日志文件存储路径，默认是es根目录下的log目录
http.port: 9201 # 设置对外服务http端口
transport.tcp.port: 9301 # 设置节点之间交互的tcp端口
```
* 修改两个数据节点的配置文件，再修改第二个数据节点
```bash
vim /opt/es-data-node2/config/elasticsearch.yml
```
```yml
node.name: es-node2 # 配置节点名
node.master: false # 是否有资格被选举为master，ES默认集群中第一台机器为主节点
node.data: true # 是否存储索引数据，默认 true
node.attr.box_type: hot
#path.conf: /opt/es-data-node2/config # 设置配置文件存储路径，默认是es根目录下的config目录
path.data: /data/es-node2/data # 设置索引数据存储路径，默认是es根目录下的data目录
path.logs: /data/es-node2/log # 设置日志文件存储路径，默认是es根目录下的log目录
http.port: 9202 # 设置对外服务http端口
transport.tcp.port: 9302 # 设置节点之间交互的tcp端口
```
**5. 创建ES存储数据和log目录**
```bash
# 根据之前每个节点的配置文件内配置path进行创建或修改
mkdir -p /data/es-master/data
mkdir -p /data/es-node1/data
mkdir -p /data/es-node2/data
mkdir -p /data/es-master/log
mkdir -p /data/es-node1/log
mkdir -p /data/es-node2/log
```
**6. 因为ES不能用root用户启动，所以要新建用户**
```bash
groupadd es # 新建用户组es
useradd es -g es# 新建用户并添加到es用户组
passwd es # 也可以更改用户密码（输入 123123）
```
**7. 授权es用户对目录的操作权限**
```bash
chown -R es:es  /data/es-master/
chown -R es:es  /data/es-node1/
chown -R es:es  /data/es-node2/
```
**8. 启动ES集群**
```bash
# 需切换为es用户
su es
# 启动服务
./opt/elasticsearch7.4-x86/bin/elasticsearch -d
./opt/es-data-node1/bin/elasticsearch -d
./opt/es-data-node2/bin/elasticsearch -d
```
* 后台运行ES可以加入-p 命令 让es在后台运行， -p 参数 记录进程ID为一个文件# 设置后台启动
```bash
./opt/elasticsearch7.4-x86/bin/elasticsearch  -p /tmp/elasticsearch-pid -d
```
* 结束进程
```bash
# 查看运行的pid
cat /tmp/elasticsearch-pid && echo
# 结束进程
kill -SIGTERM {pid}
```
# Docker安装Elasticsearch集群
# 生产环境重要系统配置
## 禁用交换区
多数操作系统尝试为文件系统缓存使用更多的内存，会迫切的交换未使用的应用内存。这可能导致JVM堆内存部分或者执行页被置换出到磁盘。
交换对节点的稳定性非常不友好，并且
有三种方式禁用交换，首选是完全禁用交换，如果不能完全禁用交换区，那么需要跟你环境来决定是最小化交换区还是内存锁定

**1. 超过当前最大文件描述符**
如果出现 `max file descriptions`，修改`limits.conf`
```bash
vim /etc/security/limits.conf # 修改限制文件
```
向文件内添加文件数
```bash 
*  soft nofile 65536
*  hard nofile 65536
* soft memlock unlimited 
* hard memlock unlimited
```
**2. 超过当前最大线程数**
如果出现 `max number of threads`，修改`limits.d/20-nproc.conf`
```bash
vim /etc/security/limits.d/20-nproc.conf
```
修改参数
```bash
*  soft    nproc   4096
*  hard   nproc   4096
# 或者不限制也行
# root       soft    nproc     unlimited 
```
**3. 超过当前最大虚拟内存**
如果出现 `virtual memory areas`，修改`sysctl.conf`
```bash
vim /etc/sysctl.conf
```
修改参数
```bash
vm.max_map_count=262144
# 也可使用下面命令临时修改内存限制
sysctl -w vm.max_map_count=262144
```
# 在主节点机器上进行验证
当我们配置好并启动集群后，因为主节点打开了 `http.port` 并且主节点主要用于整个集群的管理，所以建议在配置 `kibana` 时只配置主节点就好。
不过在我们验证时可以**通过以下命令进行验证集群的搭建状况**
```bash
curl  -X GET http://localhost:9200/_cat/nodes #get请求查看集群健康状态

#将会响应如下，带星号的就是指向的主节点
127.0.0.1 69 93 1 0.06 0.07 0.06 dilm * es-master
127.0.0.1 69 93 1 0.06 0.07 0.06 dil  - es-node1
127.0.0.1 56 93 1 0.06 0.07 0.06 dil  - es-node2
```