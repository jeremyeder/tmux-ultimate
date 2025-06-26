#!/usr/bin/env python3
"""
Tests for tmux_questionnaire.py
"""

import pytest
import json
from unittest.mock import patch, mock_open, MagicMock
from tmux_questionnaire import TmuxQuestionnaire, TmuxConfig


class TestTmuxConfig:
    """Test the TmuxConfig dataclass"""

    def test_config_defaults(self):
        """Test that config has sensible defaults"""
        config = TmuxConfig()
        assert config.prefix_key == "C-b"
        assert config.enable_mouse is True
        assert config.color_scheme == "default"
        assert config.terminal_mode == "vi"
        assert config.use_tpm is True

    def test_config_to_dict(self):
        """Test config can be converted to dictionary"""
        config = TmuxConfig()
        config_dict = config.__dict__
        assert isinstance(config_dict, dict)
        assert "prefix_key" in config_dict
        assert "color_scheme" in config_dict


class TestTmuxQuestionnaire:
    """Test the TmuxQuestionnaire class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.questionnaire = TmuxQuestionnaire()

    def test_initialization(self):
        """Test questionnaire initializes correctly"""
        assert self.questionnaire.config is not None
        assert hasattr(self.questionnaire, "questions")
        assert hasattr(self.questionnaire, "help_texts")
        assert hasattr(self.questionnaire, "color_schemes")

    def test_color_schemes_initialization(self):
        """Test color schemes are properly initialized"""
        color_schemes = self.questionnaire._initialize_color_schemes()
        assert "dracula" in color_schemes
        assert "nord" in color_schemes
        assert "lfgm" in color_schemes

        # Test LFGM theme colors
        lfgm = color_schemes["lfgm"]
        assert "bg" in lfgm
        assert "fg" in lfgm
        assert "accent" in lfgm

    def test_help_texts_initialization(self):
        """Test help texts are properly initialized"""
        help_texts = self.questionnaire._initialize_help_texts()
        assert "color_scheme" in help_texts
        assert "LFGM" in help_texts["color_scheme"]
        assert "prefix_key" in help_texts

    @patch("builtins.input", return_value="y")
    def test_ask_yes_no_default_yes(self, mock_input):
        """Test yes/no question with default yes"""
        result = self.questionnaire._ask_yes_no("Test question?", True)
        assert result is True

    @patch("builtins.input", return_value="n")
    def test_ask_yes_no_explicit_no(self, mock_input):
        """Test yes/no question with explicit no"""
        result = self.questionnaire._ask_yes_no("Test question?", True)
        assert result is False

    @patch("builtins.input", return_value="")
    def test_ask_yes_no_default_fallback(self, mock_input):
        """Test yes/no question falls back to default"""
        result = self.questionnaire._ask_yes_no("Test question?", False)
        assert result is False

    @patch("builtins.input", side_effect=["invalid", "y"])
    def test_ask_yes_no_invalid_then_valid(self, mock_input):
        """Test yes/no question handles invalid input"""
        result = self.questionnaire._ask_yes_no("Test question?", False)
        assert result is True

    @patch("builtins.input", return_value="1")
    def test_ask_choice_first_option(self, mock_input):
        """Test choice question selects first option"""
        choices = [("opt1", "Option 1"), ("opt2", "Option 2")]
        result = self.questionnaire._ask_choice("Choose:", choices, "opt1")
        assert result == "opt1"

    @patch("builtins.input", return_value="2")
    def test_ask_choice_second_option(self, mock_input):
        """Test choice question selects second option"""
        choices = [("opt1", "Option 1"), ("opt2", "Option 2")]
        result = self.questionnaire._ask_choice("Choose:", choices, "opt1")
        assert result == "opt2"

    @patch("builtins.input", return_value="")
    def test_ask_choice_default(self, mock_input):
        """Test choice question uses default"""
        choices = [("opt1", "Option 1"), ("opt2", "Option 2")]
        result = self.questionnaire._ask_choice("Choose:", choices, "opt2")
        assert result == "opt2"

    @patch("builtins.input", side_effect=["0", "1"])
    def test_ask_choice_invalid_then_valid(self, mock_input):
        """Test choice question handles invalid input"""
        choices = [("opt1", "Option 1"), ("opt2", "Option 2")]
        result = self.questionnaire._ask_choice("Choose:", choices, "opt1")
        assert result == "opt1"

    @patch("builtins.input", return_value="test_value")
    def test_ask_text_input(self, mock_input):
        """Test text input question"""
        result = self.questionnaire._ask_text("Enter text:", "default")
        assert result == "test_value"

    @patch("builtins.input", return_value="")
    def test_ask_text_default(self, mock_input):
        """Test text input uses default when empty"""
        result = self.questionnaire._ask_text("Enter text:", "default")
        assert result == "default"

    @patch("builtins.input", return_value="?")
    @patch("builtins.print")
    def test_help_system(self, mock_print, mock_input):
        """Test that help system is called"""
        with patch.object(self.questionnaire, "_show_help") as mock_help:
            # Mock a second input after help
            mock_input.side_effect = ["?", "y"]
            result = self.questionnaire._ask_yes_no("Test?", True, "test_help")
            mock_help.assert_called_once_with("test_help")

    @patch("builtins.input", return_value="1")
    def test_ask_choice_colored(self, mock_input):
        """Test colored choice question"""
        choices = [("dracula", "Dracula theme"), ("nord", "Nord theme")]
        result = self.questionnaire._ask_choice_colored(
            "Choose theme:", choices, "dracula"
        )
        assert result == "dracula"

    @patch("os.path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open)
    def test_save_config(self, mock_file, mock_exists):
        """Test configuration saving"""
        self.questionnaire.config.color_scheme = "lfgm"
        self.questionnaire.config.prefix_key = "C-a"

        result = self.questionnaire._save_config()
        assert result is True
        mock_file.assert_called_once()

    @patch("os.path.exists", return_value=True)
    def test_save_config_file_exists(self, mock_exists):
        """Test save fails when file exists"""
        result = self.questionnaire._save_config()
        assert result is False


class TestIntegration:
    """Integration tests for questionnaire workflow"""

    @patch("builtins.input")
    @patch("os.path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open)
    def test_complete_questionnaire_workflow(self, mock_file, mock_exists, mock_input):
        """Test complete questionnaire workflow"""
        # Mock user inputs for a complete run
        mock_input.side_effect = [
            "2",  # prefix key: C-a
            "y",  # enable mouse
            "6",  # color scheme: LFGM
            "y",  # show time
            "y",  # show date
            "n",  # show hostname
            "1",  # status position: bottom
            "5000",  # history limit
            "n",  # automatic rename
            "y",  # renumber windows
            "1",  # base index
            "1",  # pane base index
            "1",  # terminal mode: vi
            "y",  # 256 colors
            "y",  # true colors
            "y",  # vim navigation
            "y",  # vim copy mode
            "y",  # use TPM
            "y",  # enable logging
        ]

        questionnaire = TmuxQuestionnaire()
        config = questionnaire.run_questionnaire()

        assert config.prefix_key == "C-a"
        assert config.enable_mouse is True
        assert config.color_scheme == "lfgm"
        assert config.terminal_mode == "vi"
        assert config.use_tpm is True


@pytest.mark.integration
class TestConfigValidation:
    """Test configuration validation"""

    def test_all_color_schemes_valid(self):
        """Test all color schemes have required fields"""
        questionnaire = TmuxQuestionnaire()
        color_schemes = questionnaire._initialize_color_schemes()

        for scheme_name, scheme_colors in color_schemes.items():
            assert "bg" in scheme_colors, f"Missing bg in {scheme_name}"
            assert "fg" in scheme_colors, f"Missing fg in {scheme_name}"
            assert "accent" in scheme_colors, f"Missing accent in {scheme_name}"

    def test_lfgm_theme_colors(self):
        """Test LFGM theme has proper Mets colors"""
        questionnaire = TmuxQuestionnaire()
        color_schemes = questionnaire._initialize_color_schemes()
        lfgm = color_schemes["lfgm"]

        # Test that LFGM contains Mets blue and orange
        assert "48;2;0;45;114" in lfgm["bg"]  # Mets blue background
        assert "38;2;255;103;31" in lfgm["accent"]  # Mets orange accent
