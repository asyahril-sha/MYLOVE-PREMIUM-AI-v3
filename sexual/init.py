#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - SEXUAL SYSTEMS PACKAGE INIT
=============================================================================
Inisialisasi package sexual systems
Catatan: Kode tidak explicit, data akan diproses oleh AI engine
"""

from .positions import PositionDatabase, get_position_database, DifficultyLevel, IntensityLevel
from .areas import AreaDatabase, AreaCategory, get_area_database
from .climax import ClimaxDatabase, ClimaxIntensity, ClimaxType, get_climax_database
from .preferences import PreferenceLearner
from .aftercare import AftercareSystem, AftercareType
from .scene_generator import SexSceneGenerator, ScenePhase, IntensityLevel as SceneIntensityLevel
from .level_11_12 import PremiumSexualFeatures

__all__ = [
    'PositionDatabase',
    'get_position_database',
    'DifficultyLevel',
    'IntensityLevel',
    'AreaDatabase',
    'AreaCategory',
    'get_area_database',
    'ClimaxDatabase',
    'ClimaxIntensity',
    'ClimaxType',
    'get_climax_database',
    'PreferenceLearner',
    'AftercareSystem',
    'AftercareType',
    'SexSceneGenerator',
    'ScenePhase',
    'SceneIntensityLevel',
    'PremiumSexualFeatures',
]

__version__ = "2.0.0"
