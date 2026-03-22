#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - BOT COMMANDS
=============================================================================
Error handler dan utility commands
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


# =============================================================================
# ERROR HANDLER
# =============================================================================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Global error handler untuk semua error di bot
    
    Args:
        update: Update object dari Telegram
        context: Context object dari PTB
    """
    logger.error(f"Update {update} caused error {context.error}")
    
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ Terjadi error internal. Silakan coba lagi nanti."
            )
    except Exception as e:
        logger.error(f"Error sending error message: {e}")


# =============================================================================
# DUMMY COMMANDS (untuk backward compatibility dan fallback)
# =============================================================================

async def dominant_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Mode dominant diaktifkan
    Untuk kompatibilitas dengan V1
    """
    await update.message.reply_text("⚡ Mode dominant diaktifkan.")


async def pause_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Pause session
    User bisa menjeda percakapan
    """
    context.user_data['paused'] = True
    await update.message.reply_text("⏸️ Sesi dijeda. Ketik /unpause untuk melanjutkan.")


async def unpause_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Unpause session
    Melanjutkan percakapan yang di-pause
    """
    context.user_data['paused'] = False
    await update.message.reply_text("▶️ Sesi dilanjutkan.")


async def sessions_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Lihat semua session (belum fully implemented)
    """
    await update.message.reply_text(
        "📋 **DAFTAR SESSION**\n\n"
        "Fitur ini sedang dalam pengembangan.\n"
        "Gunakan /start untuk memulai session baru.",
        parse_mode='Markdown'
    )


# =============================================================================
# ADMIN COMMANDS (opsional, untuk debugging)
# =============================================================================

async def debug_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Debug command untuk admin
    Menampilkan informasi session saat ini
    """
    user_id = update.effective_user.id
    
    # Cek apakah admin (opsional, bisa diaktifkan nanti)
    # if user_id != settings.admin_id:
    #     await update.message.reply_text("❌ Command hanya untuk admin")
    #     return
    
    debug_info = (
        f"🔍 **DEBUG INFO**\n\n"
        f"Session ID: {context.user_data.get('current_session', 'None')}\n"
        f"Bot Name: {context.user_data.get('bot_name', 'None')}\n"
        f"Role: {context.user_data.get('current_role', 'None')}\n"
        f"Level: {context.user_data.get('intimacy_level', 1)}/12\n"
        f"Total Chats: {context.user_data.get('total_chats', 0)}\n"
        f"Paused: {context.user_data.get('paused', False)}\n"
        f"Location: {context.user_data.get('current_location', 'None')}\n"
        f"Clothing: {context.user_data.get('current_clothing', 'None')}\n"
        f"Position: {context.user_data.get('current_position', 'None')}"
    )
    
    await update.message.reply_text(debug_info, parse_mode='Markdown')


# =============================================================================
# STATS COMMAND (admin only - simple version)
# =============================================================================

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Statistik sederhana bot (admin only)
    """
    user_id = update.effective_user.id
    
    # Cek admin - bisa diaktifkan nanti
    # if user_id != settings.admin_id:
    #     await update.message.reply_text("❌ Command hanya untuk admin")
    #     return
    
    # Simple stats
    total_sessions = len(context.bot_data.get('active_sessions', {}))
    total_users = len(context.bot_data.get('users', {}))
    
    stats_text = (
        f"📊 **BOT STATISTICS**\n\n"
        f"Active Sessions: {total_sessions}\n"
        f"Total Users: {total_users}\n"
        f"Uptime: (belum diimplementasikan)"
    )
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')


# =============================================================================
# DB STATS COMMAND (admin only)
# =============================================================================

async def db_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Statistik database (admin only)
    """
    user_id = update.effective_user.id
    
    # Cek admin - bisa diaktifkan nanti
    # if user_id != settings.admin_id:
    #     await update.message.reply_text("❌ Command hanya untuk admin")
    #     return
    
    await update.message.reply_text(
        "🗄️ **DATABASE STATISTICS**\n\n"
        "Fitur ini akan menampilkan:\n"
        "• Total sessions\n"
        "• Total messages\n"
        "• Database size\n"
        "• Backup info\n\n"
        "_(Dalam pengembangan)_",
        parse_mode='Markdown'
    )


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [
    # Error handler
    'error_handler',
    # Dummy commands
    'dominant_command',
    'pause_command',
    'unpause_command',
    'sessions_command',
    # Admin commands
    'debug_command',
    'stats_command',
    'db_stats_command',
]
