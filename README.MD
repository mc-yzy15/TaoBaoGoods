# TaoBaoGoods

**版本 1.2.5** | 淘宝自动购 · 深度防检测版

`TaoBaoGoods` 是一款基于 Selenium 的淘宝自动化购物流程工具，内置 **Flet 图形界面**（默认）和纯 CLI 模式，集成多重反检测措施。

## 功能特性

- **Flet 图形界面**（默认）：现代化 GUI，配置编辑 + 实时运行状态面板
- **纯 CLI 模式**：无需桌面环境，脚本化运行
- **深度反检测**：WebGL/Canvas/navigator 等指纹随机化，模拟真实浏览器环境
- **定时抢购**：支持指定时间自动提交订单（CLI：`--purchase-time`）
- **Dry-Run**：无需打开浏览器，验证配置和流程完整性
- **商品管理 GUI**：图形化添加/编辑/删除待购商品
- **凭据灵活管理**：支持配置文件、环境变量、运行时输入三种方式

## 仓库结构

```
TaoBaoGoods/
├── src/                      # Python 源码
│   ├── __init__.py           # 包入口，版本信息
│   ├── __main__.py           # python -m src 入口
│   ├── app.py                # 核心应用逻辑
│   ├── browser_session.py    # Selenium 浏览器会话
│   ├── cli.py                # CLI 入口 + Flet GUI 启动
│   ├── config.py             # 配置加载与校验
│   ├── gui.py                # Flet 图形界面（默认交互方式）
│   ├── paths.py              # 路径管理
│   ├── stealth.py            # 反检测措施（WebGL/Canvas 伪造等）
│   └── status.py             # 状态输出抽象
├── config/
│   └── default.yaml          # 默认配置文件
├── scripts/
│   ├── init.ps1              # 创建虚拟环境并安装
│   └── start.ps1             # 启动入口（支持 --config / --dry-run）
├── tests/                    # 单元测试
├── docs/
│   └── README.md             # 项目文档（用于 PyPI 等分发平台）
├── AGENTS.md                 # AI agent 项目指南
├── pyproject.toml            # setuptools 构建配置
└── requirements.txt          # pip 依赖
```

## 初始化

```powershell
.\scripts\init.ps1
```

## 启动

默认启动 Flet 图形界面（推荐）：

```powershell
.\scripts\start.ps1
```

纯 CLI 模式（无需桌面环境）：

```powershell
.\scripts\start.ps1 --cli
.\scripts\start.ps1 --cli --dry-run
```

指定配置文件：

```powershell
.\scripts\start.ps1 --config config\default.yaml
```

## CLI 定时抢购

```powershell
.\scripts\start.ps1 --cli --purchase-time "2026-04-20 10:00:00"
```

## 配置

默认配置位于 `config/default.yaml`。

```yaml
window_size: "1280,720"       # 浏览器窗口大小
proxy: ""                      # 代理地址，如 http://127.0.0.1:7890
driver_path: "chromedriver.exe" # ChromeDriver 路径（绝对或 PATH 中的命令名）
username: ""                   # 淘宝用户名，留空则运行时输入
password: ""                   # 淘宝密码，留空则运行时输入
items:
  - url: "https://item.taobao.com/item.htm?id=xxxx"
    quantity: 1                # 购买数量
```

### 环境变量

环境变量优先级高于配置文件：

| 变量名 | 说明 |
|--------|------|
| `TAOBAOGOODS_USERNAME` | 淘宝用户名 |
| `TAOBAOGOODS_PASSWORD` | 淘宝密码 |

## 反检测技术

- **WebGL 指纹伪造**：vendor/renderer/parameter 随机化，返回 Intel Iris OpenGL Engine
- **Canvas 指纹噪声**：自动在 `toDataURL`/`getImageData` 中注入随机噪声
- **navigator 属性伪造**：languages/webgl/plugins/permissions/hardwareConcurrency 等
- **Chrome 运行时模拟**：完整模拟 `window.chrome` 对象
- **网络环境模拟**：connection/effectiveType/rtt 等参数伪造
- **人类行为模拟**：随机延迟、随机偏移点击、随机滚动

## 当前约束

- 真实淘宝页面选择器需要在真实站点上复核，页面更新后可能需要调整。
- `--dry-run` 只验证配置、入口和流程编排，不打开浏览器。
- 滑块验证码触发时需手动在浏览器中完成验证。

## 技术栈

- Python ≥ 3.10
- **Flet** 0.27+（GUI 框架）
- Selenium 4.x + selenium-stealth
- PyYAML
- setuptools (pyproject.toml)
