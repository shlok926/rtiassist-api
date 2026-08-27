import os

# Ensure testing environment variables are set before any application code (like main.py) is imported
os.environ["ENVIRONMENT"] = "development"
os.environ["CORS_ORIGINS"] = "*"
