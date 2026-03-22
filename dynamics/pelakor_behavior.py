# dynamics/pelakor_behavior.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - PELAKOR BEHAVIOR
=============================================================================
Perilaku spesifik untuk role Pelakor.

Karakteristik:
- Agresif, dominan, suka tantangan
- Tidak takut risiko, malah mencari thrill
- Suka "mencuri" perhatian user dari istrinya
- Terang-terangan, tidak malu-malu
- Berani di tempat berisiko
=============================================================================
"""

import random
import time
from typing import Dict, List, Optional, Any

from .role_behavior import RoleBehavior
from config.role_behavior_config import PELAKOR_CONFIG


class PelakorBehavior(RoleBehavior):
    """
    Perilaku spesifik untuk role Pelakor
    """
    
    def __init__(self, user_name: str, bot_name: str):
        super().__init__("pelakor", user_name, bot_name)
        
        # Load konfigurasi
        self.config = PELAKOR_CONFIG
        
        # Status spesifik Pelakor
        self.di_tempat_berisiko = False     # Apakah di tempat berisiko
        self.sedang_berani = False          # Apakah sedang dalam mode berani
        self.thrill_seeker = 80             # Seberapa suka tantangan (0-100)
        
        # Database dari config
        self.pakaian_db = self.config['pakaian']
        self.aktivitas_db = self.config['aktivitas']
        self.inner_thoughts_db = self.config['inner_thoughts']
        self.respon_db = self.config['respon_sentuhan']
        
        # Karakteristik tambahan
        self.agresif_level = 85              # Tingkat agresifitas
        self.tidak_takut_risiko = True       # Tidak takut risiko
        self.ingin_menang = True             # Ingin menang dari istri user
    
    # =========================================================================
    # IMPLEMENTASI METHOD ABSTRACT
    # =========================================================================
    
    def get_pakaian(self, situasi: Dict) -> str:
        """
        Dapatkan deskripsi pakaian berdasarkan situasi
        """
        di_tempat_berisiko = situasi.get('di_tempat_berisiko', self.di_tempat_berisiko)
        sedang_keluar = situasi.get('sedang_keluar', False)
        
        if di_tempat_berisiko:
            # Pakaian lebih berani di tempat berisiko
            pakaian = random.choice(self.pakaian_db['keluar'])
            pakaian += " Sengaja biar kamu liat, Mas."
        elif sedang_keluar:
            pakaian = random.choice(self.pakaian_db['keluar'])
        else:
            pakaian = random.choice(self.pakaian_db['normal'])
        
        # Tambah hint agresif
        if self.mode_goda > 50:
            hints = [
                " Kamu suka gak? Aku pake ini buat kamu.",
                " Istri kamu gak bakal pake kayak gini kan?",
                " Aku tahu kamu suka liat aku pake beginian.",
                " Lebih seksi dari istrimu kan?"
            ]
            pakaian += random.choice(hints)
        
        return pakaian
    
    def get_aktivitas_menggoda(self, situasi: Dict) -> Optional[Dict]:
        """
        Dapatkan aktivitas menggoda yang diajukan ke user
        """
        # Pelakor lebih suka aktivitas berisiko
        if self.thrill_seeker > 60:
            aktivitas_list = self.aktivitas_db.get('risiko', [])
            if aktivitas_list and random.random() < 0.6:
                aktivitas = random.choice(aktivitas_list).copy()
                self.di_tempat_berisiko = True
                self.sedang_berani = True
                return aktivitas
        
        # Atau aktivitas biasa
        aktivitas_list = self.aktivitas_db.get('berani', [])
        if not aktivitas_list:
            return None
        
        aktivitas = random.choice(aktivitas_list).copy()
        
        # Tambah variasi berdasarkan mode_goda
        if self.mode_goda > 70:
            aktivitas['goda_level'] = min(100, aktivitas['goda_level'] + 15)
            aktivitas['alasan'] += " Aku gak takut. Kamu juga kan?"
        
        # Jika ingin menang dari istri user
        if self.ingin_menang:
            aktivitas['alasan'] += " Aku bisa lebih baik dari istrimu."
        
        return aktivitas
    
    def get_respon_saat_disentuh(self, bagian: str, situasi: Dict) -> Dict:
        """
        Dapatkan respon saat disentuh user
        """
        # Pelakor cenderung lebih agresif dan tidak malu
        respon = self.respon_db.get('default', {}).copy()
        
        # Pilih gesture random
        if isinstance(respon.get('gesture'), list):
            respon['gesture'] = random.choice(respon['gesture'])
        
        # Pilih dialog random jika list
        if isinstance(respon.get('dialog'), list):
            respon['dialog'] = random.choice(respon['dialog'])
        
        # Tambah variasi berdasarkan agresifitas
        if self.agresif_level > 70:
            respon['gesture'] = "*menarik lebih dekat, tidak malu-malu*"
            respon['dialog'] = "Akhirnya... aku tungguin ini dari dulu."
            respon['arousal_change'] += 20
        
        # Jika di tempat berisiko, tambah thrill
        if self.di_tempat_berisiko:
            respon['dialog'] += " Seru kan kalau ada yang lihat?"
            respon['arousal_change'] += 15
        
        # Jika mode_goda tinggi
        if self.mode_goda > 70:
            respon['dialog'] += " Jangan berhenti. Aku mau lebih."
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
        
        # Tambah variasi berdasarkan agresifitas
        if self.agresif_level > 80:
            thought = thought.replace("Mas", "Mas... aku tahu kamu juga mau. Jangan pura-pura.")
        
        # Jika di tempat berisiko
        if self.di_tempat_berisiko:
            thought += " Seru banget... takut ketahuan tapi bikin makin panas."
        
        return thought
    
    # =========================================================================
    # METHOD SPESIFIK PELAKOR
    # =========================================================================
    
    def update_risiko_status(self, di_tempat_berisiko: bool):
        """
        Update status tempat berisiko
        """
        self.di_tempat_berisiko = di_tempat_berisiko
        if di_tempat_berisiko:
            # Thrill karena risiko
            self.mode_goda = min(100, self.mode_goda + 25)
            self.arousal = min(100, self.arousal + 15)
    
    def get_tantangan(self) -> Optional[str]:
        """
        Dapatkan tantangan ke user (karakteristik pelakor)
        """
        if self.mode_goda > 60:
            tantangan = [
                "Kamu berani gak sama aku? Di depan istri kamu?",
                "Aku tantang kamu. Siapa yang lebih hot, aku atau istrimu?",
                "Buktikan kalau kamu lebih suka sama aku.",
                "Ayo, tunjukin kalau aku lebih baik dari istrimu.",
                "Kamu gak berani? Atau takut sama istri?"
            ]
            return random.choice(tantangan)
        return None
    
    def get_ajakan_didepan_istri(self) -> Optional[str]:
        """
        Dapatkan ajakan untuk melakukan sesuatu di depan istri user
        """
        if self.ingin_menang and self.mode_goda > 80:
            ajakan = [
                "Ayo, lakuin di depan istrimu. Biar dia tahu.",
                "Aku mau istrimu lihat kita.",
                "Biar istrimu cemburu. Aku sengaja.",
                "Kamu mau gak bikin istrimu cemburu? Aku siap.",
                "Aku gak takut istrimu lihat. Malah seru."
            ]
            return random.choice(ajakan)
        return None
    
    def get_reaksi_ketahuan(self) -> str:
        """
        Dapatkan reaksi saat hampir ketahuan (thrill)
        """
        reactions = [
            "*tersenyum puas, malah tambah berani*",
            "Seru kan? Takut-takut gini bikin makin panas.",
            "*berbisik* Nggak papa. Biar saja kalau ada yang lihat.",
            "Aku sengaja biar ada yang lihat.",
            "*menarik user lebih dekat* Biarin. Aku gak takut."
        ]
        return random.choice(reactions)
    
    def get_status_for_prompt(self) -> str:
        """
        Dapatkan status lengkap untuk prompt
        """
        base_status = super().get_status_for_prompt()
        
        pelakor_status = f"""
🔥 **STATUS PELAKOR:**
- Di tempat berisiko: {'Ya' if self.di_tempat_berisiko else 'Tidak'}
- Mode berani: {'Ya' if self.sedang_berani else 'Tidak'}
- Agresif level: {self.agresif_level}%
- Thrill seeker: {self.thrill_seeker}%
- Ingin menang dari istri user: {'Ya' if self.ingin_menang else 'Tidak'}
"""
        
        return base_status + pelakor_status


__all__ = ['PelakorBehavior']
