# config.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - KONFIGURASI UTAMA (V3 ENHANCED)
=============================================================================
"""

import os
import secrets
from typing import Optional, Dict, Any, List
from pathlib import Path

# ===== IMPORT PYDANTIC YANG BENAR =====
from pydantic import Field, validator, BaseModel
from pydantic_settings import BaseSettings


# =============================================================================
# DATABASE SETTINGS
# =============================================================================
class DatabaseSettings(BaseModel):
    """Konfigurasi database"""
    type: str = Field("sqlite", env='DB_TYPE')
    path: Path = Field(Path("data/mylove.db"), env='DB_PATH')
    pool_size: int = Field(5, env='DB_POOL_SIZE')
    timeout: int = Field(30, env='DB_TIMEOUT')
    
    @property
    def url(self) -> str:
        return f"sqlite+aiosqlite:///{self.path}"


# =============================================================================
# AI SETTINGS
# =============================================================================
class AISettings(BaseModel):
    """Konfigurasi AI DeepSeek"""
    temperature: float = Field(0.9, env='AI_TEMPERATURE')
    max_tokens: int = Field(2000, env='AI_MAX_TOKENS')
    timeout: int = Field(30, env='AI_TIMEOUT')
    model: str = Field("deepseek-chat", env='AI_MODEL')
    
    min_message_length: int = Field(500, env='MIN_MESSAGE_LENGTH')
    max_message_length: int = Field(2000, env='MAX_MESSAGE_LENGTH')


# =============================================================================
# WEBHOOK SETTINGS
# =============================================================================
class WebhookSettings(BaseModel):
    """Konfigurasi webhook"""
    url: Optional[str] = Field(None, env='WEBHOOK_URL')
    port: int = Field(8080, env='PORT')
    path: str = Field("/webhook", env='WEBHOOK_PATH')
    secret_token: Optional[str] = Field(None, env='WEBHOOK_SECRET')
    max_retries: int = Field(5, env='WEBHOOK_MAX_RETRIES')
    enable_polling_fallback: bool = Field(True, env='ENABLE_POLLING_FALLBACK')


# =============================================================================
# INTIMACY SETTINGS
# =============================================================================
class IntimacySettings(BaseModel):
    """Sistem level intimacy time-based"""
    reset_level: int = Field(7, env='RESET_LEVEL')
    max_level: int = Field(12, env='MAX_LEVEL')
    aftercare_enabled: bool = Field(True, env='AFTERCARE_ENABLED')
    
    level_targets: Dict[int, int] = {
        1: 0, 2: 5, 3: 12, 4: 20, 5: 30, 6: 42,
        7: 60, 8: 75, 9: 90, 10: 105, 11: 120, 12: 135
    }


# =============================================================================
# PDKT SETTINGS
# =============================================================================
class PDKTSettings(BaseModel):
    """Sistem PDKT Natural"""
    chemistry_decay_rate: float = Field(0.01, env='CHEMISTRY_DECAY')
    mood_evolution_rate: float = Field(0.1, env='MOOD_EVOLUTION')
    dream_chance: float = Field(0.3, env='DREAM_CHANCE')
    sixth_sense_chance: float = Field(0.15, env='SIXTH_SENSE_CHANCE')


# =============================================================================
# SESSION SETTINGS
# =============================================================================
class SessionSettings(BaseModel):
    """Sistem session"""
    id_format: str = "MYLOVE-{bot_name}-{role}-{user_id}-{date}-{seq:03d}"
    storage_type: str = Field("sqlite+json", env='SESSION_STORAGE')
    session_dir: Path = Field(Path("data/sessions"), env='SESSION_DIR')
    retention_days: int = Field(30, env='SESSION_RETENTION_DAYS')
    auto_delete: bool = Field(True, env='SESSION_AUTO_DELETE')


# =============================================================================
# MEMORY SETTINGS (V3 ENHANCED)
# =============================================================================
class MemorySettings(BaseModel):
    """Sistem memory dengan Hippocampus dan V3 enhancements"""
    vector_db_dir: Path = Field(Path("data/vector_db"), env='VECTOR_DB_DIR')
    working_memory_capacity: int = Field(20, env='WORKING_MEMORY_CAPACITY')
    working_memory_expire: int = Field(86400, env='WORKING_MEMORY_EXPIRE')
    consolidation_interval: int = Field(3600, env='CONSOLIDATION_INTERVAL')
    forgetting_threshold: float = Field(0.3, env='FORGETTING_THRESHOLD')
    # V3: Memory directory untuk emotional memory
    memory_dir: Path = Field(Path("data/memory"), env='MEMORY_DIR')


# =============================================================================
# EMOTIONAL SETTINGS (V3 NEW)
# =============================================================================
class EmotionalSettings(BaseModel):
    """Konfigurasi Emotional Flow System V3"""
    arousal_decay_rate: float = Field(0.02, env='AROUSAL_DECAY_RATE')
    empathy_factor_base: float = Field(0.6, env='EMPATHY_FACTOR_BASE')
    arousal_threshold_horny: int = Field(70, env='AROUSAL_THRESHOLD_HORNY')
    arousal_threshold_climax: int = Field(90, env='AROUSAL_THRESHOLD_CLIMAX')
    mood_change_probability: float = Field(0.05, env='MOOD_CHANGE_PROBABILITY')


# =============================================================================
# ROLE SETTINGS (V3 NEW)
# =============================================================================
class RoleSettings(BaseModel):
    """Konfigurasi Role Behavior System V3"""
    ipar_jealousy_factor: float = Field(0.3, env='IPAR_JEALOUSY_FACTOR')
    teman_kantor_risk_factor: float = Field(0.4, env='TEMAN_KANTOR_RISK_FACTOR')
    janda_experience_factor: float = Field(0.8, env='JANDA_EXPERIENCE_FACTOR')
    pelakor_aggression_factor: float = Field(0.9, env='PELAKOR_AGGRESSION_FACTOR')
    istri_orang_guilt_factor: float = Field(0.7, env='ISTRI_ORANG_GUILT_FACTOR')
    pdkt_shyness_factor: float = Field(0.6, env='PDKT_SHYNESS_FACTOR')
    sepupu_curiosity_factor: float = Field(0.7, env='SEPUPU_CURIOSITY_FACTOR')
    teman_sma_nostalgia_factor: float = Field(0.6, env='TEMAN_SMA_NOSTALGIA_FACTOR')
    mantan_knowledge_factor: float = Field(0.8, env='MANTAN_KNOWLEDGE_FACTOR')


# =============================================================================
# PERFORMANCE SETTINGS (V3 NEW)
# =============================================================================
class PerformanceSettings(BaseModel):
    """Konfigurasi Performance Monitoring V3"""
    target_response_time: float = Field(3.0, env='TARGET_RESPONSE_TIME')
    max_memory_mb: int = Field(500, env='MAX_MEMORY_MB')
    slow_operation_threshold: float = Field(5.0, env='SLOW_OPERATION_THRESHOLD')
    cache_ttl: int = Field(300, env='CACHE_TTL')


# =============================================================================
# BACKUP SETTINGS
# =============================================================================
class BackupSettings(BaseModel):
    """Sistem backup otomatis"""
    enabled: bool = Field(True, env='BACKUP_ENABLED')
    interval: int = Field(3600, env='BACKUP_INTERVAL')
    retention_days: int = Field(7, env='BACKUP_RETENTION_DAYS')
    backup_dir: Path = Field(Path("data/backups"), env='BACKUP_DIR')
    s3_bucket: Optional[str] = Field(None, env='BACKUP_S3_BUCKET')


# =============================================================================
# LOGGING SETTINGS
# =============================================================================
class LoggingSettings(BaseModel):
    """Konfigurasi logging"""
    level: str = Field("INFO", env='LOG_LEVEL')
    log_dir: Path = Field(Path("data/logs"), env='LOG_DIR')
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


# =============================================================================
# FEATURE SETTINGS
# =============================================================================
class FeatureSettings(BaseModel):
    """Feature toggles"""
    sexual_enabled: bool = Field(True, env='SEXUAL_CONTENT_ENABLED')
    public_risk_enabled: bool = Field(True, env='PUBLIC_RISK_ENABLED')
    bot_initiative_enabled: bool = Field(True, env='BOT_INITIATIVE_ENABLED')
    aftercare_enabled: bool = Field(True, env='AFTERCARE_ENABLED')
    threesome_enabled: bool = Field(True, env='THREESOME_ENABLED')
    memory_enabled: bool = Field(True, env='MEMORY_ENABLED')
    # V3: New feature toggles
    emotional_flow_enabled: bool = Field(True, env='EMOTIONAL_FLOW_ENABLED')
    spatial_awareness_enabled: bool = Field(True, env='SPATIAL_AWARENESS_ENABLED')
    role_behavior_enabled: bool = Field(True, env='ROLE_BEHAVIOR_ENABLED')


# =============================================================================
# MAIN SETTINGS CLASS
# =============================================================================
class Settings(BaseSettings):
    """
    MYLOVE PREMIUM AI - Main Settings V3
    """
    
    # API Keys
    deepseek_api_key: str = Field(..., env='DEEPSEEK_API_KEY')
    telegram_token: str = Field(..., env='TELEGRAM_TOKEN')
    admin_id: int = Field(..., env='ADMIN_ID')
    
    # Component settings
    database: DatabaseSettings = DatabaseSettings()
    ai: AISettings = AISettings()
    webhook: WebhookSettings = WebhookSettings()
    intimacy: IntimacySettings = IntimacySettings()
    pdkt: PDKTSettings = PDKTSettings()
    session: SessionSettings = SessionSettings()
    memory: MemorySettings = MemorySettings()
    backup: BackupSettings = BackupSettings()
    logging: LoggingSettings = LoggingSettings()
    features: FeatureSettings = FeatureSettings()
    
    # V3: New component settings
    emotional: EmotionalSettings = EmotionalSettings()
    role: RoleSettings = RoleSettings()
    performance: PerformanceSettings = PerformanceSettings()
    
    # Paths
    base_dir: Path = Path(__file__).parent
    
    @validator('deepseek_api_key')
    def validate_deepseek_key(cls, v):
        if not v or v == "your_deepseek_api_key_here":
            raise ValueError("DEEPSEEK_API_KEY tidak boleh kosong")
        return v
    
    @validator('telegram_token')
    def validate_telegram_token(cls, v):
        if not v or v == "your_telegram_bot_token_here":
            raise ValueError("TELEGRAM_TOKEN tidak boleh kosong")
        if ':' not in v:
            raise ValueError("Format TELEGRAM_TOKEN tidak valid")
        return v
    
    @validator('admin_id')
    def validate_admin_id(cls, v):
        if v == 0:
            raise ValueError("ADMIN_ID harus diisi")
        return v
    
    def create_directories(self):
        """Create all necessary directories"""
        dirs = [
            self.logging.log_dir,
            self.memory.vector_db_dir,
            self.memory.memory_dir,  # V3: tambah memory_dir
            self.backup.backup_dir,
            self.session.session_dir,
            self.base_dir / "data",
        ]
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
        return self
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# =============================================================================
# GLOBAL SETTINGS INSTANCE
# =============================================================================
settings = Settings()
settings.create_directories()

print("=" * 70)
print("💕 MYLOVE PREMIUM AI V3 - SETTINGS LOADED")
print("=" * 70)
print(f"📊 Database: {settings.database.type} @ {settings.database.path}")
print(f"🤖 AI Model: {settings.ai.model}")
print(f"👑 Admin ID: {settings.admin_id}")
print(f"🎭 Emotional Flow: {'ENABLED' if settings.features.emotional_flow_enabled else 'DISABLED'}")
print(f"📍 Spatial Awareness: {'ENABLED' if settings.features.spatial_awareness_enabled else 'DISABLED'}")
print(f"🎭 Role Behavior: {'ENABLED' if settings.features.role_behavior_enabled else 'DISABLED'}")
print("=" * 70)

__all__ = ['settings']
