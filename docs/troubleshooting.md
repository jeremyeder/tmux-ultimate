---
sidebar_position: 6
---

# Troubleshooting & FAQ

## Common Issues

### Configuration Generation

#### "Command not found: python3"
**Problem**: Python 3 is not installed or not in PATH.

**Solutions**:
- **Ubuntu/Debian**: `sudo apt install python3`
- **CentOS/RHEL**: `sudo yum install python3` or `sudo dnf install python3`
- **macOS**: `brew install python` or use system Python
- **Try alternative**: Use `python` instead of `python3`

#### "Permission denied when writing config"
**Problem**: No write permissions to target directory.

**Solutions**:
```bash
# Check permissions
ls -la ~/.tmux.conf

# Use alternative location
python3 tmux_ultimate.py -o /tmp/tmux.conf

# Fix permissions (if needed)
chmod 644 ~/.tmux.conf
```

#### "File already exists" safety warning
**Problem**: tmux-ultimate won't overwrite existing configurations.

**Solutions**:
```bash
# Backup existing config
mv ~/.tmux.conf ~/.tmux.conf.backup

# Or use different output location
python3 tmux_ultimate.py -o ~/new-tmux.conf
```

### tmux Configuration

#### Colors not displaying correctly
**Problem**: Terminal doesn't support true color or wrong TERM setting.

**Solutions**:
```bash
# Check current TERM
echo $TERM

# Set proper TERM for tmux
export TERM=screen-256color
# or
export TERM=tmux-256color

# Enable true color in tmux config
set-option -sa terminal-overrides ",xterm*:Tc"

# Test color support
curl -s https://gist.githubusercontent.com/lifepillar/09a44b8cf0f9397465614e622979107f/raw/24-bit-color.sh | bash
```

#### Status bar not updating
**Problem**: Status bar shows static content or doesn't refresh.

**Solutions**:
```bash
# Check status settings
tmux show-options -g status
tmux show-options -g status-interval

# Reload configuration
tmux source-file ~/.tmux.conf

# Manual refresh
tmux refresh-client
```

#### Key bindings not working
**Problem**: Custom key bindings don't respond.

**Solutions**:
```bash
# Check prefix key
tmux show-options -g prefix

# List all key bindings
tmux list-keys

# Check for conflicts
tmux list-keys | grep "your-key"

# Test prefix key
# Press prefix, then : and type: display-message "Prefix works!"
```

### Plugin Issues

#### TPM not installing plugins
**Problem**: `Prefix + I` doesn't install plugins.

**Solutions**:
```bash
# Check TPM installation
ls ~/.tmux/plugins/tpm

# Install TPM manually
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

# Verify plugin list in config
grep "@plugin" ~/.tmux.conf

# Reload config and try again
tmux source-file ~/.tmux.conf
```

#### Plugins installed but not working
**Problem**: Plugins appear in directory but functionality missing.

**Solutions**:
```bash
# Check plugin directory
ls ~/.tmux/plugins/

# Verify plugin loading
tmux show-environment -g TMUX_PLUGIN_MANAGER_PATH

# Check for errors
tmux source-file ~/.tmux.conf 2>&1 | grep -i error

# Try manual plugin loading
~/.tmux/plugins/tpm/bin/install_plugins
```

#### Plugin key bindings conflict
**Problem**: Plugin key bindings override custom bindings.

**Solutions**:
```bash
# Check binding conflicts
tmux list-keys | sort

# Unbind conflicting keys
tmux unbind-key <key>

# Use custom prefix for plugin bindings
set -g @plugin_prefix 'M-' # Alt key prefix
```

### System Integration

#### Clipboard not working
**Problem**: Copy/paste between tmux and system clipboard fails.

**Solutions**:
```bash
# Install clipboard tools
# Linux:
sudo apt install xclip  # or xsel
# macOS: (built-in with pbcopy/pbpaste)

# Check tmux-yank plugin
grep "tmux-yank" ~/.tmux.conf

# Test clipboard manually
echo "test" | xclip -selection clipboard  # Linux
echo "test" | pbcopy                      # macOS
```

#### SSH session issues
**Problem**: tmux behaves differently over SSH.

**Solutions**:
```bash
# Forward X11 for clipboard (Linux)
ssh -X user@host

# Set proper TERM in SSH
echo 'export TERM=screen-256color' >> ~/.bashrc

# Check SSH_AUTH_SOCK forwarding
echo $SSH_AUTH_SOCK

# Update tmux environment
tmux set-environment SSH_AUTH_SOCK $SSH_AUTH_SOCK
```

### Performance Issues

#### Slow startup or response
**Problem**: tmux starts slowly or responds sluggishly.

**Solutions**:
```bash
# Check status interval
tmux show-options -g status-interval

# Reduce update frequency
set -g status-interval 60

# Disable problematic plugins temporarily
# Comment out plugins in ~/.tmux.conf

# Check system load
htop  # or top
```

#### High CPU usage
**Problem**: tmux process consuming excessive CPU.

**Solutions**:
```bash
# Check running processes
ps aux | grep tmux

# Monitor tmux activity
tmux list-sessions -F "#{session_name}: #{session_windows} windows"

# Disable activity monitoring if not needed
set -g monitor-activity off
set -g visual-activity off
```

## Frequently Asked Questions

### General Questions

**Q: Can I use tmux-ultimate with my existing configuration?**
A: tmux-ultimate creates a complete new configuration. Back up your existing config first, then either:
- Use tmux-ultimate's output as a base and add your customizations
- Generate to a test location and merge manually

**Q: How do I update my configuration later?**
A: Re-run the questionnaire. tmux-ultimate will create a new configuration file. Always backup your current config first.

**Q: Can I use tmux-ultimate on servers without internet?**
A: Yes, tmux-ultimate works offline. However, plugin installation requires internet connectivity. You can:
- Generate configs on a connected machine and transfer them
- Install plugins manually by copying plugin directories

### Configuration Questions

**Q: How do I change the prefix key after generation?**
A: Edit your `~/.tmux.conf` file:
```bash
# Change from Ctrl-b to Ctrl-a
set -g prefix C-a
unbind C-b
bind C-a send-prefix
```

**Q: Can I use multiple color schemes?**
A: No, tmux uses one color scheme at a time. However, you can:
- Generate multiple configs with different themes
- Manually customize colors in your config
- Use plugins that provide theme switching

**Q: How do I add custom key bindings?**
A: Add them to your `~/.tmux.conf` file:
```bash
# Example: Alt+h/j/k/l for pane navigation
bind -n M-h select-pane -L
bind -n M-j select-pane -D
bind -n M-k select-pane -U
bind -n M-l select-pane -R
```

### Plugin Questions

**Q: How do I remove a plugin?**
A: 
1. Remove the plugin line from `~/.tmux.conf`
2. Reload config: `tmux source-file ~/.tmux.conf`
3. Clean up: `Prefix + alt + u`

**Q: Can I install plugins not included in tmux-ultimate?**
A: Yes! Add any TPM-compatible plugin:
```bash
set -g @plugin 'author/plugin-name'
```
Then press `Prefix + I` to install.

**Q: Why aren't my plugin key bindings working?**
A: Check for conflicts:
```bash
tmux list-keys | grep <your-key>
```
Plugin bindings may be overridden by later configurations.

### Advanced Questions

**Q: How do I set up tmux for pair programming?**
A: Use socket sharing:
```bash
# Create shared socket
tmux -S /tmp/shared new-session -d -s shared

# Make it accessible
chmod 777 /tmp/shared

# Others can connect with
tmux -S /tmp/shared attach -t shared
```

**Q: Can I run tmux inside tmux?**
A: Yes, but you'll need different prefix keys:
```bash
# Outer tmux: Ctrl-b
# Inner tmux: Ctrl-a
set -g prefix C-a
```

**Q: How do I debug tmux configuration issues?**
A: Use these debugging techniques:
```bash
# Check configuration syntax
tmux source-file ~/.tmux.conf 2>&1

# Show all options
tmux show-options -g

# Show all key bindings
tmux list-keys

# Check plugin loading
ls ~/.tmux/plugins/
```

## Getting Help

### Documentation Resources
- [tmux manual](https://man.openbsd.org/tmux)
- [tmux wiki](https://github.com/tmux/tmux/wiki)
- [TPM documentation](https://github.com/tmux-plugins/tpm)

### Community Support
- [tmux-ultimate GitHub Issues](https://github.com/jeremyeder/tmux-ultimate/issues)
- [Stack Overflow - tmux](https://stackoverflow.com/questions/tagged/tmux)
- [r/tmux on Reddit](https://reddit.com/r/tmux)

### Reporting Bugs
When reporting issues with tmux-ultimate:

1. **Include your environment**:
   ```bash
   python3 --version
   tmux -V
   echo $TERM
   uname -a
   ```

2. **Describe the problem**: What you expected vs. what happened

3. **Include steps to reproduce**: Exact commands and inputs

4. **Attach relevant files**: Configuration files, error messages

5. **Mention workarounds**: If you found any temporary solutions