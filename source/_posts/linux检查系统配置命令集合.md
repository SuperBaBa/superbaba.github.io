---
title: Linux下查看CPU型号,内存大小,硬盘空间的命令
comments: true
date: 2019-09-21 18:13:13
categories:
	- linux之旅
tags:
thumbnail: /images/linux.jpg
---

#### 1. 查看CPU
1.1 查看CPU个数
```bash
$ cat /proc/cpuinfo | grep "physical id" | uniq | wc -l
```
 **uniq命令：删除重复行;wc –l命令：统计行数**

1.2 查看CPU核数
```bash
$ cat /proc/cpuinfo | grep "cpu cores" | uniq

cpu cores : 4
```
1.3 查看CPU型号
```bash
$ cat /proc/cpuinfo | grep 'model name' |uniq

model name : Intel(R) Xeon(R) CPU E5630 @ 2.53GHz
```


总结：该服务器有2个4核CPU，型号Intel(R) Xeon(R) CPU E5630 @ 2.53GHz
#### 2. 查看内存
2.1 查看内存总数
```bash
$ cat /proc/meminfo | grep MemTotal

MemTotal: 32941268 kB # 内存32G
```

#### 3. 查看硬盘
3.1 查看硬盘大小
```bash
$ fdisk -l | grep Disk
```

df -hl 查看磁盘剩余空间
 
df -h 查看每个根路径的分区大小
 
du -sh [目录名] 返回该目录的大小
 
du -sm [文件夹] 返回该文件夹总M数
 
du -h [目录名] 查看指定文件夹下的所有文件大小（包含子文件夹）

