import os
from dotenv import load_dotenv
load_dotenv()

def _parse_origins(val: str):
    # allow comma or space separated list in .env
    return [o.strip() for o in val.replace(" ", "").split(",") if o.strip()]
def load_settings():
    return {
        "DB_URL": os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://microlearn:admin@localhost:5432/microlearn"
        ),
        "JWT_SECRET": os.getenv("JWT_SECRET", "superlongrandomstringchangeme123456789"),
        "JWT_TTL_HOURS": int(os.getenv("JWT_TTL_HOURS", "8")),
        "COOKIE_NAME": os.getenv("COOKIE_NAME", "session"),
        "COOKIE_SECURE": os.getenv("COOKIE_SECURE", "false").lower() == "true",
        "COOKIE_SAMESITE": os.getenv("COOKIE_SAMESITE", "Lax"),  # Lax | None | Strict
        "COOKIE_DOMAIN": os.getenv("COOKIE_DOMAIN"),  # usually None locally
        "CORS_ORIGINS":_parse_origins(os.getenv("CORS_ORIGINS", "http://localhost:3000"))
    }
