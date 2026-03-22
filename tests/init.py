# tests/__init__.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - TESTS PACKAGE
=============================================================================
Package untuk unit testing dan simulasi V3
"""

# =============================================================================
# V3 NEW (SEMUA BARU)
# =============================================================================
# Test modules (di-import saat dibutuhkan, tidak auto-load)
# from .test_emotional_flow import *
# from .test_spatial_awareness import *
# from .test_role_behavior import *
# from .simulate_conversation import *
# from .run_all_tests import *

__all__ = [
    # Test modules (akan di-load saat dipanggil)
    'test_emotional_flow',
    'test_spatial_awareness',
    'test_role_behavior',
    'simulate_conversation',
    'run_all_tests',
]

__version__ = "3.0.0"
