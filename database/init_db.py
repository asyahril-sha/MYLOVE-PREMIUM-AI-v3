#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - DATABASE INITIALIZATION
=============================================================================
File ini akan menjalankan migrasi database secara otomatis.
Cukup jalankan sekali saat pertama kali deploy, atau panggil dari main.py.
=============================================================================
"""

import asyncio
import logging
import sys
import os

# Tambahkan path project
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import init_db, close_db
from database.migrate import run_migrations, fix_missing_columns
from database.repository import Repository

logger = logging.getLogger(__name__)


async def init_database():
    """
    Inisialisasi database lengkap dengan semua state persistence
    """
    logger.info("=" * 60)
    logger.info("🚀 MYLOVE PREMIUM AI - DATABASE INITIALIZATION")
    logger.info("=" * 60)
    
    try:
        # 1. Inisialisasi koneksi database
        logger.info("📁 Initializing database connection...")
        await init_db()
        
        # 2. Jalankan semua migrasi
        logger.info("📊 Running migrations...")
        await run_migrations()
        
        # 3. Verifikasi dan perbaiki kolom yang hilang (untuk user_sessions)
        logger.info("🔍 Verifying and fixing missing columns...")
        await fix_missing_columns()
        
        # 4. Test repository untuk user_sessions
        logger.info("🔧 Testing repository...")
        repo = Repository()
        
        # Test create/get/delete user session
        test_user_id = 999999
        test_data = {
            'session_id': 'TEST-001',
            'role': 'test',
            'bot_name': 'TestBot',
            'current_location': 'test_location',
            'current_clothing': 'test_clothing',
            'current_position': 'test_position',
            'current_activity': 'testing',
            'intimacy_level': 1,
            'total_chats': 0,
            'kakak_status': 'ada',
            'suami_status': 'ada',
            'current_emotion': 'netral',
            'arousal_level': 0,
            'promises': [],
            'plans': [],
            'user_preferences': {}
        }
        
        try:
            await repo.save_user_session_state(test_user_id, test_data)
            loaded = await repo.load_user_session_state(test_user_id)
            
            if loaded and loaded.get('current_location') == 'test_location':
                logger.info("✅ Repository test passed - user_sessions working")
            else:
                logger.warning("⚠️ Repository test incomplete")
            
            # Clean up test data
            await repo.delete_user_session_state(test_user_id)
            
        except Exception as e:
            logger.warning(f"⚠️ Repository test warning: {e}")
        
        # 5. Verifikasi tabel dan kolom user_sessions
        from database.connection import get_db
        db = await get_db()
        
        result = await db.fetch_one(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='user_sessions'"
        )
        
        if result:
            columns = await db.fetch_all("PRAGMA table_info(user_sessions)")
            column_names = [col['name'] for col in columns]
            logger.info(f"📋 user_sessions columns: {len(column_names)} columns")
            
            # Cek kolom kritis
            critical_columns = ['current_location', 'current_clothing', 'current_position', 
                               'kakak_status', 'suami_status', 'current_emotion', 'arousal_level',
                               'promises', 'plans', 'user_preferences']
            
            missing_critical = [col for col in critical_columns if col not in column_names]
            if missing_critical:
                logger.error(f"❌ Missing critical columns: {missing_critical}")
                logger.info("🔄 Running fix_missing_columns again...")
                await fix_missing_columns()
            else:
                logger.info("✅ All critical columns present")
        else:
            logger.error("❌ user_sessions table not found after migration")
            return False
        
        logger.info("=" * 60)
        logger.info("✅ DATABASE INITIALIZATION COMPLETE!")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        await close_db()


async def main():
    """
    Main function untuk dijalankan langsung
    """
    success = await init_database()
    
    if success:
        print("\n✅ Database initialized successfully!")
        print("   Bot siap dijalankan.\n")
    else:
        print("\n❌ Database initialization failed!")
        print("   Periksa error di atas.\n")
    
    return success


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run
    asyncio.run(main())
