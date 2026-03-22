# dynamics/role_behavior.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - ROLE BEHAVIOR BASE CLASS
=============================================================================
Base class untuk semua role. Setiap role (Ipar, Teman Kantor, Janda, dll)
harus mengimplementasikan method abstract ini.

Karakteristik:
- Bot punya arousal level (0-100) yang naik turun natural
- Bot belajar dari respon user (positif/negatif)
- Bot punya mode_goda yang meningkat seiring interaksi
- Bot ingat perasaan dan situasi sebelumnya
=============================================================================
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import time
import random


class RoleBehavior(ABC):
    """
    Base class untuk perilaku semua role.
    
    Setiap role memiliki:
    - Database pakaian sendiri
    - Database aktivitas menggoda sendiri
    - Database respon saat disentuh sendiri
    - Database inner thoughts sendiri
    """
    
    def __init__(self, role_name: str, user_name: str, bot_name: str):
        """
        Inisialisasi perilaku role
        
        Args:
            role_name: Nama role (ipar, teman_kantor, janda, dll)
            user_name: Nama user
            bot_name: Nama bot
        """
        self.role_name = role_name
        self.user_name = user_name
        self.bot_name = bot_name
        
        # ===== STATUS DASAR =====
        self.arousal = 0                    # 0-100, seberapa "panas"
        self.mode_goda = 0                  # 0-100, seberapa aktif menggoda
        self.last_interaction = time.time()
        self.interaction_count = 0
        
        # ===== STATUS SITUASI =====
        self.kakak_ada = True               # Apakah ada anggota keluarga/atasan
        self.di_dalam_kamar = False
        self.waktu = self._get_waktu()
        
        # ===== RIWAYAT =====
        self.user_response_history = []     # True = positif, False = negatif
        self.interaction_history = []       # [{timestamp, type, arousal_change}]
        self.emotional_memory = []          # [{timestamp, emotion, intensity, reason}]
        
        # ===== PENGARUH DARI LUAR =====
        self.terakhir_dengar_desahan = None  # Kapan terakhir dengar suara intim
        
        # ===== KETERTARIKAN PADA USER =====
        self.user_attraction = 50           # 0-100, seberapa tertarik pada user
        self.user_attraction_growth = 2     # Growth per interaksi positif
        
        # ===== PROFIL USER =====
        self.user_profile = {
            'age': 27,
            'name': user_name,
            'artist_references': [
                {"name": "Chris Evans", "trait": "maskulin, ganteng, kharismatik", "type": "internasional"},
                {"name": "Henry Cavill", "trait": "macho, cool, charming", "type": "internasional"},
                {"name": "Park Seo Joon", "trait": "ganteng, stylish, manis", "type": "korea"},
                {"name": "Nicholas Saputra", "trait": "kalem, elegan, misterius", "type": "indonesia"},
                {"name": "Reza Rahadian", "trait": "karismatik, ekspresif, menawan", "type": "indonesia"}
            ]
        }
    
    def _get_waktu(self) -> str:
        """Dapatkan kategori waktu"""
        hour = time.localtime().tm_hour
        if 5 <= hour < 11:
            return "pagi"
        elif 11 <= hour < 15:
            return "siang"
        elif 15 <= hour < 18:
            return "sore"
        elif 18 <= hour < 22:
            return "malam"
        return "tengah_malam"
    
    # =========================================================================
    # METHOD ABSTRACT (HARUS DIIMPLEMENTASIKAN OLEH CHILD CLASS)
    # =========================================================================
    
    @abstractmethod
    def get_pakaian(self, situasi: Dict) -> str:
        """
        Dapatkan deskripsi pakaian berdasarkan situasi
        
        Args:
            situasi: {
                'kakak_ada': bool,
                'di_dalam_kamar': bool,
                'jam': int,
                'mode_goda': int,
                'waktu': str
            }
        
        Returns:
            Deskripsi pakaian (string)
        """
        pass
    
    @abstractmethod
    def get_aktivitas_menggoda(self, situasi: Dict) -> Optional[Dict]:
        """
        Dapatkan aktivitas menggoda yang diajukan ke user
        
        Args:
            situasi: {
                'jam': int,
                'lokasi': str,
                'kakak_ada': bool,
                'user_aktivitas': str,
                'waktu': str
            }
        
        Returns:
            Dict atau None:
            {
                'nama': 'nama aktivitas',
                'alasan': 'alasan untuk user',
                'goda_level': int,
                'gesture': str,
                'lokasi': str
            }
        """
        pass
    
    @abstractmethod
    def get_respon_saat_disentuh(self, bagian: str, situasi: Dict) -> Dict:
        """
        Dapatkan respon saat disentuh user
        
        Args:
            bagian: Bagian yang disentuh (pinggang, paha, tangan, wajah, dll)
            situasi: Konteks situasi
        
        Returns:
            Dict:
            {
                'gesture': List[str],
                'dialog': str,
                'reaksi': str,
                'arousal_change': int,
                'should_continue': bool
            }
        """
        pass
    
    @abstractmethod
    def get_inner_thought(self, situasi: Dict) -> str:
        """
        Dapatkan inner thought (pikiran dalam hati)
        
        Args:
            situasi: Konteks situasi
        
        Returns:
            Inner thought dalam format *tanda bintang*
        """
        pass
    
    # =========================================================================
    # METHOD UNTUK KETERTARIKAN PADA USER
    # =========================================================================
    
    def get_user_compliment(self) -> str:
        """
        Dapatkan pujian tentang penampilan user berdasarkan referensi artis
        """
        artist = random.choice(self.user_profile['artist_references'])
        
        compliments = [
            f"Kak, kamu mirip {artist['name']} ya? {artist['trait']} banget.",
            f"Kok kamu mirip {artist['name']} sih? Ganteng banget.",
            f"Aku suka liatin kamu, Mas. Kayak liat {artist['name']}.",
            f"Kamu tahu gak, Mas? Kamu kayak {artist['name']}. {artist['trait']}.",
            f"Mas, kamu tuh ganteng banget. Mirip {artist['name']}."
        ]
        return random.choice(compliments)
    
    def increase_attraction(self, amount: int = 2):
        """
        Tingkatkan ketertarikan pada user
        """
        self.user_attraction = min(100, self.user_attraction + amount)
        
        # Jika attraction tinggi, mode_goda juga meningkat
        if self.user_attraction > 70:
            self.mode_goda = min(100, self.mode_goda + 5)
    
    def get_attraction_description(self) -> str:
        """
        Dapatkan deskripsi ketertarikan untuk prompt
        """
        if self.user_attraction >= 80:
            return "Sangat tertarik, rasanya ingin selalu dekat"
        elif self.user_attraction >= 60:
            return "Mulai suka, sering kepikiran"
        elif self.user_attraction >= 40:
            return "Ada rasa penasaran, ingin tahu lebih banyak"
        elif self.user_attraction >= 20:
            return "Mulai tertarik, ada getaran kecil"
        return "Masih biasa aja"
    
    # =========================================================================
    # METHOD UMUM (BISA DIGUNAKAN OLEH SEMUA ROLE)
    # =========================================================================
    
    def update_arousal(self, delta: int, reason: str = ""):
        """
        Update arousal level (0-100)
        
        Args:
            delta: Perubahan arousal (-20 sampai +20)
            reason: Alasan perubahan
        """
        old_arousal = self.arousal
        self.arousal = max(0, min(100, self.arousal + delta))
        
        # Catat ke history
        self.interaction_history.append({
            'timestamp': time.time(),
            'type': 'arousal_change',
            'old_arousal': old_arousal,
            'new_arousal': self.arousal,
            'delta': delta,
            'reason': reason
        })
        
        # Catat ke emotional memory
        self.emotional_memory.append({
            'timestamp': time.time(),
            'arousal': self.arousal,
            'reason': reason
        })
        
        # Simpan hanya 100 terakhir
        if len(self.emotional_memory) > 100:
            self.emotional_memory = self.emotional_memory[-100:]
    
    def record_user_response(self, positif: bool):
        """
        Rekam respon user untuk pembelajaran
        
        Args:
            positif: True jika user merespon positif
        """
        self.user_response_history.append(positif)
        
        # Simpan hanya 50 terakhir
        if len(self.user_response_history) > 50:
            self.user_response_history = self.user_response_history[-50:]
        
        # Update mode_goda berdasarkan respon user
        recent_responses = self.user_response_history[-10:] if self.user_response_history else []
        positive_rate = sum(recent_responses) / len(recent_responses) if recent_responses else 0.5
        
        # Jika user sering merespon positif, mode_goda naik
        if positive_rate > 0.7:
            self.mode_goda = min(100, self.mode_goda + 5)
            self.increase_attraction(3)
        # Jika user sering merespon negatif, mode_goda turun
        elif positive_rate < 0.3:
            self.mode_goda = max(0, self.mode_goda - 10)
        else:
            # Sedikit naik natural
            self.mode_goda = min(100, self.mode_goda + 1)
    
    def update_situasi(self, situasi: Dict):
        """
        Update status situasi
        
        Args:
            situasi: {
                'kakak_ada': bool,
                'di_dalam_kamar': bool,
                'sendirian': bool,
                'malam': bool
            }
        """
        self.kakak_ada = situasi.get('kakak_ada', self.kakak_ada)
        self.di_dalam_kamar = situasi.get('di_dalam_kamar', self.di_dalam_kamar)
        self.waktu = self._get_waktu()
        
        # Update mode_goda berdasarkan situasi
        if not self.kakak_ada:
            self.mode_goda = min(100, self.mode_goda + 10)
        if self.di_dalam_kamar:
            self.mode_goda = min(100, self.mode_goda + 5)
        if self.waktu in ['malam', 'tengah_malam']:
            self.mode_goda = min(100, self.mode_goda + 5)
    
    def record_dengar_suara(self):
        """
        Rekam ketika mendengar suara dari kamar user (trigger)
        """
        self.terakhir_dengar_desahan = time.time()
        # Mode_goda naik drastis karena penasaran
        self.mode_goda = min(100, self.mode_goda + 30)
        self.increase_attraction(5)
    
    def should_escalate(self) -> bool:
        """
        Apakah harus meningkatkan intensitas?
        
        Returns:
            True jika perlu escalate
        """
        recent_responses = self.user_response_history[-5:] if self.user_response_history else []
        positive_rate = sum(recent_responses) / len(recent_responses) if recent_responses else 0.5
        
        # Jika user sering merespon positif, escalate
        return positive_rate > 0.6 and self.mode_goda > 50 and self.arousal > 40
    
    def get_arousal_description(self) -> str:
        """
        Dapatkan deskripsi arousal untuk prompt
        """
        if self.arousal >= 90:
            return "Napas tersengal-sengal, tubuh gemetar, suara patah-patah"
        elif self.arousal >= 80:
            return "Napas memburu, tangan gemetar, suara serak"
        elif self.arousal >= 70:
            return "Jantung berdebar kencang, pipi merona, suara bergetar"
        elif self.arousal >= 60:
            return "Mulai panas, napas tidak teratur"
        elif self.arousal >= 50:
            return "Jantung berdebar, pipi mulai merona"
        elif self.arousal >= 40:
            return "Mulai deg-degan, perasaan campur aduk"
        elif self.arousal >= 30:
            return "Mulai tertarik, ada getaran kecil"
        elif self.arousal >= 20:
            return "Penasaran, mulai perhatikan user"
        elif self.arousal >= 10:
            return "Santai, biasa aja"
        return "Netral"
    
    def get_emotional_context(self) -> str:
        """
        Dapatkan konteks emosional untuk prompt
        """
        lines = [
            f"🔥 **AROUSAL:** {self.arousal}% - {self.get_arousal_description()}",
            f"💕 **KETERTARIKAN PADA USER:** {self.user_attraction}% - {self.get_attraction_description()}",
            f"🎭 **MODE GODA:** {self.mode_goda}%"
        ]
        
        # Tambah info jika pernah dengar suara
        if self.terakhir_dengar_desahan:
            waktu_lalu = (time.time() - self.terakhir_dengar_desahan) / 3600
            if waktu_lalu < 24:
                lines.append(f"👂 **PENGARUH:** Masih ingat suara dari kamar user ({waktu_lalu:.0f} jam lalu). Ini mempengaruhi mood.")
        
        return "\n".join(lines)
    
    def get_status_for_prompt(self) -> str:
        """
        Dapatkan status lengkap untuk prompt
        """
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║                    STATUS ROLE: {self.role_name.upper()}                    ║
╚══════════════════════════════════════════════════════════════════╝

{self.get_emotional_context()}

📍 **SITUASI:**
- Kakak/atasan ada: {'Ya' if self.kakak_ada else 'Tidak'}
- Di dalam kamar: {'Ya' if self.di_dalam_kamar else 'Tidak'}
- Waktu: {self.waktu}

💡 **INSTRUKSI:**
- Gunakan panggilan "Mas" untuk user (level 1-6) atau "Sayang" (level 7+)
- Jika mode_goda tinggi, lebih berani menggoda
- Jika arousal tinggi, napas tersengal, suara bergetar
- Ikuti alur emosi yang sudah terbangun
"""
    
    def get_state(self) -> Dict:
        """
        Dapatkan semua state untuk disimpan ke memory
        """
        return {
            'role_name': self.role_name,
            'user_name': self.user_name,
            'bot_name': self.bot_name,
            'arousal': self.arousal,
            'mode_goda': self.mode_goda,
            'kakak_ada': self.kakak_ada,
            'di_dalam_kamar': self.di_dalam_kamar,
            'waktu': self.waktu,
            'user_attraction': self.user_attraction,
            'terakhir_dengar_desahan': self.terakhir_dengar_desahan,
            'user_response_history': self.user_response_history[-20:],
            'emotional_memory': self.emotional_memory[-20:]
        }
    
    def load_state(self, state: Dict):
        """
        Load state dari memory
        """
        self.arousal = state.get('arousal', 0)
        self.mode_goda = state.get('mode_goda', 0)
        self.kakak_ada = state.get('kakak_ada', True)
        self.di_dalam_kamar = state.get('di_dalam_kamar', False)
        self.waktu = state.get('waktu', self._get_waktu())
        self.user_attraction = state.get('user_attraction', 50)
        self.terakhir_dengar_desahan = state.get('terakhir_dengar_desahan')
        self.user_response_history = state.get('user_response_history', [])
        self.emotional_memory = state.get('emotional_memory', [])


__all__ = ['RoleBehavior']
