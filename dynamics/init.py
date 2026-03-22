# dynamics/__init__.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - DYNAMICS PACKAGE
=============================================================================
Package untuk sistem dinamis bot (lokasi, pakaian, posisi, emosi, dll)
"""

# =============================================================================
# V2 EXISTING (TIDAK BERUBAH)
# =============================================================================
from .location import LocationSystem, LocationType
from .position import PositionSystem, PositionType
from .clothing import ClothingSystem
from .expression import ExpressionEngine, ExpressionType
from .sound import SoundEngine, SoundType
from .nickname import NicknameSystem
from .name_generator import NameGenerator, get_name_generator
from .location_validator import LocationValidator
from .physical import PhysicalSensation, SensationType
from .mood_swing import MoodSwing, MoodType

# =============================================================================
# V3 NEW (FILE BARU)
# =============================================================================
from .role_behavior import RoleBehavior
from .ipar_behavior import IparBehavior
from .teman_kantor_behavior import TemanKantorBehavior
from .janda_behavior import JandaBehavior
from .pelakor_behavior import PelakorBehavior
from .istri_orang_behavior import IstriOrangBehavior
from .pdkt_behavior import PDKTBehavior
from .sepupu_behavior import SepupuBehavior
from .teman_sma_behavior import TemanSmaBehavior
from .mantan_behavior import MantanBehavior
from .emotional_flow import EmotionalFlow, EmotionalState
from .spatial_awareness import SpatialAwareness
from .gesture_db import get_gesture, get_gesture_by_combination

# =============================================================================
# CONFIG IMPORTS (DARI configs FOLDER)
# =============================================================================
from configs.role_behavior_config import (
    IPAR_CONFIG,
    TEMAN_KANTOR_CONFIG,
    JANDA_CONFIG,
    PELAKOR_CONFIG,
    ISTRI_ORANG_CONFIG,
    PDKT_CONFIG,
    SEPUPU_CONFIG,
    TEMAN_SMA_CONFIG,
    MANTAN_CONFIG,
    get_role_config,
    get_all_role_names
)

from configs.gesture_config import (
    POSITION_GESTURES,
    ACTIVITY_GESTURES,
    EMOTION_GESTURES,
    AROUSAL_GESTURES,
    SPECIAL_SITUATION_GESTURES,
    get_position_gesture,
    get_activity_gesture,
    get_emotion_gesture,
    get_arousal_gesture,
    get_special_gesture,
    get_random_gesture
)

__all__ = [
    # V2 Existing
    'LocationSystem',
    'LocationType',
    'PositionSystem',
    'PositionType',
    'ClothingSystem',
    'ExpressionEngine',
    'ExpressionType',
    'SoundEngine',
    'SoundType',
    'NicknameSystem',
    'NameGenerator',
    'get_name_generator',
    'LocationValidator',
    'PhysicalSensation',
    'SensationType',
    'MoodSwing',
    'MoodType',
    
    # V3 New
    'RoleBehavior',
    'IparBehavior',
    'TemanKantorBehavior',
    'JandaBehavior',
    'PelakorBehavior',
    'IstriOrangBehavior',
    'PDKTBehavior',
    'SepupuBehavior',
    'TemanSmaBehavior',
    'MantanBehavior',
    'EmotionalFlow',
    'EmotionalState',
    'SpatialAwareness',
    'get_gesture',
    'get_gesture_by_combination',
    
    # Config exports
    'IPAR_CONFIG',
    'TEMAN_KANTOR_CONFIG',
    'JANDA_CONFIG',
    'PELAKOR_CONFIG',
    'ISTRI_ORANG_CONFIG',
    'PDKT_CONFIG',
    'SEPUPU_CONFIG',
    'TEMAN_SMA_CONFIG',
    'MANTAN_CONFIG',
    'get_role_config',
    'get_all_role_names',
    'POSITION_GESTURES',
    'ACTIVITY_GESTURES',
    'EMOTION_GESTURES',
    'AROUSAL_GESTURES',
    'SPECIAL_SITUATION_GESTURES',
    'get_position_gesture',
    'get_activity_gesture',
    'get_emotion_gesture',
    'get_arousal_gesture',
    'get_special_gesture',
    'get_random_gesture',
]

__version__ = "3.0.0"
