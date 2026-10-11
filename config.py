import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent

# Load username and password
load_dotenv(PROJECT_ROOT / ".env")

# Select environment
TEST_ENV = os.getenv("TEST_ENV", "DEV").upper()

env_files = {
    "DEV": ".env.dev",
    "QA": ".env.qa",
    "STAGING": ".env.staging"
}

if TEST_ENV not in env_files:
    raise ValueError("Invalid environment")

# Load environment-specific URL
load_dotenv(
    PROJECT_ROOT / env_files[TEST_ENV],
    override=True
)

ENV_NAME = os.getenv("ENV_NAME", TEST_ENV)
BASE_URL = os.getenv("BASE_URL")
TEST_USERNAME = os.getenv("TEST_USERNAME")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")