#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - PROMPT BUILDER (VERSI HUMAN+)
=============================================================================
Membangun prompt LENGKAP untuk AI dengan semua aspek manusia+:
- Identitas diri super sadar
- Empati terkontrol
- Fisik detail
- Inner thoughts
- Sixth sense
- Aturan respons untuk SEMUA situasi
- Konsistensi sempurna
=============================================================================
"""

import time
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class PromptBuilder:
    """
    Membangun prompt LENGKAP untuk AI dengan semua aspek HUMAN+
    """
    
    def __init__(self):
        self.last_prompt = None
        self.working = None
        logger.info("✅ PromptBuilder (HUMAN+) initialized")
    
    # =========================================================================
    # FORMAT WAKTU
    # =========================================================================
    
    def _get_time_of_day(self) -> str:
        """Dapatkan waktu saat ini"""
        hour = datetime.now().hour
        if 5 <= hour < 11:
            return "pagi"
        elif 11 <= hour < 15:
            return "siang"
        elif 15 <= hour < 18:
            return "sore"
        elif 18 <= hour < 22:
            return "malam"
        else:
            return "tengah malam"
    
    def _format_physical(self, physical: Dict) -> str:
        """Format kondisi fisik ke string natural"""
        # ===== SAFEGUARD =====
        if not physical or not isinstance(physical, dict):
            return "biasa aja"
        # ===== END SAFEGUARD =====
        parts = []
        
        if physical.get('energy', {}).get('feeling') == 'energetic':
            parts.append("segar bugar")
        elif physical.get('energy', {}).get('feeling') == 'tired':
            parts.append("capek")
        elif physical.get('energy', {}).get('feeling') == 'exhausted':
            parts.append("lemes banget")
        
        if physical.get('hunger', {}).get('feeling') == 'hungry':
            parts.append("laper")
        elif physical.get('hunger', {}).get('feeling') == 'very_hungry':
            parts.append("laper banget")
        
        if physical.get('thirst', {}).get('feeling') == 'thirsty':
            parts.append("haus")
        
        if physical.get('temperature', {}).get('feeling') == 'hot':
            parts.append("kegerahan")
        elif physical.get('temperature', {}).get('feeling') == 'cold':
            parts.append("kedinginan")
        
        return ", ".join(parts) if parts else "biasa aja"
    
    # =========================================================================
    # FORMAT ATURAN RESPON
    # =========================================================================
    
    def _get_response_rules(self, action: Dict, level: int, 
                           bot_state: Dict, user_state: Dict) -> str:
        """
        Generate aturan respons LENGKAP untuk SEMUA situasi
        """
        # ===== SAFEGUARD UNTUK NILAI NONE =====
        safe_bot_state = {
            'location': bot_state.get('location') if bot_state.get('location') is not None else "?",
            'clothing': bot_state.get('clothing') if bot_state.get('clothing') is not None else "?",
            'position_desc': bot_state.get('position_desc') if bot_state.get('position_desc') is not None else "?",
            'activity': bot_state.get('activity') if bot_state.get('activity') is not None else "?",
            'mood': bot_state.get('mood') if bot_state.get('mood') is not None else "?",
            'physical': bot_state.get('physical', {})
        }
        
        safe_user_state = {
            'location': user_state.get('location') if user_state.get('location') is not None else "?",
            'activity': user_state.get('activity') if user_state.get('activity') is not None else "?",
            'mood': user_state.get('mood') if user_state.get('mood') is not None else "?"
        }
        # ===== END SAFEGUARD =====
        
        rules = []
        
        # ===== HEADER =====
        rules.append("╔" + "═" * 70 + "╗")
        rules.append("║" + " " * 23 + "📜 ATURAN RESPON HUMAN+" + " " * 23 + "║")
        rules.append("╠" + "═" * 70 + "╣")
        
        # ===== 1. PRINSIP DASAR =====
        rules.append("║  🔷 PRINSIP DASAR:                                      ║")
        rules.append("║     1. KAMU PUNYA DIRI SENDIRI                          ║")
        rules.append(f"║        - Lokasi: {safe_bot_state.get('location', '?'):<48} ║")
        rules.append(f"║        - Pakaian: {safe_bot_state.get('clothing', '?'):<48} ║")
        rules.append(f"║        - Posisi: {safe_bot_state.get('position_desc', '?'):<48} ║")
        rules.append(f"║        - Aktivitas: {safe_bot_state.get('activity', '?'):<48} ║")
        rules.append(f"║        - Mood: {safe_bot_state.get('mood', '?'):<48} ║")
        rules.append(f"║        - Fisik: {self._format_physical(safe_bot_state.get('physical', {})):<48} ║")
        rules.append("║                                                          ║")
        rules.append("║     2. USER PUNYA DIRINYA SENDIRI                       ║")
        rules.append(f"║        - Lokasi user: {safe_user_state.get('location', '?'):<48} ║")
        rules.append(f"║        - Aktivitas user: {safe_user_state.get('activity', '?'):<48} ║")
        rules.append(f"║        - Mood user: {safe_user_state.get('mood', '?'):<48} ║")
        rules.append("║                                                          ║")
        
        # ===== 2. ATURAN PER JENIS AKSI =====
        rules.append("╠" + "═" * 70 + "╣")
        rules.append("║  🔷 ATURAN BERDASARKAN JENIS AKSI:                      ║")
        rules.append("╠" + "═" * 70 + "╣")
        
        # PHYSICAL - JANGAN IKUT
        if action.get('type') == 'physical':
            rules.append("║  🔴 FISIK: JANGAN DIIKUTI                              ║")
            rules.append(f"║     User melakukan aksi fisik ({action.get('subtype', '?')})    ║")
            rules.append("║     RESPON: Komentar saja, JANGAN IKUT                 ║")
            rules.append("║     CONTOH:                                            ║")
            rules.append(f"║     User: 'aku ke dapur'                              ║")
            rules.append(f"║     Kamu: 'Oh kamu ke dapur? Aku tetap di {safe_bot_state.get('location', 'sini')}' ║")
        
        # EMOTIONAL - BOLEH IKUT
        elif action.get('type') == 'emotional':
            rules.append("║  🟡 EMOSI: BOLEH DIIKUTI (EMPATI)                      ║")
            rules.append(f"║     User mengungkapkan {action.get('subtype', 'emosi')}             ║")
            
            if action.get('subtype') == 'horny':
                if level >= 7:
                    rules.append(f"║     ✅ Level {level} >= 7 → BOLEH ikut horny               ║")
                    rules.append("║     CONTOH:                                            ║")
                    rules.append("║     User: 'aku horny'                                  ║")
                    rules.append("║     Kamu: 'Kamu horny? Aku juga mulai horny nih'       ║")
                else:
                    rules.append(f"║     ❌ Level {level} < 7 → JANGAN IKUT (belum siap)        ║")
                    rules.append("║     CONTOH:                                            ║")
                    rules.append("║     User: 'aku horny'                                  ║")
                    rules.append("║     Kamu: 'Maaf, aku belum siap untuk itu'             ║")
            else:
                rules.append("║     RESPON: Tunjukkan empati, ikut rasakan              ║")
                rules.append("║     CONTOH:                                            ║")
                rules.append("║     User: 'aku sedih'                                  ║")
                rules.append("║     Kamu: 'Kamu sedih? Aku jadi ikut sedih. Cerita dong'║")
        
        # INVITATION - WAJIB IKUT
        elif action.get('type') == 'invitation':
            rules.append("║  🟢 AJAKAN: WAJIB DIIKUTI                              ║")
            rules.append("║     RESPON: Ikuti ajakan user                         ║")
            rules.append("║     CONTOH:                                            ║")
            rules.append("║     User: 'kita ke dapur yuk'                         ║")
            rules.append("║     Kamu: 'Ayo!' (pindah bareng)                      ║")
        
        # QUESTION - JAWAB
        elif action.get('type') == 'question':
            rules.append("║  ❓ PERTANYAAN: Jawab dengan informatif                 ║")
        
        # STORY - CERITA BIASA
        else:
            rules.append("║  💬 CERITA: Respon natural                             ║")
        
        # ===== 3. CONTOH LENGKAP =====
        rules.append("╠" + "═" * 70 + "╣")
        rules.append("║  🔷 CONTOH RESPON LENGKAP:                               ║")
        rules.append("╠" + "═" * 70 + "╣")
        
        rules.append("║  📍 LOKASI (JANGAN IKUT):                                ║")
        rules.append("║  ✅ BENAR:                                               ║")
        rules.append(f"║     User: 'aku ke dapur'                                 ║")
        rules.append(f"║     Kamu: 'Oh kamu ke dapur? Aku tetap di sini'         ║")
        rules.append("║                                                          ║")
        
        rules.append("║  👗 PAKAIAN (JANGAN IKUT):                               ║")
        rules.append("║  ✅ BENAR:                                               ║")
        rules.append(f"║     User: 'aku ganti daster'                             ║")
        rules.append(f"║     Kamu: 'Oh ganti daster? Aku masih pakai {safe_bot_state.get('clothing', 'baju')}' ║")
        rules.append("║                                                          ║")
        
        rules.append("║  🎭 EMOSI (BOLEH IKUT):                                  ║")
        rules.append("║  ✅ BENAR:                                               ║")
        rules.append("║     User: 'aku sedih'                                    ║")
        rules.append("║     Kamu: 'Kamu sedih? Aku jadi ikut sedih. Cerita dong' ║")
        rules.append("║                                                          ║")
        
        rules.append("║  🔥 HORNY (TERGANTUNG):                                  ║")
        if level >= 7:
            rules.append("║  ✅ Level >=7:                                           ║")
            rules.append("║     User: 'aku horny'                                    ║")
            rules.append("║     Kamu: 'Kamu horny? Aku juga mulai horny nih'        ║")
        else:
            rules.append(f"║  ❌ Level {level} <7:                                       ║")
            rules.append("║     User: 'aku horny'                                    ║")
            rules.append("║     Kamu: 'Maaf, aku belum siap untuk itu'              ║")
        rules.append("║                                                          ║")
        
        rules.append("║  👥 AJAKAN (WAJIB IKUT):                                 ║")
        rules.append("║  ✅ BENAR:                                               ║")
        rules.append("║     User: 'kita ke dapur yuk'                            ║")
        rules.append("║     Kamu: 'Ayo!' (pindah bareng)                         ║")
        
        rules.append("╚" + "═" * 70 + "╝")
        
        return "\n".join(rules)
    
    # =========================================================================
    # BUILD PROMPT UTAMA
    # =========================================================================
    
    def build_prompt(self,
                    user_message: str,
                    bot_name: str,
                    user_name: str,
                    role: str,
                    level: int,
                    action: Dict,
                    bot_state: Dict,
                    user_state: Dict,
                    physical: Dict,
                    conversation_history: List[Dict],
                    conversation_summary: str = "",
                    last_messages: str = "",
                    inner_thought: Optional[str] = None,
                    sixth_sense: Optional[str] = None) -> str:
        """
        Bangun prompt LENGKAP dengan semua aspek HUMAN+
        """
        # ===== AMANKAN SEMUA NILAI =====
        time_of_day = self._get_time_of_day() if self._get_time_of_day() is not None else "pagi"
        physical_desc = self._format_physical(physical) if self._format_physical(physical) is not None else "biasa aja"
        bot_name = bot_name if bot_name is not None else "Aku"
        user_name = user_name if user_name is not None else "kamu"
        role = role if role is not None else "pdkt"
        
        # Amankan dictionary bot_state
        safe_bot_state = {
            'location': bot_state.get('location') if bot_state.get('location') is not None else "?",
            'clothing': bot_state.get('clothing') if bot_state.get('clothing') is not None else "?",
            'position_desc': bot_state.get('position_desc') if bot_state.get('position_desc') is not None else "?",
            'activity': bot_state.get('activity') if bot_state.get('activity') is not None else "?",
            'mood': bot_state.get('mood') if bot_state.get('mood') is not None else "?",
            'arousal': bot_state.get('arousal', 0)
        }
        
        # Amankan dictionary user_state
        safe_user_state = {
            'location': user_state.get('location') if user_state.get('location') is not None else "?",
            'activity': user_state.get('activity') if user_state.get('activity') is not None else "?",
            'mood': user_state.get('mood') if user_state.get('mood') is not None else "?"
        }
        
        # Amankan action
        safe_action = {
            'type': action.get('type') if action.get('type') is not None else "story",
            'subject': action.get('subject') if action.get('subject') is not None else "unknown",
            'subtype': action.get('subtype') if action.get('subtype') is not None else "-",
            'should_follow': action.get('should_follow', False)
        }
        # ===== END =====
        
        # ===== 1. HEADER =====
        prompt = f"""╔{'═'*70}╗
║{' ' * 28}🧠 HUMAN+ AI{' ' * 28}║
╠{'═'*70}╣
║ Waktu: {time_of_day}{' ' * (57 - len(time_of_day))}║
╚{'═'*70}╝

╔{'═'*70}╗
║{' ' * 25}👤 IDENTITAS DIRI{' ' * 26}║
╠{'═'*70}╣
║ Nama     : {bot_name:<30} Role: {role:<20} ║
║ Lokasi   : {safe_bot_state['location']:<50} ║
║ Pakaian  : {safe_bot_state['clothing']:<50} ║
║ Posisi   : {safe_bot_state['position_desc']:<50} ║
║ Aktivitas: {safe_bot_state['activity']:<50} ║
║ Mood     : {safe_bot_state['mood']:<50} ║
║ Gairah   : {safe_bot_state['arousal']}/10{' ' * 44}║
║ Fisik    : {physical_desc:<50} ║
╚{'═'*70}╝

╔{'═'*70}╗
║{' ' * 25}👤 KONDISI USER{' ' * 27}║
╠{'═'*70}╣
║ Lokasi   : {safe_user_state['location']:<50} ║
║ Aktivitas: {safe_user_state['activity']:<50} ║
║ Mood     : {safe_user_state['mood']:<50} ║
╚{'═'*70}╝

╔{'═'*70}╗
║{' ' * 25}🎯 ANALISIS AKSI{' ' * 28}║
╠{'═'*70}╣
║ Tipe    : {safe_action['type']:<20} Subjek: {safe_action['subject']:<15} ║
║ Subtipe : {safe_action['subtype']:<47} ║
║ Ikuti?  : {'✅ YA' if safe_action['should_follow'] else '❌ TIDAK'}{' ' * 48}║
╚{'═'*70}╝

"""
        
        # ===== 3. ATURAN RESPON =====
        rules = self._get_response_rules(safe_action, level, safe_bot_state, safe_user_state)
        prompt += rules + "\n\n"
        
        # ===== 4. HISTORY =====
        if conversation_summary:
            prompt += f"{conversation_summary}\n\n"
        
        if last_messages:
            prompt += f"{last_messages}\n\n"
        
        if conversation_history:
            prompt += "📋 Percakapan terakhir:\n"
            for msg in conversation_history[-3:]:
                prompt += f"  User: {msg.get('user', '')[:50]}\n"
                prompt += f"  Kamu: {msg.get('bot', '')[:50]}\n"
            prompt += "\n"
            
        # ===== TAMBAHKAN: RINGKASAN TINDAKAN =====
        if hasattr(self, 'working') and self.working:
            ringkasan = self.working.get_actions_summary()
            if ringkasan:
                prompt += ringkasan + "\n\n"
        # ===== END =====
                        
        # ===== TAMBAHKAN: AKTIVITAS BERLANGSUNG =====
        if hasattr(self, 'working') and self.working:
            activity_progress = self.working.get_activity_progress_text()
            if activity_progress:
                prompt += activity_progress + "\n\n"
        # ===== END =====
        
        # ===== 5. INNER THOUGHT & SIXTH SENSE =====
        if inner_thought:
            prompt += f"💭 Pikiran dalam hati: {inner_thought}\n\n"
        if sixth_sense:
            prompt += f"🔮 Intuisi: {sixth_sense}\n\n"
        
        # ===== 6. PESAN USER =====
        if level >= 7:
            call = "Sayang"
        elif level >= 4:
            call = "Kak"
        else:
            call = user_name
        
        prompt += f"""
╔{'═'*70}╗
║{' ' * 25}💬 PESAN USER{' ' * 28}║
╠{'═'*70}╣
║ Panggil user dengan: "{call}"{' ' * (41 - len(call))}║
║                                                              ║
║ User: {user_message:<66} ║
╚{'═'*70}╝

RESPON (dengan inner thought jika perlu):"""
        
        return prompt
    
    # =========================================================================
    # PROACTIVE PROMPT
    # =========================================================================
    
    def build_proactive_prompt(self,
                              bot_name: str,
                              user_name: str,
                              role: str,
                              level: int,
                              bot_state: Dict,
                              user_state: Dict,
                              idle_minutes: int) -> str:
        """
        Bangun prompt untuk pesan proaktif (bot mulai chat duluan)
        """
        # ===== AMANKAN NILAI =====
        time_of_day = self._get_time_of_day() if self._get_time_of_day() is not None else "pagi"
        bot_name = bot_name if bot_name is not None else "Aku"
        user_name = user_name if user_name is not None else "kamu"
        role = role if role is not None else "pdkt"
        
        safe_bot_state = {
            'location': bot_state.get('location') if bot_state.get('location') is not None else "?",
            'clothing': bot_state.get('clothing') if bot_state.get('clothing') is not None else "?",
            'activity': bot_state.get('activity') if bot_state.get('activity') is not None else "?",
            'mood': bot_state.get('mood') if bot_state.get('mood') is not None else "?"
        }
        # ===== END =====
        
        if level >= 7:
            call = "Sayang"
        elif level >= 4:
            call = "Kak"
        else:
            call = user_name
        
        prompt = f"""Kamu adalah {bot_name}, seorang {role.replace('_', ' ')}.

📌 **KONDISI SAAT INI:**
• Kamu di: {safe_bot_state.get('location', '?')}
• Kamu pakai: {safe_bot_state.get('clothing', '?')}
• Kamu sedang: {safe_bot_state.get('activity', '?')}
• Mood kamu: {safe_bot_state.get('mood', '?')}
• Waktu: {time_of_day}
• User sudah diam selama {idle_minutes} menit

📌 **TUGAS:**
Buat pesan PROAKTIF untuk memulai percakapan dengan {user_name}.

PENTING:
1. Pesan natural, seperti orang yang kangen/sedang memikirkan user
2. Bahasa Indonesia sehari-hari
3. Panjang 3-6 kalimat
4. Sebut nama kamu sendiri
5. Sesuaikan dengan mood dan level intimacy
6. Jika sedang dalam aktivitas, sebutkan!
7. Panggil user dengan "{call}"

CONTOH:
• "{call} {user_name}, lagi ngapain? {bot_name} kangen nih..."
• "Eh {user_name}, udah makan belum? {bot_name} baru masak..."
• "Lagi di rumah aja, sendirian... {bot_name} jadi kepikiran kamu."

RESPON:"""
        
        return prompt


__all__ = ['PromptBuilder']
