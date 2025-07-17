"""ASCII art for WHOIS JULIUS"""

from utils import print_colored, Colors
import random

def show_ascii_art():
    """Display random ASCII art"""
    arts = [
        {
            "name": "Code",
            "art": """
    < / >
   /     \\
  / () () \\
  \\   -   /
   |  o  |
   \\___/
            """,
            "color": Colors.GREEN
        },
        {
            "name": "Terminal",
            "art": """
 ╔════════════════════╗
 ║ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ║
 ║ ░░░░░░░░░░░░░░░░░░ ║
 ║ julius@whois-julius║
 ║ $ _                ║
 ╚════════════════════╝
            """,
            "color": Colors.CYAN
        },
        {
            "name": "Binary",
            "art": """
 01001010 01010101 01001100
 01001001 01010101 01010011
 
 01000100 01010101 01000100
 01000101 01001110
            """,
            "color": Colors.BLUE
        }
    ]
    
    selected = random.choice(arts)
    print_colored(f"\n=== {selected['name']} ===", Colors.YELLOW)
    print_colored(selected['art'], selected['color'])
