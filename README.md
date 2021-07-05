# 简介
这是一个使用`Hexo`框架进行建站的工程，主要使用静态页面进行部署
# 步骤
1. 使用`git clone`命令从代码仓库拉取源码
```shell
git clone https://xxxxx.git
```

2. 安装`Hexo`框架脚手架
```bash
npm install -g hexo-cli
```
如果出现网络不好半天拉不下来，那么可以安装`cnpm`，并配置淘宝镜像
```shell
npm install cnpm --regitry=https://taobo.npm.com
```

3. 在已安装`npm`的前提下进行在本地代码仓库安装依赖
```shell
cnpm install
```

4. 执行`hexo server`命令访问本地`http://localhost:4000`
```bash
hexo server
```
