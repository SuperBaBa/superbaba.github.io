---
title: 安全并正确地重启Elasticsearch集群
date: 2021-11-14 23:48:22
tags: 
  - 文档型数据库
  - 全文搜索
  - NoSQL
categories: Elastcisearch
---

[TOC]
# 前言
elasticsearch本身具有高可用性，可以做到停机不停服务，在重启elasticsearch后可能存在数据丢失，或者是“启动ES后，怎么一直有大量的数据在迁移？”
# 问题原因其本质
**原因有两点：**
1. ES中的数据``不是实时写入``磁盘的。
数据进入ES后先进入data buffer `segment`和`transientLog`这两个buffer，（此处又涉及到数据防丢失的机制）然后进入操作系统文件系统缓存的数据段，最后再特定时机（两个条件，一个是segment到达容量，一个是到达refresh时间间隔）下才刷入磁盘。即在内存中有很多数据是没写入磁盘的。
2. ES的分片自动分配迁移机制。
当集群发现经过`一分钟`后（index.unassigned.node_left.delayed_timeout参数设置）还连接不上某个节点，就会把集群内的数据重新进行分布，即使后来节点重新连接上，原来的数据因为重新分布也无效了。


# 提前准备
1. 检查废弃日志查看你使用的所有废弃功能，并更新相关的代码
2. 检阅Elasticsearch的迭代变更，并对代码和新版本的配置有必要更改的地方进行更改
3. 如果你有使用插件，确保每一个插件能够兼容新版本的Elasticsearch
4. 在升级生产环境的Elasticsearch集群之前，需要在一个独立的环境测试一下升级更新
5. 通过快照`snapshot`的形式进行备份


# 准备重启集群


设置集群重新分配的类型，使用`cluster.routing.allocation.enable`设置选项。

启用或禁用分片重新分配的类型：
- `all` - (默认) 允许所有类型分片重新分配.
- `primaries` - 只允许主分片重新分配.
- `new_primaries` - 只允许新索引的主分片重新分配.
- `none` - 所有索引的任何类型分片不被允许重新分配.

1. 关闭分片分配
```http
PUT _cluster/settings{
  "persistent": {
    "cluster.routing.allocation.enable": "none"
    }
}
```
2. 停止索引并执行同步刷新
```http
POST _flush/synced
```
3. 暂时停止机器学习和数据仓库相关任务
```bash
curl -X POST "localhost:9200/_ml/set_upgrade_mode?enabled=true&pretty"

# 或者是
POST /_ml/set_upgrade_mode?enabled=true&pretty
```
4. 关闭所有节点
* 如果是通过`systemd`运行的Elastiseach
```bash
sudo systemctl stop elasticsearch.service
```
* 如果是用SysV的`init`运行Elasticsearch
```bash
sudo -i service elasticsearch stop
```
* 如果是通过`守护进程(daemon)`运行elasticsearch
```bash
kill $(cat pid)
```

5. 执行完更改动作后开始重启elasticsearch
```bash
cd  $ES_HOME/bin ./elasticsearch -d -p $ES_HOME/pid.txt
```

6. ，启用分片自动分布

```http
PUT _cluster/settings { 
    "persistent": {
        "cluster.routing.allocation.enable": null }
}
```





# 更新集群
* 使用 Debian 或者 RPM 包进行更新:
使用`rpm`或者`dpkg`全装新包，所有文件安装将会被安装到操作系统上合适的位置，并且**elasticsearch的配置文件将会被保留**，不会被覆盖。
&emsp;
*  使用 ` zip` 或者是`tar` 压缩包进行更新:
    1. 解压压缩包到一个新的或指定的目录，如果你没有使用外部指定的 `config`
    2. 如果**不需要使用外部**的 `config`目录和 `jvm.options`，可以复制旧版本的配置文件目录到新安装的配置文件目录。
    如果**需要指定外部**的 `config`目录和 `jvm.options`则需要配置环境变量`ES_PATH_CONF` Elasticsearch启动时将会在环境脚本`elasticsearch-env` 中进行调用，如下图：
    ![update-es-configuration](https://images.marcus659.com/typora/update-es-configuration.png)
    3. 在`elasticsearch.yml`中配置指定`path.data` ，即指定外部data目录路径，如果不使用外部指定`data`目录，可以把外部data目录复制到新安装的目录中。
    
    >如果使用了监控功能，当你更新elasticsearch集群并要`复用`监控数据时，监控时通过辨认经过持久化的节点`UUID`（独一无二的）进行区分的，这个`UUID`值存储在`data目录里`
