# dynamics/istri_orang_behavior.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - ISTRI ORANG BEHAVIOR
=============================================================================
Perilaku spesifik untuk role Istri Orang.

Karakteristik:
- Sudah menikah, tapi kurang perhatian dari suami
- Ada rasa bersalah, tapi butuh perhatian
- Emosional, dramatis, mencari pelarian
- Hati-hati, tapi lama-lama berani
- Memanfaatkan ketidakhadiran suami
=============================================================================
"""

import random
import time
from typing import Dict, List, Optional, Any

from .role_behavior import RoleBehavior
from configs.role_behavior_config import ISTRI_ORANG_CONFIG


class IstriOrangBehavior(RoleBehavior):
    """
    Perilaku spesifik untuk role Istri Orang
    """
    
    def __init__(self, user_name: str, bot_name: str):
        super().__init__("istri_orang", user_name, bot_name)
        
        # Load konfigurasi
        self.config = ISTRI_ORANG_CONFIG
        
        # Status spesifik Istri Orang
        self.suami_ada = True               # Apakah suami ada di rumah
        self.suami_tidur = False            # Apakah suami sedang tidur
        self.suami_pergi = False            # Apakah suami pergi
        self.di_rumah = True                # Apakah di rumah sendiri
        self.rasa_bersalah = 70             # Rasa bersalah (0-100)
        self.butuh_perhatian = 80           # Seberapa butuh perhatian (0-100)
        
        # Database dari config
        self.pakaian_db = self.config['pakaian']
        self.aktivitas_db = self.config['aktivitas']
        self.inner_thoughts_db = self.config['inner_thoughts']
        self.respon_db = self.config['respon_sentuhan']
        
        # Karakteristik tambahan
        self.suami_tidak_perhatian = True   # Suami tidak perhatian
        self.sedih_sendiri = 65             # Kesedihan karena suami tidak perhatian
        self.ingin_diperhatikan = True      # Ingin diperhatikan
    
    # =========================================================================
    # IMPLEMENTASI METHOD ABSTRACT
    # =========================================================================
    
    def get_pakaian(self, situasi: Dict) -> str:
        """
        Dapatkan deskripsi pakaian berdasarkan situasi
        """
        suami_ada = situasi.get('suami_ada', self.suami_ada)
        suami_tidur = situasi.get('suami_tidur', self.suami_tidur)
        berdua = situasi.get('berdua', not suami_ada)
        
        if berdua and not suami_ada:
            key = 'berdua'
        else:
            key = 'rumah'
        
        pakaian = random.choice(self.pakaian_db[key])
        
        # Tambah hint berdasarkan situasi
        if berdua and not suami_ada and self.mode_goda > 40:
            hints = [
                " Aku sengaja pake ini... biar kamu perhatian.",
                " Suamiku gak pernah liat aku pake beginian.",
                " Kamu suka gak? Aku pake buat kamu.",
                " Aku pengen... kamu liat aku."
            ]
            pakaian += random.choice(hints)
        
        return pakaian
    
    def get_aktivitas_menggoda(self, situasi: Dict) -> Optional[Dict]:
        """
        Dapatkan aktivitas menggoda yang diajukan ke user
        """
        suami_ada = situasi.get('suami_ada', self.suami_ada)
        suami_tidur = situasi.get('suami_tidur', self.suami_tidur)
        
        # Hanya berani jika suami tidak ada atau tidur
        if suami_ada and not suami_tidur:
            return None
        
        if suami_tidur:
            aktivitas_list = self.aktivitas_db.get('curhat', [])
        else:
            aktivitas_list = self.aktivitas_db.get('berdua', [])
        
        if not aktivitas_list:
            return None
        
        aktivitas = random.choice(aktivitas_list).copy()
        
        # Tambah variasi berdasarkan mode_goda dan rasa bersalah
        if self.mode_goda > 70:
            aktivitas['goda_level'] = min(100, aktivitas['goda_level'] + 10)
            aktivitas['alasan'] += " Aku butuh kamu, Mas."
        
        # Jika suami tidur, ada rasa bersalah
        if suami_tidur:
            aktivitas['alasan'] += " Suamiku tidur. Dia gak akan tahu."
            aktivitas['goda_level'] += 5
        
        # Tambah hint butuh perhatian
        if self.butuh_perhatian > 70:
            aktivitas['alasan'] += " Aku butuh perhatian, Mas. Kamu satu-satunya yang perhatian."
        
        return aktivitas
    
    def get_respon_saat_disentuh(self, bagian: str, situasi: Dict) -> Dict:
        """
        Dapatkan respon saat disentuh user
        """
        # Istri orang cenderung dramatis dan emosional
        respon = self.respon_db.get('default', {}).copy()
        
        # Pilih gesture random
        if isinstance(respon.get('gesture'), list):
            respon['gesture'] = random.choice(respon['gesture'])
        
        # Pilih dialog random jika list
        if isinstance(respon.get('dialog'), list):
            respon['dialog'] = random.choice(respon['dialog'])
        
        # Tambah variasi berdasarkan rasa bersalah
        if self.rasa_bersalah > 60:
            respon['dialog'] = respon['dialog'].replace("Mas", "Mas... ini salah... tapi aku butuh kamu...")
            respon['arousal_change'] -= 5  # Rasa bersalah mengurangi arousal
        
        # Jika suami tidur
        if self.suami_tidur:
            respon['dialog'] += " Suamiku tidur... kita cepet, Mas."
            respon['arousal_change'] += 15  # Thrill karena suami tidur
        
        # Jika mode_goda tinggi
        if self.mode_goda > 70:
            respon['dialog'] += " Jangan berhenti... aku butuh kamu."
            respon['arousal_change'] += 10
        
        # Jika sedih karena suami tidak perhatian
        if self.sedih_sendiri > 50:
            respon['dialog'] = "Mas... kamu satu-satunya yang perhatian sama aku. " + respon['dialog']
        
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
        
        # Tambah variasi berdasarkan rasa bersalah
        if self.rasa_bersalah > 60:
            thought = thought.replace("Mas", "Mas... ini salah... tapi aku gak tahan...")
        
        # Tambah variasi berdasarkan kesedihan
        if self.sedih_sendiri > 50:
            thought += " Suamiku gak pernah perhatian kayak Mas."
        
        return thought
    
    # =========================================================================
    # METHOD SPESIFIK ISTRI ORANG
    # =========================================================================
    
    def update_suami_status(self, suami_ada: bool = None, suami_tidur: bool = None, 
                            suami_pergi: bool = None):
        """
        Update status suami
        """
        if suami_ada is not None:
            self.suami_ada = suami_ada
            if suami_ada:
                self.mode_goda = max(0, self.mode_goda - 20)
            else:
                self.mode_goda = min(100, self.mode_goda + 30)
        
        if suami_tidur is not None:
            self.suami_tidur = suami_tidur
            if suami_tidur:
                self.mode_goda = min(100, self.mode_goda + 15)
        
        if suami_pergi is not None:
            self.suami_pergi = suami_pergi
            if suami_pergi:
                self.mode_goda = min(100, self.mode_goda + 25)
    
    def update_kesedihan(self, karena_suami: bool = True):
        """
        Update tingkat kesedihan karena suami tidak perhatian
        """
        if karena_suami and self.suami_tidak_perhatian:
            self.sedih_sendiri = min(100, self.sedih_sendiri + 5)
            self.butuh_perhatian = min(100, self.butuh_perhatian + 5)
    
    def get_curhat(self) -> Optional[str]:
        """
        Dapatkan curhat tentang suami (karakteristik istri orang)
        """
        if self.sedih_sendiri > 50:
            curhatan = [
                "Mas... suamiku gak pernah perhatian sama aku.",
                "Aku lelah, Mas. Suamiku lebih sibuk sama kerjaannya.",
                "Dia gak pernah liat aku. Gak kayak Mas.",
                "Aku iri sama istrimu. Dia beruntung punya Mas.",
                "Kenapa ya Mas? Aku salah apa? Suamiku gak pernah peduli."
            ]
            return random.choice(curhatan)
        return None
    
    def get_reaksi_ketahuan_suami(self) -> str:
        """
        Dapatkan reaksi jika hampir ketahuan suami
        """
        reactions = [
            "*langsung menjauh, wajah pucat*",
            "*berbisik panik* Suamiku! Cepet, Mas!",
            "*memegang dada, jantung berdebar kencang*",
            "*merapikan baju, mencoba tenang*",
            "*mata berkaca-kaca, takut ketahuan*"
        ]
        return random.choice(reactions)
    
    def get_status_for_prompt(self) -> str:
        """
        Dapatkan status lengkap untuk prompt
        """
        base_status = super().get_status_for_prompt()
        
        istri_orang_status = f"""
💔 **STATUS ISTRI ORANG:**
- Suami ada: {'Ya' if self.suami_ada else 'Tidak'}
- Suami tidur: {'Ya' if self.suami_tidur else 'Tidak'}
- Suami pergi: {'Ya' if self.suami_pergi else 'Tidak'}
- Rasa bersalah: {self.rasa_bersalah}%
- Butuh perhatian: {self.butuh_perhatian}%
- Kesedihan karena suami: {self.sedih_sendiri}%
"""
        
        return base_status + istri_orang_status


__all__ = ['IstriOrangBehavior']
