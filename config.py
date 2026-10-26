import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load .env file from the project root
load_dotenv(BASE_DIR / ".env")


class Config:
    """Base application configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "shoplytics-academic-dev-key-2026")
    BASE_DIR = BASE_DIR
    
    # Database Settings
    MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "shoplytics_db")
    
    # Fallback to local SQLite if MySQL is unreachable or for isolated testing
    SQLITE_DB_PATH = str(BASE_DIR / "instance" / "shoplytics_fallback.db")
    USE_SQLITE_FALLBACK = os.getenv("USE_SQLITE_FALLBACK", "true").lower() in ("true", "1", "yes")

    # Uploads & Temporary Export storage
    UPLOAD_FOLDER = BASE_DIR / "data" / "uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload

    # ML & Forecasting Configuration
    ML_MODEL_DIR = BASE_DIR / "ml" / "saved_models"
    LSTM_LOOKBACK_DAYS = int(os.getenv("LSTM_LOOKBACK_DAYS", "30"))
    LSTM_EPOCHS = int(os.getenv("LSTM_EPOCHS", "25"))
    LSTM_BATCH_SIZE = int(os.getenv("LSTM_BATCH_SIZE", "16"))
    LSTM_FORECAST_HORIZON = int(os.getenv("LSTM_FORECAST_HORIZON", "14"))

    # Ensure runtime directories exist
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    ML_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "instance").mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    MYSQL_DB = "shoplytics_test_db"
    USE_SQLITE_FALLBACK = True
    SQLITE_DB_PATH = ":memory:"


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
