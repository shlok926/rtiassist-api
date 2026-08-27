import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey" if ENVIRONMENT == "development" else None)
if ENVIRONMENT == "production" and not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY must be set in production")

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
AUTHORITY_VERIFICATION_MAX_AGE_DAYS = int(os.getenv("AUTHORITY_VERIFICATION_MAX_AGE_DAYS", "180"))
