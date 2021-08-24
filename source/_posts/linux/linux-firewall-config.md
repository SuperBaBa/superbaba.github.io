---
title: CentOS 7.0的是firewall防火墙设置
comments: true
date: 2019-09-21 18:17:54
categories:
	- linux之旅
tags:
thumbnail: /images/linux.jpg
---

CentOS 7.0默认使用的是firewall作为防火墙，使用iptables必须重新设置一下
1. 直接关闭防火墙
&emsp;
```bash
systemctl stop firewalld.service #停止firewall
```
&emsp;
```bash
systemctl disable firewalld.service #禁止firewall开机启动
```
<!--more-->
&emsp;
```bash
firewall-cmd --state #查看状态，running 表示运行
```
&emsp;
在不改变状态的条件下重新加载防火墙：
```bash
firewall-cmd --reload
```
&emsp;

启用某个服务 
```bash
firewall-cmd --zone=public --add-service=https #临时

firewall-cmd --permanent --zone=public --add-service=https #永久
```

开启某个端口
```bash
firewall-cmd --permanent --zone=public --add-port=8080-8081/tcp //永久

firewall-cmd --zone=public --add-port=8080-8081/tcp //临时
```
使用命令加载设置
```bash
firewall-cmd --reload
```
查看开启的端口和服务
```bash
firewall-cmd --permanent --zone=public --list-services 
#服务空格隔开   

例如 dhcpv6-client https ss

firewall-cmd --permanent --zone=public --list-ports
#端口空格隔开 

例如 8080-8081/tcp 8388/tcp 80/tcp
```
设置某个ip 访问某个服务
```bash
firewall-cmd --permanent --zone=public --add-rich-rule="rule family="ipv4" source address="192.168.0.4/24" service name="http" accept"

#ip 192.168.0.4/24 访问 http
```
删除上面设置的规则
```bash
firewall-cmd --permanent --zone=public --remove-rich-rule="rule family="ipv4" source address="192.168.0.4/24" service name="http" accept"
```
检查设定是否生效
```
iptables -L -n | grep 21
```
```
ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:21 ctstate NEW
```
执行命令
```
firewall-cmd --list-all
```
显示：
```
public (default)
  interfaces:
  sources:
  services: dhcpv6-client ftp ssh
  ports:
  masquerade: no
  forward-ports:
  icmp-blocks:
  rich rules:
```
  
查询服务的启动状态
```
firewall-cmd --query-service ftp
yes
firewall-cmd --query-service ssh
yes
firewall-cmd --query-service samba
no
firewall-cmd --query-service http
no
```
&emsp;
&emsp;
2. 设置
iptables serviceyum -y install iptables-services
如果要修改防火墙配置，
如增加防火墙端口3306
vi /etc/sysconfig/iptables 增加规则-A INPUT -m state --state NEW -m tcp -p tcp --dport 3306 -j ACCEPT保存退出后
```bash
systemctl restart iptables.service 
#重启防火墙使配置生效
systemctl enable iptables.service 
#设置防火墙开机启动最后重启系统使设置生效即可。
```