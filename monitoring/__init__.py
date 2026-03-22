#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - MONITORING PACKAGE INIT
=============================================================================
"""

from .metrics import MetricsCollector, get_metrics_collector
from .dashboard import DashboardServer

__all__ = [
    'MetricsCollector',
    'get_metrics_collector',
    'DashboardServer',
]

__version__ = "2.0.0"
