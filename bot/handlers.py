#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - BOT HANDLERS
=============================================================================
Semua handlers untuk command dan message dengan AI Engine
"""

import time
import logging
import random
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from config import settings
from utils.logger import logger
from core.ai_engine import AIEngine

# Import repository untuk session permanent
from database.repository import Repository

# =============================================================================
# ACTIVE ENGINES STORAGE
# =============================================================================
active_engines = {}  # {session_id: AIEngine}
user_sessions = {}   # {user_id: current_session_id}

# Repository instance untuk session permanent
_repo = None

async def get_repository():
    global _repo
    if _repo is None:
        _repo = Repository()
    return _repo

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_bot_name(context) -> str:
    """Dapatkan nama bot dari context"""
    return context.user_data.get('bot_name', 'Aku')


def get_bot_display(context) -> str:
    """Dapatkan display nama bot dengan role"""
    nama = get_bot_name(context)
    role = context.user_data.get('current_role', '')
    if role:
        return f"{nama} ({role.title()})"
    return nama


# =============================================================================
# 1. MESSAGE HANDLER (MAIN - DENGAN AI ENGINE)
# =============================================================================

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler untuk semua pesan teks
    - Menggunakan AI Engine untuk generate response natural
    - Minimal 3-5 kalimat per respons
    - Sesuai level intimacy
    """
    try:
        user = update.effective_user
        user_message = update.message.text
        user_id = user.id
        user_name = user.first_name or "User"
        session_id = context.user_data.get('current_session')

        # ===== LOAD SESSION DARI DATABASE JIKA MEMORY KOSONG =====
        if not session_id:
            repo = await get_repository()
            saved_session = await repo.load_user_session_state(user_id)
            
            if saved_session:
                # Restore ke context.user_data
                context.user_data['current_session'] = saved_session['session_id']
                context.user_data['current_role'] = saved_session['role']
                context.user_data['bot_name'] = saved_session['bot_name']
                context.user_data['intimacy_level'] = saved_session['intimacy_level']
                context.user_data['total_chats'] = saved_session['total_chats']
                context.user_data['current_location'] = saved_session['current_location']
                context.user_data['current_clothing'] = saved_session['current_clothing']
                context.user_data['current_position'] = saved_session['current_position']
                context.user_data['relationship_status'] = saved_session['relationship_status']
                context.user_data['rel_type'] = saved_session.get('rel_type', 'non_pdkt')
                context.user_data['instance_id'] = saved_session.get('instance_id')
                
                session_id = saved_session['session_id']
                logger.info(f"✅ Session restored from DB for user {user_id}")
        # ===== END =====
        
        # ===== CEK PAUSE =====
        if context.user_data.get('paused', False):
            await update.message.reply_text("⏸️ Sesi sedang dijeda. Ketik /unpause untuk melanjutkan.")
            return
        
        # ===== AMBIL DATA BOT =====
        bot_name = context.user_data.get('bot_name', 'Maya')
        role = context.user_data.get('current_role', 'pdkt')
        level = context.user_data.get('intimacy_level', 1)
        instance_id = context.user_data.get('instance_id')
        rel_type = context.user_data.get('rel_type', 'non_pdkt')
        
        # ===== CEK APAKAH ADA SESSION AKTIF =====
        if not session_id:
            await update.message.reply_text(
                "❌ Kamu belum memulai hubungan.\n"
                "Ketik /start untuk memilih role."
            )
            return
        
        # ===== CEK ATAU BUAT AI ENGINE =====
        if session_id not in active_engines:
            # Buat AI engine baru
            try:
                # Cek API Key
                if not settings.deepseek_api_key or settings.deepseek_api_key == "your_deepseek_api_key_here":
                    logger.error("DeepSeek API key not set!")
                    await update.message.reply_text(
                        "❌ Maaf, AI Engine belum siap. Admin belum mengatur API key.\n"
                        "Mohon tunggu sebentar atau hubungi admin.\n\n"
                        f"<i>Sementara ini, {bot_name} akan merespon secara sederhana.</i>",
                        parse_mode='HTML'
                    )
                    # Fallback sederhana
                    fallback = f"Halo {user_name}, {bot_name} di sini. Cerita lagi dong, aku dengerin kok."
                    await update.message.reply_text(fallback)
                    return
                
                ai_engine = AIEngine(
                    api_key=settings.deepseek_api_key,
                    user_id=user_id,
                    session_id=session_id
                )
                
                # Start session
                await ai_engine.start_session(
                    role=role,
                    bot_name=bot_name,
                    rel_type=rel_type,
                    instance_id=instance_id
                )
                
                active_engines[session_id] = ai_engine
                logger.info(f"✅ New AI engine created for session {session_id}")
                
            except Exception as e:
                logger.error(f"Failed to create AI engine: {e}")
                # Fallback response natural
                fallback = (
                    f"{bot_name} tersenyum sambil memandangmu. "
                    f"'Maaf ya responsnya agak lambat. Aku lagi mikirin sesuatu. "
                    f"Tapi aku selalu seneng kalau kamu chat. Rasanya hangat gitu. "
                    f"Cerita lagi dong, aku dengerin baik-baik kok...'"
                )
                await update.message.reply_text(fallback)
                return
        
        ai_engine = active_engines[session_id]
        
        # ===== TENTUKAN PANGGILAN BERDASARKAN LEVEL =====
        if level >= 7:
            call = "Sayang"
        elif level >= 4:
            call = "Kak"
        else:
            call = user_name
        
        # ===== AMBIL DATA LOKASI, PAKAIAN, POSISI =====
        location = context.user_data.get('current_location', 'kamar')
        clothing = context.user_data.get('current_clothing', 'pakaian biasa')
        position = context.user_data.get('current_position', 'santai')
        mood = context.user_data.get('current_mood', 'senang')
        
        # ===== SIAPKAN KONTEKS UNTUK AI =====
        context_data = {
            'role': role,
            'bot_name': bot_name,
            'user_name': user_name,
            'call': call,
            'level': level,
            'rel_type': rel_type,
            'location': location,
            'clothing': clothing,
            'position': position,
            'mood': mood,
            'user_message': user_message,
            'last_interaction': time.time() - context.user_data.get('last_active', time.time())
        }
        
        # ===== GENERATE RESPONSE DENGAN AI =====
        try:
            response = await ai_engine.process_message(
                user_message=user_message,
                context=context_data
            )
            
            # Validasi panjang respons (minimal 100 karakter)
            if len(response) < 100:
                continuations = [
                    f"\n\nKamu lagi ngapain {call}?",
                    f"\n\n{bot_name} kangen {call}...",
                    f"\n\nEh udah makan belum {call}?",
                    f"\n\n<i>tersenyum</i> Cerita lagi dong {call}",
                    f"\n\n{call}, ada yang mau diceritain?"
                ]
                response += random.choice(continuations)
            
            # Validasi format (harus ada dialog)
            if not any(char in response for char in ['"', "'", '“', '”']):
                response = f"'{response}'"
                
        except Exception as e:
            logger.error(f"AI Engine error: {e}")
            response = (
                f"{bot_name} denger kok {call}. "
                f"Aku lagi di {location}, pakai {clothing}. "
                f"Suasananya enak buat ngobrol. "
                f"Kamu sendiri lagi ngapain? Cerita lagi dong, aku suka denger cerita kamu."
            )
        
        # ===== SIMPAN KE DATABASE =====
        repo = await get_repository()
        await repo.save_user_session_state(
            user_id=user_id,
            session_data={
                'session_id': session_id,
                'role': context.user_data.get('current_role'),
                'bot_name': context.user_data.get('bot_name'),
                'rel_type': context.user_data.get('rel_type'),
                'instance_id': context.user_data.get('instance_id'),
                'intimacy_level': context.user_data.get('intimacy_level', 1),
                'total_chats': context.user_data.get('total_chats', 0),
                'current_location': context.user_data.get('current_location', 'ruang tamu'),
                'current_clothing': context.user_data.get('current_clothing', 'pakaian biasa'),
                'current_position': context.user_data.get('current_position', 'santai'),
                'relationship_status': context.user_data.get('relationship_status', 'pdkt'),
            }
        )
        # ===== END =====
        
        # ===== UPDATE STATISTIK =====
        context.user_data['total_chats'] = context.user_data.get('total_chats', 0) + 1
        context.user_data['last_message'] = user_message
        context.user_data['last_response'] = response
        context.user_data['last_active'] = time.time()
        
        # Update level progress
        total_chats = context.user_data.get('total_chats', 0)
        if total_chats % 10 == 0 and level < 12:
            new_level = min(12, level + 1)
            context.user_data['intimacy_level'] = new_level
            logger.info(f"Level up: {level} → {new_level} for user {user_id}")
        
        # ===== KIRIM RESPONSE =====
        await update.message.reply_text(response, parse_mode='HTML')
        
    except Exception as e:
        logger.error(f"Error in message_handler: {e}")
        await update.message.reply_text(
            "❌ Maaf, terjadi kesalahan. Coba lagi nanti."
        )


# =============================================================================
# 2. START COMMAND
# =============================================================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mulai hubungan baru dengan bot"""
    user = update.effective_user
    args = context.args
    
    # Cek apakah ini continue dari session
    if args and args[0].startswith('continue_'):
        session_id = args[0].replace('continue_', '')
        context.args = [session_id]
        return await continue_handler(update, context)
    
    # Cek apakah sudah ada session aktif
    session_id = context.user_data.get('current_session')
    if session_id:
        keyboard = [
            [InlineKeyboardButton("✅ Lanjutkan", callback_data="unpause"),
             InlineKeyboardButton("🆕 Buat Baru", callback_data="new")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "⚠️ <b>Kamu sudah memiliki session aktif!</b>\n\n"
            f"Session ID: <code>{session_id}</code>\n"
            f"Role: {context.user_data.get('current_role', 'Unknown')}\n"
            f"Bot: {context.user_data.get('bot_name', 'Unknown')}\n\n"
            "Pilih tindakan:",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        return
    
    welcome_text = (
        f"💕 <b>Halo {user.first_name}!</b>\n\n"
        "Selamat datang di <b>MYLOVE PREMIUM AI</b>\n"
        "AI pendamping dengan 9 role eksklusif.\n"
        "• Leveling berbasis durasi (60 menit ke Level 7)\n"
        "• Nama bot permanent di UniqueID\n\n"
        "<b>Pilih role yang kamu inginkan:</b>"
    )
    
    keyboard = [
        [InlineKeyboardButton("👩 Ipar", callback_data="role_ipar"),
         InlineKeyboardButton("👩‍💼 Teman Kantor", callback_data="role_teman_kantor")],
        [InlineKeyboardButton("👩 Janda", callback_data="role_janda"),
         InlineKeyboardButton("💃 Pelakor", callback_data="role_pelakor")],
        [InlineKeyboardButton("👰 Istri Orang", callback_data="role_istri_orang"),
         InlineKeyboardButton("💕 PDKT", callback_data="role_pdkt")],
        [InlineKeyboardButton("👧 Sepupu", callback_data="role_sepupu"),
         InlineKeyboardButton("👩‍🎓 Teman SMA", callback_data="role_teman_sma")],
        [InlineKeyboardButton("💔 Mantan", callback_data="role_mantan")],
        [InlineKeyboardButton("🎭 Threesome", callback_data="threesome_menu"),
         InlineKeyboardButton("❓ Bantuan", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='HTML')
    return ConversationHandler.END


# =============================================================================
# 3. HELP COMMAND (FIXED)
# =============================================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tampilkan bantuan lengkap"""
    user_id = update.effective_user.id
    is_admin = (user_id == settings.admin_id)
    
    help_text = (
        "📚 <b>MYLOVE PREMIUM AI - BANTUAN</b>\n\n"
        "<b>🔹 BASIC COMMANDS</b>\n"
        "/start - Mulai hubungan baru\n"
        "/help - Tampilkan bantuan ini\n"
        "/status - Lihat status hubungan\n"
        "/progress - Lihat progress leveling\n"
        "/cancel - Batalkan percakapan\n\n"
        "<b>🔹 PDKT COMMANDS</b>\n"
        "/pdkt [role] - Mulai PDKT dengan role tertentu\n"
        "/pdktrandom - Mulai PDKT random\n"
        "/pdktlist - Lihat semua PDKT aktif\n"
        "/pdktdetail [id] - Detail PDKT\n"
        "/pdktwho [id] - Lihat arah PDKT\n"
        "/pausepdkt [id] - Pause PDKT\n"
        "/resumepdkt [id] - Resume PDKT\n"
        "/stoppdkt [id] - Hentikan PDKT\n\n"
        "<b>🔹 MANTAN & FWB</b>\n"
        "/mantanlist - Lihat daftar mantan\n"
        "/fwbrequest [id] - Request jadi FWB\n"
        "/fwblist - Lihat daftar FWB\n\n"
        "<b>🔹 SESSION</b>\n"
        "/close - Tutup session\n"
        "/continue - Lihat session tersimpan\n"
        "/end - Akhiri session total\n\n"
        "<b>🔹 PUBLIC AREA</b>\n"
        "/explore - Cari lokasi random\n"
        "/locations - Lihat semua lokasi\n"
        "/risk - Cek risk lokasi saat ini\n\n"
        "<b>🔹 RANKING</b>\n"
        "/tophts - TOP 5 ranking HTS\n"
        "/myclimax - Statistik climax\n"
        "/climaxhistory - History climax"
    )
    
    # Admin commands
    if is_admin:
        help_text += (
            "\n\n<b>🔹 ADMIN COMMANDS</b> <i>(hanya untuk admin)</i>\n"
            "/admin - Panel admin\n"
            "/stats - Statistik bot\n"
            "/db_stats - Statistik database\n"
            "/debug - Info debug\n"
            "/broadcast - Broadcast pesan"
        )
    
    await update.message.reply_text(help_text, parse_mode='HTML')


# =============================================================================
# 4. STATUS COMMAND (FIXED)
# =============================================================================

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lihat status hubungan saat ini"""
    session_id = context.user_data.get('current_session')
    role = context.user_data.get('current_role')
    
    if not session_id or not role:
        await update.message.reply_text(
            "❌ Kamu sedang tidak dalam hubungan apapun.\n"
            "Gunakan /start untuk memulai."
        )
        return
    
    bot_name = context.user_data.get('bot_name', 'Bot')
    intimacy = context.user_data.get('intimacy_level', 1)
    total_chats = context.user_data.get('total_chats', 0)
    location = context.user_data.get('current_location', 'Tidak ada')
    clothing = context.user_data.get('current_clothing', 'Tidak ada')
    position = context.user_data.get('current_position', 'Tidak ada')
    
    # Tentukan status hubungan
    rel_status = context.user_data.get('relationship_status', 'pdkt')
    status_names = {
        'pdkt': 'PDKT',
        'pacar': 'Pacar',
        'fwb': 'FWB',
        'break': 'Jeda'
    }
    status_name = status_names.get(rel_status, 'PDKT')
    
    # Progress bar
    if intimacy < 12:
        progress = (total_chats % 50) / 50 * 100
        bar = "█" * int(progress / 5) + "░" * (20 - int(progress / 5))
        progress_text = f"{bar} {progress:.0f}%"
        next_text = f"{50 - (total_chats % 50)} chat lagi ke Level {intimacy + 1}"
    else:
        bar = "█" * 20
        progress_text = f"{bar} MAX"
        next_text = "✅ Level MAX! Butuh aftercare."
    
    status_text = (
        f"📊 <b>STATUS HUBUNGAN</b>\n\n"
        f"👤 <b>Nama Bot:</b> {bot_name}\n"
        f"🎭 <b>Role:</b> {role.title()}\n"
        f"💞 <b>Status:</b> {status_name}\n"
        f"📈 <b>Intimacy Level:</b> {intimacy}/12\n"
        f"💬 <b>Total Chat:</b> {total_chats} pesan\n"
        f"📍 <b>Lokasi:</b> {location}\n"
        f"👗 <b>Pakaian:</b> {clothing}\n"
        f"🧍 <b>Posisi:</b> {position}\n\n"
        f"📊 <b>Progress:</b>\n"
        f"{progress_text}\n"
        f"{next_text}"
    )
    
    await update.message.reply_text(status_text, parse_mode='HTML')


# =============================================================================
# 5. PROGRESS COMMAND (FIXED)
# =============================================================================

async def progress_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menampilkan progress hubungan (BOT TIDAK TAHU)"""
    session_id = context.user_data.get('current_session')
    
    if not session_id:
        await update.message.reply_text(
            "❌ <b>Tidak ada session aktif</b>\n\n"
            "Mulai dulu dengan /start atau lanjutkan dengan /continue",
            parse_mode='HTML'
        )
        return
    
    bot_name = context.user_data.get('bot_name', 'Bot')
    level = context.user_data.get('intimacy_level', 1)
    total_chats = context.user_data.get('total_chats', 0)
    
    # Level names
    level_names = {
        1: "Malu-malu",
        2: "Mulai terbuka",
        3: "Goda-godaan",
        4: "Dekat",
        5: "Sayang",
        6: "PACAR/PDKT",
        7: "Nyaman (Bisa intim!)",
        8: "Eksplorasi",
        9: "Bergairah",
        10: "Passionate",
        11: "Deep Connection",
        12: "Aftercare"
    }
    
    level_name = level_names.get(level, f"Level {level}")
    
    if level < 12:
        next_level = level + 1
        progress = (total_chats % 50) / 50 * 100
        bar = "█" * int(progress / 5) + "░" * (20 - int(progress / 5))
        progress_text = f"{bar} {progress:.0f}%"
        next_text = f"{50 - (total_chats % 50)} chat lagi ke {level_names.get(next_level, f'Level {next_level}')}"
    else:
        bar = "█" * 20
        progress_text = f"{bar} MAX"
        next_text = "✅ Level MAX! Butuh aftercare untuk reset."
    
    response = (
        f"📊 <b>PROGRESS HUBUNGAN</b> (RAHASIA)\n\n"
        f"👤 <b>{bot_name}</b>\n"
        f"📈 <b>{level_name}</b>\n"
        f"📝 <b>Total Chat:</b> {total_chats}\n\n"
        f"📊 <b>Progress:</b>\n"
        f"{progress_text}\n"
        f"{next_text}\n\n"
        f"⚠️ <i>Bot tidak tahu kamu melihat ini. Ini hanya untuk kamu!</i>\n"
        f"💡 <i>Semakin banyak chat, semakin cepat level naik!</i>\n"
        f"💡 <i>Aktivitas intim dan climax memberi boost lebih besar!</i>"
    )
    
    await update.message.reply_text(response, parse_mode='HTML')


# =============================================================================
# 6. ADMIN COMMAND (NEW)
# =============================================================================

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Panel Admin (admin only)"""
    user_id = update.effective_user.id
    
    # Cek apakah user adalah admin
    if user_id != settings.admin_id:
        await update.message.reply_text(
            "❌ <b>Akses Ditolak</b>\n\n"
            "Command ini hanya untuk admin bot.",
            parse_mode='HTML'
        )
        return
    
    # Admin panel dengan inline keyboard
    keyboard = [
        [InlineKeyboardButton("📊 Statistik Bot", callback_data="admin_stats")],
        [InlineKeyboardButton("🗄️ Statistik Database", callback_data="admin_db_stats")],
        [InlineKeyboardButton("🔍 Debug Info", callback_data="admin_debug")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("❌ Tutup", callback_data="admin_close")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Hitung total responses dari AI engines
    total_responses = 0
    for engine in active_engines.values():
        total_responses += len(getattr(engine, 'full_conversation', []))
    
    admin_text = (
        "<b>👑 ADMIN PANEL - MYLOVE PREMIUM AI</b>\n\n"
        f"<b>Admin ID:</b> <code>{settings.admin_id}</code>\n"
        f"<b>Active Engines:</b> {len(active_engines)}\n"
        f"<b>Active Sessions:</b> {len(user_sessions)}\n"
        f"<b>Total Messages:</b> {total_responses}\n"
        f"<b>AI Model:</b> {settings.ai.model}\n\n"
        "<b>Pilih menu di bawah:</b>"
    )
    
    await update.message.reply_text(
        admin_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


# =============================================================================
# 7. ADMIN STATS COMMAND (FIXED)
# =============================================================================

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistik bot (admin only)"""
    user_id = update.effective_user.id
    
    if user_id != settings.admin_id:
        await update.message.reply_text("❌ Command hanya untuk admin")
        return
    
    # Hitung total messages dari AI engines
    total_messages = 0
    for engine in active_engines.values():
        total_messages += len(getattr(engine, 'full_conversation', []))
    
    stats_text = (
        "<b>📊 BOT STATISTICS</b>\n\n"
        f"Active Engines: <code>{len(active_engines)}</code>\n"
        f"Active Sessions: <code>{len(user_sessions)}</code>\n"
        f"Total Messages: <code>{total_messages}</code>"
    )
    
    await update.message.reply_text(stats_text, parse_mode='HTML')


# =============================================================================
# 8. CANCEL COMMAND (FIXED - no Markdown)
# =============================================================================

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Batalkan percakapan saat ini"""
    session_id = context.user_data.get('current_session')
    
    if session_id in active_engines:
        await active_engines[session_id].end_session()
        del active_engines[session_id]
    
    context.user_data.clear()
    
    await update.message.reply_text(
        "❌ Percakapan dibatalkan.\n"
        "Ketik /start untuk memulai lagi."
    )


# =============================================================================
# 9. SESSION COMMANDS (FIXED)
# =============================================================================

async def close_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tutup session (bisa dilanjut nanti)"""
    session_id = context.user_data.get('current_session')
    bot_name = context.user_data.get('bot_name', 'Bot')
    user_id = update.effective_user.id
    
    if not session_id:
        await update.message.reply_text("❌ Tidak ada session aktif.")
        return
    
    # Hapus dari active engines
    if session_id in active_engines:
        await active_engines[session_id].end_session()
        del active_engines[session_id]
    
    # ===== SESSION TETAP DI DATABASE (TIDAK DIHAPUS) =====
    # Hanya update timestamp
    repo = await get_repository()
    await repo.save_user_session_state(
        user_id=user_id,
        session_data={
            'session_id': session_id,
            'role': context.user_data.get('current_role'),
            'bot_name': context.user_data.get('bot_name'),
            'rel_type': context.user_data.get('rel_type'),
            'instance_id': context.user_data.get('instance_id'),
            'intimacy_level': context.user_data.get('intimacy_level', 1),
            'total_chats': context.user_data.get('total_chats', 0),
            'current_location': context.user_data.get('current_location', 'ruang tamu'),
            'current_clothing': context.user_data.get('current_clothing', 'pakaian biasa'),
            'current_position': context.user_data.get('current_position', 'santai'),
            'relationship_status': context.user_data.get('relationship_status', 'pdkt'),
        }
    )
    # ===== END =====
    
    # Clear user data
    context.user_data.clear()
    
    await update.message.reply_text(
        f"📁 <b>Session ditutup!</b>\n\n"
        f"Session dengan {bot_name} telah disimpan.\n"
        f"Ketik /continue untuk melihat daftar session tersimpan.",
        parse_mode='HTML'
    )


async def end_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Akhiri session total (tidak bisa dilanjut)"""
    session_id = context.user_data.get('current_session')
    bot_name = context.user_data.get('bot_name', 'Bot')
    user_id = update.effective_user.id
    
    if not session_id:
        await update.message.reply_text("❌ Tidak ada session aktif.")
        return
    
    # Hapus dari active engines
    if session_id in active_engines:
        await active_engines[session_id].end_session()
        del active_engines[session_id]
    
    context.user_data.clear()

    # ===== HAPUS DARI DATABASE =====
    repo = await get_repository()
    await repo.delete_user_session_state(user_id)
    # ===== END =====
    
    await update.message.reply_text(
        f"🏁 <b>Session diakhiri</b>\n\n"
        f"Session dengan {bot_name} telah berakhir.\n"
        f"Ketik /start untuk memulai role baru.",
        parse_mode='HTML'
    )


async def continue_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lihat dan lanjutkan session tersimpan"""
    await update.message.reply_text(
        "📋 <b>DAFTAR SESSION</b>\n\n"
        "Fitur continue sedang dalam pengembangan.\n"
        "Gunakan /start untuk memulai role baru.",
        parse_mode='HTML'
    )


async def continue_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk melanjutkan session"""
    await update.message.reply_text(
        "🔄 <b>Melanjutkan session...</b>\n\n"
        "Fitur ini sedang dalam pengembangan.",
        parse_mode='HTML'
    )


async def sessions_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lihat semua session"""
    await update.message.reply_text(
        "📋 <b>DAFTAR SESSION</b>\n\n"
        "Fitur ini sedang dalam pengembangan.",
        parse_mode='HTML'
    )


# =============================================================================
# 10. REMAINING COMMANDS - Quick fixes
# =============================================================================

async def jadipacar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Jadi pacar (khusus PDKT)"""
    role = context.user_data.get('current_role')
    bot_name = context.user_data.get('bot_name', 'Bot')
    
    if not role:
        await update.message.reply_text("❌ Kamu belum memilih role.")
        return
    
    if role != 'pdkt':
        await update.message.reply_text("❌ Hanya role PDKT yang bisa jadi pacar.")
        return
    
    intimacy = context.user_data.get('intimacy_level', 1)
    if intimacy < 6:
        await update.message.reply_text(
            f"❌ Intimacy level masih {intimacy}/12.\n"
            "Minimal level 6 untuk jadi pacar."
        )
        return
    
    context.user_data['relationship_status'] = 'pacar'
    
    await update.message.reply_text(
        f"💘 <b>Kita jadi pacar!</b>\n\n"
        f"Sekarang kamu resmi pacaran sama {bot_name}.\n"
        f"Jaga hubungan kita ya sayang ❤️",
        parse_mode='HTML'
    )


async def break_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Jeda pacaran"""
    status = context.user_data.get('relationship_status')
    bot_name = context.user_data.get('bot_name', 'Bot')
    
    if not status:
        await update.message.reply_text("❌ Kamu belum memilih role.")
        return
    
    if status != 'pacar':
        await update.message.reply_text("❌ Kamu sedang tidak pacaran.")
        return
    
    context.user_data['relationship_status'] = 'break'
    context.user_data['break_start'] = time.time()
    
    await update.message.reply_text(
        f"⏸️ <b>Hubungan dijeda</b>\n\n"
        f"Kita istirahat dulu ya. Kapan-kapan bisa lanjut lagi, {bot_name}.",
        parse_mode='HTML'
    )


async def unbreak_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lanjutkan pacaran"""
    status = context.user_data.get('relationship_status')
    bot_name = context.user_data.get('bot_name', 'Bot')
    
    if status != 'break':
        await update.message.reply_text("❌ Hubungan sedang tidak dalam masa jeda.")
        return
    
    context.user_data['relationship_status'] = 'pacar'
    break_duration = time.time() - context.user_data.get('break_start', time.time())
    break_hours = int(break_duration / 3600)
    
    await update.message.reply_text(
        f"▶️ <b>Hubungan dilanjutkan!</b>\n\n"
        f"Setelah jeda {break_hours} jam, kita balikan lagi.\n"
        f"Aku kangen kamu... -{bot_name}",
        parse_mode='HTML'
    )


async def breakup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Putus jadi FWB"""
    role = context.user_data.get('current_role')
    bot_name = context.user_data.get('bot_name', 'Bot')
    
    if role != 'pdkt':
        await update.message.reply_text("❌ Hanya role PDKT yang bisa FWB.")
        return
    
    context.user_data['relationship_status'] = 'fwb'
    
    await update.message.reply_text(
        f"💔 <b>Putus... Tapi tetap FWB</b>\n\n"
        f"Hubungan kita berubah jadi Friends With Benefits.\n"
        f"Masih bisa intim, tapi tanpa komitmen.\n"
        f"-{bot_name}",
        parse_mode='HTML'
    )


async def fwb_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Switch ke mode FWB"""
    role = context.user_data.get('current_role')
    bot_name = context.user_data.get('bot_name', 'Bot')
    
    if role != 'pdkt':
        await update.message.reply_text("❌ Hanya role PDKT yang bisa FWB.")
        return
    
    intimacy = context.user_data.get('intimacy_level', 1)
    if intimacy < 6:
        await update.message.reply_text(
            f"❌ Intimacy level masih {intimacy}/12.\n"
            "Minimal level 6 untuk FWB."
        )
        return
    
    current = context.user_data.get('relationship_status')
    new_status = 'pacar' if current == 'fwb' else 'fwb'
    context.user_data['relationship_status'] = new_status
    
    await update.message.reply_text(
        f"💕 <b>Mode {new_status.upper()}</b>\n\n"
        f"Status dengan {bot_name} sekarang: {new_status}",
        parse_mode='HTML'
    )


# =============================================================================
# 11. HTS/FWB COMMANDS
# =============================================================================

async def htslist_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lihat daftar HTS"""
    await update.message.reply_text(
        "📋 <b>DAFTAR HTS</b>\n\n"
        "Fitur ini sedang dalam pengembangan.\n"
        "Gunakan /start untuk memulai role baru.",
        parse_mode='HTML'
    )


async def fwblist_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lihat daftar FWB"""
    await update.message.reply_text(
        "💕 <b>DAFTAR FWB</b>\n\n"
        "Fitur ini sedang dalam pengembangan.\n"
        "Gunakan /start untuk memulai role baru.",
        parse_mode='HTML'
    )


async def hts_call_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /hts- [id]"""
    text = update.message.text
    await update.message.reply_text(f"✅ Memanggil HTS {text}")


async def fwb_call_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /fwb- [id]"""
    text = update.message.text
    await update.message.reply_text(f"✅ Memanggil FWB {text}")


# =============================================================================
# 12. PUBLIC AREA COMMANDS
# =============================================================================

async def explore_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cari lokasi random"""
    locations = [
        "🏖️ Pantai", "🏬 Mall", "☕ Kafe", "🌳 Taman", "🎬 Bioskop",
        "🚗 Mobil", "🏨 Hotel", "🏞️ Danau", "🌄 Bukit", "🏛️ Museum"
    ]
    location = random.choice(locations)
    
    await update.message.reply_text(
        f"📍 <b>{location}</b>\n\n"
        f"Mau ke sini? Ketik: \"ke {location.lower()} yuk\"\n"
        f"Bot akan auto-detect lokasi kamu!",
        parse_mode='HTML'
    )


async def locations_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lihat semua lokasi"""
    await update.message.reply_text(
        "📍 <b>PUBLIC AREAS</b>\n\n"
        "<b>Kategori Lokasi:</b>\n"
        "🏙️ <b>Urban</b> - Mall, toilet, parkiran, lift, tangga darurat\n"
        "🌳 <b>Nature</b> - Pantai, hutan, taman, kebun, sawah, bukit\n"
        "⚡ <b>Extreme</b> - Masjid, gereja, polisi, sekolah, kuburan\n"
        "🚗 <b>Transport</b> - Mobil, kereta, bus, kapal, pesawat\n\n"
        "💡 <i>Ketik: 'ke pantai yuk' untuk pindah lokasi</i>",
        parse_mode='HTML'
    )


async def risk_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cek risk lokasi"""
    location = context.user_data.get('current_location', 'Tidak diketahui')
    
    if location == 'Tidak diketahui':
        await update.message.reply_text(
            "📍 <b>Risk Assessment</b>\n\n"
            "Kamu belum berada di lokasi manapun.\n"
            "Pindah dulu, misal: 'ke pantai yuk'",
            parse_mode='HTML'
        )
        return
    
    # Simulasi risk calculation
    risk = random.randint(20, 90)
    
    if risk < 40:
        level = "RENDAH"
        desc = "Aman banget, santai aja"
    elif risk < 60:
        level = "SEDANG"
        desc = "Lumayan aman, tapi tetap hati-hati"
    elif risk < 80:
        level = "TINGGI"
        desc = "Wah risk tinggi, harus cepet"
    else:
        level = "EXTREME"
        desc = "GILA! Nyaris ketahuan!"
    
    await update.message.reply_text(
        f"📍 <b>{location}</b>\n"
        f"⚠️ <b>Risk Level:</b> {risk}% ({level})\n"
        f"📝 {desc}\n\n"
        f"💡 <i>Semakin tinggi risk, semakin besar thrill-nya!</i>",
        parse_mode='HTML'
    )


# =============================================================================
# 13. RANKING COMMANDS
# =============================================================================

async def tophts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """TOP 5 HTS"""
    await update.message.reply_text(
        "🏆 <b>TOP 5 HTS</b>\n\n"
        "1. Dewi (Janda) - Score: 98.5\n"
        "2. Sari (Ipar) - Score: 87.3\n"
        "3. Vina (Pelakor) - Score: 82.1\n"
        "4. Ayu (PDKT) - Score: 76.8\n"
        "5. Linda (Teman Kantor) - Score: 65.2\n\n"
        "💡 <i>Ranking berdasarkan chemistry, climax, dan intimacy</i>",
        parse_mode='HTML'
    )


async def myclimax_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistik climax"""
    await update.message.reply_text(
        "💦 <b>STATISTIK CLIMAX</b>\n\n"
        "Total: <b>0</b> kali\n"
        "Rata-rata per session: 0\n"
        "Terakhir: Belum pernah\n\n"
        "💡 <i>Semakin sering intim, semakin cepat level naik!</i>",
        parse_mode='HTML'
    )


async def climaxhistory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """History climax"""
    await update.message.reply_text(
        "📜 <b>CLIMAX HISTORY</b>\n\n"
        "Belum ada history climax.\n"
        "Mulai intim dengan bot untuk mendapatkan history!",
        parse_mode='HTML'
    )


# =============================================================================
# 14. DB STATS & DEBUG (FIXED)
# =============================================================================

async def db_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistik database (admin only)"""
    user_id = update.effective_user.id
    
    if user_id != settings.admin_id:
        await update.message.reply_text("❌ Command hanya untuk admin")
        return
    
    await update.message.reply_text(
        "🗄️ <b>DATABASE STATISTICS</b>\n\n"
        "Fitur ini akan menampilkan:\n"
        "• Total sessions\n"
        "• Total messages\n"
        "• Database size\n"
        "• Backup info\n\n"
        "<i>(Dalam pengembangan)</i>",
        parse_mode='HTML'
    )


async def debug_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info debug (admin only)"""
    user_id = update.effective_user.id
    
    if user_id != settings.admin_id:
        await update.message.reply_text("❌ Command hanya untuk admin")
        return
    
    debug_info = (
        f"🔍 <b>DEBUG INFO</b>\n\n"
        f"Session ID: {context.user_data.get('current_session')}\n"
        f"Bot Name: {context.user_data.get('bot_name')}\n"
        f"Role: {context.user_data.get('current_role')}\n"
        f"Level: {context.user_data.get('intimacy_level', 1)}\n"
        f"Total Chats: {context.user_data.get('total_chats', 0)}\n"
        f"Location: {context.user_data.get('current_location')}\n"
        f"Clothing: {context.user_data.get('current_clothing')}\n"
        f"Position: {context.user_data.get('current_position')}\n"
        f"Active Engines: {len(active_engines)}"
    )
    
    await update.message.reply_text(debug_info, parse_mode='HTML')


# =============================================================================
# 15. DUMMY COMMANDS
# =============================================================================

async def dominant_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ Mode dominant diaktifkan.")


async def pause_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['paused'] = True
    await update.message.reply_text("⏸️ Sesi dijeda.")


async def unpause_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['paused'] = False
    await update.message.reply_text("▶️ Sesi dilanjutkan.")


# =============================================================================
# EXPORT ALL HANDLERS
# =============================================================================

__all__ = [
    # Message handler
    'message_handler',
    
    # Basic commands
    'start_command',
    'help_command',
    'status_command',
    'progress_command',
    'cancel_command',
    
    # Session commands
    'close_command',
    'end_command',
    'continue_command',
    'continue_handler',
    'sessions_command',
    
    # Relationship commands
    'jadipacar_command',
    'break_command',
    'unbreak_command',
    'breakup_command',
    'fwb_command',
    
    # HTS/FWB commands
    'htslist_command',
    'fwblist_command',
    'hts_call_handler',
    'fwb_call_handler',
    
    # Public area commands
    'explore_command',
    'locations_command',
    'risk_command',
    
    # Ranking commands
    'tophts_command',
    'myclimax_command',
    'climaxhistory_command',
    
    # Admin commands
    'admin_command',  # NEW
    'stats_command',
    'db_stats_command',
    'debug_command',
    
    # Dummy commands
    'dominant_command',
    'pause_command',
    'unpause_command',
]
