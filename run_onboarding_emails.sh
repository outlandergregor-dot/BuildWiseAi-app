#!/bin/bash
#
# BuildWiseAI Onboarding Email Runner
# 
# This wrapper script simplifies running the onboarding email sender
# and provides additional error handling and notification capabilities.
#

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="${SCRIPT_DIR}/send_onboarding_emails.py"
LOG_FILE="${SCRIPT_DIR}/onboarding_emails.log"
LOCK_FILE="${SCRIPT_DIR}/.onboarding_emails.lock"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if script is already running
check_lock() {
    if [ -f "$LOCK_FILE" ]; then
        PID=$(cat "$LOCK_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            log_warn "Script is already running (PID: $PID). Exiting."
            exit 0
        else
            log_warn "Removing stale lock file"
            rm -f "$LOCK_FILE"
        fi
    fi
}

# Function to create lock file
create_lock() {
    echo $$ > "$LOCK_FILE"
}

# Function to remove lock file
remove_lock() {
    rm -f "$LOCK_FILE"
}

# Trap to ensure lock file is removed on exit
trap remove_lock EXIT INT TERM

# Main execution
main() {
    log_info "Starting BuildWiseAI Onboarding Email Sender"
    log_info "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # Check for lock file
    check_lock
    
    # Create lock file
    create_lock
    
    # Check if Python script exists
    if [ ! -f "$PYTHON_SCRIPT" ]; then
        log_error "Python script not found: $PYTHON_SCRIPT"
        exit 1
    fi
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed"
        exit 1
    fi
    
    # Check if requests library is installed
    if ! python3 -c "import requests" 2>/dev/null; then
        log_warn "requests library not found. Installing..."
        sudo pip3 install requests
    fi
    
    # Run the Python script
    log_info "Executing onboarding email sender..."
    
    if python3 "$PYTHON_SCRIPT" "$@"; then
        log_info "Onboarding email sender completed successfully"
        exit 0
    else
        EXIT_CODE=$?
        log_error "Onboarding email sender failed with exit code: $EXIT_CODE"
        
        # Check if log file exists and show last few lines
        if [ -f "$LOG_FILE" ]; then
            log_info "Last 10 lines of log file:"
            tail -n 10 "$LOG_FILE"
        fi
        
        exit $EXIT_CODE
    fi
}

# Run main function
main "$@"
