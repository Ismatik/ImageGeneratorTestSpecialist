# Image Generator Test Specialist Bot

Telegram bot prototype for a catalog-based shop assistant. The bot remains dormant until the administrator activates it, manages an allow-list of users, and exposes product categories retrieved from 1C. Future iterations will generate preview images for the chosen categories.

## Project Goals
- Admin-only activation to keep the bot under direct control.
- Admin commands to register or remove approved users by phone number.
- Allow-listed users can browse product categories fetched from 1C via inline buttons.
- Follow-up: generate images after a category is chosen to aid product discovery.

## Current State
- Aiogram v3 skeleton with dispatcher, router, and logging already wired.
- Default command registration helper (`buttons/buttons.py`).
- Pydantic-based configuration that reads the Telegram token from `.env`.
- Logging target defined in `config.py` (create `logs/` before running).

## Project Structure
```
.
├── buttons/         # Router logic and default command configuration
├── config.py        # Environment-driven configuration using Pydantic
├── main.py          # Bot entrypoint and dispatcher setup
├── requirements.txt # Python dependencies
├── .env             # Secrets (BOT_API_KEY)
└── users.xlsx       # Placeholder storage for approved users
```

## Prerequisites
- Python 3.10 or newer (Aiogram v3 requirement).
- Telegram bot token stored in `.env` as `BOT_API_KEY` (generated via @BotFather).
- Access to your 1C instance or mock endpoints for category retrieval.

## Setup
1. Clone the repository and enter the project directory.
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create the logging directory before running the bot:
   ```bash
   mkdir -p logs
   ```
5. Populate `.env` with your Telegram bot token:
   ```env
   BOT_API_KEY=123456:ABCDEF
   ```
6. Launch the bot:
   ```bash
   python main.py
   ```

## Recommended Next Steps
- Implement admin authentication and `/start` gating logic.
- Persist the allow-list (e.g., SQLite, Google Sheets, or 1C).
- Integrate 1C API calls to populate the category buttons dynamically.
- Add image generation once category selection is in place.
- Expand logging, error handling, and test coverage.

## License
This project currently has no explicit license. Add one if you intend to distribute or open-source the bot.
