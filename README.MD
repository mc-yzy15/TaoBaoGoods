# TaoBaoGoods

## 项目简介

`TaoBaoGoods` 是一个可以帮助用户抢购淘宝商品的工具，包括 Python 脚本版本和 C 语言版本。该工具使用自动化技术实现购买流程，支持 Chrome 浏览器。通过自动化操作，用户可以在商品上架后立即下单，提高抢购成功率。

## 特性

- 支持 Chrome 浏览器
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
- C 语言版本提供简洁的用户界面
- C 语言版本提供更快的执行速度和更低的资源占用

## 安装步骤

>**以下命令均需使用powershell执行（.bat为双击运行）**

### 安装ChromeDriver

1. 下载ChromeDriver，并解压到任意目录，[参考这位大佬的教程](https://blog.csdn.net/zhoukeguai/article/details/113247342)
2. 将解压后的文件夹重命名为`chromedriver`，并移动到`C:\Windows\System32`目录下或本项目目录下（python_Version\.venv\Lib\site-packages\selenium\webdriver\chrome\chromedriver`）
3. 验证是否安装成功：打开powershell，输入`chromedriver --version`，如果返回版本号，则安装成功

### Python 脚本版本

1. **安装 Python3**: 确保您的系统上已安装 python3。可以从 [python 官网](https://python.org/) 下载并安装。
1.2 **打开powershell，输入`python --version`，如果返回版本号，则安装成功**
2. **克隆仓库**: 使用 Git 克隆本项目到本地。

   ```powershell
   git clone "https://github.com/mc-yzy15/TaoBaoGoods.git"
   cd TaoBaoGoods
3. **安装依赖**: 进入项目目录后，安装所需的依赖包。

   ```powershell
   .\init.ps1
   ```

### 使用 EXE 版本

1. **下载**: 下载 release 中的 `TaoBaoAutoBuyer.exe` 文件。(或下载 `TaoBaoAutoBuyer.zip`并[解压](https://blog.csdn.net/BidaWaves/article/details/142530432))
2. **配置EXE**: 打开 `TaoBaoAutoBuyer.exe`，点击配置并填入账号密码及商品链接。
3. **使用EXE**: 打开即用。

### 使用说明

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

### C 语言版本使用说明

#### 系统要求
- Windows 10/11 操作系统
- Visual Studio 2022（社区版、专业版或企业版）
- Chrome 浏览器和对应版本的 ChromeDriver

#### 编译方法
1. **安装 Visual Studio 2022**：确保安装了 C/C++ 开发工具和 Windows SDK
2. **打开解决方案**：使用 Visual Studio 2022 打开 `C_Version\TaoBaoAutoBuyer.sln`
3. **选择配置**：在顶部菜单栏选择 Debug 或 Release 模式
4. **编译项目**：点击 "生成" -> "生成解决方案" 或按 F7 快捷键

#### 编译结果
- Debug 模式生成的可执行文件：`C_Version\Debug\TaoBaoAutoBuyer.exe`
- Release 模式生成的可执行文件：`C_Version\Release\TaoBaoAutoBuyer.exe`

#### 配置方法
1. 编辑 `C_Version\DefaultConfig.txt` 文件
2. 配置项说明：
   ```
   window_size=1280,720  # 浏览器窗口大小
   proxy=  # 代理地址（可选）
   driver_path=chromedriver.exe  # ChromeDriver路径
   username=your_username  # 淘宝用户名
   password=your_password  # 淘宝密码
   item=https://detail.tmall.com/item.htm?id=1234567890,2  # 商品链接和数量
   ```

#### 使用方法
1. 确保 ChromeDriver 与您的 Chrome 浏览器版本匹配
2. 将 ChromeDriver 放置在与可执行文件相同的目录下或设置正确的路径
3. 双击运行编译后的可执行文件
4. 程序将自动启动浏览器并执行购买流程

## 贡献指南

欢迎任何形式的贡献！如果您有任何建议或发现 bug，请提交 issue 或 pull request。

## 致谢

本项目基于 [Python](https://www.python.org/) 编写，感谢 [Python](https://www.python.org/) 的开源社区。

## 联系我们

如果您有任何问题或建议，欢迎联系我们。

1. 邮箱：[yingmoliuguang@yeah.net](mailto:yingmoliuguang@yeah.net)

## 许可证

本项目采用 [GPLv3.0 许可证](Licence)。
