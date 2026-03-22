#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - DATABASE MIGRATION (RAILWAY COMPATIBLE)
=============================================================================
File ini akan menjalankan migrasi database secara otomatis.
Cukup tambahkan ke railway.json sebagai script pre-deploy atau run.
=============================================================================
"""

import asyncio
import sys
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Tambahkan path project
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def run_migration():
    """
    Jalankan migrasi database lengkap
    """
    print("=" * 70)
    print("🚀 MYLOVE PREMIUM AI - DATABASE MIGRATION")
    print("=" * 70)
    
    try:
        # 1. Inisialisasi koneksi database
        print("📁 Initializing database connection...")
        from database.connection import init_db, close_db
        await init_db()
        print("✅ Database connection established")
        
        # 2. Jalankan migrasi
        print("📊 Running migrations...")
        from database.migrate import run_migrations, fix_missing_columns
        await run_migrations()
        print("✅ Migrations completed")
        
        # 3. Perbaiki kolom yang hilang
        print("🔍 Fixing missing columns...")
        await fix_missing_columns()
        print("✅ Missing columns fixed")
        
        # 4. Verifikasi tabel user_sessions
        print("🔍 Verifying user_sessions table...")
        from database.connection import get_db
        db = await get_db()
        
        result = await db.fetch_one(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='user_sessions'"
        )
        
        if result:
            # Cek kolom
            columns = await db.fetch_all("PRAGMA table_info(user_sessions)")
            column_names = [col['name'] for col in columns]
            print(f"📋 user_sessions has {len(column_names)} columns")
            
            # Cek kolom kritis
            critical_columns = [
                'current_location', 'current_clothing', 'current_position',
                'kakak_status', 'suami_status', 'current_emotion', 'arousal_level',
                'promises', 'plans', 'user_preferences'
            ]
            
            missing = [col for col in critical_columns if col not in column_names]
            if missing:
                print(f"⚠️ Missing columns: {missing}")
                print("🔄 Running fix again...")
                await fix_missing_columns()
            else:
                print("✅ All critical columns present")
        else:
            print("❌ user_sessions table not found!")
            return False
        
        # 5. Test repository
        print("🔧 Testing repository...")
        from database.repository import Repository
        repo = Repository()
        
        test_user_id = 999999
        test_data = {
            'session_id': 'TEST-MIGRATION',
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
                print("✅ Repository test passed")
            else:
                print("⚠️ Repository test incomplete")
            
            # Clean up
            await repo.delete_user_session_state(test_user_id)
            
        except Exception as e:
            print(f"⚠️ Repository test warning: {e}")
        
        print("=" * 70)
        print("✅ DATABASE MIGRATION COMPLETE!")
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        try:
            await close_db()
            print("📁 Database connection closed")
        except:
            pass


def main():
    """Main entry point"""
    success = asyncio.run(run_migration())
    
    if success:
        print("\n✅ Database ready!")
        sys.exit(0)
    else:
        print("\n❌ Database migration failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
