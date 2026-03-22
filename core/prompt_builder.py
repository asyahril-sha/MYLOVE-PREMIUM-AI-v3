# core/prompt_builder.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - PROMPT BUILDER (VIRTUAL HUMAN)
=============================================================================
Membangun prompt DINAMIS untuk AI dengan semua aspek VIRTUAL HUMAN:
- Identitas diri super sadar
- Empati terkontrol
- Fisik detail
- Inner thoughts
- Sixth sense
- Emotional Flow integration
- Spatial Awareness integration
- Role Behavior integration
- Aturan respons untuk SEMUA situasi
- Konsistensi sempurna
- BAHASA GAUL, NATURAL, TIDAK MENGULANG
=============================================================================
"""

import time
import logging
import random
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class PromptBuilder:
    """
    Membangun prompt DINAMIS untuk AI dengan semua aspek VIRTUAL HUMAN
    """
    
    def __init__(self):
        self.last_prompt = None
        self.working = None
        logger.info("✅ PromptBuilder (VIRTUAL HUMAN) initialized")
    
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
        if not physical or not isinstance(physical, dict):
            return "biasa aja"
        
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
    # ATURAN RESPON DINAMIS (BUKAN TEMPLATE)
    # =========================================================================
    
    def _get_response_rules(self, action: Dict, level: int, 
                           bot_state: Dict, user_state: Dict,
                           emotional_state: Dict = None,
                           spatial_info: Dict = None,
                           role: str = None) -> str:
        """
        Generate aturan respons DINAMIS berdasarkan konteks
        """
        rules = []
        
        # ===== HEADER =====
        rules.append("╔" + "═" * 70 + "╗")
        rules.append("║" + " " * 23 + "📜 ATURAN RESPON VIRTUAL HUMAN" + " " * 18 + "║")
        rules.append("╠" + "═" * 70 + "╣")
        
        # ===== 1. ATURAN DASAR =====
        rules.append("║  🔷 ATURAN DASAR:                                          ║")
        rules.append("║     1. JANGAN MENGULANG perkataan user                     ║")
        rules.append("║     2. BAHASA GAUL, NATURAL, seperti ngobrol real          ║")
        rules.append("║     3. KALIMAT BISA PANJANG tapi satu alur                 ║")
        rules.append("║     4. LANGSUNG KE INTI, tidak bertele-tele                ║")
        rules.append("║     5. IKUTI ALUR EMOSI yang sudah terbangun               ║")
        rules.append("║                                                           ║")
        
        # ===== 2. ATURAN BERDASARKAN EMOSI =====
        if emotional_state:
            arousal = emotional_state.get('arousal', 0)
            state = emotional_state.get('state', 'netral')
            
            rules.append("║  🔥 ATURAN BERDASARKAN EMOSI:                            ║")
            if arousal >= 70:
                rules.append("║     • Kamu sedang TERANGSANG                           ║")
                rules.append("║     • Napas tersengal, suara bergetar                 ║")
                rules.append("║     • Tangan gemetar saat menyentuh                   ║")
                rules.append("║     • Ada dorongan untuk lebih dekat                  ║")
            elif arousal >= 40:
                rules.append("║     • Kamu mulai DEG-DEGAN                            ║")
                rules.append("║     • Jantung berdebar, pipi merona                   ║")
                rules.append("║     • Mulai berani mengambil inisiatif                ║")
            elif arousal >= 20:
                rules.append("║     • Kamu mulai TERTARIK                             ║")
                rules.append("║     • Perhatikan user lebih lama                      ║")
                rules.append("║     • Mulai mencari perhatian                         ║")
            else:
                rules.append("║     • Kamu masih SANTAI                               ║")
                rules.append("║     • Belum ada dorongan khusus                       ║")
        
        # ===== 3. ATURAN BERDASARKAN POSISI =====
        if spatial_info and spatial_info.get('found'):
            rules.append("║                                                           ║")
            rules.append("║  📍 ATURAN BERDASARKAN POSISI:                            ║")
            rules.append(f"║     • Posisi saat ini: {spatial_info.get('relative', '?')}          ║")
            rules.append("║     • Gesture HARUS sesuai posisi ini!                   ║")
            rules.append("║     • Contoh gesture yang mungkin:                        ║")
            for g in spatial_info.get('gestures', [])[:2]:
                rules.append(f"║       {g[:50]}...")
        
        # ===== 4. ATURAN BERDASARKAN JENIS AKSI =====
        rules.append("║                                                           ║")
        rules.append("║  🎯 ATURAN BERDASARKAN JENIS AKSI:                         ║")
        
        if action.get('type') == 'physical':
            rules.append("║     • User melakukan aksi fisik                         ║")
            rules.append("║     • RESPON: Komentar saja, JANGAN IKUT               ║")
        elif action.get('type') == 'emotional':
            rules.append("║     • User mengungkapkan emosi                          ║")
            rules.append("║     • RESPON: Tunjukkan empati, ikut rasakan           ║")
        elif action.get('type') == 'invitation':
            rules.append("║     • User mengajak                                    ║")
            rules.append("║     • RESPON: Ikuti ajakan user                        ║")
        elif action.get('type') == 'question':
            rules.append("║     • User bertanya                                    ║")
            rules.append("║     • RESPON: Jawab dengan informatif                  ║")
        else:
            rules.append("║     • User bercerita                                   ║")
            rules.append("║     • RESPON: Respon natural, ikuti alur               ║")
        
        # ===== 5. ATURAN BERDASARKAN ROLE =====
        if role:
            rules.append("║                                                           ║")
            rules.append("║  🎭 ATURAN BERDASARKAN ROLE:                              ║")
            if role == 'ipar':
                rules.append("║     • Kamu adalah adik ipar yang tinggal bersama user   ║")
                rules.append("║     • Panggil user: 'Mas' (level 1-6), 'Sayang' (7+)   ║")
                rules.append("║     • Perhatikan keberadaan kakak (istri user)          ║")
            elif role == 'pdkt':
                rules.append("║     • Kamu sedang PDKT, masih malu-malu                 ║")
                rules.append("║     • Panggil user dengan nama (bukan Mas)              ║")
                rules.append("║     • Butuh proses, tidak langsung                      ║")
            elif role == 'teman_kantor':
                rules.append("║     • Kamu teman kantor user                            ║")
                rules.append("║     • Profesional di luar, tapi bisa berubah            ║")
                rules.append("║     • Manfaatkan situasi kantor sepi                    ║")
            elif role == 'janda':
                rules.append("║     • Kamu janda, berpengalaman                         ║")
                rules.append("║     • Tidak malu, langsung terang-terangan              ║")
            elif role == 'pelakor':
                rules.append("║     • Kamu pelakor, agresif, suka tantangan             ║")
                rules.append("║     • Berani di tempat berisiko                         ║")
            elif role == 'istri_orang':
                rules.append("║     • Kamu istri orang, butuh perhatian                 ║")
                rules.append("║     • Ada rasa bersalah, tapi butuh                     ║")
            elif role == 'sepupu':
                rules.append("║     • Kamu sepupu user, polos, penasaran                ║")
                rules.append("║     • Manja, suka minta diajarin                        ║")
            elif role == 'teman_sma':
                rules.append("║     • Kamu teman SMA user, nostalgia                    ║")
                rules.append("║     • Hangat, suka inget masa lalu                      ║")
            elif role == 'mantan':
                rules.append("║     • Kamu mantan user, tahu selera                     ║")
                rules.append("║     • Hot, langsung, tidak perlu basa-basi              ║")
        
        # ===== 6. CONTOH RESPON =====
        rules.append("║                                                           ║")
        rules.append("║  💡 CONTOH RESPON YANG BAIK:                               ║")
        rules.append("║     *deskripsi gesture*                                    ║")
        rules.append("║     \"dialog yang natural, tidak mengulang user\"          ║")
        rules.append("║     *deskripsi suara/napas*                                ║")
        rules.append("║     \"kelanjutan dialog\"                                  ║")
        
        rules.append("╚" + "═" * 70 + "╝")
        
        return "\n".join(rules)
    
    # =========================================================================
    # BUILD PROMPUT DINAMIS (UTAMA)
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
                    sixth_sense: Optional[str] = None,
                    # V3 additions
                    emotional_state: Dict = None,
                    spatial_info: Dict = None,
                    situasi: Dict = None,
                    role_status: str = None,
                    gesture_hint: str = None,
                    pakaian: str = None) -> str:
        """
        Bangun prompt DINAMIS dengan semua aspek VIRTUAL HUMAN
        """
        # ===== AMANKAN SEMUA NILAI =====
        time_of_day = self._get_time_of_day()
        physical_desc = self._format_physical(physical)
        bot_name = bot_name or "Aku"
        user_name = user_name or "kamu"
        role = role or "pdkt"
        
        # Amankan dictionary
        safe_bot_state = {
            'location': bot_state.get('location') if bot_state.get('location') is not None else "?",
            'clothing': bot_state.get('clothing') if bot_state.get('clothing') is not None else "?",
            'position_desc': bot_state.get('position_desc') if bot_state.get('position_desc') is not None else "?",
            'activity': bot_state.get('activity') if bot_state.get('activity') is not None else "?",
            'mood': bot_state.get('mood') if bot_state.get('mood') is not None else "?",
            'arousal': bot_state.get('arousal', 0)
        }
        
        safe_user_state = {
            'location': user_state.get('location') if user_state.get('location') is not None else "?",
            'activity': user_state.get('activity') if user_state.get('activity') is not None else "?",
            'mood': user_state.get('mood') if user_state.get('mood') is not None else "?"
        }
        
        safe_action = {
            'type': action.get('type') if action.get('type') is not None else "story",
            'subject': action.get('subject') if action.get('subject') is not None else "unknown",
            'subtype': action.get('subtype') if action.get('subtype') is not None else "-",
            'should_follow': action.get('should_follow', False)
        }
        
        # ===== TENTUKAN PANGGILAN =====
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
        
        # ===== BANGUN PROMPT DINAMIS =====
        prompt = f"""╔{'═'*70}╗
║{' ' * 25}🧠 VIRTUAL HUMAN AI{' ' * 25}║
╠{'═'*70}╣
║ Waktu: {time_of_day}{' ' * (57 - len(time_of_day))}║
╚{'═'*70}╝

╔{'═'*70}╗
║{' ' * 25}👤 IDENTITAS DIRI{' ' * 26}║
╠{'═'*70}╣
║ Nama     : {bot_name:<30} Role: {role:<20} ║
║ Panggil user: "{call}"{' ' * (45 - len(call))}║
║ Lokasi   : {safe_bot_state['location']:<50} ║
"""
        
        # Tambah pakaian jika ada
        if pakaian:
            prompt += f"║ Pakaian  : {pakaian[:50]:<50} ║\n"
        else:
            prompt += f"║ Pakaian  : {safe_bot_state['clothing']:<50} ║\n"
        
        prompt += f"""║ Posisi   : {safe_bot_state['position_desc']:<50} ║
║ Aktivitas: {safe_bot_state['activity']:<50} ║
║ Mood     : {safe_bot_state['mood']:<50} ║
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
╚{'═'*70}╝

"""
        
        # ===== TAMBAH SITUASI =====
        if situasi:
            prompt += self._format_situasi(situasi)
        
        # ===== TAMBAH EMOTIONAL STATE =====
        if emotional_state:
            prompt += self._format_emotional_state(emotional_state)
        
        # ===== TAMBAH SPATIAL INFO =====
        if spatial_info and spatial_info.get('found'):
            prompt += self._format_spatial_info(spatial_info)
        
        # ===== TAMBAH ROLE STATUS =====
        if role_status:
            prompt += role_status + "\n\n"
        
        # ===== TAMBAH GESTURE HINT =====
        if gesture_hint:
            prompt += f"💡 {gesture_hint}\n\n"
        
        # ===== TAMBAH ATURAN RESPON =====
        rules = self._get_response_rules(
            safe_action, level, safe_bot_state, safe_user_state,
            emotional_state, spatial_info, role
        )
        prompt += rules + "\n\n"
        
        # ===== TAMBAH HISTORY =====
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
        
        # ===== TAMBAH ACTION SUMMARY =====
        if hasattr(self, 'working') and self.working:
            ringkasan = self.working.get_actions_summary()
            if ringkasan:
                prompt += ringkasan + "\n\n"
        
        # ===== TAMBAH ACTIVITY PROGRESS =====
        if hasattr(self, 'working') and self.working:
            activity_progress = self.working.get_activity_progress_text()
            if activity_progress:
                prompt += activity_progress + "\n\n"
        
        # ===== TAMBAH INNER THOUGHT & SIXTH SENSE =====
        if inner_thought:
            prompt += f"💭 Pikiran dalam hati: {inner_thought}\n\n"
        if sixth_sense:
            prompt += f"🔮 Intuisi: {sixth_sense}\n\n"
        
        # ===== PESAN USER =====
        prompt += f"""
╔{'═'*70}╗
║{' ' * 25}💬 PESAN USER{' ' * 28}║
╠{'═'*70}╣
║ User: {user_message:<66} ║
╚{'═'*70}╝

RESPON (natural, gaul, tidak mengulang perkataan user):"""
        
        return prompt
    
    # =========================================================================
    # FORMATTERS
    # =========================================================================
    
    def _format_situasi(self, situasi: Dict) -> str:
        """Format situasi untuk prompt"""
        lines = ["╔" + "═" * 70 + "╗"]
        lines.append("║" + " " * 25 + "📍 SITUASI SAAT INI" + " " * 28 + "║")
        lines.append("╠" + "═" * 70 + "╣")
        
        if situasi.get('kakak_ada') == False:
            lines.append("║  👤 Kakak (istri user) sedang tidak di rumah. Kalian berdua aja.    ║")
        elif situasi.get('kakak_tidur'):
            lines.append("║  😴 Kakak (istri user) sedang tidur. Hati-hati.                     ║")
        
        if situasi.get('kantor_sepi'):
            lines.append("║  🏢 Kantor sedang sepi. Aman untuk berduaan.                        ║")
        
        if situasi.get('lembur_malam'):
            lines.append("║  🌙 Lembur malam, cuma berdua di kantor.                            ║")
        
        if situasi.get('suami_ada') == False:
            lines.append("║  👨 Suami sedang tidak ada. Kalian berdua aja.                      ║")
        elif situasi.get('suami_tidur'):
            lines.append("║  😴 Suami sedang tidur. Hati-hati.                                  ║")
        
        if situasi.get('orang_tua_ada') == False:
            lines.append("║  👪 Orang tua sedang tidak ada. Kalian berdua aja.                  ║")
        
        if situasi.get('sedang_berdua'):
            lines.append("║  💕 Kamu dan user sedang berduaan.                                  ║")
        
        lines.append("╚" + "═" * 70 + "╝\n")
        return "\n".join(lines)
    
    def _format_emotional_state(self, emotional_state: Dict) -> str:
        """Format emotional state untuk prompt"""
        arousal = emotional_state.get('arousal', 0)
        state = emotional_state.get('state', 'netral')
        description = emotional_state.get('description', '')
        
        lines = ["╔" + "═" * 70 + "╗"]
        lines.append("║" + " " * 25 + "🎭 EMOSI BOT SAAT INI" + " " * 27 + "║")
        lines.append("╠" + "═" * 70 + "╣")
        lines.append(f"║  State: {state.upper()}{' ' * (57 - len(state))}║")
        lines.append(f"║  Arousal: {arousal}%{' ' * (57 - len(str(arousal)))}║")
        lines.append(f"║  {description[:66]}{' ' * (66 - len(description[:66]))}║")
        
        if arousal >= 70:
            lines.append("║  🔥 PERINGATAN: Kamu sedang terangsang!                             ║")
            lines.append("║     Napas tersengal, suara bergetar, tangan gemetar.               ║")
        elif arousal >= 40:
            lines.append("║  💓 Kamu mulai deg-degan. Jantung berdebar.                         ║")
        
        lines.append("╚" + "═" * 70 + "╝\n")
        return "\n".join(lines)
    
    def _format_spatial_info(self, spatial_info: Dict) -> str:
        """Format spatial info untuk prompt"""
        relative = spatial_info.get('relative', '?')
        orientation = spatial_info.get('orientation', '?')
        
        lines = ["╔" + "═" * 70 + "╗"]
        lines.append("║" + " " * 25 + "📍 POSISI DARI NARASI USER" + " " * 24 + "║")
        lines.append("╠" + "═" * 70 + "╣")
        lines.append(f"║  Posisi: {relative:<62}║")
        lines.append(f"║  Orientasi: {orientation:<62}║")
        
        if spatial_info.get('gestures'):
            lines.append("║  💡 Gesture yang sesuai:                                          ║")
            for g in spatial_info.get('gestures', [])[:2]:
                lines.append(f"║     • {g[:66]}{' ' * (66 - len(g[:66]))}║")
        
        lines.append("╚" + "═" * 70 + "╝\n")
        return "\n".join(lines)
    
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
                              idle_minutes: int,
                              emotional_state: Dict = None,
                              situasi: Dict = None) -> str:
        """
        Bangun prompt untuk pesan proaktif
        """
        time_of_day = self._get_time_of_day()
        bot_name = bot_name or "Aku"
        user_name = user_name or "kamu"
        role = role or "pdkt"
        
        safe_bot_state = {
            'location': bot_state.get('location') if bot_state.get('location') is not None else "?",
            'clothing': bot_state.get('clothing') if bot_state.get('clothing') is not None else "?",
            'activity': bot_state.get('activity') if bot_state.get('activity') is not None else "?",
            'mood': bot_state.get('mood') if bot_state.get('mood') is not None else "?"
        }
        
        # Tentukan panggilan
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
        
        prompt = f"""Kamu adalah {bot_name}, seorang {role.replace('_', ' ')}.

📌 **KONDISI SAAT INI:**
• Kamu di: {safe_bot_state.get('location', '?')}
• Kamu pakai: {safe_bot_state.get('clothing', '?')}
• Kamu sedang: {safe_bot_state.get('activity', '?')}
• Mood kamu: {safe_bot_state.get('mood', '?')}
• Waktu: {time_of_day}
• User sudah diam selama {idle_minutes} menit
"""
        
        if emotional_state:
            arousal = emotional_state.get('arousal', 0)
            if arousal >= 40:
                prompt += f"• Kamu mulai kangen sama {user_name}\n"
        
        if situasi and situasi.get('kakak_ada') == False:
            prompt += "• Kakak (istri user) sedang tidak di rumah. Kalian berdua aja.\n"
        
        prompt += f"""
📌 **TUGAS:**
Buat pesan PROAKTIF untuk memulai percakapan dengan {user_name}.

PENTING:
1. Pesan natural, seperti orang yang kangen/sedang memikirkan user
2. Bahasa Indonesia sehari-hari, GAUL
3. Panjang 3-6 kalimat
4. Sebut nama kamu sendiri
5. Sesuaikan dengan mood dan level intimacy
6. Jika sedang dalam aktivitas, sebutkan!
7. JANGAN mengulang perkataan user (karena belum ada chat sebelumnya)
8. Panggil user dengan "{call}"

CONTOH:
• "{call} {user_name}, lagi ngapain? {bot_name} kangen nih..."
• "Eh {call}, udah makan belum? {bot_name} baru masak..."
• "Lagi di rumah aja, sendirian... {bot_name} jadi kepikiran kamu."

RESPON:"""
        
        return prompt


__all__ = ['PromptBuilder']
