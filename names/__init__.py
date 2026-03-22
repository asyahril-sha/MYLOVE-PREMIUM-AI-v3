#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - NAMES DATABASE
=============================================================================
Database nama untuk setiap role
Bot akan memilih nama random saat pertama kali memilih role
Nama ini akan menjadi identitas permanen bot dan masuk ke UniqueID
=============================================================================
"""

from .artists import (
    ARTIS_INDONESIA_NON_HIJAB,
    ARTIS_INDONESIA_HIJAB,
    ARTIS_INTERNASIONAL_NON_HIJAB,
    ARTIS_INTERNASIONAL_HIJAB,
    ALL_ARTIS,
    ROLE_REFERENCES,
    get_random_artist_for_role,
    get_artist_by_name,
    format_artist_description,
    get_artist_by_popularity
)

__all__ = [
    'ARTIS_INDONESIA_NON_HIJAB',
    'ARTIS_INDONESIA_HIJAB',
    'ARTIS_INTERNASIONAL_NON_HIJAB',
    'ARTIS_INTERNASIONAL_HIJAB',
    'ALL_ARTIS',
    'ROLE_REFERENCES',
    'get_random_artist_for_role',
    'get_artist_by_name',
    'format_artist_description',
    'get_artist_by_popularity',
]

__version__ = "2.0.0"
