# IFLOW 上下文文档

## 项目概述

`TaoBaoGoods` 是一个自动化购买淘宝商品的工具，包含 Python 脚本版本和 C 语言版本。它通过模拟用户操作来实现自动登录、添加商品到购物车、结算和提交订单等流程，旨在提高抢购商品的成功率。

### 主要特性

- 支持 Chrome 浏览器自动化
- 支持自动登录和自动下单
- 支持自定义商品链接、数量、抢购时间等参数
- 提供 Python 和 C 语言两个版本
- C 语言版本具有更快的执行速度和更低的资源占用

## 项目结构

```
TaoBaoGoods/
├── C_Version/                   # C 语言版本源代码
│   ├── browser.c                # 浏览器操作相关函数
│   ├── browser.h                # 浏览器操作相关头文件
│   ├── config.c                 # 配置文件加载和解析
│   ├── config.h                 # 配置相关头文件
│   ├── main.c                   # C 程序主入口
│   ├── ui.c                     # 用户界面实现
│   ├── ui.h                     # 用户界面相关头文件
│   ├── TaoBaoGoods.sln          # Visual Studio 解决方案文件
│   ├── TaoBaoGoods.vcxproj      # Visual Studio 项目文件
│   ├── build.bat                # Windows 批处理编译脚本
│   └── DefaultConfig.txt        # 默认配置文件
├── python_Version/              # Python 脚本版本
│   ├── config.yaml              # 配置文件
│   ├── main.py                  # Python 程序主文件
│   ├── requirements.txt         # Python 依赖包列表
│   ├── start.bat                # Windows 启动脚本
│   └── start.ps1                # PowerShell 启动脚本
├── DefaultConfig.yaml           # 默认配置文件 (Python 版本)
├── IFLOW.md                     # 项目上下文文档
├── README.MD                    # 项目说明文档
└── Licence                      # 许可证文件
```

## Python 版本

### 技术栈

- Python 3
- Selenium WebDriver (用于浏览器自动化)
- Tkinter (用于图形用户界面)
- PyYAML (用于配置文件解析)

### 配置文件

配置文件 `python_Version/config.yaml` 包含以下主要配置项：

- `driver_path`: ChromeDriver 路径
- `proxy`: 代理服务器地址
- `window_size`: 浏览器窗口大小
- `username`: 淘宝用户名
- `password`: 淘宝密码
- `items`: 商品列表 (包含 URL 和数量)
- `retry_times`: 下单失败重试次数
- `retry_interval`: 下单失败重试间隔 (秒)
- `continue_on_success`: 下单成功后是否继续
- `exit_on_failure`: 下单失败后是否退出程序

### 运行方式

1. 安装依赖: `pip install -r requirements.txt`
2. 配置 `config.yaml` 文件
3. 运行脚本: `python main.py` 或使用 `start.bat`/`start.ps1`

## C 语言版本

### 技术栈

- C 语言
- Win32 API (用于用户界面和进程管理)
- ChromeDriver (通过命令行启动)
- Visual Studio 2022 (开发环境)

### 配置文件

配置文件 `C_Version/DefaultConfig.txt` 包含以下主要配置项：

- `window_size`: 浏览器窗口大小
- `proxy`: 代理服务器地址
- `driver_path`: ChromeDriver 路径
- `username`: 淘宝用户名
- `password`: 淘宝密码
- `item`: 商品链接和数量 (可配置多个)

### 编译和运行

#### 使用 Visual Studio 2022:
1. 使用 Visual Studio 2022 打开 `C_Version\TaoBaoGoods.sln`
2. 选择 Debug 或 Release 模式并编译
3. 配置 `DefaultConfig.txt` 文件
4. 运行生成的可执行文件

#### 使用命令行编译:
1. 确保已安装 MinGW 或 Visual Studio Build Tools
2. 运行 `build.bat` 脚本进行编译
3. 配置 `DefaultConfig.txt` 文件
4. 运行生成的可执行文件

## 开发约定

- Python 版本使用面向对象的方式组织代码
- C 语言版本遵循模块化设计，将功能拆分到不同的源文件中
- 配置文件使用 YAML (Python) 和自定义格式 (C) 进行管理
- 使用日志记录程序运行状态和错误信息
- 提供图形用户界面显示程序状态
- 项目支持多平台编译 (x86, x64, ARM64)
- 使用 UTF-8 编码确保中文支持