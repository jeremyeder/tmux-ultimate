---
sidebar_position: 5
---

# Plugin Management

tmux-ultimate includes comprehensive plugin management through TPM (Tmux Plugin Manager), making it easy to extend tmux functionality.

## TPM (Tmux Plugin Manager)

TPM is the standard plugin manager for tmux, allowing you to easily install, update, and remove plugins.

### Installation

tmux-ultimate can automatically install TPM for you through the main menu. See the [Installation Guide](installation.md#tpm-installation) for manual setup instructions.

### Key Bindings

Once TPM is installed and configured:

- **`Prefix + I`** - Install new plugins
- **`Prefix + U`** - Update plugins
- **`Prefix + alt + u`** - Remove/uninstall plugins not in config

## Default Plugin Set

tmux-ultimate includes these essential plugins by default:

### tmux-sensible
**Repository**: `tmux-plugins/tmux-sensible`  
**Purpose**: Provides sensible default settings

**Features**:
- Better default key bindings
- Improved mouse support
- UTF-8 support
- Enhanced scrolling behavior
- Sane defaults for status keys

**Configuration**: None required - works automatically

---

### tmux-resurrect
**Repository**: `tmux-plugins/tmux-resurrect`  
**Purpose**: Save and restore tmux sessions

**Key Bindings**:
- `Prefix + Ctrl-s` - Save current session
- `Prefix + Ctrl-r` - Restore saved session

**What gets saved**:
- All sessions, windows, and panes
- Window and pane layout
- Active and alternative session
- Active and alternative window for each session
- Windows with focus
- Active pane for each window
- "Grouped sessions" (useful for multi-monitor setup)

**Advanced Features**:
- Save and restore vim/neovim sessions
- Save and restore shell history
- Custom save/restore hooks

---

### tmux-continuum
**Repository**: `tmux-plugins/tmux-continuum`  
**Purpose**: Automatic session saving and restoration

**Features**:
- Automatic session saves every 15 minutes
- Automatic session restore when tmux starts
- Works seamlessly with tmux-resurrect
- Configurable save interval

**Status Bar Integration**:
Shows last save time in status bar (optional)

---

### tmux-copycat
**Repository**: `tmux-plugins/tmux-copycat`  
**Purpose**: Enhanced search in copy mode

**Key Bindings**:
- `Prefix + /` - Regex search
- `Prefix + Ctrl-f` - Simple file search
- `Prefix + Ctrl-g` - Jumping over git status files
- `Prefix + Alt-h` - Jumping over SHA-1/SHA-256 hashes
- `Prefix + Ctrl-u` - URL search
- `Prefix + Ctrl-d` - Number search

**Search Navigation**:
- `n` - Jump to next match
- `N` - Jump to previous match

---

### tmux-yank
**Repository**: `tmux-plugins/tmux-yank`  
**Purpose**: Copy to system clipboard

**Copy Mode Key Bindings**:
- `y` - Copy selection to system clipboard
- `Y` - Copy whole line to system clipboard (without newline)

**Normal Mode Key Bindings**:
- `Prefix + y` - Copy current command line to clipboard
- `Prefix + Y` - Copy current pane's current path to clipboard

**System Compatibility**:
- **Linux**: Uses `xclip` or `xsel`
- **macOS**: Uses `pbcopy`
- **Windows**: Uses `clip.exe`
- **Termux (Android)**: Uses `termux-clipboard-set`

## Additional Available Plugins

### tmux-open
**Repository**: `tmux-plugins/tmux-open`  
**Purpose**: Open files and URLs from tmux

**Key Bindings** (in copy mode):
- `o` - Open highlighted file/URL
- `Ctrl-o` - Open highlighted file/URL in `$EDITOR`
- `Shift-s` - Search highlighted text (Google)

**Supported File Types**:
- URLs (http/https/ftp)
- Local files
- Email addresses

---

### tmux-fzf
**Repository**: `sainnhe/tmux-fzf`  
**Purpose**: Fuzzy finder integration

**Key Binding**: `Prefix + F`

**Features**:
- Session management
- Window management  
- Pane management
- Key binding help
- Command history

**Requirements**: `fzf` must be installed

---

### tmux-prefix-highlight
**Repository**: `tmux-plugins/tmux-prefix-highlight`  
**Purpose**: Visual prefix key indicator

**Features**:
- Shows when prefix key is pressed
- Customizable colors and position
- Copy mode indicator
- Synchronize panes indicator

**Status Bar Integration**:
```bash
set -g status-right '#{prefix_highlight} | %a %Y-%m-%d %H:%M'
```

---

### tmux-cpu
**Repository**: `tmux-plugins/tmux-cpu`  
**Purpose**: System resource monitoring

**Status Bar Variables**:
- `#{cpu_percentage}` - CPU usage percentage
- `#{cpu_bg_color}` - Background color based on CPU usage
- `#{cpu_fg_color}` - Foreground color based on CPU usage
- `#{ram_percentage}` - RAM usage percentage
- `#{gram_percentage}` - GPU RAM usage (if available)

---

### tmux-battery
**Repository**: `tmux-plugins/tmux-battery`  
**Purpose**: Battery status display

**Status Bar Variables**:
- `#{battery_percentage}` - Battery percentage
- `#{battery_status_bg}` - Background color based on battery status
- `#{battery_status_fg}` - Foreground color based on battery status
- `#{battery_remain}` - Remaining battery time

## Custom Plugin Configuration

### Adding New Plugins

1. **Edit your tmux configuration**:
   ```bash
   # Add to ~/.tmux.conf
   set -g @plugin 'author/plugin-name'
   ```

2. **Reload tmux configuration**:
   ```bash
   tmux source-file ~/.tmux.conf
   ```

3. **Install the plugin**:
   Press `Prefix + I`

### Plugin-Specific Configuration

Most plugins support configuration variables:

```bash
# tmux-resurrect example
set -g @resurrect-capture-pane-contents 'on'
set -g @resurrect-strategy-vim 'session'
set -g @resurrect-save-shell-history 'on'

# tmux-continuum example  
set -g @continuum-restore 'on'
set -g @continuum-save-interval '10'

# tmux-prefix-highlight example
set -g @prefix_highlight_fg 'white'
set -g @prefix_highlight_bg 'blue'
```

## Plugin Troubleshooting

### Common Issues

**Plugins not loading**
1. Check TPM installation: `ls ~/.tmux/plugins/tpm`
2. Verify plugin list in config
3. Try manual installation: `Prefix + I`

**Key bindings conflict**
1. List current bindings: `tmux list-keys`
2. Check plugin documentation for conflicts
3. Use custom key bindings if needed

**Plugin not found**
1. Verify repository name and author
2. Check internet connection
3. Try cloning manually to `~/.tmux/plugins/`

### Debugging Commands

```bash
# Show plugin environment
tmux show-environment -g TMUX_PLUGIN_MANAGER_PATH

# List installed plugins
ls ~/.tmux/plugins/

# Check plugin loading
tmux source-file ~/.tmux.conf && echo "Config loaded successfully"
```

## Creating Custom Plugins

Basic plugin structure:
```
~/.tmux/plugins/my-plugin/
├── plugin.tmux          # Main plugin script
├── scripts/
│   └── helper.sh       # Helper scripts
└── README.md           # Documentation
```

Example `plugin.tmux`:
```bash
#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Plugin functionality here
tmux bind-key F5 run-shell "$CURRENT_DIR/scripts/helper.sh"
```

### Best Practices

1. **Use the `@plugin` syntax** for easy management
2. **Follow TPM conventions** for compatibility
3. **Document key bindings** and configuration options
4. **Test with minimal configurations** to avoid conflicts
5. **Use unique prefixes** for custom key bindings