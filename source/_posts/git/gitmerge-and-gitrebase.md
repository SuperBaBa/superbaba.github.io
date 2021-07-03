---
title: git merge命令解析
comments: true
date: 2019-09-22 10:56:45
categories: 开发工具
tags:
  - Git
thumbnail: /images/artilce-banner/git.jpg
---
[TOC]
## git-merge用途：
1. 用于git-pull中，来整合另一代码仓库中的变化（即：git pull = git fetch + git merge）
2. 用于从一个分支到另一个分支的合并
>警告：运行git-merge时含有大量的未commit文件很容易让你陷入困境，这将使你在冲突中难以回退。因此非常不鼓励在使用git-merge时存在未commit的文件，建议使用git-stash命令将这些未commit文件暂存起来，并在解决冲突以后使用git stash pop把这些未commit文件还原出来。


