# memory/__init__.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - MEMORY PACKAGE
=============================================================================
Package untuk sistem memory bot (working, episodic, semantic, dll)
"""

# =============================================================================
# V2 EXISTING (TIDAK BERUBAH)
# =============================================================================
from .working_memory import WorkingMemory
from .episodic import EpisodicMemory, EpisodeType
from .semantic import SemanticMemory, FactCategory
from .compact_memory import CompactMemory
from .forgetting import SemanticForgetting, ForgetType
from .state_tracker import StateTracker, StateType
from .memory_bridge import MemoryBridge, MemoryType, MemoryImportance

# =============================================================================
# V3 NEW (FILE BARU)
# =============================================================================
from .emotional_memory import EmotionalMemory
from .scene_memory import SceneMemory

__all__ = [
    # V2 Existing
    'WorkingMemory',
    'EpisodicMemory',
    'EpisodeType',
    'SemanticMemory',
    'FactCategory',
    'CompactMemory',
    'SemanticForgetting',
    'ForgetType',
    'StateTracker',
    'StateType',
    'MemoryBridge',
    'MemoryType',
    'MemoryImportance',
    
    # V3 New
    'EmotionalMemory',
    'SceneMemory',
]

__version__ = "3.0.0"
