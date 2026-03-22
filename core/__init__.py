#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - CORE PACKAGE INIT
=============================================================================
"""

# AI Engine
from .ai_engine import AIEngine
from .intent_analyzer import IntentAnalyzer, UserIntent, Sentiment
from .name_detector import NameDetector, get_name_detector
from .prompt_builder import PromptBuilder
from .context_analyzer import ContextAnalyzer

# Optional imports (with fallback)
try:
    from .personality import PersonalitySystem
except ImportError:
    PersonalitySystem = None

try:
    from .proactive_generator import ProactiveMessageGenerator, ProactiveType
except ImportError:
    ProactiveMessageGenerator = None
    ProactiveType = None

try:
    from .story_predictor import StoryPredictor, StoryArc
except ImportError:
    StoryPredictor = None
    StoryArc = None

try:
    from .scene_recommender import SceneRecommender, SceneType
except ImportError:
    SceneRecommender = None
    SceneType = None

try:
    from .consciousness import ContinuousConsciousness
except ImportError:
    ContinuousConsciousness = None

__all__ = [
    'AIEngine',
    'IntentAnalyzer',
    'UserIntent',
    'Sentiment',
    'NameDetector',
    'get_name_detector',
    'PromptBuilder',
    'ContextAnalyzer',
    'PersonalitySystem',
    'ProactiveMessageGenerator',
    'ProactiveType',
    'StoryPredictor',
    'StoryArc',
    'SceneRecommender',
    'SceneType',
    'ContinuousConsciousness',
]

__version__ = "2.0.0"
