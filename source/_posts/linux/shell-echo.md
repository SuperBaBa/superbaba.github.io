---
title: echo命令常用方法总结
comments: true
date: 2019-09-21 16:11:27
categories: shell
tags:
  - Linux
thumbnail: /images/linux.jpg
---
[TOC]

echo 用于字符串的输出。命令格式：
```bash
echo string

# 不带-e选项的 echo，将 \n 认为是普通字符；
[roc@roclinux ~]$ echo "Hello World\n"
Hello World\n
# 使用了-e选项的 echo，会将 \n 认为是换行符。
[roc@roclinux ~]$ echo -e "Hello World\n"
Hello World
```
<!--more-->
## echo用于显示变量
```bash
#我们定义了一个变量, 叫作str
[roc@roclinux ~]$ str="Hello World"
 
#在echo后面加上str变量, 照样可以显示出来
[roc@roclinux ~]$ echo "$str, good morning"
Hello World, good morning
```
## echo 后面的引号

|输入命令|输出内容|解 释|
|--|--|--|
|echo '$USER * $(date)'|$USER * $(date)|单引号无视所有特殊字符，所有字符在它眼里 都是普通字符，都是芸芸众生
|echo "$USER * $(date)"|root * Thu Feb 25 12:03:48 CST 2016|双引号会无视文件通配符，但“$”、“\”、 会起作用，我管它们叫“美金”、“砍刀”、 “硫酸雨”
|echo $USER * $(date)|root book others Thu Feb 25 12:03:48 CST 2016|$USER 被翻译了 root, * 被翻译成了当前目录下的目录结构
## 在 Shell 中显示色彩
```bash
echo -e "\033[颜色1;颜色2m 要展示的文字 \033[0m"
```

格式详解：
* -e选项：表示允许反斜杠（对字符）转义。
* \033[颜色1；颜色2m：称为**                                                                                  转义序列**，它本身是一个整体，中间不要有空格。
* \033[：转义序列的开始。其中\033代表Esc符号，也可以使用\E或\e来代替。
* 颜色1和颜色2：表示字体的前景色或背景色，至于颜色1和颜色2哪一个表示前景色，哪一个表示背景色，由其设定的数值来决定，前景色和背景色的数值空间是不同的。
* m：转义序列的终止标志。
*  \033[0m：表示将颜色恢复回原来的配色。


|色彩| 黑 | 红 | 绿 | 黄|  蓝 |洋红|青|白|
|--- | --- | --- | --- |--- | --- | --- | --- |---|
|前景色|30|31|32|33|34|35|36|37|
|背景色|40|41|42|43|44|45|46|47|

