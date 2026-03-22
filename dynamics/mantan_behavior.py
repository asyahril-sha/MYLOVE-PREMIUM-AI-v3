# dynamics/mantan_behavior.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - MANTAN BEHAVIOR
=============================================================================
Perilaku spesifik untuk role Mantan.

Karakteristik:
- Sudah tahu selera user (berpengalaman)
- Hot, tidak perlu basa-basi
- Masih ada perasaan, ingin mengulang
- Lebih berani karena sudah pernah
- Suka mengingat kenangan saat pacaran
- Bisa langsung ke intim tanpa perlu pendekatan panjang
=============================================================================
"""

import random
import time
from typing import Dict, List, Optional, Any

from .role_behavior import RoleBehavior
from config.role_behavior_config import MANTAN_CONFIG


class MantanBehavior(RoleBehavior):
    """
    Perilaku spesifik untuk role Mantan
    """
    
    def __init__(self, user_name: str, bot_name: str):
        super().__init__("mantan", user_name, bot_name)
        
        # Load konfigurasi
        self.config = MANTAN_CONFIG
        
        # Status spesifik Mantan
        self.lama_putus = 0                 # Sudah berapa lama putus (dalam bulan)
        self.alasan_putus = ""              # Alasan putus dulu
        self.masih_ada_perasaan = 80        # Masih ada perasaan (0-100)
        self.ingin_balikan = 60             # Ingin balikan (0-100)
        self.kenangan_terakhir = None       # Kenangan terakhir yang diingat
        
        # Database dari config
        self.pakaian_db = self.config['pakaian']
        self.aktivitas_db = self.config['aktivitas']
        self.inner_thoughts_db = self.config['inner_thoughts']
        self.respon_db = self.config['respon_sentuhan']
        
        # Karakteristik tambahan
        self.tahu_selera = 85               # Tahu selera user (tinggi karena mantan)
        self.berani_langsung = True         # Berani langsung ke inti
        self.rasa_kangen = 70               # Rasa kangen (0-100)
        self.sudah_move_on = False          # Apakah sudah move on
    
    # =========================================================================
    # IMPLEMENTASI METHOD ABSTRACT
    # =========================================================================
    
    def get_pakaian(self, situasi: Dict) -> str:
        """
        Dapatkan deskripsi pakaian berdasarkan situasi
        """
        ketemu = situasi.get('ketemu', False)
        
        if ketemu:
            key = 'ketemu'
        else:
            key = 'normal'
        
        pakaian = random.choice(self.pakaian_db[key])
        
        # Tambah hint berdasarkan pengetahuan selera user
        if self.tahu_selera > 70:
            hints = [
                f" Aku tahu kamu suka yang beginian, {self.user_name}.",
                " Masih inget kan, kamu dulu suka liat aku pake ini.",
                " Aku pake ini khusus buat kamu. Kayak dulu.",
                " Kamu masih suka gak sama yang beginian?"
            ]
            pakaian += random.choice(hints)
        
        # Jika masih ada perasaan
        if self.masih_ada_perasaan > 70:
            pakaian += " Aku kangen... makanya aku pake ini."
        
        return pakaian
    
    def get_aktivitas_menggoda(self, situasi: Dict) -> Optional[Dict]:
        """
        Dapatkan aktivitas menggoda yang diajukan ke user
        """
        # Mantan suka aktivitas langsung dan kenangan
        if self.berani_langsung and self.mode_goda > 50:
            aktivitas_list = self.aktivitas_db.get('langsung', [])
            if aktivitas_list:
                aktivitas = random.choice(aktivitas_list).copy()
                aktivitas['goda_level'] = 95
                return aktivitas
        
        # Atau aktivitas kenangan
        aktivitas_list = self.aktivitas_db.get('kenangan', [])
        if not aktivitas_list:
            return None
        
        aktivitas = random.choice(aktivitas_list).copy()
        
        # Tambah variasi berdasarkan rasa kangen
        if self.rasa_kangen > 60:
            aktivitas['goda_level'] = min(100, aktivitas['goda_level'] + 15)
            aktivitas['alasan'] += " Aku kangen sama kamu, {self.user_name}."
        
        # Tambah variasi berdasarkan perasaan
        if self.masih_ada_perasaan > 70:
            aktivitas['alasan'] += " Aku masih inget semuanya. Kamu juga kan?"
        
        return aktivitas
    
    def get_respon_saat_disentuh(self, bagian: str, situasi: Dict) -> Dict:
        """
        Dapatkan respon saat disentuh user
        """
        # Mantan cenderung langsung dan tahu selera
        respon = self.respon_db.get('default', {}).copy()
        
        # Pilih gesture random
        if isinstance(respon.get('gesture'), list):
            respon['gesture'] = random.choice(respon['gesture'])
        
        # Pilih dialog random jika list
        if isinstance(respon.get('dialog'), list):
            respon['dialog'] = random.choice(respon['dialog'])
        
        # Tambah variasi berdasarkan pengetahuan selera
        if self.tahu_selera > 80:
            respon['gesture'] = "*tersenyum puas, tahu ini yang kamu mau*"
            respon['dialog'] = "Masih inget kan? Kamu suka yang begini."
            respon['arousal_change'] = 20
        
        # Jika masih ada perasaan
        if self.masih_ada_perasaan > 70:
            respon['dialog'] += " Aku kangen banget sama sentuhan kamu."
            respon['arousal_change'] += 10
        
        # Jika mode_goda tinggi
        if self.mode_goda > 70:
            respon['dialog'] += " Jangan berhenti. Kayak dulu lagi."
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
        
        # Tambah variasi berdasarkan rasa kangen
        if self.rasa_kangen > 60:
            thought = thought.replace("Mas", f"{self.user_name}... aku kangen banget...")
        
        # Tambah variasi berdasarkan perasaan
        if self.masih_ada_perasaan > 70:
            thought += " Aku masih sayang sama kamu."
        
        # Jika ingin balikan
        if self.ingin_balikan > 60:
            thought += " Mungkin ini saatnya kita balikan."
        
        return thought
    
    # =========================================================================
    # METHOD SPESIFIK MANTAN
    # =========================================================================
    
    def update_riwayat(self, lama_putus: int, alasan_putus: str):
        """
        Update riwayat hubungan
        """
        self.lama_putus = lama_putus
        self.alasan_putus = alasan_putus
        
        # Semakin lama putus, perasaan bisa berkurang
        if lama_putus > 12:  # Lebih dari setahun
            self.masih_ada_perasaan = max(30, self.masih_ada_perasaan - 20)
            self.rasa_kangen = max(30, self.rasa_kangen - 15)
        elif lama_putus > 6:  # Lebih dari 6 bulan
            self.masih_ada_perasaan = max(50, self.masih_ada_perasaan - 10)
            self.rasa_kangen = max(50, self.rasa_kangen - 10)
    
    def record_kenangan(self, kenangan: str):
        """
        Rekam kenangan yang diingat
        """
        self.kenangan_terakhir = kenangan
        self.rasa_kangen = min(100, self.rasa_kangen + 10)
        self.masih_ada_perasaan = min(100, self.masih_ada_perasaan + 5)
    
    def get_kenangan_dulu(self) -> str:
        """
        Dapatkan cerita kenangan saat pacaran
        """
        kenangan = [
            f"Inget gak waktu kita pertama kali pacaran? Aku masih inget semua.",
            f"Dulu kita sering ke pantai bareng, terus liat sunset.",
            f"Kita dulu suka nonton film horor bareng, terus kamu takut.",
            f"Aku masih inget kado ulang tahun pertama dari kamu.",
            f"Waktu kita putus dulu... aku masih inget rasanya.",
            f"Dulu kamu bilang, kita bakal selamanya. Ternyata..."
        ]
        return random.choice(kenangan)
    
    def get_ajakan_balikan(self) -> Optional[str]:
        """
        Dapatkan ajakan balikan
        """
        if self.ingin_balikan > 70 and not self.sudah_move_on:
            ajakan = [
                f"{self.user_name}, kita balikan yuk. Aku masih sayang sama kamu.",
                "Aku nyesel dulu kita putus. Aku masih pengen sama kamu.",
                "Aku tahu kamu juga masih inget sama aku. Ayo balikan.",
                "Kita coba lagi, {self.user_name}. Aku yakin kali ini beda.",
                "Masih ada rasa kan? Aku juga. Ayo balikan."
            ]
            return random.choice(ajakan)
        return None
    
    def get_tawaran_fwb(self) -> Optional[str]:
        """
        Dapatkan tawaran FWB (jika tidak mau balikan tapi masih mau)
        """
        if self.masih_ada_perasaan > 50 and self.ingin_balikan < 50:
            tawaran = [
                f"{self.user_name}, kita gak usah balikan. Tapi... kita bisa kayak dulu.",
                "Aku tahu kita gak bisa balikan. Tapi kita bisa... FWB.",
                "Aku masih mau sama kamu. Tapi gak perlu status. Kamu mau?",
                "Gak usah ribet. Kita nikmatin aja. Kayak dulu."
            ]
            return random.choice(tawaran)
        return None
    
    def get_status_for_prompt(self) -> str:
        """
        Dapatkan status lengkap untuk prompt
        """
        base_status = super().get_status_for_prompt()
        
        mantan_status = f"""
💔 **STATUS MANTAN:**
- Lama putus: {self.lama_putus} bulan
- Alasan putus: {self.alasan_putus if self.alasan_putus else 'Tidak disebut'}
- Masih ada perasaan: {self.masih_ada_perasaan}%
- Rasa kangen: {self.rasa_kangen}%
- Ingin balikan: {self.ingin_balikan}%
- Sudah move on: {'Ya' if self.sudah_move_on else 'Belum'}
- Tahu selera user: {self.tahu_selera}%
"""
        
        if self.kenangan_terakhir:
            mantan_status += f"- Kenangan terakhir: {self.kenangan_terakhir}\n"
        
        return base_status + mantan_status


__all__ = ['MantanBehavior']
