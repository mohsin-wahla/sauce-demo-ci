"""Load test configuration from environment variables."""

import os

from dotenv import load_dotenv

# override=True so .env USERNAME/PASSWORD win over the OS USERNAME on Windows.
load_dotenv(override=True)

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")
USERNAME = os.getenv("USERNAME", "standard_user")
PASSWORD = os.getenv("PASSWORD", "secret_sauc")

# Stable catalog item used by cart and checkout tests.
DEFAULT_PRODUCT = "Sauce Labs Backpack"
