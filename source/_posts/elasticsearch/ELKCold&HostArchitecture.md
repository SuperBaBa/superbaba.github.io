---
title: ELK冷热架构实现
date: 2021-11-14 20:22:12
tags: 
  - 文档型数据库
  - 全文搜索
  - NoSQL
categories: Elastcisearch  
---

[TOC]
在使用ELK做日志中心时，经常会遇到这种情况：
 - 今天的日志正在被频繁的索引，同时也有很频繁的搜索，**前几日的日志虽然没有那么频繁的搜索，但是也需要保存相当一段时间**。
 + 随着时间的推移，数据量越来越大，**需要去手动或使用定时任务删除一批数据**，释放出内存和磁盘空间
 + 索引越来越多，分片和segment不断增加，**ES为了快速访问磁盘上的索引文件，需要在内存中驻留一些数据**，即segment memory，大量的segment和segment memory占据着内存空间，同时也会消耗越来越多的CPU，分片过多带来的影响
 + 稍微熟悉ES的同学知道，**JVM heap分配不能超过32GB**，当我们一台机器配置128GB RAM, 48TB磁盘空间时，如果跑一个ES实例的话，那么只能用到**不到32GB Memory**，但是**磁盘可能保存的文件还不到10T**
 + 当用户做跨度较大的查询时，过多的磁盘IO和CPU消耗会对写入造成影响。
 + 想要聚合分析日志，**却发现日志中输出的字段无法定制化**，只能将日志这些个性化字段输出在某一个字段中
 > **扩展阅读**：
 > 当分片过多时，查询时汇总排序的数据将会引起过多的并发，过多并发带来的线程切换造成大量的CPU损耗；索引的删除和配置更新更慢可以参考这个[Issue#18776](https://github.com/elastic/elasticsearch/issues/18776);
 >
 > 过多的shard也带来更多小的segment，而过多的小segment会带来非常显著的heap内存消耗，特别是如果查询线程配置得很多的情况下。



# 冷热集群的搭建

对于日志或指标（metric）类时序性强的ES索引，因为数据量大，并且写入和查询大多都是近期时间内的数据。我们可以采用hot-warm-cold架构将索引数据切分成hot/warm/cold的索引。hot索引负责最新数据的读写，可使用内存存储；warm索引负责较旧数据的读取，可使用内存或SSD存储；cold索引很少被读取，可使用大容量磁盘存储。随着时间的推移，数据不断从hot索引->warm索引->cold索引迁移。针对不同阶段的索引我们还可以调整索引的主分片数，副本数，单分片的segment数等等，更好的利用机器资源。
![elk-clod-hot-architecture](https://images.marcus659.com/typora/elk-clod-hot-architecture.png)

# ILM生命周期的划分
ILM 一共将索引生命周期分为四个阶段(Phase)：

* __Hot 阶段__
    在这个阶段，它会不断地进行查询和写入(数据读写)，数据量也会不断增加(副本虽然可以提高查询速率但也会影响写入速度)。由于该阶段需要进行大量的数据读写，因此需要高配置的节点，一般建议将节点内存与磁盘比控制在 32 左右，比如 64GB 内存搭配 2TB 的 SSD 硬盘。

 * **Warm 阶段**
     Warm 阶段，基本不会再进行数据的索引，相对来说查询 `search` 回比较多一点。由于该阶段主要负责数据的读取，中等配置的节点即可满足需求，可以将节点内存与磁盘比提高到 64~96 之间，比如 64GB 内存搭配 4~6TB 的 HDD 磁盘。
     
* **Cold 阶段**
    Cold 阶段可类别比为人类中年到老年的阶段，在这个阶段，它退休了，在社会有需要的时候才出来输出下知识(数据读取)，大部分情况都是静静地待着。由于该阶段只负责少量的数据读取工作，低等配置的节点即可满足要求，可以将节点内存与磁盘比进一步提高到 96 以上，比如128，即 64GB 内存搭配 8 TB 的 HDD 磁盘。
    
* **Delete 阶段**
    Delete 阶段可类比为人类寿终正寝的阶段，在发光发热之后，静静地逝去，Rest in Peace~ILM 对于索引的生命周期进行了非常详细的划分，但它并不强制要求必须有这个4个阶段，用户可以根据自己的需求组合成自己的生命周期。
# Logstash读取数据
```bash
 output {
      elasticsearch {
//发生rollover时的写入索引的别名
        ilm_rollover_alias => "myindex"
//将会附在ilm_rollover_alias的值后面共同构成索引名，myindex-00001
        ilm_pattern => "00001"
//使用的索引策略
        ilm_policy => "my_policy"
//使用的索引模版名称
        template_name => "my_template"
      }
    }
```

# 索引生命周期管理


索引策略控制这一个索引的生命从Hot -> Warm -> Cold -> Delete 阶段，每个阶段都可以配置不同的转化行为（Action）。下面我们看下几个常用的Action:
Rollover
当写入索引达到了一定的大小，文档数量或创建时间时，Rollover可创建一个新的写入索引，将旧的写入索引的别名去掉，并把别名赋给新的写入索引。所以便可以通过切换别名控制写入的索引是谁。它可用于Hot阶段。
Shrink
减少一个索引的主分片数，可用于Warm阶段。需要注意的是当shink完成后索引名会由原来的<origin-index-name>变为shrink-<origin-index-name>.
Force merge
可触发一个索引分片的segment merge，同时释放掉被删除文档的占用空间。用于Warm阶段。
Allocate
可指定一个索引的副本数，用于warm, cold阶段。

## 索引模板创建
```bash
PUT _ilm/policy/my_policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
//rollover前距离索引的创建时间最大为7天
            "max_age": "7d",
//rollover前索引的最大大小不超过50G
            "max_size": "50G",
//rollover前索引的最大文档数不超过1个（测试用）
            "max_docs": 1,
          }
        }
      },
      "warm": {
//rollover之后进入warm阶段的时间不小于30天
        "min_age": "30d",
        "actions": {
          "forcemerge": {
//强制分片merge到segment为1
            "max_num_segments": 1
          },
          "shrink": {
//收缩分片数为1
            "number_of_shards": 1
          },
          "allocate": {
//副本数为2
            "number_of_replicas": 2
          }
        }
      },
      "cold": {
//rollover之后进入cold阶段的时间不小于60天
        "min_age": "60d",
        "actions": {
          "allocate": {
            "require": {
//分配到cold 节点，ES可根据机器资源配置不同类型的节点
              "type": "cold"
            }
          }
        }
      },
      "delete": {
//rollover之后进入cold阶段的时间不小于60天
        "min_age": "90d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}

```
```bash
PUT _template/my_template
{
//模版匹配的索引名以"index-"开头
  "index_patterns": ["myindex-*"],                 
  "settings": {
//索引分片数为2
    "number_of_shards":2 ,
//索引副本数为1 
    "number_of_replicas": 1,
//索引使用的索引策略为my_policy
    "index.lifecycle.name": "full_policy",    
//索引rollover后切换的索引别名为  test-alias
    "index.lifecycle.rollover_alias": "myindex"    
  }
}
```
```bash
PUT index-000001
{
  "aliases": {
    "myindex":{ //别名为 myindex
//允许索引被写入数据
      "is_write_index": true 
    }
  }
}
```
## 索引证明周期策略
# 日志结构化