#!/bin/bash

# whois-julius launcher script
# Author: Julius Duden

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# ASCII Banner
echo -e "${BLUE}"
cat << "EOF"
██╗    ██╗██╗  ██╗ ██████╗ ██╗███████╗         ██╗██╗   ██╗██╗     ██╗██╗   ██╗███████╗
██║    ██║██║  ██║██╔═══██╗██║██╔════╝         ██║██║   ██║██║     ██║██║   ██║██╔════╝
██║ █╗ ██║███████║██║   ██║██║███████╗         ██║██║   ██║██║     ██║██║   ██║███████╗
██║███╗██║██╔══██║██║   ██║██║╚════██║    ██   ██║██║   ██║██║     ██║██║   ██║╚════██║
╚███╔███╔╝██║  ██║╚██████╔╝██║███████║    ╚█████╔╝╚██████╔╝███████╗██║╚██████╔╝███████║
 ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚══════╝     ╚════╝  ╚═════╝ ╚══════╝╚═╝ ╚═════╝ ╚══════╝
EOF
echo -e "${NC}"
echo -e "${GREEN}Welcome to WHOIS JULIUS v1.0${NC}"
echo ""

# Detect environment
IS_MINGW=false
if [[ "$(uname -s)" == MINGW* ]]; then
    IS_MINGW=true
    echo -e "${YELLOW}Detected MINGW environment (Git Bash)${NC}"
fi

# Set Python command based on environment
PYTHON_CMD="python3"
if $IS_MINGW; then
    # On MINGW/Git Bash, python3 might not be available, try python first
    if command -v python &> /dev/null; then
        PYTHON_CMD="python"
    fi
fi

# Check if Python is installed
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo -e "${RED}Error: Python is not installed or not found in PATH.${NC}"
    echo -e "Please install Python 3.11 or higher from https://www.python.org/downloads/"
    echo -e "If Python is already installed, ensure it's available in your PATH."
    exit 1
fi

echo -e "Using Python command: ${YELLOW}$PYTHON_CMD${NC}"

# Check Python version
PY_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "Python version: ${YELLOW}$PY_VERSION${NC}"

# Check if Python version is sufficient (without bc)
PY_MAJOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.major)")
PY_MINOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.minor)")

if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 6 ]); then
    echo -e "${RED}Error: Python 3.6 or higher required. Found: $PY_VERSION${NC}"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create virtual environment.${NC}"
        exit 1
    fi
fi

# Activate virtual environment
echo -e "Activating virtual environment..."
if $IS_MINGW; then
    # MINGW/Git Bash needs different activation path
    source venv/Scripts/activate
else
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
fi

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to activate virtual environment.${NC}"
    echo -e "Try running: ${YELLOW}source venv/Scripts/activate${NC}"
    exit 1
fi

# Verify activation worked
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}Warning: Virtual environment might not be properly activated${NC}"
fi

# Install requirements if needed
if [ ! -f ".installed" ]; then
    echo -e "Installing dependencies..."
    pip install -r requirements.txt > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to install dependencies.${NC}"
        exit 1
    fi
    touch .installed
fi

# Set environment variables for games like Snake
export PYTHONPATH="$PWD:$PYTHONPATH"
export TERM=xterm-256color  # Ensure terminal supports required features

# Get terminal size for display
if command -v tput &> /dev/null; then
    TERM_COLS=$(tput cols)
    TERM_ROWS=$(tput lines)
    echo -e "Terminal size: ${YELLOW}${TERM_COLS}x${TERM_ROWS}${NC}"
    
    if [ "$TERM_COLS" -lt 80 ] || [ "$TERM_ROWS" -lt 24 ]; then
        echo -e "${YELLOW}Warning: Terminal size is smaller than recommended (80x24).${NC}"
        echo -e "Games may not display optimally. Consider resizing your terminal."
    fi
fi

# Set UTF-8 locale if not already set
export LC_ALL=C.UTF-8 2>/dev/null || export LC_ALL=en_US.UTF-8 2>/dev/null || true
export LANG=C.UTF-8 2>/dev/null || export LANG=en_US.UTF-8 2>/dev/null || true

# Windows compatibility settings
if [[ "$(uname -s)" == MINGW* ]] || [[ "$(uname -s)" == CYGWIN* ]]; then
    # For Windows Git Bash or Cygwin
    export PYTHONIOENCODING=utf-8
    export PYTHONLEGACYWINDOWSSTDIO=1  # Fix for Windows console I/O
    # Enable UTF-8 in Windows console
    chcp.com 65001 > /dev/null 2>&1 || true
fi

# Clear setup messages and run the main application
echo -e "Starting application...\n"
sleep 1
clear  # Clear the setup messages before starting the app
$PYTHON_CMD core/main.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Application exited with an error.${NC}"
    exit 1
fi

# Deactivate virtual environment
deactivate 2>/dev/null
echo -e "\n${GREEN}Thanks for using WHOIS JULIUS!${NC}"
