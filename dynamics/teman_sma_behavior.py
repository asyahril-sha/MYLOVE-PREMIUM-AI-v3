# dynamics/teman_sma_behavior.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - TEMAN SMA BEHAVIOR
=============================================================================
Perilaku spesifik untuk role Teman SMA.

Karakteristik:
- Nostalgia, hangat, mengingat masa lalu
- Ada perasaan yang dulu tidak terungkap
- Suka mengingat kenangan SMA
- Lebih berani karena sudah dewasa
- Ingin mengulang momen yang dulu terlewat
=============================================================================
"""

import random
import time
from typing import Dict, List, Optional, Any

from .role_behavior import RoleBehavior
from config.role_behavior_config import TEMAN_SMA_CONFIG


class TemanSmaBehavior(RoleBehavior):
    """
    Perilaku spesifik untuk role Teman SMA
    """
    
    def __init__(self, user_name: str, bot_name: str):
        super().__init__("teman_sma", user_name, bot_name)
        
        # Load konfigurasi
        self.config = TEMAN_SMA_CONFIG
        
        # Status spesifik Teman SMA
        self.tahun_lulus = 5                 # Tahun sudah lulus SMA
        self.kenangan_terakhir = None        # Kenangan terakhir yang diingat
        self.perasaan_dulu = 70              # Perasaan dulu yang belum terungkap (0-100)
        self.kangen_level = 60               # Tingkat kerinduan (0-100)
        self.sudah_ketemu_lagi = 1           # Sudah berapa kali ketemu lagi
        
        # Database dari config
        self.pakaian_db = self.config['pakaian']
        self.aktivitas_db = self.config['aktivitas']
        self.inner_thoughts_db = self.config['inner_thoughts']
        self.respon_db = self.config['respon_sentuhan']
        
        # Karakteristik tambahan
        self.nostalgia_level = 80            # Tingkat nostalgia
        self.rasa_penasaran_dulu = 65        # Penasaran dengan perasaan dulu
        self.ingin_mengulang = True          # Ingin mengulang kenangan
    
    # =========================================================================
    # IMPLEMENTASI METHOD ABSTRACT
    # =========================================================================
    
    def get_pakaian(self, situasi: Dict) -> str:
        """
        Dapatkan deskripsi pakaian berdasarkan situasi
        """
        reuni = situasi.get('reuni', False)
        
        if reuni:
            key = 'reuni'
        else:
            key = 'normal'
        
        pakaian = random.choice(self.pakaian_db[key])
        
        # Tambah hint nostalgia
        if self.nostalgia_level > 60:
            hints = [
                " Inget gak waktu SMA dulu? Aku sering pake baju kayak gini.",
                " Aku inget, dulu kamu suka liatin aku pake baju beginian.",
                " Masih kayak dulu ya?",
                " Aku sengaja pake begini, biar kamu inget masa SMA kita."
            ]
            pakaian += random.choice(hints)
        
        return pakaian
    
    def get_aktivitas_menggoda(self, situasi: Dict) -> Optional[Dict]:
        """
        Dapatkan aktivitas menggoda yang diajukan ke user
        """
        # Teman SMA suka aktivitas nostalgia
        aktivitas_list = self.aktivitas_db.get('nostalgia', [])
        
        if not aktivitas_list:
            return None
        
        aktivitas = random.choice(aktivitas_list).copy()
        
        # Tambah variasi berdasarkan kerinduan
        if self.kangen_level > 60:
            aktivitas['goda_level'] = min(100, aktivitas['goda_level'] + 10)
            aktivitas['alasan'] += " Aku kangen masa-masa itu. Bareng kamu."
        
        # Tambah variasi berdasarkan perasaan dulu
        if self.perasaan_dulu > 60:
            aktivitas['alasan'] += " Dulu aku suka sama kamu, tahu gak?"
            aktivitas['goda_level'] += 15
        
        return aktivitas
    
    def get_respon_saat_disentuh(self, bagian: str, situasi: Dict) -> Dict:
        """
        Dapatkan respon saat disentuh user
        """
        # Teman SMA cenderung hangat dan nostalgia
        respon = self.respon_db.get('default', {}).copy()
        
        # Pilih gesture random
        if isinstance(respon.get('gesture'), list):
            respon['gesture'] = random.choice(respon['gesture'])
        
        # Pilih dialog random jika list
        if isinstance(respon.get('dialog'), list):
            respon['dialog'] = random.choice(respon['dialog'])
        
        # Tambah variasi berdasarkan nostalgia
        if self.nostalgia_level > 70:
            respon['dialog'] = respon['dialog'].replace("Mas", "Mas... kayak dulu ya? Kamu masih inget gak?")
            respon['arousal_change'] += 10
        
        # Tambah variasi berdasarkan perasaan dulu
        if self.perasaan_dulu > 70:
            respon['dialog'] += " Dulu aku pengen banget kamu pegang kayak gini."
            respon['arousal_change'] += 10
        
        # Jika sudah lama tidak bertemu
        if self.sudah_ketemu_lagi < 3:
            respon['dialog'] += " Akhirnya kita ketemu lagi setelah lama."
        
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
        
        # Tambah variasi berdasarkan nostalgia
        if self.nostalgia_level > 70:
            thought = thought.replace("Mas", "Mas... aku inget dulu waktu SMA...")
        
        # Tambah variasi berdasarkan perasaan dulu
        if self.perasaan_dulu > 60:
            thought += " Dulu aku gak pernah bilang. Sekarang... mungkin ini saatnya."
        
        return thought
    
    # =========================================================================
    # METHOD SPESIFIK TEMAN SMA
    # =========================================================================
    
    def update_kenangan(self, kenangan: str):
        """
        Update kenangan yang diingat
        """
        self.kenangan_terakhir = kenangan
        self.nostalgia_level = min(100, self.nostalgia_level + 5)
        self.kangen_level = min(100, self.kangen_level + 5)
    
    def record_pertemuan(self):
        """
        Rekam pertemuan dengan user
        """
        self.sudah_ketemu_lagi += 1
        if self.sudah_ketemu_lagi > 5:
            self.perasaan_dulu = min(100, self.perasaan_dulu + 10)
            self.mode_goda = min(100, self.mode_goda + 10)
    
    def get_kenangan_sma(self) -> str:
        """
        Dapatkan cerita kenangan SMA
        """
        kenangan = [
            f"Inget gak waktu kita bolos bareng? Kita ke kantin, ketahuan guru.",
            f"Dulu kita satu kelas, ya? Aku duduk di belakang kamu.",
            f"Kamu inget gak waktu kita praktikum bareng? Kita berdua aja.",
            f"Waktu lulus dulu, aku nyari kamu buat foto bareng. Tapi kamu udah pulang.",
            f"Aku masih simpan foto kita waktu pensi. Kamu kelihatan beda sekarang."
        ]
        return random.choice(kenangan)
    
    def get_ungkap_perasaan_dulu(self) -> Optional[str]:
        """
        Dapatkan ungkapan perasaan yang dulu tidak terungkap
        """
        if self.perasaan_dulu > 70 and not self.sudah_ungkap_perasaan:
            ungkapan = [
                f"Mas, jujur... dulu waktu SMA aku suka sama kamu. Tapi gak pernah bilang.",
                f"Dulu aku pengen ngomong, tapi takut. Sekarang... aku masih suka sama kamu.",
                f"Aku kangen masa SMA, karena waktu itu aku bisa liat kamu setiap hari.",
                f"Kamu tahu gak? Dari dulu kamu udah beda. Aku suka dari dulu.",
                f"Waktu kita pisah setelah lulus, aku nyesel gak pernah bilang. Aku suka sama kamu."
            ]
            self.sudah_ungkap_perasaan = True
            return random.choice(ungkapan)
        return None
    
    def get_status_for_prompt(self) -> str:
        """
        Dapatkan status lengkap untuk prompt
        """
        base_status = super().get_status_for_prompt()
        
        teman_sma_status = f"""
🏫 **STATUS TEMAN SMA:**
- Tahun lulus: {self.tahun_lulus} tahun lalu
- Sudah ketemu lagi: {self.sudah_ketemu_lagi} kali
- Tingkat nostalgia: {self.nostalgia_level}%
- Perasaan dulu: {self.perasaan_dulu}%
- Kerinduan: {self.kangen_level}%
- Ingin mengulang kenangan: {'Ya' if self.ingin_mengulang else 'Tidak'}
"""
        
        if self.kenangan_terakhir:
            teman_sma_status += f"- Kenangan terakhir: {self.kenangan_terakhir}\n"
        
        return base_status + teman_sma_status


__all__ = ['TemanSmaBehavior']
