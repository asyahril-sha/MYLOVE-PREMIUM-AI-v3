#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - DATABASE MODELS
=============================================================================
Data models untuk semua entitas dengan Pydantic validation
Menggabungkan semua model dari V1 dan V2
"""

import time
import json
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum


# =============================================================================
# ENUMS - SEMUA STATUS YANG DIGUNAKAN
# =============================================================================

class RelationshipStatus(str, Enum):
    """Status hubungan"""
    HTS = "hts"
    FWB = "fwb"
    PACAR = "pacar"
    PUTUS = "putus"
    BREAK = "break"
    ENDED = "ended"


class PDKTStatus(str, Enum):
    """Status PDKT"""
    ACTIVE = "active"
    PAUSED = "paused"
    ENDED = "ended"


class PDKTDirection(str, Enum):
    """Arah PDKT"""
    USER_KE_BOT = "user_ke_bot"
    BOT_KE_USER = "bot_ke_user"
    TIMBAL_BALIK = "timbal_balik"
    BINGUNG = "bingung"


class ChemistryLevel(str, Enum):
    """Level chemistry"""
    DINGIN = "dingin"
    BIASA = "biasa"
    HANGAT = "hangat"
    COCOK = "cocok"
    SANGAT_COCOK = "sangat_cocok"
    SOULMATE = "soulmate"


class MoodType(str, Enum):
    """Tipe mood"""
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    TIRED = "tired"
    ROMANTIC = "romantic"
    PLAYFUL = "playful"
    JEALOUS = "jealous"
    SHY = "shy"
    ANGRY = "angry"
    CALM = "calm"
    LONELY = "lonely"
    NOSTALGIC = "nostalgic"


class MemoryType(str, Enum):
    """Tipe memori"""
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    RELATIONSHIP = "relationship"
    COMPACT = "compact"


class MilestoneType(str, Enum):
    """Tipe milestone"""
    FIRST_KISS = "first_kiss"
    FIRST_INTIM = "first_intim"
    FIRST_DATE = "first_date"
    FIRST_FWB = "first_fwb"
    FIRST_HTS = "first_hts"
    BECAME_PACAR = "became_pacar"
    BECAME_FWB = "became_fwb"
    BECAME_MANTAN = "became_mantan"
    LEVEL_UP = "level_up"
    AFTERCARE = "aftercare"
    RESET = "reset"
    BREAK_UP = "break_up"
    CAN_INTIM = "can_intim"
    AFTERCARE_READY = "aftercare_ready"


class SessionStatus(str, Enum):
    """Status session"""
    ACTIVE = "active"
    CLOSED = "closed"
    EXPIRED = "expired"


class FWBStatus(str, Enum):
    """Status FWB"""
    ACTIVE = "active"
    PAUSED = "paused"
    ENDED = "ended"


class HTSStatus(str, Enum):
    """Status HTS"""
    ACTIVE = "active"
    EXPIRED = "expired"


class MantanStatus(str, Enum):
    """Status mantan"""
    PUTUS = "putus"
    FWB_REQUESTED = "fwb_requested"
    FWB_ACCEPTED = "fwb_accepted"
    FWB_DECLINED = "fwb_declined"
    FWB_ENDED = "fwb_ended"


class BackupType(str, Enum):
    """Tipe backup"""
    AUTO = "auto"
    MANUAL = "manual"


class BackupStatus(str, Enum):
    """Status backup"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class PreferenceType(str, Enum):
    """Tipe preferensi"""
    POSITION = "position"
    AREA = "area"
    ACTIVITY = "activity"
    LOCATION = "location"
    ROLE = "role"
    FOREPLAY = "foreplay"
    AFTERCARE = "aftercare"


# =============================================================================
# CONSTANTS UNTUK PTB CONVERSATION HANDLER
# =============================================================================
class Constants:
    """Constants untuk PTB ConversationHandler"""
    
    # Conversation States
    SELECTING_ROLE = 1
    SELECTING_BOT_NAME = 2
    SELECTING_BOT_ROLE = 3
    SELECTING_DOMINANCE = 4
    SELECTING_PERSONALITY = 5
    SELECTING_APPEARANCE = 6
    CONFIRMATION = 7
    CHATTING = 8
    SELECTING_ACTION = 9
    SELECTING_LOCATION = 10
    SELECTING_CLOTHING = 11
    SELECTING_ACTIVITY = 12
    AWAITING_RESPONSE = 13
    CONFIRM_END = 14
    CONFIRM_CLOSE = 15
    CONFIRM_BROADCAST = 16
    SELECTING_PDKT = 17
    SELECTING_MANTAN = 18
    SELECTING_FWB = 19
    
    # Roles
    ROLE_IPAR = "ipar"
    ROLE_TEMAN_KANTOR = "teman_kantor"
    ROLE_JANDA = "janda"
    ROLE_PELAKOR = "pelakor"
    ROLE_ISTRI_ORANG = "istri_orang"
    ROLE_PDKT = "pdkt"
    ROLE_SEPUPU = "sepupu"
    ROLE_TEMAN_SMA = "teman_sma"
    ROLE_MANTAN = "mantan"
    
    # Callback patterns
    AGREE_18 = "agree_18"
    UNPAUSE = "unpause"
    NEW = "new"


# =============================================================================
# USER MODEL
# =============================================================================

class User(BaseModel):
    """Model untuk user Telegram"""
    id: Optional[int] = None
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: float = Field(default_factory=time.time)
    last_active: float = Field(default_factory=time.time)
    total_interactions: int = 0
    preferences: Dict[str, Any] = Field(default_factory=dict)
    settings: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('telegram_id')
    def validate_telegram_id(cls, v):
        if v <= 0:
            raise ValueError('telegram_id must be positive')
        return v
    
    def to_dict(self) -> Dict:
        return {
            'telegram_id': self.telegram_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at,
            'last_active': self.last_active,
            'total_interactions': self.total_interactions,
            'preferences': json.dumps(self.preferences),
            'settings': json.dumps(self.settings)
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        return cls(
            id=data.get('id'),
            telegram_id=data['telegram_id'],
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            created_at=data.get('created_at', time.time()),
            last_active=data.get('last_active', time.time()),
            total_interactions=data.get('total_interactions', 0),
            preferences=json.loads(data.get('preferences', '{}')),
            settings=json.loads(data.get('settings', '{}'))
        )


# =============================================================================
# SESSION MODEL
# =============================================================================

class Session(BaseModel):
    """Model untuk session chat dengan nama bot permanent"""
    id: str
    user_id: int
    bot_name: str
    role: str
    status: SessionStatus = SessionStatus.ACTIVE
    start_time: float = Field(default_factory=time.time)
    end_time: Optional[float] = None
    last_message_time: float = Field(default_factory=time.time)
    total_messages: int = 0
    intimacy_level: int = 1
    location: Optional[str] = None
    summary: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('role')
    def validate_role(cls, v):
        valid_roles = ['ipar', 'janda', 'pelakor', 'istri_orang', 
                      'pdkt', 'sepupu', 'teman_kantor', 'teman_sma', 'mantan']
        if v not in valid_roles:
            raise ValueError(f'role must be one of {valid_roles}')
        return v
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'bot_name': self.bot_name,
            'role': self.role,
            'status': self.status.value,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'last_message_time': self.last_message_time,
            'total_messages': self.total_messages,
            'intimacy_level': self.intimacy_level,
            'location': self.location,
            'summary': self.summary,
            'metadata': json.dumps(self.metadata)
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Session':
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            bot_name=data.get('bot_name', 'Aurora'),
            role=data['role'],
            status=SessionStatus(data.get('status', 'active')),
            start_time=data.get('start_time', time.time()),
            end_time=data.get('end_time'),
            last_message_time=data.get('last_message_time', time.time()),
            total_messages=data.get('total_messages', 0),
            intimacy_level=data.get('intimacy_level', 1),
            location=data.get('location'),
            summary=data.get('summary'),
            metadata=json.loads(data.get('metadata', '{}'))
        )


# =============================================================================
# CONVERSATION MODEL
# =============================================================================

class Conversation(BaseModel):
    """Model untuk pesan dalam session"""
    id: Optional[int] = None
    session_id: str
    timestamp: float = Field(default_factory=time.time)
    user_message: str
    bot_response: str
    intent: Optional[str] = None
    mood: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            'session_id': self.session_id,
            'timestamp': self.timestamp,
            'user_message': self.user_message,
            'bot_response': self.bot_response,
            'intent': self.intent,
            'mood': self.mood
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Conversation':
        return cls(
            id=data.get('id'),
            session_id=data['session_id'],
            timestamp=data.get('timestamp', time.time()),
            user_message=data['user_message'],
            bot_response=data['bot_response'],
            intent=data.get('intent'),
            mood=data.get('mood')
        )


# =============================================================================
# PDKT SESSION MODEL
# =============================================================================

class PDKTSession(BaseModel):
    """Model untuk session PDKT Natural"""
    id: str
    user_id: int
    role: str
    bot_name: str
    status: PDKTStatus = PDKTStatus.ACTIVE
    direction: PDKTDirection
    chemistry_score: float = 50.0
    chemistry_level: ChemistryLevel = ChemistryLevel.BIASA
    mood: MoodType = MoodType.CALM
    level: int = 1
    total_duration: float = 0.0
    total_chats: int = 0
    total_intim: int = 0
    total_climax: int = 0
    created_at: float = Field(default_factory=time.time)
    last_interaction: float = Field(default_factory=time.time)
    paused_at: Optional[float] = None
    ended_at: Optional[float] = None
    end_reason: Optional[str] = None
    inner_thoughts: List[str] = Field(default_factory=list)
    milestones: List[Dict] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'role': self.role,
            'bot_name': self.bot_name,
            'status': self.status.value,
            'direction': self.direction.value,
            'chemistry_score': self.chemistry_score,
            'chemistry_level': self.chemistry_level.value,
            'mood': self.mood.value,
            'level': self.level,
            'total_duration': self.total_duration,
            'total_chats': self.total_chats,
            'total_intim': self.total_intim,
            'total_climax': self.total_climax,
            'created_at': self.created_at,
            'last_interaction': self.last_interaction,
            'paused_at': self.paused_at,
            'ended_at': self.ended_at,
            'end_reason': self.end_reason,
            'inner_thoughts': json.dumps(self.inner_thoughts),
            'milestones': json.dumps(self.milestones),
            'metadata': json.dumps(self.metadata)
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PDKTSession':
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            role=data['role'],
            bot_name=data['bot_name'],
            status=PDKTStatus(data.get('status', 'active')),
            direction=PDKTDirection(data.get('direction', 'user_ke_bot')),
            chemistry_score=data.get('chemistry_score', 50.0),
            chemistry_level=ChemistryLevel(data.get('chemistry_level', 'biasa')),
            mood=MoodType(data.get('mood', 'calm')),
            level=data.get('level', 1),
            total_duration=data.get('total_duration', 0.0),
            total_chats=data.get('total_chats', 0),
            total_intim=data.get('total_intim', 0),
            total_climax=data.get('total_climax', 0),
            created_at=data.get('created_at', time.time()),
            last_interaction=data.get('last_interaction', time.time()),
            paused_at=data.get('paused_at'),
            ended_at=data.get('ended_at'),
            end_reason=data.get('end_reason'),
            inner_thoughts=json.loads(data.get('inner_thoughts', '[]')),
            milestones=json.loads(data.get('milestones', '[]')),
            metadata=json.loads(data.get('metadata', '{}'))
        )


# =============================================================================
# MANTAN MODEL
# =============================================================================

class Mantan(BaseModel):
    """Model untuk mantan dari PDKT"""
    id: str
    user_id: int
    pdkt_id: str
    bot_name: str
    role: str
    status: MantanStatus = MantanStatus.PUTUS
    putus_time: float = Field(default_factory=time.time)
    putus_reason: str
    chemistry_history: List[Dict] = Field(default_factory=list)
    milestones: List[Dict] = Field(default_factory=list)
    total_chats: int = 0
    total_intim: int = 0
    total_climax: int = 0
    first_kiss_time: Optional[float] = None
    first_intim_time: Optional[float] = None
    become_pacar_time: Optional[float] = None
    last_chat_time: float = Field(default_factory=time.time)
    fwb_requests: List[Dict] = Field(default_factory=list)
    fwb_start_time: Optional[float] = None
    fwb_end_time: Optional[float] = None
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'pdkt_id': self.pdkt_id,
            'bot_name': self.bot_name,
            'role': self.role,
            'status': self.status.value,
            'putus_time': self.putus_time,
            'putus_reason': self.putus_reason,
            'chemistry_history': json.dumps(self.chemistry_history),
            'milestones': json.dumps(self.milestones),
            'total_chats': self.total_chats,
            'total_intim': self.total_intim,
            'total_climax': self.total_climax,
            'first_kiss_time': self.first_kiss_time,
            'first_intim_time': self.first_intim_time,
            'become_pacar_time': self.become_pacar_time,
            'last_chat_time': self.last_chat_time,
            'fwb_requests': json.dumps(self.fwb_requests),
            'fwb_start_time': self.fwb_start_time,
            'fwb_end_time': self.fwb_end_time
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Mantan':
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            pdkt_id=data['pdkt_id'],
            bot_name=data['bot_name'],
            role=data['role'],
            status=MantanStatus(data.get('status', 'putus')),
            putus_time=data.get('putus_time', time.time()),
            putus_reason=data['putus_reason'],
            chemistry_history=json.loads(data.get('chemistry_history', '[]')),
            milestones=json.loads(data.get('milestones', '[]')),
            total_chats=data.get('total_chats', 0),
            total_intim=data.get('total_intim', 0),
            total_climax=data.get('total_climax', 0),
            first_kiss_time=data.get('first_kiss_time'),
            first_intim_time=data.get('first_intim_time'),
            become_pacar_time=data.get('become_pacar_time'),
            last_chat_time=data.get('last_chat_time', time.time()),
            fwb_requests=json.loads(data.get('fwb_requests', '[]')),
            fwb_start_time=data.get('fwb_start_time'),
            fwb_end_time=data.get('fwb_end_time')
        )


# =============================================================================
# FWB RELATION MODEL
# =============================================================================

class FWBRelation(BaseModel):
    """Model untuk hubungan FWB"""
    id: str
    user_id: int
    mantan_id: str
    bot_name: str
    role: str
    status: FWBStatus = FWBStatus.ACTIVE
    created_at: float = Field(default_factory=time.time)
    last_interaction: float = Field(default_factory=time.time)
    chemistry_score: float = 50.0
    climax_count: int = 0
    intim_count: int = 0
    total_chats: int = 0
    pause_history: List[Dict] = Field(default_factory=list)
    ended_at: Optional[float] = None
    end_reason: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'mantan_id': self.mantan_id,
            'bot_name': self.bot_name,
            'role': self.role,
            'status': self.status.value,
            'created_at': self.created_at,
            'last_interaction': self.last_interaction,
            'chemistry_score': self.chemistry_score,
            'climax_count': self.climax_count,
            'intim_count': self.intim_count,
            'total_chats': self.total_chats,
            'pause_history': json.dumps(self.pause_history),
            'ended_at': self.ended_at,
            'end_reason': self.end_reason
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'FWBRelation':
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            mantan_id=data['mantan_id'],
            bot_name=data['bot_name'],
            role=data['role'],
            status=FWBStatus(data.get('status', 'active')),
            created_at=data.get('created_at', time.time()),
            last_interaction=data.get('last_interaction', time.time()),
            chemistry_score=data.get('chemistry_score', 50.0),
            climax_count=data.get('climax_count', 0),
            intim_count=data.get('intim_count', 0),
            total_chats=data.get('total_chats', 0),
            pause_history=json.loads(data.get('pause_history', '[]')),
            ended_at=data.get('ended_at'),
            end_reason=data.get('end_reason')
        )


# =============================================================================
# HTS RELATION MODEL
# =============================================================================

class HTSRelation(BaseModel):
    """Model untuk hubungan HTS (dari NON-PDKT)"""
    id: str
    user_id: int
    role: str
    bot_name: str
    status: HTSStatus = HTSStatus.ACTIVE
    created_at: float = Field(default_factory=time.time)
    expiry_time: float
    last_interaction: float = Field(default_factory=time.time)
    chemistry_score: float = 50.0
    climax_count: int = 0
    intimacy_level: int = 7
    total_chats: int = 0
    total_intim: int = 0
    history: List[Dict] = Field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'role': self.role,
            'bot_name': self.bot_name,
            'status': self.status.value,
            'created_at': self.created_at,
            'expiry_time': self.expiry_time,
            'last_interaction': self.last_interaction,
            'chemistry_score': self.chemistry_score,
            'climax_count': self.climax_count,
            'intimacy_level': self.intimacy_level,
            'total_chats': self.total_chats,
            'total_intim': self.total_intim,
            'history': json.dumps(self.history)
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'HTSRelation':
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            role=data['role'],
            bot_name=data['bot_name'],
            status=HTSStatus(data.get('status', 'active')),
            created_at=data.get('created_at', time.time()),
            expiry_time=data['expiry_time'],
            last_interaction=data.get('last_interaction', time.time()),
            chemistry_score=data.get('chemistry_score', 50.0),
            climax_count=data.get('climax_count', 0),
            intimacy_level=data.get('intimacy_level', 7),
            total_chats=data.get('total_chats', 0),
            total_intim=data.get('total_intim', 0),
            history=json.loads(data.get('history', '[]'))
        )


# =============================================================================
# MEMORY MODEL
# =============================================================================

class Memory(BaseModel):
    """Model untuk memori (episodic/semantic)"""
    id: Optional[int] = None
    user_id: int
    role: Optional[str] = None
    memory_type: MemoryType
    content: str
    importance: float = 0.5
    emotional_tag: Optional[str] = None
    timestamp: float = Field(default_factory=time.time)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('importance')
    def validate_importance(cls, v):
        if v < 0 or v > 1:
            raise ValueError('importance must be between 0 and 1')
        return v
    
    def to_dict(self) -> Dict:
        return {
            'user_id': self.user_id,
            'role': self.role,
            'memory_type': self.memory_type.value,
            'content': self.content,
            'importance': self.importance,
            'emotional_tag': self.emotional_tag,
            'timestamp': self.timestamp,
            'metadata': json.dumps(self.metadata)
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Memory':
        return cls(
            id=data.get('id'),
            user_id=data['user_id'],
            role=data.get('role'),
            memory_type=MemoryType(data['memory_type']),
            content=data['content'],
            importance=data.get('importance', 0.5),
            emotional_tag=data.get('emotional_tag'),
            timestamp=data.get('timestamp', time.time()),
            metadata=json.loads(data.get('metadata', '{}'))
        )


# =============================================================================
# PREFERENCE MODEL
# =============================================================================

class Preference(BaseModel):
    """Model untuk preferensi user"""
    id: Optional[int] = None
    user_id: int
    role: Optional[str] = None
    pref_type: PreferenceType
    item: str
    score: float = 0.5
    count: int = 1
    last_updated: float = Field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            'user_id': self.user_id,
            'role': self.role,
            'pref_type': self.pref_type.value,
            'item': self.item,
            'score': self.score,
            'count': self.count,
            'last_updated': self.last_updated
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Preference':
        return cls(
            id=data.get('id'),
            user_id=data['user_id'],
            role=data.get('role'),
            pref_type=PreferenceType(data['pref_type']),
            item=data['item'],
            score=data.get('score', 0.5),
            count=data.get('count', 1),
            last_updated=data.get('last_updated', time.time())
        )


# =============================================================================
# MILESTONE MODEL
# =============================================================================

class Milestone(BaseModel):
    """Model untuk milestone dalam hubungan"""
    id: Optional[int] = None
    user_id: int
    role: Optional[str] = None
    milestone_type: MilestoneType
    description: Optional[str] = None
    timestamp: float = Field(default_factory=time.time)
    intimacy_level: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'user_id': self.user_id,
            'role': self.role,
            'milestone_type': self.milestone_type.value,
            'description': self.description,
            'timestamp': self.timestamp,
            'intimacy_level': self.intimacy_level,
            'metadata': json.dumps(self.metadata)
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Milestone':
        return cls(
            id=data.get('id'),
            user_id=data['user_id'],
            role=data.get('role'),
            milestone_type=MilestoneType(data['milestone_type']),
            description=data.get('description'),
            timestamp=data.get('timestamp', time.time()),
            intimacy_level=data.get('intimacy_level'),
            metadata=json.loads(data.get('metadata', '{}'))
        )


# =============================================================================
# BACKUP MODEL
# =============================================================================

class Backup(BaseModel):
    """Model untuk history backup"""
    id: Optional[int] = None
    filename: str
    size: Optional[int] = None
    created_at: float = Field(default_factory=time.time)
    type: BackupType = BackupType.AUTO
    status: BackupStatus = BackupStatus.COMPLETED
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'filename': self.filename,
            'size': self.size,
            'created_at': self.created_at,
            'type': self.type.value,
            'status': self.status.value,
            'metadata': json.dumps(self.metadata)
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Backup':
        return cls(
            id=data.get('id'),
            filename=data['filename'],
            size=data.get('size'),
            created_at=data.get('created_at', time.time()),
            type=BackupType(data.get('type', 'auto')),
            status=BackupStatus(data.get('status', 'completed')),
            metadata=json.loads(data.get('metadata', '{}'))
        )


# =============================================================================
# THREESOME MODELS
# =============================================================================

class ThreesomeParticipant(BaseModel):
    """Model untuk partisipan threesome"""
    id: Optional[int] = None
    threesome_session_id: str
    user_id: int
    bot_name: str
    role: str
    instance_id: Optional[str] = None
    participant_type: str
    name: str
    intimacy_level: int = 1
    status: str = "active"
    
    def to_dict(self) -> Dict:
        return {
            'threesome_session_id': self.threesome_session_id,
            'user_id': self.user_id,
            'bot_name': self.bot_name,
            'role': self.role,
            'instance_id': self.instance_id,
            'participant_type': self.participant_type,
            'name': self.name,
            'intimacy_level': self.intimacy_level,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ThreesomeParticipant':
        return cls(
            id=data.get('id'),
            threesome_session_id=data['threesome_session_id'],
            user_id=data['user_id'],
            bot_name=data.get('bot_name', 'Aurora'),
            role=data['role'],
            instance_id=data.get('instance_id'),
            participant_type=data['participant_type'],
            name=data['name'],
            intimacy_level=data.get('intimacy_level', 1),
            status=data.get('status', 'active')
        )


class ThreesomeSession(BaseModel):
    """Model untuk session threesome"""
    id: str
    user_id: int
    type: str
    status: str = "active"
    created_at: float = Field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    last_activity: float = Field(default_factory=time.time)
    total_messages: int = 0
    climax_count: int = 0
    aftercare_needed: bool = False
    current_focus: Optional[int] = None
    last_pattern: Optional[str] = None
    participants: List[Dict] = Field(default_factory=list)
    interactions: List[Dict] = Field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'status': self.status,
            'created_at': self.created_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'last_activity': self.last_activity,
            'total_messages': self.total_messages,
            'climax_count': self.climax_count,
            'aftercare_needed': self.aftercare_needed,
            'current_focus': self.current_focus,
            'last_pattern': self.last_pattern,
            'participants': json.dumps(self.participants),
            'interactions': json.dumps(self.interactions[-50:])
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ThreesomeSession':
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            type=data['type'],
            status=data.get('status', 'active'),
            created_at=data.get('created_at', time.time()),
            started_at=data.get('started_at'),
            completed_at=data.get('completed_at'),
            last_activity=data.get('last_activity', time.time()),
            total_messages=data.get('total_messages', 0),
            climax_count=data.get('climax_count', 0),
            aftercare_needed=data.get('aftercare_needed', False),
            current_focus=data.get('current_focus'),
            last_pattern=data.get('last_pattern'),
            participants=json.loads(data.get('participants', '[]')),
            interactions=json.loads(data.get('interactions', '[]'))
        )

# =============================================================================
# RELATIONSHIP MODEL (V1 COMPATIBILITY)
# =============================================================================

class Relationship(BaseModel):
    """Model untuk hubungan (HTS/FWB/Pacar) - V1 compatibility"""
    id: Optional[int] = None
    user_id: int
    bot_name: str = "Aurora"
    role: str
    instance_id: Optional[str] = None
    status: str = "hts"
    intimacy_level: int = 1
    total_interactions: int = 0
    total_intim_sessions: int = 0
    total_climax: int = 0
    created_at: float = Field(default_factory=time.time)
    last_interaction: float = Field(default_factory=time.time)
    preferences: Dict[str, Any] = Field(default_factory=dict)
    milestones: List[Dict] = Field(default_factory=list)
    history: List[Dict] = Field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'user_id': self.user_id,
            'bot_name': self.bot_name,
            'role': self.role,
            'instance_id': self.instance_id,
            'status': self.status,
            'intimacy_level': self.intimacy_level,
            'total_interactions': self.total_interactions,
            'total_intim_sessions': self.total_intim_sessions,
            'total_climax': self.total_climax,
            'created_at': self.created_at,
            'last_interaction': self.last_interaction,
            'preferences': json.dumps(self.preferences),
            'milestones': json.dumps(self.milestones),
            'history': json.dumps(self.history)
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Relationship':
        return cls(
            id=data.get('id'),
            user_id=data['user_id'],
            bot_name=data.get('bot_name', 'Aurora'),
            role=data['role'],
            instance_id=data.get('instance_id'),
            status=data.get('status', 'hts'),
            intimacy_level=data.get('intimacy_level', 1),
            total_interactions=data.get('total_interactions', 0),
            total_intim_sessions=data.get('total_intim_sessions', 0),
            total_climax=data.get('total_climax', 0),
            created_at=data.get('created_at', time.time()),
            last_interaction=data.get('last_interaction', time.time()),
            preferences=json.loads(data.get('preferences', '{}')),
            milestones=json.loads(data.get('milestones', '[]')),
            history=json.loads(data.get('history', '[]'))
        )
        
# =============================================================================
# USER SESSION PERMANEN (UNTUK MEMORY PERSISTENT)
# =============================================================================

class UserSession(BaseModel):
    """Model untuk session permanen user (disimpan di database)"""
    id: Optional[int] = None
    user_id: int
    session_id: Optional[str] = None
    role: Optional[str] = None
    bot_name: Optional[str] = None
    rel_type: Optional[str] = None
    instance_id: Optional[str] = None
    intimacy_level: int = 1
    total_chats: int = 0
    current_location: str = "ruang tamu"
    current_clothing: str = "pakaian biasa"
    current_position: str = "santai"
    relationship_status: str = "pdkt"
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            'user_id': self.user_id,
            'session_id': self.session_id,
            'role': self.role,
            'bot_name': self.bot_name,
            'rel_type': self.rel_type,
            'instance_id': self.instance_id,
            'intimacy_level': self.intimacy_level,
            'total_chats': self.total_chats,
            'current_location': self.current_location,
            'current_clothing': self.current_clothing,
            'current_position': self.current_position,
            'relationship_status': self.relationship_status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserSession':
        return cls(
            id=data.get('id'),
            user_id=data['user_id'],
            session_id=data.get('session_id'),
            role=data.get('role'),
            bot_name=data.get('bot_name'),
            rel_type=data.get('rel_type'),
            instance_id=data.get('instance_id'),
            intimacy_level=data.get('intimacy_level', 1),
            total_chats=data.get('total_chats', 0),
            current_location=data.get('current_location', 'ruang tamu'),
            current_clothing=data.get('current_clothing', 'pakaian biasa'),
            current_position=data.get('current_position', 'santai'),
            relationship_status=data.get('relationship_status', 'pdkt'),
            created_at=data.get('created_at', time.time()),
            updated_at=data.get('updated_at', time.time())
        )

# =============================================================================
# EXPORT ALL MODELS
# =============================================================================

__all__ = [
    # Enums
    'RelationshipStatus',
    'PDKTStatus',
    'PDKTDirection',
    'ChemistryLevel',
    'MoodType',
    'MemoryType',
    'MilestoneType',
    'SessionStatus',
    'FWBStatus',
    'HTSStatus',
    'MantanStatus',
    'BackupType',
    'BackupStatus',
    'PreferenceType',
    
    # Constants
    'Constants',
    
    # Main Models
    'User',
    'Session',
    'Conversation',
    'PDKTSession',
    'Mantan',
    'FWBRelation',
    'HTSRelation',
    'Memory',
    'Preference',
    'Milestone',
    'Backup',
    
    # Threesome Models
    'ThreesomeParticipant',
    'ThreesomeSession',

    # User
    'UserSession',
]
