# TaoBaoGoods

## 项目简介

`TaoBaoGoods` 是一个可以帮助用户抢购淘宝商品的工具，包括 Python 脚本版本和 EXE 版本。该工具使用 Selenium 和 ChromeDriver 实现自动化购买，支持 Chrome 和 Firefox 浏览器。通过自动化操作，用户可以在商品上架后立即下单，提高抢购成功率。

## 特性

- 支持 Chrome 和 Firefox 浏览器
- 支持自动登录和自动下单
- 支持自定义商品链接和数量
- 支持自定义抢购时间
- 支持自定义浏览器窗口大小
- 支持自定义浏览器代理
- 支持自定义下单数量
- 支持自定义下单间隔
- 支持自定义下单失败重试次数
- 支持自定义下单失败重试间隔
- 支持自定义下单成功后继续下单
- 支持自定义下单失败后退出程序
- 支持自定义下单失败后继续下单

## 安装步骤

### Python 脚本版本

1. **安装 Python3**: 确保您的系统上已安装 python3。可以从 [python 官网](https://python.org/) 下载并安装。
2. **克隆仓库**: 使用 Git 克隆本项目到本地。

   ```bash
   git clone https://github.com/yourusername/TaoBaoGoods.git
   cd TaoBaoGoods
3. **安装依赖**: 进入项目目录后，安装所需的依赖包。

### 使用 EXE 版本

1. **下载**: 下载release 中的exe文件。
2. **安装依赖**: 使用依赖包管理工具安装依赖。

### 使用说明

#### python 脚本版本

配置脚本: 根据需要修改 config.py 文件中的配置项，如淘宝账号、密码、目标商品链接等。

运行脚本: 使用以下命令启动脚本。

```bash
python main.py
```

#### EXE 版本

配置EXE: 打开 EXE 点击配置并填入账号密码及商品链接。

使用EXE：打开即用

## 贡献指南

欢迎任何形式的贡献！如果您有任何建议或发现 bug，请提交 issue 或 pull request。

## 许可证

本项目采用 [GPLv3.0 许可证](Licence)。
