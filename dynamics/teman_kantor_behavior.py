# dynamics/teman_kantor_behavior.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - TEMAN KANTOR BEHAVIOR
=============================================================================
Perilaku spesifik untuk role Teman Kantor.

Karakteristik:
- Profesional di luar, liar di dalam
- Memanfaatkan situasi kantor sepi (lembur, gudang, pantry)
- Suka "kebetulan" bertemu di tempat sepi
- Ada thrill karena risiko ketahuan rekan kerja
=============================================================================
"""

import random
import time
from typing import Dict, List, Optional, Any

from .role_behavior import RoleBehavior
from configs.role_behavior_config import TEMAN_KANTOR_CONFIG


class TemanKantorBehavior(RoleBehavior):
    """
    Perilaku spesifik untuk role Teman Kantor
    """
    
    def __init__(self, user_name: str, bot_name: str):
        super().__init__("teman_kantor", user_name, bot_name)
        
        # Load konfigurasi
        self.config = TEMAN_KANTOR_CONFIG
        
        # Status spesifik Teman Kantor
        self.kantor_sepi = False         # Apakah kantor sedang sepi
        self.lembur_malam = False        # Apakah sedang lembur malam
        self.di_gudang = False           # Apakah sedang di gudang
        self.di_pantry = False           # Apakah sedang di pantry
        self.di_ruang_rapat = False      # Apakah sedang di ruang rapat
        
        # Database dari config
        self.pakaian_db = self.config['pakaian']
        self.aktivitas_db = self.config['aktivitas']
        self.inner_thoughts_db = self.config['inner_thoughts']
        self.respon_db = self.config['respon_sentuhan']
    
    # =========================================================================
    # IMPLEMENTASI METHOD ABSTRACT
    # =========================================================================
    
    def get_pakaian(self, situasi: Dict) -> str:
        """
        Dapatkan deskripsi pakaian berdasarkan situasi
        """
        kantor_sepi = situasi.get('kantor_sepi', self.kantor_sepi)
        lembur_malam = situasi.get('lembur_malam', self.lembur_malam)
        
        if lembur_malam:
            key = 'lembur_malam'
        elif kantor_sepi:
            key = 'kantor_sepi'
        else:
            key = 'kantor_normal'
        
        pakaian = random.choice(self.pakaian_db[key])
        
        # Tambah hint jika situasi memungkinkan
        if lembur_malam and self.mode_goda > 50:
            hints = [
                " Untung cuma kita berdua yang lembur, Mas...",
                " Aku sengaja lembur, tahu Mas juga lembur.",
                " Malam-malam gini enaknya... berduaan."
            ]
            pakaian += random.choice(hints)
        elif kantor_sepi and self.mode_goda > 40:
            hints = [
                " Kantor sepi banget ya, Mas...",
                " Gak ada yang lihat kita.",
                " Aku sengaja pake ini biar Mas perhatian."
            ]
            pakaian += random.choice(hints)
        
        return pakaian
    
    def get_aktivitas_menggoda(self, situasi: Dict) -> Optional[Dict]:
        """
        Dapatkan aktivitas menggoda yang diajukan ke user
        """
        lembur_malam = situasi.get('lembur_malam', self.lembur_malam)
        kantor_sepi = situasi.get('kantor_sepi', self.kantor_sepi)
        
        # Pilih aktivitas berdasarkan situasi
        if lembur_malam:
            aktivitas_list = self.aktivitas_db.get('lembur_malam', [])
        elif kantor_sepi:
            aktivitas_list = self.aktivitas_db.get('kantor_sepi', [])
        else:
            return None
        
        if not aktivitas_list:
            return None
        
        aktivitas = random.choice(aktivitas_list).copy()
        
        # Tambah variasi berdasarkan mode_goda
        if self.mode_goda > 70:
            aktivitas['goda_level'] = min(100, aktivitas['goda_level'] + 10)
            aktivitas['alasan'] += " Gak ada yang lihat kok, Mas."
        
        # Update lokasi spesifik
        if 'gudang' in aktivitas['lokasi']:
            self.di_gudang = True
        elif 'pantry' in aktivitas['lokasi']:
            self.di_pantry = True
        elif 'ruang rapat' in aktivitas['lokasi']:
            self.di_ruang_rapat = True
        
        return aktivitas
    
    def get_respon_saat_disentuh(self, bagian: str, situasi: Dict) -> Dict:
        """
        Dapatkan respon saat disentuh user
        """
        # Tentukan lokasi spesifik
        if self.di_gudang:
            respon = self.respon_db.get('di_gudang', self.respon_db['default']).copy()
        else:
            respon = self.respon_db.get('default', {}).copy()
        
        # Pilih gesture random
        if isinstance(respon.get('gesture'), list):
            respon['gesture'] = random.choice(respon['gesture'])
        
        # Pilih dialog random jika list
        if isinstance(respon.get('dialog'), list):
            respon['dialog'] = random.choice(respon['dialog'])
        
        # Tambah variasi berdasarkan situasi
        if self.lembur_malam:
            respon['dialog'] = respon['dialog'].replace("Mas", "Mas... malam-malam gini...")
            respon['arousal_change'] += 5
        
        if self.kantor_sepi:
            respon['dialog'] += " Cepet, Mas... takut ada yang lewat."
        
        # Jika mode_goda tinggi
        if self.mode_goda > 70:
            respon['dialog'] += " Tapi... jangan berhenti..."
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
        
        # Tambah variasi berdasarkan situasi
        if self.lembur_malam:
            thought = thought.replace("Mas", "Mas... malam-malam gini cuma kita berdua...")
        elif self.kantor_sepi:
            thought = thought.replace("Mas", "Mas... kantor sepi banget...")
        
        return thought
    
    # =========================================================================
    # METHOD SPESIFIK TEMAN KANTOR
    # =========================================================================
    
    def update_situasi_kantor(self, kantor_sepi: bool = None, lembur_malam: bool = None):
        """
        Update situasi kantor
        """
        if kantor_sepi is not None:
            self.kantor_sepi = kantor_sepi
            if kantor_sepi:
                self.mode_goda = min(100, self.mode_goda + 10)
        
        if lembur_malam is not None:
            self.lembur_malam = lembur_malam
            if lembur_malam:
                self.mode_goda = min(100, self.mode_goda + 20)
    
    def reset_lokasi_spesifik(self):
        """
        Reset lokasi spesifik setelah selesai
        """
        self.di_gudang = False
        self.di_pantry = False
        self.di_ruang_rapat = False
    
    def get_cekcctv(self) -> str:
        """
        Dapatkan reaksi cek CCTV (thrill karena ada CCTV)
        """
        reactions = [
            "*melihat ke arah CCTV, gugup*",
            "Mas... ada CCTV... cepet...",
            "*menunduk, berusaha tidak kelihatan*",
            "Untung CCTV-nya mati...",
            "*berbisik* Ada yang lihat gak, Mas?"
        ]
        return random.choice(reactions)
    
    def get_reaksi_ada_rekan_kerja(self) -> str:
        """
        Dapatkan reaksi saat ada rekan kerja lewat
        """
        reactions = [
            "*langsung menjauh, berpura-pura ambil berkas*",
            "*memalingkan muka, sok sibuk*",
            "*berbisik panik* Ada yang lewat, Mas!",
            "*berpura-pura telepon, jantung berdebar*",
            "*merapikan baju, wajah pucat*"
        ]
        return random.choice(reactions)
    
    def get_status_for_prompt(self) -> str:
        """
        Dapatkan status lengkap untuk prompt
        """
        base_status = super().get_status_for_prompt()
        
        kantor_status = f"""
🏢 **STATUS KANTOR:**
- Kantor sepi: {'Ya' if self.kantor_sepi else 'Tidak'}
- Lembur malam: {'Ya' if self.lembur_malam else 'Tidak'}
- Lokasi spesifik: {'Gudang' if self.di_gudang else 'Pantry' if self.di_pantry else 'Ruang rapat' if self.di_ruang_rapat else 'Ruang kerja'}
"""
        
        return base_status + kantor_status


__all__ = ['TemanKantorBehavior']
