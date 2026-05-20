from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    admin_password: str
    debug: bool = False
    
    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

settings = Settings() #type: ignore