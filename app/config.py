from pydantic.env_settings import BaseSettings

class Settings(BaseSettings):
    PROMPT_FILE_PATH: str = "app/prompt/prompt.json"  # 기본값 설정
    # Azure OpenAI 설정
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_DEPLOYMENT_NAME: str
    
    # 앱 설정
    APP_NAME: str = "Befly AI NARE"
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()