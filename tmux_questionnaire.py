#!/usr/bin/env python3
"""
Interactive TMUX Configuration Questionnaire
Generates the ultimate tmux configuration file for Linux power users
"""

import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
from enum import Enum


class PrefixKey(Enum):
    CTRL_B = "C-b"
    CTRL_A = "C-a"
    CTRL_SPACE = "C-Space"
    CUSTOM = "custom"


class ColorScheme(Enum):
    DEFAULT = "default"
    DRACULA = "dracula"
    NORD = "nord"
    GRUVBOX = "gruvbox"
    SOLARIZED = "solarized"
    CATPPUCCIN = "catppuccin"
    LFGM = "lfgm"
    CUSTOM = "custom"


class TerminalMode(Enum):
    EMACS = "emacs"
    VI = "vi"


@dataclass
class TmuxConfig:
    """Data class to hold all tmux configuration options"""

    # Core Settings
    prefix_key: str = "C-b"
    custom_prefix: str = ""
    enable_mouse: bool = True

    # Appearance
    color_scheme: str = "default"
    custom_colors: Optional[Dict[str, str]] = None
    show_time: bool = True
    show_date: bool = True
    show_hostname: bool = False
    show_session_name: bool = True
    show_window_status: bool = True

    # Behavior
    history_limit: int = 5000
    automatic_rename: bool = False
    renumber_windows: bool = True
    base_index: int = 1
    pane_base_index: int = 1

    # Terminal Integration
    terminal_mode: str = "vi"
    enable_256_colors: bool = True
    enable_true_colors: bool = True

    # Vim Integration
    vim_navigation: bool = False
    vim_copy_mode: bool = True

    # Plugins
    use_tpm: bool = True
    plugins: Optional[List[str]] = None

    # Advanced Features
    enable_copy_paste: bool = False
    custom_key_bindings: Optional[List[Dict[str, str]]] = None
    status_position: str = "bottom"

    # Development Features
    enable_pane_synchronization: bool = False
    enable_logging: bool = True

    def __post_init__(self):
        if self.custom_colors is None:
            self.custom_colors = {}
        if self.plugins is None:
            self.plugins = [
                "tmux-sensible",
                "tmux-resurrect",
                "tmux-continuum",
                "tmux-copycat",
                "tmux-yank",
            ]
        if self.custom_key_bindings is None:
            self.custom_key_bindings = []


class TmuxQuestionnaire:
    """Interactive questionnaire for tmux configuration"""

    def __init__(self):
        self.config = TmuxConfig()
        self.questions = self._initialize_questions()
        self.help_texts = self._initialize_help_texts()
        self.color_schemes = self._initialize_color_schemes()

    def _initialize_questions(self) -> List[Dict[str, Any]]:
        """Initialize the questionnaire structure"""
        return [
            {
                "section": "🔧 Core Settings",
                "questions": [
                    {
                        "key": "prefix_key",
                        "question": "What prefix key would you like to use?",
                        "type": "choice",
                        "choices": [
                            ("C-b", "Ctrl+B (default)"),
                            ("C-a", "Ctrl+A (popular alternative)"),
                            ("C-Space", "Ctrl+Space (recommended for Vim users)"),
                            ("custom", "Custom prefix key"),
                        ],
                        "default": "C-b",
                        "help": "prefix_key",
                    },
                    {
                        "key": "custom_prefix",
                        "question": "Enter your custom prefix key (e.g., 'C-x'):",
                        "type": "text",
                        "condition": lambda cfg: cfg.prefix_key == "custom",
                        "help": "custom_prefix",
                    },
                    {
                        "key": "enable_mouse",
                        "question": "Enable mouse support? (click to select panes, resize with drag)",
                        "type": "bool",
                        "default": True,
                        "help": "enable_mouse",
                    },
                ],
            },
            {
                "section": "🎨 Appearance & Status Bar",
                "questions": [
                    {
                        "key": "color_scheme",
                        "question": "Choose a color scheme:",
                        "type": "choice_colored",
                        "choices": [
                            ("default", "Default tmux colors"),
                            ("dracula", "Dracula theme"),
                            ("nord", "Nord theme"),
                            ("gruvbox", "Gruvbox theme"),
                            ("solarized", "Solarized theme"),
                            ("catppuccin", "Catppuccin theme"),
                            ("lfgm", "LFGM (New York Mets)"),
                            ("custom", "Custom colors"),
                        ],
                        "default": "default",
                        "help": "color_scheme",
                    },
                    {
                        "key": "show_time",
                        "question": "Show current time in status bar?",
                        "type": "bool",
                        "default": True,
                        "help": "show_time",
                    },
                    {
                        "key": "show_date",
                        "question": "Show current date in status bar?",
                        "type": "bool",
                        "default": True,
                        "help": "show_date",
                    },
                    {
                        "key": "show_hostname",
                        "question": "Show hostname in status bar?",
                        "type": "bool",
                        "default": False,
                        "help": "show_hostname",
                    },
                    {
                        "key": "status_position",
                        "question": "Status bar position:",
                        "type": "choice",
                        "choices": [("bottom", "Bottom"), ("top", "Top")],
                        "default": "bottom",
                        "help": "status_position",
                    },
                ],
            },
            {
                "section": "⚙️ Behavior & Performance",
                "questions": [
                    {
                        "key": "history_limit",
                        "question": "History buffer size (lines to keep in scrollback):",
                        "type": "number",
                        "default": 5000,
                        "min": 1000,
                        "max": 50000,
                        "help": "history_limit",
                    },
                    {
                        "key": "automatic_rename",
                        "question": "Allow automatic window renaming?",
                        "type": "bool",
                        "default": False,
                        "help": "automatic_rename",
                    },
                    {
                        "key": "renumber_windows",
                        "question": "Automatically renumber windows when one is closed?",
                        "type": "bool",
                        "default": True,
                        "help": "renumber_windows",
                    },
                    {
                        "key": "base_index",
                        "question": "Starting index for windows (0 or 1):",
                        "type": "choice",
                        "choices": [(0, "Start at 0"), (1, "Start at 1 (recommended)")],
                        "default": 1,
                        "help": "base_index",
                    },
                ],
            },
            {
                "section": "🖥️ Terminal Integration",
                "questions": [
                    {
                        "key": "terminal_mode",
                        "question": "Status line key bindings mode:",
                        "type": "choice",
                        "choices": [("emacs", "Emacs mode"), ("vi", "Vi mode")],
                        "default": "vi",
                        "help": "terminal_mode",
                    },
                    {
                        "key": "enable_256_colors",
                        "question": "Enable 256 color support?",
                        "type": "bool",
                        "default": True,
                        "help": "enable_256_colors",
                    },
                    {
                        "key": "enable_true_colors",
                        "question": "Enable true color (24-bit) support?",
                        "type": "bool",
                        "default": True,
                        "help": "enable_true_colors",
                    },
                ],
            },
            {
                "section": "🏗️ Vim Integration",
                "questions": [
                    {
                        "key": "vim_navigation",
                        "question": "Enable Vim-style pane navigation (h,j,k,l)?",
                        "type": "bool",
                        "default": False,
                        "help": "vim_navigation",
                    },
                    {
                        "key": "vim_copy_mode",
                        "question": "Enable Vim-style copy mode bindings?",
                        "type": "bool",
                        "default": True,
                        "help": "vim_copy_mode",
                    },
                ],
            },
            {
                "section": "🔌 Plugin Management",
                "questions": [
                    {
                        "key": "use_tpm",
                        "question": "Use TPM (Tmux Plugin Manager)?",
                        "type": "bool",
                        "default": True,
                        "help": "use_tpm",
                    },
                    {
                        "key": "plugins",
                        "question": "Select plugins to install:",
                        "type": "multiselect",
                        "choices": [
                            ("tmux-sensible", "Sensible defaults"),
                            ("tmux-resurrect", "Restore sessions after restart"),
                            ("tmux-continuum", "Continuous saving of sessions"),
                            ("tmux-copycat", "Enhanced search"),
                            ("tmux-yank", "System clipboard integration"),
                            ("tmux-sidebar", "File tree sidebar"),
                            ("tmux-battery", "Battery status"),
                            ("tmux-cpu", "CPU usage display"),
                            ("tmux-net-speed", "Network speed display"),
                        ],
                        "condition": lambda cfg: cfg.use_tpm,
                        "help": "plugins",
                    },
                ],
            },
            {
                "section": "🚀 Advanced Features",
                "questions": [
                    {
                        "key": "enable_pane_synchronization",
                        "question": "Enable pane synchronization toggle?",
                        "type": "bool",
                        "default": False,
                        "help": "enable_pane_synchronization",
                    },
                    {
                        "key": "enable_logging",
                        "question": "Enable session logging capabilities?",
                        "type": "bool",
                        "default": True,
                        "help": "enable_logging",
                    },
                ],
            },
        ]

    def _initialize_help_texts(self) -> Dict[str, str]:
        """Initialize help text for each configuration option"""
        return {
            "prefix_key": "The prefix key is pressed before all tmux commands. Default is Ctrl+B, but many users prefer Ctrl+A (like GNU Screen) or Ctrl+Space for easier typing.",
            "custom_prefix": "Enter a custom prefix key using tmux syntax (e.g., 'C-x' for Ctrl+X, 'M-a' for Alt+A).",
            "enable_mouse": "Mouse support allows you to click to select panes/windows, drag to resize panes, and scroll with the mouse wheel. Useful for beginners but some power users prefer keyboard-only.",
            "color_scheme": "Choose a color theme for tmux. This affects the status bar, pane borders, and window indicators. Popular themes include Dracula (dark purple), Nord (blue-gray), Gruvbox (retro), and LFGM (New York Mets blue and orange).",
            "show_time": "Display current time (HH:MM format) in the status bar. Useful for keeping track of time while working in terminal.",
            "show_date": "Display current date (YYYY-MM-DD format) in the status bar alongside or instead of time.",
            "show_hostname": "Display the hostname/computer name in status bar. Useful when working on multiple remote servers.",
            "status_position": "Position of the status bar. 'Bottom' is traditional, 'Top' can be useful if you want status info more visible.",
            "history_limit": "Number of lines kept in scrollback buffer per window. Higher values use more memory but let you scroll back further. 5000 is a good balance.",
            "automatic_rename": "Whether tmux automatically renames windows based on the running command. 'No' gives you more control over window names.",
            "renumber_windows": "When windows are closed, automatically renumber remaining windows to eliminate gaps (e.g., 1,3,5 becomes 1,2,3).",
            "base_index": "Starting number for windows and panes. '1' is more intuitive since most people don't think of '0' as the first item.",
            "terminal_mode": "Key binding style for command line editing in tmux. 'Emacs' uses Ctrl+A/E to move, 'Vi' uses h/j/k/l and modes like Vim.",
            "enable_256_colors": "Enables 256-color support for better color themes and syntax highlighting. Most modern terminals support this.",
            "enable_true_colors": "Enables 24-bit true color support for even better colors. Newer feature, ensure your terminal supports it.",
            "vim_navigation": "Use h/j/k/l keys (after prefix) to navigate between panes, just like in Vim. Natural for Vim users.",
            "vim_copy_mode": "Use Vim-style keys in copy mode: 'v' to select, 'y' to yank/copy. Makes copying text more familiar for Vim users.",
            "use_tpm": "TPM (Tmux Plugin Manager) lets you easily install and manage tmux plugins. Highly recommended for extended functionality.",
            "plugins": "Popular tmux plugins: sensible (better defaults), resurrect (save sessions), continuum (auto-save), copycat (better search), yank (clipboard), sidebar (file browser), monitoring plugins.",
            "enable_copy_paste": "Integration with system clipboard using xclip/pbcopy. Lets you copy from tmux to other applications easily.",
            "enable_pane_synchronization": "Adds a key binding to toggle synchronization across all panes in a window. When enabled, typing in one pane types in all panes simultaneously.",
            "enable_logging": "Adds key bindings to start/stop logging all terminal output to files. Useful for keeping records of terminal sessions.",
        }

    def _initialize_color_schemes(self) -> Dict[str, Dict[str, str]]:
        """Initialize ANSI color codes for each color scheme"""
        return {
            "default": {"bg": "\033[40m", "fg": "\033[37m", "accent": "\033[36m"},
            "dracula": {
                "bg": "\033[48;2;40;42;54m",
                "fg": "\033[38;2;248;248;242m",
                "accent": "\033[38;2;189;147;249m",
            },
            "nord": {
                "bg": "\033[48;2;46;52;64m",
                "fg": "\033[38;2;216;222;233m",
                "accent": "\033[38;2;94;129;172m",
            },
            "gruvbox": {
                "bg": "\033[48;2;40;40;40m",
                "fg": "\033[38;2;235;219;178m",
                "accent": "\033[38;2;214;93;14m",
            },
            "solarized": {
                "bg": "\033[48;2;0;43;54m",
                "fg": "\033[38;2;131;148;150m",
                "accent": "\033[38;2;38;139;210m",
            },
            "catppuccin": {
                "bg": "\033[48;2;30;30;46m",
                "fg": "\033[38;2;205;214;244m",
                "accent": "\033[38;2;203;166;247m",
            },
            "lfgm": {
                "bg": "\033[48;2;0;45;114m",
                "fg": "\033[38;2;255;255;255m",
                "accent": "\033[38;2;255;103;31m",
            },
            "custom": {"bg": "\033[45m", "fg": "\033[37m", "accent": "\033[33m"},
        }

    def _show_help(self, help_key: str):
        """Display help text for a configuration option"""
        help_text = self.help_texts.get(help_key, "No help available for this option.")
        print(f"\n📚 Help: {help_text}\n")

    def run_questionnaire(self) -> TmuxConfig:
        """Run the interactive questionnaire"""
        print("🚀 Welcome to the Ultimate TMUX Configuration Generator!")
        print("=" * 60)
        print("This questionnaire will help you create the perfect tmux configuration")
        print("for your Linux power user setup.")
        print("\n📚 Type '?' at any prompt for help about that option.\n")

        for section in self.questions:
            print(f"\n{section['section']}")
            print("-" * 40)

            for question in section["questions"]:
                # Check if question should be shown based on condition
                if "condition" in question and not question["condition"](self.config):
                    continue

                self._ask_question(question)

        return self.config

    def _ask_question(self, question: Dict[str, Any]):
        """Ask a single question and update config"""
        key = question["key"]
        question_text = question["question"]
        question_type = question["type"]

        help_key = question.get("help")

        if question_type == "bool":
            default = question.get("default", False)
            answer = self._ask_yes_no(question_text, default, help_key)
            setattr(self.config, key, answer)

        elif question_type == "choice":
            choices = question["choices"]
            default = question.get("default")
            answer = self._ask_choice(question_text, choices, default, help_key)
            setattr(self.config, key, answer)

        elif question_type == "choice_colored":
            choices = question["choices"]
            default = question.get("default")
            answer = self._ask_choice_colored(question_text, choices, default, help_key)
            setattr(self.config, key, answer)

        elif question_type == "multiselect":
            choices = question["choices"]
            answers = self._ask_multiselect(question_text, choices, help_key)
            setattr(self.config, key, answers)

        elif question_type == "number":
            default_num = question.get("default", 0)
            min_val = question.get("min", 0)
            max_val = question.get("max", 999999)
            answer_num = self._ask_number(
                question_text, default_num, min_val, max_val, help_key
            )
            setattr(self.config, key, answer_num)

        elif question_type == "text":
            default_text = question.get("default", "")
            answer_text = self._ask_text(question_text, default_text, help_key)
            setattr(self.config, key, answer_text)

    def _ask_yes_no(
        self, question: str, default: bool = False, help_key: Optional[str] = None
    ) -> bool:
        """Ask a yes/no question with error handling"""
        default_str = "Y/n" if default else "y/N"
        max_attempts = 5
        attempt = 0

        while attempt < max_attempts:
            try:
                response = (
                    input(f"{question} [{default_str}] (? for help): ").strip().lower()
                )
                if response == "?" and help_key:
                    self._show_help(help_key)
                    continue
                if not response:
                    return default
                if response in ["y", "yes", "1", "true"]:
                    return True
                if response in ["n", "no", "0", "false"]:
                    return False
                print("Please enter 'y' or 'n' (or '?' for help)")
                attempt += 1
            except (EOFError, KeyboardInterrupt):
                print("\n\nOperation cancelled by user.")
                raise KeyboardInterrupt("User cancelled operation")
            except Exception as e:
                print(f"Unexpected error: {e}")
                attempt += 1

        print(f"Too many invalid attempts. Using default: {'yes' if default else 'no'}")
        return default

    def _ask_choice(
        self,
        question: str,
        choices: List[tuple],
        default: Any = None,
        help_key: Optional[str] = None,
    ) -> Any:
        """Ask a multiple choice question with error handling"""
        if not choices:
            print("Error: No choices provided")
            return default

        print(f"\n{question}")
        for i, (value, description) in enumerate(choices, 1):
            marker = " (default)" if value == default else ""
            print(f"  {i}. {description}{marker}")

        max_attempts = 5
        attempt = 0

        while attempt < max_attempts:
            try:
                response = input(
                    f"Choose option [1-{len(choices)}] (? for help): "
                ).strip()
                if response == "?" and help_key:
                    self._show_help(help_key)
                    continue
                if not response and default is not None:
                    return default

                choice_num = int(response) - 1
                if 0 <= choice_num < len(choices):
                    return choices[choice_num][0]
                else:
                    print(f"Please enter a number between 1 and {len(choices)}")
            except ValueError:
                print("Please enter a valid number (or '?' for help)")

    def _ask_choice_colored(
        self,
        question: str,
        choices: List[tuple],
        default: Any = None,
        help_key: Optional[str] = None,
    ) -> Any:
        """Ask a multiple choice question with colored options for color schemes"""
        print(f"\n{question}")
        reset = "\033[0m"

        for i, (value, description) in enumerate(choices, 1):
            marker = " (default)" if value == default else ""
            if value in self.color_schemes:
                colors = self.color_schemes[value]
                colored_text = f"{colors['bg']}{colors['fg']} {description} {reset}"
                print(f"  {i}. {colored_text}{marker}")
            else:
                print(f"  {i}. {description}{marker}")

        while True:
            try:
                response = input(
                    f"Choose option [1-{len(choices)}] (? for help): "
                ).strip()
                if response == "?" and help_key:
                    self._show_help(help_key)
                    continue
                if not response and default is not None:
                    return default

                choice_num = int(response) - 1
                if 0 <= choice_num < len(choices):
                    return choices[choice_num][0]
                else:
                    print(f"Please enter a number between 1 and {len(choices)}")
            except ValueError:
                print("Please enter a valid number (or '?' for help)")

    def _ask_multiselect(
        self, question: str, choices: List[tuple], help_key: Optional[str] = None
    ) -> List[str]:
        """Ask a multiple selection question"""
        print(f"\n{question}")
        print("(Enter comma-separated numbers, or press Enter for none)")
        for i, (value, description) in enumerate(choices, 1):
            print(f"  {i}. {description}")

        while True:
            response = input("Choose options (? for help): ").strip()
            if response == "?" and help_key:
                self._show_help(help_key)
                continue
            if not response:
                return []

            try:
                selected_nums = [
                    int(x.strip()) for x in response.split(",") if x.strip()
                ]
                selected_values = []

                for num in selected_nums:
                    if 1 <= num <= len(choices):
                        selected_values.append(choices[num - 1][0])
                    else:
                        raise ValueError(f"Invalid choice: {num}")

                return selected_values
            except ValueError as e:
                print(
                    f"Error: {e}. Please enter valid numbers separated by commas (or '?' for help)."
                )

    def _ask_number(
        self,
        question: str,
        default: int,
        min_val: int,
        max_val: int,
        help_key: Optional[str] = None,
    ) -> int:
        """Ask for a numeric input"""
        while True:
            try:
                response = input(f"{question} [{default}] (? for help): ").strip()
                if response == "?" and help_key:
                    self._show_help(help_key)
                    continue
                if not response:
                    return default

                value = int(response)
                if min_val <= value <= max_val:
                    return value
                else:
                    print(f"Please enter a number between {min_val} and {max_val}")
            except ValueError:
                print("Please enter a valid number (or '?' for help)")

    def _ask_text(
        self, question: str, default: str = "", help_key: Optional[str] = None
    ) -> str:
        """Ask for text input"""
        while True:
            response = input(f"{question} [{default}] (? for help): ").strip()
            if response == "?" and help_key:
                self._show_help(help_key)
                continue
            return response if response else default

    def _save_config(self, partial: bool = False) -> bool:
        """Save configuration to JSON file with error handling"""
        try:
            # Save configuration to JSON for the generator
            config_path = os.path.join(os.path.dirname(__file__), "tmux_config.json")

            # If this is a partial save, keep a backup
            if partial and os.path.exists(config_path):
                import shutil

                backup_path = config_path + ".backup"
                shutil.copy2(config_path, backup_path)

            with open(config_path, "w") as f:
                json.dump(asdict(self.config), f, indent=2)

            return True

        except (IOError, OSError, PermissionError) as e:
            print(f"⚠️  Warning: Could not save configuration: {e}")
            return False
        except Exception as e:
            print(f"⚠️  Warning: Unexpected error saving configuration: {e}")
            return False


def main():
    """Main function to run the questionnaire"""
    try:
        questionnaire = TmuxQuestionnaire()
        config = questionnaire.run_questionnaire()

        print("\n" + "=" * 60)
        print("🎉 Configuration complete!")
        print("=" * 60)

        # Save configuration using the error-handling method
        if questionnaire._save_config():
            config_path = os.path.join(os.path.dirname(__file__), "tmux_config.json")
            print(f"Configuration saved to: {config_path}")
            print("\nNext steps:")
            print("1. Run the tmux config generator to create your .tmux.conf file")
            print("2. Copy the generated config to ~/.tmux.conf")
            print("3. Reload tmux or start a new session to apply changes")
        else:
            print("⚠️  Configuration could not be saved. Please check file permissions.")

        return config

    except KeyboardInterrupt:
        print("\n\n⚠️  Questionnaire interrupted by user.")
        print("Configuration may be incomplete. Run again to complete setup.")
        return None
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please try running the questionnaire again.")
        return None


if __name__ == "__main__":
    main()
