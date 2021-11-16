---
title: git add 相关命令学习
comments: true
date: 2019-09-22 10:56:32
categories: 开发工具
tags:
  - Git
thumbnail: /images/artilce-banner/git.jpg
---
[TOC]
# git add -A 和 git add . 的区别
* git add -A  提交**所有变化**
(git add --all 的缩写)
&emsp;
* git add -u  提交被**修改(modified)** 和被 **删除(deleted)** 文件，不包括新文件(new)
(git add --update 的缩写)
&emsp;
* git add   提交 **新文件(new)** 和被 **修改(modified)**  文件，不包括被删除(deleted)文件
<!--more-->