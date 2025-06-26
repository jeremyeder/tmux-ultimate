---
sidebar_position: 3
---

# Usage Guide

## Basic Usage

The simplest way to use tmux-ultimate is to run the interactive questionnaire:

```bash
python3 tmux_ultimate.py
```

This will guide you through all configuration options and create a `.tmux.conf` file in your home directory.

## Command Line Options

### Output File Location

Use the `-o` flag to specify where to save your configuration:

```bash
# Save to a custom location
python3 tmux_ultimate.py -o /path/to/my-tmux.conf

# Save to /tmp for testing
python3 tmux_ultimate.py -o /tmp/test-tmux.conf
```

### Safety Features

tmux-ultimate will **never overwrite** an existing configuration file. If a file already exists at the target location, the tool will:

1. Display a safety warning
2. Show the existing file location
3. Prompt you to choose a different location

## Interactive Menu

When you run tmux-ultimate, you'll see a main menu with these options:

1. **Generate tmux configuration** - Start the questionnaire
2. **Install TPM and plugins** - Set up plugin management
3. **Exit** - Quit the application

## The Questionnaire Process

### Question Types

You'll encounter several types of questions:

**Yes/No Questions**
```
Enable mouse support? (y/n) [default: y]: 
```

**Multiple Choice**

<div style={{fontFamily: 'monospace', fontSize: '14px', backgroundColor: '#1e1e1e', color: '#ffffff', padding: '16px', borderRadius: '8px', margin: '16px 0'}}>
  <div style={{marginBottom: '8px'}}>Choose your color scheme:</div>
  <div style={{backgroundColor: '#282a36', color: '#f8f8f2', padding: '4px 8px', margin: '2px 0', borderRadius: '4px'}}>
    1. <span style={{backgroundColor: '#bd93f9', color: '#282a36', padding: '2px 6px', borderRadius: '3px', fontWeight: 'bold'}}> Dracula </span> (dark purple theme)
  </div>
  <div style={{backgroundColor: '#2e3440', color: '#d8dee9', padding: '4px 8px', margin: '2px 0', borderRadius: '4px'}}>
    2. <span style={{backgroundColor: '#88c0d0', color: '#2e3440', padding: '2px 6px', borderRadius: '3px', fontWeight: 'bold'}}> Nord </span> (arctic blue theme)
  </div>
  <div style={{backgroundColor: '#282828', color: '#ebdbb2', padding: '4px 8px', margin: '2px 0', borderRadius: '4px'}}>
    3. <span style={{backgroundColor: '#fe8019', color: '#282828', padding: '2px 6px', borderRadius: '3px', fontWeight: 'bold'}}> Gruvbox </span> (retro warm theme)
  </div>
  <div style={{backgroundColor: '#002b36', color: '#839496', padding: '4px 8px', margin: '2px 0', borderRadius: '4px'}}>
    4. <span style={{backgroundColor: '#268bd2', color: '#002b36', padding: '2px 6px', borderRadius: '3px', fontWeight: 'bold'}}> Solarized </span> (balanced contrast theme)
  </div>
  <div style={{backgroundColor: '#1e1e2e', color: '#cdd6f4', padding: '4px 8px', margin: '2px 0', borderRadius: '4px'}}>
    5. <span style={{backgroundColor: '#f5c2e7', color: '#1e1e2e', padding: '2px 6px', borderRadius: '3px', fontWeight: 'bold'}}> Catppuccin </span> (pastel theme)
  </div>
  <div style={{backgroundColor: '#002d72', color: '#ffffff', padding: '4px 8px', margin: '2px 0', borderRadius: '4px'}}>
    6. <span style={{backgroundColor: '#ff671f', color: '#ffffff', padding: '2px 6px', borderRadius: '3px', fontWeight: 'bold'}}> LFGM </span> (New York Mets)
  </div>
  <div style={{marginTop: '8px', color: '#888'}}>Your choice [default: 1]:</div>
</div>

**Text Input**
```
Custom status right format (or press Enter for default): 
```

### Getting Help

For any question, type `?` and press Enter to get detailed help:

```
Choose your prefix key combination:
  1. Ctrl-b (tmux default)
  2. Ctrl-a (screen-like)
Your choice [default: 1]: ?

HELP: The prefix key is the key combination you press before tmux commands.
- Ctrl-b is the tmux default and doesn't conflict with many programs
- Ctrl-a is familiar to GNU Screen users but may conflict with shell shortcuts
Press Enter to continue...
```


## Configuration Categories

The questionnaire covers these areas:

### Basic Settings
- Terminal mode (vi/emacs)
- Prefix key combination
- Mouse support
- History limit

### Visual Appearance
- Color scheme selection
- Status bar configuration
- Window and pane titles
- Border styles

### Key Bindings
- Vim-style copy mode
- Custom pane navigation
- Window management shortcuts

### Plugin Management
- TPM (Tmux Plugin Manager) setup
- Essential plugin selection
- Plugin-specific configuration

### Advanced Features
- Session logging
- System clipboard integration
- Automatic session restoration

## After Generation

Once your configuration is generated:

1. **Review the file** (optional):
   ```bash
   cat ~/.tmux.conf
   ```

2. **Apply the configuration**:
   ```bash
   # If tmux is not running
   tmux new-session

   # If tmux is already running
   tmux source-file ~/.tmux.conf
   ```

3. **Install plugins** (if TPM is enabled):
   - Press `Prefix + I` (capital i) to install plugins
   - Wait for installation to complete

## Tips and Best Practices

### Testing Configurations

Always test new configurations safely:

```bash
# Generate to a test location
python3 tmux_ultimate.py -o /tmp/test.conf

# Test the configuration
tmux -f /tmp/test.conf new-session

# If satisfied, copy to permanent location
cp /tmp/test.conf ~/.tmux.conf
```

### Backup Your Settings

Before making changes:

```bash
# Backup existing configuration
cp ~/.tmux.conf ~/.tmux.conf.backup.$(date +%Y%m%d)
```

### Iterative Improvement

You can run tmux-ultimate multiple times to refine your configuration:

1. Generate initial configuration
2. Use tmux with the new settings
3. Identify areas for improvement
4. Re-run the questionnaire with different choices

### Plugin Management

If you enabled TPM, see the [complete plugin guide](plugins.md) for key bindings and management.

## Common Workflows

### First-Time Setup
```bash
# 1. Run questionnaire
python3 tmux_ultimate.py

# 2. Start tmux
tmux new-session

# 3. Install plugins (if using TPM)
# Press: Prefix + I
```

### Configuration Updates
```bash
# 1. Backup current config
cp ~/.tmux.conf ~/.tmux.conf.backup

# 2. Generate new config to test location
python3 tmux_ultimate.py -o /tmp/new.conf

# 3. Test the new configuration
tmux -f /tmp/new.conf new-session

# 4. If satisfied, replace main config
mv /tmp/new.conf ~/.tmux.conf

# 5. Reload in existing sessions
tmux source-file ~/.tmux.conf
```