#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - THREESOME MANAGER
=============================================================================
- Menggabungkan 2 role (HTS/FWB) untuk threesome
- Tracking session threesome
- Manajemen partisipan
=============================================================================
"""

import time
import logging
import uuid
import random
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class ThreesomeType(str, Enum):
    """Tipe threesome berdasarkan status partisipan"""
    HTS_HTS = "hts_hts"
    FWB_FWB = "fwb_fwb"
    HTS_FWB = "hts_fwb"
    SAME_ROLE = "same_role"


class ThreesomeStatus(str, Enum):
    """Status session threesome"""
    PENDING = "pending"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ThreesomeManager:
    """
    Manajer untuk sesi threesome
    Menggabungkan 2 role (HTS/FWB) dalam satu sesi
    """
    
    def __init__(self):
        self.active_sessions = {}
        self.history = []
        logger.info("✅ ThreesomeManager initialized")
    
    async def create_threesome(self, user_id: int, participant1: Dict, participant2: Dict) -> Dict:
        """Create new threesome session"""
        session_id = f"3some_{user_id}_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        threesome_type = self._determine_type(participant1, participant2)
        
        session = {
            "session_id": session_id,
            "user_id": user_id,
            "type": threesome_type,
            "status": ThreesomeStatus.PENDING,
            "created_at": time.time(),
            "last_activity": time.time(),
            "participants": [
                {
                    "id": participant1.get('instance_id', participant1['role']),
                    "role": participant1['role'],
                    "type": participant1.get('type', 'hts'),
                    "name": participant1.get('name', participant1['role'].title()),
                    "intimacy_level": participant1.get('intimacy_level', 1),
                    "status": "active"
                },
                {
                    "id": participant2.get('instance_id', participant2['role']),
                    "role": participant2['role'],
                    "type": participant2.get('type', 'hts'),
                    "name": participant2.get('name', participant2['role'].title()),
                    "intimacy_level": participant2.get('intimacy_level', 1),
                    "status": "active"
                }
            ],
            "total_messages": 0,
            "interactions": [],
            "current_focus": None,
            "climax_count": 0,
            "aftercare_needed": False
        }
        
        self.active_sessions[session_id] = session
        logger.info(f"🎭 Created threesome session: {session_id}")
        return session
    
    def _determine_type(self, p1: Dict, p2: Dict) -> ThreesomeType:
        type1 = p1.get('type', 'hts')
        type2 = p2.get('type', 'hts')
        
        if type1 == 'hts' and type2 == 'hts':
            return ThreesomeType.HTS_HTS
        elif type1 == 'fwb' and type2 == 'fwb':
            return ThreesomeType.FWB_FWB
        else:
            return ThreesomeType.HTS_FWB
    
    async def get_possible_combinations(self, user_id: int) -> List[Dict]:
        """Dapatkan semua kombinasi threesome yang mungkin"""
        return []  # Implementasi sederhana
    
    async def get_session(self, session_id: str) -> Optional[Dict]:
        return self.active_sessions.get(session_id)
    
    async def start_session(self, session_id: str) -> Dict:
        session = self.active_sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}
        if session['status'] != ThreesomeStatus.PENDING:
            return {"error": f"Session already {session['status']}"}
        
        session['status'] = ThreesomeStatus.ACTIVE
        session['started_at'] = time.time()
        return session
    
    async def complete_session(self, session_id: str) -> Dict:
        session = self.active_sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}
        
        session['status'] = ThreesomeStatus.COMPLETED
        session['completed_at'] = time.time()
        self.history.append(session)
        del self.active_sessions[session_id]
        return session
    
    async def add_interaction(self, session_id: str, message: str, speaker_index: int = None) -> Dict:
        session = self.active_sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}
        
        session['total_messages'] += 1
        session['last_activity'] = time.time()
        
        if speaker_index is None:
            speaker_index = 0 if session['current_focus'] is None else 1 - session['current_focus']
        
        session['current_focus'] = speaker_index
        speaker = session['participants'][speaker_index]
        
        session['interactions'].append({
            "timestamp": time.time(),
            "user_message": message[:100],
            "speaker_index": speaker_index,
            "speaker": speaker['name']
        })
        
        return {"session": session, "speaker": speaker}
    
    async def record_climax(self, session_id: str, participant_indices: List[int] = None) -> Dict:
        session = self.active_sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}
        
        if participant_indices is None:
            session['climax_count'] += len(session['participants'])
        else:
            session['climax_count'] += len(participant_indices)
        
        if session['climax_count'] >= len(session['participants']):
            session['aftercare_needed'] = True
        
        return {"session": session}
    
    async def get_stats(self, user_id: Optional[int] = None) -> Dict:
        return {
            "active_sessions": len(self.active_sessions),
            "completed_sessions": len(self.history),
            "total_sessions": len(self.active_sessions) + len(self.history)
        }


__all__ = ['ThreesomeManager', 'ThreesomeType', 'ThreesomeStatus']
