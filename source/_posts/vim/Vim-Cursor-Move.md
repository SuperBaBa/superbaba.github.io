---
title: Vim的光标移动
date: 2021-11-10 14:48:22
tags: vim
categories: 开发工具
---
[TOC]
# 单位级
`h` 向左一字符
`j` 下一行
`k` 上一行
`l` 向右一字符
# 单词级
`w` or `W` 向右移动到下一单词开头
`e` or `E` 向右移动到单词结尾
`b` or `B` 向左移动到单词开头
>**注意**：所有小写单词都是以分词符作为单词界限，大写字母以空格作为界限

>在下面字符块中感受一下各种移动吧！
This project's GitHub url is https://github.com/dofy/learn-vimPlease clone it to your local folder and open the first file which isnamed file-one.md via following command "vim file-one.md"and welcome to http://geekpark.net :)
# 块级
`gg` 到文档第一行
`G` 到文档最后一行
`0` 到行首（第 1 列）
`^` 到第一个非空白字符
`$` 到行尾
`Ctrl-d`    向下移动半页
`Ctrl-u`    向上移动半页
`Ctrl-f `    向下移动一页
`Ctrl-b`    向上移动一页
`:<N>` or `<N>gg` 跳转到第 N 行
`:+<N>` or `<N>j` 向下跳 N 行
`:-<N>` or `<N>k` 向上跳 N 行
>注意：
所有命令前都可以加一个数字 N，表示对后面的命令执行 N 次，例如你想向下移动 3 行，除了
可以用 :+3 之外，还可以用 3j 来实现同样的效果。
另外，上面实际上有两种命令：
一种是键入后
立即执行的，比如 gg；
还有一种是先输入 : 的（后面还会出现先按 / 的），这类命令需要在
输入完成后按回车执行，后面的教程中也是一样。

# 简单设置 vim
`:set number` 显示行号
`:set relativenumber` 显示相对行号（这个非常重要，慢慢体会）
`:set hlsearch` 搜索结果高亮
`:set autoindent` 自动缩进
`:set smartindent` 智能缩进
`:set tabstop=4` 设置 tab 制表符所占宽度为 4
:set softtabstop=4 设置按 tab 时缩进的宽度为 4
:set shiftwidth=4 设置自动缩进宽度为 4
:set expandtab 缩进时将 tab 制表符转换为空格
:filetype on 开启文件类型检测
:syntax on 开启语法高亮