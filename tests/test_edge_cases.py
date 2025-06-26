#!/usr/bin/env python3
"""
Tests for edge case handling improvements
"""

import pytest
from unittest.mock import patch, mock_open
from tmux_generator import TmuxConfigGenerator
from tmux_questionnaire import TmuxQuestionnaire


class TestGeneratorEdgeCases:
    """Test edge cases in TmuxConfigGenerator"""

    def test_none_config_data(self):
        """Test generator handles None config data gracefully"""
        generator = TmuxConfigGenerator(None)
        config = generator.generate_config()

        assert isinstance(config, str)
        assert len(config) > 100
        assert "set -g prefix C-b" in config  # Should use default

    def test_empty_config_data(self):
        """Test generator handles empty config data"""
        generator = TmuxConfigGenerator({})
        config = generator.generate_config()

        assert isinstance(config, str)
        assert len(config) > 100
        assert "set -g prefix C-b" in config  # Should use default

    def test_invalid_config_type(self):
        """Test generator rejects non-dict config data"""
        with pytest.raises(TypeError):
            TmuxConfigGenerator("invalid")

        with pytest.raises(TypeError):
            TmuxConfigGenerator(123)

        with pytest.raises(TypeError):
            TmuxConfigGenerator([])

    def test_invalid_config_values(self):
        """Test generator sanitizes invalid config values"""
        invalid_config = {
            "prefix_key": 123,  # Should be string
            "enable_mouse": "yes",  # Should be bool
            "history_limit": "lots",  # Should be int
            "color_scheme": "nonexistent",  # Invalid scheme
            "terminal_mode": "invalid",  # Invalid mode
            "plugins": "not a list",  # Should be list
            "unknown_key": "ignored",  # Unknown key
        }

        generator = TmuxConfigGenerator(invalid_config)
        config = generator.generate_config()

        # Should generate valid config with defaults
        assert isinstance(config, str)
        assert len(config) > 100
        assert "set -g prefix C-b" in config  # Default prefix
        assert "set -g history-limit 5000" in config  # Default history

    def test_extreme_values(self):
        """Test generator handles extreme values properly"""
        extreme_config = {
            "history_limit": -1000,  # Too low
            "base_index": 99,  # Invalid
            "status_position": "sideways",  # Invalid
        }

        generator = TmuxConfigGenerator(extreme_config)
        config = generator.generate_config()

        # Should use safe defaults
        assert "set -g history-limit 5000" in config
        assert "set -g base-index 1" in config
        assert "set -g status-position bottom" in config


class TestQuestionnaireEdgeCases:
    """Test edge cases in TmuxQuestionnaire"""

    @patch("builtins.open", side_effect=PermissionError("Access denied"))
    def test_save_config_permission_error(self, mock_file):
        """Test questionnaire handles file permission errors"""
        questionnaire = TmuxQuestionnaire()
        result = questionnaire._save_config()
        assert result is False

    @patch("builtins.open", side_effect=IOError("Disk full"))
    def test_save_config_io_error(self, mock_file):
        """Test questionnaire handles IO errors"""
        questionnaire = TmuxQuestionnaire()
        result = questionnaire._save_config()
        assert result is False

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump", side_effect=ValueError("Invalid JSON"))
    def test_save_config_json_error(self, mock_json, mock_file):
        """Test questionnaire handles JSON serialization errors"""
        questionnaire = TmuxQuestionnaire()
        result = questionnaire._save_config()
        assert result is False

    @patch("builtins.open", new_callable=mock_open)
    def test_save_config_success(self, mock_file):
        """Test questionnaire saves config successfully"""
        questionnaire = TmuxQuestionnaire()
        result = questionnaire._save_config()
        assert result is True

    def test_config_defaults_completeness(self):
        """Test that all config keys have proper defaults"""
        questionnaire = TmuxQuestionnaire()
        config = questionnaire.config

        # Check that all expected attributes exist
        expected_attrs = [
            "prefix_key",
            "enable_mouse",
            "color_scheme",
            "show_time",
            "show_date",
            "history_limit",
            "terminal_mode",
            "use_tpm",
            "vim_navigation",
            "vim_copy_mode",
            "plugins",
        ]

        for attr in expected_attrs:
            assert hasattr(config, attr), f"Missing config attribute: {attr}"


class TestIntegrationEdgeCases:
    """Test edge cases in the complete workflow"""

    def test_malformed_json_recovery(self):
        """Test recovery from malformed config JSON"""
        malformed_json = '{"prefix_key": "C-a", "invalid_json'

        with patch("builtins.open", mock_open(read_data=malformed_json)):
            # Should handle gracefully and use defaults
            try:
                import json

                config_data = json.loads(malformed_json)
            except json.JSONDecodeError:
                config_data = {}  # Fallback to empty config

            generator = TmuxConfigGenerator(config_data)
            config = generator.generate_config()

            assert isinstance(config, str)
            assert len(config) > 100

    def test_partial_config_completion(self):
        """Test generator completes partial configurations"""
        partial_config = {
            "prefix_key": "C-a",
            "color_scheme": "lfgm",
            # Missing many other keys
        }

        generator = TmuxConfigGenerator(partial_config)
        config = generator.generate_config()

        # Should include the specified options
        assert "set -g prefix C-a" in config
        assert "#002d72" in config  # LFGM blue

        # Should also include defaults for missing options
        assert "set -g mouse on" in config  # Default mouse setting
        assert "set -g history-limit 5000" in config  # Default history

    def test_unicode_and_special_characters(self):
        """Test handling of unicode and special characters in config"""
        special_config = {
            "custom_prefix": "ñ",  # Unicode character
            "color_scheme": "test with spaces",  # Invalid scheme name
        }

        generator = TmuxConfigGenerator(special_config)
        config = generator.generate_config()

        # Should handle gracefully and use defaults
        assert isinstance(config, str)
        assert len(config) > 100
