---
title: git reset 三种模式
comments: true
date: 2021-12-26 21:23:16
categories: 开发工具
tags:
  - Git
thumbnail: /images/artilce-banner/git.jpg
---
有时候我们在commit提交代码后，发现这一次commit的内容是有错误的，那么有两种处理方法：
1. 修改错误内容，再次commit一次
2. 使用git reset 命令撤销这一次错误的commit
第一种方法比较直接，但会多次一次commit记录。第二种方法会直接清楚错误的commit，由此咱们也可以知道`git reset`是一个让HEAD指针指向其他方向的命令。

# git reset 有哪三种模式
- reset --hard
```bash
git reset --hard
```
不保留工作目录和暂存区，使用这个模式，在重置HEAD和branch的同时，也会重置 stage 和 working tree 中的内容，也就是放弃掉你当前已commit或未commit的所有变动
![modify HEAD](https://images.marcus659.com/typora/gitreset-soft-01.gif)
- reset --soft
```bash
git reset --soft
```
保留工作目录，并把重置 HEAD 所带来的新的差异放进暂存区
- reset --mixed
```bash
git reset --mixed
```
保留工作目录，并清空暂存区



