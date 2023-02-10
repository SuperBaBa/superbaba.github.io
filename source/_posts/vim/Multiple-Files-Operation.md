---
title: Vim的光标移动
date: 2022-12-10 14:48:22
tags: Vim
categories: 开发工具
---
# 打开多个文件
在还没有开启vim时可能需要同时打开多个文件
```bash
vim file1 file2 file3
```

如果此时已经启动了vim可以在vim中继续打开其他文件
```bash
#打开文件file1
vim file1
#然后再file1命令模式下输入:e 打开文件/opt/file2
:e /opt/file2
```

当我们打开多个文件需要同时打开多个窗口时，使用vim编辑模式命令
```bash
#水平切分窗口
:sp 
#垂直切分窗口
:vsplist
```

# 文件之间切换
```bash
#上一个文件 
:bp
#下一个文件 
:bn
#列出打开的文件，带编号 
:ls
#切换至第n个文件 对于用(v)split在多个窗格中打开的文件，这种方法只会在当前窗格中切换不同的文件。 
:b1~n
``` 

# 窗口切换
Ctrl+w+方向键 —— 切换到前／下／上／后一个窗格 
Ctrl+w+h/j/k/l —— 同上 
Ctrl+ww —— 依次向后切换到下一个窗格中