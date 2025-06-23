# Tech Product Tracker

A Python-based web scraping application that monitors and tracks prices of tech products across various online stores. Get notified about price changes and track your favorite tech products effortlessly.

## Features

- Web scraping of tech product prices from multiple sources
- Price history tracking and storage
- Telegram bot integration for notifications
- Scheduled price checks
- Customizable alert system
- Browser automation for dynamic content scraping

## Project Structure

```
tech-product-tracker/
├── src/
│   ├── alerts/        # Notification system
│   ├── config.py      # Configuration settings
│   ├── fetchers/      # Web scraping implementations
│   ├── parsers/       # HTML parsing utilities
│   ├── scheduler/     # Scheduling system
│   ├── snapshots/     # Price history snapshots
│   ├── storage/       # Data storage implementations
│   └── utils/         # Helper utilities
├── pyproject.toml     # Project dependencies and metadata
└── README.md         # Project documentation
```

## Requirements

- Python 3.10 or higher
- Dependencies listed in `pyproject.toml`
- Playwright browser binaries (installed automatically during setup)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tech-product-tracker.git
   cd tech-product-tracker
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate     # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install .
   ```

4. Install Playwright and browser binaries:
   ```bash
   pip install playwright
   playwright install  # This will download and install browser binaries
   ```

## Configuration

1. Create a `.env` file in the project root with your configuration:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token
   # Add other configuration variables as needed
   ```

## Usage

[Coming soon]

## Dependencies

- requests: HTTP library for making web requests
- beautifulsoup4: HTML parsing and web scraping
- python-telegram-bot: Telegram bot integration
- pandas: Data manipulation and analysis
- schedule: Job scheduling
- python-dotenv: Environment variable management
- playwright: Browser automation for dynamic content scraping

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is for educational purposes only. Make sure to review and comply with the terms of service of any websites you plan to scrape.
