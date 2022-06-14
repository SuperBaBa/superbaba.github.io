---
title: Maven -pl -am -amd 参数学习
date: 2022-06-14 13:00:00
categories: Maven
---
# 场景
每次我们在使用maven管理工程时，可能需要指定编译打包某一个模块，在此时我们就需要使用`-pl`参数来指定顶层pom的module
```bash
 +- simple-project-parent
 |  +- simple-service
 |  |  \- simple-core                                                     
 |  +- simple-web                                              
 |  |  +- simple-core    
 |  \- simple-core  
```
如上工程结构，如果我们可以发现 `simple-service`和 `simple-web` 这两个模块均依赖了`simple-core`，这时如果需要单独对`simple-web`进行编译打包部署，那么我们肯定会在`simple-parent`这个目录下的顶层pom执行`mvn clean install -Dmaven.test.skip=true`，这时将会对simple-parent所有的module做聚合操作，如果module实在太多也是一个相当漫长的过程，那么我们**能不能只编译打包自己想要的module呢？**

# 构建指定模块
参考Maven官网的 [maven cli option reference](https://maven.apache.org/ref/3-LATEST/maven-embedder/cli.html) 可以看到 `-pl`、`-am`、`-amd`三个参数


|Options|Description|简单理解|
|-- |-- |-- |
|`--am`, `--also-make`|	If project list is specified, also build projects required by the list | 指定构建工程后，工程所依赖的模块也会被构建|
|`--amd`, `--also-make-dependents`|	If project list is specified, also build projects that depend on projects on the list | 指定构建工程后，依赖这个工程的模块也会被构建|
|`-pl`, `--projects`|Comma-delimited list of specified reactor projects to build instead of all projects. A project can be specified by [groupId]:artifactId or by its relative path| 指定需要构建的模块，或者是pom的相对路径， 可以使用列表用逗号分隔|
|`--amd`, `--also-make-dependents`|	If project list is specified, also build projects that depend on projects on the list | 指定构建工程后，依赖这个工程的模块也会被构建|
|`-P`, `--activate-profiles`|Comma-delimited list of profiles to activate| 指定激活环境，如`mvn package -P prod`打包生产环境的包|
|`-N`, `--non-recursive`|Do not recurse into sub-projects|不使用递归构建|
|`-rf`, `--resume-from`|Resume reactor from specified project|根据指定的工程继续构建|

# Exmple
仍然使用上文中的`simple-project-parent`工程进行构建，依赖结构如上文不变

1. **构建指定模块并构建其依赖的所有工程**，在顶层pom(simple-project-parent目录下)中运行`mvn clean install -pl com.exmple:simple-web -am`, 可以看到
  - `simple-project-parent`被构建并安装到本地仓库
  - `simple-core`被构建并安装到本地仓库
  - `simple-web`被构建并安装到本地仓库
  - `simple-service`并不被`simple-web`依赖，因此并没有参与构建打包过程
  
> 命令中 com.exmple:simple-web可以改成simple-web，同一groupId无需再写groupId，直接写文件夹名也是可以的，如simple-web模块name是simple-web，但文件夹名为web，那么写web也是可以的

2. **构建指定模块，同时依赖指定工程的模块也进行构建**，在顶层pom(simple-project-parent目录下)中运行`mvn clean install -pl com.exmple:simple-core -amd`, 可以看到
  - `simple-core`被构建并安装到本地仓库
  - `simple-web`被构建并安装到本地仓库
  - `simple-service`被构建并安装到本地仓库
  - `simple-project-parent`并不依赖`simple-core`，因此不参与打包构建


3. **指定多个工程**，在顶层pom(simple-project-parent目录下)中运行`mvn clean install -pl simple-core,simple-service -amd`, 可以看到
  - `simple-core`被构建并安装到本地仓库
  - `simple-web`被构建并安装到本地仓库
  - `simple-service`被构建并安装到本地仓库
  - `simple-project-parent`并不依赖任何一个工程，因此不参与打包构建

4. **不递归构建**，在顶层pom(simple-project-parent目录下)中运行`mvn clean install -N`, 可以看到
  - `simple-project-parent`被构建并安装到本地仓库
  - 其他工程没有被父pom递归，不参与构建和打包

