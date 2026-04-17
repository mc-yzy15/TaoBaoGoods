# TaoBaoGoods

`TaoBaoGoods` 当前主线为 Python 版本，本分支仅保留 Python 源码与相关配置。

## 仓库结构

- `src/`: Python 主线源码。
- `config/default.yaml`: 默认配置文件。
- `scripts/init.ps1`: 创建虚拟环境并安装项目。
- `scripts/start.ps1`: 启动入口，支持 `--config` 与 `--dry-run`。
- `tests/`: 单元测试。

## 初始化

```powershell
cd python_Version
.\scripts\init.ps1
```

## 启动

```powershell
cd python_Version
.\scripts\start.ps1
```

## Dry-run

```powershell
cd python_Version
.\scripts\start.ps1 --dry-run
```

## 配置

默认配置位于 `config/default.yaml`。

- `window_size`: 浏览器窗口大小，格式为 `宽,高`。
- `proxy`: 代理地址，留空表示不使用。
- `driver_path`: ChromeDriver 路径，支持绝对路径或 PATH 中的命令名。
- `items`: 商品列表，每项包含 `url` 和正整数 `quantity`。
- `username` / `password`: 可选，留空时可在运行时输入。

环境变量优先级高于配置文件：

- `TAOBAOGOODS_USERNAME`
- `TAOBAOGOODS_PASSWORD`

## 当前约束

- 真实淘宝页面选择器仍需要在真实站点上复核。
- `--dry-run` 只验证配置、入口和流程编排，不打开浏览器。
