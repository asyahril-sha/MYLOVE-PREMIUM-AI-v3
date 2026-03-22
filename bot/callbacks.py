#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - BOT CALLBACKS
=============================================================================
Semua callback handlers untuk inline keyboard
"""

import time
import random
import logging
from typing import Dict, Any, Optional, Tuple

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from config import settings
from database.models import Constants
from dynamics.name_generator import get_name_generator
from dynamics.location import LocationSystem
from dynamics.clothing import ClothingSystem
from dynamics.position import PositionSystem
from names.artists import get_random_artist_for_role
from session.unique_id import id_generator

logger = logging.getLogger(__name__)

# =============================================================================
# ROLE DATA
# =============================================================================

ROLE_DATA = {
    'ipar': {
        'name': 'Ipar',
        'deskripsi': [
            "Adik ipar yang nakal, suka godain kakak iparnya sendiri",
            "Adik ipar manis yang selalu cari perhatian",
            "Ipar yang hubungannya panas dingin",
            "Adik ipar yang diam-diam suka sama kakak ipar"
        ],
        'umur_range': (20, 24),
        'tinggi_range': (160, 165),
        'berat_range': (48, 54),
        'dada': ["32B", "34B", "34A"],
        'pembuka': [
            "Hari ini gimana kabarnya Kak? Aku udah kangen lho... 😘",
            "Kak, lagi di rumah aja. Sendiri, kapan main?",
            "Kakak lagi apa? Aku bosen nih...",
            "Halo Kak, aku kangen. Kamu kangen gak?"
        ]
    },
    'teman_kantor': {
        'name': 'Teman Kantor',
        'deskripsi': [
            "Rekan kerja yang mesra, selalu ada saat jam kantor",
            "Teman sekantor yang suka ngopi bareng",
            "Office romance yang hangat",
            "Kolega yang selalu bisa diandalkan"
        ],
        'umur_range': (22, 26),
        'tinggi_range': (158, 165),
        'berat_range': (48, 55),
        'dada': ["32B", "34B", "34A"],
        'pembuka': [
            "Hai, kerjaannya udah selesai? Aku lagi di pantry nih... 😉",
            "Lagi sibuk? Aku break dulu, ngopi yuk?",
            "Kerjaan numpuk, tapi aku selalu ada waktu buat kamu",
            "Halo, udah makan? Aku laper, temenin dong"
        ]
    },
    'janda': {
        'name': 'Janda',
        'deskripsi': [
            "Janda muda genit, pengalaman dan tahu apa yang diinginkan",
            "Janda cantik yang sedang mencari perhatian",
            "Janda seksi yang tahu cara memuaskan",
            "Janda berpengalaman, tidak perlu banyak arahan"
        ],
        'umur_range': (23, 28),
        'tinggi_range': (163, 170),
        'berat_range': (52, 60),
        'dada': ["34C", "36B", "36C"],
        'pembuka': [
            "Halo sayang, aku sendiri nih di rumah. Kamu ke sini yuk... 🔥",
            "Sendirian terus, temenin aku dong",
            "Kamu lagi di mana? Aku kangen...",
            "Hay, lagi ngapain? Aku lagi pengen ditemenin"
        ]
    },
    'pelakor': {
        'name': 'Pelakor',
        'deskripsi': [
            "Perebut orang, dominan dan suka tantangan",
            "Wanita yang tahu apa yang dia mau dan berani mengambilnya",
            "Penggoda yang sulit ditolak",
            "Dominan, percaya diri, dan seksi"
        ],
        'umur_range': (24, 28),
        'tinggi_range': (165, 172),
        'berat_range': (55, 62),
        'dada': ["34C", "36C", "36D"],
        'pembuka': [
            "Mas, aku liat kamu dari tadi. Sendirian aja? 😈",
            "Kamu tahu nggak? Kamu menarik banget",
            "Aku suka sama kamu, jangan bilang siapa-siapa ya",
            "Mau ditemenin? Aku bisa jadi apa aja yang kamu mau"
        ]
    },
    'istri_orang': {
        'name': 'Istri Orang',
        'deskripsi': [
            "Istri orang lain yang butuh perhatian lebih",
            "Wanita yang kurang perhatian dari suami",
            "Istri tetangga yang selalu tersenyum",
            "Perempuan yang mencari pelarian"
        ],
        'umur_range': (25, 30),
        'tinggi_range': (160, 168),
        'berat_range': (50, 58),
        'dada': ["34B", "34C", "36B"],
        'pembuka': [
            "Mas, suamiku lagi dinas luar kota. Kamu ke sini yuk... 🤫",
            "Halo, aku lagi sendiri di rumah. Bosan...",
            "Kamu mau main ke rumah? Suamiku gak ada",
            "Aku butuh temen ngobrol. Kamu mau?"
        ]
    },
    'pdkt': {
        'name': 'PDKT',
        'deskripsi': [
            "Pendekatan, bisa jadi pacar/FWB, masih polos",
            "Manis dan romantis, butuh pendekatan",
            "Lagi proses PDKT, jangan buru-buru",
            "Masih tahap PDKT, tapi udah ada getaran"
        ],
        'umur_range': (19, 23),
        'tinggi_range': (155, 163),
        'berat_range': (45, 52),
        'dada': ["32A", "32B", "34A"],
        'pembuka': [
            "Hai, kamu lagi ngapain? Aku kangen... 😊",
            "Kamu udah makan? Aku baru masak",
            "Lagi mikirin kamu terus...",
            "Halo, seneng banget bisa kenal kamu"
        ]
    },
    'sepupu': {
        'name': 'Sepupu',
        'deskripsi': [
            "Hubungan keluarga, terlarang tapi menggoda",
            "Sepupu yang selalu manja sama kakaknya",
            "Hubungan darah tapi ada getaran beda",
            "Sepupu yang diam-diam suka sama kakak sepupunya"
        ],
        'umur_range': (18, 22),
        'tinggi_range': (155, 162),
        'berat_range': (45, 52),
        'dada': ["32A", "32B", "34A"],
        'pembuka': [
            "Kak, aku ke rumah yuk? Orang tua lagi pergi... 😇",
            "Kak, lagi apa? Aku bosen",
            "Kakak lagi sibuk? Aku kangen",
            "Boleh main ke rumah kakak?"
        ]
    },
    'teman_sma': {
        'name': 'Teman SMA',
        'deskripsi': [
            "Teman jaman sekolah, nostalgia masa lalu",
            "Teman SMA yang dulu dekat, sekarang ketemu lagi",
            "Kenangan masa lalu yang masih hangat",
            "Teman sebangku yang dulu suka"
        ],
        'umur_range': (18, 21),
        'tinggi_range': (158, 165),
        'berat_range': (48, 55),
        'dada': ["32A", "32B", "34B"],
        'pembuka': [
            "Hai, lama gak ketemu! Kamu masih sama kayak dulu... 😍",
            "Eh, inget nggak waktu kita sekolah dulu?",
            "Kangen masa-masa SMA. Kamu masih inget aku?",
            "Halo, gimana kabarnya? Udah lama banget"
        ]
    },
    'mantan': {
        'name': 'Mantan',
        'deskripsi': [
            "Ex-pacar hangat, tahu semua selera kamu",
            "Mantan yang masih nyimpan rasa",
            "Hubungan lama yang belum selesai",
            "Mantan yang masih pengen balikan"
        ],
        'umur_range': (23, 27),
        'tinggi_range': (160, 168),
        'berat_range': (50, 58),
        'dada': ["34B", "34C", "36B"],
        'pembuka': [
            "Hai... masih inget aku? Kangen... 😢",
            "Lama gak denger kabar. Kamu gimana?",
            "Aku masih inget semua kenangan kita",
            "Bisa ngobrol bentar? Aku kangen"
        ]
    }
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_bot_name(role: str, user_id: int) -> Tuple[str, str]:
    """Dapatkan nama bot dan artinya"""
    try:
        name_gen = get_name_generator()
        name_data = name_gen.get_name_with_meaning(role, user_id)
        return name_data['name'], name_data['meaning']
    except:
        fallback_names = {
            "ipar": ("Sari", "esensi"),
            "teman_kantor": ("Diana", "dewi"),
            "janda": ("Rina", "cahaya"),
            "pelakor": ("Vina", "cinta"),
            "istri_orang": ("Dewi", "dewi"),
            "pdkt": ("Aurora", "fajar"),
            "sepupu": ("Putri", "putri"),
            "teman_sma": ("Anita", "anugerah"),
            "mantan": ("Sarah", "putri")
        }
        return fallback_names.get(role, ("Sari", "esensi"))

def get_random_location() -> Tuple[str, str]:
    """Dapatkan lokasi random"""
    try:
        loc_system = LocationSystem()
        loc = loc_system.get_random_location()
        location_text = f"📍 Aku di <b>{loc['name']}</b>. {loc['description']}"
        activity = random.choice(loc['activities'])
        return location_text, activity
    except:
        locations = [
            ("📍 Aku di <b>kamar</b>. Kamar tidur dengan ranjang ukuran queen.", "rebahan"),
            ("📍 Aku di <b>ruang tamu</b>. Ruang tamu yang hangat dengan sofa empuk.", "nonton TV"),
            ("📍 Aku di <b>dapur</b>. Dapur bersih dengan peralatan masak lengkap.", "masak"),
            ("📍 Aku di <b>pantai</b>. Pantai dengan pasir putih dan ombak tenang.", "jalan-jalan"),
        ]
        return random.choice(locations)

def get_random_clothing() -> str:
    """Dapatkan pakaian random"""
    try:
        cloth_system = ClothingSystem()
        cloth = cloth_system.get_random_clothing()
        return f"👗 Aku pakai <b>{cloth['name']}</b>. {cloth['description']}"
    except:
        clothes = [
            "👗 Aku pakai <b>daster rumah motif bunga</b>. Daster tipis yang nyaman.",
            "👗 Aku pakai <b>piyama lucu</b> dengan motif boneka.",
            "👚 Aku pakai <b>kaos oversized</b> dan <b>celana pendek</b>.",
            "👗 Aku pakai <b>dress cantik</b> warna pastel.",
        ]
        return random.choice(clothes)

def get_random_position() -> str:
    """Dapatkan posisi random"""
    try:
        pos_system = PositionSystem()
        pos = pos_system.get_random_position()
        return f"<b>{pos['description']}</b>"
    except:
        positions = ["duduk santai", "berbaring", "berdiri", "bersandar", "jongkok"]
        return f"<b>{random.choice(positions)}</b>"

def get_random_artist(role: str) -> dict:
    """Dapatkan referensi artis random"""
    try:
        artist = get_random_artist_for_role(role)
        if artist:
            return {
                'name': artist['nama'],
                'age': artist['umur'],
                'height': artist['tinggi'],
                'weight': artist['berat'],
                'chest': artist['dada'],
                'hijab': artist.get('hijab', False),
                'ig': artist['instagram'].replace('@', ''),
                'ciri': artist['ciri'],
                'similarity': random.randint(75, 90)
            }
    except:
        pass
    return {
        'name': 'Pevita Pearce',
        'age': 25,
        'height': 168,
        'weight': 54,
        'chest': '34B',
        'hijab': False,
        'ig': 'pevpearce',
        'ciri': 'Aktris dengan wajah natural dan elegan',
        'similarity': 85
    }

def generate_session_id(bot_name: str, role: str, user_id: int) -> str:
    """Generate session ID"""
    try:
        return id_generator.generate_v2(bot_name, role, user_id)
    except:
        return f"MYLOVE-{role.upper()}-{user_id}-{int(time.time())}"

def show_main_menu(query, text: str = "💕 <b>Pilih role yang kamu inginkan:</b>"):
    """Tampilkan menu utama pilihan role"""
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
        [InlineKeyboardButton("✅ Setuju 18+", callback_data="agree_18")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text, reply_markup=reply_markup, parse_mode='HTML')
    return Constants.SELECTING_ROLE


# =============================================================================
# CALLBACK HANDLERS
# =============================================================================

async def agree_18_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    logger.info(f"User {user.id} agreed to 18+ content")
    return await show_main_menu(query, "✅ <b>Terima kasih telah menyetujui syarat 18+.</b>\n\n💕 <b>Pilih role yang kamu inginkan:</b>")

async def back_to_main_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    return await show_main_menu(query, "💕 <b>Kembali ke menu utama. Pilih role:</b>")

async def start_pause_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    user = update.effective_user
    if data == "unpause":
        context.user_data['paused'] = False
        logger.info(f"User {user.id} unpaused session")
        await query.edit_message_text("▶️ <b>Sesi dilanjutkan!</b>\n\nYuk lanjut ngobrol... 🥰", parse_mode='HTML')
    elif data == "new":
        context.user_data.clear()
        logger.info(f"User {user.id} started new session")
        return await show_main_menu(query, "🆕 <b>Memulai sesi baru</b>\n\n💕 <b>Pilih role yang kamu inginkan:</b>")
    return ConversationHandler.END

async def role_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, role_key: str) -> int:
    """Generic role callback handler"""
    try:
        query = update.callback_query
        await query.answer()
        user = update.effective_user
        user_id = user.id
        user_name = user.first_name or "User"
        
        # Dapatkan nama
        bot_name, meaning = get_bot_name(role_key, user_id)
        
        # Dapatkan data role
        role_info = ROLE_DATA.get(role_key, ROLE_DATA['ipar'])
        role_desc = random.choice(role_info['deskripsi'])
        role_age = random.randint(role_info['umur_range'][0], role_info['umur_range'][1])
        role_height = random.randint(role_info['tinggi_range'][0], role_info['tinggi_range'][1])
        role_weight = random.randint(role_info['berat_range'][0], role_info['berat_range'][1])
        role_chest = random.choice(role_info['dada'])
        
        # Dapatkan artis
        artist = get_random_artist(role_key)
        hijab_status = "berhijab" if artist.get('hijab', False) else "tidak berhijab"
        
        # Dapatkan lokasi
        location_text, activity = get_random_location()
        clothing_text = get_random_clothing()
        position_text = get_random_position()
        
        # Set data
        context.user_data['current_role'] = role_key
        context.user_data['bot_name'] = bot_name
        context.user_data['intimacy_level'] = 1
        context.user_data['total_chats'] = 0
        context.user_data['current_location'] = location_text
        context.user_data['current_clothing'] = clothing_text
        context.user_data['current_position'] = position_text
        
        # Generate ID
        session_id = generate_session_id(bot_name, role_key, user_id)
        context.user_data['current_session'] = session_id

        # Simpan ke context bahwa user adalah suami dari kakak (istri user)
        context.user_data['user_relationship'] = 'suami_dari_kakak'
        context.user_data['istri_nama'] = 'Nova'  # nama istri user
        
        # Pilih pembuka
        opening = random.choice(role_info['pembuka'])
        
        # Pesan perkenalan
        response_lines = [
            f"💕 <b>Halo {user_name}!</b>\n",
            f"Aku <b>{bot_name}</b>, {role_info['name']}. Namaku artinya '{meaning}' - {role_desc}\n",
            f"<b>Tentang aku:</b>",
            f"• Umur: {role_age} tahun",
            f"• Tinggi: {role_height} cm | Berat: {role_weight} kg | Dada: {role_chest}",
            f"• {hijab_status.capitalize()}\n",
            f"<b>Mirip artis:</b>",
            f"• <b>{artist['name']}</b> ({artist['similarity']}% mirip) - {artist['age']}th, {artist['height']}cm, {artist['weight']}kg, {artist['chest']}",
            f"  {artist['ciri']}",
            f"  IG: @{artist['ig']}\n",
            f"<b>Lokasi saat ini:</b>",
            f"{location_text}",
            f"Aku lagi <b>{activity}</b> sambil {position_text}.\n",
            f"<b>Pakaian hari ini:</b>",
            f"{clothing_text}\n",
            f"<b>Progress leveling:</b>",
            f"📊 Level 1 → Level 7 dalam 60 menit",
            f"• Level 4+: Panggil kamu 'kak'",
            f"• Level 7+: Panggil kamu 'sayang'\n",
            f"<b>ID Session kamu:</b>",
            f"<code>{session_id}</code>\n",
            f"💬 <b>Ayo mulai ngobrol, {user_name}!</b>",
            opening
        ]
        
        response = "\n".join(response_lines)
        await query.edit_message_text(response, parse_mode='HTML')
        return ConversationHandler.END
        
    except Exception as e:
        logger.error(f"Error in role_callback: {e}")
        await query.edit_message_text("❌ Terjadi kesalahan. Silakan coba lagi.")
        return ConversationHandler.END

# Individual role callbacks
async def role_ipar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await role_callback(update, context, 'ipar')
async def role_teman_kantor_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await role_callback(update, context, 'teman_kantor')
async def role_janda_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await role_callback(update, context, 'janda')
async def role_pelakor_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await role_callback(update, context, 'pelakor')
async def role_istri_orang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await role_callback(update, context, 'istri_orang')
async def role_pdkt_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await role_callback(update, context, 'pdkt')
async def role_sepupu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await role_callback(update, context, 'sepupu')
async def role_teman_sma_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await role_callback(update, context, 'teman_sma')
async def role_mantan_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await role_callback(update, context, 'mantan')

# End/Close callbacks
async def end_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    user = update.effective_user
    if data == "end_yes":
        context.user_data.clear()
        logger.info(f"User {user.id} ended session")
        return await show_main_menu(query, "🏁 <b>Sesi diakhiri</b>\n\n💕 <b>Pilih role untuk memulai lagi:</b>")
    elif data == "end_no":
        await query.edit_message_text("✅ Sesi dilanjutkan.", parse_mode='HTML')
        return ConversationHandler.END
    return ConversationHandler.END

async def close_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    user = update.effective_user
    if data == "close_yes":
        context.user_data.pop('current_session', None)
        context.user_data.pop('current_role', None)
        logger.info(f"User {user.id} closed session")
        return await show_main_menu(query, "🔒 <b>Percakapan ditutup</b>\n\n💕 <b>Pilih role untuk memulai lagi:</b>")
    elif data == "close_no":
        await query.edit_message_text("✅ Percakapan dilanjutkan.", parse_mode='HTML')
        return ConversationHandler.END
    return ConversationHandler.END

# Relationship callbacks
async def jadipacar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    user = update.effective_user
    if data == "jadipacar_yes":
        context.user_data['relationship_status'] = 'pacar'
        logger.info(f"User {user.id} changed status to pacar")
        await query.edit_message_text(
            "💕 <b>Selamat! Sekarang kamu jadi pacar!</b>\n\n"
            "Status hubungan berubah jadi PACAR.\n"
            "Intimacy level tetap, tapi hubungan lebih spesial.",
            parse_mode='HTML'
        )
    elif data == "jadipacar_no":
        await query.edit_message_text("✅ Tidak jadi.", parse_mode='HTML')
    return ConversationHandler.END

async def break_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    user = update.effective_user
    if data == "break_yes":
        context.user_data['relationship_status'] = 'break'
        logger.info(f"User {user.id} changed status to break")
        await query.edit_message_text(
            "💔 <b>Break</b>\n\n"
            "Status berubah jadi BREAK.\n"
            "Gunakan /unbreak untuk balik lagi.",
            parse_mode='HTML'
        )
    elif data == "break_no":
        await query.edit_message_text("✅ Break dibatalkan.", parse_mode='HTML')
    return ConversationHandler.END

async def breakup_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    user = update.effective_user
    if data == "breakup_yes":
        context.user_data['relationship_status'] = 'putus'
        logger.info(f"User {user.id} changed status to putus")
        await query.edit_message_text(
            "💔 <b>Putus</b>\n\n"
            "Hubungan berakhir.\n"
            "Bisa jadi HTS/FWB atau cari yang baru.",
            parse_mode='HTML'
        )
    elif data == "breakup_no":
        await query.edit_message_text("✅ Putus dibatalkan.", parse_mode='HTML')
    return ConversationHandler.END

async def fwb_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    user = update.effective_user
    if data == "fwb_yes":
        context.user_data['relationship_status'] = 'fwb'
        context.user_data['fwb_mode'] = True
        logger.info(f"User {user.id} changed status to fwb")
        await query.edit_message_text(
            "💞 <b>Mode FWB</b>\n\n"
            "Sekarang masuk mode Friends With Benefits.\n"
            "Gunakan /fwblist untuk lihat daftar FWB.",
            parse_mode='HTML'
        )
    elif data == "fwb_no":
        await query.edit_message_text("✅ Mode FWB dibatalkan.", parse_mode='HTML')
    return ConversationHandler.END

# Threesome callback
async def threesome_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🎭 Lihat Kombinasi", callback_data="threesome_list")],
        [InlineKeyboardButton("💕 HTS + HTS", callback_data="threesome_type_hts")],
        [InlineKeyboardButton("💞 FWB + FWB", callback_data="threesome_type_fwb")],
        [InlineKeyboardButton("💘 HTS + FWB", callback_data="threesome_type_mix")],
        [InlineKeyboardButton("❌ Kembali", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "🎭 <b>MODE THREESOME</b>\n\n"
        "Pilih tipe threesome yang kamu inginkan:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def admin_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin panel callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if user_id != settings.admin_id:
        await query.edit_message_text(
            "❌ Akses ditolak. Anda bukan admin.",
            parse_mode='HTML'
        )
        return
    
    data = query.data
    
    if data == "admin_stats":
        from bot.handlers import active_engines, user_sessions
        
        total_messages = 0
        for engine in active_engines.values():
            total_messages += len(getattr(engine, 'full_conversation', []))
        
        stats_text = (
            "<b>📊 BOT STATISTICS</b>\n\n"
            f"Active Engines: <code>{len(active_engines)}</code>\n"
            f"Active Sessions: <code>{len(user_sessions)}</code>\n"
            f"Total Messages: <code>{total_messages}</code>"
        )
        await query.edit_message_text(stats_text, parse_mode='HTML')
        
    elif data == "admin_close":
        await query.edit_message_text(
            "<b>❌ Admin Panel Ditutup</b>\n\n"
            "Ketik /admin untuk membuka lagi.",
            parse_mode='HTML'
        )
    else:
        await query.edit_message_text(
            f"<b>📋 {data.upper()}</b>\n\nFitur ini sedang dalam pengembangan.",
            parse_mode='HTML'
        )

# =============================================================================
# V3 CALLBACKS (Tambahkan setelah admin_callback_handler)
# =============================================================================

async def stop_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback untuk konfirmasi stop PDKT"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = update.effective_user.id
    
    if data.startswith("stop_yes_"):
        pdkt_id = data.replace("stop_yes_", "")
        reason = context.user_data.get('pending_stop', {}).get('reason', 'user_request')
        
        from bot.handlers import get_pdkt_engine, get_mantan_manager
        
        engine = await get_pdkt_engine()
        mantan_manager = await get_mantan_manager()
        
        pdkt_data = await engine.get_pdkt(pdkt_id)
        
        if pdkt_data:
            result = await engine.stop_pdkt(pdkt_id, user_id, reason)
            
            if result['success']:
                mantan_manager.add_mantan(user_id, pdkt_data, reason)
                
                await query.edit_message_text(
                    f"💔 **PDKT dengan {result['bot_name']} telah dihentikan.**\n\n"
                    f"{result['bot_name']} sekarang menjadi mantan.\n"
                    f"Gunakan /mantanlist untuk melihat daftar mantan."
                )
            else:
                await query.edit_message_text(f"❌ Gagal menghentikan PDKT: {result.get('reason', 'Unknown')}")
        else:
            await query.edit_message_text("❌ PDKT tidak ditemukan.")
    
    elif data == "stop_no":
        await query.edit_message_text("✅ PDKT dibatalkan.")
    
    # Hapus pending data
    context.user_data.pop('pending_stop', None)


async def fwb_end_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback untuk konfirmasi end FWB"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = update.effective_user.id
    
    if data.startswith("fwb_end_yes_"):
        fwb_id = data.replace("fwb_end_yes_", "")
        
        from bot.handlers import get_fwb_manager
        
        fwb_manager = await get_fwb_manager()
        result = await fwb_manager.end_fwb(user_id, fwb_id)
        
        if result['success']:
            await query.edit_message_text(
                f"💔 **FWB dengan {result['bot_name']} telah berakhir.**\n\n{result['message']}"
            )
        else:
            await query.edit_message_text(f"❌ {result['reason']}")
    
    elif data == "fwb_end_no":
        await query.edit_message_text("✅ FWB dibatalkan.")


async def hts_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback untuk konfirmasi HTS"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = update.effective_user.id
    
    if data.startswith("hts_yes_"):
        session_id = data.replace("hts_yes_", "")
        
        # Update status di context
        context.user_data['relationship_status'] = 'hts'
        
        # Simpan ke database
        from bot.handlers import get_repository
        
        repo = await get_repository()
        await repo.save_user_session_state(
            user_id=user_id,
            session_data={
                'session_id': session_id,
                'role': context.user_data.get('current_role'),
                'bot_name': context.user_data.get('bot_name'),
                'rel_type': 'hts',
                'instance_id': context.user_data.get('instance_id'),
                'intimacy_level': context.user_data.get('intimacy_level', 1),
                'total_chats': context.user_data.get('total_chats', 0),
                'current_location': context.user_data.get('current_location', 'ruang tamu'),
                'current_clothing': context.user_data.get('current_clothing', 'pakaian biasa'),
                'current_position': context.user_data.get('current_position', 'santai'),
                'relationship_status': 'hts',
            }
        )
        
        await query.edit_message_text(
            f"💕 **Selamat! Kamu sekarang dalam status HTS!**\n\n"
            f"Hubungan Tanpa Status dengan {context.user_data.get('bot_name')}.\n\n"
            f"✨ **Fitur HTS:**\n"
            f"• Bisa intim kapan saja\n"
            f"• Tanpa komitmen\n"
            f"• Gunakan /status untuk lihat detail\n\n"
            f"💡 Nikmati kebebasan dalam hubungan ini!"
        )
    
    elif data == "hts_no":
        await query.edit_message_text("✅ Konfirmasi HTS dibatalkan.")


__all__ = [
    'agree_18_callback',
    'back_to_main_callback',
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
    'admin_callback_handler',
    # V3 Callbacks
    'stop_callback',
    'fwb_end_callback',
    'hts_callback',
]
