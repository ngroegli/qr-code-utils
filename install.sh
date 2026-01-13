#!/bin/bash

###############################################################################
# QR Code Utils - Installer Script
# Sets up the QR Code Utils environment with virtual environment
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Configuration
QR_UTILS_HOME="$HOME/.qr-utils"
CONFIG_DIR="$QR_UTILS_HOME"
LOGS_DIR="$QR_UTILS_HOME/logs"
OUTPUT_DIR="$QR_UTILS_HOME/output"
VENV_DIR="$SCRIPT_DIR/venv"

print_header() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════╗"
    echo "║       QR Code Utils - Installer v1.0.2        ║"
    echo "╚════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

check_python() {
    print_step "Checking Python installation..."

    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_success "Python $PYTHON_VERSION found"
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
        print_success "Python $PYTHON_VERSION found"
        PYTHON_CMD="python"
    else
        print_error "Python not found. Please install Python 3.7 or higher."
        exit 1
    fi

    # Check Python version
    PYTHON_MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info[0])')
    PYTHON_MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info[1])')

    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
        print_error "Python 3.7 or higher is required. Found: $PYTHON_VERSION"
        exit 1
    fi
}

check_pip() {
    print_step "Checking pip installation..."

    if command -v pip3 &> /dev/null; then
        print_success "pip3 found"
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        print_success "pip found"
        PIP_CMD="pip"
    else
        print_error "pip not found. Please install pip."
        exit 1
    fi
}

create_venv() {
    print_step "Creating virtual environment..."

    if [ -d "$VENV_DIR" ]; then
        print_warning "Virtual environment already exists at $VENV_DIR"
        read -p "Do you want to recreate it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$VENV_DIR"
            $PYTHON_CMD -m venv "$VENV_DIR"
            print_success "Virtual environment recreated"
        else
            print_step "Using existing virtual environment"
        fi
    else
        $PYTHON_CMD -m venv "$VENV_DIR"
        print_success "Virtual environment created at $VENV_DIR"
    fi
}

create_directories() {
    print_step "Creating directories..."

    # Create main directory
    if [ ! -d "$QR_UTILS_HOME" ]; then
        mkdir -p "$QR_UTILS_HOME"
        print_success "Created $QR_UTILS_HOME"
    else
        print_warning "Directory $QR_UTILS_HOME already exists"
    fi

    # Create subdirectories
    for dir in "$LOGS_DIR" "$OUTPUT_DIR"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            print_success "Created $dir"
        else
            print_warning "Directory $dir already exists"
        fi
    done
}

install_dependencies() {
    print_step "Installing Python dependencies in virtual environment..."

    # Activate venv
    source "$VENV_DIR/bin/activate"

    if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
        pip install --upgrade pip
        pip install -r "$SCRIPT_DIR/requirements.txt"
        print_success "Dependencies installed successfully"
    else
        print_error "requirements.txt not found"
        exit 1
    fi

    # Deactivate venv
    deactivate
}

create_default_config() {
    print_step "Creating default configuration..."

    CONFIG_FILE="$CONFIG_DIR/config.yml"

    if [ -f "$CONFIG_FILE" ]; then
        print_warning "Config file already exists at $CONFIG_FILE"
        read -p "Do you want to overwrite it? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_step "Keeping existing configuration"
            return
        fi
    fi

    cat > "$CONFIG_FILE" << 'EOF'
qr_settings:
  version: 1
  error_correction: H
  box_size: 10
  border: 4
  fill_color: black
  back_color: white
output_format: png
default_output_dir: ~/.qr-utils/output
vcard_defaults:
  version: '3.0'
EOF

    print_success "Default configuration created at $CONFIG_FILE"
}

setup_alias() {
    print_step "Setting up qr-utils alias..."

    WRAPPER_SCRIPT="$SCRIPT_DIR/qr-utils.sh"

    # Make wrapper executable
    chmod +x "$WRAPPER_SCRIPT" 2>/dev/null || true

    # Add alias to both .bashrc and .zshrc
    for RC_FILE in "$HOME/.bashrc" "$HOME/.zshrc"; do
        if [ -f "$RC_FILE" ]; then
            # Check if alias is already added
            if ! grep -q "# QR Code Utils alias" "$RC_FILE" 2>/dev/null; then
                echo "" >> "$RC_FILE"
                echo "# QR Code Utils alias" >> "$RC_FILE"
                echo "alias qr-utils='$WRAPPER_SCRIPT'" >> "$RC_FILE"
                print_success "Added alias to $RC_FILE"
            else
                print_warning "Alias already configured in $RC_FILE"
            fi
        fi
    done

    print_warning "Please run 'source ~/.bashrc' or 'source ~/.zshrc' to activate the alias"
    print_success "You can then run 'qr-utils' from anywhere"
}

print_summary() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════╗"
    echo "║     Installation completed successfully!      ║"
    echo "╚════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Installation Summary:${NC}"
    echo "  • Config directory:  $CONFIG_DIR"
    echo "  • Logs directory:    $LOGS_DIR"
    echo "  • Output directory:  $OUTPUT_DIR"
    echo "  • Virtual env:       $VENV_DIR"
    echo "  • Wrapper script:    $SCRIPT_DIR/qr-utils.sh"
    echo ""
    echo -e "${BLUE}Quick Start:${NC}"
    echo "  • Generate URL QR:  qr-utils url --url 'https://example.com'"
    echo "  • Generate WiFi QR: qr-utils wifi --ssid 'MyNet' --password 'pass'"
    echo "  • Show help:        qr-utils --help"
    echo ""
    echo -e "${YELLOW}Note:${NC} Run 'source ~/.bashrc' or 'source ~/.zshrc' first!"
    echo ""
    echo -e "${BLUE}Documentation:${NC}"
    echo "  • User Guide:       docs/USER_GUIDE.md"
    echo "  • API Reference:    docs/API_REFERENCE.md"
    echo "  • Architecture:     docs/drawings/"
    echo ""
}

# Main installation flow
main() {
    print_header

    check_python
    check_pip
    create_venv
    create_directories
    install_dependencies
    create_default_config
    setup_alias
    print_summary

    echo -e "${GREEN}Happy QR coding! 🎉${NC}"
}

# Run main function
main
