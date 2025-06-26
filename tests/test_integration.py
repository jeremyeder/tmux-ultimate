#!/usr/bin/env python3
"""
Integration tests for the complete tmux-ultimate workflow
"""

import pytest
import os
import tempfile
import json
from unittest.mock import patch, mock_open, MagicMock

# Import the modules we're testing
from tmux_questionnaire import TmuxQuestionnaire, TmuxConfig
from tmux_generator import TmuxConfigGenerator


@pytest.mark.integration
class TestCompleteWorkflow:
    """Test the complete workflow from questionnaire to config generation"""
    
    def test_questionnaire_to_config_generation(self):
        """Test complete workflow: questionnaire → config data → tmux.conf"""
        # Step 1: Simulate questionnaire responses
        mock_responses = [
            '2',    # prefix: C-a
            'y',    # mouse support
            '6',    # color scheme: LFGM
            'y',    # show time
            'y',    # show date
            'n',    # show hostname
            '1',    # status position: bottom
            '5000', # history limit
            'n',    # automatic rename
            'y',    # renumber windows
            '1',    # base index
            '1',    # pane base index
            '1',    # terminal mode: vi
            'y',    # 256 colors
            'y',    # true colors
            'y',    # vim navigation
            'y',    # vim copy mode
            'y',    # use TPM
            'y',    # enable logging
        ]
        
        with patch('builtins.input', side_effect=mock_responses):
            with patch('os.path.exists', return_value=False):
                with patch('builtins.open', new_callable=mock_open):
                    questionnaire = TmuxQuestionnaire()
                    config = questionnaire.run_questionnaire()
        
        # Step 2: Verify questionnaire results
        assert config.prefix_key == "C-a"
        assert config.enable_mouse is True
        assert config.color_scheme == "lfgm"
        assert config.show_time is True
        assert config.use_tpm is True
        assert config.vim_navigation is True
        
        # Step 3: Generate tmux configuration
        config_dict = config.__dict__
        generator = TmuxConfigGenerator(config_dict)
        tmux_config = generator.generate_config()
        
        # Step 4: Verify generated configuration
        assert isinstance(tmux_config, str)
        assert len(tmux_config) > 500  # Should be substantial
        
        # Verify key settings made it through
        assert "set -g prefix C-a" in tmux_config
        assert "unbind C-b" in tmux_config
        assert "bind C-a send-prefix" in tmux_config
        assert "set -g mouse on" in tmux_config
        
        # Verify LFGM theme
        assert "#002d72" in tmux_config  # Mets blue
        assert "#ff671f" in tmux_config  # Mets orange
        assert "# Lfgm Color Scheme" in tmux_config
        
        # Verify vim integration
        assert "bind h select-pane -L" in tmux_config
        assert "bind j select-pane -D" in tmux_config
        assert "bind k select-pane -U" in tmux_config
        assert "bind l select-pane -R" in tmux_config
        
        # Verify TPM setup
        assert "set -g @plugin 'tmux-plugins/tpm'" in tmux_config
        assert "run '~/.tmux/plugins/tpm/tpm'" in tmux_config
        
        # Verify status bar
        assert "set -g status-left" in tmux_config
        assert "set -g status-right" in tmux_config
        assert "%Y-%m-%d" in tmux_config  # Date
        assert "%H:%M" in tmux_config     # Time
    
    def test_all_color_schemes_workflow(self):
        """Test workflow with all color schemes"""
        base_config = {
            "prefix_key": "C-b",
            "enable_mouse": True,
            "show_time": True,
            "use_tpm": False,  # Simplify for testing
            "vim_navigation": False,
        }
        
        color_schemes = ["dracula", "nord", "gruvbox", "solarized", "catppuccin", "lfgm"]
        
        for scheme in color_schemes:
            config = base_config.copy()
            config["color_scheme"] = scheme
            
            generator = TmuxConfigGenerator(config)
            tmux_config = generator.generate_config()
            
            # Should generate valid config for each scheme
            assert len(tmux_config) > 200
            assert f"# {scheme.title()} Color Scheme" in tmux_config
            assert "set -g status-bg" in tmux_config
            assert "set -g status-fg" in tmux_config
            
            # LFGM specific checks
            if scheme == "lfgm":
                assert "#002d72" in tmux_config  # Mets blue
                assert "#ff671f" in tmux_config  # Mets orange
    
    def test_plugin_integration_workflow(self):
        """Test workflow with various plugin configurations"""
        plugin_sets = [
            [],  # No plugins
            ["tmux-sensible"],  # Single plugin
            ["tmux-sensible", "tmux-resurrect", "tmux-yank"],  # Multiple plugins
            ["tmux-sensible", "tmux-resurrect", "tmux-continuum", "tmux-copycat", "tmux-yank"],  # Full set
        ]
        
        for plugins in plugin_sets:
            config = {
                "prefix_key": "C-b",
                "color_scheme": "dracula",
                "use_tpm": True,
                "plugins": plugins
            }
            
            generator = TmuxConfigGenerator(config)
            tmux_config = generator.generate_config()
            
            # Should always include TPM base
            assert "set -g @plugin 'tmux-plugins/tpm'" in tmux_config
            assert "run '~/.tmux/plugins/tpm/tpm'" in tmux_config
            
            # Should include all specified plugins
            for plugin in plugins:
                assert f"set -g @plugin 'tmux-plugins/{plugin}'" in tmux_config


@pytest.mark.integration
class TestConfigValidation:
    """Test generated configurations are valid"""
    
    def test_generated_config_syntax(self):
        """Test that generated config has valid tmux syntax"""
        config = {
            "prefix_key": "C-a",
            "enable_mouse": True,
            "color_scheme": "lfgm",
            "show_time": True,
            "show_date": True,
            "terminal_mode": "vi",
            "vim_navigation": True,
            "use_tpm": True,
            "plugins": ["tmux-sensible", "tmux-resurrect"]
        }
        
        generator = TmuxConfigGenerator(config)
        tmux_config = generator.generate_config()
        
        lines = tmux_config.split('\n')
        valid_tmux_commands = [
            'set', 'bind', 'unbind', 'run', 'if', 'display', 'new-session',
            'split-window', 'select-pane', 'resize-pane', 'kill-pane',
            'new-window', 'select-window', 'rename-window', 'kill-window'
        ]
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Should start with a valid tmux command
                first_word = line.split()[0] if line.split() else ""
                assert any(first_word.startswith(cmd) for cmd in valid_tmux_commands), \
                    f"Invalid tmux command line: {line}"
    
    def test_config_completeness(self):
        """Test that generated config includes all major sections"""
        config = {
            "prefix_key": "C-a",
            "enable_mouse": True,
            "color_scheme": "lfgm",
            "terminal_mode": "vi",
            "vim_navigation": True,
            "use_tpm": True,
            "enable_logging": True
        }
        
        generator = TmuxConfigGenerator(config)
        tmux_config = generator.generate_config()
        
        # Should include all major configuration sections
        expected_sections = [
            "CORE SETTINGS",
            "APPEARANCE",
            "BEHAVIOR SETTINGS",
            "TERMINAL INTEGRATION",
            "VIM INTEGRATION",
            "PLUGIN CONFIGURATION",
            "ADVANCED FEATURES"
        ]
        
        for section in expected_sections:
            assert section in tmux_config, f"Missing section: {section}"
    
    def test_lfgm_theme_completeness(self):
        """Test LFGM theme has complete styling"""
        config = {
            "prefix_key": "C-b",
            "color_scheme": "lfgm",
        }
        
        generator = TmuxConfigGenerator(config)
        tmux_config = generator.generate_config()
        
        # Should include comprehensive LFGM styling
        lfgm_elements = [
            "status-bg",
            "status-fg", 
            "window-status-current-style",
            "pane-border-style",
            "pane-active-border-style",
            "status-left-style",
            "status-right-style",
            "message-style"
        ]
        
        for element in lfgm_elements:
            assert element in tmux_config, f"Missing LFGM styling: {element}"
        
        # Should use Mets colors
        assert "#002d72" in tmux_config  # Primary blue
        assert "#ff671f" in tmux_config  # Primary orange


@pytest.mark.integration  
class TestErrorHandling:
    """Test error handling in integration scenarios"""
    
    def test_invalid_config_data(self):
        """Test handling of invalid configuration data"""
        invalid_configs = [
            {},  # Empty config
            {"invalid_key": "value"},  # Unknown keys
            {"prefix_key": "invalid"},  # Invalid values
            {"color_scheme": "nonexistent"},  # Unknown color scheme
        ]
        
        for config in invalid_configs:
            generator = TmuxConfigGenerator(config)
            # Should not crash, should generate something reasonable
            try:
                tmux_config = generator.generate_config()
                assert isinstance(tmux_config, str)
                assert len(tmux_config) > 0
            except Exception as e:
                pytest.fail(f"Generator crashed with config {config}: {e}")
    
    def test_missing_required_fields(self):
        """Test handling when required config fields are missing"""
        minimal_config = {"prefix_key": "C-b"}
        
        generator = TmuxConfigGenerator(minimal_config)
        tmux_config = generator.generate_config()
        
        # Should generate valid config with defaults
        assert "set -g prefix C-b" in tmux_config
        assert len(tmux_config) > 100  # Should have reasonable content
    
    def test_file_system_error_handling(self):
        """Test handling of file system errors during save"""
        questionnaire = TmuxQuestionnaire()
        questionnaire.config.prefix_key = "C-a"
        
        # Test with permission denied
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            result = questionnaire._save_config()
            assert result is False
        
        # Test with IO error
        with patch('builtins.open', side_effect=IOError("Disk full")):
            result = questionnaire._save_config()
            assert result is False


@pytest.mark.slow
class TestPerformance:
    """Test performance of the complete workflow"""
    
    def test_questionnaire_performance(self):
        """Test questionnaire completes in reasonable time"""
        import time
        
        mock_responses = ['1'] * 20  # Answer 1 to all questions
        
        start_time = time.time()
        
        with patch('builtins.input', side_effect=mock_responses):
            with patch('os.path.exists', return_value=False):
                with patch('builtins.open', new_callable=mock_open):
                    questionnaire = TmuxQuestionnaire()
                    config = questionnaire.run_questionnaire()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete quickly (under 1 second without user interaction)
        assert duration < 1.0, f"Questionnaire took too long: {duration} seconds"
        assert config is not None
    
    def test_generation_performance(self):
        """Test config generation completes quickly"""
        import time
        
        config = {
            "prefix_key": "C-a",
            "color_scheme": "lfgm",
            "use_tpm": True,
            "plugins": ["tmux-sensible", "tmux-resurrect", "tmux-continuum"]
        }
        
        start_time = time.time()
        
        generator = TmuxConfigGenerator(config)
        tmux_config = generator.generate_config()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should generate quickly
        assert duration < 0.1, f"Generation took too long: {duration} seconds"
        assert len(tmux_config) > 500  # Should generate substantial config


@pytest.mark.integration
class TestBackwardCompatibility:
    """Test backward compatibility with existing configurations"""
    
    def test_legacy_config_structure(self):
        """Test that legacy config structures still work"""
        # Simulate older config format
        legacy_config = {
            "prefix": "C-a",  # Old key name
            "mouse": True,    # Old key name
            "theme": "dracula"  # Old key name
        }
        
        # Should handle gracefully or with clear mapping
        generator = TmuxConfigGenerator(legacy_config)
        tmux_config = generator.generate_config()
        
        # Should generate something reasonable
        assert isinstance(tmux_config, str)
        assert len(tmux_config) > 100
    
    def test_config_migration(self):
        """Test migration of old configuration formats"""
        # This would test any migration logic for older configs
        old_format = {
            "colors": "dark",
            "mouse_enabled": True,
            "prefix_key": "C-a"
        }
        
        # For now, just ensure it doesn't crash
        generator = TmuxConfigGenerator(old_format)
        config = generator.generate_config()
        assert isinstance(config, str)