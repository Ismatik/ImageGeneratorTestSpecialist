from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    BOT_API_KEY: SecretStr
    ADMIN_PHONE_NUMBERS : SecretStr

config = Config()

LOG_FILE = "/home/ikki/Desktop/Koinot/ImageGeneratorTestSpecialist/logs/bot.log"
