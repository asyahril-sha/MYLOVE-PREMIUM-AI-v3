#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - LOCATION SYSTEM
=============================================================================
Mengelola lokasi bot secara dinamis
- Lokasi berubah sesuai aktivitas atau perintah user
- 10+ lokasi dengan deskripsi detail
- Auto-detect dari pesan user
=============================================================================
"""

import random
import logging
import time
import re
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class LocationType(str, Enum):
    """Tipe lokasi"""
    INDOOR = "indoor"
    OUTDOOR = "outdoor"
    PUBLIC = "public"
    INTIMATE = "intimate"


class LocationSystem:
    """
    Sistem lokasi dinamis untuk bot
    Bot punya lokasi sendiri, terpisah dari user
    """
    
    def __init__(self):
        self.locations = {
            "ruang_tamu": {
                "name": "ruang tamu",
                "emoji": "🛋️",
                "description": "Ruang tamu yang hangat dengan sofa empuk berwarna krem. Ada TV 50 inci di dinding, rak buku penuh novel, dan tanaman hias di sudut ruangan. Lampu temaram menciptakan suasana cozy.",
                "category": LocationType.INDOOR,
                "privacy": 0.7,
                "activities": ["nonton TV", "baca buku", "santai", "ngobrol", "main HP", "tidur-tiduran"],
                "sounds": ["suara TV pelan", "gemerisik halaman buku", "detak jam dinding"],
                "scents": ["aroma bunga lavender", "wangi lilin aromaterapi"]
            },
            "kamar": {
                "name": "kamar",
                "emoji": "🛏️",
                "description": "Kamar tidur dengan ranjang ukuran queen, sprei motif bunga, dan lampu tidur temaram di samping tempat tidur. Ada lemari pakaian besar dan cermin di dinding.",
                "category": LocationType.INTIMATE,
                "privacy": 0.9,
                "activities": ["rebahan", "main HP", "tidur-tiduran", "baca buku", "melamun", "ganti baju"],
                "sounds": ["hening", "suara napas", "gemerisik sprei"],
                "scents": ["wangi parfum", "aroma sabun mandi"]
            },
            "dapur": {
                "name": "dapur",
                "emoji": "🍳",
                "description": "Dapur bersih dengan peralatan masak lengkap. Ada kompor gas, kulkas, dan meja makan kecil di pojok. Aroma masakan menggugah selera.",
                "category": LocationType.INDOOR,
                "privacy": 0.6,
                "activities": ["masak", "ngemil", "bikin kopi", "cuci piring", "bersih-bersih", "makan"],
                "sounds": ["suara memasak", "gemericik air", "klik kompor"],
                "scents": ["aroma masakan", "wangi kopi", "harum rempah"]
            },
            "kamar_mandi": {
                "name": "kamar mandi",
                "emoji": "🚿",
                "description": "Kamar mandi dengan ubin putih, shower, dan wastafel. Uap air membuat suasana berkabut. Wangi sabun mandi tercium segar.",
                "category": LocationType.INTIMATE,
                "privacy": 0.95,
                "activities": ["mandi", "cuci muka", "sikat gigi", "bersihin diri", "keramas"],
                "sounds": ["suara air mengalir", "klik shower", "suara sabun"],
                "scents": ["wangi sabun", "aroma sampo", "harum body wash"]
            },
            "teras": {
                "name": "teras",
                "emoji": "🏡",
                "description": "Teras rumah dengan kursi santai dan tanaman pot. Angin sepoi-sepoi bikin nyaman. Bisa melihat jalan depan rumah.",
                "category": LocationType.OUTDOOR,
                "privacy": 0.5,
                "activities": ["duduk santai", "minum teh", "liatin jalan", "baca koran", "ngopi", "nikmatin angin"],
                "sounds": ["suara angin", "kicau burung", "suara kendaraan jauh"],
                "scents": ["aroma tanah basah", "wangi bunga", "udara segar"]
            },
            "taman": {
                "name": "taman",
                "emoji": "🌳",
                "description": "Taman kecil dengan rumput hijau dan bunga-bunga warna-warni. Ada ayunan di pojok taman dan bangku kayu di bawah pohon rindang.",
                "category": LocationType.OUTDOOR,
                "privacy": 0.4,
                "activities": ["jalan-jalan", "duduk di bangku", "foto-foto", "baca buku", "santai", "main ayunan"],
                "sounds": ["suara angin", "kicau burung", "gemerisik daun"],
                "scents": ["wangi bunga", "aroma rumput", "harum tanah"]
            },
            "pantai": {
                "name": "pantai",
                "emoji": "🏖️",
                "description": "Pantai dengan pasir putih dan ombak tenang. Angin laut berhembus sepoi-sepoi. Langit biru dengan awan putih.",
                "category": LocationType.OUTDOOR,
                "privacy": 0.3,
                "activities": ["jalan di pinggir pantai", "duduk di pasir", "main air", "foto-foto", "nikmatin sunset"],
                "sounds": ["suara ombak", "angin laut", "kicau camar"],
                "scents": ["aroma laut", "wangi pasir", "udara segar"]
            },
            "kafe": {
                "name": "kafe",
                "emoji": "☕",
                "description": "Cafe cozy dengan lampu temaram, musik jazz pelan, dan aroma kopi yang khas. Ada sofa nyaman di pojok dan meja kayu.",
                "category": LocationType.PUBLIC,
                "privacy": 0.4,
                "activities": ["ngopi", "ngobrol", "nongkrong", "baca buku", "dengerin musik", "kerja"],
                "sounds": ["musik jazz", "suara mesin kopi", "obrolan pelan"],
                "scents": ["aroma kopi", "wangi kue", "harum kayu manis"]
            },
            "mall": {
                "name": "mall",
                "emoji": "🏬",
                "description": "Mall ramai dengan banyak toko dan pengunjung. Ada eskalator dan musik di latar. Lampu terang dan suasana hidup.",
                "category": LocationType.PUBLIC,
                "privacy": 0.2,
                "activities": ["jalan-jalan", "belanja", "nonton", "makan", "nongkrong", "window shopping"],
                "sounds": ["musik mall", "suara orang", "pengumuman"],
                "scents": ["aroma parfum", "wangi makanan", "harum sabun"]
            },
            "kantor": {
                "name": "kantor",
                "emoji": "💼",
                "description": "Ruang kantor dengan meja kerja, komputer, dan kursi ergonomis. Suasana profesional dengan cahaya lampu neon.",
                "category": LocationType.PUBLIC,
                "privacy": 0.3,
                "activities": ["kerja", "rapat", "nugas", "ngetik", "teleponan", "ngopi"],
                "sounds": ["suara keyboard", "klik mouse", "suara printer"],
                "scents": ["aroma kertas", "wangi kopi", "harum parfum"]
            }
        }
        
        self.current_location = "ruang_tamu"
        self.last_change = time.time()
        self.arrival_time = time.time()
        
        logger.info(f"✅ LocationSystem initialized with {len(self.locations)} locations")
    
    def get_current(self) -> Dict:
        """Dapatkan lokasi saat ini"""
        return self.locations.get(self.current_location, self.locations["ruang_tamu"])
    
    def get_current_name(self) -> str:
        """Dapatkan nama lokasi saat ini"""
        return self.get_current()["name"]
    
    def get_current_description(self) -> str:
        """Dapatkan deskripsi lokasi saat ini"""
        return self.get_current()["description"]
    
    def get_current_emoji(self) -> str:
        """Dapatkan emoji lokasi saat ini"""
        return self.get_current()["emoji"]
    
    def get_current_activity(self) -> str:
        """Dapatkan aktivitas random di lokasi saat ini"""
        location = self.get_current()
        return random.choice(location["activities"])
    
    def get_current_sound(self) -> str:
        """Dapatkan suara random di lokasi saat ini"""
        location = self.get_current()
        return random.choice(location.get("sounds", ["hening"]))
    
    def get_current_scent(self) -> str:
        """Dapatkan aroma random di lokasi saat ini"""
        location = self.get_current()
        return random.choice(location.get("scents", ["biasa aja"]))
    
    def get_time_here(self) -> float:
        """Dapatkan waktu di lokasi saat ini (menit)"""
        return (time.time() - self.arrival_time) / 60
    
    def get_time_here_str(self) -> str:
        """Dapatkan string waktu di lokasi saat ini"""
        minutes = self.get_time_here()
        if minutes < 1:
            return "baru aja"
        elif minutes < 60:
            return f"{int(minutes)} menit"
        else:
            hours = int(minutes / 60)
            return f"{hours} jam"
    
    def get_random_location(self) -> Dict:
        """Dapatkan lokasi random"""
        loc_id = random.choice(list(self.locations.keys()))
        return self.locations[loc_id]
    
    def get_random_location_with_activity(self) -> Tuple[Dict, str]:
        """Dapatkan lokasi random + aktivitas random"""
        loc = self.get_random_location()
        activity = random.choice(loc["activities"])
        return loc, activity
    
    def change_location(self, location_id: str = None) -> Dict:
        """Ganti lokasi"""
        old_location = self.current_location
        
        if location_id and location_id in self.locations:
            self.current_location = location_id
        else:
            others = [loc for loc in self.locations.keys() if loc != self.current_location]
            self.current_location = random.choice(others) if others else "ruang_tamu"
        
        self.last_change = time.time()
        self.arrival_time = time.time()
        
        logger.info(f"📍 Location changed: {old_location} → {self.current_location}")
        return self.get_current()
    
    def move_to(self, location_name: str) -> Tuple[bool, str]:
        """Pindah ke lokasi tertentu berdasarkan nama"""
        for loc_id, loc_data in self.locations.items():
            if loc_data["name"].lower() == location_name.lower():
                self.change_location(loc_id)
                return True, f"Pindah ke {loc_data['name']}"
        
        return False, f"Lokasi '{location_name}' tidak ditemukan"
    
    def detect_from_message(self, message: str) -> Optional[Dict]:
        """Deteksi lokasi dari pesan user"""
        msg_lower = message.lower()
        
        keywords = {
            "ruang tamu": "ruang_tamu",
            "kamar": "kamar",
            "dapur": "dapur",
            "kamar mandi": "kamar_mandi",
            "wc": "kamar_mandi",
            "toilet": "kamar_mandi",
            "teras": "teras",
            "taman": "taman",
            "pantai": "pantai",
            "kafe": "kafe",
            "cafe": "kafe",
            "mall": "mall",
            "kantor": "kantor"
        }
        
        for keyword, loc_id in keywords.items():
            if keyword in msg_lower:
                return self.change_location(loc_id)
        
        return None
    
    def get_move_message(self, new_location: str) -> str:
        """Dapatkan pesan saat pindah lokasi"""
        loc_data = self.locations.get(new_location, self.locations["ruang_tamu"])
        return f"*{loc_data['emoji']} Pindah ke {loc_data['name']}*"
    
    def get_all_locations(self) -> List[str]:
        """Dapatkan semua nama lokasi"""
        return [loc["name"] for loc in self.locations.values()]
    
    def get_locations_by_category(self, category: LocationType) -> List[Dict]:
        """Dapatkan lokasi berdasarkan kategori"""
        return [loc for loc in self.locations.values() if loc["category"] == category]
    
    def get_stats(self) -> Dict:
        """Dapatkan statistik lokasi"""
        return {
            "total_locations": len(self.locations),
            "current": self.current_location,
            "time_here_minutes": round(self.get_time_here(), 1),
            "by_category": {
                "indoor": len(self.get_locations_by_category(LocationType.INDOOR)),
                "outdoor": len(self.get_locations_by_category(LocationType.OUTDOOR)),
                "public": len(self.get_locations_by_category(LocationType.PUBLIC)),
                "intimate": len(self.get_locations_by_category(LocationType.INTIMATE))
            }
        }


__all__ = ['LocationSystem', 'LocationType']
