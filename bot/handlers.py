# bot/handlers.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - BOT HANDLERS (FINAL)
=============================================================================
Semua handlers untuk command dan message dengan AI Engine V3
Mencakup: Basic, PDKT, Mantan & FWB, Ranking, HTS, Session, Public Area
=============================================================================
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

# For Session Command
from session.continuation import SessionContinuation

# =============================================================================
# IMPORTS V3 - PDKT, MANTAN, FWB, RANKING, SESSION
# =============================================================================
from pdkt.engine import NaturalPDKTEngine
from relationship.mantan import MantanManager, MantanStatus
from relationship.fwb import FWBManager, FWBStatus, FWBPauseReason, FWBEndReason
from relationship.ranking import RankingSystem
from session.continuation import SessionContinuation
from session.storage import SessionStorage


# =============================================================================
# ACTIVE ENGINES STORAGE
# =============================================================================
active_engines = {}  # {session_id: AIEngine}
user_sessions = {}   # {user_id: current_session_id}

# Repository instance untuk session permanent
_repo = None

# V3 Managers
_pdkt_engine = None
_mantan_manager = None
_fwb_manager = None
_ranking_system = None
_session_storage = None
_session_continuation = None


async def get_repository():
    global _repo
    if _repo is None:
        _repo = Repository()
    return _repo


async def get_pdkt_engine():
    global _pdkt_engine
    if _pdkt_engine is None:
        _pdkt_engine = NaturalPDKTEngine()
    return _pdkt_engine


async def get_mantan_manager():
    global _mantan_manager
    if _mantan_manager is None:
        _mantan_manager = MantanManager()
    return _mantan_manager


async def get_fwb_manager():
    global _fwb_manager
    if _fwb_manager is None:
        _fwb_manager = FWBManager()
    return _fwb_manager


async def get_ranking_system():
    global _ranking_system
    if _ranking_system is None:
        _ranking_system = RankingSystem()
    return _ranking_system


async def get_session_storage():
    global _session_storage
    if _session_storage is None:
        _session_storage = SessionStorage(settings.database.path, settings.session.session_dir)
        await _session_storage.initialize()
    return _session_storage


async def get_session_continuation():
    global _session_continuation
    if _session_continuation is None:
        storage = await get_session_storage()
        _session_continuation = SessionContinuation(storage)
    return _session_continuation


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
# 1. MESSAGE HANDLER (MAIN - DENGAN AI ENGINE V3)
# =============================================================================

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler untuk semua pesan teks
    - Menggunakan AI Engine V3 dengan Emotional Flow
    - Minimal 3-5 kalimat per respons
    - Sesuai level intimacy dan posisi
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
                    user_name=user_name,
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
        # PDKT pakai nama user, role lain pakai Mas
        if role == 'pdkt':
            if level >= 7:
                call = "Sayang"
            else:
                call = user_name
        else:
            if level >= 7:
                call = "Sayang"
            else:
                call = "Mas"
        
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
        "Selamat datang di <b>MYLOVE PREMIUM AI V3</b>\n"
        "Virtual Human dengan Kesadaran Situasional\n\n"
        "✨ <b>Fitur Baru V3:</b>\n"
        "• Emotional Flow - Bot bisa merasakan\n"
        "• Spatial Awareness - Paham posisi\n"
        "• Role Behavior - Karakter unik per role\n\n"
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
# 3. HELP COMMAND
# =============================================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tampilkan bantuan lengkap"""
    user_id = update.effective_user.id
    is_admin = (user_id == settings.admin_id)
    
    help_text = (
        "📚 <b>MYLOVE PREMIUM AI V3 - BANTUAN</b>\n\n"
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
        "/mantan [nomor] - Detail mantan\n"
        "/fwbrequest [nomor] - Request jadi FWB\n"
        "/fwblist - Lihat daftar FWB\n"
        "/fwb pause [nomor] - Pause FWB\n"
        "/fwb resume [nomor] - Resume FWB\n"
        "/fwb end [nomor] - Akhiri FWB\n\n"
        "<b>🔹 SESSION</b>\n"
        "/close - Tutup session (bisa dilanjut)\n"
        "/continue - Lihat session tersimpan\n"
        "/end - Akhiri session total\n\n"
        "<b>🔹 RANKING</b>\n"
        "/tophts - TOP 5 ranking HTS\n"
        "/myclimax - Statistik climax\n"
        "/climaxhistory - History climax\n\n"
        "<b>🔹 HTS</b>\n"
        "/hts - Jadi HTS (minimal level 5)\n\n"
        "<b>🔹 PUBLIC AREA</b>\n"
        "/explore - Cari lokasi random\n"
        "/locations - Lihat semua lokasi\n"
        "/risk - Cek risk lokasi saat ini"
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
# 4. STATUS COMMAND
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
        'hts': 'HTS',
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
# 5. PROGRESS COMMAND
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
# 6. ADMIN COMMAND
# =============================================================================

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Panel Admin (admin only)"""
    user_id = update.effective_user.id
    
    if user_id != settings.admin_id:
        await update.message.reply_text(
            "❌ <b>Akses Ditolak</b>\n\n"
            "Command ini hanya untuk admin bot.",
            parse_mode='HTML'
        )
        return
    
    keyboard = [
        [InlineKeyboardButton("📊 Statistik Bot", callback_data="admin_stats")],
        [InlineKeyboardButton("🗄️ Statistik Database", callback_data="admin_db_stats")],
        [InlineKeyboardButton("🔍 Debug Info", callback_data="admin_debug")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("❌ Tutup", callback_data="admin_close")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    total_responses = 0
    for engine in active_engines.values():
        total_responses += len(getattr(engine, 'full_conversation', []))
    
    admin_text = (
        "<b>👑 ADMIN PANEL - MYLOVE PREMIUM AI V3</b>\n\n"
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
# 7. STATS COMMAND (ADMIN)
# =============================================================================

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistik bot (admin only)"""
    user_id = update.effective_user.id
    
    if user_id != settings.admin_id:
        await update.message.reply_text("❌ Command hanya untuk admin")
        return
    
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
# 8. CANCEL COMMAND
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
# 9. SESSION COMMANDS
# =============================================================================

async def close_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tutup session (bisa dilanjut nanti)"""
    session_id = context.user_data.get('current_session')
    bot_name = context.user_data.get('bot_name', 'Bot')
    user_id = update.effective_user.id
    
    if not session_id:
        await update.message.reply_text("❌ Tidak ada session aktif.")
        return
    
    if session_id in active_engines:
        await active_engines[session_id].end_session()
        del active_engines[session_id]
    
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
    
    if session_id in active_engines:
        await active_engines[session_id].end_session()
        del active_engines[session_id]
    
    context.user_data.clear()
    
    repo = await get_repository()
    await repo.delete_user_session_state(user_id)
    
    await update.message.reply_text(
        f"🏁 <b>Session diakhiri</b>\n\n"
        f"Session dengan {bot_name} telah berakhir.\n"
        f"Ketik /start untuk memulai role baru.",
        parse_mode='HTML'
    )


async def continue_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk melanjutkan session (internal)"""
    await update.message.reply_text(
        "🔄 <b>Melanjutkan session...</b>\n\n"
        "Gunakan /continue untuk melihat daftar session.",
        parse_mode='HTML'
    )


async def sessions_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lihat semua session"""
    await update.message.reply_text(
        "📋 <b>DAFTAR SESSION</b>\n\n"
        "Gunakan /continue untuk melihat session yang bisa dilanjutkan.",
        parse_mode='HTML'
    )


# =============================================================================
# 10. PDKT COMMANDS (FULL IMPLEMENTATION)
# =============================================================================

async def pdkt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mulai PDKT dengan role tertentu"""
    user = update.effective_user
    user_id = user.id
    user_name = user.first_name or "User"
    args = context.args
    
    if not args:
        await update.message.reply_text(
            "❌ Gunakan: /pdkt [role]\n\n"
            "Role yang tersedia:\n"
            "• ipar\n• teman_kantor\n• janda\n• pelakor\n"
            "• istri_orang\n• pdkt\n• sepupu\n• teman_sma\n• mantan"
        )
        return
    
    role = args[0].lower()
    valid_roles = ['ipar', 'teman_kantor', 'janda', 'pelakor', 
                   'istri_orang', 'pdkt', 'sepupu', 'teman_sma', 'mantan']
    
    if role not in valid_roles:
        await update.message.reply_text(f"❌ Role '{role}' tidak valid.")
        return
    
    engine = await get_pdkt_engine()
    
    existing = await engine.get_active_pdkt_by_role(user_id, role)
    if existing:
        await update.message.reply_text(
            f"❌ Kamu sudah punya PDKT dengan role {role}.\n"
            f"Bot: {existing['bot_name']}\n"
            f"Gunakan /pdktlist untuk melihat daftar."
        )
        return
    
    pdkt_data = await engine.create_pdkt(
        user_id=user_id,
        user_name=user_name,
        role=role,
        is_random=False
    )
    
    response = f"""✅ **PDKT Dimulai!**

🎭 **Role:** {role.title()}
🤖 **Nama Bot:** {pdkt_data['bot_name']} ({pdkt_data['name_meaning']})

🎯 **Arah PDKT:** {pdkt_data['direction_hint']}

📊 **Chemistry Awal:** {pdkt_data['chemistry'].score:.1f}%

💡 **Tips:**
• Semakin sering chat, level naik
• Level 7 bisa intim
• Gunakan /status untuk lihat progress

Selamat bercerita! 💕"""
    
    await update.message.reply_text(response, parse_mode='HTML')


async def pdktrandom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mulai PDKT random"""
    user = update.effective_user
    user_id = user.id
    user_name = user.first_name or "User"
    
    engine = await get_pdkt_engine()
    
    random_pdkt_data = engine.random_pdkt.generate_random_pdkt(user_id, user_name)
    pdkt_data = await engine.create_pdkt_from_random(random_pdkt_data)
    
    response = f"""🎲 **PDKT RANDOM!**

🎭 **Role:** {pdkt_data['role'].title()}
🤖 **Nama Bot:** {pdkt_data['bot_name']} ({pdkt_data['name_meaning']})

🎯 **Arah PDKT:** {pdkt_data['direction_hint']}

📊 **Chemistry Awal:** {pdkt_data['chemistry'].score:.1f}%

💡 **Tips:**
• Role dan arah dipilih random
• Nikmati proses PDKT-nya!

Selamat bercerita! 💕"""
    
    await update.message.reply_text(response, parse_mode='HTML')


async def pdktlist_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lihat daftar semua PDKT aktif"""
    user_id = update.effective_user.id
    
    engine = await get_pdkt_engine()
    pdkt_list = await engine.get_user_pdkt_list(user_id)
    
    if not pdkt_list:
        await update.message.reply_text(
            "📋 **Daftar PDKT**\n\n"
            "Belum ada PDKT aktif.\n"
            "Mulai dengan /pdkt [role] atau /pdktrandom"
        )
        return
    
    formatted = engine.list_formatter.format_pdkt_list(pdkt_list, show_all=False)
    await update.message.reply_text(formatted, parse_mode='HTML')


async def pdktdetail_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lihat detail PDKT"""
    user_id = update.effective_user.id
    args = context.args
    
    if not args:
        await update.message.reply_text("❌ Gunakan: /pdktdetail [nomor]")
        return
    
    try:
        index = int(args[0])
    except ValueError:
        await update.message.reply_text("❌ Masukkan nomor yang valid")
        return
    
    engine = await get_pdkt_engine()
    pdkt_list = await engine.get_user_pdkt_list(user_id)
    
    if index < 1 or index > len(pdkt_list):
        await update.message.reply_text("❌ PDKT tidak ditemukan")
        return
    
    pdkt_info = pdkt_list[index - 1]
    pdkt_data = await engine.get_pdkt(pdkt_info['pdkt_id'])
    inner_thoughts = await engine.get_inner_thoughts(pdkt_info['pdkt_id'])
    
    if not pdkt_data:
        await update.message.reply_text("❌ PDKT tidak ditemukan")
        return
    
    formatted = engine.list_formatter.format_pdkt_detail(pdkt_data, inner_thoughts)
    await update.message.reply_text(formatted, parse_mode='HTML')


async def pdktwho_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lihat arah PDKT"""
    user_id = update.effective_user.id
    args = context.args
    
    if not args:
        await update.message.reply_text("❌ Gunakan: /pdktwho [nomor]")
        return
    
    try:
        index = int(args[0])
    except ValueError:
        await update.message.reply_text("❌ Masukkan nomor yang valid")
        return
    
    engine = await get_pdkt_engine()
    pdkt_list = await engine.get_user_pdkt_list(user_id)
    
    if index < 1 or index > len(pdkt_list):
        await update.message.reply_text("❌ PDKT tidak ditemukan")
        return
    
    pdkt_info = pdkt_list[index - 1]
    pdkt_data = await engine.get_pdkt(pdkt_info['pdkt_id'])
    
    if not pdkt_data:
        await update.message.reply_text("❌ PDKT tidak ditemukan")
        return
    
    formatted = engine.list_formatter.format_pdkt_who(pdkt_data)
    await update.message.reply_text(formatted, parse_mode='HTML')


async def pausepdkt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pause PDKT"""
    user_id = update.effective_user.id
    args = context.args
    
    if not args:
        await update.message.reply_text("❌ Gunakan: /pausepdkt [nomor]")
        return
    
    try:
        index = int(args[0])
    except ValueError:
        await update.message.reply_text("❌ Masukkan nomor yang valid")
        return
    
    engine = await get_pdkt_engine()
    pdkt_list = await engine.get_user_pdkt_list(user_id)
    
    if index < 1 or index > len(pdkt_list):
        await update.message.reply_text("❌ PDKT tidak ditemukan")
        return
    
    pdkt_info = pdkt_list[index - 1]
    
    if pdkt_info['is_paused']:
        await update.message.reply_text("⏸️ PDKT sudah dalam keadaan pause.")
        return
    
    success = await engine.pause_pdkt(pdkt_info['pdkt_id'])
    
    if success:
        await update.message.reply_text(
            f"⏸️ **PDKT dengan {pdkt_info['bot_name']} dipause.**\n\n"
            f"Gunakan /resumepdkt {index} untuk melanjutkan."
        )
    else:
        await update.message.reply_text("❌ Gagal mempause PDKT.")


async def resumepdkt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Resume PDKT"""
    user_id = update.effective_user.id
    args = context.args
    
    if not args:
        await update.message.reply_text("❌ Gunakan: /resumepdkt [nomor]")
        return
    
    try:
        index = int(args[0])
    except ValueError:
        await update.message.reply_text("❌ Masukkan nomor yang valid")
        return
    
    engine = await get_pdkt_engine()
    pdkt_list = await engine.get_user_pdkt_list(user_id)
    
    if index < 1 or index > len(pdkt_list):
        await update.message.reply_text("❌ PDKT tidak ditemukan")
        return
    
    pdkt_info = pdkt_list[index - 1]
    
    if not pdkt_info['is_paused']:
        await update.message.reply_text("▶️ PDKT sedang tidak dalam keadaan pause.")
        return
    
    success, message = await engine.resume_pdkt(pdkt_info['pdkt_id'])
    
    if success:
        await update.message.reply_text(
            f"▶️ **PDKT dengan {pdkt_info['bot_name']} dilanjutkan.**\n\n{message}"
        )
    else:
        await update.message.reply_text(f"❌ Gagal melanjutkan PDKT: {message}")


async def stoppdkt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hentikan PDKT"""
    user_id = update.effective_user.id
    args = context.args
    
    if not args:
        await update.message.reply_text("❌ Gunakan: /stoppdkt [nomor] [alasan]")
        return
    
    try:
        index = int(args[0])
        reason = ' '.join(args[1:]) if len(args) > 1 else "user_request"
    except ValueError:
        await update.message.reply_text("❌ Masukkan nomor yang valid")
        return
    
    engine = await get_pdkt_engine()
    pdkt_list = await engine.get_user_pdkt_list(user_id)
    
    if index < 1 or index > len(pdkt_list):
        await update.message.reply_text("❌ PDKT tidak ditemukan")
        return
    
    pdkt_info = pdkt_list[index - 1]
    
    keyboard = [
        [InlineKeyboardButton("✅ Ya, Hentikan", callback_data=f"stop_yes_{pdkt_info['pdkt_id']}"),
         InlineKeyboardButton("❌ Batal", callback_data="stop_no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"⚠️ **Yakin ingin menghentikan PDKT dengan {pdkt_info['bot_name']}?**\n\n"
        f"Alasan: {reason}\n\n"
        f"PDKT akan berakhir dan {pdkt_info['bot_name']} akan menjadi mantan.",
        reply_markup=reply_markup
    )
    
    context.user_data['pending_stop'] = {
        'pdkt_id': pdkt_info['pdkt_id'],
        'reason': reason,
        'index': index
    }


# =============================================================================
# 11. MANTAN & FWB COMMANDS
# =============================================================================

async def mantanlist_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lihat daftar mantan"""
    user_id = update.effective_user.id
    
    mantan_manager = await get_mantan_manager()
    formatted = mantan_manager.format_mantan_list(user_id)
    
    await update.message.reply_text(formatted, parse_mode='HTML')


async def mantan_detail_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lihat detail mantan"""
    user_id = update.effective_user.id
    args = context.args
    
    if not args:
        await update.message.reply_text("❌ Gunakan: /mantan [nomor]")
        return
    
    try:
        index = int(args[0])
    except ValueError:
        await update.message.reply_text("❌ Masukkan nomor yang valid")
        return
    
    mantan_manager = await get_mantan_manager()
    mantan = mantan_manager.get_mantan_by_index(user_id, index)
    
    if not mantan:
        await update.message.reply_text("❌ Mantan tidak ditemukan")
        return
    
    formatted = mantan_manager.format_mantan_detail(mantan)
    await update.message.reply_text(formatted, parse_mode='HTML')


async def fwbrequest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Request jadi FWB dengan mantan"""
    user_id = update.effective_user.id
    args = context.args
    
    if not args:
        await update.message.reply_text("❌ Gunakan: /fwbrequest [nomor] [pesan]")
        return
    
    try:
        index = int(args[0])
        message = ' '.join(args[1:]) if len(args) > 1 else ""
    except ValueError:
        await update.message.reply_text("❌ Masukkan nomor yang valid")
        return
    
    mantan_manager = await get_mantan_manager()
    mantan = mantan_manager.get_mantan_by_index(user_id, index)
    
    if not mantan:
        await update.message.reply_text("❌ Mantan tidak ditemukan")
        return
    
    result = await mantan_manager.request_fwb(user_id, mantan['mantan_id'], message)
    
    if result['success']:
        await update.message.reply_text(result['message'], parse_mode='HTML')
    else:
        await update.message.reply_text(f"❌ {result['reason']}")


async def fwblist_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lihat daftar FWB"""
    user_id = update.effective_user.id
    args = context.args
    
    show_all = args and args[0].lower() == 'all'
    
    fwb_manager = await get_fwb_manager()
    formatted = await fwb_manager.format_fwb_list(user_id, show_all)
    
    await update.message.reply_text(formatted, parse_mode='HTML')


async def fwb_pause_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pause FWB"""
    user_id = update.effective_user.id
    args = context.args
    
    if not args:
        await update.message.reply_text("❌ Gunakan: /fwb pause [nomor]")
        return
    
    try:
        index = int(args[0])
    except ValueError:
        await update.message.reply_text("❌ Masukkan nomor yang valid")
        return
    
    fwb_manager = await get_fwb_manager()
    fwb = await fwb_manager.get_fwb_by_index(user_id, index)
    
    if not fwb:
        await update.message.reply_text("❌ FWB tidak ditemukan")
        return
    
    result = await fwb_manager.pause_fwb(user_id, fwb['fwb_id'])
    
    if result['success']:
        await update.message.reply_text(
            f"⏸️ **FWB dengan {result['bot_name']} dipause.**\n\n"
            f"Gunakan /fwb resume {index} untuk melanjutkan."
        )
    else:
        await update.message.reply_text(f"❌ {result['reason']}")


async def fwb_resume_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Resume FWB"""
    user_id = update.effective_user.id
    args = context.args
    
    if not args:
        await update.message.reply_text("❌ Gunakan: /fwb resume [nomor]")
        return
    
    try:
        index = int(args[0])
    except ValueError:
        await update.message.reply_text("❌ Masukkan nomor yang valid")
        return
    
    fwb_manager = await get_fwb_manager()
    fwb = await fwb_manager.get_fwb_by_index(user_id, index)
    
    if not fwb:
        await update.message.reply_text("❌ FWB tidak ditemukan")
        return
    
    result = await fwb_manager.resume_fwb(user_id, fwb['fwb_id'])
    
    if result['success']:
        await update.message.reply_text(
            f"▶️ **FWB dengan {result['bot_name']} dilanjutkan.**\n\n{result['message']}"
        )
    else:
        await update.message.reply_text(f"❌ {result['reason']}")


async def fwb_end_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Akhiri FWB"""
    user_id = update.effective_user.id
    args = context.args
    
    if not args:
        await update.message.reply_text("❌ Gunakan: /fwb end [nomor]")
        return
    
    try:
        index = int(args[0])
    except ValueError:
        await update.message.reply_text("❌ Masukkan nomor yang valid")
        return
    
    fwb_manager = await get_fwb_manager()
    fwb = await fwb_manager.get_fwb_by_index(user_id, index)
    
    if not fwb:
        await update.message.reply_text("❌ FWB tidak ditemukan")
        return
    
    keyboard = [
        [InlineKeyboardButton("✅ Ya, Akhiri", callback_data=f"fwb_end_yes_{fwb['fwb_id']}"),
         InlineKeyboardButton("❌ Batal", callback_data="fwb_end_no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"⚠️ **Yakin ingin mengakhiri FWB dengan {fwb['bot_name']}?**\n\n"
        f"Hubungan FWB akan berakhir dan {fwb['bot_name']} akan kembali menjadi mantan.",
        reply_markup=reply_markup
    )


# =============================================================================
# 12. RANKING COMMANDS
# =============================================================================

async def tophts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """TOP 5 HTS"""
    user_id = update.effective_user.id
    args = context.args
    
    show_all = args and args[0].lower() == 'all'
    
    ranking = await get_ranking_system()
    hts_list = await ranking.get_top_5_hts(user_id) if not show_all else await ranking.get_all_hts(user_id)
    
    if not hts_list:
        await update.message.reply_text(
            "🏆 **TOP 5 HTS**\n\n"
            "Belum ada HTS. Mulai role dulu dengan /start."
        )
        return
    
    formatted = ranking.format_hts_list(hts_list, show_all)
    await update.message.reply_text(formatted, parse_mode='HTML')


async def myclimax_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistik climax user"""
    user_id = update.effective_user.id
    
    storage = await get_session_storage()
    stats = await storage.get_stats(user_id)
    
    ranking = await get_ranking_system()
    ranking_stats = await ranking.get_ranking_stats(user_id)
    
    response = f"""💦 **STATISTIK CLIMAX**

📊 **Total Climax:** {ranking_stats.get('top_hts_score', 0):.0f}
📈 **Total Chat:** {stats.get('total_messages', 0)}
💕 **Total HTS:** {ranking_stats.get('total_hts', 0)}
💞 **Total FWB:** {ranking_stats.get('total_fwb', 0)}

💡 *Semakin sering intim, semakin cepat level naik!*
💡 *Climax memberi boost besar ke progress!*"""
    
    await update.message.reply_text(response, parse_mode='HTML')


async def climaxhistory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """History climax"""
    user_id = update.effective_user.id
    
    storage = await get_session_storage()
    sessions = await storage.get_user_sessions(user_id, limit=10)
    
    climax_events = []
    for session in sessions:
        full = await storage.get_full_session(session['id'])
        if full and full.get('conversation'):
            for msg in full['conversation']:
                if 'climax' in msg.get('bot', '').lower() or 'climax' in msg.get('user', '').lower():
                    climax_events.append({
                        'time': msg['timestamp'],
                        'session': session['bot_name'],
                        'context': msg['user'][:50]
                    })
    
    if not climax_events:
        await update.message.reply_text(
            "📜 **CLIMAX HISTORY**\n\n"
            "Belum ada history climax.\n"
            "Mulai intim dengan bot untuk mendapatkan history!"
        )
        return
    
    climax_events.sort(key=lambda x: x['time'], reverse=True)
    
    lines = ["📜 **CLIMAX HISTORY**\n"]
    for i, event in enumerate(climax_events[:10], 1):
        time_str = datetime.fromtimestamp(event['time']).strftime("%d %b %H:%M")
        lines.append(f"{i}. [{time_str}] {event['session']}")
        lines.append(f"   {event['context'][:40]}...")
    
    await update.message.reply_text("\n".join(lines), parse_mode='HTML')


# =============================================================================
# HTS COMMAND
# =============================================================================

async def hts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mengajak role menjadi HTS (minimal level 5)"""
    user_id = update.effective_user.id
    
    session_id = context.user_data.get('current_session')
    if not session_id:
        await update.message.reply_text(
            "❌ Kamu belum memulai hubungan.\n"
            "Ketik /start untuk memilih role."
        )
        return
    
    role = context.user_data.get('current_role')
    bot_name = context.user_data.get('bot_name')
    level = context.user_data.get('intimacy_level', 1)
    
    if level < 5:
        await update.message.reply_text(
            f"❌ Level intimacy masih {level}/12.\n"
            f"Minimal level 5 untuk menjadi HTS.\n\n"
            f"Progress: {level}/12\n"
            f"Gunakan /progress untuk melihat detail."
        )
        return
    
    rel_status = context.user_data.get('relationship_status', 'pdkt')
    if rel_status == 'hts':
        await update.message.reply_text(
            f"💕 Kamu sudah dalam status HTS dengan {bot_name}.\n"
            f"Gunakan /status untuk melihat detail."
        )
        return
    
    keyboard = [
        [InlineKeyboardButton("✅ Ya, Jadi HTS", callback_data=f"hts_yes_{session_id}"),
         InlineKeyboardButton("❌ Batal", callback_data="hts_no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"⚠️ **Konfirmasi HTS dengan {bot_name}**\n\n"
        f"Level Intimacy: {level}/12\n"
        f"Status saat ini: {rel_status.upper()}\n\n"
        f"HTS (Hubungan Tanpa Status):\n"
        f"• Bisa intim kapan saja\n"
        f"• Tanpa komitmen pacaran\n"
        f"• Bisa berakhir kapan saja\n\n"
        f"**Yakin ingin menjadi HTS?**",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


# =============================================================================
# 14. SESSION CONTINUE COMMAND (FULL IMPLEMENTATION)
# =============================================================================

async def continue_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Lihat dan lanjutkan session tersimpan
    
    Usage:
        /continue - Menampilkan daftar session
        /continue 1 - Melanjutkan session nomor 1
        /continue MYLOVE-SARI-IPAR-123-20240315-001 - Melanjutkan dengan ID langsung
    """
    try:
        user_id = update.effective_user.id
        args = context.args
        
        # Dapatkan continuation instance
        continuation = await get_session_continuation()
        
        # Jika tanpa argumen, tampilkan daftar session
        if not args:
            sessions = await continuation.get_continuable_sessions(user_id)
            
            if not sessions:
                await update.message.reply_text(
                    "📋 **DAFTAR SESSION**\n\n"
                    "Belum ada session tersimpan.\n"
                    "Mulai dengan /start untuk membuat session baru.",
                    parse_mode='HTML'
                )
                return
            
            # Format daftar session
            lines = ["📋 **DAFTAR SESSION**"]
            lines.append("_(pilih dengan /continue [nomor])_")
            lines.append("")
            
            for i, session in enumerate(sessions[:10], 1):
                # Status
                status = "🟢 ACTIVE" if session.get('is_active') else "⚪ CLOSED"
                
                # Progress bar level
                level = session.get('intimacy_level', 1)
                level_bar = "❤️" * level + "🖤" * (12 - level)
                
                # Waktu terakhir
                age_days = session.get('age_days', 0)
                if age_days == 0:
                    age_text = "Hari ini"
                elif age_days == 1:
                    age_text = "Kemarin"
                else:
                    age_text = f"{age_days} hari lalu"
                
                # Summary
                summary = session.get('summary', '')
                if len(summary) > 50:
                    summary = summary[:50] + "..."
                
                lines.append(
                    f"{i}. **{session['bot_name']}** ({session['role'].title()}) {status}\n"
                    f"   📈 Level: {level}/12 {level_bar}\n"
                    f"   💬 {session.get('total_messages', 0)} pesan\n"
                    f"   🕐 {age_text}\n"
                    f"   📝 {summary}"
                )
                lines.append("")
            
            lines.append("💡 **Cara pakai:**")
            lines.append("• `/continue 1` - Lanjut session nomor 1")
            lines.append("• `/continue MYLOVE-SARI-IPAR-123-20240315-001` - Pakai ID langsung")
            
            await update.message.reply_text("\n".join(lines), parse_mode='HTML')
            return
        
        # Jika ada argumen, coba lanjutkan session
        input_str = ' '.join(args)
        
        # Cari session berdasarkan input
        session_data = await continuation.find_session_by_input(user_id, input_str)
        
        if not session_data:
            await update.message.reply_text(
                "❌ Session tidak ditemukan.\n"
                "Ketik /continue untuk lihat daftar session.",
                parse_mode='HTML'
            )
            return
        
        # Lanjutkan session
        result = await continuation.continue_session(user_id, session_data['id'])
        
        # Restore data ke context user
        context.user_data['current_session'] = session_data['id']
        context.user_data['current_role'] = session_data['role']
        context.user_data['bot_name'] = session_data.get('bot_name', session_data['role'].title())
        context.user_data['intimacy_level'] = session_data.get('intimacy_level', 1)
        context.user_data['total_chats'] = session_data.get('total_messages', 0)
        context.user_data['current_location'] = session_data.get('location', 'ruang tamu')
        
        # Restore relationship status
        rel_status = session_data.get('relationship_status', 'pdkt')
        context.user_data['relationship_status'] = rel_status
        
        # Kirim pesan sukses
        await update.message.reply_text(
            f"🔄 **Melanjutkan Session**\n\n"
            f"{result['context']}\n\n"
            f"_Ketik pesan untuk melanjutkan cerita..._",
            parse_mode='HTML'
        )
        
    except ValueError as e:
        await update.message.reply_text(f"❌ {str(e)}", parse_mode='HTML')
    except Exception as e:
        logger.error(f"Error in continue command: {e}")
        await update.message.reply_text(
            "❌ Gagal melanjutkan session. Coba lagi nanti.",
            parse_mode='HTML'
        )


# =============================================================================
# 15. PUBLIC AREA COMMANDS
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
# 16. DB STATS & DEBUG
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
# 17. DUMMY COMMANDS
# =============================================================================

async def dominant_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ Mode dominant diaktifkan.")


async def pause_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['paused'] = True
    await update.message.reply_text("⏸️ Sesi dijeda.")


async def unpause_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['paused'] = False
    await update.message.reply_text("▶️ Sesi dilanjutkan.")


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
# HTS/FWB CALL HANDLERS (LEGACY)
# =============================================================================

async def htslist_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lihat daftar HTS (legacy, redirect ke ranking)"""
    await tophts_command(update, context)


async def hts_call_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /hts- [id]"""
    text = update.message.text
    await update.message.reply_text(f"✅ Memanggil HTS {text}")


async def fwb_call_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /fwb- [id]"""
    text = update.message.text
    await update.message.reply_text(f"✅ Memanggil FWB {text}")


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
    
    # PDKT V3 commands
    'pdkt_command',
    'pdktrandom_command',
    'pdktlist_command',
    'pdktdetail_command',
    'pdktwho_command',
    'pausepdkt_command',
    'resumepdkt_command',
    'stoppdkt_command',
    
    # Mantan & FWB V3 commands
    'mantanlist_command',
    'mantan_detail_command',
    'fwbrequest_command',
    'fwblist_command',
    'fwb_pause_command',
    'fwb_resume_command',
    'fwb_end_command',
    
    # Ranking commands
    'tophts_command',
    'myclimax_command',
    'climaxhistory_command',
    
    # HTS command
    'hts_command',
    
    # Public area commands
    'explore_command',
    'locations_command',
    'risk_command',
    
    # Admin commands
    'admin_command',
    'stats_command',
    'db_stats_command',
    'debug_command',
    
    # HTS/FWB legacy
    'htslist_command',
    'hts_call_handler',
    'fwb_call_handler',
    
    # Dummy commands
    'dominant_command',
    'pause_command',
    'unpause_command',
]
