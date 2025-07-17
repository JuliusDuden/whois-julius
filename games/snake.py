"""Snake Game for Terminal - Complete Rewrite"""

import random
import time
import os
import sys
import json

# Platform-specific imports
if sys.platform == 'win32':
    import msvcrt
else:
    import select
    import tty
    import termios

class SnakeGame:
    def __init__(self):
        self.is_windows = sys.platform == 'win32'
        self.width = 30
        self.height = 15
        self.score = 0
        self.running = False
        self.player_name = ""
        self.scores_file = "data/snake_scores.json"
        
        # Colors
        self.GREEN = '\033[32m'
        self.RED = '\033[31m'
        self.YELLOW = '\033[33m'
        self.BLUE = '\033[34m'
        self.CYAN = '\033[36m'
        self.BOLD = '\033[1m'
        self.RESET = '\033[0m'
        
        # Game symbols
        self.SNAKE_HEAD = 'O'
        self.SNAKE_BODY = 'o'
        self.FOOD = '*'
        self.WALL = '#'
        
        # Load scores
        self.load_scores()
        
    def load_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists(self.scores_file):
                with open(self.scores_file, 'r') as f:
                    self.high_scores = json.load(f)
            else:
                self.high_scores = []
        except:
            self.high_scores = []
            
    def save_scores(self):
        """Save high scores to file"""
        try:
            os.makedirs(os.path.dirname(self.scores_file), exist_ok=True)
            with open(self.scores_file, 'w') as f:
                json.dump(self.high_scores, f, indent=2)
        except:
            pass
            
    def add_score(self, name, score):
        """Add new score to high scores"""
        self.high_scores.append({"name": name, "score": score})
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:10]
        self.save_scores()
        
    def get_high_score(self):
        """Get current high score"""
        return self.high_scores[0]["score"] if self.high_scores else 0
        
    def clear_screen(self):
        """Clear the screen"""
        os.system('cls' if self.is_windows else 'clear')
        
    def hide_cursor(self):
        """Hide the cursor"""
        print("\033[?25l", end='', flush=True)
        
    def show_cursor(self):
        """Show the cursor"""
        print("\033[?25h", end='', flush=True)
        
    def move_cursor_home(self):
        """Move cursor to home position"""
        print("\033[H", end='', flush=True)
        
    def get_key(self):
        """Get a single key press"""
        if self.is_windows:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\xe0':  # Special key
                    key = msvcrt.getch()
                    if key == b'H': return 'UP'
                    elif key == b'P': return 'DOWN'
                    elif key == b'K': return 'LEFT'
                    elif key == b'M': return 'RIGHT'
                else:
                    try:
                        return key.decode('utf-8').lower()
                    except:
                        return ''
        else:
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                key = sys.stdin.read(1)
                if key == '\x1b':  # ESC sequence
                    try:
                        sys.stdin.read(1)  # [
                        arrow = sys.stdin.read(1)
                        if arrow == 'A': return 'UP'
                        elif arrow == 'B': return 'DOWN'
                        elif arrow == 'C': return 'RIGHT'
                        elif arrow == 'D': return 'LEFT'
                    except:
                        pass
                return key.lower()
        return None
        
    def get_input(self):
        """Get input with prompt"""
        if self.is_windows:
            result = ""
            while True:
                key = msvcrt.getch()
                if key == b'\r':  # Enter
                    print()
                    break
                elif key == b'\x08':  # Backspace
                    if result:
                        result = result[:-1]
                        print('\b \b', end='', flush=True)
                elif key == b'\xe0':  # Special key
                    msvcrt.getch()  # Consume second byte
                    continue
                else:
                    try:
                        char = key.decode('utf-8')
                        if char.isprintable():
                            result += char
                            print(char, end='', flush=True)
                    except:
                        continue
            return result
        else:
            return input()
            
    def show_menu(self):
        """Show main menu"""
        while True:
            self.clear_screen()
            print(f"{self.BOLD}{self.GREEN}SNAKE GAME{self.RESET}")
            print("=" * 20)
            print()
            print(f"{self.CYAN}1. Play Game{self.RESET}")
            print(f"{self.CYAN}2. View Scoreboard{self.RESET}")
            print(f"{self.CYAN}3. Quit{self.RESET}")
            print()
            print(f"Choose option (1-3): ", end='', flush=True)
            
            if self.is_windows:
                # Wait for key press
                key = msvcrt.getch()
                if key == b'\xe0':  # Special key
                    msvcrt.getch()  # Consume second byte
                    continue
                try:
                    choice = key.decode('utf-8')
                    print(choice)  # Echo the choice
                except:
                    continue
            else:
                choice = input().strip()
                
            if choice == '1':
                self.start_game()
                # After game ends, continue to show menu
            elif choice == '2':
                self.show_scoreboard()
            elif choice == '3':
                return  # Exit the menu loop
            else:
                print()
                print(f"{self.RED}Invalid choice! Please press 1, 2, or 3.{self.RESET}")
                print("Press any key to continue...")
                if self.is_windows:
                    msvcrt.getch()
                else:
                    input()
                    
    def get_player_name(self):
        """Get player name"""
        self.clear_screen()
        print(f"{self.BOLD}{self.GREEN}SNAKE GAME{self.RESET}")
        print("=" * 20)
        print()
        print("Enter your name (max 12 chars): ", end='', flush=True)
        
        if self.is_windows:
            name = ""
            while True:
                key = msvcrt.getch()
                if key == b'\r':  # Enter
                    print()
                    break
                elif key == b'\x08':  # Backspace
                    if name:
                        name = name[:-1]
                        print('\b \b', end='', flush=True)
                elif key == b'\xe0':  # Special key
                    msvcrt.getch()  # Consume second byte
                    continue
                elif len(name) < 12:
                    try:
                        char = key.decode('utf-8')
                        if char.isalnum() or char == ' ':
                            name += char
                            print(char, end='', flush=True)
                    except:
                        continue
        else:
            name = input()
            
        return name.strip() if name.strip() else "Anonymous"
        
    def show_scoreboard(self):
        """Show high scores"""
        self.clear_screen()
        print(f"{self.BOLD}{self.YELLOW}TOP 10 SCOREBOARD{self.RESET}")
        print("=" * 30)
        print()
        
        if not self.high_scores:
            print(f"{self.CYAN}No scores yet!{self.RESET}")
        else:
            print(f"{'Rank':<5} {'Name':<15} {'Score':<6}")
            print("-" * 30)
            for i, entry in enumerate(self.high_scores, 1):
                color = self.YELLOW if i <= 3 else self.CYAN
                print(f"{color}{i:<5} {entry['name']:<15} {entry['score']:<6}{self.RESET}")
                
        print()
        print("Press any key to continue...")
        
        if self.is_windows:
            msvcrt.getch()
        else:
            input()
            
    def start_game(self):
        """Start the game"""
        self.player_name = self.get_player_name()
        self.score = 0
        self.running = True
        
        # Initialize snake and food
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = 'RIGHT'
        self.next_direction = 'RIGHT'
        self.place_food()
        
        # Clear screen and hide cursor for smooth gameplay
        self.clear_screen()
        self.hide_cursor()
        
        try:
            # Start the game loop
            if not self.is_windows:
                try:
                    fd = sys.stdin.fileno()
                    old_settings = termios.tcgetattr(fd)
                    tty.setraw(fd)
                    self.game_loop()
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                except:
                    self.game_loop()
            else:
                self.game_loop()
        except KeyboardInterrupt:
            self.running = False
        finally:
            # Always show cursor after game ends
            self.show_cursor()
            
    def place_food(self):
        """Place food randomly"""
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
            
    def game_loop(self):
        """Main game loop"""
        last_move = time.time()
        speed = 0.25  # Balanced speed
        
        # Draw initial game state
        self.draw_game()
        
        while self.running:
            # Handle input more frequently
            for _ in range(5):  # Check input multiple times per frame
                key = self.get_key()
                if key == 'q':
                    self.running = False
                    break
                elif key == 'w' or key == 'UP':
                    if self.direction != 'DOWN':
                        self.next_direction = 'UP'
                elif key == 's' or key == 'DOWN':
                    if self.direction != 'UP':
                        self.next_direction = 'DOWN'
                elif key == 'a' or key == 'LEFT':
                    if self.direction != 'RIGHT':
                        self.next_direction = 'LEFT'
                elif key == 'd' or key == 'RIGHT':
                    if self.direction != 'LEFT':
                        self.next_direction = 'RIGHT'
                        
                time.sleep(0.002)  # Small delay between input checks
                
            # Move snake
            current_time = time.time()
            if current_time - last_move >= speed:
                self.direction = self.next_direction
                
                # Calculate new head position
                head_x, head_y = self.snake[0]
                if self.direction == 'UP':
                    new_head = (head_x, head_y - 1)
                elif self.direction == 'DOWN':
                    new_head = (head_x, head_y + 1)
                elif self.direction == 'LEFT':
                    new_head = (head_x - 1, head_y)
                elif self.direction == 'RIGHT':
                    new_head = (head_x + 1, head_y)
                    
                # Check collisions
                if (new_head[0] < 0 or new_head[0] >= self.width or
                    new_head[1] < 0 or new_head[1] >= self.height or
                    new_head in self.snake):
                    self.game_over()
                    break
                    
                # Add new head
                self.snake.insert(0, new_head)
                
                # Check if food eaten
                if new_head == self.food:
                    self.score += 10
                    self.place_food()
                    speed = max(0.1, speed - 0.003)  # Gradually increase speed
                else:
                    self.snake.pop()  # Remove tail
                    
                self.draw_game()
                last_move = current_time
                
            time.sleep(0.01)  # Small delay
            
    def draw_game(self):
        """Draw the game without flickering"""
        # Use cursor positioning instead of clearing screen
        self.move_cursor_home()
        
        # Header
        print(f"{self.BOLD}{self.GREEN}SNAKE GAME - {self.player_name}{self.RESET}")
        print(f"Score: {self.score} | High Score: {self.get_high_score()}")
        print("WASD to move, Q to quit")
        print()
        
        # Create grid
        grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Place snake
        for i, (x, y) in enumerate(self.snake):
            if 0 <= x < self.width and 0 <= y < self.height:
                grid[y][x] = self.SNAKE_HEAD if i == 0 else self.SNAKE_BODY
                
        # Place food
        fx, fy = self.food
        if 0 <= fx < self.width and 0 <= fy < self.height:
            grid[fy][fx] = self.FOOD
            
        # Draw borders and grid
        border = self.BLUE + self.WALL * (self.width + 2) + self.RESET
        print(border)
        
        for row in grid:
            line = self.BLUE + self.WALL + self.RESET
            for cell in row:
                if cell == self.SNAKE_HEAD:
                    line += self.BOLD + self.GREEN + cell + self.RESET
                elif cell == self.SNAKE_BODY:
                    line += self.GREEN + cell + self.RESET
                elif cell == self.FOOD:
                    line += self.BOLD + self.RED + cell + self.RESET
                else:
                    line += cell
            line += self.BLUE + self.WALL + self.RESET
            print(line)
            
        print(border)
        
        # Clear any remaining lines from previous frame
        print("\033[J", end='', flush=True)
        
    def game_over(self):
        """Handle game over"""
        self.running = False
        self.show_cursor()  # Make sure cursor is visible
        
        # Give a moment for the game loop to stop
        time.sleep(0.5)
        
        # Clear screen properly
        self.clear_screen()
        
        # Add score to high scores
        self.add_score(self.player_name, self.score)
        
        print(f"{self.BOLD}{self.RED}GAME OVER!{self.RESET}")
        print()
        print(f"Player: {self.CYAN}{self.player_name}{self.RESET}")
        print(f"Final Score: {self.YELLOW}{self.score}{self.RESET}")
        
        if self.score == self.get_high_score() and self.score > 0:
            print(f"{self.BOLD}{self.YELLOW}NEW HIGH SCORE!{self.RESET}")
            
        print()
        print("Press any key to continue...")
        
        if self.is_windows:
            msvcrt.getch()
        else:
            input()
            
    def run(self):
        """Main entry point"""
        try:
            self.show_menu()
        except KeyboardInterrupt:
            pass
        finally:
            self.clear_screen()
            print("Thanks for playing!")
