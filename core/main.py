#!/usr/bin/env python3
"""
whois-julius - Terminal-Based Developer Portfolio
Main entry point for WHOIS JULIUS
"""

import sys
import os
import io
from commands import CommandDispatcher
from utils import clear_screen, print_colored, Colors

# Set UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class WhoisJulius:
    def __init__(self):
        self.dispatcher = CommandDispatcher()
        self.running = True
        
    def display_prompt(self):
        """Display the command prompt"""
        print_colored("julius@whois-julius", Colors.GREEN, end="")
        print_colored(":", Colors.WHITE, end="")
        print_colored("~", Colors.BLUE, end="")
        print_colored("$ ", Colors.WHITE, end="")
        
    def run(self):
        """Main application loop"""
        clear_screen()
        print_colored("Type 'help' for available commands\n", Colors.CYAN)
        
        while self.running:
            try:
                self.display_prompt()
                command = input().strip().lower()
                
                if command == "exit":
                    print_colored("\nGoodbye! Thanks for visiting.\n", Colors.GREEN)
                    self.running = False
                elif command == "clear":
                    clear_screen()
                else:
                    self.dispatcher.execute(command)
                    
            except KeyboardInterrupt:
                print_colored("\n\nUse 'exit' to quit properly.\n", Colors.YELLOW)
            except Exception as e:
                print_colored(f"\nError: {str(e)}\n", Colors.RED)

if __name__ == "__main__":
    app = WhoisJulius()
    app.run()
