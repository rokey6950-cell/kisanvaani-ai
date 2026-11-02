"""
Vercel Serverless Function entry point for KisanVaani AI FastAPI backend.
Maps incoming /api requests directly to the FastAPI ASGI application.
"""

import sys
from pathlib import Path

# Add project root directory to sys.path so 'backend' and 'knowledge' are discoverable
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.main import app
from backend.app.database.connection import init_db
from backend.app.services.knowledge_retrieval import knowledge_service

# Ensure database tables and knowledge base are preloaded for serverless invocation
try:
    init_db()
    if not knowledge_service.loaded:
        knowledge_service.load_knowledge_base()
except Exception as e:
    import logging
    logging.getLogger("kisanvaani.serverless").warning(f"Serverless initialization note: {e}")

