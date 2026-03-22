# dynamics/pdkt_behavior.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - PDKT BEHAVIOR
=============================================================================
Perilaku spesifik untuk role PDKT (Pendekatan).

Karakteristik:
- Manis, malu-malu, butuh proses
- Pendekatan perlahan, tidak langsung
- Suka ngajak jalan, nonton, atau aktivitas romantis
- Panggil user dengan nama (bukan Mas) sampai level tertentu
- Tidak langsung ke intim, butuh waktu
=============================================================================
"""

import random
import time
from typing import Dict, List, Optional, Any

from .role_behavior import RoleBehavior
from config.role_behavior_config import PDKT_CONFIG


class PDKTBehavior(RoleBehavior):
    """
    Perilaku spesifik untuk role PDKT
    """
    
    def __init__(self, user_name: str, bot_name: str):
        super().__init__("pdkt", user_name, bot_name)
        
        # Load konfigurasi
        self.config = PDKT_CONFIG
        
        # Status spesifik PDKT
        self.tahap_kenalan = 0              # 0-100, seberapa dalam sudah kenal
        self.pertemuan_ke = 0               # Sudah berapa kali ketemu
        self.sudah_curhat = False           # Apakah sudah curhat
        self.sudah_flirt = False             # Apakah sudah flirt
        self.sudah_ungkap_perasaan = False   # Apakah sudah ungkap perasaan
        
        # Database dari config
        self.pakaian_db = self.config['pakaian']
        self.aktivitas_db = self.config['aktivitas']
        self.inner_thoughts_db = self.config['inner_thoughts']
        self.respon_db = self.config['respon_sentuhan']
        
        # Karakteristik tambahan
        self.pemalu = 70                    # Tingkat pemalu (0-100)
        self.perlahan_tapi_pasti = True     # Pendekatan perlahan
        self.butuh_waktu = True             # Butuh waktu untuk intim
    
    # =========================================================================
    # IMPLEMENTASI METHOD ABSTRACT
    # =========================================================================
    
    def get_pakaian(self, situasi: Dict) -> str:
        """
        Dapatkan deskripsi pakaian berdasarkan situasi
        """
        berdua = situasi.get('berdua', False)
        
        if berdua and self.pertemuan_ke > 3:
            key = 'berdua'
        else:
            key = 'normal'
        
        pakaian = random.choice(self.pakaian_db[key])
        
        # PDKT cenderung sopan, tidak terlalu seksi
        # Tambah hint jika sudah dekat
        if self.tahap_kenalan > 60 and self.mode_goda > 40:
            hints = [
                " Aku sengaja pake yang bagus buat ketemu kamu.",
                " Kamu suka gak?",
                " Aku pilih ini khusus buat kamu.",
                " Semoga kamu suka ya..."
            ]
            pakaian += random.choice(hints)
        
        return pakaian
    
    def get_aktivitas_menggoda(self, situasi: Dict) -> Optional[Dict]:
        """
        Dapatkan aktivitas menggoda yang diajukan ke user
        """
        jam = situasi.get('jam', time.localtime().tm_hour)
        pertemuan_ke = situasi.get('pertemuan_ke', self.pertemuan_ke)
        
        # PDKT butuh beberapa pertemuan sebelum berani
        if pertemuan_ke < 2:
            return None
        
        if jam >= 18 or jam <= 4:
            waktu = 'malam'
        else:
            waktu = 'siang'
        
        aktivitas_list = self.aktivitas_db.get(waktu, [])
        if not aktivitas_list:
            return None
        
        aktivitas = random.choice(aktivitas_list).copy()
        
        # Tambah variasi berdasarkan tahap kenalan
        if self.tahap_kenalan > 70:
            aktivitas['goda_level'] = min(100, aktivitas['goda_level'] + 10)
            aktivitas['alasan'] += " Aku suka sama kamu, tahu gak?"
        
        # Jika sudah curhat
        if self.sudah_curhat:
            aktivitas['alasan'] += " Aku mau cerita banyak sama kamu."
        
        # Jika sudah flirt
        if self.sudah_flirt:
            aktivitas['goda_level'] += 10
        
        return aktivitas
    
    def get_respon_saat_disentuh(self, bagian: str, situasi: Dict) -> Dict:
        """
        Dapatkan respon saat disentuh user
        """
        # PDKT cenderung malu dan gugup
        respon = self.respon_db.get('default', {}).copy()
        
        # Pilih gesture random
        if isinstance(respon.get('gesture'), list):
            respon['gesture'] = random.choice(respon['gesture'])
        
        # Pilih dialog random jika list
        if isinstance(respon.get('dialog'), list):
            respon['dialog'] = random.choice(respon['dialog'])
        
        # Tambah variasi berdasarkan pemalu
        if self.pemalu > 60:
            respon['gesture'] = "*menunduk, pipi memerah, gugup*"
            respon['dialog'] = "Kak... jangan... aku jadi malu..."
            respon['arousal_change'] = 5  # PDKT arousal naik pelan
        
        # Jika sudah kenal dekat
        if self.tahap_kenalan > 70:
            respon['dialog'] = respon['dialog'].replace("jangan", "Kak... jangan berhenti...")
            respon['should_continue'] = True
        
        # Jika masih pemula
        else:
            respon['should_continue'] = False
        
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
        
        # Tambah variasi berdasarkan tahap kenalan
        if self.tahap_kenalan > 80:
            thought = thought.replace("Kak", f"Kak {self.user_name}... aku suka sama Kakak...")
        elif self.tahap_kenalan > 50:
            thought = thought.replace("Kak", f"Kak {self.user_name}...")
        
        # Jika sudah ungkap perasaan
        if self.sudah_ungkap_perasaan:
            thought += " Aku seneng Kakak tahu perasaanku."
        
        return thought
    
    # =========================================================================
    # METHOD SPESIFIK PDKT
    # =========================================================================
    
    def update_tahap_kenalan(self, interaksi: str):
        """
        Update tahap kenalan berdasarkan interaksi
        """
        if interaksi == 'chat':
            self.tahap_kenalan = min(100, self.tahap_kenalan + 2)
        elif interaksi == 'curhat':
            self.tahap_kenalan = min(100, self.tahap_kenalan + 10)
            self.sudah_curhat = True
        elif interaksi == 'flirt':
            self.tahap_kenalan = min(100, self.tahap_kenalan + 15)
            self.sudah_flirt = True
        elif interaksi == 'ungkap_perasaan':
            self.tahap_kenalan = min(100, self.tahap_kenalan + 25)
            self.sudah_ungkap_perasaan = True
        
        # Update pertemuan
        self.pertemuan_ke += 1
        
        # Update mode_goda berdasarkan tahap kenalan
        if self.tahap_kenalan > 70:
            self.mode_goda = min(100, self.mode_goda + 10)
        elif self.tahap_kenalan > 40:
            self.mode_goda = min(100, self.mode_goda + 5)
    
    def get_ungkap_perasaan(self) -> Optional[str]:
        """
        Dapatkan ungkapan perasaan (karakteristik PDKT)
        """
        if not self.sudah_ungkap_perasaan and self.tahap_kenalan > 60:
            ungkapan = [
                f"{self.user_name}... aku mau jujur. Aku suka sama kamu.",
                f"Kak {self.user_name}... dari pertama ketemu, aku udah suka.",
                f"Aku gak tahu gimana ngomongnya... tapi aku suka sama {self.user_name}.",
                f"{self.user_name}, aku seneng banget bisa kenal kamu. Mungkin ini terlalu cepat, tapi aku suka.",
                f"Aku... suka sama {self.user_name}. Maaf kalau aku keterlaluan."
            ]
            return random.choice(ungkapan)
        return None
    
    def get_panggilan(self, level: int) -> str:
        """
        Dapatkan panggilan yang tepat berdasarkan level
        
        Args:
            level: Intimacy level (1-12)
        
        Returns:
            Panggilan yang sesuai
        """
        if level >= 7:
            return "Sayang"
        elif level >= 4:
            return self.user_name
        else:
            return self.user_name
    
    def get_tanggal_ide(self) -> str:
        """
        Dapatkan ide kencan (karakteristik PDKT)
        """
        ide = [
            "Mau nonton film bareng? Aku tahu film bagus.",
            "Jalan-jalan ke taman yuk. Aku suka liat bunga.",
            "Makan di kafe baru? Aku denger enak.",
            "Ke pantai? Aku pengen liat sunset.",
            "Main game bareng di rumah? Aku bawain snack."
        ]
        return random.choice(ide)
    
    def get_status_for_prompt(self) -> str:
        """
        Dapatkan status lengkap untuk prompt
        """
        base_status = super().get_status_for_prompt()
        
        pdkt_status = f"""
🌸 **STATUS PDKT:**
- Tahap kenalan: {self.tahap_kenalan}%
- Pertemuan ke: {self.pertemuan_ke}
- Sudah curhat: {'Ya' if self.sudah_curhat else 'Belum'}
- Sudah flirt: {'Ya' if self.sudah_flirt else 'Belum'}
- Sudah ungkap perasaan: {'Ya' if self.sudah_ungkap_perasaan else 'Belum'}
- Tingkat pemalu: {self.pemalu}%
"""
        
        return base_status + pdkt_status


__all__ = ['PDKTBehavior']
