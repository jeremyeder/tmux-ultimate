#!/usr/bin/env python3
"""
TMUX Configuration Generator
Generates .tmux.conf file based on questionnaire responses
"""

import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


class TmuxConfigGenerator:
    """Generate tmux configuration file from questionnaire responses"""

    def __init__(self, config_data: Dict):
        # Initialize color schemes first (needed for validation)
        self._initialize_color_schemes()

        # Validate and sanitize input config
        if config_data is None:
            config_data = {}

        if not isinstance(config_data, dict):
            raise TypeError(
                f"Config data must be a dictionary, got {type(config_data)}"
            )

        # Create a sanitized copy to avoid modifying the original
        self.config = self._sanitize_config(config_data)
        self.lines = []

    def _initialize_color_schemes(self):
        """Initialize color schemes definitions"""
        self.color_schemes = {
            "dracula": {
                "bg": "#282a36",
                "fg": "#f8f8f2",
                "current_line": "#44475a",
                "comment": "#6272a4",
                "cyan": "#8be9fd",
                "green": "#50fa7b",
                "orange": "#ffb86c",
                "pink": "#ff79c6",
                "purple": "#bd93f9",
                "red": "#ff5555",
                "yellow": "#f1fa8c",
            },
            "nord": {
                "polar_night_0": "#2e3440",
                "polar_night_1": "#3b4252",
                "polar_night_2": "#434c5e",
                "polar_night_3": "#4c566a",
                "snow_storm_0": "#d8dee9",
                "snow_storm_1": "#e5e9f0",
                "snow_storm_2": "#eceff4",
                "frost_0": "#8fbcbb",
                "frost_1": "#88c0d0",
                "frost_2": "#81a1c1",
                "frost_3": "#5e81ac",
                "aurora_0": "#bf616a",
                "aurora_1": "#d08770",
                "aurora_2": "#ebcb8b",
                "aurora_3": "#a3be8c",
                "aurora_4": "#b48ead",
            },
            "gruvbox": {
                "bg": "#282828",
                "fg": "#ebdbb2",
                "red": "#cc241d",
                "green": "#98971a",
                "yellow": "#d79921",
                "blue": "#458588",
                "purple": "#b16286",
                "aqua": "#689d6a",
                "gray": "#a89984",
                "orange": "#d65d0e",
            },
            "solarized": {
                "base03": "#002b36",
                "base02": "#073642",
                "base01": "#586e75",
                "base00": "#657b83",
                "base0": "#839496",
                "base1": "#93a1a1",
                "base2": "#eee8d5",
                "base3": "#fdf6e3",
                "yellow": "#b58900",
                "orange": "#cb4b16",
                "red": "#dc322f",
                "magenta": "#d33682",
                "violet": "#6c71c4",
                "blue": "#268bd2",
                "cyan": "#2aa198",
                "green": "#859900",
            },
            "catppuccin": {
                "rosewater": "#f5e0dc",
                "flamingo": "#f2cdcd",
                "pink": "#f5c2e7",
                "mauve": "#cba6f7",
                "red": "#f38ba8",
                "maroon": "#eba0ac",
                "peach": "#fab387",
                "yellow": "#f9e2af",
                "green": "#a6e3a1",
                "teal": "#94e2d5",
                "sky": "#89dceb",
                "sapphire": "#74c7ec",
                "blue": "#89b4fa",
                "lavender": "#b4befe",
                "text": "#cdd6f4",
                "subtext1": "#bac2de",
                "subtext0": "#a6adc8",
                "overlay2": "#9399b2",
                "overlay1": "#7f849c",
                "overlay0": "#6c7086",
                "surface2": "#585b70",
                "surface1": "#45475a",
                "surface0": "#313244",
                "base": "#1e1e2e",
                "mantle": "#181825",
                "crust": "#11111b",
            },
            "lfgm": {
                "bg": "#002d72",
                "fg": "#ffffff",
                "primary_blue": "#002d72",
                "primary_orange": "#ff671f",
                "secondary_blue": "#0047ab",
                "secondary_orange": "#ff8c00",
                "light_blue": "#4472c4",
                "light_orange": "#ffa366",
                "dark_blue": "#001a44",
                "white": "#ffffff",
                "black": "#000000",
                "gray": "#cccccc",
            },
        }

    def _sanitize_config(self, config_data: Dict) -> Dict:
        """Sanitize and validate configuration data with safe defaults"""
        # Define safe defaults for all configuration options
        defaults = {
            "prefix_key": "C-b",
            "custom_prefix": "",
            "enable_mouse": True,
            "color_scheme": "default",
            "show_time": True,
            "show_date": True,
            "show_hostname": False,
            "show_session_name": True,
            "status_position": "bottom",
            "history_limit": 5000,
            "automatic_rename": False,
            "renumber_windows": True,
            "base_index": 1,
            "pane_base_index": 1,
            "terminal_mode": "emacs",
            "enable_256_colors": True,
            "enable_true_colors": True,
            "vim_navigation": False,
            "vim_copy_mode": False,
            "use_tpm": False,
            "plugins": [],
            "enable_copy_paste": False,
            "enable_pane_synchronization": False,
            "enable_logging": False,
        }

        # Start with defaults
        sanitized = defaults.copy()

        # Safely overlay user config
        for key, value in config_data.items():
            if key in defaults:
                # Type validation based on defaults
                expected_type = type(defaults[key])
                if isinstance(value, expected_type):
                    sanitized[key] = value
                else:
                    print(
                        f"⚠️  Warning: Invalid type for '{key}' (expected {expected_type.__name__}, got {type(value).__name__}). Using default."
                    )
            else:
                print(f"⚠️  Warning: Unknown configuration key '{key}' ignored.")

        # Additional validation for specific values
        if (
            sanitized["color_scheme"] not in self.color_schemes
            and sanitized["color_scheme"] != "default"
        ):
            print(
                f"⚠️  Warning: Unknown color scheme '{sanitized['color_scheme']}'. Using default."
            )
            sanitized["color_scheme"] = "default"

        if sanitized["history_limit"] < 100 or sanitized["history_limit"] > 1000000:
            print(
                f"⚠️  Warning: History limit {sanitized['history_limit']} out of range (100-1000000). Using 5000."
            )
            sanitized["history_limit"] = 5000

        if sanitized["base_index"] not in [0, 1]:
            print(f"⚠️  Warning: Invalid base_index {sanitized['base_index']}. Using 1.")
            sanitized["base_index"] = 1
            sanitized["pane_base_index"] = 1

        if sanitized["terminal_mode"] not in ["emacs", "vi"]:
            print(
                f"⚠️  Warning: Invalid terminal_mode '{sanitized['terminal_mode']}'. Using 'emacs'."
            )
            sanitized["terminal_mode"] = "emacs"

        if sanitized["status_position"] not in ["top", "bottom"]:
            print(
                f"⚠️  Warning: Invalid status_position '{sanitized['status_position']}'. Using 'bottom'."
            )
            sanitized["status_position"] = "bottom"

        # Ensure plugins is a list
        if not isinstance(sanitized["plugins"], list):
            print(
                f"⚠️  Warning: Plugins must be a list, got {type(sanitized['plugins'])}. Using empty list."
            )
            sanitized["plugins"] = []

        return sanitized

    def generate_config(self) -> str:
        """Generate the complete tmux configuration"""
        self._add_header()
        self._add_core_settings()
        self._add_appearance_settings()
        self._add_behavior_settings()
        self._add_terminal_integration()
        self._add_vim_integration()
        self._add_key_bindings()
        self._add_plugin_configuration()
        self._add_advanced_features()
        self._add_footer()

        return "\n".join(self.lines)

    def _add_header(self):
        """Add configuration file header"""
        self.lines.extend(
            [
                "# ═══════════════════════════════════════════════════════════════════",
                "# Ultimate TMUX Configuration",
                f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "# Generated by: TMUX Ultimate Configuration Generator",
                "# ═══════════════════════════════════════════════════════════════════",
                "",
                "# Reload configuration with Prefix + r",
                'bind r source-file ~/.tmux.conf \\; display-message "Config reloaded!"',
                "",
            ]
        )

    def _add_core_settings(self):
        """Add core tmux settings"""
        self.lines.extend(
            [
                "# ═══════════════════════════════════════════════════════════════════",
                "# CORE SETTINGS",
                "# ═══════════════════════════════════════════════════════════════════",
                "",
            ]
        )

        # Prefix key configuration
        prefix = self.config.get("prefix_key", "C-b")
        if prefix == "custom":
            prefix = self.config.get("custom_prefix", "C-b")

        # Always set the prefix explicitly for clarity
        self.lines.extend(["# Set prefix key", f"set -g prefix {prefix}", ""])

        if prefix != "C-b":
            self.lines.extend(
                [
                    "# Unbind default prefix and set new prefix",
                    "unbind C-b",
                    f"bind {prefix} send-prefix",
                    "",
                ]
            )

        # Mouse support
        if self.config.get("enable_mouse", True):
            self.lines.extend(["# Enable mouse support", "set -g mouse on", ""])

    def _add_appearance_settings(self):
        """Add appearance and status bar settings"""
        self.lines.extend(
            [
                "# ═══════════════════════════════════════════════════════════════════",
                "# APPEARANCE & STATUS BAR",
                "# ═══════════════════════════════════════════════════════════════════",
                "",
            ]
        )

        # Color support
        if self.config.get("enable_256_colors", True):
            self.lines.extend(
                ["# Enable 256 colors", 'set -g default-terminal "screen-256color"', ""]
            )

        if self.config.get("enable_true_colors", True):
            self.lines.extend(
                [
                    "# Enable true color support",
                    'set -ga terminal-overrides ",*256col*:Tc"',
                    "",
                ]
            )

        # Status bar position
        position = self.config.get("status_position", "bottom")
        self.lines.extend(
            [f"# Status bar position", f"set -g status-position {position}", ""]
        )

        # Color scheme
        color_scheme = self.config.get("color_scheme", "default")
        if color_scheme != "default":
            self._add_color_scheme(color_scheme)

        # Status bar content
        self._add_status_bar_config()

    def _add_color_scheme(self, scheme: str):
        """Add color scheme configuration"""
        if scheme not in self.color_schemes:
            return

        colors = self.color_schemes[scheme]

        self.lines.extend([f"# {scheme.title()} Color Scheme", ""])

        if scheme == "dracula":
            self.lines.extend(
                [
                    f"set -g status-bg '{colors['current_line']}'",
                    f"set -g status-fg '{colors['fg']}'",
                    f"set -g window-status-current-style 'bg={colors['purple']},fg={colors['bg']}'",
                    f"set -g pane-border-style 'fg={colors['comment']}'",
                    f"set -g pane-active-border-style 'fg={colors['purple']}'",
                    "",
                ]
            )
        elif scheme == "nord":
            self.lines.extend(
                [
                    f"set -g status-bg '{colors['polar_night_0']}'",
                    f"set -g status-fg '{colors['snow_storm_0']}'",
                    f"set -g window-status-current-style 'bg={colors['frost_3']},fg={colors['snow_storm_2']}'",
                    f"set -g pane-border-style 'fg={colors['polar_night_2']}'",
                    f"set -g pane-active-border-style 'fg={colors['frost_1']}'",
                    "",
                ]
            )
        elif scheme == "gruvbox":
            self.lines.extend(
                [
                    f"set -g status-bg '{colors['bg']}'",
                    f"set -g status-fg '{colors['fg']}'",
                    f"set -g window-status-current-style 'bg={colors['orange']},fg={colors['bg']}'",
                    f"set -g pane-border-style 'fg={colors['gray']}'",
                    f"set -g pane-active-border-style 'fg={colors['orange']}'",
                    "",
                ]
            )
        elif scheme == "solarized":
            self.lines.extend(
                [
                    f"set -g status-bg '{colors['base02']}'",
                    f"set -g status-fg '{colors['base0']}'",
                    f"set -g window-status-current-style 'bg={colors['blue']},fg={colors['base3']}'",
                    f"set -g pane-border-style 'fg={colors['base01']}'",
                    f"set -g pane-active-border-style 'fg={colors['blue']}'",
                    "",
                ]
            )
        elif scheme == "catppuccin":
            self.lines.extend(
                [
                    f"set -g status-bg '{colors['base']}'",
                    f"set -g status-fg '{colors['text']}'",
                    f"set -g window-status-current-style 'bg={colors['mauve']},fg={colors['base']}'",
                    f"set -g pane-border-style 'fg={colors['surface0']}'",
                    f"set -g pane-active-border-style 'fg={colors['mauve']}'",
                    "",
                ]
            )
        elif scheme == "lfgm":
            self.lines.extend(
                [
                    f"set -g status-bg '{colors['primary_blue']}'",
                    f"set -g status-fg '{colors['white']}'",
                    f"set -g window-status-current-style 'bg={colors['primary_orange']},fg={colors['white']}'",
                    f"set -g pane-border-style 'fg={colors['secondary_blue']}'",
                    f"set -g pane-active-border-style 'fg={colors['primary_orange']}'",
                    f"set -g status-left-style 'bg={colors['primary_orange']},fg={colors['white']}'",
                    f"set -g status-right-style 'bg={colors['light_blue']},fg={colors['white']}'",
                    f"set -g window-status-style 'bg={colors['secondary_blue']},fg={colors['white']}'",
                    f"set -g message-style 'bg={colors['primary_orange']},fg={colors['white']}'",
                    f"set -g message-command-style 'bg={colors['light_orange']},fg={colors['dark_blue']}'",
                    "",
                ]
            )

    def _add_status_bar_config(self):
        """Add status bar configuration"""
        status_left = []
        status_right = []

        # Left side - session info
        if self.config.get("show_session_name", True):
            status_left.append("#S")

        # Right side - system info
        if self.config.get("show_hostname", False):
            status_right.append("#H")

        if self.config.get("show_date", True):
            status_right.append("%Y-%m-%d")

        if self.config.get("show_time", True):
            status_right.append("%H:%M")

        if status_left or status_right:
            self.lines.extend(
                [
                    "# Status bar configuration",
                    f"set -g status-left '[{' | '.join(status_left)}] '",
                    f"set -g status-right ' {' | '.join(status_right)}'",
                    "set -g status-left-length 50",
                    "set -g status-right-length 50",
                    "",
                ]
            )

    def _add_behavior_settings(self):
        """Add behavior settings"""
        self.lines.extend(
            [
                "# ═══════════════════════════════════════════════════════════════════",
                "# BEHAVIOR SETTINGS",
                "# ═══════════════════════════════════════════════════════════════════",
                "",
            ]
        )

        # History limit
        history_limit = self.config.get("history_limit", 5000)
        self.lines.extend(
            [f"# History buffer size", f"set -g history-limit {history_limit}", ""]
        )

        # Window indexing
        base_index = self.config.get("base_index", 1)
        if base_index != 0:
            self.lines.extend(
                [
                    "# Start windows and panes at 1, not 0",
                    f"set -g base-index {base_index}",
                    f"setw -g pane-base-index {base_index}",
                    "",
                ]
            )

        # Automatic rename
        if not self.config.get("automatic_rename", False):
            self.lines.extend(
                [
                    "# Disable automatic window renaming",
                    "set-option -g allow-rename off",
                    "",
                ]
            )

        # Renumber windows
        if self.config.get("renumber_windows", True):
            self.lines.extend(
                [
                    "# Renumber windows when a window is closed",
                    "set -g renumber-windows on",
                    "",
                ]
            )

    def _add_terminal_integration(self):
        """Add terminal integration settings"""
        self.lines.extend(
            [
                "# ═══════════════════════════════════════════════════════════════════",
                "# TERMINAL INTEGRATION",
                "# ═══════════════════════════════════════════════════════════════════",
                "",
            ]
        )

        # Terminal mode
        terminal_mode = self.config.get("terminal_mode", "emacs")
        if terminal_mode == "vi":
            self.lines.extend(
                ["# Use Vi mode", "setw -g mode-keys vi", "set -g status-keys vi", ""]
            )

    def _add_vim_integration(self):
        """Add Vim integration settings"""
        if not (
            self.config.get("vim_navigation", False)
            or self.config.get("vim_copy_mode", False)
        ):
            return

        self.lines.extend(
            [
                "# ═══════════════════════════════════════════════════════════════════",
                "# VIM INTEGRATION",
                "# ═══════════════════════════════════════════════════════════════════",
                "",
            ]
        )

        # Vim navigation
        if self.config.get("vim_navigation", False):
            prefix = self.config.get("prefix_key", "C-b")
            if prefix == "custom":
                prefix = self.config.get("custom_prefix", "C-b")

            self.lines.extend(
                [
                    "# Vim-style pane navigation",
                    f"bind h select-pane -L",
                    f"bind j select-pane -D",
                    f"bind k select-pane -U",
                    f"bind l select-pane -R",
                    "",
                    "# Vim-style pane resizing",
                    f"bind -r H resize-pane -L 5",
                    f"bind -r J resize-pane -D 5",
                    f"bind -r K resize-pane -U 5",
                    f"bind -r L resize-pane -R 5",
                    "",
                ]
            )

        # Vim copy mode
        if self.config.get("vim_copy_mode", False):
            self.lines.extend(
                [
                    "# Vim-style copy mode",
                    "bind P paste-buffer",
                    "bind-key -T copy-mode-vi v send-keys -X begin-selection",
                    "bind-key -T copy-mode-vi y send-keys -X copy-selection",
                    "bind-key -T copy-mode-vi r send-keys -X rectangle-toggle",
                    "",
                ]
            )

    def _add_key_bindings(self):
        """Add custom key bindings"""
        self.lines.extend(
            [
                "# ═══════════════════════════════════════════════════════════════════",
                "# KEY BINDINGS",
                "# ═══════════════════════════════════════════════════════════════════",
                "",
            ]
        )

        # Common useful bindings
        self.lines.extend(
            [
                "# Split panes using | and -",
                "bind | split-window -h",
                "bind - split-window -v",
                "unbind '\"'",
                "unbind %",
                "",
                "# Switch panes using Alt+arrow without prefix",
                "bind -n M-Left select-pane -L",
                "bind -n M-Right select-pane -R",
                "bind -n M-Up select-pane -U",
                "bind -n M-Down select-pane -D",
                "",
            ]
        )

        # Pane synchronization
        if self.config.get("enable_pane_synchronization", False):
            self.lines.extend(
                [
                    "# Toggle pane synchronization",
                    "bind S set-window-option synchronize-panes",
                    "",
                ]
            )

    def _add_plugin_configuration(self):
        """Add plugin configuration"""
        if not self.config.get("use_tpm", False):
            return

        plugins = self.config.get("plugins", [])
        if not plugins:
            return

        self.lines.extend(
            [
                "# ═══════════════════════════════════════════════════════════════════",
                "# PLUGIN CONFIGURATION",
                "# ═══════════════════════════════════════════════════════════════════",
                "",
                "# List of plugins",
                "set -g @plugin 'tmux-plugins/tpm'",
                "",
            ]
        )

        # Plugin mappings
        plugin_map = {
            "tmux-sensible": "tmux-plugins/tmux-sensible",
            "tmux-resurrect": "tmux-plugins/tmux-resurrect",
            "tmux-continuum": "tmux-plugins/tmux-continuum",
            "tmux-copycat": "tmux-plugins/tmux-copycat",
            "tmux-yank": "tmux-plugins/tmux-yank",
            "tmux-sidebar": "tmux-plugins/tmux-sidebar",
            "tmux-battery": "tmux-plugins/tmux-battery",
            "tmux-cpu": "tmux-plugins/tmux-cpu",
            "tmux-net-speed": "tmux-plugins/tmux-net-speed",
        }

        for plugin in plugins:
            if plugin in plugin_map:
                self.lines.append(f"set -g @plugin '{plugin_map[plugin]}'")

        self.lines.extend(["", "# Plugin configurations", ""])

        # Plugin-specific configurations
        if "tmux-continuum" in plugins and "tmux-resurrect" in plugins:
            self.lines.extend(
                [
                    "# tmux-continuum configuration",
                    "set -g @continuum-restore 'on'",
                    "set -g @continuum-save-interval '15'",
                    "",
                ]
            )

        if "tmux-yank" in plugins:
            self.lines.extend(
                [
                    "# tmux-yank configuration",
                    "set -g @yank_selection_mouse 'clipboard'",
                    "",
                ]
            )

        # TPM initialization
        self.lines.extend(
            [
                "# Initialize TMUX plugin manager (keep this line at the very bottom of tmux.conf)",
                "run '~/.tmux/plugins/tpm/tpm'",
                "",
            ]
        )

    def _add_advanced_features(self):
        """Add advanced features"""
        advanced_features = [
            self.config.get("enable_copy_paste", False),
            self.config.get("enable_logging", False),
        ]

        if not any(advanced_features):
            return

        self.lines.extend(
            [
                "# ═══════════════════════════════════════════════════════════════════",
                "# ADVANCED FEATURES",
                "# ═══════════════════════════════════════════════════════════════════",
                "",
            ]
        )

        # System clipboard integration
        if self.config.get("enable_copy_paste", False):
            self.lines.extend(
                [
                    "# System clipboard integration",
                    'bind C-c run "tmux save-buffer - | xclip -i -sel clipboard"',
                    'bind C-v run "tmux set-buffer \\"$(xclip -o -sel clipboard)\\"; tmux paste-buffer"',
                    "",
                ]
            )

        # Session logging
        if self.config.get("enable_logging", False):
            self.lines.extend(
                [
                    "# Session logging",
                    "bind-key H pipe-pane -o 'cat >>~/tmux-#W.log' \\; display-message 'Started logging to ~/tmux-#W.log'",
                    "bind-key h pipe-pane \\; display-message 'Ended logging to ~/tmux-#W.log'",
                    "",
                ]
            )

    def _add_footer(self):
        """Add configuration file footer"""
        self.lines.extend(
            [
                "# ═══════════════════════════════════════════════════════════════════",
                "# END OF CONFIGURATION",
                "# ═══════════════════════════════════════════════════════════════════",
                "",
                "# To apply changes:",
                "# 1. Save this file as ~/.tmux.conf",
                "# 2. Reload with: tmux source-file ~/.tmux.conf",
                "# 3. Or use the reload binding: Prefix + r",
                "",
            ]
        )


def main():
    """Main function to generate tmux configuration"""
    config_path = os.path.join(os.path.dirname(__file__), "tmux_config.json")

    if not os.path.exists(config_path):
        print("❌ Configuration file not found!")
        print("Please run the questionnaire first: python tmux_questionnaire.py")
        return

    # Load configuration
    with open(config_path, "r") as f:
        config_data = json.load(f)

    # Generate configuration
    generator = TmuxConfigGenerator(config_data)
    tmux_config = generator.generate_config()

    # Save configuration
    output_path = os.path.join(os.path.dirname(__file__), "tmux.conf")
    with open(output_path, "w") as f:
        f.write(tmux_config)

    print("🎉 TMUX configuration generated successfully!")
    print(f"📄 Configuration saved to: {output_path}")
    print("\n📋 Next steps:")
    print("1. Review the generated configuration")
    print("2. Copy to your home directory: cp tmux.conf ~/.tmux.conf")
    print("3. If using TPM plugins, install them first:")
    print("   git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm")
    print("4. Reload tmux: tmux source-file ~/.tmux.conf")
    print("5. If using plugins, install them with: Prefix + I")

    print("\n🚀 Your ultimate tmux configuration is ready!")


if __name__ == "__main__":
    main()
