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

   ```powershell
   git clone "https://github.com/mc-yzy15/TaoBaoGoods.git"
   cd TaoBaoGoods
3. **安装依赖**: 进入项目目录后，安装所需的依赖包。

   ```powershell
   .\init.py
   ```

### 使用 EXE 版本

1. **下载**: 下载 release 中的 `TaoBaoAutoBuyer.exe` 文件。
2. **配置EXE**: 打开 `TaoBaoAutoBuyer.exe`，点击配置并填入账号密码及商品链接。
3. **使用EXE**: 打开即用。

### 使用说明

>**以下命令均需使用powershell执行**

#### python 脚本版本

配置脚本: 根据需要修改 config.yaml 文件中的配置项，如淘宝账号、密码、目标商品链接等。

##### 淘宝自动购买器配置文件说明

以下是对 `config.yaml` 文件中各个配置项的详细说明：

| 配置项            | 说明                                                                 |
|-------------------|----------------------------------------------------------------------|
| driver_path       | ChromeDriver路径。请确保路径正确指向你的ChromeDriver可执行文件。     |
| proxy             | 代理服务器地址（格式：`http://your.proxy.address:port`）。如果不需要使用代理，可以留空。 |
| window_size       | 浏览器窗口大小（格式：`宽度,高度`），例如：`1920,1080`。            |
| username          | 淘宝用户名。请填写你用于登录淘宝的用户名。                           |
| password          | 淘宝密码。请填写你用于登录淘宝的密码。                               |
| items             | 商品列表。每个商品包含一个URL和数量。                                |
| retry_times       | 下单失败重试次数。当下单失败时，程序将重试指定次数。                 |
| retry_interval    | 下单失败重试间隔（秒）。每次重试之间的时间间隔。                      |
| continue_on_success | 下单成功后是否继续尝试下单其他商品。值为`true`或`false`。           |
| exit_on_failure   | 下单失败后是否退出程序。值为`true`或`false`。                         |

### 示例配置文件 (`config.yaml`)

```yaml
driver_path: 'path/to/chromedriver'  # ChromeDriver路径
proxy: 'http://your.proxy.address:port'  # 代理地址
window_size: '1920,1080'  # 浏览器窗口大小
username: 'your_username'  # 淘宝用户名
password: 'your_password'  # 淘宝密码
items:
  - url: 'https://detail.tmall.com/item.htm?id=1234567890'
    quantity: 2
  # 添加更多商品
retry_times: 3  # 下单失败重试次数
retry_interval: 5  # 下单失败重试间隔（秒）
continue_on_success: true  # 下单成功后继续下单
exit_on_failure: false  # 下单失败后退出程序
```

运行脚本: 使用以下命令启动脚本。

```powershell
.\start.ps1
```

#### EXE 版本

配置EXE: 打开 EXE 点击配置并填入账号密码及商品链接。

使用EXE：打开即用

## 贡献指南

欢迎任何形式的贡献！如果您有任何建议或发现 bug，请提交 issue 或 pull request。

## 许可证

本项目采用 [GPLv3.0 许可证](Licence)。
