# TaoBaoGoods Python Mainline

## Layout

- `src/taobaogoods/`: Python source code.
- `config/default.yaml`: single source of truth for the default config.
- `scripts/init.ps1`: creates `.venv` and installs the project.
- `scripts/start.ps1`: runs the packaged entrypoint with `--config` and `--dry-run` support.
- `tests/`: unit tests for config loading, path resolution, and flow orchestration.

## Runtime notes

- The Python implementation is the only maintained automation mainline.
- `TAOBAOGOODS_USERNAME` and `TAOBAOGOODS_PASSWORD` override values in the YAML config.
- If credentials are missing from both the environment and the config, the app prompts at runtime.
- `--dry-run` validates configuration and flow wiring without opening Chrome.
