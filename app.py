"""
RTIAssist API — Hugging Face Spaces Entry Point
Bot runs in webhook mode — integrated into FastAPI, no polling subprocess.
"""

import os
from main import app  # noqa: F401

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
