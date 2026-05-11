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
  <strong>輕量級終端命令別名智慧管理器 CLI</strong>
</p>

<p align="center">
  一款強大的命令列工具，用於管理 Shell 別名，具備智慧推薦、使用統計、跨 Shell 同步等功能
</p>

---

## 🎉 專案介紹

**AliasForge** 是一款專為開發者設計的終端命令別名管理工具。它解決了命令別名管理混亂、難以跨 Shell 同步、缺乏使用洞察等痛點，讓你的終端工作流程更加高效。

### 💡 靈感來源

在日常開發中，我們經常需要使用各種命令別名來提高效率。然而，傳統的別名管理方式存在以下問題：
- 📝 別名分散在各個設定檔中，難以統一管理
- 🔄 不同 Shell（bash/zsh/fish）之間同步困難
- 📊 無法了解哪些別名真正被使用
- 💾 缺乏備份和恢復機制

**AliasForge** 應運而生，提供一站式別名管理解決方案！

### ✨ 自研差異化亮點

| 特性 | AliasForge | 傳統方式 |
|------|------------|----------|
| 🎯 統一管理 | ✅ 集中式資料庫管理 | ❌ 分散在設定檔 |
| 📊 使用統計 | ✅ 追蹤別名使用頻率 | ❌ 無統計功能 |
| 🔄 跨Shell同步 | ✅ 自動識別並同步 | ❌ 手動複製 |
| 💡 智慧推薦 | ✅ 從歷史命令推薦 | ❌ 無推薦功能 |
| 💾 自動備份 | ✅ 每次修改自動備份 | ❌ 無備份機制 |

---

## ✨ 核心特性

### 📝 別名管理
- **➕ 新增別名** - 快速建立新別名，支援描述、標籤、分組
- **✏️ 編輯別名** - 靈活修改已有別名
- **🗑️ 刪除別名** - 安全刪除，支援撤銷
- **🔍 搜尋別名** - 模糊搜尋，快速定位

### 🐚 多Shell支援
- **Bash** - 完美相容 `.bashrc`
- **Zsh** - 支援 `.zshrc` 設定
- **Fish** - 適配 Fish Shell 語法
- **🔄 自動同步** - 一鍵同步到當前 Shell

### 📊 智慧統計
- **📈 使用頻率追蹤** - 記錄每個別名的使用次數
- **🏆 熱門別名排行** - 了解最常用的命令
- **⚠️ 未使用提醒** - 發現冗餘別名

### 💡 智慧推薦
- **📜 歷史分析** - 從 Shell 歷史中分析常用命令
- **🎯 自動建議** - 智慧推薦可建立的別名

### 💾 資料安全
- **🔄 自動備份** - 每次修改自動建立備份
- **📤 匯出功能** - 支援 YAML/JSON 格式匯出
- **📥 匯入功能** - 輕鬆遷移和分享

---

## 🚀 快速開始

### 📋 環境要求

- **Python**: 3.8 或更高版本
- **作業系統**: Linux / macOS / Windows

### 📦 安裝

```bash
# 使用 pip 安裝
pip install aliasforge

# 或使用 pipx 安裝（推薦）
pipx install aliasforge
```

### 🎮 基本使用

```bash
# 查看說明
aliasforge --help

# 新增別名
aliasforge add gs "git status" --desc "顯示 Git 狀態" --tag git

# 列出所有別名
aliasforge list

# 搜尋別名
aliasforge search git

# 同步到 Shell 設定
aliasforge sync

# 查看使用統計
aliasforge stats
```

---

## 📖 詳細使用指南

### ➕ 新增別名

```bash
# 基本新增
aliasforge add gs "git status"

# 帶描述和標籤
aliasforge add ll "ls -la" --desc "列出所有檔案詳情" --tag file --tag ls

# 指定 Shell 和分組
aliasforge add dc "docker-compose" --shell bash --group docker
```

### 📋 列出別名

```bash
# 列出所有
aliasforge list

# 按分組篩選
aliasforge list --group git

# 按標籤篩選
aliasforge list --tag docker

# 顯示詳細資訊
aliasforge list --all
```

### 🔍 查看和搜尋

```bash
# 查看單個別名詳情
aliasforge show gs

# 搜尋別名
aliasforge search git
```

### ✏️ 編輯和刪除

```bash
# 編輯別名
aliasforge edit gs --command "git status -s"
aliasforge edit gs --desc "簡短顯示 Git 狀態"

# 刪除別名
aliasforge delete gs
aliasforge delete gs --force  # 跳過確認
```

### 🔄 同步到 Shell

```bash
# 自動偵測當前 Shell 並同步
aliasforge sync

# 指定 Shell
aliasforge sync --shell zsh
```

同步後，執行以下命令使設定生效：

```bash
# Bash
source ~/.bashrc

# Zsh
source ~/.zshrc

# Fish
source ~/.config/fish/config.fish
```

### 📊 查看統計

```bash
# 查看最近 30 天統計
aliasforge stats

# 指定天數
aliasforge stats --days 7
```

### 💡 智慧推薦

```bash
# 從命令歷史推薦別名
aliasforge suggest

# 設定最小使用次數
aliasforge suggest --min-count 5
```

### 📤 匯入匯出

```bash
# 匯出為 YAML
aliasforge export aliases.yaml

# 匯出為 JSON
aliasforge export aliases.json --format json

# 從檔案匯入
aliasforge import aliases.yaml
```

### 💾 備份管理

```bash
# 建立備份
aliasforge backup create --desc "重大更新前備份"

# 列出備份
aliasforge backup list

# 從備份恢復
aliasforge backup restore 1
```

---

## 💡 設計思路與迭代規劃

### 🏗️ 技術架構

```
AliasForge
├── cli.py          # CLI 入口（Click）
├── core/
│   ├── database.py     # SQLite 資料儲存
│   ├── alias_manager.py # 別名管理邏輯
│   └── stats.py        # 統計分析模組
└── utils/              # 工具函數
```

### 🎯 技術選型

| 元件 | 選擇 | 理由 |
|------|------|------|
| CLI 框架 | Click | 成熟穩定，社群活躍 |
| 終端 UI | Rich | 美觀強大，零依賴 |
| 資料儲存 | SQLite | 輕量級，無需額外服務 |
| 設定格式 | YAML | 人類可讀，易於編輯 |

### 🗓️ 後續迭代計劃

- [ ] **v1.1** - 新增 TUI 互動介面
- [ ] **v1.2** - 支援遠端同步（Git/Gist）
- [ ] **v1.3** - 整合 AI 智慧命名建議
- [ ] **v1.4** - 支援團隊別名庫共享
- [ ] **v2.0** - Web 管理介面

---

## 📦 打包與部署指南

### 本地開發

```bash
# 複製儲存庫
git clone https://github.com/gitstq/AliasForge.git
cd AliasForge

# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
pytest tests/ -v

# 建立分發套件
pip install build
python -m build
```

### 發布到 PyPI

```bash
# 安裝 twine
pip install twine

# 上傳到 PyPI
twine upload dist/*
```

---

## 🤝 貢獻指南

我們歡迎所有形式的貢獻！

### 提交 PR

1. Fork 本儲存庫
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'feat: 新增某某功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 建立 Pull Request

### 提交 Issue

如果發現 Bug 或有功能建議，請[建立 Issue](https://github.com/gitstq/AliasForge/issues)，我們會儘快處理。

### 提交規範

使用 [Conventional Commits](https://www.conventionalcommits.org/) 規範：

- `feat:` 新功能
- `fix:` Bug 修復
- `docs:` 文檔更新
- `refactor:` 程式碼重構
- `test:` 測試相關

---

## 📄 開源協議說明

本專案基於 **MIT 協議** 開源，您可以自由地：

- ✅ 商業使用
- ✅ 修改程式碼
- ✅ 分發副本
- ✅ 私人使用

唯一要求是保留原始版權聲明。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>

<p align="center">
  如果這個專案對你有幫助，請給一個 ⭐ Star 支持一下！
</p>
