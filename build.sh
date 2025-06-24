#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright dependencies
playwright install chromium

# Run the main script in automated mode
export AUTOMATED_MODE=true
python src/main.py 