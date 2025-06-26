#!/usr/bin/env python3
"""
TMUX Ultimate Configuration Generator
Main launcher script for the complete tmux configuration system
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path


def print_banner():
    """Print the application banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  ████████╗███╗   ███╗██╗   ██╗██╗  ██╗    ██╗   ██╗██╗  ████████╗ ║
║  ╚══██╔══╝████╗ ████║██║   ██║╚██╗██╔╝    ██║   ██║██║  ╚══██╔══╝ ║
║     ██║   ██╔████╔██║██║   ██║ ╚███╔╝     ██║   ██║██║     ██║    ║
║     ██║   ██║╚██╔╝██║██║   ██║ ██╔██╗     ██║   ██║██║     ██║    ║
║     ██║   ██║ ╚═╝ ██║╚██████╔╝██╔╝ ██╗    ╚██████╔╝███████╗██║    ║
║     ╚═╝   ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝     ╚═════╝ ╚══════╝╚═╝    ║
║                                                                   ║
║              🚀 Ultimate TMUX Configuration Generator             ║
║                   For Linux Power Users                          ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("❌ Error: Python 3.6 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)


def check_dependencies():
    """Check if required dependencies are available"""
    try:
        import json
        import dataclasses
        return True
    except ImportError as e:
        print(f"❌ Error: Missing required dependency: {e}")
        return False


def show_menu():
    """Show the main menu"""
    print("\n🎯 What would you like to do?")
    print("=" * 50)
    print("1. 📝 Run Configuration Questionnaire")
    print("2. ⚙️  Generate TMUX Configuration")
    print("3. 🔄 Complete Setup (Questionnaire + Generation)")
    print("4. 📖 View Current Configuration")
    print("5. 🔌 Install TPM & Plugins")
    print("6. 🧹 Clean Generated Files")
    print("7. ℹ️  Show Help & Instructions")
    print("8. 🚪 Exit")
    print("=" * 50)


def run_questionnaire():
    """Run the configuration questionnaire"""
    print("\n🚀 Starting Configuration Questionnaire...")
    try:
        from tmux_questionnaire import main as questionnaire_main
        return questionnaire_main()
    except ImportError:
        print("❌ Error: questionnaire module not found")
        return None
    except Exception as e:
        print(f"❌ Error running questionnaire: {e}")
        return None


def generate_config(output_path: str = None):
    """Generate the tmux configuration"""
    print("\n⚙️ Generating TMUX Configuration...")
    try:
        from tmux_generator import TmuxConfigGenerator
        import json
        
        config_json_path = os.path.join(os.path.dirname(__file__), 'tmux_config.json')
        if not os.path.exists(config_json_path):
            print("❌ Configuration file not found!")
            print("   Please run the questionnaire first.")
            return False
        
        # Load configuration
        with open(config_json_path, 'r') as f:
            config_data = json.load(f)
        
        # Generate configuration
        generator = TmuxConfigGenerator(config_data)
        tmux_config = generator.generate_config()
        
        # Determine output path
        if output_path is None:
            output_path = os.path.join(os.path.dirname(__file__), 'tmux.conf')
        
        # Final safety check
        if os.path.exists(output_path):
            print(f"❌ Safety check failed: {output_path} already exists!")
            return False
        
        # Save configuration
        with open(output_path, 'w') as f:
            f.write(tmux_config)
        
        print("🎉 TMUX configuration generated successfully!")
        print(f"📄 Configuration saved to: {output_path}")
        return True
        
    except ImportError:
        print("❌ Error: generator module not found")
        return False
    except Exception as e:
        print(f"❌ Error generating configuration: {e}")
        return False


def view_configuration(output_path: str = "tmux.conf"):
    """View the current configuration"""
    config_file = Path(output_path) if os.path.isabs(output_path) else Path("tmux.conf")
    if not config_file.exists():
        print("❌ No configuration file found!")
        print(f"   Expected location: {config_file.absolute()}")
        print("   Please generate a configuration first.")
        return
    
    print("\n📖 Current TMUX Configuration:")
    print("=" * 60)
    try:
        with open(config_file, 'r') as f:
            content = f.read()
            # Show first 50 lines to avoid overwhelming output
            lines = content.split('\n')
            for i, line in enumerate(lines[:50], 1):
                print(f"{i:3d}: {line}")
            
            if len(lines) > 50:
                print(f"... and {len(lines) - 50} more lines")
                print(f"\nTotal lines: {len(lines)}")
        
        print("=" * 60)
        print(f"📄 Full file available at: {config_file.absolute()}")
        
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")


def install_tpm_and_plugins():
    """Install TPM and configured plugins"""
    print("\n🔌 Installing TPM and Plugins...")
    
    # Check if config exists to see what plugins are enabled
    config_json_path = os.path.join(os.path.dirname(__file__), 'tmux_config.json')
    plugins = []
    
    if os.path.exists(config_json_path):
        try:
            import json
            with open(config_json_path, 'r') as f:
                config_data = json.load(f)
            plugins = config_data.get('plugins', [])
            use_tpm = config_data.get('use_tpm', False)
            
            if not use_tpm:
                print("⚠️  TPM is not enabled in your configuration.")
                print("   Please run the questionnaire and enable TPM first.")
                return False
                
        except Exception as e:
            print(f"❌ Error reading configuration: {e}")
            return False
    else:
        print("❌ Configuration file not found!")
        print("   Please run the questionnaire first.")
        return False
    
    try:
        # Install TPM
        tpm_dir = os.path.expanduser("~/.tmux/plugins/tpm")
        if not os.path.exists(tpm_dir):
            print("📦 Installing TPM (Tmux Plugin Manager)...")
            result = subprocess.run([
                "git", "clone", "https://github.com/tmux-plugins/tpm", tpm_dir
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ TPM installed successfully!")
            else:
                print(f"❌ Failed to install TPM: {result.stderr}")
                return False
        else:
            print("✅ TPM already installed.")
        
        # Show plugin installation instructions
        print(f"\n🔌 Plugins configured: {', '.join(plugins) if plugins else 'None'}")
        
        if plugins:
            print("\n📝 To install plugins:")
            print("   1. Start tmux: tmux")
            print("   2. Press: Prefix + I  (that's Prefix + Shift + i)")
            print("   3. Wait for plugins to install")
            print("   4. Press: Prefix + r  (to reload config)")
            
            print("\n💡 Plugin installation is interactive and must be done from within tmux.")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        return False


def clean_files():
    """Clean generated files"""
    files_to_clean = [
        "tmux_config.json",
        "tmux.conf"
    ]
    
    cleaned = []
    for file in files_to_clean:
        if Path(file).exists():
            try:
                Path(file).unlink()
                cleaned.append(file)
            except Exception as e:
                print(f"❌ Error deleting {file}: {e}")
    
    if cleaned:
        print(f"🧹 Cleaned files: {', '.join(cleaned)}")
    else:
        print("✨ No files to clean!")


def show_help():
    """Show help and instructions"""
    help_text = """
🔧 TMUX Ultimate Configuration Generator Help
═══════════════════════════════════════════════════════════════════

📋 OVERVIEW:
This tool helps you create the perfect tmux configuration for your 
Linux power user setup through an interactive questionnaire.

🚀 GETTING STARTED:
1. Run the questionnaire to define your preferences
2. Generate your custom tmux configuration
3. Install and apply the configuration

📝 CONFIGURATION AREAS:
• Core Settings (prefix key, mouse support)
• Appearance & Status Bar (colors, themes, layout)
• Behavior & Performance (history, indexing, naming)
• Terminal Integration (color support, key modes)
• Vim Integration (navigation, copy mode)
• Plugin Management (TPM, popular plugins)
• Advanced Features (clipboard, logging, synchronization)

⚙️ INSTALLATION STEPS:
1. Generate your configuration using this tool
2. Copy generated file: cp tmux.conf ~/.tmux.conf
3. If using plugins, install TPM first:
   git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
4. Reload tmux: tmux source-file ~/.tmux.conf
5. Install plugins (if any): Prefix + I

🔧 CUSTOMIZATION:
• All settings are configurable through the questionnaire
• Advanced users can edit the generated config file directly
• Multiple color schemes supported (Dracula, Nord, Gruvbox, etc.)
• Vim integration for seamless workflow

📚 USEFUL TMUX COMMANDS:
• Prefix + r : Reload configuration
• Prefix + | : Split window horizontally  
• Prefix + - : Split window vertically
• Prefix + h/j/k/l : Navigate panes (if Vim mode enabled)
• Alt + arrows : Navigate panes without prefix

🆘 TROUBLESHOOTING:
• Make sure tmux is installed: sudo apt install tmux (or equivalent)
• Check tmux version: tmux -V (2.6+ recommended)
• Verify Python 3.6+: python3 --version
• For plugin issues, ensure TPM is properly installed

📖 MORE RESOURCES:
• TMUX Manual: man tmux
• TMUX Wiki: https://github.com/tmux/tmux/wiki
• Popular configurations: Search "tmux.conf" on GitHub

═══════════════════════════════════════════════════════════════════
"""
    print(help_text)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="TMUX Ultimate Configuration Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 tmux_ultimate.py                    # Interactive mode, default output
  python3 tmux_ultimate.py -o /tmp/test.conf  # Interactive mode, custom output
  python3 tmux_ultimate.py -o ~/.tmux.conf    # Interactive mode, specific output

Safety: This tool will NEVER overwrite existing tmux configurations.
If the target file exists, the tool will warn you and exit safely.
        """
    )
    
    parser.add_argument(
        "-o", "--output",
        default=os.path.expanduser("~/.tmux.conf"),
        help="Output file path (default: ~/.tmux.conf)"
    )
    
    return parser.parse_args()


def check_output_file_safety(output_path: str) -> bool:
    """Check if output file is safe to write (doesn't exist)"""
    if os.path.exists(output_path):
        print(f"\n🛡️  SAFETY CHECK FAILED!")
        print(f"❌ File already exists: {output_path}")
        print(f"\n🔒 This tool will NEVER overwrite existing tmux configurations.")
        print(f"\n💡 Options:")
        print(f"   1. Use a different output path: -o /tmp/my-tmux.conf")
        print(f"   2. Move your existing config: mv {output_path} {output_path}.backup")
        print(f"   3. Choose a different filename")
        print(f"\n👋 Exiting safely to protect your existing configuration.")
        return False
    
    # Check if directory exists and is writable
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        print(f"❌ Output directory does not exist: {output_dir}")
        return False
    
    if output_dir and not os.access(output_dir, os.W_OK):
        print(f"❌ Output directory is not writable: {output_dir}")
        return False
    
    return True


def main():
    """Main application entry point"""
    args = parse_arguments()
    
    check_python_version()
    
    if not check_dependencies():
        sys.exit(1)
    
    # Safety check for output file
    if not check_output_file_safety(args.output):
        sys.exit(1)
    
    print_banner()
    print(f"\n📄 Output file: {args.output}")
    print(f"🛡️  Safety verified: File does not exist - safe to proceed\n")
    
    while True:
        show_menu()
        
        try:
            choice = input("\n🎯 Enter your choice (1-8): ").strip()
            
            if choice == '1':
                run_questionnaire()
                
            elif choice == '2':
                generate_config(args.output)
                
            elif choice == '3':
                print("\n🔄 Running Complete Setup...")
                config = run_questionnaire()
                if config:
                    print("\n" + "="*50)
                    generate_config(args.output)
                
            elif choice == '4':
                view_configuration(args.output)
                
            elif choice == '5':
                install_tpm_and_plugins()
                
            elif choice == '6':
                clean_files()
                
            elif choice == '7':
                show_help()
                
            elif choice == '8':
                print("\n👋 Thanks for using TMUX Ultimate!")
                print("   Happy tmux-ing! 🚀")
                break
                
            else:
                print("❌ Invalid choice. Please enter a number between 1-8.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
        
        # Pause before showing menu again
        if choice in ['1', '2', '3', '4', '5', '6', '7']:
            input("\n📎 Press Enter to continue...")


if __name__ == "__main__":
    main()