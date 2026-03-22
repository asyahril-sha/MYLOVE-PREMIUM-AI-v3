# config.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - KONFIGURASI UTAMA (V3 FIXED)
=============================================================================
"""

import os
import secrets
from typing import Optional, Dict, Any, List
from pathlib import Path

# ===== IMPORT PYDANTIC YANG BENAR =====
from pydantic import Field, field_validator, ConfigDict
from pydantic_settings import BaseSettings


# =============================================================================
# DATABASE SETTINGS
# =============================================================================
class DatabaseSettings(BaseSettings):
    """Konfigurasi database"""
    model_config = ConfigDict(env_prefix="DB_", extra="ignore")
    
    type: str = Field("sqlite", alias="DB_TYPE")
    path: Path = Field(Path("data/mylove.db"), alias="DB_PATH")
    pool_size: int = Field(5, alias="DB_POOL_SIZE")
    timeout: int = Field(30, alias="DB_TIMEOUT")
    
    @property
    def url(self) -> str:
        return f"sqlite+aiosqlite:///{self.path}"


# =============================================================================
# AI SETTINGS
# =============================================================================
class AISettings(BaseSettings):
    """Konfigurasi AI DeepSeek"""
    model_config = ConfigDict(env_prefix="AI_", extra="ignore")
    
    temperature: float = Field(0.9, alias="AI_TEMPERATURE")
    max_tokens: int = Field(2000, alias="AI_MAX_TOKENS")
    timeout: int = Field(30, alias="AI_TIMEOUT")
    model: str = Field("deepseek-chat", alias="AI_MODEL")
    
    min_message_length: int = Field(500, alias="MIN_MESSAGE_LENGTH")
    max_message_length: int = Field(2000, alias="MAX_MESSAGE_LENGTH")


# =============================================================================
# WEBHOOK SETTINGS
# =============================================================================
class WebhookSettings(BaseSettings):
    """Konfigurasi webhook"""
    model_config = ConfigDict(extra="ignore")
    
    url: Optional[str] = Field(None, alias="WEBHOOK_URL")
    port: int = Field(8080, alias="PORT")
    path: str = Field("/webhook", alias="WEBHOOK_PATH")
    secret_token: Optional[str] = Field(None, alias="WEBHOOK_SECRET")
    max_retries: int = Field(5, alias="WEBHOOK_MAX_RETRIES")
    enable_polling_fallback: bool = Field(True, alias="ENABLE_POLLING_FALLBACK")


# =============================================================================
# INTIMACY SETTINGS
# =============================================================================
class IntimacySettings(BaseSettings):
    """Sistem level intimacy time-based"""
    model_config = ConfigDict(extra="ignore")
    
    reset_level: int = Field(7, alias="RESET_LEVEL")
    max_level: int = Field(12, alias="MAX_LEVEL")
    aftercare_enabled: bool = Field(True, alias="AFTERCARE_ENABLED")
    
    level_targets: Dict[int, int] = {
        1: 0, 2: 5, 3: 12, 4: 20, 5: 30, 6: 42,
        7: 60, 8: 75, 9: 90, 10: 105, 11: 120, 12: 135
    }


# =============================================================================
# PDKT SETTINGS
# =============================================================================
class PDKTSettings(BaseSettings):
    """Sistem PDKT Natural"""
    model_config = ConfigDict(extra="ignore")
    
    chemistry_decay_rate: float = Field(0.01, alias="CHEMISTRY_DECAY")
    mood_evolution_rate: float = Field(0.1, alias="MOOD_EVOLUTION")
    dream_chance: float = Field(0.3, alias="DREAM_CHANCE")
    sixth_sense_chance: float = Field(0.15, alias="SIXTH_SENSE_CHANCE")


# =============================================================================
# SESSION SETTINGS
# =============================================================================
class SessionSettings(BaseSettings):
    """Sistem session"""
    model_config = ConfigDict(extra="ignore")
    
    id_format: str = "MYLOVE-{bot_name}-{role}-{user_id}-{date}-{seq:03d}"
    storage_type: str = Field("sqlite+json", alias="SESSION_STORAGE")
    session_dir: Path = Field(Path("data/sessions"), alias="SESSION_DIR")
    retention_days: int = Field(30, alias="SESSION_RETENTION_DAYS")
    auto_delete: bool = Field(True, alias="SESSION_AUTO_DELETE")


# =============================================================================
# MEMORY SETTINGS
# =============================================================================
class MemorySettings(BaseSettings):
    """Sistem memory dengan Hippocampus"""
    model_config = ConfigDict(extra="ignore")
    
    vector_db_dir: Path = Field(Path("data/vector_db"), alias="VECTOR_DB_DIR")
    working_memory_capacity: int = Field(20, alias="WORKING_MEMORY_CAPACITY")
    working_memory_expire: int = Field(86400, alias="WORKING_MEMORY_EXPIRE")
    consolidation_interval: int = Field(3600, alias="CONSOLIDATION_INTERVAL")
    forgetting_threshold: float = Field(0.3, alias="FORGETTING_THRESHOLD")
    memory_dir: Path = Field(Path("data/memory"), alias="MEMORY_DIR")


# =============================================================================
# BACKUP SETTINGS
# =============================================================================
class BackupSettings(BaseSettings):
    """Sistem backup otomatis"""
    model_config = ConfigDict(extra="ignore")
    
    enabled: bool = Field(True, alias="BACKUP_ENABLED")
    interval: int = Field(3600, alias="BACKUP_INTERVAL")
    retention_days: int = Field(7, alias="BACKUP_RETENTION_DAYS")
    backup_dir: Path = Field(Path("data/backups"), alias="BACKUP_DIR")
    s3_bucket: Optional[str] = Field(None, alias="BACKUP_S3_BUCKET")


# =============================================================================
# LOGGING SETTINGS
# =============================================================================
class LoggingSettings(BaseSettings):
    """Konfigurasi logging"""
    model_config = ConfigDict(extra="ignore")
    
    level: str = Field("INFO", alias="LOG_LEVEL")
    log_dir: Path = Field(Path("data/logs"), alias="LOG_DIR")
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


# =============================================================================
# FEATURE SETTINGS
# =============================================================================
class FeatureSettings(BaseSettings):
    """Feature toggles"""
    model_config = ConfigDict(env_prefix="", extra="ignore")
    
    sexual_enabled: bool = Field(True, alias="SEXUAL_CONTENT_ENABLED")
    public_risk_enabled: bool = Field(True, alias="PUBLIC_RISK_ENABLED")
    bot_initiative_enabled: bool = Field(True, alias="BOT_INITIATIVE_ENABLED")
    aftercare_enabled: bool = Field(True, alias="AFTERCARE_ENABLED")
    threesome_enabled: bool = Field(True, alias="THREESOME_ENABLED")
    memory_enabled: bool = Field(True, alias="MEMORY_ENABLED")
    emotional_flow_enabled: bool = Field(True, alias="EMOTIONAL_FLOW_ENABLED")
    spatial_awareness_enabled: bool = Field(True, alias="SPATIAL_AWARENESS_ENABLED")
    role_behavior_enabled: bool = Field(True, alias="ROLE_BEHAVIOR_ENABLED")


# =============================================================================
# EMOTIONAL SETTINGS (V3)
# =============================================================================
class EmotionalSettings(BaseSettings):
    """Konfigurasi Emotional Flow System V3"""
    model_config = ConfigDict(extra="ignore")
    
    arousal_decay_rate: float = Field(0.02, alias="AROUSAL_DECAY_RATE")
    empathy_factor_base: float = Field(0.6, alias="EMPATHY_FACTOR_BASE")
    arousal_threshold_horny: int = Field(70, alias="AROUSAL_THRESHOLD_HORNY")
    arousal_threshold_climax: int = Field(90, alias="AROUSAL_THRESHOLD_CLIMAX")
    mood_change_probability: float = Field(0.05, alias="MOOD_CHANGE_PROBABILITY")


# =============================================================================
# ROLE SETTINGS (V3)
# =============================================================================
class RoleSettings(BaseSettings):
    """Konfigurasi Role Behavior System V3"""
    model_config = ConfigDict(extra="ignore")
    
    ipar_jealousy_factor: float = Field(0.3, alias="IPAR_JEALOUSY_FACTOR")
    teman_kantor_risk_factor: float = Field(0.4, alias="TEMAN_KANTOR_RISK_FACTOR")
    janda_experience_factor: float = Field(0.8, alias="JANDA_EXPERIENCE_FACTOR")
    pelakor_aggression_factor: float = Field(0.9, alias="PELAKOR_AGGRESSION_FACTOR")
    istri_orang_guilt_factor: float = Field(0.7, alias="ISTRI_ORANG_GUILT_FACTOR")
    pdkt_shyness_factor: float = Field(0.6, alias="PDKT_SHYNESS_FACTOR")
    sepupu_curiosity_factor: float = Field(0.7, alias="SEPUPU_CURIOSITY_FACTOR")
    teman_sma_nostalgia_factor: float = Field(0.6, alias="TEMAN_SMA_NOSTALGIA_FACTOR")
    mantan_knowledge_factor: float = Field(0.8, alias="MANTAN_KNOWLEDGE_FACTOR")


# =============================================================================
# PERFORMANCE SETTINGS (V3)
# =============================================================================
class PerformanceSettings(BaseSettings):
    """Konfigurasi Performance Monitoring V3"""
    model_config = ConfigDict(extra="ignore")
    
    target_response_time: float = Field(3.0, alias="TARGET_RESPONSE_TIME")
    max_memory_mb: int = Field(500, alias="MAX_MEMORY_MB")
    slow_operation_threshold: float = Field(5.0, alias="SLOW_OPERATION_THRESHOLD")
    cache_ttl: int = Field(300, alias="CACHE_TTL")


# =============================================================================
# MAIN SETTINGS CLASS
# =============================================================================
class Settings(BaseSettings):
    """
    MYLOVE PREMIUM AI - Main Settings V3
    """
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # API Keys
    deepseek_api_key: str = Field(..., alias="DEEPSEEK_API_KEY")
    telegram_token: str = Field(..., alias="TELEGRAM_TOKEN")
    admin_id: int = Field(..., alias="ADMIN_ID")
    
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
    
    @field_validator('deepseek_api_key')
    @classmethod
    def validate_deepseek_key(cls, v):
        if not v or v == "your_deepseek_api_key_here":
            raise ValueError("DEEPSEEK_API_KEY tidak boleh kosong")
        return v
    
    @field_validator('telegram_token')
    @classmethod
    def validate_telegram_token(cls, v):
        if not v or v == "your_telegram_bot_token_here":
            raise ValueError("TELEGRAM_TOKEN tidak boleh kosong")
        if ':' not in v:
            raise ValueError("Format TELEGRAM_TOKEN tidak valid")
        return v
    
    @field_validator('admin_id')
    @classmethod
    def validate_admin_id(cls, v):
        if v == 0:
            raise ValueError("ADMIN_ID harus diisi")
        return v
    
    def create_directories(self):
        """Create all necessary directories"""
        dirs = [
            self.logging.log_dir,
            self.memory.vector_db_dir,
            self.memory.memory_dir,
            self.backup.backup_dir,
            self.session.session_dir,
            self.base_dir / "data",
        ]
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
        return self


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
