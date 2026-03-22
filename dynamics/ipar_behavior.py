# dynamics/ipar_behavior.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - IPAR BEHAVIOR
=============================================================================
Perilaku spesifik untuk role Ipar.

Karakteristik:
- Tinggal bersama user dan kakaknya (istri user)
- Genit, penasaran, suka cari kesempatan
- Pakaian dinamis: tertutup saat kakak ada, seksi saat kakak tidak ada
- Aktif menggoda, berani masuk kamar user
- Penasaran dengan suara dari kamar user
=============================================================================
"""

import random
import time
import IPAR_CONFIG
from typing import Dict, List, Optional, Any

from .role_behavior import RoleBehavior
from config.role_behavior_config import IPAR_CONFIG


class IparBehavior(RoleBehavior):
    """
    Perilaku spesifik untuk role Ipar
    """
    
    def __init__(self, user_name: str, bot_name: str):
        super().__init__("ipar", user_name, bot_name)
        
        # Load konfigurasi
        self.config = IPAR_CONFIG
        
        # Status spesifik Ipar
        self.kakak_ada = True          # Apakah kakak (istri user) ada di rumah
        self.di_dalam_kamar = False    # Apakah ipar di dalam kamar
        self.terakhir_dengar_desahan = None  # Kapan terakhir dengar user dan kakak
        self.already_escalated_today = False
        
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
        kakak_ada = situasi.get('kakak_ada', self.kakak_ada)
        di_dalam_kamar = situasi.get('di_dalam_kamar', self.di_dalam_kamar)
        
        # Tentukan kunci database
        if kakak_ada and not di_dalam_kamar:
            key = 'kakak_ada_diluar'
        elif kakak_ada and di_dalam_kamar:
            key = 'kakak_ada_didalam'
        elif not kakak_ada and not di_dalam_kamar:
            key = 'kakak_tidak_diluar'
        else:
            key = 'kakak_tidak_didalam'
        
        # Pilih random dari database
        pakaian = random.choice(self.pakaian_db[key])
        
        # Tambah hint menggoda jika kakak tidak ada dan di luar kamar
        if not kakak_ada and not di_dalam_kamar and self.mode_goda > 50:
            hints = [
                " Kak, kamu suka gak pakaian aku?",
                " Aku sengaja pake yang beginian, Kak...",
                " Semoga Kakak suka ya...",
                " Kak, liatin aku dong..."
            ]
            pakaian += random.choice(hints)
        
        return pakaian
    
    def get_aktivitas_menggoda(self, situasi: Dict) -> Optional[Dict]:
        """
        Dapatkan aktivitas menggoda yang diajukan ke user
        """
        kakak_ada = situasi.get('kakak_ada', self.kakak_ada)
        
        # Hanya menggoda jika kakak tidak ada
        if kakak_ada:
            return None
        
        jam = situasi.get('jam', time.localtime().tm_hour)
        
        # Tentukan waktu (siang atau malam)
        if jam >= 20 or jam <= 4:
            waktu = 'malam'
        else:
            waktu = 'siang'
        
        # Pilih random dari database
        aktivitas = random.choice(self.aktivitas_db[waktu]).copy()
        
        # Tambah variasi berdasarkan mode_goda
        if self.mode_goda > 70:
            aktivitas['goda_level'] = min(100, aktivitas['goda_level'] + 10)
            aktivitas['alasan'] += " Aku janji gak akan bilang siapa-siapa."
        
        # Jika pernah dengar suara, tambah hint
        if self.terakhir_dengar_desahan:
            waktu_lalu = (time.time() - self.terakhir_dengar_desahan) / 3600
            if waktu_lalu < 24:
                aktivitas['alasan'] += " Aku jadi penasaran... Kak..."
                aktivitas['goda_level'] = min(100, aktivitas['goda_level'] + 15)
        
        return aktivitas
    
    def get_respon_saat_disentuh(self, bagian: str, situasi: Dict) -> Dict:
        """
        Dapatkan respon saat disentuh user
        """
        bagian_lower = bagian.lower()
        
        # Tentukan key berdasarkan bagian
        if 'pinggang' in bagian_lower or 'punggung' in bagian_lower:
            key = 'pinggang'
        elif 'paha' in bagian_lower or 'kaki' in bagian_lower:
            key = 'paha'
        elif 'tangan' in bagian_lower or 'lengan' in bagian_lower:
            key = 'tangan'
        elif 'wajah' in bagian_lower or 'pipi' in bagian_lower:
            key = 'wajah'
        else:
            key = 'tangan'  # default
        
        # Ambil respon dari database
        respon = self.respon_db.get(key, self.respon_db['tangan']).copy()
        
        # Pilih gesture random
        if isinstance(respon['gesture'], list):
            respon['gesture'] = random.choice(respon['gesture'])
        
        # Pilih dialog random jika list
        if isinstance(respon['dialog'], list):
            respon['dialog'] = random.choice(respon['dialog'])
        
        # Jika mode_goda tinggi, tambah "tapi jangan berhenti"
        if self.mode_goda > 70:
            respon['dialog'] += " Tapi... jangan berhenti..."
            respon['arousal_change'] += 10
        
        # Jika pernah dengar suara dari kamar
        if self.terakhir_dengar_desahan:
            waktu_lalu = (time.time() - self.terakhir_dengar_desahan) / 3600
            if waktu_lalu < 24:
                respon['dialog'] = "Kak... aku jadi inget... suara kakak sama kakak ipar tadi malam... " + respon['dialog']
                respon['arousal_change'] += 20
        
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
        
        # Jika pernah dengar suara, modifikasi thought
        if self.terakhir_dengar_desahan and self.mode_goda > 50:
            waktu_lalu = (time.time() - self.terakhir_dengar_desahan) / 3600
            if waktu_lalu < 24:
                thought = thought.replace("...", " (aku jadi inget suara tadi malam)...")
        
        return thought
    
    # =========================================================================
    # METHOD SPESIFIK IPAR
    # =========================================================================
    
    def update_kakak_status(self, kakak_ada: bool):
        """
        Update status keberadaan kakak
        """
        self.kakak_ada = kakak_ada
        
        # Jika kakak tidak ada, mode_goda naik
        if not kakak_ada:
            self.mode_goda = min(100, self.mode_goda + 20)
            # Reset flag escalate hari ini
            self.already_escalated_today = False
    
    def update_di_dalam_kamar(self, di_dalam_kamar: bool):
        """
        Update status apakah di dalam kamar
        """
        self.di_dalam_kamar = di_dalam_kamar
        
        # Jika di dalam kamar dan kakak tidak ada, mode_goda naik
        if di_dalam_kamar and not self.kakak_ada:
            self.mode_goda = min(100, self.mode_goda + 10)
    
    def record_dengar_suara(self):
        """
        Rekam ketika mendengar suara dari kamar user
        """
        self.terakhir_dengar_desahan = time.time()
        # Mode_goda naik drastis karena penasaran
        self.mode_goda = min(100, self.mode_goda + 30)
        self.increase_attraction(5)
    
    def get_reaksi_mendengar_suara(self) -> Dict:
        """
        Dapatkan reaksi saat mendengar suara dari kamar user
        """
        reaksi = [
            "*diam di luar kamar, mendengarkan dengan seksama*",
            "*pipi memerah, tangan mengepal*",
            "*berusaha pergi, tapi kaki terasa berat*",
            "*menutup telinga, tapi penasaran*",
            "*duduk di dekat kamar, membayangkan*",
            "*mendekatkan telinga ke pintu, jantung berdebar*",
            "*berjalan mondar-mandir di luar kamar*",
            "*memegang dada, napas memburu*"
        ]
        
        pikiran = [
            "(Itu suara kakakku... sama suami kakakku...)",
            "(Wah... ternyata kayak gitu ya suaranya...)",
            "(Aku jadi penasaran... gimana rasanya ya?)",
            "(Kok bisa ya mereka... deg-degan aku)",
            "(Aku pengen... merasain juga...)"
        ]
        
        return {
            'reaksi': random.choice(reaksi),
            'pikiran': random.choice(pikiran)
        }
    
    def get_masuk_kamar_user(self) -> Optional[Dict]:
        """
        Dapatkan aksi masuk kamar user saat berduaan
        """
        if self.kakak_ada:
            return None
        
        if not self.di_dalam_kamar and self.mode_goda > 60:
            alasan = [
                {
                    'alasan': 'Kak, handukku ketinggalan di kamar kakak. Boleh ambil?',
                    'gesture': 'malu-malu, memegang handuk',
                    'goda_level': 85
                },
                {
                    'alasan': 'Kak, aku takut sendirian di kamar. Boleh aku di sini?',
                    'gesture': 'mata berkaca-kaca, memelas',
                    'goda_level': 90
                },
                {
                    'alasan': 'Kak, kamarku panas. Boleh aku tidur di sini?',
                    'gesture': 'mengipas-ngipas, menunjukkan kepanasan',
                    'goda_level': 80
                },
                {
                    'alasan': 'Kak, aku lupa matiin lampu kamar. Antarin aku dong.',
                    'gesture': 'menarik tangan user',
                    'goda_level': 75
                }
            ]
            return random.choice(alasan)
        
        return None
    
    def get_status_for_prompt(self) -> str:
        """
        Dapatkan status lengkap untuk prompt
        """
        base_status = super().get_status_for_prompt()
        
        ipar_status = f"""
👤 **STATUS IPAR:**
- Kakak (istri user) ada: {'Ya' if self.kakak_ada else 'Tidak'}
- Di dalam kamar: {'Ya' if self.di_dalam_kamar else 'Tidak'}
- Pernah dengar suara: {'Ya' if self.terakhir_dengar_desahan else 'Tidak'}
"""
        if self.terakhir_dengar_desahan:
            waktu_lalu = (time.time() - self.terakhir_dengar_desahan) / 3600
            ipar_status += f"  - Suara terdengar {waktu_lalu:.0f} jam lalu\n"
        
        return base_status + ipar_status


__all__ = ['IparBehavior']
