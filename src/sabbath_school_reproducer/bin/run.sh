#!/bin/bash
# Runner script for Sabbath School Lesson Downloader

# Check if config file is provided
if [ $# -eq 0 ]; then
    echo "Usage: ./run.sh config.yaml [options]"
    echo "Options:"
    echo "  --debug             Enable verbose debugging output"
    echo "  --debug-html-only   Only generate debug HTML without PDF generation"
    echo "No config file provided. Looking for default config.yaml..."
    
    if [ -f "config.yaml" ]; then
        CONFIG_FILE="config.yaml"
    else
        echo "No config.yaml found. Generating template config..."
        python3 bin/generate_config.py
        
        if [ -f "config.yaml" ]; then
            CONFIG_FILE="config.yaml"
            echo "Please edit config.yaml with your desired settings, then run this script again."
            exit 0
        else
            echo "Error generating config file. Please create a config file manually."
            exit 1
        fi
    fi
else
    CONFIG_FILE="$1"
fi

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Config file $CONFIG_FILE not found."
    exit 1
fi

# Check for additional flags
DEBUG_FLAG=""
DEBUG_HTML_ONLY=""

for arg in "$@"; do
    case "$arg" in
        --debug)
            DEBUG_FLAG="--debug"
            ;;
        --debug-html-only)
            DEBUG_HTML_ONLY="--debug-html-only"
            ;;
    esac
done

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )"

echo "Running Sabbath School Lesson Downloader with config: $CONFIG_FILE"
python3 "$PROJECT_ROOT/main.py" "$CONFIG_FILE" $DEBUG_FLAG $DEBUG_HTML_ONLY

# Check exit status
if [ $? -eq 0 ]; then
    echo "Process completed successfully!"
else
    echo "Process failed. Check the error messages above."
fi