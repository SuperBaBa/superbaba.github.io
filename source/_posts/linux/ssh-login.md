---
title: ssh-login
date: 2022-04-29 13:06:10
tags:
---
# What's SSH
  SSH(Secure Shell)是一种**应用层网络协议**(OSI七层网络模型)，与FTP（文件传送协议）、Telnet（远程登录协议）、DNS（域名解析协议）、SMTP（邮件传送协议），POP3协议（邮局协议），HTTP协议（Hyper Text Transfer Protocol）等协议一样，用于提供安全的 用于计算机之间的加密登录。如果一个用户从本地计算机，使用SSH协议登录另一台远程计算机，我们就可以认为，这种登录是安全的，即使被中途截获，密码也不会泄露。

  SSH只是一种协议，存在多种实现，既有商业实现，也有开源实现。本文针对的实现是OpenSSH，它是自由软件，应用非常广泛，这里只讨论SSH的登录方式，其他用法后续文章中讨论。如果要在Windows系统中使用SSH可以安装OpenSSH，
  可以[单击此处](https://docs.microsoft.com/zh-cn/windows-server/administration/openssh/openssh_install_firstuse)查看OpenSSH的是使用文档。

  > 最早的时候，互联网通信都是明文通信，一旦被截获，内容就暴露无疑。1995年，芬兰学者Tatu Ylonen设计了SSH协议，将登录信息全部加密，成为互联网安全的一个基本解决方案，迅速在全世界获得推广，目前已经成为Linux系统的标准配置。

# SSH登录过程
  1. TCP三次握手后进行SSH协议版本协商
  2. 服务端收到用户的登录请求，把自己的公钥发给用户
  3. 客户端获取到公钥，并使用MD5计算出一个128位的公钥指纹，让用户确认是否是真实主机(这就是为什么登录时需要输入yes/no进行确认)
  4. 加密算法协商后，客户端使用这个公钥，将登录密码加密后，发送到服务端
  5. 服务器端收到后用自己的私钥解密后得到用户名密码，与本地密码对比，如果密码正确，就同意用户登录。

  在上述过程中还是会发生中间人攻击的风险，(***如果有时间或条件后续可更新***)由于没有像HTTPS一样的第三方证书中心，如果被登录请求被拦截后，中间攻击人可能会发送自己伪造的公钥给客户端，客户端再进行密码输入，那么在中间人再通过伪造公钥对应的私钥进行解密，那么密码就暴露于光天化日之下，安全性荡然无存。

# SSH的基本用法-登录
  ## 口令登录
  假设你要以用户名user，登录远程主机为 login.test.com
  ```shell
  ssh user@login.test.com 

  #接下来会让用户确认公钥指纹，如下：
  The authenticity of host \'host (login.test.com)\' can\'t be established.
  RSA key fingerprint is 98:3e:d7:e0:de:9e:ac:67:28:c2:42:2d:37:16:58:4d.
　Are you sure you want to continue connecting (yes/no)?

  #输入yes后在输入登录口令即可
  Password: (enter password)

  ```
  如果确认远程主机(服务端)是用户所需要的登录的机器，那么远程主机的公钥将会保存在`$HOME/.ssh/konwn_hosts`文件中，可以根据远程主机的域名或者IP定位到保存的公钥，**下次再登录同一台远程主机的时候就无需再确认公钥指纹了**

  假设服务端设置的ssh协议端口为2324
  ```shell
  ssh user@login.test.com -p 2324
  ```

  假设客户端(用户主机)当前用户为logger，需要使用服务端(远程主机)logger用户进行登录
  ```shell
  #无需在前面添加user用户名
  ssh login.test.com 
  ```


  ## 公钥登录(免密登录)
  公钥登录免去了每次输入口令的麻烦，可以通过`ssh user@host`命令直接登录，无需输入密码。原理：**客户端将自己公钥存储在服务端`$HOME/.ssh/authorized_keys`，登录是服务端会响应一串随机字符串，客户端使用私钥加密后，远程主机使用公钥进行解密，若成功则允许登录**
