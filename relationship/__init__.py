#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - RELATIONSHIP PACKAGE INIT
=============================================================================
Inisialisasi package relationship dan export semua komponen
"""

from .intimacy import IntimacySystem
from .activity_boost import ActivityBoost, BoostType
from .ranking import RankingSystem
from .hts import HTSManager, HTSStatus
from .fwb import FWBManager, FWBStatus, FWBPauseReason, FWBEndReason
from .mantan import MantanManager, MantanStatus

__all__ = [
    'IntimacySystem',
    'ActivityBoost',
    'BoostType',
    'RankingSystem',
    'HTSManager',
    'HTSStatus',
    'FWBManager',
    'FWBStatus',
    'FWBPauseReason',
    'FWBEndReason',
    'MantanManager',
    'MantanStatus',
]

__version__ = "2.0.0"
