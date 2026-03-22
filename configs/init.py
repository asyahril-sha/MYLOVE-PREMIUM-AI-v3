# configs/__init__.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - CONFIGS PACKAGE
=============================================================================
Package untuk konfigurasi V3 (role behavior, gesture, dll)
"""

from .role_behavior_config import (
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

from .gesture_config import (
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
    # Role Behavior Config
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
    
    # Gesture Config
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
