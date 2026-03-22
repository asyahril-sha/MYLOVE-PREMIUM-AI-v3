#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - DATABASE CONNECTION
=============================================================================
Koneksi SQLite dengan async support (aiosqlite)
- Connection pooling
- Auto migration
- Performance optimizations (WAL mode, cache)
- Support close_db untuk graceful shutdown
=============================================================================
"""

import os
import time
import json
import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager

import aiosqlite

from config import settings

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    Manajemen koneksi database SQLite
    Support async operations dengan connection pooling
    """
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.pool_size = getattr(settings.database, 'pool_size', 5)
        self.timeout = getattr(settings.database, 'timeout', 30)
        self._connection = None
        self._initialized = False
        
    async def initialize(self):
        """Initialize database and create tables"""
        try:
            # Buat directory jika belum ada
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Koneksi pertama untuk setup
            self._connection = await aiosqlite.connect(
                str(self.db_path),
                timeout=self.timeout
            )
            
            # Enable foreign keys
            await self._connection.execute("PRAGMA foreign_keys = ON")
            
            # Optimize SQLite for performance
            await self._connection.execute("PRAGMA journal_mode = WAL")
            await self._connection.execute("PRAGMA synchronous = NORMAL")
            await self._connection.execute("PRAGMA cache_size = 10000")
            await self._connection.execute("PRAGMA temp_store = MEMORY")
            
            # Buat tables
            await self._create_tables()
            
            self._initialized = True
            logger.info(f"✅ Database initialized at {self.db_path}")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    async def _create_tables(self):
        """Create all database tables"""
        
        # ===== USERS TABLE =====
        await self._connection.execute('''
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
        ''')
        
        # ===== SESSIONS TABLE =====
        await self._connection.execute('''
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
                metadata TEXT,
                FOREIGN KEY (user_id) REFERENCES users (telegram_id)
            )
        ''')
        
        # ===== CONVERSATIONS TABLE =====
        await self._connection.execute('''
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
        ''')
        
        # ===== MEMORIES TABLE =====
        await self._connection.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role TEXT,
                memory_type TEXT,
                content TEXT NOT NULL,
                importance REAL DEFAULT 0.5,
                emotional_tag TEXT,
                timestamp REAL NOT NULL,
                metadata TEXT,
                FOREIGN KEY (user_id) REFERENCES users (telegram_id)
            )
        ''')
        
        # ===== RELATIONSHIPS TABLE =====
        await self._connection.execute('''
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                bot_name TEXT NOT NULL,
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
        ''')
        
        # ===== PDKT SESSIONS TABLE =====
        await self._connection.execute('''
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
        ''')
        
        # ===== PDKT INNER THOUGHTS TABLE =====
        await self._connection.execute('''
            CREATE TABLE IF NOT EXISTS pdkt_inner_thoughts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pdkt_id TEXT NOT NULL,
                thought TEXT NOT NULL,
                context TEXT,
                timestamp REAL NOT NULL,
                FOREIGN KEY (pdkt_id) REFERENCES pdkt_sessions (id)
            )
        ''')
        
        # ===== MANTAN TABLE =====
        await self._connection.execute('''
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
        ''')
        
        # ===== FWB RELATIONS TABLE =====
        await self._connection.execute('''
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
        ''')
        
        # ===== HTS RELATIONS TABLE =====
        await self._connection.execute('''
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
        ''')
        
        # ===== THREESOME SESSIONS TABLE =====
        await self._connection.execute('''
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
        ''')
        
        # ===== THREESOME PARTICIPANTS TABLE =====
        await self._connection.execute('''
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
                FOREIGN KEY (threesome_session_id) REFERENCES threesome_sessions (id)
            )
        ''')
        
        # ===== PREFERENCES TABLE =====
        await self._connection.execute('''
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
        ''')
        
        # ===== MILESTONES TABLE =====
        await self._connection.execute('''
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
        ''')
        
        # ===== BACKUPS TABLE =====
        await self._connection.execute('''
            CREATE TABLE IF NOT EXISTS backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                size INTEGER,
                created_at REAL NOT NULL,
                type TEXT DEFAULT 'auto',
                status TEXT DEFAULT 'completed',
                metadata TEXT
            )
        ''')
        
        # ===== 🔥 BARU: USER SESSIONS TABLE (STATE PERSISTENCE) =====
        await self._connection.execute('''
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
        ''')
        
        # ===== CREATE INDEXES =====
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id, status)")
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_sessions_time ON sessions(last_message_time)")
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_memories_user ON memories(user_id, role)")
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_relationships_user ON relationships(user_id, status)")
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_pdkt_sessions_user ON pdkt_sessions(user_id, status)")
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_mantan_user ON mantan(user_id)")
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_fwb_user ON fwb_relations(user_id, status)")
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_hts_user ON hts_relations(user_id, status)")
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_hts_expiry ON hts_relations(expiry_time)")
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id)")
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_user_sessions_updated_at ON user_sessions(updated_at)")
        
        await self._connection.commit()
        logger.info("✅ Database tables and indexes created")
        
    @asynccontextmanager
    async def get_connection(self):
        """Get database connection from pool"""
        if not self._initialized:
            await self.initialize()
            
        conn = None
        try:
            conn = await aiosqlite.connect(
                str(self.db_path),
                timeout=self.timeout
            )
            await conn.execute("PRAGMA foreign_keys = ON")
            yield conn
        finally:
            if conn:
                await conn.close()
                
    async def execute(self, query: str, params: tuple = ()) -> aiosqlite.Cursor:
        """Execute query and return cursor"""
        async with self.get_connection() as conn:
            cursor = await conn.execute(query, params)
            await conn.commit()
            return cursor
            
    async def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Fetch one row as dict"""
        async with self.get_connection() as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute(query, params)
            row = await cursor.fetchone()
            return dict(row) if row else None
            
    async def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """Fetch all rows as list of dicts"""
        async with self.get_connection() as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute(query, params)
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
            
    async def execute_many(self, query: str, params_list: List[tuple]):
        """Execute many inserts/updates"""
        async with self.get_connection() as conn:
            await conn.executemany(query, params_list)
            await conn.commit()
            
    async def vacuum(self):
        """Vacuum database (optimize)"""
        async with self.get_connection() as conn:
            await conn.execute("VACUUM")
            logger.info("✅ Database vacuum completed")
            
    async def backup(self, backup_path: Path) -> bool:
        """Backup database to file"""
        try:
            async with self.get_connection() as conn:
                await conn.backup(aiosqlite.connect(str(backup_path)))
            logger.info(f"✅ Database backed up to {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False
            
    async def get_stats(self) -> Dict:
        """Get database statistics"""
        stats = {}
        
        tables = [
            'users', 'sessions', 'conversations', 'memories',
            'relationships', 'pdkt_sessions', 'mantan', 'fwb_relations',
            'hts_relations', 'threesome_sessions', 'preferences', 'milestones',
            'user_sessions'
        ]
        
        for table in tables:
            try:
                result = await self.fetch_one(f"SELECT COUNT(*) as count FROM {table}")
                stats[f"{table}_count"] = result['count'] if result else 0
            except:
                stats[f"{table}_count"] = 0
                
        if self.db_path.exists():
            stats['db_size_mb'] = round(self.db_path.stat().st_size / (1024 * 1024), 2)
        else:
            stats['db_size_mb'] = 0
            
        return stats
        
    async def close(self):
        """Close database connection"""
        if self._connection:
            await self._connection.close()
            self._initialized = False
            logger.info("📁 Database connection closed")


# =============================================================================
# GLOBAL DATABASE INSTANCE
# =============================================================================

_db_instance: Optional[DatabaseConnection] = None


async def get_db() -> DatabaseConnection:
    """Get global database instance"""
    global _db_instance
    if _db_instance is None:
        db_path = settings.database.path
        _db_instance = DatabaseConnection(db_path)
        await _db_instance.initialize()
    return _db_instance


async def init_db():
    """Initialize database (for startup)"""
    db = await get_db()
    return db


# =============================================================================
# 🔥 BARU: close_db FUNCTION (UNTUK GRACEFUL SHUTDOWN)
# =============================================================================

async def close_db():
    """
    Close global database connection
    Gunakan saat shutdown bot untuk graceful shutdown
    """
    global _db_instance
    if _db_instance:
        await _db_instance.close()
        _db_instance = None
        logger.info("📁 Global database connection closed")


# =============================================================================
# COMPATIBILITY FUNCTIONS (UNTUK MIGRATE.PY)
# =============================================================================

async def execute_query(query: str, params: tuple = ()):
    """Execute query and return lastrowid (compatibility)"""
    db = await get_db()
    cursor = await db.execute(query, params)
    return cursor.lastrowid if hasattr(cursor, 'lastrowid') else None


async def fetch_one_compat(query: str, params: tuple = ()):
    """Fetch one row (compatibility)"""
    return await get_db().fetch_one(query, params)


async def fetch_all_compat(query: str, params: tuple = ()):
    """Fetch all rows (compatibility)"""
    return await get_db().fetch_all(query, params)


__all__ = [
    'DatabaseConnection',
    'get_db',
    'init_db',
    'close_db',           # 🔥 BARU
    'execute_query',
    'fetch_one_compat',
    'fetch_all_compat',
]
