#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - DATABASE MIGRATIONS
=============================================================================
Semua migrasi database untuk MYLOVE V3 dengan state persistence
=============================================================================
"""

import time
import logging
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

from database.connection import get_db, execute_query, fetch_one, fetch_all

logger = logging.getLogger(__name__)


# =============================================================================
# TABLE CREATION FUNCTIONS
# =============================================================================

async def create_users_table():
    """Create users table"""
    db = await get_db()
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL UNIQUE,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            created_at REAL NOT NULL,
            last_active REAL NOT NULL,
            total_interactions INTEGER DEFAULT 0,
            preferences TEXT DEFAULT '{}',
            settings TEXT DEFAULT '{}'
        )
    """)
    
    await db.execute("CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id)")
    await db.commit()
    logger.info("✅ users table created")


async def create_sessions_table():
    """Create sessions table"""
    db = await get_db()
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            bot_name TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            start_time REAL NOT NULL,
            end_time REAL,
            last_message_time REAL NOT NULL,
            total_messages INTEGER DEFAULT 0,
            intimacy_level INTEGER DEFAULT 1,
            location TEXT,
            summary TEXT,
            metadata TEXT DEFAULT '{}',
            created_at REAL DEFAULT (strftime('%s', 'now')),
            FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE
        )
    """)
    
    await db.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id)")
    await db.execute("CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status)")
    await db.commit()
    logger.info("✅ sessions table created")


async def create_conversations_table():
    """Create conversations table"""
    db = await get_db()
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            timestamp REAL NOT NULL,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            intent TEXT,
            mood TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
        )
    """)
    
    await db.execute("CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id)")
    await db.execute("CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp)")
    await db.commit()
    logger.info("✅ conversations table created")


async def create_pdkt_tables():
    """Create PDKT related tables"""
    db = await get_db()
    
    # PDKT sessions table
    await db.execute("""
        CREATE TABLE IF NOT EXISTS pdkt_sessions (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            bot_name TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            direction TEXT NOT NULL,
            chemistry_score REAL DEFAULT 50.0,
            chemistry_level TEXT DEFAULT 'biasa',
            mood TEXT DEFAULT 'calm',
            level INTEGER DEFAULT 1,
            total_duration REAL DEFAULT 0,
            total_chats INTEGER DEFAULT 0,
            total_intim INTEGER DEFAULT 0,
            total_climax INTEGER DEFAULT 0,
            created_at REAL NOT NULL,
            last_interaction REAL NOT NULL,
            paused_at REAL,
            ended_at REAL,
            end_reason TEXT,
            inner_thoughts TEXT DEFAULT '[]',
            milestones TEXT DEFAULT '[]',
            metadata TEXT DEFAULT '{}',
            FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE
        )
    """)
    
    # PDKT inner thoughts table
    await db.execute("""
        CREATE TABLE IF NOT EXISTS pdkt_inner_thoughts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pdkt_id TEXT NOT NULL,
            thought TEXT NOT NULL,
            context TEXT,
            timestamp REAL NOT NULL,
            FOREIGN KEY (pdkt_id) REFERENCES pdkt_sessions(id) ON DELETE CASCADE
        )
    """)
    
    await db.execute("CREATE INDEX IF NOT EXISTS idx_pdkt_user_id ON pdkt_sessions(user_id)")
    await db.execute("CREATE INDEX IF NOT EXISTS idx_pdkt_status ON pdkt_sessions(status)")
    await db.commit()
    logger.info("✅ PDKT tables created")


async def create_mantan_tables():
    """Create Mantan related tables"""
    db = await get_db()
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS mantan (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            pdkt_id TEXT NOT NULL,
            bot_name TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT DEFAULT 'putus',
            putus_time REAL NOT NULL,
            putus_reason TEXT NOT NULL,
            chemistry_history TEXT DEFAULT '[]',
            milestones TEXT DEFAULT '[]',
            total_chats INTEGER DEFAULT 0,
            total_intim INTEGER DEFAULT 0,
            total_climax INTEGER DEFAULT 0,
            first_kiss_time REAL,
            first_intim_time REAL,
            become_pacar_time REAL,
            last_chat_time REAL NOT NULL,
            fwb_requests TEXT DEFAULT '[]',
            fwb_start_time REAL,
            fwb_end_time REAL,
            FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE
        )
    """)
    
    await db.execute("CREATE INDEX IF NOT EXISTS idx_mantan_user_id ON mantan(user_id)")
    await db.commit()
    logger.info("✅ Mantan tables created")


async def create_fwb_tables():
    """Create FWB related tables"""
    db = await get_db()
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS fwb_relations (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            mantan_id TEXT NOT NULL,
            bot_name TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            created_at REAL NOT NULL,
            last_interaction REAL NOT NULL,
            chemistry_score REAL DEFAULT 50.0,
            climax_count INTEGER DEFAULT 0,
            intim_count INTEGER DEFAULT 0,
            total_chats INTEGER DEFAULT 0,
            pause_history TEXT DEFAULT '[]',
            ended_at REAL,
            end_reason TEXT,
            FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE,
            FOREIGN KEY (mantan_id) REFERENCES mantan(id) ON DELETE CASCADE
        )
    """)
    
    await db.execute("CREATE INDEX IF NOT EXISTS idx_fwb_user_id ON fwb_relations(user_id)")
    await db.execute("CREATE INDEX IF NOT EXISTS idx_fwb_status ON fwb_relations(status)")
    await db.commit()
    logger.info("✅ FWB tables created")


async def create_hts_tables():
    """Create HTS related tables"""
    db = await get_db()
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS hts_relations (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            bot_name TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            created_at REAL NOT NULL,
            expiry_time REAL NOT NULL,
            last_interaction REAL NOT NULL,
            chemistry_score REAL DEFAULT 50.0,
            climax_count INTEGER DEFAULT 0,
            intimacy_level INTEGER DEFAULT 7,
            total_chats INTEGER DEFAULT 0,
            total_intim INTEGER DEFAULT 0,
            history TEXT DEFAULT '[]',
            FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE
        )
    """)
    
    await db.execute("CREATE INDEX IF NOT EXISTS idx_hts_user_id ON hts_relations(user_id)")
    await db.execute("CREATE INDEX IF NOT EXISTS idx_hts_status ON hts_relations(status)")
    await db.commit()
    logger.info("✅ HTS tables created")


async def create_memories_table():
    """Create memories table"""
    db = await get_db()
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT,
            memory_type TEXT NOT NULL,
            content TEXT NOT NULL,
            importance REAL DEFAULT 0.5,
            emotional_tag TEXT,
            timestamp REAL NOT NULL,
            metadata TEXT DEFAULT '{}',
            FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE
        )
    """)
    
    await db.execute("CREATE INDEX IF NOT EXISTS idx_memories_user_id ON memories(user_id)")
    await db.execute("CREATE INDEX IF NOT EXISTS idx_memories_memory_type ON memories(memory_type)")
    await db.commit()
    logger.info("✅ memories table created")


async def create_preferences_table():
    """Create preferences table"""
    db = await get_db()
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT,
            pref_type TEXT NOT NULL,
            item TEXT NOT NULL,
            score REAL DEFAULT 0.5,
            count INTEGER DEFAULT 1,
            last_updated REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE,
            UNIQUE(user_id, role, pref_type, item)
        )
    """)
    
    await db.execute("CREATE INDEX IF NOT EXISTS idx_preferences_user_id ON preferences(user_id)")
    await db.commit()
    logger.info("✅ preferences table created")


async def create_milestones_table():
    """Create milestones table"""
    db = await get_db()
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT,
            milestone_type TEXT NOT NULL,
            description TEXT,
            timestamp REAL NOT NULL,
            intimacy_level INTEGER,
            metadata TEXT DEFAULT '{}',
            FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE
        )
    """)
    
    await db.execute("CREATE INDEX IF NOT EXISTS idx_milestones_user_id ON milestones(user_id)")
    await db.commit()
    logger.info("✅ milestones table created")


async def create_backups_table():
    """Create backups table"""
    db = await get_db()
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS backups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            size INTEGER,
            created_at REAL NOT NULL,
            type TEXT DEFAULT 'auto',
            status TEXT DEFAULT 'completed',
            metadata TEXT DEFAULT '{}'
        )
    """)
    
    await db.commit()
    logger.info("✅ backups table created")


async def create_threesome_tables():
    """Create threesome related tables"""
    db = await get_db()
    
    # Threesome sessions table
    await db.execute("""
        CREATE TABLE IF NOT EXISTS threesome_sessions (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            created_at REAL NOT NULL,
            started_at REAL,
            completed_at REAL,
            last_activity REAL NOT NULL,
            total_messages INTEGER DEFAULT 0,
            climax_count INTEGER DEFAULT 0,
            aftercare_needed INTEGER DEFAULT 0,
            current_focus INTEGER,
            last_pattern TEXT,
            participants TEXT DEFAULT '[]',
            interactions TEXT DEFAULT '[]',
            FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE
        )
    """)
    
    # Threesome participants table
    await db.execute("""
        CREATE TABLE IF NOT EXISTS threesome_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            threesome_session_id TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            bot_name TEXT NOT NULL,
            role TEXT NOT NULL,
            instance_id TEXT,
            participant_type TEXT NOT NULL,
            name TEXT NOT NULL,
            intimacy_level INTEGER DEFAULT 1,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (threesome_session_id) REFERENCES threesome_sessions(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE
        )
    """)
    
    await db.execute("CREATE INDEX IF NOT EXISTS idx_threesome_user_id ON threesome_sessions(user_id)")
    await db.commit()
    logger.info("✅ Threesome tables created")


async def create_user_sessions_table():
    """
    Membuat tabel user_sessions untuk menyimpan state permanen user
    """
    db = await get_db()
    
    # Cek apakah tabel sudah ada
    result = await db.fetch_one(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='user_sessions'"
    )
    
    if result:
        logger.info("📋 Table user_sessions already exists")
        return
    
    # Buat tabel dengan semua kolom
    await db.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            session_id TEXT,
            role TEXT,
            bot_name TEXT,
            rel_type TEXT,
            instance_id TEXT,
            intimacy_level INTEGER DEFAULT 1,
            total_chats INTEGER DEFAULT 0,
            current_location TEXT DEFAULT 'ruang tamu',
            current_clothing TEXT DEFAULT 'pakaian biasa',
            current_position TEXT DEFAULT 'santai',
            current_activity TEXT DEFAULT '',
            kakak_status TEXT DEFAULT 'ada',
            suami_status TEXT DEFAULT 'ada',
            kantor_sepi INTEGER DEFAULT 0,
            sedang_berdua INTEGER DEFAULT 0,
            current_emotion TEXT DEFAULT 'calm',
            arousal_level INTEGER DEFAULT 0,
            emotional_history TEXT DEFAULT '[]',
            physical_energy INTEGER DEFAULT 80,
            physical_hunger INTEGER DEFAULT 30,
            physical_thirst INTEGER DEFAULT 30,
            role_arousal INTEGER DEFAULT 0,
            role_mode_goda INTEGER DEFAULT 0,
            role_attraction INTEGER DEFAULT 50,
            scenes TEXT DEFAULT '[]',
            milestones TEXT DEFAULT '[]',
            promises TEXT DEFAULT '[]',
            plans TEXT DEFAULT '[]',
            user_preferences TEXT DEFAULT '{}',
            current_scene_id TEXT,
            relationship_status TEXT DEFAULT 'pdkt',
            created_at REAL,
            updated_at REAL
        )
    """)
    
    # Buat indeks untuk performa
    await db.execute("CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id)")
    await db.execute("CREATE INDEX IF NOT EXISTS idx_user_sessions_role ON user_sessions(role)")
    await db.execute("CREATE INDEX IF NOT EXISTS idx_user_sessions_updated_at ON user_sessions(updated_at)")
    
    await db.commit()
    
    logger.info("✅ Table user_sessions created successfully")


async def fix_missing_columns():
    """
    Perbaiki kolom yang hilang di tabel user_sessions
    Jalankan ini jika ada error 'no such column'
    """
    db = await get_db()
    
    # Cek apakah tabel ada
    result = await db.fetch_one(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='user_sessions'"
    )
    
    if not result:
        logger.warning("⚠️ user_sessions table not found, creating...")
        await create_user_sessions_table()
        return
    
    # Daftar kolom yang harus ada
    columns_to_add = {
        'current_activity': "TEXT DEFAULT ''",
        'kakak_status': "TEXT DEFAULT 'ada'",
        'suami_status': "TEXT DEFAULT 'ada'",
        'kantor_sepi': "INTEGER DEFAULT 0",
        'sedang_berdua': "INTEGER DEFAULT 0",
        'current_emotion': "TEXT DEFAULT 'calm'",
        'arousal_level': "INTEGER DEFAULT 0",
        'emotional_history': "TEXT DEFAULT '[]'",
        'physical_energy': "INTEGER DEFAULT 80",
        'physical_hunger': "INTEGER DEFAULT 30",
        'physical_thirst': "INTEGER DEFAULT 30",
        'role_arousal': "INTEGER DEFAULT 0",
        'role_mode_goda': "INTEGER DEFAULT 0",
        'role_attraction': "INTEGER DEFAULT 50",
        'scenes': "TEXT DEFAULT '[]'",
        'milestones': "TEXT DEFAULT '[]'",
        'promises': "TEXT DEFAULT '[]'",
        'plans': "TEXT DEFAULT '[]'",
        'user_preferences': "TEXT DEFAULT '{}'",
        'current_scene_id': "TEXT",
    }
    
    # Dapatkan kolom yang sudah ada
    existing = await db.fetch_all("PRAGMA table_info(user_sessions)")
    existing_names = [col['name'] for col in existing]
    
    added = 0
    for col_name, col_def in columns_to_add.items():
        if col_name not in existing_names:
            try:
                await db.execute(f"ALTER TABLE user_sessions ADD COLUMN {col_name} {col_def}")
                logger.info(f"✅ Added missing column: {col_name}")
                added += 1
            except Exception as e:
                logger.warning(f"⚠️ Could not add column {col_name}: {e}")
    
    if added > 0:
        await db.commit()
        logger.info(f"📊 Fixed {added} missing columns")
    else:
        logger.info("✅ No missing columns found")
    
    return added


# =============================================================================
# MAIN MIGRATION FUNCTION
# =============================================================================

async def run_migrations():
    """
    Menjalankan semua migrasi database
    """
    logger.info("=" * 50)
    logger.info("🚀 Running database migrations...")
    logger.info("=" * 50)
    
    # ===== TABEL UTAMA =====
    await create_users_table()
    await create_sessions_table()
    await create_conversations_table()
    
    # ===== PDKT TABLES =====
    await create_pdkt_tables()
    
    # ===== MANTAN TABLES =====
    await create_mantan_tables()
    
    # ===== FWB TABLES =====
    await create_fwb_tables()
    
    # ===== HTS TABLES =====
    await create_hts_tables()
    
    # ===== MEMORY TABLES =====
    await create_memories_table()
    await create_preferences_table()
    await create_milestones_table()
    
    # ===== BACKUP TABLE =====
    await create_backups_table()
    
    # ===== THREESOME TABLES =====
    await create_threesome_tables()
    
    # ===== USER SESSIONS TABLE (BARU) =====
    await create_user_sessions_table()
    
    # ===== VERIFIKASI =====
    db = await get_db()
    
    # Hitung jumlah tabel
    tables = await db.fetch_all("SELECT name FROM sqlite_master WHERE type='table'")
    logger.info(f"📊 Total tables: {len(tables)}")
    
    # Tampilkan daftar tabel
    for table in tables:
        logger.info(f"   • {table['name']}")
    
    logger.info("=" * 50)
    logger.info("✅ All migrations completed successfully!")
    logger.info("=" * 50)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

async def reset_user_session(user_id: int):
    """
    Reset session user (hapus semua data user)
    Gunakan dengan hati-hati, hanya untuk debugging
    
    Args:
        user_id: ID Telegram user
    """
    db = await get_db()
    
    await db.execute("DELETE FROM user_sessions WHERE user_id = ?", (user_id,))
    await db.commit()
    
    logger.info(f"🗑️ Reset user session for user {user_id}")


async def cleanup_old_sessions(days: int = 30):
    """
    Membersihkan session yang sudah tidak aktif lebih dari X hari
    
    Args:
        days: Jumlah hari untuk session dianggap kadaluarsa
    """
    db = await get_db()
    
    cutoff = time.time() - (days * 86400)
    
    # Hapus session yang tidak aktif
    result = await db.execute(
        "DELETE FROM user_sessions WHERE updated_at < ?",
        (cutoff,)
    )
    
    deleted = result.rowcount
    
    if deleted > 0:
        await db.commit()
        logger.info(f"🧹 Cleaned up {deleted} old sessions (inactive > {days} days)")
    else:
        logger.info(f"🧹 No old sessions to clean up")


async def backup_user_sessions(backup_dir: str = "backups"):
    """
    Backup semua user session ke file JSON
    
    Args:
        backup_dir: Direktori untuk menyimpan backup
    """
    import os
    from datetime import datetime
    
    db = await get_db()
    
    # Buat direktori jika belum ada
    os.makedirs(backup_dir, exist_ok=True)
    
    # Ambil semua session
    sessions = await db.fetch_all("SELECT * FROM user_sessions")
    
    if not sessions:
        logger.info("📭 No user sessions to backup")
        return
    
    # Buat nama file backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"user_sessions_backup_{timestamp}.json")
    
    # Convert ke list dict
    sessions_list = []
    for session in sessions:
        sessions_list.append(dict(session))
    
    # Simpan ke file
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(sessions_list, f, indent=2, ensure_ascii=False, default=str)
    
    logger.info(f"💾 Backup saved: {backup_file} ({len(sessions_list)} sessions)")


async def restore_user_sessions(backup_file: str):
    """
    Restore user session dari file backup
    
    Args:
        backup_file: Path file backup JSON
    """
    import os
    
    db = await get_db()
    
    if not os.path.exists(backup_file):
        logger.error(f"❌ Backup file not found: {backup_file}")
        return
    
    with open(backup_file, 'r', encoding='utf-8') as f:
        sessions = json.load(f)
    
    if not sessions:
        logger.warning("⚠️ No sessions in backup file")
        return
    
    restored = 0
    skipped = 0
    
    for session in sessions:
        user_id = session.get('user_id')
        
        if not user_id:
            skipped += 1
            continue
        
        # Cek apakah sudah ada
        existing = await db.fetch_one(
            "SELECT id FROM user_sessions WHERE user_id = ?",
            (user_id,)
        )
        
        now = time.time()
        
        if existing:
            # Update existing
            await db.execute("""
                UPDATE user_sessions SET
                    session_id = ?, role = ?, bot_name = ?, rel_type = ?,
                    instance_id = ?, intimacy_level = ?, total_chats = ?,
                    current_location = ?, current_clothing = ?, current_position = ?,
                    current_activity = ?, kakak_status = ?, suami_status = ?,
                    kantor_sepi = ?, sedang_berdua = ?, current_emotion = ?,
                    arousal_level = ?, physical_energy = ?, physical_hunger = ?,
                    physical_thirst = ?, role_arousal = ?, role_mode_goda = ?,
                    role_attraction = ?, scenes = ?, milestones = ?,
                    promises = ?, plans = ?, user_preferences = ?,
                    current_scene_id = ?, relationship_status = ?, updated_at = ?
                WHERE user_id = ?
            """, (
                session.get('session_id'), session.get('role'), session.get('bot_name'),
                session.get('rel_type'), session.get('instance_id'), session.get('intimacy_level', 1),
                session.get('total_chats', 0), session.get('current_location', 'ruang tamu'),
                session.get('current_clothing', 'pakaian biasa'), session.get('current_position', 'santai'),
                session.get('current_activity', ''), session.get('kakak_status', 'ada'),
                session.get('suami_status', 'ada'), session.get('kantor_sepi', 0),
                session.get('sedang_berdua', 0), session.get('current_emotion', 'calm'),
                session.get('arousal_level', 0), session.get('physical_energy', 80),
                session.get('physical_hunger', 30), session.get('physical_thirst', 30),
                session.get('role_arousal', 0), session.get('role_mode_goda', 0),
                session.get('role_attraction', 50), session.get('scenes', '[]'),
                session.get('milestones', '[]'), session.get('promises', '[]'),
                session.get('plans', '[]'), session.get('user_preferences', '{}'),
                session.get('current_scene_id'), session.get('relationship_status', 'pdkt'),
                now, user_id
            ))
        else:
            # Insert new
            await db.execute("""
                INSERT INTO user_sessions (
                    user_id, session_id, role, bot_name, rel_type, instance_id,
                    intimacy_level, total_chats, current_location, current_clothing,
                    current_position, current_activity, kakak_status, suami_status,
                    kantor_sepi, sedang_berdua, current_emotion, arousal_level,
                    physical_energy, physical_hunger, physical_thirst, role_arousal,
                    role_mode_goda, role_attraction, scenes, milestones, promises,
                    plans, user_preferences, current_scene_id, relationship_status,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, session.get('session_id'), session.get('role'), session.get('bot_name'),
                session.get('rel_type'), session.get('instance_id'), session.get('intimacy_level', 1),
                session.get('total_chats', 0), session.get('current_location', 'ruang tamu'),
                session.get('current_clothing', 'pakaian biasa'), session.get('current_position', 'santai'),
                session.get('current_activity', ''), session.get('kakak_status', 'ada'),
                session.get('suami_status', 'ada'), session.get('kantor_sepi', 0),
                session.get('sedang_berdua', 0), session.get('current_emotion', 'calm'),
                session.get('arousal_level', 0), session.get('physical_energy', 80),
                session.get('physical_hunger', 30), session.get('physical_thirst', 30),
                session.get('role_arousal', 0), session.get('role_mode_goda', 0),
                session.get('role_attraction', 50), session.get('scenes', '[]'),
                session.get('milestones', '[]'), session.get('promises', '[]'),
                session.get('plans', '[]'), session.get('user_preferences', '{}'),
                session.get('current_scene_id'), session.get('relationship_status', 'pdkt'),
                session.get('created_at', now), now
            ))
        
        restored += 1
    
    await db.commit()
    
    logger.info(f"📥 Restored {restored} sessions from {backup_file} (skipped: {skipped})")


async def get_user_sessions_stats() -> Dict[str, Any]:
    """
    Dapatkan statistik user sessions
    
    Returns:
        Dict statistik
    """
    db = await get_db()
    
    # Total sessions
    total = await db.fetch_one("SELECT COUNT(*) as count FROM user_sessions")
    
    # Sessions by role
    by_role = await db.fetch_all("""
        SELECT role, COUNT(*) as count 
        FROM user_sessions 
        WHERE role IS NOT NULL 
        GROUP BY role 
        ORDER BY count DESC
    """)
    
    # Average intimacy level
    avg_intimacy = await db.fetch_one("SELECT AVG(intimacy_level) as avg FROM user_sessions")
    
    # Active sessions (updated in last 24 hours)
    day_ago = time.time() - 86400
    active = await db.fetch_one(
        "SELECT COUNT(*) as count FROM user_sessions WHERE updated_at > ?",
        (day_ago,)
    )
    
    # Most common locations
    top_locations = await db.fetch_all("""
        SELECT current_location, COUNT(*) as count 
        FROM user_sessions 
        GROUP BY current_location 
        ORDER BY count DESC 
        LIMIT 5
    """)
    
    return {
        'total_sessions': total['count'] if total else 0,
        'by_role': [{'role': r['role'], 'count': r['count']} for r in by_role],
        'avg_intimacy_level': round(avg_intimacy['avg'], 1) if avg_intimacy and avg_intimacy['avg'] else 0,
        'active_24h': active['count'] if active else 0,
        'top_locations': [{'location': l['current_location'], 'count': l['count']} for l in top_locations]
    }


__all__ = [
    'run_migrations',
    'create_user_sessions_table',
    'fix_missing_columns',
    'reset_user_session',
    'cleanup_old_sessions',
    'backup_user_sessions',
    'restore_user_sessions',
    'get_user_sessions_stats',
]
