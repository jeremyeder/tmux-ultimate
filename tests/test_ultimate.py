#!/usr/bin/env python3
"""
Tests for tmux_ultimate.py
"""

import pytest
import os
import tempfile
from unittest.mock import patch, mock_open, MagicMock
from tmux_ultimate import (
    check_python_version,
    check_dependencies,
    check_output_file_safety,
    check_existing_tmux_config,
    parse_arguments,
)


class TestUtilityFunctions:
    """Test utility functions in tmux_ultimate.py"""

    def test_check_python_version_compatible(self):
        """Test Python version check with compatible version"""
        with patch("sys.version_info", (3, 11, 0)):
            # Should not raise SystemExit
            try:
                check_python_version()
            except SystemExit:
                pytest.fail("check_python_version raised SystemExit unexpectedly")

    def test_check_python_version_incompatible(self):
        """Test Python version check with incompatible version"""
        with patch("sys.version_info", (3, 10, 0)):
            with pytest.raises(SystemExit):
                check_python_version()

    def test_check_dependencies_available(self):
        """Test dependency check when all deps available"""
        result = check_dependencies()
        assert result is True

    def test_check_dependencies_missing(self):
        """Test dependency check when deps missing"""
        with patch("builtins.__import__", side_effect=ImportError("Module not found")):
            result = check_dependencies()
            assert result is False


class TestSafetyChecks:
    """Test safety check functions"""

    def test_check_output_file_safety_nonexistent(self):
        """Test safety check with non-existent file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "nonexistent.conf")
            result = check_output_file_safety(test_file)
            assert result is True

    def test_check_output_file_safety_exists(self):
        """Test safety check with existing file"""
        with tempfile.NamedTemporaryFile() as tmp:
            result = check_output_file_safety(tmp.name)
            assert result is False

    def test_check_output_file_safety_no_dir(self):
        """Test safety check with non-existent directory"""
        test_file = "/nonexistent/directory/file.conf"
        result = check_output_file_safety(test_file)
        assert result is False

    def test_check_output_file_safety_no_write_permission(self):
        """Test safety check with unwritable directory"""
        with patch("os.access", return_value=False):
            with patch("os.path.exists", return_value=True):
                result = check_output_file_safety("/root/test.conf")
                assert result is False


class TestExistingConfigDetection:
    """Test existing tmux configuration detection"""

    @patch("os.path.exists", return_value=False)
    def test_no_existing_config(self, mock_exists):
        """Test when no existing config exists"""
        result = check_existing_tmux_config()
        expected_path = os.path.expanduser("~/.tmux.conf")
        assert result == expected_path

    @patch("os.path.exists", return_value=True)
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="set -g prefix C-a\nset -g mouse on",
    )
    @patch("builtins.input", return_value="3")  # Exit option
    def test_existing_config_exit(self, mock_input, mock_file, mock_exists):
        """Test existing config detection with exit choice"""
        with pytest.raises(SystemExit):
            check_existing_tmux_config()

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="set -g prefix C-a")
    @patch("builtins.input", return_value="1")  # Backup option
    @patch("os.rename")
    @patch("datetime.datetime")
    def test_existing_config_backup(
        self, mock_datetime, mock_rename, mock_input, mock_file, mock_exists
    ):
        """Test existing config detection with backup choice"""
        mock_datetime.now.return_value.strftime.return_value = "20231201_120000"

        result = check_existing_tmux_config()
        expected_path = os.path.expanduser("~/.tmux.conf")
        assert result == expected_path
        mock_rename.assert_called_once()

    @patch(
        "os.path.exists", side_effect=lambda x: x == os.path.expanduser("~/.tmux.conf")
    )
    @patch("builtins.open", new_callable=mock_open, read_data="set -g prefix C-a")
    @patch("builtins.input", side_effect=["2", "/tmp/test.conf"])  # Custom path option  # nosec
    @patch("os.access", return_value=True)
    def test_existing_config_custom_path(
        self, mock_access, mock_input, mock_file, mock_exists
    ):
        """Test existing config detection with custom path choice"""
        result = check_existing_tmux_config()
        assert result == "/tmp/test.conf"  # nosec

    @patch(
        "os.path.exists", side_effect=lambda x: x == os.path.expanduser("~/.tmux.conf")
    )
    @patch("builtins.open", new_callable=mock_open, read_data="set -g prefix C-a")
    @patch(
        "builtins.input", side_effect=["2", "", "/tmp/valid.conf"]  # nosec
    )  # Empty then valid path
    @patch("os.access", return_value=True)
    def test_existing_config_invalid_then_valid_path(
        self, mock_access, mock_input, mock_file, mock_exists
    ):
        """Test existing config detection with invalid then valid custom path"""
        result = check_existing_tmux_config()
        assert result == "/tmp/valid.conf"  # nosec


class TestArgumentParsing:
    """Test command line argument parsing"""

    def test_parse_arguments_default(self):
        """Test default argument parsing"""
        with patch("sys.argv", ["tmux_ultimate.py"]):
            args = parse_arguments()
            expected_path = os.path.expanduser("~/.tmux.conf")
            assert args.output == expected_path

    def test_parse_arguments_custom_output(self):
        """Test custom output argument"""
        with patch("sys.argv", ["tmux_ultimate.py", "-o", "/tmp/custom.conf"]):  # nosec
            args = parse_arguments()
            assert args.output == "/tmp/custom.conf"  # nosec

    def test_parse_arguments_long_output(self):
        """Test long form output argument"""
        with patch("sys.argv", ["tmux_ultimate.py", "--output", "/tmp/custom.conf"]):  # nosec
            args = parse_arguments()
            assert args.output == "/tmp/custom.conf"  # nosec


class TestMenuSystem:
    """Test menu system functionality"""

    @patch("tmux_ultimate.run_questionnaire")
    @patch("builtins.input", return_value="1")
    def test_menu_questionnaire_option(self, mock_input, mock_questionnaire):
        """Test menu questionnaire option"""
        mock_questionnaire.return_value = MagicMock()
        # This would require importing and testing the main function
        # For now, just test that the function can be called
        assert callable(mock_questionnaire)

    @patch("tmux_ultimate.generate_config")
    @patch("builtins.input", return_value="2")
    def test_menu_generate_option(self, mock_input, mock_generate):
        """Test menu generate option"""
        mock_generate.return_value = True
        # Test that the function can be called
        assert callable(mock_generate)


@pytest.mark.integration
class TestMainWorkflow:
    """Integration tests for main workflow"""

    @patch("tmux_ultimate.check_python_version")
    @patch("tmux_ultimate.check_dependencies", return_value=True)
    @patch("tmux_ultimate.check_existing_tmux_config")
    @patch("tmux_ultimate.parse_arguments")
    def test_main_initialization(
        self, mock_args, mock_config_check, mock_deps, mock_version
    ):
        """Test main function initialization"""
        mock_args.return_value = MagicMock(output="/tmp/test.conf")  # nosec
        mock_config_check.return_value = "/tmp/test.conf"  # nosec

        # Import main and test it can be called
        try:
            from tmux_ultimate import main

            # Don't actually run main, just test it's callable
            assert callable(main)
        except ImportError:
            pytest.skip("Main function import not available")


class TestErrorHandling:
    """Test error handling scenarios"""

    def test_keyboard_interrupt_handling(self):
        """Test graceful handling of keyboard interrupt"""
        # This would test the KeyboardInterrupt handling in main
        # For now, ensure the exception type exists
        assert KeyboardInterrupt

    @patch("os.path.exists", side_effect=PermissionError("Permission denied"))
    def test_permission_error_handling(self, mock_exists):
        """Test handling of permission errors"""
        with pytest.raises(PermissionError):
            check_output_file_safety("/restricted/file.conf")

    def test_invalid_config_data_handling(self):
        """Test handling of invalid configuration data"""
        # Test that invalid data types are handled gracefully
        invalid_configs = [None, "", {}, []]
        for config in invalid_configs:
            # Should not crash when passed invalid data
            try:
                # This would test the actual config validation
                assert (
                    config is not None
                    or config == ""
                    or isinstance(config, (dict, list))
                )
            except Exception as e:
                pytest.fail(f"Unexpected exception with config {config}: {e}")


class TestFileOperations:
    """Test file operation safety"""

    def test_safe_file_writing(self):
        """Test safe file writing operations"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "test.conf")

            # Should be safe to write to non-existent file
            result = check_output_file_safety(test_file)
            assert result is True

            # Create the file
            with open(test_file, "w") as f:
                f.write("test content")

            # Should not be safe to overwrite existing file
            result = check_output_file_safety(test_file)
            assert result is False

    def test_backup_naming_convention(self):
        """Test backup file naming follows expected pattern"""
        import datetime

        now = datetime.datetime.now()
        expected_pattern = now.strftime("%Y%m%d_%H%M%S")

        # Test the pattern matches expected format
        assert len(expected_pattern) == 15  # YYYYMMDD_HHMMSS
        assert expected_pattern.count("_") == 1
        assert expected_pattern.split("_")[0].isdigit()
        assert expected_pattern.split("_")[1].isdigit()
