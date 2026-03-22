#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - DATABASE REPOSITORY
=============================================================================
Repository pattern untuk semua operasi database
Menggabungkan semua method V1 dan V2
"""

import time
import json
import logging
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

from .connection import get_db
from .models import (
    User, Session, Conversation, PDKTSession, Mantan, FWBRelation, HTSRelation,
    Memory, Preference, Milestone, Backup,
    ThreesomeSession, ThreesomeParticipant,
    RelationshipStatus, PDKTStatus, PDKTDirection, ChemistryLevel,
    MoodType, MemoryType, MilestoneType, SessionStatus,
    FWBStatus, HTSStatus, MantanStatus, BackupType, BackupStatus, PreferenceType
)

logger = logging.getLogger(__name__)


class Repository:
    """
    Repository untuk semua operasi database
    Menggabungkan method dari V1 dan V2
    """
    
    def __init__(self):
        self.db = None
        
    async def _get_db(self):
        """Get database connection"""
        if not self.db:
            self.db = await get_db()
        return self.db
    
    # =========================================================================
    # USER REPOSITORY
    # =========================================================================
    
    async def get_user(self, telegram_id: int) -> Optional[User]:
        """Get user by Telegram ID"""
        db = await self._get_db()
        result = await db.fetch_one(
            "SELECT * FROM users WHERE telegram_id = ?",
            (telegram_id,)
        )
        return User.from_dict(result) if result else None
        
    async def create_user(self, user: User) -> int:
        """Create new user"""
        db = await self._get_db()
        await db.execute(
            """
            INSERT INTO users 
            (telegram_id, username, first_name, last_name, created_at, last_active, 
             total_interactions, preferences, settings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user.telegram_id, user.username, user.first_name, user.last_name,
                user.created_at, user.last_active, user.total_interactions,
                json.dumps(user.preferences), json.dumps(user.settings)
            )
        )
        logger.info(f"✅ Created user: {user.telegram_id}")
        return user.telegram_id
        
    async def update_user(self, user: User):
        """Update existing user"""
        db = await self._get_db()
        await db.execute(
            """
            UPDATE users SET
                username = ?, first_name = ?, last_name = ?,
                last_active = ?, total_interactions = ?,
                preferences = ?, settings = ?
            WHERE telegram_id = ?
            """,
            (
                user.username, user.first_name, user.last_name,
                user.last_active, user.total_interactions,
                json.dumps(user.preferences), json.dumps(user.settings),
                user.telegram_id
            )
        )
        
    async def update_user_last_active(self, telegram_id: int):
        """Update user last active timestamp"""
        db = await self._get_db()
        await db.execute(
            "UPDATE users SET last_active = ? WHERE telegram_id = ?",
            (time.time(), telegram_id)
        )
        
    async def increment_user_interactions(self, telegram_id: int):
        """Increment user total interactions"""
        db = await self._get_db()
        await db.execute(
            """
            UPDATE users 
            SET total_interactions = total_interactions + 1,
                last_active = ?
            WHERE telegram_id = ?
            """,
            (time.time(), telegram_id)
        )
    
    # =========================================================================
    # SESSION REPOSITORY
    # =========================================================================
    
    async def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID"""
        db = await self._get_db()
        result = await db.fetch_one(
            "SELECT * FROM sessions WHERE id = ?",
            (session_id,)
        )
        return Session.from_dict(result) if result else None
        
    async def get_active_session(self, user_id: int, role: Optional[str] = None) -> Optional[Session]:
        """Get active session for user"""
        db = await self._get_db()
        query = "SELECT * FROM sessions WHERE user_id = ? AND status = 'active'"
        params = [user_id]
        
        if role:
            query += " AND role = ?"
            params.append(role)
            
        query += " ORDER BY last_message_time DESC LIMIT 1"
        
        result = await db.fetch_one(query, params)
        return Session.from_dict(result) if result else None
        
    async def get_user_sessions(self, user_id: int, limit: int = 10, include_closed: bool = True) -> List[Session]:
        """Get all sessions for user"""
        db = await self._get_db()
        if include_closed:
            query = "SELECT * FROM sessions WHERE user_id = ? ORDER BY last_message_time DESC LIMIT ?"
        else:
            query = "SELECT * FROM sessions WHERE user_id = ? AND status = 'active' ORDER BY last_message_time DESC LIMIT ?"
            
        results = await db.fetch_all(query, (user_id, limit))
        return [Session.from_dict(r) for r in results]
        
    async def create_session(self, session: Session) -> str:
        """Create new session"""
        db = await self._get_db()
        await db.execute(
            """
            INSERT INTO sessions 
            (id, user_id, bot_name, role, status, start_time, last_message_time, 
             total_messages, intimacy_level, location, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session.id, session.user_id, session.bot_name, session.role, session.status.value,
                session.start_time, session.last_message_time,
                session.total_messages, session.intimacy_level,
                session.location, json.dumps(session.metadata)
            )
        )
        logger.info(f"✅ Created session: {session.id}")
        return session.id
        
    async def update_session(self, session: Session):
        """Update existing session"""
        db = await self._get_db()
        await db.execute(
            """
            UPDATE sessions SET
                status = ?, last_message_time = ?, total_messages = ?,
                intimacy_level = ?, location = ?, summary = ?, metadata = ?
            WHERE id = ?
            """,
            (
                session.status.value, session.last_message_time, session.total_messages,
                session.intimacy_level, session.location, session.summary,
                json.dumps(session.metadata), session.id
            )
        )
        
    async def close_session(self, session_id: str, summary: Optional[str] = None):
        """Close session"""
        db = await self._get_db()
        await db.execute(
            """
            UPDATE sessions 
            SET status = 'closed', end_time = ?, summary = ?
            WHERE id = ?
            """,
            (time.time(), summary, session_id)
        )
        logger.info(f"📁 Closed session: {session_id}")
        
    async def delete_session(self, session_id: str):
        """Delete session (cascade will delete conversations)"""
        db = await self._get_db()
        await db.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        logger.info(f"🗑️ Deleted session: {session_id}")
    
    # =========================================================================
    # CONVERSATION REPOSITORY
    # =========================================================================
    
    async def add_message(self, conversation: Conversation) -> int:
        """Add message to conversation"""
        db = await self._get_db()
        cursor = await db.execute(
            """
            INSERT INTO conversations 
            (session_id, timestamp, user_message, bot_response, intent, mood)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                conversation.session_id, conversation.timestamp,
                conversation.user_message, conversation.bot_response,
                conversation.intent, conversation.mood
            )
        )
        return cursor.lastrowid
        
    async def get_session_conversations(self, session_id: str, limit: int = 50) -> List[Conversation]:
        """Get conversations for session"""
        db = await self._get_db()
        results = await db.fetch_all(
            "SELECT * FROM conversations WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?",
            (session_id, limit)
        )
        return [Conversation.from_dict(r) for r in results]
        
    async def get_recent_conversations(self, user_id: int, limit: int = 10) -> List[Conversation]:
        """Get recent conversations for user"""
        db = await self._get_db()
        results = await db.fetch_all(
            """
            SELECT c.* FROM conversations c
            JOIN sessions s ON c.session_id = s.id
            WHERE s.user_id = ?
            ORDER BY c.timestamp DESC LIMIT ?
            """,
            (user_id, limit)
        )
        return [Conversation.from_dict(r) for r in results]
    
    # =========================================================================
    # PDKT REPOSITORY
    # =========================================================================
    
    async def create_pdkt(self, pdkt: PDKTSession) -> str:
        """Create new PDKT session"""
        db = await self._get_db()
        await db.execute(
            """
            INSERT INTO pdkt_sessions 
            (id, user_id, role, bot_name, status, direction, chemistry_score,
             chemistry_level, mood, level, total_duration, total_chats,
             total_intim, total_climax, created_at, last_interaction,
             paused_at, ended_at, end_reason, inner_thoughts, milestones, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                pdkt.id, pdkt.user_id, pdkt.role, pdkt.bot_name,
                pdkt.status.value, pdkt.direction.value, pdkt.chemistry_score,
                pdkt.chemistry_level.value, pdkt.mood.value, pdkt.level,
                pdkt.total_duration, pdkt.total_chats, pdkt.total_intim,
                pdkt.total_climax, pdkt.created_at, pdkt.last_interaction,
                pdkt.paused_at, pdkt.ended_at, pdkt.end_reason,
                json.dumps(pdkt.inner_thoughts), json.dumps(pdkt.milestones),
                json.dumps(pdkt.metadata)
            )
        )
        logger.info(f"✅ Created PDKT session: {pdkt.id}")
        return pdkt.id
    
    async def get_pdkt(self, pdkt_id: str) -> Optional[PDKTSession]:
        """Get PDKT session by ID"""
        db = await self._get_db()
        result = await db.fetch_one(
            "SELECT * FROM pdkt_sessions WHERE id = ?",
            (pdkt_id,)
        )
        return PDKTSession.from_dict(result) if result else None
    
    async def get_user_pdkt_list(self, user_id: int, include_ended: bool = False) -> List[PDKTSession]:
        """Get all PDKT sessions for user"""
        db = await self._get_db()
        if include_ended:
            query = "SELECT * FROM pdkt_sessions WHERE user_id = ? ORDER BY last_interaction DESC"
        else:
            query = "SELECT * FROM pdkt_sessions WHERE user_id = ? AND status IN ('active', 'paused') ORDER BY last_interaction DESC"
        
        results = await db.fetch_all(query, (user_id,))
        return [PDKTSession.from_dict(r) for r in results]
    
    async def get_active_pdkt_by_role(self, user_id: int, role: str) -> Optional[PDKTSession]:
        """Get active PDKT for specific role"""
        db = await self._get_db()
        result = await db.fetch_one(
            "SELECT * FROM pdkt_sessions WHERE user_id = ? AND role = ? AND status = 'active' LIMIT 1",
            (user_id, role)
        )
        return PDKTSession.from_dict(result) if result else None
    
    async def update_pdkt(self, pdkt: PDKTSession):
        """Update PDKT session"""
        db = await self._get_db()
        await db.execute(
            """
            UPDATE pdkt_sessions SET
                status = ?, direction = ?, chemistry_score = ?,
                chemistry_level = ?, mood = ?, level = ?,
                total_duration = ?, total_chats = ?, total_intim = ?,
                total_climax = ?, last_interaction = ?, paused_at = ?,
                ended_at = ?, end_reason = ?, inner_thoughts = ?,
                milestones = ?, metadata = ?
            WHERE id = ?
            """,
            (
                pdkt.status.value, pdkt.direction.value, pdkt.chemistry_score,
                pdkt.chemistry_level.value, pdkt.mood.value, pdkt.level,
                pdkt.total_duration, pdkt.total_chats, pdkt.total_intim,
                pdkt.total_climax, pdkt.last_interaction, pdkt.paused_at,
                pdkt.ended_at, pdkt.end_reason,
                json.dumps(pdkt.inner_thoughts), json.dumps(pdkt.milestones),
                json.dumps(pdkt.metadata), pdkt.id
            )
        )
    
    async def pause_pdkt(self, pdkt_id: str):
        """Pause PDKT session"""
        db = await self._get_db()
        await db.execute(
            "UPDATE pdkt_sessions SET status = ?, paused_at = ? WHERE id = ?",
            (PDKTStatus.PAUSED.value, time.time(), pdkt_id)
        )
        logger.info(f"⏸️ Paused PDKT: {pdkt_id}")
    
    async def resume_pdkt(self, pdkt_id: str):
        """Resume PDKT session"""
        db = await self._get_db()
        await db.execute(
            "UPDATE pdkt_sessions SET status = ?, paused_at = NULL WHERE id = ?",
            (PDKTStatus.ACTIVE.value, pdkt_id)
        )
        logger.info(f"▶️ Resumed PDKT: {pdkt_id}")
    
    async def stop_pdkt(self, pdkt_id: str, reason: str):
        """Stop/end PDKT session"""
        db = await self._get_db()
        await db.execute(
            "UPDATE pdkt_sessions SET status = ?, ended_at = ?, end_reason = ? WHERE id = ?",
            (PDKTStatus.ENDED.value, time.time(), reason, pdkt_id)
        )
        logger.info(f"💔 Stopped PDKT: {pdkt_id}")
    
    async def add_inner_thought(self, pdkt_id: str, thought: str, context: str = ""):
        """Add inner thought to PDKT"""
        db = await self._get_db()
        await db.execute(
            """
            INSERT INTO pdkt_inner_thoughts 
            (pdkt_id, thought, context, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (pdkt_id, thought, context, time.time())
        )
    
    async def get_inner_thoughts(self, pdkt_id: str, limit: int = 10) -> List[Dict]:
        """Get inner thoughts for PDKT"""
        db = await self._get_db()
        results = await db.fetch_all(
            "SELECT * FROM pdkt_inner_thoughts WHERE pdkt_id = ? ORDER BY timestamp DESC LIMIT ?",
            (pdkt_id, limit)
        )
        return [dict(r) for r in results]
    
    # =========================================================================
    # MANTAN REPOSITORY
    # =========================================================================
    
    async def add_mantan(self, mantan: Mantan) -> str:
        """Add new mantan"""
        db = await self._get_db()
        await db.execute(
            """
            INSERT INTO mantan 
            (id, user_id, pdkt_id, bot_name, role, status, putus_time,
             putus_reason, chemistry_history, milestones, total_chats,
             total_intim, total_climax, first_kiss_time, first_intim_time,
             become_pacar_time, last_chat_time, fwb_requests,
             fwb_start_time, fwb_end_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                mantan.id, mantan.user_id, mantan.pdkt_id, mantan.bot_name,
                mantan.role, mantan.status.value, mantan.putus_time,
                mantan.putus_reason, json.dumps(mantan.chemistry_history),
                json.dumps(mantan.milestones), mantan.total_chats,
                mantan.total_intim, mantan.total_climax, mantan.first_kiss_time,
                mantan.first_intim_time, mantan.become_pacar_time,
                mantan.last_chat_time, json.dumps(mantan.fwb_requests),
                mantan.fwb_start_time, mantan.fwb_end_time
            )
        )
        logger.info(f"✅ Added mantan: {mantan.id}")
        return mantan.id
    
    async def get_mantan(self, mantan_id: str) -> Optional[Mantan]:
        """Get mantan by ID"""
        db = await self._get_db()
        result = await db.fetch_one(
            "SELECT * FROM mantan WHERE id = ?",
            (mantan_id,)
        )
        return Mantan.from_dict(result) if result else None
    
    async def get_user_mantan(self, user_id: int) -> List[Mantan]:
        """Get all mantan for user"""
        db = await self._get_db()
        results = await db.fetch_all(
            "SELECT * FROM mantan WHERE user_id = ? ORDER BY putus_time DESC",
            (user_id,)
        )
        return [Mantan.from_dict(r) for r in results]
    
    async def update_mantan_status(self, mantan_id: str, status: MantanStatus):
        """Update mantan status"""
        db = await self._get_db()
        await db.execute(
            "UPDATE mantan SET status = ? WHERE id = ?",
            (status.value, mantan_id)
        )
    
    # =========================================================================
    # FWB REPOSITORY
    # =========================================================================
    
    async def create_fwb(self, fwb: FWBRelation) -> str:
        """Create new FWB relationship"""
        db = await self._get_db()
        await db.execute(
            """
            INSERT INTO fwb_relations 
            (id, user_id, mantan_id, bot_name, role, status, created_at,
             last_interaction, chemistry_score, climax_count, intim_count,
             total_chats, pause_history, ended_at, end_reason)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                fwb.id, fwb.user_id, fwb.mantan_id, fwb.bot_name, fwb.role,
                fwb.status.value, fwb.created_at, fwb.last_interaction,
                fwb.chemistry_score, fwb.climax_count, fwb.intim_count,
                fwb.total_chats, json.dumps(fwb.pause_history),
                fwb.ended_at, fwb.end_reason
            )
        )
        logger.info(f"✅ Created FWB: {fwb.id}")
        return fwb.id
    
    async def get_fwb(self, fwb_id: str) -> Optional[FWBRelation]:
        """Get FWB by ID"""
        db = await self._get_db()
        result = await db.fetch_one(
            "SELECT * FROM fwb_relations WHERE id = ?",
            (fwb_id,)
        )
        return FWBRelation.from_dict(result) if result else None
    
    async def get_user_fwb(self, user_id: int, include_ended: bool = False) -> List[FWBRelation]:
        """Get all FWB for user"""
        db = await self._get_db()
        if include_ended:
            query = "SELECT * FROM fwb_relations WHERE user_id = ? ORDER BY last_interaction DESC"
        else:
            query = "SELECT * FROM fwb_relations WHERE user_id = ? AND status IN ('active', 'paused') ORDER BY last_interaction DESC"
        
        results = await db.fetch_all(query, (user_id,))
        return [FWBRelation.from_dict(r) for r in results]
    
    async def get_top_fwb(self, user_id: int, limit: int = 10) -> List[FWBRelation]:
        """Get top FWB by score"""
        db = await self._get_db()
        results = await db.fetch_all(
            """
            SELECT *, (chemistry_score * 0.6 + climax_count * 0.4) as score 
            FROM fwb_relations 
            WHERE user_id = ? AND status = 'active' 
            ORDER BY score DESC LIMIT ?
            """,
            (user_id, limit)
        )
        return [FWBRelation.from_dict(r) for r in results]
    
    async def update_fwb(self, fwb: FWBRelation):
        """Update FWB relationship"""
        db = await self._get_db()
        await db.execute(
            """
            UPDATE fwb_relations SET
                status = ?, last_interaction = ?, chemistry_score = ?,
                climax_count = ?, intim_count = ?, total_chats = ?,
                pause_history = ?, ended_at = ?, end_reason = ?
            WHERE id = ?
            """,
            (
                fwb.status.value, fwb.last_interaction, fwb.chemistry_score,
                fwb.climax_count, fwb.intim_count, fwb.total_chats,
                json.dumps(fwb.pause_history), fwb.ended_at, fwb.end_reason,
                fwb.id
            )
        )
    
    async def pause_fwb(self, fwb_id: str, reason: str):
        """Pause FWB relationship"""
        db = await self._get_db()
        fwb = await self.get_fwb(fwb_id)
        if fwb:
            pause_history = fwb.pause_history
            pause_history.append({
                'timestamp': time.time(),
                'action': 'pause',
                'reason': reason
            })
            
            await db.execute(
                """
                UPDATE fwb_relations SET
                    status = ?, pause_history = ?
                WHERE id = ?
                """,
                (FWBStatus.PAUSED.value, json.dumps(pause_history), fwb_id)
            )
            logger.info(f"⏸️ Paused FWB: {fwb_id}")
    
    async def resume_fwb(self, fwb_id: str):
        """Resume FWB relationship"""
        db = await self._get_db()
        fwb = await self.get_fwb(fwb_id)
        if fwb:
            pause_history = fwb.pause_history
            pause_history.append({
                'timestamp': time.time(),
                'action': 'resume'
            })
            
            await db.execute(
                """
                UPDATE fwb_relations SET
                    status = ?, pause_history = ?, last_interaction = ?
                WHERE id = ?
                """,
                (FWBStatus.ACTIVE.value, json.dumps(pause_history), time.time(), fwb_id)
            )
            logger.info(f"▶️ Resumed FWB: {fwb_id}")
    
    async def end_fwb(self, fwb_id: str, reason: str):
        """End FWB relationship"""
        db = await self._get_db()
        await db.execute(
            """
            UPDATE fwb_relations SET
                status = ?, ended_at = ?, end_reason = ?
            WHERE id = ?
            """,
            (FWBStatus.ENDED.value, time.time(), reason, fwb_id)
        )
        logger.info(f"💔 Ended FWB: {fwb_id}")
    
    # =========================================================================
    # HTS REPOSITORY
    # =========================================================================
    
    async def create_hts(self, hts: HTSRelation) -> str:
        """Create new HTS relationship"""
        db = await self._get_db()
        await db.execute(
            """
            INSERT INTO hts_relations 
            (id, user_id, role, bot_name, status, created_at, expiry_time,
             last_interaction, chemistry_score, climax_count, intimacy_level,
             total_chats, total_intim, history)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                hts.id, hts.user_id, hts.role, hts.bot_name,
                hts.status.value, hts.created_at, hts.expiry_time,
                hts.last_interaction, hts.chemistry_score, hts.climax_count,
                hts.intimacy_level, hts.total_chats, hts.total_intim,
                json.dumps(hts.history)
            )
        )
        logger.info(f"✅ Created HTS: {hts.id}")
        return hts.id
    
    async def get_hts(self, hts_id: str) -> Optional[HTSRelation]:
        """Get HTS by ID"""
        db = await self._get_db()
        result = await db.fetch_one(
            "SELECT * FROM hts_relations WHERE id = ?",
            (hts_id,)
        )
        return HTSRelation.from_dict(result) if result else None
    
    async def get_user_hts(self, user_id: int, include_expired: bool = False) -> List[HTSRelation]:
        """Get all HTS for user"""
        db = await self._get_db()
        now = time.time()
        
        if include_expired:
            query = "SELECT * FROM hts_relations WHERE user_id = ? ORDER BY last_interaction DESC"
            results = await db.fetch_all(query, (user_id,))
        else:
            query = "SELECT * FROM hts_relations WHERE user_id = ? AND status = 'active' AND expiry_time > ? ORDER BY last_interaction DESC"
            results = await db.fetch_all(query, (user_id, now))
        
        return [HTSRelation.from_dict(r) for r in results]
    
    async def get_top_hts(self, user_id: int, limit: int = 10) -> List[HTSRelation]:
        """Get top HTS by score"""
        db = await self._get_db()
        now = time.time()
        results = await db.fetch_all(
            """
            SELECT *, (chemistry_score * 0.5 + climax_count * 0.3 + intimacy_level * 0.2) as score 
            FROM hts_relations 
            WHERE user_id = ? AND status = 'active' AND expiry_time > ?
            ORDER BY score DESC LIMIT ?
            """,
            (user_id, now, limit)
        )
        return [HTSRelation.from_dict(r) for r in results]
    
    async def update_hts(self, hts: HTSRelation):
        """Update HTS relationship"""
        db = await self._get_db()
        await db.execute(
            """
            UPDATE hts_relations SET
                status = ?, last_interaction = ?, chemistry_score = ?,
                climax_count = ?, intimacy_level = ?, total_chats = ?,
                total_intim = ?, history = ?
            WHERE id = ?
            """,
            (
                hts.status.value, hts.last_interaction, hts.chemistry_score,
                hts.climax_count, hts.intimacy_level, hts.total_chats,
                hts.total_intim, json.dumps(hts.history), hts.id
            )
        )
    
    async def check_expired_hts(self, user_id: Optional[int] = None) -> int:
        """Check and mark expired HTS"""
        db = await self._get_db()
        now = time.time()
        
        if user_id:
            result = await db.execute(
                "UPDATE hts_relations SET status = ? WHERE user_id = ? AND status = 'active' AND expiry_time < ?",
                (HTSStatus.EXPIRED.value, user_id, now)
            )
        else:
            result = await db.execute(
                "UPDATE hts_relations SET status = ? WHERE status = 'active' AND expiry_time < ?",
                (HTSStatus.EXPIRED.value, now)
            )
        
        count = result.rowcount
        if count > 0:
            logger.info(f"⏰ Marked {count} HTS as expired")
        return count
    
    # =========================================================================
    # MEMORY REPOSITORY
    # =========================================================================
    
    async def add_memory(self, memory: Memory) -> int:
        """Add memory"""
        db = await self._get_db()
        cursor = await db.execute(
            """
            INSERT INTO memories 
            (user_id, role, memory_type, content, importance, emotional_tag, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                memory.user_id, memory.role, memory.memory_type.value,
                memory.content, memory.importance, memory.emotional_tag,
                memory.timestamp, json.dumps(memory.metadata)
            )
        )
        return cursor.lastrowid
        
    async def get_user_memories(self, user_id: int, memory_type: Optional[MemoryType] = None, 
                                limit: int = 50) -> List[Memory]:
        """Get memories for user"""
        db = await self._get_db()
        if memory_type:
            results = await db.fetch_all(
                "SELECT * FROM memories WHERE user_id = ? AND memory_type = ? ORDER BY importance DESC LIMIT ?",
                (user_id, memory_type.value, limit)
            )
        else:
            results = await db.fetch_all(
                "SELECT * FROM memories WHERE user_id = ? ORDER BY importance DESC LIMIT ?",
                (user_id, limit)
            )
        return [Memory.from_dict(r) for r in results]
        
    async def get_role_memories(self, user_id: int, role: str, limit: int = 20) -> List[Memory]:
        """Get memories for specific role"""
        db = await self._get_db()
        results = await db.fetch_all(
            "SELECT * FROM memories WHERE user_id = ? AND role = ? ORDER BY importance DESC LIMIT ?",
            (user_id, role, limit)
        )
        return [Memory.from_dict(r) for r in results]
    
    # =========================================================================
    # PREFERENCE REPOSITORY
    # =========================================================================
    
    async def add_preference(self, preference: Preference) -> int:
        """Add or update preference"""
        db = await self._get_db()
        
        existing = await db.fetch_one(
            """
            SELECT * FROM preferences 
            WHERE user_id = ? AND pref_type = ? AND item = ?
            """,
            (preference.user_id, preference.pref_type.value, preference.item)
        )
        
        if existing:
            await db.execute(
                """
                UPDATE preferences SET
                    score = ?, count = count + 1, last_updated = ?
                WHERE id = ?
                """,
                (preference.score, preference.last_updated, existing['id'])
            )
            return existing['id']
        else:
            cursor = await db.execute(
                """
                INSERT INTO preferences 
                (user_id, role, pref_type, item, score, count, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    preference.user_id, preference.role, preference.pref_type.value,
                    preference.item, preference.score, preference.count,
                    preference.last_updated
                )
            )
            return cursor.lastrowid
            
    async def get_top_preferences(self, user_id: int, pref_type: str, 
                                   role: Optional[str] = None, limit: int = 5) -> List[Preference]:
        """Get top preferences by score"""
        db = await self._get_db()
        if role:
            results = await db.fetch_all(
                """
                SELECT * FROM preferences 
                WHERE user_id = ? AND pref_type = ? AND role = ?
                ORDER BY score DESC LIMIT ?
                """,
                (user_id, pref_type, role, limit)
            )
        else:
            results = await db.fetch_all(
                """
                SELECT * FROM preferences 
                WHERE user_id = ? AND pref_type = ?
                ORDER BY score DESC LIMIT ?
                """,
                (user_id, pref_type, limit)
            )
        return [Preference.from_dict(r) for r in results]
    
    # =========================================================================
    # MILESTONE REPOSITORY
    # =========================================================================
    
    async def add_milestone(self, milestone: Milestone) -> int:
        """Add milestone"""
        db = await self._get_db()
        cursor = await db.execute(
            """
            INSERT INTO milestones 
            (user_id, role, milestone_type, description, timestamp, intimacy_level, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                milestone.user_id, milestone.role, milestone.milestone_type.value,
                milestone.description, milestone.timestamp, milestone.intimacy_level,
                json.dumps(milestone.metadata)
            )
        )
        return cursor.lastrowid
        
    async def get_user_milestones(self, user_id: int, limit: int = 20) -> List[Milestone]:
        """Get user milestones"""
        db = await self._get_db()
        results = await db.fetch_all(
            "SELECT * FROM milestones WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
            (user_id, limit)
        )
        return [Milestone.from_dict(r) for r in results]
        
    async def get_role_milestones(self, user_id: int, role: str, limit: int = 10) -> List[Milestone]:
        """Get milestones for specific role"""
        db = await self._get_db()
        results = await db.fetch_all(
            "SELECT * FROM milestones WHERE user_id = ? AND role = ? ORDER BY timestamp DESC LIMIT ?",
            (user_id, role, limit)
        )
        return [Milestone.from_dict(r) for r in results]
    
    # =========================================================================
    # THREESOME REPOSITORY
    # =========================================================================
    
    async def create_threesome_session(self, session: ThreesomeSession) -> str:
        """Create threesome session"""
        db = await self._get_db()
        await db.execute(
            """
            INSERT INTO threesome_sessions 
            (id, user_id, type, status, created_at, started_at, completed_at,
             last_activity, total_messages, climax_count, aftercare_needed,
             current_focus, last_pattern, participants, interactions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session.id, session.user_id, session.type, session.status,
                session.created_at, session.started_at, session.completed_at,
                session.last_activity, session.total_messages, session.climax_count,
                1 if session.aftercare_needed else 0, session.current_focus,
                session.last_pattern, json.dumps(session.participants),
                json.dumps(session.interactions)
            )
        )
        logger.info(f"✅ Created threesome session: {session.id}")
        return session.id
    
    async def get_threesome_session(self, session_id: str) -> Optional[ThreesomeSession]:
        """Get threesome session by ID"""
        db = await self._get_db()
        result = await db.fetch_one(
            "SELECT * FROM threesome_sessions WHERE id = ?",
            (session_id,)
        )
        return ThreesomeSession.from_dict(result) if result else None
    
    async def update_threesome_session(self, session: ThreesomeSession):
        """Update threesome session"""
        db = await self._get_db()
        await db.execute(
            """
            UPDATE threesome_sessions SET
                status = ?, started_at = ?, completed_at = ?, last_activity = ?,
                total_messages = ?, climax_count = ?, aftercare_needed = ?,
                current_focus = ?, last_pattern = ?, participants = ?, interactions = ?
            WHERE id = ?
            """,
            (
                session.status, session.started_at, session.completed_at,
                session.last_activity, session.total_messages, session.climax_count,
                1 if session.aftercare_needed else 0, session.current_focus,
                session.last_pattern, json.dumps(session.participants),
                json.dumps(session.interactions), session.id
            )
        )
    
    # =========================================================================
    # BACKUP REPOSITORY
    # =========================================================================
    
    async def add_backup(self, backup: Backup) -> int:
        """Add backup record"""
        db = await self._get_db()
        cursor = await db.execute(
            """
            INSERT INTO backups 
            (filename, size, created_at, type, status, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                backup.filename, backup.size, backup.created_at,
                backup.type.value, backup.status.value,
                json.dumps(backup.metadata)
            )
        )
        return cursor.lastrowid
        
    async def get_backups(self, limit: int = 10) -> List[Backup]:
        """Get recent backups"""
        db = await self._get_db()
        results = await db.fetch_all(
            "SELECT * FROM backups ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        return [Backup.from_dict(r) for r in results]
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    async def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive user statistics"""
        db = await self._get_db()
        
        # Basic stats
        sessions = await self.fetch_one(
            "SELECT COUNT(*) as count FROM sessions WHERE user_id = ?",
            (user_id,)
        )
        
        messages = await self.fetch_one(
            """
            SELECT COUNT(*) as count FROM conversations c
            JOIN sessions s ON c.session_id = s.id
            WHERE s.user_id = ?
            """,
            (user_id,)
        )
        
        # PDKT stats
        pdkt_active = await self.fetch_one(
            "SELECT COUNT(*) as count FROM pdkt_sessions WHERE user_id = ? AND status IN ('active', 'paused')",
            (user_id,)
        )
        
        pdkt_ended = await self.fetch_one(
            "SELECT COUNT(*) as count FROM pdkt_sessions WHERE user_id = ? AND status = 'ended'",
            (user_id,)
        )
        
        # Mantan stats
        mantan = await self.fetch_one(
            "SELECT COUNT(*) as count FROM mantan WHERE user_id = ?",
            (user_id,)
        )
        
        # FWB stats
        fwb_active = await self.fetch_one(
            "SELECT COUNT(*) as count FROM fwb_relations WHERE user_id = ? AND status = 'active'",
            (user_id,)
        )
        
        # HTS stats
        hts_active = await self.fetch_one(
            "SELECT COUNT(*) as count FROM hts_relations WHERE user_id = ? AND status = 'active'",
            (user_id,)
        )
        
        return {
            'total_sessions': sessions['count'] if sessions else 0,
            'total_messages': messages['count'] if messages else 0,
            'pdkt_active': pdkt_active['count'] if pdkt_active else 0,
            'pdkt_ended': pdkt_ended['count'] if pdkt_ended else 0,
            'total_pdkt': (pdkt_active['count'] if pdkt_active else 0) + (pdkt_ended['count'] if pdkt_ended else 0),
            'total_mantan': mantan['count'] if mantan else 0,
            'fwb_active': fwb_active['count'] if fwb_active else 0,
            'hts_active': hts_active['count'] if hts_active else 0,
        }
    
    async def cleanup_expired_hts(self) -> int:
        """Clean up expired HTS"""
        return await self.check_expired_hts()
    
    async def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Fetch one row"""
        db = await self._get_db()
        return await db.fetch_one(query, params)
    
    async def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """Fetch all rows"""
        db = await self._get_db()
        return await db.fetch_all(query, params)
    
    async def execute(self, query: str, params: tuple = ()):
        """Execute query"""
        db = await self._get_db()
        return await db.execute(query, params)

    # =========================================================================
    # USER SESSION PERMANEN (UNTUK MEMORY PERSISTENT)
    # =========================================================================
    
    async def save_user_session_state(self, user_id: int, session_data: Dict[str, Any]):
        """
        Simpan state session user ke database (permanen)
        
        Args:
            user_id: ID Telegram user
            session_data: Data session (role, bot_name, level, dll)
        """
        db = await self._get_db()
        
        # Cek apakah sudah ada
        existing = await db.fetch_one(
            "SELECT * FROM user_sessions WHERE user_id = ?",
            (user_id,)
        )
        
        now = time.time()
        
        if existing:
            # Update existing
            await db.execute(
                """
                UPDATE user_sessions SET
                    session_id = ?, role = ?, bot_name = ?, rel_type = ?,
                    instance_id = ?, intimacy_level = ?, total_chats = ?,
                    current_location = ?, current_clothing = ?, current_position = ?,
                    relationship_status = ?, updated_at = ?
                WHERE user_id = ?
                """,
                (
                    session_data.get('session_id'),
                    session_data.get('role'),
                    session_data.get('bot_name'),
                    session_data.get('rel_type'),
                    session_data.get('instance_id'),
                    session_data.get('intimacy_level', 1),
                    session_data.get('total_chats', 0),
                    session_data.get('current_location', 'ruang tamu'),
                    session_data.get('current_clothing', 'pakaian biasa'),
                    session_data.get('current_position', 'santai'),
                    session_data.get('relationship_status', 'pdkt'),
                    now,
                    user_id
                )
            )
            logger.debug(f"📝 Updated user session state for user {user_id}")
        else:
            # Insert new
            await db.execute(
                """
                INSERT INTO user_sessions 
                (user_id, session_id, role, bot_name, rel_type, instance_id,
                 intimacy_level, total_chats, current_location, current_clothing,
                 current_position, relationship_status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    session_data.get('session_id'),
                    session_data.get('role'),
                    session_data.get('bot_name'),
                    session_data.get('rel_type'),
                    session_data.get('instance_id'),
                    session_data.get('intimacy_level', 1),
                    session_data.get('total_chats', 0),
                    session_data.get('current_location', 'ruang tamu'),
                    session_data.get('current_clothing', 'pakaian biasa'),
                    session_data.get('current_position', 'santai'),
                    session_data.get('relationship_status', 'pdkt'),
                    now,
                    now
                )
            )
            logger.info(f"✅ Created user session state for user {user_id}")
    
    async def load_user_session_state(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Load state session user dari database
        
        Args:
            user_id: ID Telegram user
            
        Returns:
            Dict session data atau None
        """
        db = await self._get_db()
        
        result = await db.fetch_one(
            "SELECT * FROM user_sessions WHERE user_id = ?",
            (user_id,)
        )
        
        if result:
            return {
                'session_id': result['session_id'],
                'role': result['role'],
                'bot_name': result['bot_name'],
                'rel_type': result['rel_type'],
                'instance_id': result['instance_id'],
                'intimacy_level': result['intimacy_level'],
                'total_chats': result['total_chats'],
                'current_location': result['current_location'],
                'current_clothing': result['current_clothing'],
                'current_position': result['current_position'],
                'relationship_status': result['relationship_status'],
            }
        return None
    
    async def delete_user_session_state(self, user_id: int):
        """
        Hapus state session user dari database (saat /end)
        
        Args:
            user_id: ID Telegram user
        """
        db = await self._get_db()
        await db.execute(
            "DELETE FROM user_sessions WHERE user_id = ?",
            (user_id,)
        )
        logger.info(f"🗑️ Deleted user session state for user {user_id}")
    
    async def get_all_active_sessions(self) -> List[Dict]:
        """Dapatkan semua session aktif dari database"""
        db = await self._get_db()
        results = await db.fetch_all(
            "SELECT * FROM user_sessions ORDER BY updated_at DESC"
        )
        return [dict(r) for r in results]


__all__ = ['Repository']
