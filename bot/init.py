#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - BOT PACKAGE
=============================================================================
"""

from .application import create_application
from .handlers import (
    message_handler,
    start_command,
    help_command,
    status_command,
    progress_command,
    cancel_command,
    close_command,
    end_command,
    continue_command,
    # Relationship
    jadipacar_command,
    break_command,
    unbreak_command,
    breakup_command,
    fwb_command,
    # HTS/FWB
    htslist_command,
    fwblist_command,
    hts_call_handler,
    fwb_call_handler,
    # Public
    explore_command,
    locations_command,
    risk_command,
    # Ranking
    tophts_command,
    myclimax_command,
    climaxhistory_command,
    # Admin
    stats_command,
    db_stats_command,
    debug_command,
)

from .commands import (
    dominant_command,
    pause_command,
    unpause_command,
    sessions_command,
)

from .callbacks import (
    agree_18_callback,
    start_pause_callback,
    role_ipar_callback,
    role_teman_kantor_callback,
    role_janda_callback,
    role_pelakor_callback,
    role_istri_orang_callback,
    role_pdkt_callback,
    role_sepupu_callback,
    role_teman_sma_callback,
    role_mantan_callback,
    end_callback,
    close_callback,
    jadipacar_callback,
    break_callback,
    breakup_callback,
    fwb_callback,
    threesome_menu_callback,
    back_to_main_callback,
)

from .webhook import setup_webhook_sync

__all__ = [
    # Application
    'create_application',
    'setup_webhook_sync',
    
    # Handlers
    'message_handler',
    'start_command',
    'help_command',
    'status_command',
    'progress_command',
    'cancel_command',
    'close_command',
    'end_command',
    'continue_command',
    
    # Relationship
    'jadipacar_command',
    'break_command',
    'unbreak_command',
    'breakup_command',
    'fwb_command',
    
    # HTS/FWB
    'htslist_command',
    'fwblist_command',
    'hts_call_handler',
    'fwb_call_handler',
    
    # Public
    'explore_command',
    'locations_command',
    'risk_command',
    
    # Ranking
    'tophts_command',
    'myclimax_command',
    'climaxhistory_command',
    
    # Admin
    'stats_command',
    'db_stats_command',
    'debug_command',
    
    # Dummy
    'dominant_command',
    'pause_command',
    'unpause_command',
    'sessions_command',
    
    # Callbacks
    'agree_18_callback',
    'start_pause_callback',
    'role_ipar_callback',
    'role_teman_kantor_callback',
    'role_janda_callback',
    'role_pelakor_callback',
    'role_istri_orang_callback',
    'role_pdkt_callback',
    'role_sepupu_callback',
    'role_teman_sma_callback',
    'role_mantan_callback',
    'end_callback',
    'close_callback',
    'jadipacar_callback',
    'break_callback',
    'breakup_callback',
    'fwb_callback',
    'threesome_menu_callback',
    'back_to_main_callback',
]
