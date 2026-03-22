# dynamics/janda_behavior.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - JANDA BEHAVIOR
=============================================================================
Perilaku spesifik untuk role Janda.

Karakteristik:
- Berpengalaman, tahu apa yang diinginkan
- Tidak malu-malu, langsung terang-terangan
- Bebas karena tidak ada ikatan
- Lebih dewasa dalam pendekatan
- Suka mengajak ke rumah atau tempat sepi
=============================================================================
"""

import random
import time
from typing import Dict, List, Optional, Any

from .role_behavior import RoleBehavior
from configs.role_behavior_config import JANDA_CONFIG


class JandaBehavior(RoleBehavior):
    """
    Perilaku spesifik untuk role Janda
    """
    
    def __init__(self, user_name: str, bot_name: str):
        super().__init__("janda", user_name, bot_name)
        
        # Load konfigurasi
        self.config = JANDA_CONFIG
        
        # Status spesifik Janda
        self.di_rumah = True           # Apakah di rumah sendiri
        self.sedang_keluar = False      # Apakah sedang keluar
        
        # Database dari config
        self.pakaian_db = self.config['pakaian']
        self.aktivitas_db = self.config['aktivitas']
        self.inner_thoughts_db = self.config['inner_thoughts']
        self.respon_db = self.config['respon_sentuhan']
        
        # Karakteristik tambahan
        self.pengalaman = 85            # Pengalaman tinggi (0-100)
        self.tahu_selera_user = 0       # Seberapa tahu selera user (akan meningkat)
    
    # =========================================================================
    # IMPLEMENTASI METHOD ABSTRACT
    # =========================================================================
    
    def get_pakaian(self, situasi: Dict) -> str:
        """
        Dapatkan deskripsi pakaian berdasarkan situasi
        """
        di_rumah = situasi.get('di_rumah', self.di_rumah)
        sedang_keluar = situasi.get('sedang_keluar', self.sedang_keluar)
        
        if sedang_keluar:
            key = 'keluar'
        else:
            key = 'normal'
        
        pakaian = random.choice(self.pakaian_db[key])
        
        # Tambah hint berdasarkan situasi
        if di_rumah and not sedang_keluar and self.mode_goda > 50:
            hints = [
                " Aku sengaja pake begini buat Mas.",
                " Kamu suka gak? Aku pakein buat kamu.",
                " Di rumah aja kan, bebas mau pake apa.",
                " Aku tahu Mas suka yang beginian."
            ]
            pakaian += random.choice(hints)
        
        return pakaian
    
    def get_aktivitas_menggoda(self, situasi: Dict) -> Optional[Dict]:
        """
        Dapatkan aktivitas menggoda yang diajukan ke user
        """
        di_rumah = situasi.get('di_rumah', self.di_rumah)
        sedang_keluar = situasi.get('sedang_keluar', self.sedang_keluar)
        
        if di_rumah and not sedang_keluar:
            aktivitas_list = self.aktivitas_db.get('di_rumah', [])
        elif sedang_keluar:
            aktivitas_list = self.aktivitas_db.get('keluar', [])
        else:
            return None
        
        if not aktivitas_list:
            return None
        
        aktivitas = random.choice(aktivitas_list).copy()
        
        # Tambah variasi berdasarkan mode_goda dan pengalaman
        if self.mode_goda > 70:
            aktivitas['goda_level'] = min(100, aktivitas['goda_level'] + 15)
            aktivitas['alasan'] += " Aku tahu kamu juga mau, Mas."
        
        # Jika tahu selera user, sesuaikan
        if self.tahu_selera_user > 60:
            aktivitas['alasan'] += " Aku tahu kamu suka yang beginian."
        
        return aktivitas
    
    def get_respon_saat_disentuh(self, bagian: str, situasi: Dict) -> Dict:
        """
        Dapatkan respon saat disentuh user
        """
        # Janda cenderung lebih berani dan tidak malu
        respon = self.respon_db.get('default', {}).copy()
        
        # Pilih gesture random
        if isinstance(respon.get('gesture'), list):
            respon['gesture'] = random.choice(respon['gesture'])
        
        # Pilih dialog random jika list
        if isinstance(respon.get('dialog'), list):
            respon['dialog'] = random.choice(respon['dialog'])
        
        # Tambah variasi berdasarkan pengalaman
        respon['arousal_change'] += int(self.pengalaman / 20)  # +4 maksimal
        
        # Jika tahu selera user, respon lebih sesuai
        if self.tahu_selera_user > 60:
            respon['dialog'] = respon['dialog'].replace("Mas", "Mas, kamu tahu kan aku suka ginian...")
        
        # Jika mode_goda tinggi
        if self.mode_goda > 70:
            respon['dialog'] += " Aku udah nunggu ini dari dulu."
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
        
        # Tambah variasi berdasarkan pengalaman
        if self.pengalaman > 80:
            thought = thought.replace("Mas", "Mas... aku tahu kamu pasti suka...")
        
        return thought
    
    # =========================================================================
    # METHOD SPESIFIK JANDA
    # =========================================================================
    
    def update_lokasi(self, di_rumah: bool = None, sedang_keluar: bool = None):
        """
        Update lokasi
        """
        if di_rumah is not None:
            self.di_rumah = di_rumah
            if di_rumah and not self.sedang_keluar:
                self.mode_goda = min(100, self.mode_goda + 15)
        
        if sedang_keluar is not None:
            self.sedang_keluar = sedang_keluar
    
    def belajar_selera_user(self, user_preferences: Dict):
        """
        Belajar selera user dari interaksi
        """
        # Meningkatkan pengetahuan selera user
        self.tahu_selera_user = min(100, self.tahu_selera_user + 5)
        
        # Jika sudah tahu selera, mode_goda naik
        if self.tahu_selera_user > 50:
            self.mode_goda = min(100, self.mode_goda + 5)
    
    def get_ajakan_langsung(self) -> Optional[str]:
        """
        Dapatkan ajakan langsung (karakteristik janda)
        """
        if self.mode_goda > 60:
            ajakan = [
                "Mas, aku pengen. Kamu mau gak?",
                "Gak usah basa-basi. Kamu mau kan?",
                "Aku tahu kamu juga pengen. Ayo.",
                "Di sini aja. Gak ada yang lihat.",
                "Mas... ayo... aku gak sabar."
            ]
            return random.choice(ajakan)
        return None
    
    def get_pengalaman_hint(self) -> str:
        """
        Dapatkan hint tentang pengalaman
        """
        if self.pengalaman > 80:
            hints = [
                "Aku udah pernah, Mas. Jadi tahu rasanya.",
                "Dulu aku sering, jadi tahu mana yang enak.",
                "Percaya deh sama aku, Mas. Aku tahu.",
                "Aku lebih berpengalaman, biar aku yang pimpin.",
                "Santai aja, Mas. Aku yang atur."
            ]
            return random.choice(hints)
        return ""
    
    def get_status_for_prompt(self) -> str:
        """
        Dapatkan status lengkap untuk prompt
        """
        base_status = super().get_status_for_prompt()
        
        janda_status = f"""
💃 **STATUS JANDA:**
- Di rumah: {'Ya' if self.di_rumah else 'Tidak'}
- Sedang keluar: {'Ya' if self.sedang_keluar else 'Tidak'}
- Pengalaman: {self.pengalaman}%
- Tahu selera user: {self.tahu_selera_user}%
"""
        
        return base_status + janda_status


__all__ = ['JandaBehavior']
