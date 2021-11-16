---
title: Elasticsearch路由routing是个什么鬼
date: 2021-11-02 23:48:22
tags: 
  - 文档型数据库
  - 全文搜索
  - NoSQL
categories: Elastcisearch
---

[TOC]
# 什么是路由
routing的默认值是`文档id`，也可以是自定义值，根据`routing`计算出分片序号，并指定到该分片上。
索引文档时，文档会被存储到一个主分片下，其分片公式如下：
```bash
shard_num = hash(_routing) % num_primary_shards
```
由于`number_of_primary_shards`会参与路由的计算，因此主分片数量**一经指定就不能改变你**，会使routing值失效。

客户端查询请求时节点工作步骤
1. 请求被集群交给主节点
2. 主节点接收后，将请求广播到指定索引的每一个shard中
3. 每个分片执行搜索请求，并将结果返回
4. 结果在`主节点上`合并，排序后返回给用户

# 自定义路由
多数API均接收`routing`参数，如：`get`/`index`/`delete`/`bulk`/`update`/`mget`
强制使用路由，需要在`mapping`中指定路由 `require:true`
```bash
"mappings":{
    "_routing" : {
        "required" : true
      }
}
```
在写入文档时，即可配置路由
```bash
// 路由指定为 user1
PUT test-index/_doc/1?routing=user1
{
    "title":"母猪的保养",
    "city" : "漳州市",
    "county" : "红星区",
    "province" : "河北省",
}

// 查询时指定路由为 routing
GET test-index/_doc/1?routing=user1

// 或者在term查询时指定元数据 _routing 为 user1
GET my_index/_search
{
    "query": {
        "terms": {
        "_routing": [ "user1" ] 
         }
    }
}
```
在查询时，若强制使用路由的话，需要指定`routing`参数，否则会报错`routing_missing_exception`
```bash
GET test-index/_doc/111?routing=user1


# 返回响应如下
{
  "_index" : "test-index",
  "_type" : "_doc",
  "_id" : "111",
  "_version" : 1,
  "_seq_no" : 0,
  "_primary_term" : 1,
  "_routing" : "111",
  "found" : true,
  "_source" : {
    "title" : "母猪的保养",
    "city" : "漳州市",
    "county" : "红星区",
    "province" : "河北省",
 
  }
}
```
>**注意**：
>当使用自定义路由时，如果索引时使用`不同的_routing`，那么在`不同分片`上可能存在`相同的_id`。索引上所有分片文档`_id` 的唯一性由**用户自己保证**。


# 集群分片不平衡
通过API检查在使用`routing`路由时，每个分片是否均匀存储数据
```bash
GET _cat/shards
```
![es-routing-check-balance](https://images.marcus659.com/typora/es-routing-check-balance.png)

如果存在某些分片被指定存储的数据量过大时，可以使用 `index.routing_partition_size: 3`进行路由指定分片序号计算公式变更：
```bash
shard_num = (hash(_routing) + hash(_id) % routing_partition_size) % num_primary_shards
```
在设置`index_routing_partitino_size`需要注:
1. __`index_routing_partition_size` 的有效值__
`index_routing_partition_size` 在(`primary_shard_of_number`，`1`)这个开区间内，即`primary_shard_of_number` > `index_routing_partition_size`  > 1
2. 使用`index_routing_partition_size` 后存在如下限制
    * 无法创建 `join_field` 关系映射
    * `_routing` 必须开启
