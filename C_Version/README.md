# 淘宝自动购买器 - C语言版本

这是一个用C语言编写的淘宝自动购买器，可以帮助用户自动登录淘宝、添加商品到购物车、结算和提交订单。

## 功能特点

- 自动读取配置文件
- 简单的图形用户界面
- 支持配置多个商品和购买数量
- 支持代理服务器设置
- 提供详细的日志输出

## 系统要求

- Windows 操作系统
- MinGW 编译器（用于编译）
- Chrome 浏览器
- ChromeDriver（请确保版本与Chrome浏览器匹配）

## 编译方法

1. 确保已安装MinGW并将其添加到系统PATH中
2. 运行 `build.bat` 脚本进行编译
3. 编译成功后会生成 `main.exe` 可执行文件

## 配置方法

1. 打开 `DefaultConfig.txt` 文件
2. 修改以下配置项：
   - `username`: 淘宝账号用户名
   - `password`: 淘宝账号密码
   - `driver_path`: ChromeDriver的路径
   - `items`: 要购买的商品列表和数量
3. 保存配置文件

## 使用方法

1. 确保 `chromedriver.exe` 在同一目录下
2. 运行 `main.exe`
3. 程序会自动打开浏览器并执行购买流程
4. 部分操作可能需要手动确认（如验证码）

## 注意事项

1. 请确保ChromeDriver版本与您的Chrome浏览器版本匹配
2. 为了账号安全，请勿在公共电脑上保存密码
3. 使用本程序时请遵守淘宝的使用条款
4. 部分复杂操作可能需要手动完成

## 下载ChromeDriver

您可以从以下地址下载ChromeDriver：
https://chromedriver.chromium.org/downloads

请选择与您的Chrome浏览器版本匹配的ChromeDriver版本。

## 项目结构

- `main.c`: 主程序入口
- `config.c/h`: 配置文件处理模块
- `browser.c/h`: 浏览器操作模块
- `ui.c/h`: 用户界面模块
- `build.bat`: 编译脚本
- `DefaultConfig.txt`: 默认配置文件

## 许可证

本项目采用MIT许可证。详情请查看根目录下的 `License` 文件。