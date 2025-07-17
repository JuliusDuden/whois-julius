"""Matrix Rain Effect"""

import random
import time
import os
import sys
import threading

class MatrixRain:
    def __init__(self):
        self.chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()"
        self.green = '\033[32m'
        self.bright_green = '\033[92m'
        self.reset = '\033[0m'
        self.running = False
        self.is_windows = sys.platform == 'win32'
        # Detect terminal size on initialization
        self.detect_terminal_size()
        
    def detect_terminal_size(self):
        """Get the current terminal dimensions"""
        try:
            # Try to get terminal size using os.get_terminal_size
            self.cols, self.rows = os.get_terminal_size()
        except (AttributeError, OSError):
            # Fallback for environments where get_terminal_size isn't available
            try:
                import subprocess
                self.rows, self.cols = map(int, subprocess.check_output(['stty', 'size']).split())
            except (ImportError, subprocess.SubprocessError, FileNotFoundError):
                # Default fallback values
                self.cols, self.rows = 80, 24
                
        # Print detected size for user information
        print(f"Terminal size detected: {self.cols}x{self.rows}")
        
    def run(self):
        """Run the matrix effect"""
        print("\033[2J\033[H")  # Clear screen
        print(f"{self.bright_green}ENTERING THE MATRIX...{self.reset}")
        print("Press Q to exit\n")
        time.sleep(1)
        
        # Re-detect terminal size to account for any changes
        self.detect_terminal_size()
        
        # Use the appropriate version based on platform
        if self.is_windows:
            self.run_windows_ansi()
        else:
            # Try curses first, fall back to ANSI
            try:
                import curses
                curses.wrapper(self.run_curses)
            except (ImportError, Exception):
                self.run_ansi()
    
    def run_windows_ansi(self):
        """Run matrix rain with ANSI escape codes on Windows"""
        try:
            # Get terminal size - use the already detected size
            cols, rows = self.cols, self.rows
                
            # Create drops
            drops = [-1] * cols
            
            # Input handling thread
            def check_input():
                import msvcrt
                while self.running:
                    if msvcrt.kbhit():
                        key = msvcrt.getch()
                        try:
                            key_char = key.decode('utf-8').lower()
                            if key_char == 'q':
                                self.running = False
                        except UnicodeDecodeError:
                            # Handle special keys that can't be decoded
                            if key in (b'q', b'Q'):
                                self.running = False
                    time.sleep(0.1)
            
            # Start input thread
            input_thread = threading.Thread(target=check_input)
            input_thread.daemon = True
            
            print("\033[2J\033[H")  # Clear screen
            self.running = True
            input_thread.start()
            
            # Main matrix loop
            while self.running:
                # Build output
                output = "\033[H"  # Move cursor to home position
                
                # Use full terminal height (with some margin)
                for i in range(min(rows - 1, rows)):  # Use all available rows
                    line = ""
                    for j in range(min(cols, cols)):  # Use all available columns
                        if drops[j] > i and drops[j] - i < 10:
                            # Matrix head (bright green)
                            if drops[j] - i < 2:
                                line += f"{self.bright_green}{random.choice(self.chars)}{self.reset}"
                            # Matrix trail (green)
                            else:
                                line += f"{self.green}{random.choice(self.chars)}{self.reset}"
                        else:
                            line += " "
                    output += line + "\n"
                
                # Update drops
                for j in range(min(cols, cols)):
                    # Random chance to reset drop or continue
                    if drops[j] >= rows or random.random() > 0.98:
                        drops[j] = -1 * random.randint(1, 5)  # Random negative start position
                    drops[j] += 1
                
                print(output, end="")
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
            print("\033[2J\033[H")  # Clear screen
            print("\n\nExiting the Matrix...")
            time.sleep(0.5)

    def run_curses(self, stdscr):
        """Run matrix rain with curses"""
        # Setup
        curses.curs_set(0)  # Hide cursor
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_WHITE, -1)
        stdscr.nodelay(True)
        
        # Get dimensions
        max_y, max_x = stdscr.getmaxyx()
        max_x -= 1  # Avoid bottom-right corner which can cause issues
        
        # Create drops
        drops = []
        densities = []
        for i in range(max_x):
            drops.append(-1)
            densities.append(random.uniform(0.95, 0.99))
        
        # Main loop
        self.running = True
        while self.running:
            stdscr.clear()
            
            # Draw characters
            for x in range(max_x):
                if drops[x] > 0:
                    # Draw the trail
                    for y in range(drops[x]):
                        if y == drops[x] - 1:
                            # Head of the stream
                            stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
                            stdscr.addch(y, x, random.choice(self.chars))
                            stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
                        elif 0 <= y < max_y - 1:
                            # Body of the stream
                            intensity = min(255, int(255 * (drops[x] - y) / 25))
                            if intensity > 200:
                                stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
                            else:
                                stdscr.attron(curses.color_pair(1))
                            stdscr.addch(y, x, random.choice(self.chars))
                            stdscr.attroff(curses.color_pair(1))
                
                # Update the drop
                if drops[x] < 0 or drops[x] >= max_y or random.random() > densities[x]:
                    # Reset the drop
                    drops[x] = random.randint(-5, 0)
                    densities[x] = random.uniform(0.95, 0.99)
                else:
                    drops[x] += 1
            
            # Check for exit key
            try:
                key = stdscr.getch()
                if key == ord('q') or key == ord('Q'):
                    break
            except:
                pass
                
            stdscr.refresh()
            time.sleep(0.05)

    def run_ansi(self):
        """Run matrix rain with ANSI escape codes"""
        try:
            # Get terminal size
            try:
                cols, rows = os.get_terminal_size()
            except AttributeError:
                rows, cols = map(int, os.popen('stty size', 'r').read().split())
                
            # Create drops
            drops = [-1] * cols
            
            # Input handling thread
            def check_input():
                if sys.platform == 'win32':
                    import msvcrt
                    while self.running:
                        if msvcrt.kbhit():
                            key = msvcrt.getch()
                            if key in (b'q', b'Q'):
                                self.running = False
                        time.sleep(0.1)
                else:
                    # Unix-like
                    import tty
                    import termios
                    import select
                    fd = sys.stdin.fileno()
                    old_settings = termios.tcgetattr(fd)
                    try:
                        tty.setraw(fd)
                        while self.running:
                            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                                key = sys.stdin.read(1)
                                if key in ('q', 'Q'):
                                    self.running = False
                            time.sleep(0.1)
                    finally:
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            
            # Start input thread
            input_thread = threading.Thread(target=check_input)
            input_thread.daemon = True
            
            print("\033[2J\033[H")  # Clear screen
            self.running = True
            input_thread.start()
            
            while self.running:
                # Build output
                output = "\033[H"  # Move cursor to home position
                
                for i in range(min(rows - 1, 40)):  # Limit to avoid excessive output
                    line = ""
                    for j in range(min(cols, 80)):  # Limit to avoid excessive output
                        if drops[j] > i and drops[j] - i < 10:
                            # Matrix head (bright green)
                            if drops[j] - i < 2:
                                line += f"{self.bright_green}{random.choice(self.chars)}{self.reset}"
                            # Matrix trail (green)
                            else:
                                line += f"{self.green}{random.choice(self.chars)}{self.reset}"
                        else:
                            line += " "
                    output += line + "\n"
                
                # Update drops
                for j in range(cols):
                    # Random chance to reset drop or continue
                    if drops[j] >= rows or random.random() > 0.98:
                        drops[j] = -1 * random.randint(1, 5)  # Random negative start position
                    drops[j] += 1
                
                print(output, end="")
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
            print("\033[2J\033[H")  # Clear screen
            print("\n\nExiting the Matrix...")
            time.sleep(0.5)
