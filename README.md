# 🚀 TMUX Ultimate Configuration Generator

**The complete interactive solution for creating the perfect tmux configuration for Linux power users.**

## 🎯 Overview

This tool provides an interactive questionnaire-based approach to generate a comprehensive, personalized tmux configuration. Instead of manually researching and configuring hundreds of tmux options, answer a series of targeted questions and get a production-ready `.tmux.conf` file tailored to your workflow.

## ✨ Features

### 🔧 Core Configuration Areas
- **Prefix Key Options** - Choose from popular alternatives or set custom
- **Mouse Support** - Enable/disable mouse interaction  
- **Color Schemes** - Built-in themes (Dracula, Nord, Gruvbox, Solarized, Catppuccin)
- **Status Bar** - Customizable layout and information display

### 🎨 Appearance & Theming
- **Multiple Color Schemes** with carefully selected palettes
- **Status Bar Customization** - Position, content, and styling
- **256 Color & True Color Support** for modern terminals
- **Pane Border Styling** to match your theme

### ⚙️ Behavior & Performance  
- **History Buffer Configuration** - Set scrollback limits
- **Window Management** - Indexing, naming, renumbering
- **Performance Optimizations** for responsive operation

### 🏗️ Advanced Integrations
- **Vim Integration** - Navigation and copy-mode bindings
- **Plugin Management** - TPM support with popular plugins
- **System Clipboard** - Copy/paste integration
- **Terminal Mode** - Emacs or Vi key bindings

### 🔌 Plugin Ecosystem
- **TPM (Tmux Plugin Manager)** integration
- **Pre-configured Popular Plugins**:
  - tmux-sensible (better defaults)
  - tmux-resurrect (session persistence) 
  - tmux-continuum (automatic saving)
  - tmux-copycat (enhanced search)
  - tmux-yank (clipboard integration)
  - tmux-sidebar (file browser)
  - System monitoring plugins (battery, CPU, network)

## 🚀 Quick Start

### Prerequisites
- Python 3.6+
- tmux 2.6+ (recommended)
- Linux/macOS environment

### Installation & Usage

1. **Clone or download** the repository
2. **Run the main script**:
   ```bash
   python3 tmux_ultimate.py
   ```
3. **Follow the interactive menu**:
   - Choose option 3 for complete setup
   - Or run questionnaire (1) then generator (2) separately

4. **Apply the configuration**:
   ```bash
   cp tmux.conf ~/.tmux.conf
   tmux source-file ~/.tmux.conf
   ```

### Plugin Setup (if enabled)
```bash
# Install TPM
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

# Install plugins (from within tmux)
# Press: Prefix + I
```

## 📋 Configuration Categories

### 🔧 Core Settings
- Prefix key selection (Ctrl+B, Ctrl+A, Ctrl+Space, or custom)
- Mouse support toggle
- Reload key binding

### 🎨 Appearance
- **Color Schemes**: Default, Dracula, Nord, Gruvbox, Solarized, Catppuccin
- Status bar position (top/bottom)
- Date/time display options
- Hostname display
- Session name visibility

### ⚙️ Behavior
- History buffer size (1K-50K lines)
- Automatic window renaming
- Window renumbering on close
- Base index for windows/panes

### 🖥️ Terminal Integration  
- 256 color support
- True color (24-bit) support
- Key binding mode (Emacs/Vi)

### 🏗️ Vim Integration
- Vim-style pane navigation (h,j,k,l)
- Vim-style copy mode bindings
- Vim-compatible key mappings

### 🔌 Plugins
- TPM integration
- Curated plugin selection
- Automatic plugin configuration

### 🚀 Advanced Features
- System clipboard integration
- Pane synchronization
- Session logging
- Custom key bindings

## 📁 Generated Files

- `tmux_config.json` - Questionnaire responses
- `tmux.conf` - Generated tmux configuration
- Comprehensive comments and documentation

## 🎨 Color Schemes

### Dracula Theme
- Background: `#282a36`
- Foreground: `#f8f8f2` 
- Accent: `#bd93f9` (purple)

### Nord Theme
- Background: `#2e3440`
- Foreground: `#d8dee9`
- Accent: `#5e81ac` (blue)

### Gruvbox Theme
- Background: `#282828`
- Foreground: `#ebdbb2`
- Accent: `#d65d0e` (orange)

### Solarized Theme
- Background: `#002b36`
- Foreground: `#839496`
- Accent: `#268bd2` (blue)

### Catppuccin Theme
- Background: `#1e1e2e`
- Foreground: `#cdd6f4`
- Accent: `#cba6f7` (mauve)

## 🔧 Key Bindings

### Default Bindings (customizable)
- `Prefix + r` - Reload configuration
- `Prefix + |` - Split horizontally  
- `Prefix + -` - Split vertically
- `Alt + arrows` - Navigate panes without prefix

### Vim Mode (if enabled)
- `Prefix + h/j/k/l` - Navigate panes
- `Prefix + H/J/K/L` - Resize panes
- Vi-style copy mode selection

## 🔍 Example Configurations

### Minimal Setup
- Default colors
- Basic key bindings
- Mouse support
- Essential settings only

### Power User Setup
- Custom color scheme
- Vim integration
- Multiple plugins
- Advanced key bindings
- System integration

### Developer Setup
- IDE-like features
- Session management
- Clipboard integration
- Monitoring plugins

## 🆘 Troubleshooting

### Common Issues

**Tmux not found**
```bash
# Ubuntu/Debian
sudo apt install tmux

# CentOS/RHEL
sudo yum install tmux

# macOS
brew install tmux
```

**Colors not working**
- Ensure terminal supports 256 colors
- Check `$TERM` environment variable
- Verify terminal-specific color settings

**Plugins not loading**
- Ensure TPM is installed correctly
- Check plugin installation path
- Verify tmux version compatibility

**Key bindings not working**
- Check for conflicting bindings
- Verify prefix key is correctly set
- Test bindings after reload

### Version Compatibility
- Tmux 2.6+: Full feature support
- Tmux 2.1-2.5: Most features supported
- Tmux <2.1: Limited compatibility

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional color schemes
- More plugin integrations  
- Windows/WSL support
- Advanced automation features

## 📚 Resources

- [Tmux Manual](https://man.openbsd.org/tmux.1)
- [Tmux Wiki](https://github.com/tmux/tmux/wiki)
- [TPM Documentation](https://github.com/tmux-plugins/tpm)
- [Tmux Plugin List](https://github.com/tmux-plugins/list)

## 📄 License

MIT License - feel free to use, modify, and distribute.

---

**Created for Linux power users who want tmux configured right the first time.** 🚀