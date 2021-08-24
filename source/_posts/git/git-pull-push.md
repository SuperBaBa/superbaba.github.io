---
title: git push/pull 远程库学习
comments: true
date: 2019-09-22 10:56:16
categories:
	- Git手札
tags:
thumbnail: /images/artilce-banner/git.jpg
---
# git push/pull 远程库学习
git push 命令用于将本地分支更新，推送到远程主机。
```shell
$ git push <远程主机名> <本地分支名>:<远程分支名>
```
**注意** ： 分支推送顺序写法是<来源地>:<目的地>
* git pull 是<远程分支>:<本地分支>
* git push 是<本地分支>:<远程分支>
### 常用
1.本地分支与远程分支存在追踪关系
```shell
$ git push origin master
```
以上命令，将本地master分支推送到origin主机的master分支。
&nbsp;
2.省略本地分支
```shell
$ git push origin :master
# 等同于
$ git push origin --delete master
```
以上推送一个空的本地分支到远程分支，表示删除远程分支
&nbsp;
3.使用-u选项制定一个默认主机，这样在后面就可以不添加任何参数，使用git push
```shell
$ git push -u origin master
```
以上表示将本地的master分支推送到origin主机，同时指定origin为默认主机，
