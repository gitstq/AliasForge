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
  <strong>Lightweight Terminal Command Alias Intelligent Manager CLI</strong>
</p>

<p align="center">
  A powerful command-line tool for managing shell aliases with smart suggestions, usage statistics, and cross-shell sync
</p>

---

## 🎉 Introduction

**AliasForge** is a terminal command alias management tool designed specifically for developers. It solves pain points like scattered alias management, difficult cross-shell synchronization, and lack of usage insights, making your terminal workflow more efficient.

### 💡 Inspiration

In daily development, we often use various command aliases to improve efficiency. However, traditional alias management has these issues:
- 📝 Aliases scattered across configuration files, hard to manage uniformly
- 🔄 Difficult to sync between different shells (bash/zsh/fish)
- 📊 No way to know which aliases are actually used
- 💾 Lack of backup and recovery mechanisms

**AliasForge** was born to provide a one-stop alias management solution!

### ✨ Unique Features

| Feature | AliasForge | Traditional |
|---------|------------|-------------|
| 🎯 Unified Management | ✅ Centralized database | ❌ Scattered in config files |
| 📊 Usage Statistics | ✅ Track alias frequency | ❌ No statistics |
| 🔄 Cross-Shell Sync | ✅ Auto-detect and sync | ❌ Manual copy |
| 💡 Smart Suggestions | ✅ Recommend from history | ❌ No suggestions |
| 💾 Auto Backup | ✅ Backup on every change | ❌ No backup mechanism |

---

## ✨ Core Features

### 📝 Alias Management
- **➕ Add Alias** - Quickly create new aliases with descriptions, tags, and groups
- **✏️ Edit Alias** - Flexibly modify existing aliases
- **🗑️ Delete Alias** - Safe deletion with undo support
- **🔍 Search Alias** - Fuzzy search for quick location

### 🐚 Multi-Shell Support
- **Bash** - Perfect compatibility with `.bashrc`
- **Zsh** - Support for `.zshrc` configuration
- **Fish** - Adapted for Fish Shell syntax
- **🔄 Auto Sync** - One-click sync to current shell

### 📊 Smart Statistics
- **📈 Usage Tracking** - Record usage count for each alias
- **🏆 Top Aliases** - Know your most used commands
- **⚠️ Unused Alerts** - Discover redundant aliases

### 💡 Smart Suggestions
- **📜 History Analysis** - Analyze frequently used commands from shell history
- **🎯 Auto Suggestions** - Intelligently recommend aliases to create

### 💾 Data Security
- **🔄 Auto Backup** - Automatic backup on every modification
- **📤 Export** - Support YAML/JSON format export
- **📥 Import** - Easy migration and sharing

---

## 🚀 Quick Start

### 📋 Requirements

- **Python**: 3.8 or higher
- **OS**: Linux / macOS / Windows

### 📦 Installation

```bash
# Install with pip
pip install aliasforge

# Or install with pipx (recommended)
pipx install aliasforge
```

### 🎮 Basic Usage

```bash
# Show help
aliasforge --help

# Add alias
aliasforge add gs "git status" --desc "Show Git status" --tag git

# List all aliases
aliasforge list

# Search aliases
aliasforge search git

# Sync to shell config
aliasforge sync

# View usage statistics
aliasforge stats
```

---

## 📖 Detailed Usage Guide

### ➕ Add Alias

```bash
# Basic add
aliasforge add gs "git status"

# With description and tags
aliasforge add ll "ls -la" --desc "List all files with details" --tag file --tag ls

# Specify shell and group
aliasforge add dc "docker-compose" --shell bash --group docker
```

### 📋 List Aliases

```bash
# List all
aliasforge list

# Filter by group
aliasforge list --group git

# Filter by tag
aliasforge list --tag docker

# Show detailed info
aliasforge list --all
```

### 🔍 View and Search

```bash
# View single alias details
aliasforge show gs

# Search aliases
aliasforge search git
```

### ✏️ Edit and Delete

```bash
# Edit alias
aliasforge edit gs --command "git status -s"
aliasforge edit gs --desc "Show short Git status"

# Delete alias
aliasforge delete gs
aliasforge delete gs --force  # Skip confirmation
```

### 🔄 Sync to Shell

```bash
# Auto-detect current shell and sync
aliasforge sync

# Specify shell
aliasforge sync --shell zsh
```

After syncing, run the following command to apply changes:

```bash
# Bash
source ~/.bashrc

# Zsh
source ~/.zshrc

# Fish
source ~/.config/fish/config.fish
```

### 📊 View Statistics

```bash
# View last 30 days statistics
aliasforge stats

# Specify days
aliasforge stats --days 7
```

### 💡 Smart Suggestions

```bash
# Suggest aliases from command history
aliasforge suggest

# Set minimum usage count
aliasforge suggest --min-count 5
```

### 📤 Import/Export

```bash
# Export as YAML
aliasforge export aliases.yaml

# Export as JSON
aliasforge export aliases.json --format json

# Import from file
aliasforge import aliases.yaml
```

### 💾 Backup Management

```bash
# Create backup
aliasforge backup create --desc "Backup before major changes"

# List backups
aliasforge backup list

# Restore from backup
aliasforge backup restore 1
```

---

## 💡 Design Philosophy & Roadmap

### 🏗️ Technical Architecture

```
AliasForge
├── cli.py          # CLI entry point (Click)
├── core/
│   ├── database.py     # SQLite data storage
│   ├── alias_manager.py # Alias management logic
│   └── stats.py        # Statistics analysis module
└── utils/              # Utility functions
```

### 🎯 Technology Choices

| Component | Choice | Reason |
|-----------|--------|--------|
| CLI Framework | Click | Mature, stable, active community |
| Terminal UI | Rich | Beautiful, powerful, zero dependencies |
| Data Storage | SQLite | Lightweight, no extra services needed |
| Config Format | YAML | Human readable, easy to edit |

### 🗓️ Future Roadmap

- [ ] **v1.1** - Add TUI interactive interface
- [ ] **v1.2** - Support remote sync (Git/Gist)
- [ ] **v1.3** - Integrate AI smart naming suggestions
- [ ] **v1.4** - Support team alias library sharing
- [ ] **v2.0** - Web management interface

---

## 📦 Build & Deployment Guide

### Local Development

```bash
# Clone repository
git clone https://github.com/gitstq/AliasForge.git
cd AliasForge

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Build distribution package
pip install build
python -m build
```

### Publish to PyPI

```bash
# Install twine
pip install twine

# Upload to PyPI
twine upload dist/*
```

---

## 🤝 Contributing

We welcome all forms of contributions!

### Submit PR

1. Fork this repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add some feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Create Pull Request

### Submit Issue

If you find a bug or have a feature suggestion, please [create an Issue](https://github.com/gitstq/AliasForge/issues), we'll handle it as soon as possible.

### Commit Convention

Use [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code refactoring
- `test:` Test related

---

## 📄 License

This project is open-sourced under the **MIT License**. You are free to:

- ✅ Commercial use
- ✅ Modify code
- ✅ Distribute copies
- ✅ Private use

The only requirement is to retain the original copyright notice.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>

<p align="center">
  If this project helps you, please give it a ⭐ Star!
</p>
