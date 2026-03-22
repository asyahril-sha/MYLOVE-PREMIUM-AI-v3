# bot/application.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - PTB APPLICATION FACTORY
=============================================================================
Membuat dan mengkonfigurasi aplikasi Telegram Bot dengan semua handler
Termasuk handler untuk V3: PDKT, Mantan & FWB, Ranking, HTS, Session Continue
=============================================================================
"""

import logging
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler
)
from telegram.request import HTTPXRequest

from config import settings
from database.models import Constants
from bot.handlers import (
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
    # PDKT V3
    pdkt_command,
    pdktrandom_command,
    pdktlist_command,
    pdktdetail_command,
    pdktwho_command,
    pausepdkt_command,
    resumepdkt_command,
    stoppdkt_command,
    # Mantan & FWB V3
    mantanlist_command,
    mantan_detail_command,
    fwbrequest_command,
    fwblist_command,
    fwb_pause_command,
    fwb_resume_command,
    fwb_end_command,
    # Ranking
    tophts_command,
    myclimax_command,
    climaxhistory_command,
    # HTS
    hts_command,
    # Public
    explore_command,
    locations_command,
    risk_command,
    # Admin
    admin_command,
    stats_command,
    db_stats_command,
    debug_command,
    # Dummy
    dominant_command,
    pause_command,
    unpause_command,
    sessions_command,
    # HTS/FWB legacy
    htslist_command,
    hts_call_handler,
    fwb_call_handler,
)
from bot.callbacks import (
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
    admin_callback_handler,
    # V3 Callbacks
    stop_callback,
    fwb_end_callback,
    hts_callback,
)
from bot.commands import error_handler
from bot.webhook import setup_webhook_sync


# =============================================================================
# BOT STATES
# =============================================================================
class BotStates:
    """States for conversation handlers"""
    
    SELECTING_ROLE = 1
    SELECTING_BOT_NAME = 2
    SELECTING_BOT_ROLE = 3
    SELECTING_DOMINANCE = 4
    SELECTING_PERSONALITY = 5
    SELECTING_APPEARANCE = 6
    CONFIRMATION = 7
    CHATTING = 8
    SELECTING_ACTION = 9
    SELECTING_LOCATION = 10
    SELECTING_CLOTHING = 11
    SELECTING_ACTIVITY = 12
    AWAITING_RESPONSE = 13
    CONFIRM_END = 14
    CONFIRM_CLOSE = 15
    CONFIRM_BROADCAST = 16
    SELECTING_PDKT = 17
    SELECTING_MANTAN = 18
    SELECTING_FWB = 19


def create_application() -> Application:
    """
    Create and configure telegram application untuk MYLOVE V3
    """
    
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("🔧 Creating PTB application for MYLOVE V3...")
    logger.info("=" * 60)
    
    # Custom request dengan timeout besar
    request = HTTPXRequest(
        connection_pool_size=50,
        connect_timeout=60,
        read_timeout=60,
        write_timeout=60,
        pool_timeout=60,
    )
    
    # Build application
    app = ApplicationBuilder() \
        .token(settings.telegram_token) \
        .request(request) \
        .concurrent_updates(True) \
        .build()
    
    # ===== AMBIL STATE DARI CONSTANTS =====
    SELECTING_ROLE = getattr(Constants, 'SELECTING_ROLE', BotStates.SELECTING_ROLE)
    CONFIRM_END = getattr(Constants, 'CONFIRM_END', BotStates.CONFIRM_END)
    CONFIRM_CLOSE = getattr(Constants, 'CONFIRM_CLOSE', BotStates.CONFIRM_CLOSE)
    CONFIRM_BROADCAST = getattr(Constants, 'CONFIRM_BROADCAST', BotStates.CONFIRM_BROADCAST)
    
    # =========================================================================
    # CONVERSATION HANDLERS
    # =========================================================================
    
    # Start conversation
    start_conv = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            SELECTING_ROLE: [
                CallbackQueryHandler(agree_18_callback, pattern='^agree_18$'),
                CallbackQueryHandler(start_pause_callback, pattern='^(unpause|new)$'),
                CallbackQueryHandler(role_ipar_callback, pattern='^role_ipar$'),
                CallbackQueryHandler(role_teman_kantor_callback, pattern='^role_teman_kantor$'),
                CallbackQueryHandler(role_janda_callback, pattern='^role_janda$'),
                CallbackQueryHandler(role_pelakor_callback, pattern='^role_pelakor$'),
                CallbackQueryHandler(role_istri_orang_callback, pattern='^role_istri_orang$'),
                CallbackQueryHandler(role_pdkt_callback, pattern='^role_pdkt$'),
                CallbackQueryHandler(role_sepupu_callback, pattern='^role_sepupu$'),
                CallbackQueryHandler(role_teman_sma_callback, pattern='^role_teman_sma$'),
                CallbackQueryHandler(role_mantan_callback, pattern='^role_mantan$'),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel_command)],
        name="start_conversation",
        persistent=False,
        per_user=True,
        per_chat=True,
        per_message=False
    )
    
    # End conversation
    end_conv = ConversationHandler(
        entry_points=[CommandHandler('end', end_command)],
        states={
            CONFIRM_END: [CallbackQueryHandler(end_callback, pattern='^end_')],
        },
        fallbacks=[CommandHandler('cancel', cancel_command)],
        name="end_conversation",
        persistent=False,
        per_user=True,
        per_chat=True,
        per_message=False
    )
    
    # Close conversation
    close_conv = ConversationHandler(
        entry_points=[CommandHandler('close', close_command)],
        states={
            CONFIRM_CLOSE: [CallbackQueryHandler(close_callback, pattern='^close_')],
        },
        fallbacks=[CommandHandler('cancel', cancel_command)],
        name="close_conversation",
        persistent=False,
        per_user=True,
        per_chat=True,
        per_message=False
    )
    
    # Relationship conversations
    rel_conv = ConversationHandler(
        entry_points=[
            CommandHandler('jadipacar', jadipacar_command),
            CommandHandler('break', break_command),
            CommandHandler('breakup', breakup_command),
            CommandHandler('fwb', fwb_command)
        ],
        states={
            CONFIRM_BROADCAST: [
                CallbackQueryHandler(jadipacar_callback, pattern='^jadipacar_'),
                CallbackQueryHandler(break_callback, pattern='^break_'),
                CallbackQueryHandler(breakup_callback, pattern='^breakup_'),
                CallbackQueryHandler(fwb_callback, pattern='^fwb_'),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel_command)],
        name="relationship_conversation",
        persistent=False,
        per_user=True,
        per_chat=True,
        per_message=False
    )
    
    # =========================================================================
    # ADD CONVERSATION HANDLERS
    # =========================================================================
    app.add_handler(start_conv)
    app.add_handler(end_conv)
    app.add_handler(close_conv)
    app.add_handler(rel_conv)
    
    # =========================================================================
    # COMMAND HANDLERS
    # =========================================================================
    logger.info("  • Registering command handlers...")
    
    # Basic commands
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("progress", progress_command))
    app.add_handler(CommandHandler("cancel", cancel_command))
    
    # Session commands
    app.add_handler(CommandHandler("close", close_command))
    app.add_handler(CommandHandler("end", end_command))
    app.add_handler(CommandHandler("continue", continue_command))
    app.add_handler(CommandHandler("sessions", sessions_command))
    
    # Dummy commands
    app.add_handler(CommandHandler("dominant", dominant_command))
    app.add_handler(CommandHandler("pause", pause_command))
    app.add_handler(CommandHandler("unpause", unpause_command))
    
    # Relationship commands
    app.add_handler(CommandHandler("jadipacar", jadipacar_command))
    app.add_handler(CommandHandler("break", break_command))
    app.add_handler(CommandHandler("unbreak", unbreak_command))
    app.add_handler(CommandHandler("breakup", breakup_command))
    app.add_handler(CommandHandler("fwb", fwb_command))
    
    # =========================================================================
    # PDKT V3 COMMANDS
    # =========================================================================
    logger.info("  • Registering PDKT V3 commands...")
    app.add_handler(CommandHandler("pdkt", pdkt_command))
    app.add_handler(CommandHandler("pdktrandom", pdktrandom_command))
    app.add_handler(CommandHandler("pdktlist", pdktlist_command))
    app.add_handler(CommandHandler("pdktdetail", pdktdetail_command))
    app.add_handler(CommandHandler("pdktwho", pdktwho_command))
    app.add_handler(CommandHandler("pausepdkt", pausepdkt_command))
    app.add_handler(CommandHandler("resumepdkt", resumepdkt_command))
    app.add_handler(CommandHandler("stoppdkt", stoppdkt_command))
    
    # =========================================================================
    # MANTAN & FWB V3 COMMANDS
    # =========================================================================
    logger.info("  • Registering Mantan & FWB V3 commands...")
    app.add_handler(CommandHandler("mantanlist", mantanlist_command))
    app.add_handler(CommandHandler("mantan", mantan_detail_command))
    app.add_handler(CommandHandler("fwbrequest", fwbrequest_command))
    app.add_handler(CommandHandler("fwblist", fwblist_command))
    app.add_handler(CommandHandler("fwb", fwb_command))
    app.add_handler(CommandHandler("fwb_pause", fwb_pause_command))
    app.add_handler(CommandHandler("fwb_resume", fwb_resume_command))
    app.add_handler(CommandHandler("fwb_end", fwb_end_command))
    
    # =========================================================================
    # RANKING COMMANDS
    # =========================================================================
    logger.info("  • Registering Ranking commands...")
    app.add_handler(CommandHandler("tophts", tophts_command))
    app.add_handler(CommandHandler("myclimax", myclimax_command))
    app.add_handler(CommandHandler("climaxhistory", climaxhistory_command))
    
    # =========================================================================
    # HTS COMMAND (NEW)
    # =========================================================================
    logger.info("  • Registering HTS command...")
    app.add_handler(CommandHandler("hts", hts_command))
    
    # =========================================================================
    # HTS/FWB LEGACY COMMANDS (pattern matching)
    # =========================================================================
    logger.info("  • Registering HTS/FWB legacy commands...")
    app.add_handler(CommandHandler("htslist", htslist_command))
    app.add_handler(CommandHandler("fwblist", fwblist_command))
    app.add_handler(MessageHandler(filters.Regex(r'^/hts-'), hts_call_handler))
    app.add_handler(MessageHandler(filters.Regex(r'^/fwb-'), fwb_call_handler))
    
    # =========================================================================
    # PUBLIC AREA COMMANDS
    # =========================================================================
    logger.info("  • Registering Public Area commands...")
    app.add_handler(CommandHandler("explore", explore_command))
    app.add_handler(CommandHandler("locations", locations_command))
    app.add_handler(CommandHandler("risk", risk_command))
    
    # =========================================================================
    # ADMIN COMMANDS
    # =========================================================================
    logger.info("  • Registering Admin commands...")
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("db_stats", db_stats_command))
    app.add_handler(CommandHandler("debug", debug_command))
    
    # =========================================================================
    # MESSAGE HANDLER (HARUS PALING AKHIR)
    # =========================================================================
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # =========================================================================
    # CALLBACK HANDLERS
    # =========================================================================
    logger.info("  • Registering callback handlers...")
    
    # Role callbacks
    app.add_handler(CallbackQueryHandler(agree_18_callback, pattern='^agree_18$'))
    app.add_handler(CallbackQueryHandler(start_pause_callback, pattern='^(unpause|new)$'))
    app.add_handler(CallbackQueryHandler(role_ipar_callback, pattern='^role_ipar$'))
    app.add_handler(CallbackQueryHandler(role_teman_kantor_callback, pattern='^role_teman_kantor$'))
    app.add_handler(CallbackQueryHandler(role_janda_callback, pattern='^role_janda$'))
    app.add_handler(CallbackQueryHandler(role_pelakor_callback, pattern='^role_pelakor$'))
    app.add_handler(CallbackQueryHandler(role_istri_orang_callback, pattern='^role_istri_orang$'))
    app.add_handler(CallbackQueryHandler(role_pdkt_callback, pattern='^role_pdkt$'))
    app.add_handler(CallbackQueryHandler(role_sepupu_callback, pattern='^role_sepupu$'))
    app.add_handler(CallbackQueryHandler(role_teman_sma_callback, pattern='^role_teman_sma$'))
    app.add_handler(CallbackQueryHandler(role_mantan_callback, pattern='^role_mantan$'))
    
    # Session callbacks
    app.add_handler(CallbackQueryHandler(end_callback, pattern='^end_'))
    app.add_handler(CallbackQueryHandler(close_callback, pattern='^close_'))
    
    # Relationship callbacks
    app.add_handler(CallbackQueryHandler(jadipacar_callback, pattern='^jadipacar_'))
    app.add_handler(CallbackQueryHandler(break_callback, pattern='^break_'))
    app.add_handler(CallbackQueryHandler(breakup_callback, pattern='^breakup_'))
    app.add_handler(CallbackQueryHandler(fwb_callback, pattern='^fwb_'))
    
    # Threesome callbacks
    app.add_handler(CallbackQueryHandler(threesome_menu_callback, pattern='^threesome_menu$'))
    app.add_handler(CallbackQueryHandler(back_to_main_callback, pattern='^back_to_main$'))
    
    # Admin callbacks
    app.add_handler(CallbackQueryHandler(admin_callback_handler, pattern='^admin_'))
    
    # =========================================================================
    # V3 CALLBACK HANDLERS (BARU)
    # =========================================================================
    logger.info("  • Registering V3 callback handlers...")
    
    # Stop PDKT callback
    app.add_handler(CallbackQueryHandler(stop_callback, pattern='^stop_'))
    
    # FWB End callback
    app.add_handler(CallbackQueryHandler(fwb_end_callback, pattern='^fwb_end_'))
    
    # HTS callback
    app.add_handler(CallbackQueryHandler(hts_callback, pattern='^hts_'))
    
    # =========================================================================
    # ERROR HANDLER
    # =========================================================================
    app.add_error_handler(error_handler)
    
    # Log jumlah handlers
    handler_count = sum(len(h) for h in app.handlers.values())
    logger.info(f"✅ All handlers registered: {handler_count} handlers")
    logger.info("   • Basic commands: 5")
    logger.info("   • PDKT V3 commands: 8")
    logger.info("   • Mantan & FWB V3 commands: 7")
    logger.info("   • Ranking commands: 3")
    logger.info("   • HTS command: 1")
    logger.info("   • Session commands: 4")
    logger.info("   • Public Area commands: 3")
    logger.info("   • Admin commands: 4")
    logger.info("   • Callback handlers: 25+")
    logger.info("   • V3 Callbacks: 3")
    logger.info("=" * 60)
    
    return app


__all__ = ['create_application', 'BotStates']
