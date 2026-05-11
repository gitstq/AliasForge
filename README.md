<p align="center">
  <a href="README.md">简体中文</a> | <a href="README_TW.md">繁體中文</a> | <a href="README_EN.md">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey.svg" alt="Platform">
</p>

<h1 align="center">⚡ AliasForge</h1>

<p align="center">
  <strong>轻量级终端命令别名智能管理器 CLI</strong>
</p>

<p align="center">
  一款强大的命令行工具，用于管理 Shell 别名，具备智能推荐、使用统计、跨 Shell 同步等功能
</p>

---

## 🎉 项目介绍

**AliasForge** 是一款专为开发者设计的终端命令别名管理工具。它解决了命令别名管理混乱、难以跨 Shell 同步、缺乏使用洞察等痛点，让你的终端工作流程更加高效。

### 💡 灵感来源

在日常开发中，我们经常需要使用各种命令别名来提高效率。然而，传统的别名管理方式存在以下问题：
- 📝 别名分散在各个配置文件中，难以统一管理
- 🔄 不同 Shell（bash/zsh/fish）之间同步困难
- 📊 无法了解哪些别名真正被使用
- 💾 缺乏备份和恢复机制

**AliasForge** 应运而生，提供一站式别名管理解决方案！

### ✨ 自研差异化亮点

| 特性 | AliasForge | 传统方式 |
|------|------------|----------|
| 🎯 统一管理 | ✅ 集中式数据库管理 | ❌ 分散在配置文件 |
| 📊 使用统计 | ✅ 追踪别名使用频率 | ❌ 无统计功能 |
| 🔄 跨Shell同步 | ✅ 自动识别并同步 | ❌ 手动复制 |
| 💡 智能推荐 | ✅ 从历史命令推荐 | ❌ 无推荐功能 |
| 💾 自动备份 | ✅ 每次修改自动备份 | ❌ 无备份机制 |

---

## ✨ 核心特性

### 📝 别名管理
- **➕ 添加别名** - 快速创建新别名，支持描述、标签、分组
- **✏️ 编辑别名** - 灵活修改已有别名
- **🗑️ 删除别名** - 安全删除，支持撤销
- **🔍 搜索别名** - 模糊搜索，快速定位

### 🐚 多Shell支持
- **Bash** - 完美兼容 `.bashrc`
- **Zsh** - 支持 `.zshrc` 配置
- **Fish** - 适配 Fish Shell 语法
- **🔄 自动同步** - 一键同步到当前 Shell

### 📊 智能统计
- **📈 使用频率追踪** - 记录每个别名的使用次数
- **🏆 热门别名排行** - 了解最常用的命令
- **⚠️ 未使用提醒** - 发现冗余别名

### 💡 智能推荐
- **📜 历史分析** - 从 Shell 历史中分析常用命令
- **🎯 自动建议** - 智能推荐可创建的别名

### 💾 数据安全
- **🔄 自动备份** - 每次修改自动创建备份
- **📤 导出功能** - 支持 YAML/JSON 格式导出
- **📥 导入功能** - 轻松迁移和分享

---

## 🚀 快速开始

### 📋 环境要求

- **Python**: 3.8 或更高版本
- **操作系统**: Linux / macOS / Windows

### 📦 安装

```bash
# 使用 pip 安装
pip install aliasforge

# 或使用 pipx 安装（推荐）
pipx install aliasforge
```

### 🎮 基本使用

```bash
# 查看帮助
aliasforge --help

# 添加别名
aliasforge add gs "git status" --desc "显示 Git 状态" --tag git

# 列出所有别名
aliasforge list

# 搜索别名
aliasforge search git

# 同步到 Shell 配置
aliasforge sync

# 查看使用统计
aliasforge stats
```

---

## 📖 详细使用指南

### ➕ 添加别名

```bash
# 基本添加
aliasforge add gs "git status"

# 带描述和标签
aliasforge add ll "ls -la" --desc "列出所有文件详情" --tag file --tag ls

# 指定 Shell 和分组
aliasforge add dc "docker-compose" --shell bash --group docker
```

### 📋 列出别名

```bash
# 列出所有
aliasforge list

# 按分组筛选
aliasforge list --group git

# 按标签筛选
aliasforge list --tag docker

# 显示详细信息
aliasforge list --all
```

### 🔍 查看和搜索

```bash
# 查看单个别名详情
aliasforge show gs

# 搜索别名
aliasforge search git
```

### ✏️ 编辑和删除

```bash
# 编辑别名
aliasforge edit gs --command "git status -s"
aliasforge edit gs --desc "简短显示 Git 状态"

# 删除别名
aliasforge delete gs
aliasforge delete gs --force  # 跳过确认
```

### 🔄 同步到 Shell

```bash
# 自动检测当前 Shell 并同步
aliasforge sync

# 指定 Shell
aliasforge sync --shell zsh
```

同步后，运行以下命令使配置生效：

```bash
# Bash
source ~/.bashrc

# Zsh
source ~/.zshrc

# Fish
source ~/.config/fish/config.fish
```

### 📊 查看统计

```bash
# 查看最近 30 天统计
aliasforge stats

# 指定天数
aliasforge stats --days 7
```

### 💡 智能推荐

```bash
# 从命令历史推荐别名
aliasforge suggest

# 设置最小使用次数
aliasforge suggest --min-count 5
```

### 📤 导入导出

```bash
# 导出为 YAML
aliasforge export aliases.yaml

# 导出为 JSON
aliasforge export aliases.json --format json

# 从文件导入
aliasforge import aliases.yaml
```

### 💾 备份管理

```bash
# 创建备份
aliasforge backup create --desc "重大更新前备份"

# 列出备份
aliasforge backup list

# 从备份恢复
aliasforge backup restore 1
```

---

## 💡 设计思路与迭代规划

### 🏗️ 技术架构

```
AliasForge
├── cli.py          # CLI 入口（Click）
├── core/
│   ├── database.py     # SQLite 数据存储
│   ├── alias_manager.py # 别名管理逻辑
│   └── stats.py        # 统计分析模块
└── utils/              # 工具函数
```

### 🎯 技术选型

| 组件 | 选择 | 理由 |
|------|------|------|
| CLI 框架 | Click | 成熟稳定，社区活跃 |
| 终端 UI | Rich | 美观强大，零依赖 |
| 数据存储 | SQLite | 轻量级，无需额外服务 |
| 配置格式 | YAML | 人类可读，易于编辑 |

### 🗓️ 后续迭代计划

- [ ] **v1.1** - 添加 TUI 交互界面
- [ ] **v1.2** - 支持远程同步（Git/Gist）
- [ ] **v1.3** - 集成 AI 智能命名建议
- [ ] **v1.4** - 支持团队别名库共享
- [ ] **v2.0** - Web 管理界面

---

## 📦 打包与部署指南

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/gitstq/AliasForge.git
cd AliasForge

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v

# 构建分发包
pip install build
python -m build
```

### 发布到 PyPI

```bash
# 安装 twine
pip install twine

# 上传到 PyPI
twine upload dist/*
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 提交 PR

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: 添加某某功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 提交 Issue

如果发现 Bug 或有功能建议，请[创建 Issue](https://github.com/gitstq/AliasForge/issues)，我们会尽快处理。

### 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关

---

## 📄 开源协议说明

本项目基于 **MIT 协议** 开源，您可以自由地：

- ✅ 商业使用
- ✅ 修改代码
- ✅ 分发副本
- ✅ 私人使用

唯一要求是保留原始版权声明。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>

<p align="center">
  如果这个项目对你有帮助，请给一个 ⭐ Star 支持一下！
</p>
