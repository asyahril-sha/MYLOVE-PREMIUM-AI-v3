#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - SIMPLE RUNNER
=============================================================================
Cukup jalankan: python run_bot_simple.py
Tanpa konfirmasi, langsung start bot
=============================================================================
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def quick_check():
    """Quick check before starting"""
    logger.info("🔍 Quick check...")
    
    # Cek .env
    if not Path(".env").exists():
        logger.error("❌ .env file not found. Please copy from .env.example")
        return False
    
    # Cek API key
    try:
        from config import settings
        if not settings.deepseek_api_key or settings.deepseek_api_key == "your_deepseek_api_key_here":
            logger.error("❌ DeepSeek API key not configured")
            return False
        if not settings.telegram_token or settings.telegram_token == "your_telegram_bot_token_here":
            logger.error("❌ Telegram token not configured")
            return False
    except Exception as e:
        logger.error(f"❌ Config error: {e}")
        return False
    
    # Buat direktori
    for d in ['data', 'data/logs', 'data/backups', 'data/sessions', 'data/vector_db', 'data/memory']:
        Path(d).mkdir(parents=True, exist_ok=True)
    
    logger.info("✅ Quick check passed")
    return True


def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║     💕 MYLOVE PREMIUM AI V3 - VIRTUAL HUMAN                     ║
║                                                                  ║
║     Starting bot...                                             ║
║     Press Ctrl+C to stop                                        ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    if not quick_check():
        return
    
    try:
        from main import main
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n👋 Bot stopped")
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
