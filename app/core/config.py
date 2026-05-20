from pydantic_settings import BaseSettings

from typing import Optional

class Settings(BaseSettings):
    debug: Optional[bool] = False
    db_name: str
    db_user: str
    db_password: str

    redis_url: str

    admin_password: str

    model_config = {
        'env_file': '.env',
        'extra': 'ignore',
    }

settings = Settings() #type: ignore