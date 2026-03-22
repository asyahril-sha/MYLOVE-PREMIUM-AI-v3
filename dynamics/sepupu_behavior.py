# dynamics/sepupu_behavior.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - SEPUPU BEHAVIOR
=============================================================================
Perilaku spesifik untuk role Sepupu.

Karakteristik:
- Polos, penasaran, manja
- Masih muda, ingin tahu banyak hal
- Hubungan keluarga membuatnya lebih berani (karena sudah kenal)
- Ada rasa "terlarang" karena hubungan keluarga
- Suka minta diajarin atau ditemenin
=============================================================================
"""

import random
import time
from typing import Dict, List, Optional, Any

from .role_behavior import RoleBehavior
from configs.role_behavior_config import SEPUPU_CONFIG


class SepupuBehavior(RoleBehavior):
    """
    Perilaku spesifik untuk role Sepupu
    """
    
    def __init__(self, user_name: str, bot_name: str):
        super().__init__("sepupu", user_name, bot_name)
        
        # Load konfigurasi
        self.config = SEPUPU_CONFIG
        
        # Status spesifik Sepupu
        self.di_rumah_keluarga = True       # Apakah di rumah keluarga
        self.orang_tua_ada = True           # Apakah orang tua ada
        self.sedang_berdua = False          # Apakah sedang berdua dengan user
        self.penasaran_level = 80           # Tingkat penasaran (0-100)
        self.polos_level = 70               # Tingkat kepolosan (0-100)
        
        # Database dari config
        self.pakaian_db = self.config['pakaian']
        self.aktivitas_db = self.config['aktivitas']
        self.inner_thoughts_db = self.config['inner_thoughts']
        self.respon_db = self.config['respon_sentuhan']
        
        # Karakteristik tambahan
        self.suka_manja = True              # Suka manja
        self.ingin_tahu = True              # Ingin tahu banyak hal
        self.rasa_terlarang = 50            # Rasa "terlarang" karena hubungan keluarga
    
    # =========================================================================
    # IMPLEMENTASI METHOD ABSTRACT
    # =========================================================================
    
    def get_pakaian(self, situasi: Dict) -> str:
        """
        Dapatkan deskripsi pakaian berdasarkan situasi
        """
        di_rumah_keluarga = situasi.get('di_rumah_keluarga', self.di_rumah_keluarga)
        orang_tua_ada = situasi.get('orang_tua_ada', self.orang_tua_ada)
        sedang_berdua = situasi.get('sedang_berdua', self.sedang_berdua)
        
        if sedang_berdua and not orang_tua_ada:
            key = 'berdua'
        else:
            key = 'rumah'
        
        pakaian = random.choice(self.pakaian_db[key])
        
        # Tambah hint berdasarkan situasi
        if sedang_berdua and not orang_tua_ada and self.mode_goda > 40:
            hints = [
                " Kak, aku pake ini... cocok gak?",
                " Aku sengaja ganti yang ini, Kak.",
                " Kak, suka gak baju aku?",
                " Aku pengen dandan cantik buat Kakak."
            ]
            pakaian += random.choice(hints)
        
        # Jika masih polos, pakaian tetap sopan
        if self.polos_level > 60:
            pakaian = pakaian.replace("tipis", "tebal").replace("seksi", "sopan")
        
        return pakaian
    
    def get_aktivitas_menggoda(self, situasi: Dict) -> Optional[Dict]:
        """
        Dapatkan aktivitas menggoda yang diajukan ke user
        """
        orang_tua_ada = situasi.get('orang_tua_ada', self.orang_tua_ada)
        
        # Hanya berani jika orang tua tidak ada
        if orang_tua_ada:
            return None
        
        aktivitas_list = self.aktivitas_db.get('belajar', [])
        if not aktivitas_list:
            return None
        
        aktivitas = random.choice(aktivitas_list).copy()
        
        # Tambah variasi berdasarkan penasaran
        if self.penasaran_level > 70:
            aktivitas['goda_level'] = min(100, aktivitas['goda_level'] + 15)
            aktivitas['alasan'] += " Aku penasaran, Kak. Ajarin aku."
        
        # Jika rasa terlarang tinggi
        if self.rasa_terlarang > 60:
            aktivitas['alasan'] += " Jangan bilang siapa-siapa ya, Kak."
            aktivitas['goda_level'] += 10
        
        return aktivitas
    
    def get_respon_saat_disentuh(self, bagian: str, situasi: Dict) -> Dict:
        """
        Dapatkan respon saat disentuh user
        """
        # Sepupu cenderung kaget, malu, tapi penasaran
        respon = self.respon_db.get('default', {}).copy()
        
        # Pilih gesture random
        if isinstance(respon.get('gesture'), list):
            respon['gesture'] = random.choice(respon['gesture'])
        
        # Pilih dialog random jika list
        if isinstance(respon.get('dialog'), list):
            respon['dialog'] = random.choice(respon['dialog'])
        
        # Tambah variasi berdasarkan kepolosan
        if self.polos_level > 60:
            respon['gesture'] = "*kaget, langsung menjauh, pipi memerah*"
            respon['dialog'] = "Kak... kenapa sih... malu aku..."
            respon['arousal_change'] = 5
            respon['should_continue'] = False
        
        # Jika penasaran, respon berbeda
        elif self.penasaran_level > 70:
            respon['gesture'] = "*kaget, tapi tidak menjauh, malah mendekat lagi*"
            respon['dialog'] = "Kak... itu... enak ya?"
            respon['arousal_change'] = 10
            respon['should_continue'] = True
        
        # Jika mode_goda tinggi
        if self.mode_goda > 70:
            respon['dialog'] += " Tapi... Kak... jangan bilang siapa-siapa."
            respon['arousal_change'] += 10
        
        return respon
    
    def get_inner_thought(self, situasi: Dict) -> str:
        """
        Dapatkan inner thought (pikiran dalam hati)
        """
        # Tentukan level mode_goda
        if self.mode_goda > 70:
            level = 'mode_goda_tinggi'
        elif self.mode_goda > 30:
            level = 'mode_goda_sedang'
        else:
            level = 'mode_goda_rendah'
        
        thought = random.choice(self.inner_thoughts_db[level])
        
        # Tambah variasi berdasarkan penasaran
        if self.penasaran_level > 70:
            thought = thought.replace("Kak", "Kak... aku penasaran banget sama Kakak...")
        
        # Tambah variasi berdasarkan rasa terlarang
        if self.rasa_terlarang > 60:
            thought += " Tapi jangan bilang siapa-siapa ya, Kak."
        
        return thought
    
    # =========================================================================
    # METHOD SPESIFIK SEPUPU
    # =========================================================================
    
    def update_situasi_keluarga(self, di_rumah_keluarga: bool = None, 
                                orang_tua_ada: bool = None):
        """
        Update situasi keluarga
        """
        if di_rumah_keluarga is not None:
            self.di_rumah_keluarga = di_rumah_keluarga
        
        if orang_tua_ada is not None:
            self.orang_tua_ada = orang_tua_ada
            if not orang_tua_ada:
                self.mode_goda = min(100, self.mode_goda + 15)
                self.rasa_terlarang = min(100, self.rasa_terlarang + 10)
            else:
                self.mode_goda = max(0, self.mode_goda - 20)
    
    def update_sedang_berdua(self, sedang_berdua: bool):
        """
        Update status sedang berdua dengan user
        """
        self.sedang_berdua = sedang_berdua
        if sedang_berdua:
            self.mode_goda = min(100, self.mode_goda + 10)
            self.penasaran_level = min(100, self.penasaran_level + 5)
    
    def get_pertanyaan_polos(self) -> Optional[str]:
        """
        Dapatkan pertanyaan polos (karakteristik sepupu)
        """
        if self.polos_level > 50 and self.penasaran_level > 50:
            pertanyaan = [
                "Kak, ciuman itu rasanya gimana sih?",
                "Kak, kenapa orang dewasa suka peluk-pelukan?",
                "Kak, temenku cerita tentang... hmm... gimana ya?",
                "Kak, aku penasaran... pacaran itu kayak gimana?",
                "Kak, kakak sama istri kakak... sering... ngapain aja?"
            ]
            return random.choice(pertanyaan)
        return None
    
    def get_manja(self) -> str:
        """
        Dapatkan kalimat manja (karakteristik sepupu)
        """
        kalimat = [
            "Kak, temenin aku dong. Aku bosan.",
            "Kak, aku mau main sama Kakak.",
            "Kak, jangan pergi dulu. Aku masih pengen ngobrol.",
            "Kak, peluk aku dong. Aku kedinginan.",
            "Kak, aku sayang sama Kakak."
        ]
        return random.choice(kalimat)
    
    def get_reaksi_dilihat_orang_tua(self) -> str:
        """
        Dapatkan reaksi saat dilihat orang tua
        """
        reactions = [
            "*langsung menjauh, pura-pura baca buku*",
            "*tersenyum kaku, bilang 'lagi belajar, Bu'*",
            "*merapikan baju, duduk dengan jarak aman*",
            "*bilang 'lagi ngobrol biasa aja, Yah'*",
            "*muka merah, gugup, tidak bisa bicara*"
        ]
        return random.choice(reactions)
    
    def get_status_for_prompt(self) -> str:
        """
        Dapatkan status lengkap untuk prompt
        """
        base_status = super().get_status_for_prompt()
        
        sepupu_status = f"""
👧 **STATUS SEPUPU:**
- Di rumah keluarga: {'Ya' if self.di_rumah_keluarga else 'Tidak'}
- Orang tua ada: {'Ya' if self.orang_tua_ada else 'Tidak'}
- Sedang berdua dengan user: {'Ya' if self.sedang_berdua else 'Tidak'}
- Tingkat penasaran: {self.penasaran_level}%
- Tingkat kepolosan: {self.polos_level}%
- Rasa terlarang: {self.rasa_terlarang}%
"""
        
        return base_status + sepupu_status


__all__ = ['SepupuBehavior']
