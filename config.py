from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    BOT_API_KEY: SecretStr
    ADMIN_ID : SecretStr

config = Config()

LOG_FILE = "/home/ikki/Desktop/Koinot/ImageGeneratorTestSpecialist/logs/bot.log"
USERS_PATH = Path("/home/ikki/Desktop/Koinot/ImageGeneratorTestSpecialist/users.xlsx")