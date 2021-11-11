# VS Code 开发 Java 指南

  在进行开发时，如果你厌倦了使用EditPlus开发，那么必然需要选择一个IDE(Integrated Development Environment )，也就是集成开发环境，通常大家耳熟听过的有`InteillJ Idea`、`Eclipse`、`MyEclipse`，这些开发工具，其中我觉得最好用的当属`Idea`莫属，特别它的旗舰版，其中只有旗舰版才有的**`Diagram`**功能让我每次查看类关系时，屡试不爽，不仅清晰明了还能当做png图片进行导出，上图感受下。

![Diagram](http://images.marcus659.com/typora/idea-digram01.gif)

## 配置Java开发支持

首先我们必须得安装VS Code 和 Java开发环境，这两个配置就不在此处赘述了，无论是解压缩安装还是二进制安装都可以，此处只分享进行Java开发必须装的插件扩展。

- [Language Support for Java(TM) by Red Hat](https://marketplace.visualstudio.com/items?itemName=redhat.java)
- [Debugger for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-debug)
- [Java Test Runner](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-test)
- [Maven for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-maven)
- [Project Manager for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-dependency)
- [Visual Studio IntelliCode](https://marketplace.visualstudio.com/items?itemName=VisualStudioExptTeam.vscodeintellicode)

这些插件都是进行Java开发必须要的，在vscode打开的情况下，可以点击这里[一键安装](vscode:extension/vscjava.vscode-java-pack)所有扩展包。当然如果你不想安装这么多，也可以分开安装，其中`Language Support for Java(TM) by Red Hat`和`Debugger for Java`这两个扩展是需要安装的，不然可能无法支持Java程序编译、代码高亮、代码补全等开发必要功能