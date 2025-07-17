"""Utility functions for terminal operations"""

import os
import sys
import time
from enum import Enum

class Colors(Enum):
    """ANSI color codes"""
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
def print_colored(text, color=Colors.WHITE, end='\n'):
    """Print colored text to terminal"""
    if isinstance(color, Colors):
        color = color.value
    print(f"{color}{text}{Colors.RESET.value}", end=end)
    
def typewriter_effect(text, delay=0.03):
    """Print text with typewriter effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
    
def center_text(text, width=80):
    """Center text in terminal"""
    return text.center(width)
    
def create_box(content, width=60):
    """Create a box around content"""
    lines = content.split('\n')
    box = ['┌' + '─' * (width - 2) + '┐']
    
    for line in lines:
        if len(line) > width - 4:
            line = line[:width - 7] + '...'
        box.append('│ ' + line.ljust(width - 4) + ' │')
        
    box.append('└' + '─' * (width - 2) + '┘')
    return '\n'.join(box)
