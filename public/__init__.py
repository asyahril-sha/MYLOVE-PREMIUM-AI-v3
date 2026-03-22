#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - PUBLIC AREAS PACKAGE INIT
=============================================================================
Inisialisasi package public areas
"""

from .locations import PublicLocations
from .risk import RiskCalculator
from .thrill import ThrillSystem
from .auto_select import LocationAutoSelector
from .events import RandomEvents

__all__ = [
    'PublicLocations',
    'RiskCalculator',
    'ThrillSystem',
    'LocationAutoSelector',
    'RandomEvents',
]

__version__ = "2.0.0"
