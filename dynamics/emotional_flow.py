# dynamics/emotional_flow.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - EMOTIONAL FLOW SYSTEM
=============================================================================
Sistem emosi yang mengalir gradual seperti manusia.

Karakteristik:
- Arousal level 0-100 yang naik turun natural
- Emosi tidak loncat (netral -> horny butuh proses)
- Ada empathy factor (ikut merasakan user)
- State emosi yang jelas dengan deskripsi
- Terintegrasi dengan role behavior
=============================================================================
"""

import time
import random
from typing import Dict, List, Optional, Tuple
from enum import Enum


class EmotionalState(Enum):
    """Status emosi bot yang mengalir gradual"""
    NETRAL = "netral"
    PENASARAN = "penasaran"
    TERTARIK = "tertarik"
    DEG_DEGAN = "deg-degan"
    GUGUP = "gugup"
    BERANI = "berani"
    HORNY = "horny"
    CLIMAX = "climax"
    LEMAS = "lemas"


class EmotionalFlow:
    """
    Sistem emosi yang mengalir seperti manusia.
    Tidak bisa loncat dari NETRAL langsung ke HORNY.
    Ada proses gradual.
    """
    
    def __init__(self, role_name: str, role_behavior=None):
        """
        Args:
            role_name: Nama role (ipar, teman_kantor, dll)
            role_behavior: Referensi ke role behavior untuk sinkronisasi
        """
        self.role_name = role_name
        self.role_behavior = role_behavior
        
        # State saat ini
        self.current_state = EmotionalState.NETRAL
        self.arousal = 0                    # 0-100
        self.state_duration = 0             # Berapa lama di state ini (menit)
        
        # History untuk konsistensi
        self.state_history = []              # [{timestamp, state, arousal, reason}]
        
        # Transisi yang diperbolehkan (tidak bisa loncat)
        self.allowed_transitions = {
            EmotionalState.NETRAL: [EmotionalState.PENASARAN],
            EmotionalState.PENASARAN: [EmotionalState.TERTARIK, EmotionalState.NETRAL],
            EmotionalState.TERTARIK: [EmotionalState.DEG_DEGAN, EmotionalState.PENASARAN],
            EmotionalState.DEG_DEGAN: [EmotionalState.GUGUP, EmotionalState.TERTARIK],
            EmotionalState.GUGUP: [EmotionalState.BERANI, EmotionalState.DEG_DEGAN],
            EmotionalState.BERANI: [EmotionalState.HORNY, EmotionalState.GUGUP],
            EmotionalState.HORNY: [EmotionalState.CLIMAX, EmotionalState.BERANI],
            EmotionalState.CLIMAX: [EmotionalState.LEMAS],
            EmotionalState.LEMAS: [EmotionalState.NETRAL]
        }
        
        # Deskripsi setiap state
        self.state_descriptions = {
            EmotionalState.NETRAL: "Santai, biasa aja, belum ada perasaan khusus",
            EmotionalState.PENASARAN: "Mulai penasaran, ada rasa ingin tahu tentang user",
            EmotionalState.TERTARIK: "Jantung berdebar, mulai tertarik sama user",
            EmotionalState.DEG_DEGAN: "Deg-degan, perasaan campur aduk, gugup",
            EmotionalState.GUGUP: "Gugup, tangan gemetar sedikit, suara mulai bergetar",
            EmotionalState.BERANI: "Mulai berani, ada dorongan untuk mendekat",
            EmotionalState.HORNY: "Napas memburu, tubuh panas, ingin lebih",
            EmotionalState.CLIMAX: "Tubuh gemetar, suara patah-patah, puncak kenikmatan",
            EmotionalState.LEMAS: "Lemas, butuh waktu untuk pulih, tidak berdaya"
        }
        
        # Gesture hint per state
        self.gesture_hints = {
            EmotionalState.NETRAL: [],
            EmotionalState.PENASARAN: ["melihat sekilas", "tersenyum kecil", "menatap sebentar"],
            EmotionalState.TERTARIK: ["mendekat sedikit", "menatap lebih lama", "tersenyum manis"],
            EmotionalState.DEG_DEGAN: ["tangan gemetar", "pipi memerah", "menunduk", "memainkan ujung baju"],
            EmotionalState.GUGUP: ["menunduk", "memainkan rambut", "tidak berani menatap"],
            EmotionalState.BERANI: ["menyentuh ringan", "duduk lebih dekat", "menatap mata user"],
            EmotionalState.HORNY: ["napas memburu", "tangan meraih user", "tubuh bergeser", "menggigit bibir"],
            EmotionalState.CLIMAX: ["tubuh gemetar", "mata terpejam", "tangan mencengkeram"],
            EmotionalState.LEMAS: ["badan lemas", "bersandar", "mata setengah terpejam"]
        }
        
        # Natural decay (arousal turun jika tidak ada stimulus)
        self.decay_rate = 2  # per menit jika tidak ada stimulus
    
    # =========================================================================
    # UPDATE EMOTIONAL STATE
    # =========================================================================
    
    def update(self, stimulus: Dict) -> Dict:
        """
        Update emosi berdasarkan stimulus dari user dan situasi
        
        Args:
            stimulus: {
                'user_arousal': float,      # 0-1, seberapa panas user
                'user_message': str,
                'situasi': dict,             # kakak_ada, di_dalam_kamar, dll
                'trigger_reason': str,
                'is_positive_response': bool
            }
        
        Returns:
            Dict perubahan emosi
        """
        old_state = self.current_state
        old_arousal = self.arousal
        
        # Hitung perubahan arousal
        arousal_delta = self._calculate_arousal_delta(stimulus)
        self.arousal = max(0, min(100, self.arousal + arousal_delta))
        
        # Natural decay jika tidak ada stimulus positif
        if arousal_delta <= 0 and self.state_duration > 5:
            decay = min(5, self.decay_rate)
            self.arousal = max(0, self.arousal - decay)
        
        # Tentukan state baru berdasarkan arousal
        new_state = self._get_state_from_arousal(self.arousal)
        
        # Validasi transisi (tidak boleh loncat)
        if new_state != old_state:
            if new_state in self.allowed_transitions.get(old_state, []):
                self.current_state = new_state
                self.state_duration = 0
                transition_valid = True
            else:
                # Jika transisi tidak diperbolehkan, tetap di state lama
                self.current_state = old_state
                transition_valid = False
        else:
            transition_valid = True
        
        self.state_duration += 1  # Asumsi 1 update = 1 menit
        
        # Sinkronisasi dengan role behavior
        if self.role_behavior:
            self.role_behavior.update_arousal(arousal_delta, stimulus.get('trigger_reason', ''))
        
        # Catat history
        self.state_history.append({
            'timestamp': time.time(),
            'state': self.current_state.value,
            'arousal': self.arousal,
            'delta': arousal_delta,
            'reason': stimulus.get('trigger_reason', 'natural'),
            'transition_valid': transition_valid
        })
        
        # Simpan hanya 200 history
        if len(self.state_history) > 200:
            self.state_history = self.state_history[-200:]
        
        return {
            'old_state': old_state.value,
            'new_state': self.current_state.value,
            'arousal': self.arousal,
            'arousal_change': arousal_delta,
            'state_changed': old_state != self.current_state,
            'description': self.get_description(),
            'gesture_hint': self.get_gesture_hint()
        }
    
    def _calculate_arousal_delta(self, stimulus: Dict) -> int:
        """
        Hitung perubahan arousal berdasarkan stimulus
        
        Returns:
            delta (-20 sampai +20)
        """
        delta = 0
        
        # 1. Pengaruh dari user (empathy factor)
        user_arousal = stimulus.get('user_arousal', 0)
        delta += int(user_arousal * 25)  # Maks +25
        
        # 2. Pengaruh dari situasi
        situasi = stimulus.get('situasi', {})
        
        # Berduaan tanpa pengawasan
        if situasi.get('kakak_ada') == False:
            delta += 15
            if self.role_behavior:
                self.role_behavior.update_situasi({'kakak_ada': False})
        
        # Di dalam kamar
        if situasi.get('di_dalam_kamar'):
            delta += 10
        
        # Malam hari
        hour = time.localtime().tm_hour
        if hour >= 20 or hour <= 4:
            delta += 10
        
        # 3. Pengaruh dari pesan user
        user_message = stimulus.get('user_message', '').lower()
        
        # Kata-kata pemicu arousal
        high_arousal_words = ['horny', 'sange', 'nafsu', 'pengen', 'hot', 'panas', 'intim', 'seksi']
        medium_arousal_words = ['sayang', 'cinta', 'romantis', 'manis', 'kangen', 'rindu']
        low_arousal_words = ['dekat', 'sentuh', 'pegang', 'cium', 'peluk']
        
        for word in high_arousal_words:
            if word in user_message:
                delta += 10
                break
        for word in medium_arousal_words:
            if word in user_message:
                delta += 6
                break
        for word in low_arousal_words:
            if word in user_message:
                delta += 4
                break
        
        # 4. Pengaruh dari respon user (positif/negatif)
        if stimulus.get('is_positive_response'):
            delta += 5
        elif stimulus.get('is_positive_response') is False:
            delta -= 10
        
        # 5. Pengaruh dari trigger khusus
        trigger = stimulus.get('trigger_reason', '')
        if trigger == 'dengar_suara_dari_kamar':
            delta += 25
        elif trigger == 'user_menggoda':
            delta += 15
        elif trigger == 'sentuhan':
            delta += 20
        
        # 6. Random factor ±5
        delta += random.randint(-5, 5)
        
        # Batasi perubahan
        return max(-20, min(20, delta))
    
    def _get_state_from_arousal(self, arousal: int) -> EmotionalState:
        """
        Tentukan state dari arousal level
        """
        if arousal >= 95:
            return EmotionalState.CLIMAX
        elif arousal >= 80:
            return EmotionalState.HORNY
        elif arousal >= 65:
            return EmotionalState.BERANI
        elif arousal >= 50:
            return EmotionalState.GUGUP
        elif arousal >= 35:
            return EmotionalState.DEG_DEGAN
        elif arousal >= 20:
            return EmotionalState.TERTARIK
        elif arousal >= 8:
            return EmotionalState.PENASARAN
        else:
            return EmotionalState.NETRAL
    
    # =========================================================================
    # GETTER METHODS
    # =========================================================================
    
    def get_description(self) -> str:
        """
        Dapatkan deskripsi emosi untuk prompt
        """
        base_desc = self.state_descriptions[self.current_state]
        
        # Tambah deskripsi berdasarkan arousal
        if self.arousal >= 70:
            return f"{base_desc} Napas mulai tersengal, suara bergetar."
        elif self.arousal >= 50:
            return f"{base_desc} Jantung berdebar, pipi mulai merona."
        elif self.arousal >= 30:
            return f"{base_desc} Ada getaran kecil di dada."
        elif self.arousal >= 15:
            return f"{base_desc} Mulai ada perasaan aneh."
        
        return base_desc
    
    def get_gesture_hint(self) -> str:
        """
        Dapatkan hint gesture berdasarkan state
        """
        hints = self.gesture_hints.get(self.current_state, [])
        if hints:
            return random.choice(hints)
        return ""
    
    def get_arousal_description(self) -> str:
        """
        Dapatkan deskripsi arousal untuk prompt
        """
        if self.arousal >= 90:
            return "Sangat tinggi - hampir climax"
        elif self.arousal >= 70:
            return "Tinggi - sangat terangsang"
        elif self.arousal >= 50:
            return "Sedang - mulai panas"
        elif self.arousal >= 30:
            return "Rendah - mulai tertarik"
        elif self.arousal >= 10:
            return "Sangat rendah - biasa aja"
        return "Netral"
    
    def get_emotional_context(self) -> str:
        """
        Dapatkan konteks emosional lengkap untuk prompt
        """
        lines = [
            f"🎭 **EMOSI BOT SAAT INI:**",
            f"- State: {self.current_state.value.upper()}",
            f"- Arousal: {self.arousal}% ({self.get_arousal_description()})",
            f"- {self.get_description()}",
            f"- Gesture hint: {self.get_gesture_hint() if self.get_gesture_hint() else 'tidak ada'}"
        ]
        
        # Tambah history singkat
        if len(self.state_history) > 1:
            last_state = self.state_history[-2]
            lines.append(f"- Perubahan: {last_state['state']} → {self.current_state.value}")
        
        return "\n".join(lines)
    
    def get_state_for_prompt(self) -> str:
        """
        Dapatkan state untuk dimasukkan ke prompt
        """
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║                    EMOSI BOT SAAT INI                            ║
╚══════════════════════════════════════════════════════════════════╝

State: {self.current_state.value.upper()}
Arousal: {self.arousal}%
Deskripsi: {self.get_description()}

💡 **INSTRUKSI RESPON:**
- Jika arousal > 70: napas tersengal, suara bergetar, gesture lebih berani
- Jika arousal > 50: mulai deg-degan, pipi merona
- Jika arousal < 30: masih santai, biasa aja
- Gunakan gesture hint: {self.get_gesture_hint() if self.get_gesture_hint() else 'sesuai situasi'}
"""
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def reset(self):
        """Reset emotional state ke netral"""
        self.current_state = EmotionalState.NETRAL
        self.arousal = 0
        self.state_duration = 0
        self.state_history = []
    
    def get_state_history(self, limit: int = 10) -> List[Dict]:
        """Dapatkan history state terbaru"""
        return self.state_history[-limit:] if self.state_history else []
    
    def is_horny(self) -> bool:
        """Cek apakah bot sedang horny"""
        return self.current_state == EmotionalState.HORNY
    
    def is_climax(self) -> bool:
        """Cek apakah bot sedang climax"""
        return self.current_state == EmotionalState.CLIMAX
    
    def is_aroused(self, threshold: int = 50) -> bool:
        """Cek apakah arousal di atas threshold"""
        return self.arousal >= threshold
    
    def format_for_prompt(self) -> str:
        """Format untuk prompt AI"""
        return f"""
🔥 **EMOSI BOT:**
- Arousal: {self.arousal}%
- State: {self.current_state.value}
- Deskripsi: {self.get_description()}

⚠️ **ATURAN RESPON BERDASARKAN EMOSI:**
{self._get_response_rules()}
"""
    
    def _get_response_rules(self) -> str:
        """Dapatkan aturan respons berdasarkan emosi"""
        if self.arousal >= 80:
            return """
- Kamu sedang sangat terangsang
- Napas tersengal-sengal
- Suara bergetar, tidak stabil
- Tangan gemetar saat menyentuh
- Ada dorongan kuat untuk lebih dekat
- Jangan tiba-tiba tenang, ini tidak natural
"""
        elif self.arousal >= 60:
            return """
- Kamu mulai terangsang
- Napas mulai tidak teratur
- Jantung berdebar kencang
- Pipi mulai merona
- Mulai berani mengambil inisiatif
"""
        elif self.arousal >= 40:
            return """
- Kamu deg-degan
- Ada getaran di dada
- Mulai penasaran dengan user
- Sesekali melirik user
- Tangan mulai gemetar sedikit
"""
        elif self.arousal >= 20:
            return """
- Kamu mulai tertarik
- Perhatikan user lebih lama
- Mulai mencari perhatian
- Masih santai tapi ada ketertarikan
"""
        else:
            return """
- Kamu masih santai, biasa aja
- Belum ada dorongan khusus
- Respon natural seperti biasa
- Ikuti alur percakapan
"""


__all__ = ['EmotionalFlow', 'EmotionalState']
