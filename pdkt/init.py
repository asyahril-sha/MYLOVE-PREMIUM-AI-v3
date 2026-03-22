#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - PDKT NATURAL PACKAGE INIT
=============================================================================
PDKT dengan realisme 99% mirip manusia
- Chemistry natural (Dingin → Soulmate)
- Dua arah (user ngejar / bot ngejar)
- Multi-PDKT dengan pause/resume
- Memory PERMANEN untuk PDKT → PACAR → MANTAN
=============================================================================
"""

from .engine import NaturalPDKTEngine
from .chemistry import ChemistrySystem, ChemistryLevel, ChemistryScore
from .direction import DirectionSystem, PDKTDirection
from .mood import MoodSystem, MoodType
from .dreams import DreamSystem, DreamType
from .random_pdkt import RandomPDKTSystem
from .list_formatter import PDKTListFormatter

__all__ = [
    'NaturalPDKTEngine',
    'ChemistrySystem',
    'ChemistryLevel',
    'ChemistryScore',
    'DirectionSystem',
    'PDKTDirection',
    'MoodSystem',
    'MoodType',
    'DreamSystem',
    'DreamType',
    'RandomPDKTSystem',
    'PDKTListFormatter',
]

__version__ = "2.0.0"
