#!/usr/bin/env python3
"""
Tests for tmux_generator.py
"""

import pytest
from tmux_generator import TmuxConfigGenerator


class TestTmuxConfigGenerator:
    """Test the TmuxConfigGenerator class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.sample_config = {
            "prefix_key": "C-b",
            "enable_mouse": True,
            "color_scheme": "dracula",
            "show_time": True,
            "show_date": True,
            "show_hostname": False,
            "status_position": "bottom",
            "history_limit": 5000,
            "automatic_rename": False,
            "renumber_windows": True,
            "base_index": 1,
            "pane_base_index": 1,
            "terminal_mode": "vi",
            "enable_256_colors": True,
            "enable_true_colors": True,
            "vim_navigation": True,
            "vim_copy_mode": True,
            "use_tpm": True,
            "plugins": ["tmux-sensible", "tmux-resurrect"],
            "enable_logging": False,
        }
        self.generator = TmuxConfigGenerator(self.sample_config)

    def test_initialization(self):
        """Test generator initializes correctly"""
        # Generator adds default values, so check key values are preserved
        assert self.generator.config["prefix_key"] == self.sample_config["prefix_key"]
        assert (
            self.generator.config["enable_mouse"] == self.sample_config["enable_mouse"]
        )
        assert (
            self.generator.config["color_scheme"] == self.sample_config["color_scheme"]
        )
        assert self.generator.config["use_tpm"] == self.sample_config["use_tpm"]
        assert hasattr(self.generator, "lines")
        assert hasattr(self.generator, "color_schemes")
        assert "lfgm" in self.generator.color_schemes

    def test_color_schemes_contain_lfgm(self):
        """Test LFGM color scheme is properly defined"""
        lfgm = self.generator.color_schemes["lfgm"]
        assert "primary_blue" in lfgm
        assert "primary_orange" in lfgm
        assert lfgm["primary_blue"] == "#002d72"  # Mets blue
        assert lfgm["primary_orange"] == "#ff671f"  # Mets orange

    def test_generate_config_basic(self):
        """Test basic config generation"""
        config_output = self.generator.generate_config()
        assert isinstance(config_output, str)
        assert "# Ultimate TMUX Configuration" in config_output
        assert "set -g prefix C-b" in config_output
        assert "set -g mouse on" in config_output

    def test_generate_config_lfgm_theme(self):
        """Test LFGM theme configuration"""
        self.generator.config["color_scheme"] = "lfgm"
        config_output = self.generator.generate_config()

        assert "# Lfgm Color Scheme" in config_output
        assert "#002d72" in config_output  # Mets blue
        assert "#ff671f" in config_output  # Mets orange

    def test_core_settings(self):
        """Test core settings generation"""
        self.generator._add_core_settings()
        config_lines = "\n".join(self.generator.lines)

        assert "set -g prefix C-b" in config_lines
        assert "set -g mouse on" in config_lines
        # base-index is in behavior settings, not core settings

    def test_appearance_settings(self):
        """Test appearance settings generation"""
        self.generator._add_appearance_settings()
        config_lines = "\n".join(self.generator.lines)

        assert "# Dracula Color Scheme" in config_lines
        assert "set -g status-position bottom" in config_lines

    def test_behavior_settings(self):
        """Test behavior settings generation"""
        self.generator._add_behavior_settings()
        config_lines = "\n".join(self.generator.lines)

        assert "set -g history-limit 5000" in config_lines
        assert "set -g renumber-windows on" in config_lines
        assert "set-option -g allow-rename off" in config_lines

    def test_terminal_integration(self):
        """Test terminal integration settings"""
        self.generator._add_terminal_integration()
        config_lines = "\n".join(self.generator.lines)

        assert "setw -g mode-keys vi" in config_lines
        # Note: screen-256color is in appearance settings, not terminal integration

    def test_vim_integration(self):
        """Test vim integration settings"""
        self.generator._add_vim_integration()
        config_lines = "\n".join(self.generator.lines)

        assert "bind h select-pane -L" in config_lines
        assert "bind j select-pane -D" in config_lines
        assert "bind k select-pane -U" in config_lines
        assert "bind l select-pane -R" in config_lines

    def test_plugin_configuration(self):
        """Test plugin configuration generation"""
        self.generator._add_plugin_configuration()
        config_lines = "\n".join(self.generator.lines)

        assert "set -g @plugin 'tmux-plugins/tpm'" in config_lines
        assert "set -g @plugin 'tmux-plugins/tmux-sensible'" in config_lines
        assert "set -g @plugin 'tmux-plugins/tmux-resurrect'" in config_lines
        assert "run '~/.tmux/plugins/tpm/tpm'" in config_lines

    def test_custom_prefix_key(self):
        """Test custom prefix key configuration"""
        self.generator.config["prefix_key"] = "C-a"
        self.generator._add_core_settings()
        config_lines = "\n".join(self.generator.lines)

        assert "set -g prefix C-a" in config_lines
        assert "unbind C-b" in config_lines
        assert "bind C-a send-prefix" in config_lines

    def test_status_bar_configuration(self):
        """Test status bar configuration"""
        self.generator._add_status_bar_config()
        config_lines = "\n".join(self.generator.lines)

        assert "set -g status-left" in config_lines
        assert "set -g status-right" in config_lines
        assert "%Y-%m-%d" in config_lines  # Date format
        assert "%H:%M" in config_lines  # Time format

    def test_all_color_schemes_generate(self):
        """Test all color schemes generate valid configs"""
        schemes = ["dracula", "nord", "gruvbox", "solarized", "catppuccin", "lfgm"]

        for scheme in schemes:
            self.generator.config["color_scheme"] = scheme
            self.generator.lines = []  # Reset lines
            self.generator._add_color_scheme(scheme)
            config_lines = "\n".join(self.generator.lines)

            assert f"# {scheme.title()} Color Scheme" in config_lines
            assert "set -g status-bg" in config_lines
            assert "set -g status-fg" in config_lines

    def test_plugins_list_handling(self):
        """Test various plugin list configurations"""
        # Test empty plugins (TPM should still be configured)
        self.generator.config["use_tpm"] = True
        self.generator.config["plugins"] = []
        self.generator._add_plugin_configuration()
        config_lines = "\n".join(self.generator.lines)
        # Even with empty plugins, TPM base should be configured
        assert "set -g @plugin 'tmux-plugins/tpm'" in config_lines

        # Test with plugins
        self.generator.lines = []
        self.generator.config["plugins"] = ["tmux-sensible", "tmux-yank"]
        self.generator._add_plugin_configuration()
        config_lines = "\n".join(self.generator.lines)
        assert "tmux-sensible" in config_lines
        assert "tmux-yank" in config_lines

    def test_no_tpm_configuration(self):
        """Test configuration without TPM"""
        self.generator.config["use_tpm"] = False
        self.generator._add_plugin_configuration()
        config_lines = "\n".join(self.generator.lines)

        # Should not contain TPM-related config
        assert "tpm" not in config_lines.lower()

    def test_logging_configuration(self):
        """Test logging feature configuration"""
        self.generator.config["enable_logging"] = True
        self.generator._add_advanced_features()
        config_lines = "\n".join(self.generator.lines)

        assert "bind-key H pipe-pane" in config_lines
        assert "cat >>~/tmux" in config_lines


class TestConfigOutput:
    """Test complete configuration output"""

    def test_valid_tmux_syntax(self):
        """Test generated config has valid tmux syntax"""
        config = {
            "prefix_key": "C-b",
            "enable_mouse": True,
            "color_scheme": "lfgm",
            "show_time": True,
            "show_date": True,
            "terminal_mode": "vi",
            "use_tpm": True,
            "plugins": ["tmux-sensible"],
        }

        generator = TmuxConfigGenerator(config)
        output = generator.generate_config()

        # Basic syntax checks
        lines = output.split("\n")
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                # Should be valid tmux command
                assert any(
                    line.startswith(cmd)
                    for cmd in ["set", "bind", "unbind", "run", "if"]
                ), f"Invalid tmux command: {line}"

    def test_lfgm_theme_complete(self):
        """Test complete LFGM theme implementation"""
        config = {"color_scheme": "lfgm"}
        generator = TmuxConfigGenerator(config)
        output = generator.generate_config()

        # Check for Mets colors
        assert "#002d72" in output  # Primary blue
        assert "#ff671f" in output  # Primary orange
        assert "status-bg" in output
        assert "status-fg" in output
        assert "pane-border" in output


@pytest.mark.integration
class TestGeneratorIntegration:
    """Integration tests for generator"""

    def test_questionnaire_to_generator_integration(self):
        """Test data flows correctly from questionnaire to generator"""
        # Simulate questionnaire output
        config_data = {
            "prefix_key": "C-a",
            "enable_mouse": True,
            "color_scheme": "lfgm",
            "show_time": True,
            "use_tpm": True,
            "plugins": ["tmux-sensible", "tmux-resurrect"],
        }

        generator = TmuxConfigGenerator(config_data)
        output = generator.generate_config()

        # Verify key settings made it through
        assert "set -g prefix C-a" in output
        assert "set -g mouse on" in output
        assert "#002d72" in output  # LFGM blue
        assert "tmux-sensible" in output
        assert "tmux-resurrect" in output

    def test_all_features_integration(self):
        """Test all features work together"""
        config_data = {
            "prefix_key": "C-Space",
            "enable_mouse": True,
            "color_scheme": "lfgm",
            "show_time": True,
            "show_date": True,
            "show_hostname": True,
            "terminal_mode": "vi",
            "vim_navigation": True,
            "vim_copy_mode": True,
            "use_tpm": True,
            "plugins": ["tmux-sensible", "tmux-resurrect", "tmux-yank"],
            "enable_logging": True,
        }

        generator = TmuxConfigGenerator(config_data)
        output = generator.generate_config()

        # Should be substantial config
        assert len(output) > 1000  # Reasonable size check
        assert output.count("\n") > 20  # Multiple sections

        # Key features present
        assert "C-Space" in output
        assert "LFGM" in output or "lfgm" in output or "Lfgm" in output
        assert "vi" in output
        assert "tpm" in output
        assert "logging" in output.lower() or "pipe-pane" in output
