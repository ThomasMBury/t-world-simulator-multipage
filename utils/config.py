# utils/config.py
import os

# Determine if running locally or on the server
ENV = os.getenv("APP_ENV", "local")  # Default to "local" if not set

# Global flags based on environment
IS_LOCAL = ENV == "local"
IS_PRODUCTION = ENV == "production"

# Enforce parameter limits if not running locally
PARAM_LIMITS = not IS_LOCAL
