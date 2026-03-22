#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - DATABASE MIGRATION
=============================================================================
Migrasi database dari V1 ke V2
Cukup jalankan sekali: python database/migrate.py
"""

import sqlite3
import time
import os
from pathlib import Path
from datetime import datetime


def migrate():
    """Migrasi database ke V2"""
    
    print("=" * 60)
    print("🚀 MYLOVE PREMIUM AI - DATABASE MIGRATION")
    print("=" * 60)
    
    # Lokasi database
    db_path = Path("data/mylove.db")
    
    # Pastikan folder data ada
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Backup jika sudah ada
    if db_path.exists():
        backup_path = db_path.parent / f"mylove_backup_{int(time.time())}.db"
        print(f"📁 Creating backup: {backup_path}")
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
    
    # Konek ke database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"📁 Database: {db_path}")
    print("🔄 Running migrations...")
    
    # =========================================================================
    # TABEL USERS
    # =========================================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            created_at REAL NOT NULL,
            last_active REAL NOT NULL,
            total_interactions INTEGER DEFAULT 0,
            preferences TEXT,
            settings TEXT
        )
    """)
    print("  ✅ users")
    
    # =========================================================================
    # TABEL SESSIONS (DENGAN BOT_NAME)
    # =========================================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            bot_name TEXT NOT NULL DEFAULT 'Aurora',
            role TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            start_time REAL NOT NULL,
            end_time REAL,
            last_message_time REAL NOT NULL,
            total_messages INTEGER DEFAULT 0,
            intimacy_level INTEGER DEFAULT 1,
            location TEXT,
            summary TEXT,
            metadata TEXT,
            FOREIGN KEY (user_id) REFERENCES users (telegram_id)
        )
    """)
    print("  ✅ sessions (with bot_name)")
    
    # =========================================================================
    # TABEL CONVERSATIONS
    # =========================================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            timestamp REAL NOT NULL,
            user_message TEXT,
            bot_response TEXT,
            intent TEXT,
            mood TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        )
    """)
    print("  ✅ conversations")
    
    # =========================================================================
    # TABEL PDKT SESSIONS
    # =========================================================================
    cursor.execute("""
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
            total_duration REAL DEFAULT 0.0,
            total_chats INTEGER DEFAULT 0,
            total_intim INTEGER DEFAULT 0,
            total_climax INTEGER DEFAULT 0,
            created_at REAL NOT NULL,
            last_interaction REAL NOT NULL,
            paused_at REAL,
            ended_at REAL,
            end_reason TEXT,
            inner_thoughts TEXT,
            milestones TEXT,
            metadata TEXT
        )
    """)
    print("  ✅ pdkt_sessions")
    
    # =========================================================================
    # TABEL PDKT INNER THOUGHTS
    # =========================================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pdkt_inner_thoughts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pdkt_id TEXT NOT NULL,
            thought TEXT NOT NULL,
            context TEXT,
            timestamp REAL NOT NULL,
            FOREIGN KEY (pdkt_id) REFERENCES pdkt_sessions (id)
        )
    """)
    print("  ✅ pdkt_inner_thoughts")
    
    # =========================================================================
    # TABEL MANTAN
    # =========================================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mantan (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            pdkt_id TEXT NOT NULL,
            bot_name TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT DEFAULT 'putus',
            putus_time REAL NOT NULL,
            putus_reason TEXT NOT NULL,
            chemistry_history TEXT,
            milestones TEXT,
            total_chats INTEGER DEFAULT 0,
            total_intim INTEGER DEFAULT 0,
            total_climax INTEGER DEFAULT 0,
            first_kiss_time REAL,
            first_intim_time REAL,
            become_pacar_time REAL,
            last_chat_time REAL NOT NULL,
            fwb_requests TEXT,
            fwb_start_time REAL,
            fwb_end_time REAL
        )
    """)
    print("  ✅ mantan")
    
    # =========================================================================
    # TABEL FWB RELATIONS
    # =========================================================================
    cursor.execute("""
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
            pause_history TEXT,
            ended_at REAL,
            end_reason TEXT
        )
    """)
    print("  ✅ fwb_relations")
    
    # =========================================================================
    # TABEL HTS RELATIONS
    # =========================================================================
    cursor.execute("""
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
            history TEXT
        )
    """)
    print("  ✅ hts_relations")
    
    # =========================================================================
    # TABEL MEMORIES
    # =========================================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT,
            memory_type TEXT NOT NULL,
            content TEXT NOT NULL,
            importance REAL DEFAULT 0.5,
            emotional_tag TEXT,
            timestamp REAL NOT NULL,
            metadata TEXT,
            FOREIGN KEY (user_id) REFERENCES users (telegram_id)
        )
    """)
    print("  ✅ memories")
    
    # =========================================================================
    # TABEL RELATIONSHIPS
    # =========================================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            bot_name TEXT NOT NULL DEFAULT 'Aurora',
            role TEXT NOT NULL,
            instance_id TEXT,
            status TEXT DEFAULT 'hts',
            intimacy_level INTEGER DEFAULT 1,
            total_interactions INTEGER DEFAULT 0,
            total_intim_sessions INTEGER DEFAULT 0,
            total_climax INTEGER DEFAULT 0,
            created_at REAL NOT NULL,
            last_interaction REAL NOT NULL,
            preferences TEXT,
            milestones TEXT,
            history TEXT
        )
    """)
    print("  ✅ relationships")
    
    # =========================================================================
    # TABEL THREESOME SESSIONS
    # =========================================================================
    cursor.execute("""
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
            participants TEXT,
            interactions TEXT,
            FOREIGN KEY (user_id) REFERENCES users (telegram_id)
        )
    """)
    print("  ✅ threesome_sessions")
    
    # =========================================================================
    # TABEL THREESOME PARTICIPANTS
    # =========================================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS threesome_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            threesome_session_id TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            bot_name TEXT NOT NULL DEFAULT 'Aurora',
            role TEXT NOT NULL,
            instance_id TEXT,
            participant_type TEXT NOT NULL,
            name TEXT NOT NULL,
            intimacy_level INTEGER DEFAULT 1,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (threesome_session_id) REFERENCES threesome_sessions (id)
        )
    """)
    print("  ✅ threesome_participants")
    
    # =========================================================================
    # TABEL PREFERENCES
    # =========================================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT,
            pref_type TEXT NOT NULL,
            item TEXT NOT NULL,
            score REAL DEFAULT 0.5,
            count INTEGER DEFAULT 1,
            last_updated REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (telegram_id)
        )
    """)
    print("  ✅ preferences")
    
    # =========================================================================
    # TABEL MILESTONES
    # =========================================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT,
            milestone_type TEXT NOT NULL,
            description TEXT,
            timestamp REAL NOT NULL,
            intimacy_level INTEGER,
            metadata TEXT,
            FOREIGN KEY (user_id) REFERENCES users (telegram_id)
        )
    """)
    print("  ✅ milestones")
    
    # =========================================================================
    # TABEL BACKUPS
    # =========================================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS backups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            size INTEGER,
            created_at REAL NOT NULL,
            type TEXT DEFAULT 'auto',
            status TEXT DEFAULT 'completed',
            metadata TEXT
        )
    """)
    print("  ✅ backups")
    
    # =========================================================================
    # TABEL USER SESSIONS (UNTUK PERMANENT STORAGE)
    # =========================================================================
    cursor.execute("""
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
            relationship_status TEXT DEFAULT 'pdkt',
            created_at REAL,
            updated_at REAL
        )
    """)
    print("  ✅ user_sessions")
    
    # =========================================================================
    # CREATE INDEXES
    # =========================================================================
    
    # Users indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_telegram ON users(telegram_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_active ON users(last_active)")
    
    # Sessions indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id, status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_time ON sessions(last_message_time)")
    
    # Conversations indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_session ON conversations(session_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_time ON conversations(timestamp)")
    
    # PDKT indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pdkt_user ON pdkt_sessions(user_id, status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pdkt_role ON pdkt_sessions(role)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pdkt_thoughts ON pdkt_inner_thoughts(pdkt_id)")
    
    # Mantan indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_mantan_user ON mantan(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_mantan_status ON mantan(status)")
    
    # FWB indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fwb_user ON fwb_relations(user_id, status)")
    
    # HTS indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_hts_user ON hts_relations(user_id, status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_hts_expiry ON hts_relations(expiry_time)")
    
    # Memories indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_user ON memories(user_id, role)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(memory_type)")
    
    # Relationships indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_relationships_user ON relationships(user_id, status)")
    
    # Threesome indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_threesome_user ON threesome_sessions(user_id)")
    
    # Preferences indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_preferences_user ON preferences(user_id, pref_type)")
    
    # Milestones indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_milestones_user ON milestones(user_id, timestamp)")
    
    # User sessions indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_sessions_user ON user_sessions(user_id)")
    
    print("  ✅ indexes")
    
    # =========================================================================
    # MIGRATION LOG TABLE
    # =========================================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS migration_log (
            version TEXT PRIMARY KEY,
            migrated_at REAL NOT NULL,
            description TEXT
        )
    """)
    
    # Cek apakah sudah migrasi
    cursor.execute("SELECT version FROM migration_log WHERE version = 'v2'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO migration_log (version, migrated_at, description) VALUES (?, ?, ?)",
            ('v2', time.time(), 'MYLOVE PREMIUM AI - Full V2 migration')
        )
        print("  ✅ migration_log updated")
    
    # =========================================================================
    # COMMIT & FINISH
    # =========================================================================
    conn.commit()
    
    # Cek hasil
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("=" * 60)
    print(f"✅ MIGRATION COMPLETED! {len(tables)} tables available:")
    for table in tables:
        print(f"   • {table[0]}")
    print("=" * 60)
    
    # =========================================================================
    # VERIFY TABLES
    # =========================================================================
    print("\n📊 VERIFYING TABLES...")
    required_tables = [
        'users', 'sessions', 'conversations', 'pdkt_sessions',
        'pdkt_inner_thoughts', 'mantan', 'fwb_relations', 'hts_relations',
        'memories', 'relationships', 'threesome_sessions', 'threesome_participants',
        'preferences', 'milestones', 'backups', 'migration_log', 'user_sessions'
    ]
    
    missing = []
    for table in required_tables:
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        if not cursor.fetchone():
            missing.append(table)
    
    if missing:
        print(f"⚠️ Missing tables: {missing}")
    else:
        print("✅ All required tables present!")
    
    # =========================================================================
    # DATABASE SIZE
    # =========================================================================
    if db_path.exists():
        size_bytes = db_path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        print(f"📦 Database size: {size_mb:.2f} MB")
    
    conn.close()
    
    print("\n🎉 Migration successful! Your MYLOVE PREMIUM AI database is ready.")
    return True


if __name__ == "__main__":
    migrate()
