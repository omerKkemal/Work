#!/bin/bash

# =========================================================================== #
# Author: Omer Kemal                                                          #
# Website: https://www.johndoe.com                                            #
# Social Media:                                                               #
#   - Facebook: https://www.facebook.com/johndoe                              #
#   - Telegram: https://t.me/johndoe                                          #
#   - Twitter: @JohnDoe                                                       #
#   - GitHub: https://github.com/johndoe                                      #
# =========================================================================== #

# Detect operating system
OS="$(uname)"
if [[ "$OS" == "Linux" ]]; then
    ENV_ACTIVATE="source venv/bin/activate"
elif [[ "$OS" == "Darwin" ]]; then
    ENV_ACTIVATE="source venv/bin/activate"  # macOS is similar to Linux
elif [[ "$OS" =~ MINGW|CYGWIN|MSYS ]]; then
    ENV_ACTIVATE=".venv\\Scripts\\activate"   # Windows
else
    echo "Unsupported OS: $OS"
    exit 1
fi

# Activate virtual environment
$ENV_ACTIVATE

# Run initialization script
python init.py

# Run the Flask application
python app.py