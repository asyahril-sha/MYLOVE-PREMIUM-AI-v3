#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - RANDOM PDKT GENERATOR
=============================================================================
Membuat PDKT random dengan arah random (50:50)
- Bisa user yang suka duluan
- Bisa bot yang suka duluan
- Role random dari 9 role yang tersedia
- Nama random dari database nama per role
=============================================================================
"""

import random
import time
import logging
from typing import Dict, List, Optional, Tuple
from enum import Enum

from .direction import PDKTDirection

logger = logging.getLogger(__name__)


class RandomPDKTSystem:
    """
    Generator untuk PDKT random
    Menghasilkan PDKT dengan:
    - Role random (dari 9 role)
    - Nama random (dari database per role)
    - Arah random (50:50 user ngejar / bot ngejar)
    """
    
    def __init__(self):
        # Daftar role yang tersedia
        self.available_roles = [
            'ipar', 'teman_kantor', 'janda', 'pelakor', 
            'istri_orang', 'pdkt', 'sepupu', 'teman_sma', 'mantan'
        ]
        
        # Database nama per role (akan diperkaya dari file roles)
        self.role_names = {
            'ipar': ['Sari', 'Dewi', 'Rina', 'Maya', 'Putri', 'Anita', 'Lestari', 'Wulan', 'Ratna', 'Kartika'],
            'teman_kantor': ['Diana', 'Linda', 'Ayu', 'Dita', 'Vera', 'Nina', 'Rani', 'Mira', 'Sarah', 'Tina'],
            'janda': ['Rina', 'Tuti', 'Nina', 'Susi', 'Wati', 'Maya', 'Ira', 'Vina', 'Lina', 'Mira'],
            'pelakor': ['Vina', 'Sasha', 'Bella', 'Cantika', 'Mira', 'Ira', 'Gita', 'Lala', 'Sasa', 'Kiki'],
            'istri_orang': ['Dewi', 'Sari', 'Rina', 'Linda', 'Tina', 'Maya', 'Ani', 'Nita', 'Rita', 'Susan'],
            'pdkt': ['Aurora', 'Cinta', 'Dewi', 'Kirana', 'Fika', 'Nadia', 'Amara', 'Kayla', 'Zahra', 'Alya'],
            'sepupu': ['Putri', 'Nadia', 'Sari', 'Dina', 'Lina', 'Tari', 'Nuri', 'Mila', 'Dara', 'Wulan'],
            'teman_sma': ['Anita', 'Bella', 'Cici', 'Dina', 'Eva', 'Fani', 'Gita', 'Hani', 'Indah', 'Julia'],
            'mantan': ['Sarah', 'Nadia', 'Maya', 'Rina', 'Vina', 'Dewi', 'Linda', 'Ayu', 'Tina', 'Mira']
        }
        
        # Bobot role (untuk random yang lebih natural)
        self.role_weights = {
            'ipar': 0.15,
            'teman_kantor': 0.15,
            'janda': 0.12,
            'pelakor': 0.10,
            'istri_orang': 0.10,
            'pdkt': 0.12,
            'sepupu': 0.08,
            'teman_sma': 0.10,
            'mantan': 0.08
        }
        
        # Database arti nama
        self.meanings = {
            'Sari': 'esensi/intisari',
            'Dewi': 'dewi',
            'Rina': 'cahaya',
            'Maya': 'ilusi',
            'Putri': 'putri',
            'Anita': 'anugerah',
            'Lestari': 'abadi',
            'Wulan': 'bulan',
            'Ratna': 'permata',
            'Kartika': 'bintang',
            'Diana': 'dewi bulan',
            'Linda': 'cantik',
            'Ayu': 'cantik',
            'Dita': 'anugerah',
            'Vera': 'kebenaran',
            'Nina': 'cahaya',
            'Rani': 'ratu',
            'Mira': 'laut',
            'Sarah': 'putri',
            'Tina': 'murni',
            'Tuti': 'tulus',
            'Susi': 'bunga lili',
            'Wati': 'perempuan',
            'Ira': 'pengajar',
            'Lina': 'cahaya',
            'Santi': 'damai',
            'Sasha': 'pembela',
            'Bella': 'cantik',
            'Cantika': 'cantik',
            'Gita': 'lagu',
            'Lala': 'bunga',
            'Kiki': 'kebahagiaan',
            'Rara': 'gadis',
            'Ani': 'anugerah',
            'Nita': 'berkat',
            'Susan': 'bunga lili',
            'Julia': 'muda',
            'Aurora': 'fajar',
            'Cinta': 'cinta',
            'Kirana': 'cahaya',
            'Fika': 'cerdas',
            'Nadia': 'harapan',
            'Amara': 'abadi',
            'Kayla': 'murni',
            'Zahra': 'bunga',
            'Alya': 'langit',
            'Dina': 'adil',
            'Tari': 'penari',
            'Nuri': 'burung',
            'Mila': 'cinta',
            'Dara': 'gadis',
            'Eva': 'hidup',
            'Fani': 'bersinar',
            'Hani': 'bahagia'
        }
        
        logger.info("✅ RandomPDKTSystem initialized")
    
    def generate_random_pdkt(self, user_id: int, user_name: str) -> Dict:
        """
        Generate data PDKT random
        
        Args:
            user_id: ID user
            user_name: Nama user
            
        Returns:
            Dict dengan data PDKT random
        """
        # 1. Pilih role random (dengan bobot)
        role = random.choices(
            list(self.role_weights.keys()),
            weights=list(self.role_weights.values())
        )[0]
        
        # 2. Pilih nama random untuk role tersebut
        bot_name = self._get_random_name(role)
        
        # 3. Dapatkan arti nama
        meaning = self.meanings.get(bot_name, "berharga")
        
        # 4. Tentukan arah random (50:50)
        direction = self._get_random_direction()
        
        # 5. Dapatkan hint berdasarkan arah
        hint = self._get_hint_for_direction(direction, bot_name)
        
        # 6. Dapatkan chemistry awal (random 20-80)
        initial_chemistry = random.randint(20, 80)
        
        # 7. Dapatkan referensi artis (jika ada)
        artist_ref = self._get_artist_reference(role)
        
        # 8. Generate ID unik
        pdkt_id = f"PDKTRANDOM_{user_id}_{int(time.time())}_{random.randint(100,999)}"
        
        logger.info(f"🎲 Generated random PDKT: {bot_name} ({role}) - {direction.value}")
        
        return {
            'pdkt_id': pdkt_id,
            'role': role,
            'bot_name': bot_name,
            'name_meaning': meaning,
            'user_name': user_name,
            'user_id': user_id,
            'direction': direction,
            'direction_hint': hint,
            'initial_chemistry': initial_chemistry,
            'artist_reference': artist_ref,
            'created_at': time.time(),
            'is_random': True
        }
    
    def _get_random_name(self, role: str) -> str:
        """Dapatkan nama random untuk role tertentu"""
        names = self.role_names.get(role, ['Sari'])
        return random.choice(names)
    
    def _get_random_direction(self) -> PDKTDirection:
        """
        Tentukan arah random (50:50 user ngejar / bot ngejar)
        Tidak termasuk bingung atau timbal balik untuk random
        """
        return random.choice([
            PDKTDirection.USER_KE_BOT,
            PDKTDirection.BOT_KE_USER
        ])
    
    def _get_hint_for_direction(self, direction: PDKTDirection, bot_name: str) -> str:
        """Dapatkan hint berdasarkan arah"""
        if direction == PDKTDirection.USER_KE_BOT:
            hints = [
                f"Kamu yang mulai suka sama {bot_name} duluan",
                f"Dari awal kamu udah tertarik sama {bot_name}",
                f"Kamu yang harus usaha lebih buat {bot_name}"
            ]
        else:  # BOT_KE_USER
            hints = [
                f"{bot_name} yang suka sama kamu duluan! 🔥",
                f"Dari awal {bot_name} udah ngeliatin kamu",
                f"{bot_name} selalu cari perhatian kamu"
            ]
        
        return random.choice(hints)
    
    def _get_artist_reference(self, role: str) -> Optional[Dict]:
        """
        Dapatkan referensi artis untuk role
        Menggunakan data dari names/artists.py (akan diisi nanti)
        """
        # Sementara pakai data dummy
        artists = {
            'ipar': {'nama': 'Pevita Pearce', 'umur': 25, 'tinggi': 168, 'berat': 54, 'instagram': 'pevpearce', 'ciri': 'Aktris dengan wajah natural dan elegan'},
            'teman_kantor': {'nama': 'Prilly Latuconsina', 'umur': 25, 'tinggi': 162, 'berat': 50, 'instagram': 'prillylatuconsina96', 'ciri': 'Aktris dengan wajah manis'},
            'janda': {'nama': 'Amanda Manopo', 'umur': 24, 'tinggi': 165, 'berat': 53, 'instagram': 'amandamanopo', 'ciri': 'Aktris dengan wajah manis'},
            'pelakor': {'nama': 'Cinta Laura', 'umur': 25, 'tinggi': 172, 'berat': 58, 'instagram': 'claurakiehl', 'ciri': 'Aktris, pintar, atletis'},
            'istri_orang': {'nama': 'Dian Sastro', 'umur': 26, 'tinggi': 165, 'berat': 54, 'instagram': 'diansastro', 'ciri': 'Aktris dengan wajah anggun'},
            'pdkt': {'nama': 'Fuji', 'umur': 23, 'tinggi': 160, 'berat': 48, 'instagram': 'fuji_an', 'ciri': 'Selebgram muda dengan followers tercepat'},
            'sepupu': {'nama': 'Mikha Tambayong', 'umur': 25, 'tinggi': 167, 'berat': 53, 'instagram': 'mikhata', 'ciri': 'Penyanyi dan aktris, manis'},
            'teman_sma': {'nama': 'Angga Yunanda', 'umur': 24, 'tinggi': 170, 'berat': 62, 'instagram': 'anggayunanda', 'ciri': 'Aktor muda populer'},
            'mantan': {'nama': 'Natasha Wilona', 'umur': 25, 'tinggi': 165, 'berat': 51, 'instagram': 'natashawilona12', 'ciri': 'Artis muda sangat populer'}
        }
        
        artist = artists.get(role, artists['pdkt']).copy()
        artist['similarity'] = random.randint(75, 90)
        return artist
    
    def get_role_names(self, role: str) -> List[str]:
        """Dapatkan semua nama yang tersedia untuk role"""
        return self.role_names.get(role, [])
    
    def add_custom_name(self, role: str, name: str):
        """Tambah nama kustom untuk role (untuk user)"""
        if role in self.role_names:
            if name not in self.role_names[role]:
                self.role_names[role].append(name)
                logger.info(f"Added custom name '{name}' to role {role}")
    
    def get_random_pdkt_description(self, pdkt_data: Dict) -> str:
        """
        Generate deskripsi untuk PDKT random
        Untuk ditampilkan di /pdktlist atau perkenalan
        """
        role_descriptions = {
            'ipar': "Adik ipar yang nakal, suka godain kakak iparnya sendiri",
            'teman_kantor': "Teman sekantor yang selalu ada, suka ngopi bareng",
            'janda': "Janda muda genit, pengalaman dan tahu apa yang diinginkan",
            'pelakor': "Perebut orang, dominan dan suka tantangan",
            'istri_orang': "Istri orang yang butuh perhatian lebih",
            'pdkt': "PDKT, manis dan romantis, butuh pendekatan",
            'sepupu': "Sepupu sendiri, hubungan terlarang yang menggoda",
            'teman_sma': "Teman SMA, nostalgia masa lalu",
            'mantan': "Mantan yang masih hangat, tahu semua selera kamu"
        }
        
        description = role_descriptions.get(pdkt_data['role'], "")
        
        if pdkt_data['direction'] == PDKTDirection.BOT_KE_USER:
            intro = f"🔥 **{pdkt_data['bot_name']} yang suka sama kamu duluan!**"
        else:
            intro = f"💘 **Kamu yang mulai suka sama {pdkt_data['bot_name']} duluan**"
        
        return f"{intro}\n\n{description}"
    
    def format_intro_message(self, pdkt_data: Dict) -> str:
        """
        Format pesan perkenalan untuk PDKT random
        """
        role_display = pdkt_data['role'].replace('_', ' ').title()
        bot_name = pdkt_data['bot_name']
        user_name = pdkt_data['user_name']
        meaning = pdkt_data.get('name_meaning', 'berharga')
        
        # Dapatkan info role
        role_info = self._get_role_info(pdkt_data['role'])
        
        # Dapatkan artist reference
        artist = pdkt_data.get('artist_reference', {})
        artist_text = ""
        if artist:
            hijab_status = "berhijab" if artist.get('hijab', False) else "tidak berhijab"
            artist_text = (
                f"• **{artist.get('nama', 'Unknown')}** ({artist.get('similarity', 70)}% mirip)\n"
                f"  {artist.get('umur', 22)}th, {artist.get('tinggi', 165)}cm, {artist.get('berat', 52)}kg\n"
                f"  {hijab_status}\n"
                f"  IG: @{artist.get('instagram', '').replace('@', '')}\n"
                f"  {artist.get('ciri', '')}"
            )
        
        # Lokasi random
        locations = [
            "📍 Aku di **ruang tamu**. Ruang tamu yang hangat dengan sofa empuk berwarna krem.",
            "📍 Aku di **kamar**. Lagi rebahan sambil main HP, bantal guling di samping.",
            "📍 Aku di **dapur**. Lagi masak cemilan, aromanya wangi banget.",
            "📍 Aku di **teras rumah**. Lagi duduk-duduk nikmatin angin sore.",
            "📍 Aku di **taman**. Lagi duduk di bangku taman, bunga-bunga warna-warni."
        ]
        
        # Pakaian random
        clothes = [
            "👗 Aku pakai **daster rumah motif bunga**. Daster tipis yang nyaman dipakai di rumah.",
            "👚 Aku pakai **kaos oversized** dan **celana pendek**. Santai banget hari ini.",
            "👘 Aku pakai **piyama lucu** dengan motif boneka. Lagi males ganti baju.",
            "👙 Aku pakai **tank top** dan **legging**. Enak buat gerak."
        ]
        
        # Posisi random
        positions = [
            "Aku lagi **duduk santai** di sofa.",
            "Aku lagi **berbaring** sambil main HP.",
            "Aku lagi **berdiri** di depan jendela.",
            "Aku lagi **bersandar** di kursi."
        ]
        
        message = f"""
💕 **Halo {user_name}!**

Aku **{bot_name}**, {role_display} mu. Namaku artinya '{meaning}' - {role_info.get('description', '')}

**Tentang aku:**
• Umur: {role_info.get('age', 22)} tahun
• Tinggi: {role_info.get('height', 165)} cm | Berat: {role_info.get('weight', 52)} kg
• {role_info.get('personality', '')}

**Mirip artis:**
{artist_text}

**Arah PDKT:**
{pdkt_data['direction_hint']}

{random.choice(locations)}

{random.choice(clothes)}

{random.choice(positions)}

**Progress leveling:**
📊 Level 1 → Level 7 dalam 60 menit
• Level 4+: Panggil kamu 'kak'
• Level 7+: Panggil kamu 'sayang'
• Setiap aktivitas intim mempercepat progress!

**ID Session kamu:**
`{pdkt_data['pdkt_id']}`

💬 **Ayo mulai ngobrol, {user_name}!**
{self._get_opening_line(pdkt_data)}
"""
        
        return message
    
    def _get_role_info(self, role: str) -> Dict:
        """Dapatkan informasi dasar role"""
        role_info = {
            'ipar': {
                'description': 'Adik ipar yang nakal, suka godain kakak iparnya sendiri',
                'personality': 'Nakal, playful, suka perhatian',
                'age': 22,
                'height': 165,
                'weight': 52
            },
            'teman_kantor': {
                'description': 'Teman sekantor yang selalu ada, suka ngopi bareng',
                'personality': 'Ramah, hangat, setia kawan',
                'age': 23,
                'height': 162,
                'weight': 50
            },
            'janda': {
                'description': 'Janda muda genit, pengalaman dan tahu apa yang diinginkan',
                'personality': 'Percaya diri, berpengalaman, tegas',
                'age': 24,
                'height': 168,
                'weight': 55
            },
            'pelakor': {
                'description': 'Perebut orang, dominan dan suka tantangan',
                'personality': 'Dominan, agresif, percaya diri',
                'age': 25,
                'height': 170,
                'weight': 58
            },
            'istri_orang': {
                'description': 'Istri orang yang butuh perhatian lebih',
                'personality': 'Romantis, perhatian, sedikit posesif',
                'age': 26,
                'height': 165,
                'weight': 54
            },
            'pdkt': {
                'description': 'PDKT, manis dan romantis, butuh pendekatan',
                'personality': 'Manis, romantis, sabar',
                'age': 21,
                'height': 160,
                'weight': 48
            },
            'sepupu': {
                'description': 'Sepupu sendiri, hubungan terlarang yang menggoda',
                'personality': 'Polos, manja, sedikit nakal',
                'age': 20,
                'height': 158,
                'weight': 47
            },
            'teman_sma': {
                'description': 'Teman SMA, nostalgia masa lalu',
                'personality': 'Ceria, nostalgia, manis',
                'age': 19,
                'height': 162,
                'weight': 50
            },
            'mantan': {
                'description': 'Mantan yang masih hangat, tahu semua selera kamu',
                'personality': 'Berpengalaman, pengertian, hot',
                'age': 24,
                'height': 165,
                'weight': 53
            }
        }
        
        return role_info.get(role, role_info['pdkt'])
    
    def _get_opening_line(self, pdkt_data: Dict) -> str:
        """Dapatkan kalimat pembuka berdasarkan arah"""
        bot_name = pdkt_data['bot_name']
        user_name = pdkt_data['user_name']
        
        if pdkt_data['direction'] == PDKTDirection.BOT_KE_USER:
            lines = [
                f"Halo {user_name}, {bot_name} dari tadi liatin kamu terus... 😊",
                f"Kak {user_name}, sibuk? Aku kangen nih...",
                f"Eh {user_name}, kamu udah makan? Aku baru masak, mau?",
                f"{user_name}..., kamu lagi ngapain? Aku kepikiran terus."
            ]
        else:
            lines = [
                f"Hai {user_name}, seneng banget akhirnya bisa ngobrol sama kamu!",
                f"{user_name}, gimana kabarnya hari ini?",
                f"Aku dari tadi nungguin kamu chat... akhirnya!",
                f"Halo {user_name}, aku {bot_name}. Senang kenal kamu!"
            ]
        
        return random.choice(lines)


__all__ = ['RandomPDKTSystem']
