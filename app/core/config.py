from pydantic_settings import BaseSettings

from typing import Optional

class Settings(BaseSettings):
    debug: Optional[bool] = False

    model_config = {
        'env_file': '.env',
        'extra': 'ignore',
    }

settings = Settings()