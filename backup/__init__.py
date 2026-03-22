#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - BACKUP PACKAGE INIT
=============================================================================
"""

from .automated import AutoBackup, get_backup_manager
from .recovery import RecoveryManager
from .verify import BackupVerifier

__all__ = [
    'AutoBackup',
    'get_backup_manager',
    'RecoveryManager',
    'BackupVerifier',
]

__version__ = "2.0.0"
