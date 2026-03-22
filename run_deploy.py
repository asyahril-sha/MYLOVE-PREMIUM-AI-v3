#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - DEPLOYMENT RUNNER
=============================================================================
Script untuk deployment di Railway (non-interaktif)
Tidak ada input, langsung menjalankan semua langkah
=============================================================================
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Tambahkan path ke root project
sys.path.insert(0, str(Path(__file__).parent))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def check_environment():
    """Cek environment tanpa input interaktif"""
    logger.info("=" * 60)
    logger.info("🔍 CHECKING ENVIRONMENT (DEPLOYMENT MODE)")
    logger.info("=" * 60)
    
    errors = []
    
    # Cek .env file
    env_path = Path(".env")
    if not env_path.exists():
        logger.error("❌ .env file not found! Please set environment variables in Railway.")
        logger.info("   Required variables:")
        logger.info("   - TELEGRAM_TOKEN")
        logger.info("   - DEEPSEEK_API_KEY")
        logger.info("   - ADMIN_ID")
        return False
    
    # Cek API Key
    try:
        from config import settings
        
        if not settings.deepseek_api_key or settings.deepseek_api_key == "your_deepseek_api_key_here":
            errors.append("DeepSeek API key not configured")
        else:
            logger.info(f"✅ DeepSeek API Key: {settings.deepseek_api_key[:10]}...")
        
        if not settings.telegram_token or settings.telegram_token == "your_telegram_bot_token_here":
            errors.append("Telegram token not configured")
        else:
            logger.info(f"✅ Telegram Token: {settings.telegram_token[:10]}...")
        
        if settings.admin_id == 0:
            logger.warning("⚠️ Admin ID not configured")
        else:
            logger.info(f"✅ Admin ID: {settings.admin_id}")
            
    except Exception as e:
        errors.append(f"Failed to load config: {e}")
    
    # Buat direktori yang diperlukan
    required_dirs = [
        'data', 'data/logs', 'data/backups', 
        'data/sessions', 'data/vector_db', 'data/memory'
    ]
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"✅ Directory: {dir_name}")
    
    if errors:
        logger.error("\n❌ ERRORS FOUND:")
        for err in errors:
            logger.error(f"   - {err}")
        return False
    
    logger.info("\n✅ Environment is ready!")
    return True


def run_migration():
    """Jalankan migrasi database"""
    logger.info("\n" + "=" * 60)
    logger.info("🗄️ RUNNING DATABASE MIGRATION")
    logger.info("=" * 60)
    
    try:
        from database.migrate import migrate
        migrate()
        logger.info("✅ Migration completed")
        return True
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        return False


def start_bot():
    """Start the bot"""
    logger.info("\n" + "=" * 60)
    logger.info("🚀 STARTING MYLOVE PREMIUM AI V3")
    logger.info("=" * 60)
    
    try:
        from main import main
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n👋 Bot stopped")
    except Exception as e:
        logger.error(f"❌ Bot crashed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def main():
    """Main runner untuk deployment"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     💕 MYLOVE PREMIUM AI V3 - DEPLOYMENT MODE                   ║
║     Running on Railway (Non-Interactive)                        ║
║                                                                  ║
║     🔧 Automatic Setup:                                         ║
║     • Checking environment variables                           ║
║     • Creating directories                                      ║
║     • Running database migration                                ║
║     • Starting bot                                              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Check environment
    if not check_environment():
        logger.error("Environment check failed. Please set environment variables.")
        sys.exit(1)
    
    # Step 2: Run migration
    if not run_migration():
        logger.warning("Migration failed, but continuing...")
    
    # Step 3: Start bot
    logger.info("\n" + "=" * 60)
    logger.info("🚀 STARTING BOT...")
    logger.info("Press Ctrl+C to stop")
    logger.info("=" * 60)
    
    start_bot()


if __name__ == "__main__":
    main()
