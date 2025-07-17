"""Command dispatcher for WHOIS JULIUS"""

import json
import random
import os
from pathlib import Path
from utils import print_colored, Colors, typewriter_effect
from ascii import show_ascii_art

class CommandDispatcher:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.data_path = self.base_path / "data"
        
    def execute(self, command):
        """Execute a given command"""
        commands = {
            "help": self.show_help,
            "cv": self.show_cv,
            "projects": self.show_projects,
            "contact": self.show_contact,
            "quote": self.show_quote,
            "asciiart": self.show_ascii,
            "snake": self.play_snake,
            "matrix": self.show_matrix,
        }
        
        if command in commands:
            commands[command]()
        else:
            print_colored(f"Command not found: {command}", Colors.RED)
            print_colored("Type 'help' for available commands", Colors.YELLOW)
            
    def show_help(self):
        """Display available commands"""
        help_text = """
╔═══════════════════════════════════════════════════════════╗
║                    AVAILABLE COMMANDS                      ║
╠═══════════════════════════════════════════════════════════╣
║  help      - Show this help menu                          ║
║  cv        - Display my curriculum vitae                  ║
║  projects  - Show my portfolio projects                   ║
║  contact   - Get my contact information                   ║
║  quote     - Display a random tech quote                  ║
║  asciiart  - Show ASCII art                               ║
║  snake     - Play Snake game                              ║
║  matrix    - Experience the Matrix                        ║
║  clear     - Clear the terminal                           ║
║  exit      - Exit WHOIS JULIUS                            ║
╚═══════════════════════════════════════════════════════════╝
        """
        print_colored(help_text, Colors.CYAN)
        
    def show_cv(self):
        """Display CV from file"""
        cv_file = self.data_path / "cv.txt"
        if cv_file.exists():
            print_colored("\n=== CURRICULUM VITAE ===\n", Colors.GREEN)
            try:
                with open(cv_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    typewriter_effect(content, 0.01)
            except UnicodeDecodeError:
                # Fallback to latin-1 if UTF-8 fails
                with open(cv_file, 'r', encoding='latin-1') as f:
                    content = f.read()
                    typewriter_effect(content, 0.01)
        else:
            print_colored("CV file not found!", Colors.RED)
            
    def show_projects(self):
        """Display projects from JSON"""
        projects_file = self.data_path / "projects.json"
        if projects_file.exists():
            with open(projects_file, 'r', encoding='utf-8') as f:
                projects = json.load(f)
            
            print_colored("\n=== PORTFOLIO PROJECTS ===\n", Colors.GREEN)
            for i, project in enumerate(projects, 1):
                print_colored(f"[{i}] {project['title']} ({project['year']})", Colors.CYAN)
                print_colored(f"    {project['desc']}\n", Colors.WHITE)
        else:
            print_colored("Projects file not found!", Colors.RED)
            
    def show_contact(self):
        """Display contact information"""
        contact_file = self.data_path / "contact.json"
        if contact_file.exists():
            with open(contact_file, 'r', encoding='utf-8') as f:
                contact = json.load(f)
            
            print_colored("\n=== CONTACT INFORMATION ===\n", Colors.GREEN)
            for key, value in contact.items():
                print_colored(f"{key.capitalize()}: ", Colors.CYAN, end="")
                print_colored(value, Colors.WHITE)
            print()
        else:
            print_colored("Contact file not found!", Colors.RED)
            
    def show_quote(self):
        """Display a random quote"""
        quotes_file = self.data_path / "quotes.txt"
        if quotes_file.exists():
            with open(quotes_file, 'r', encoding='utf-8') as f:
                quotes = [line.strip() for line in f if line.strip()]
            
            if quotes:
                quote = random.choice(quotes)
                print_colored(f"\n💡 {quote}\n", Colors.YELLOW)
        else:
            print_colored("Quotes file not found!", Colors.RED)
            
    def show_ascii(self):
        """Display ASCII art"""
        show_ascii_art()
        
    def play_snake(self):
        """Launch Snake game"""
        try:
            # Use a more robust import mechanism
            import importlib.util
            import sys
            
            # Get absolute path to snake.py
            snake_path = os.path.join(self.base_path, "games", "snake.py")
            
            if not os.path.exists(snake_path):
                print_colored(f"Snake game file not found at: {snake_path}", Colors.RED)
                return
                
            # Import the module dynamically
            spec = importlib.util.spec_from_file_location("snake", snake_path)
            snake_module = importlib.util.module_from_spec(spec)
            sys.modules["snake"] = snake_module
            spec.loader.exec_module(snake_module)
            
            # Run the game
            game = snake_module.SnakeGame()
            game.run()
        except ImportError as e:
            print_colored(f"Import error: {str(e)}", Colors.RED)
        except Exception as e:
            print_colored(f"Error loading Snake game: {str(e)}", Colors.RED)
            import traceback
            print_colored(traceback.format_exc(), Colors.RED)

    def show_matrix(self):
        """Launch Matrix effect"""
        try:
            # Use a more robust import mechanism
            import importlib.util
            import sys
            
            # Get absolute path to matrix.py
            matrix_path = os.path.join(self.base_path, "games", "matrix.py")
            
            if not os.path.exists(matrix_path):
                print_colored(f"Matrix effect file not found at: {matrix_path}", Colors.RED)
                return
                
            # Import the module dynamically
            spec = importlib.util.spec_from_file_location("matrix", matrix_path)
            matrix_module = importlib.util.module_from_spec(spec)
            sys.modules["matrix"] = matrix_module
            spec.loader.exec_module(matrix_module)
            
            # Run the matrix effect
            matrix = matrix_module.MatrixRain()
            matrix.run()
        except ImportError as e:
            print_colored(f"Import error: {str(e)}", Colors.RED)
        except Exception as e:
            print_colored(f"Error loading Matrix effect: {str(e)}", Colors.RED)
            import traceback
            print_colored(traceback.format_exc(), Colors.RED)
