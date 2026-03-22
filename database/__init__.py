#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - DATABASE PACKAGE INIT
=============================================================================
"""

from .connection import DatabaseConnection, get_db, init_db
from .models import (
    # V1 Models
    User, Session, Conversation, Memory,
    Preference, Milestone, Backup, Constants,
    # V1 Compatibility
    Relationship,
    # V2 Models
    PDKTSession, Mantan, FWBRelation, HTSRelation,
    ThreesomeSession, ThreesomeParticipant
)
from .repository import Repository

__all__ = [
    'DatabaseConnection',
    'get_db',
    'init_db',
    'Repository',
    'User',
    'Session',
    'Conversation',
    'Memory',
    'Preference',
    'Milestone',
    'Backup',
    'Constants',
    'Relationship',
    # V2
    'PDKTSession',
    'Mantan',
    'FWBRelation',
    'HTSRelation',
    'ThreesomeSession',
    'ThreesomeParticipant',
]

__version__ = "2.0.0"
