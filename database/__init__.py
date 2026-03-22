#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - DATABASE PACKAGE INIT
=============================================================================
"""

from .connection import DatabaseConnection, get_db, init_db, close_db
from .models import (
    # V1 Models
    User, Session, Conversation, Memory,
    Preference, Milestone, Backup, Constants,
    # V1 Compatibility
    Relationship,
    # V2 Models
    PDKTSession, Mantan, FWBRelation, HTSRelation,
    ThreesomeSession, ThreesomeParticipant,
    # V3 State Persistence
    UserSession
)
from .repository import Repository
from .migrate import run_migrations, fix_missing_columns
from .init_db import init_database

__all__ = [
    'DatabaseConnection',
    'get_db',
    'init_db',
    'close_db',
    'Repository',
    'run_migrations',
    'fix_missing_columns',
    'init_database',
    # Models
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
    # V3
    'UserSession',
]

__version__ = "2.0.0"
