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
from configs.role_behavior import RoleBehavior
from configs.ipar_behavior import IparBehavior
from configs.teman_kantor_behavior import TemanKantorBehavior
from configs.janda_behavior import JandaBehavior
from configs.pelakor_behavior import PelakorBehavior
from configs.istri_orang_behavior import IstriOrangBehavior
from configs.pdkt_behavior import PDKTBehavior
from configs.sepupu_behavior import SepupuBehavior
from configs.teman_sma_behavior import TemanSmaBehavior
from configs.mantan_behavior import MantanBehavior
from .emotional_flow import EmotionalFlow, EmotionalState
from .spatial_awareness import SpatialAwareness
from .gesture_db import get_gesture, get_gesture_by_combination
from configs.role_behavior_config

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
]

__version__ = "3.0.0"
