
# Image Generator Test Specialist Bot

Telegram bot for catalog-based shop assistant. Admins can register users by username, and both admins and users can browse product categories and nomenclature from a JSON catalog. The bot can generate and send images from catalog data using PIL (Pillow).

## Features
- Admin-only activation and user registration by username (not phone).
- Admin commands to add/remove users (stored in `users.xlsx`).
- Inline button navigation for categories and nomenclature, loaded from `JS.Json`.
- Sends images generated from the `ФайлКартинки` field using Pillow.
- Aiogram v3, Pydantic config, and logging to file.

## Project Structure
```
.
├── buttons/         # Routers and UI logic (admin, user, categories)
├── config.py        # Pydantic config, .env loading
├── main.py          # Bot entrypoint and dispatcher setup
├── requirements.txt # Python dependencies
├── .env             # Secrets (BOT_API_KEY, ADMIN_ID)
├── users.xlsx       # Registered users (by username)
├── JS.Json          # Product catalog (categories, nomenclature, images)
```

## Prerequisites
- Python 3.10 or newer
- Telegram bot token in `.env` as `BOT_API_KEY`
- Admin user ID in `.env` as `ADMIN_ID`

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
5. Populate `.env` with your Telegram bot token and admin ID:
   ```env
   BOT_API_KEY=123456:ABCDEF
   ADMIN_ID=123456789
   ```
6. Launch the bot:
   ```bash
   python main.py
   ```

## Notes
- All category and nomenclature navigation is via inline buttons.
- Images are generated from the `ФайлКартинки` field in the JSON catalog using Pillow.
- User registration is by Telegram username (with @).
- Logging is written to `logs/bot.log`.
- Expand logging, error handling, and test coverage.

## License
This project currently has no explicit license. Add one if you intend to distribute or open-source the bot.
