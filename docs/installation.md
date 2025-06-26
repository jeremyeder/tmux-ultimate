---
sidebar_position: 2
---

# Installation

## Prerequisites

Before installing tmux-ultimate, ensure you have the following installed:

### Required
- **Python 3.11+**: The questionnaire tool is written in Python
- **tmux 2.1+**: The terminal multiplexer we're configuring
- **Git**: To clone the repository

### Recommended
- **tmux 3.0+**: For best feature compatibility
- **A terminal with true color support**: For optimal color scheme display

## Installation Methods

### Method 1: Clone from GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/jeremyeder/tmux-ultimate.git

# Navigate to the directory
cd tmux-ultimate

# Make the script executable (optional)
chmod +x tmux_ultimate.py
```

### Method 2: Download ZIP

1. Go to the [GitHub repository](https://github.com/jeremyeder/tmux-ultimate)
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file to your desired location

## Verify Installation

Test that everything is working:

```bash
# Check Python version
python3 --version

# Check tmux version
tmux -V

# Test the questionnaire tool
python3 tmux_ultimate.py --help
```

## System-Specific Setup

### Ubuntu/Debian

```bash
# Install required packages
sudo apt update
sudo apt install python3 tmux git

# Optional: Install newer tmux version from PPA
sudo add-apt-repository ppa:kelleyk/tmux
sudo apt update
sudo apt install tmux
```

### CentOS/RHEL/Fedora

```bash
# Install required packages
sudo dnf install python3 tmux git

# Or for older versions:
sudo yum install python3 tmux git
```

### macOS

```bash
# Using Homebrew
brew install python tmux git

# Or using MacPorts
sudo port install python3 tmux git
```

## TPM Installation

tmux-ultimate can automatically install TPM (Tmux Plugin Manager) for you, but you can also install it manually:

```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

## Post-Installation

1. **Backup existing configuration** (if you have one):
   ```bash
   cp ~/.tmux.conf ~/.tmux.conf.backup
   ```

2. **Run the questionnaire**:
   ```bash
   python3 tmux_ultimate.py
   ```

3. **Start or reload tmux**:
   ```bash
   # Start a new session
   tmux new-session

   # Or reload existing configuration
   tmux source-file ~/.tmux.conf
   ```

## Next Steps

After installation:

1. **Run the questionnaire**: `python3 tmux_ultimate.py`
2. **Learn the interface**: [Usage Guide](usage.md)
3. **Explore plugins**: [Plugin Management](plugins.md)
4. **Get help if needed**: [Troubleshooting Guide](troubleshooting.md)