---
title: Linux之间文件传输scp
comments: true
date: 2019-09-21 18:11:09
categories: shell
tags:
  - Linux
thumbnail: /images/linux.jpg
---

把本地的source.txt文件拷贝到192.168.0.10机器上的/home/work目录下
```bash
scp /home/work/source.txt work@192.168.0.10:/home/work/ 
```
把192.168.0.10机器上的source.txt文件拷贝到本地的/home/work目录下
```bash
scp work@192.168.0.10:/home/work/source.txt /home/work/ 
```
把192.168.0.10机器上的source.txt文件拷贝到192.168.0.11机器的/home/work目录下
```bash
scp work@192.168.0.10:/home/work/source.txt work@192.168.0.11:/home/work/ 
```
拷贝文件夹，加-r参数
```bash
scp -r /home/work/sourcedir work@192.168.0.10:/home/work/ 
```