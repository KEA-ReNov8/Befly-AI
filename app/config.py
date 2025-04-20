from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROMPT_FILE_PATH: str = "app/prompt/prompt.json"
    # Azure OpenAI 설정 (선택적)
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_DEPLOYMENT_NAME: Optional[str] = None

    # Google API (필수)
    GOOGLE_API_KEY: str
    
    # 앱 설정
    APP_NAME: str = "Befly_AI_NARE"
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()