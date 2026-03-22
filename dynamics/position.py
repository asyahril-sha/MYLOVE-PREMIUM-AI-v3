#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - POSITION SYSTEM
=============================================================================
Mengelola posisi tubuh bot
- Posisi berubah sesuai aktivitas
- 8+ posisi tubuh dengan deskripsi
- Random position untuk callback
=============================================================================
"""

import random
import logging
import time
from typing import Dict, List, Optional, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class PositionType(str, Enum):
    """Tipe posisi"""
    DUDUK = "duduk"
    BERDIRI = "berdiri"
    BERBARING = "berbaring"
    BERSANDAR = "bersandar"
    JONGKOK = "jongkok"
    MERANGKAK = "merangkak"
    MIRING = "miring"
    TELENTANG = "telentang"
    TELUNGKUP = "telungkup"
    DUDUK_SILA = "duduk_sila"


class PositionSystem:
    """
    Sistem posisi tubuh dinamis
    Bot punya posisi sendiri yang berubah natural
    """
    
    def __init__(self):
        self.positions = {
            "duduk": {
                "name": "duduk",
                "description": "duduk santai",
                "type": PositionType.DUDUK,
                "emoji": "🧘",
                "intimacy_allowed": True,
                "activities": ["ngobrol", "nonton TV", "baca buku", "main HP", "kerja", "ngopi", "melamun"]
            },
            "berdiri": {
                "name": "berdiri",
                "description": "berdiri tegak",
                "type": PositionType.BERDIRI,
                "emoji": "🧍",
                "intimacy_allowed": True,
                "activities": ["masak", "cuci piring", "siap-siap", "ngantri", "stretch", "foto", "ngobrol"]
            },
            "berbaring": {
                "name": "berbaring",
                "description": "berbaring",
                "type": PositionType.BERBARING,
                "emoji": "😴",
                "intimacy_allowed": True,
                "activities": ["tidur-tiduran", "rebahan", "istirahat", "baca buku", "main HP", "melamun", "nonton"]
            },
            "bersandar": {
                "name": "bersandar",
                "description": "bersandar di sofa/dinding",
                "type": PositionType.BERSANDAR,
                "emoji": "🛋️",
                "intimacy_allowed": True,
                "activities": ["santai", "ngobrol", "nunggu", "ngopi", "melamun", "dengerin musik", "baca"]
            },
            "jongkok": {
                "name": "jongkok",
                "description": "jongkok",
                "type": PositionType.JONGKOK,
                "emoji": "🏃",
                "intimacy_allowed": False,
                "activities": ["bersih-bersih", "main sama kucing", "foto", "ngambil barang", "berkebun", "stretch"]
            },
            "merangkak": {
                "name": "merangkak",
                "description": "merangkak",
                "type": PositionType.MERANGKAK,
                "emoji": "🐱",
                "intimacy_allowed": True,
                "activities": ["nyari barang", "main", "bersih-bersih", "beres-beres", "olahraga"]
            },
            "miring": {
                "name": "miring",
                "description": "berbaring miring",
                "type": PositionType.MIRING,
                "emoji": "💤",
                "intimacy_allowed": True,
                "activities": ["tidur", "rebahan", "nonton HP", "baca buku", "ngelamun", "pelukan"]
            },
            "telentang": {
                "name": "telentang",
                "description": "telentang",
                "type": PositionType.TELENTANG,
                "emoji": "⭐",
                "intimacy_allowed": True,
                "activities": ["tidur", "rebahan", "stretch", "meditasi", "tarik napas", "bintang"]
            },
            "telungkup": {
                "name": "telungkup",
                "description": "telungkup (tengkurap)",
                "type": PositionType.TELUNGKUP,
                "emoji": "😴",
                "intimacy_allowed": True,
                "activities": ["tidur", "baca buku", "main HP", "pijat", "relaksasi"]
            },
            "duduk_sila": {
                "name": "duduk bersila",
                "description": "duduk bersila",
                "type": PositionType.DUDUK_SILA,
                "emoji": "🧘‍♀️",
                "intimacy_allowed": True,
                "activities": ["meditasi", "ngobrol", "baca", "main HP", "yoga", "santai"]
            }
        }
        
        self.current_position = "duduk"
        self.last_change = time.time()
        
        logger.info(f"✅ PositionSystem initialized with {len(self.positions)} positions")
    
    def get_current(self) -> Dict:
        """Dapatkan posisi saat ini"""
        return self.positions.get(self.current_position, self.positions["duduk"])
    
    def get_current_name(self) -> str:
        """Dapatkan nama posisi saat ini"""
        return self.get_current()["name"]
    
    def get_current_description(self) -> str:
        """Dapatkan deskripsi posisi saat ini"""
        return self.get_current()["description"]
    
    def get_current_emoji(self) -> str:
        """Dapatkan emoji posisi saat ini"""
        return self.get_current()["emoji"]
    
    def get_current_type(self) -> PositionType:
        """Dapatkan tipe posisi saat ini"""
        return self.get_current()["type"]
    
    def get_current_activity(self) -> str:
        """Dapatkan aktivitas random di posisi saat ini"""
        position = self.get_current()
        return random.choice(position["activities"])
    
    def get_random_position(self) -> Dict:
        """Dapatkan posisi random (untuk callback)"""
        pos_id = random.choice(list(self.positions.keys()))
        return self.positions[pos_id]
    
    def get_random_position_with_activity(self) -> Tuple[Dict, str]:
        """Dapatkan posisi random + aktivitas random"""
        pos = self.get_random_position()
        activity = random.choice(pos["activities"])
        return pos, activity
    
    def change_position(self, position_id: str = None) -> Dict:
        """Ganti posisi"""
        old_position = self.current_position
        
        if position_id and position_id in self.positions:
            self.current_position = position_id
        else:
            others = [p for p in self.positions.keys() if p != self.current_position]
            self.current_position = random.choice(others) if others else "duduk"
        
        self.last_change = time.time()
        
        logger.info(f"🧍 Position changed: {old_position} → {self.current_position}")
        return self.get_current()
    
    def change_by_activity(self, activity: str) -> Dict:
        """Ganti posisi berdasarkan aktivitas"""
        for pos_id, pos_data in self.positions.items():
            if activity in pos_data["activities"]:
                self.current_position = pos_id
                self.last_change = time.time()
                logger.info(f"🧍 Position changed by activity: {activity} → {pos_data['name']}")
                break
        else:
            self.change_position()
        
        return self.get_current()
    
    def random_change(self, chance: float = 0.1) -> Optional[Dict]:
        """Random ganti posisi (10% chance)"""
        if random.random() < chance:
            return self.change_position()
        return None
    
    def get_position_for_intimacy(self, level: int) -> Dict:
        """
        Dapatkan posisi yang cocok untuk level intimacy
        
        Args:
            level: Level intimacy (1-12)
        
        Returns:
            Position dict
        """
        if level <= 3:
            # Posisi sederhana
            candidates = ["duduk", "berdiri", "bersandar"]
        elif level <= 6:
            # Mulai eksplorasi
            candidates = ["duduk", "berbaring", "miring", "duduk_sila"]
        elif level <= 9:
            # Posisi intim
            candidates = ["berbaring", "miring", "telentang", "merangkak"]
        else:
            # Semua posisi
            candidates = list(self.positions.keys())
        
        pos_id = random.choice(candidates)
        return self.positions[pos_id]
    
    def get_all_positions(self) -> List[str]:
        """Dapatkan semua nama posisi"""
        return [pos["name"] for pos in self.positions.values()]
    
    def get_positions_by_type(self, pos_type: PositionType) -> List[Dict]:
        """Dapatkan posisi berdasarkan tipe"""
        return [pos for pos in self.positions.values() if pos["type"] == pos_type]
    
    def format_position_text(self) -> str:
        """Format teks posisi untuk ditampilkan"""
        pos = self.get_current()
        return f"🧍 Aku lagi **{pos['description']}**."
    
    def get_change_message(self) -> str:
        """Dapatkan pesan saat ganti posisi"""
        pos = self.get_current()
        return f"*{pos['emoji']} Aku {pos['description']}*"
    
    def get_stats(self) -> Dict:
        """Dapatkan statistik posisi"""
        return {
            "total_positions": len(self.positions),
            "current": self.current_position,
            "by_type": {
                "duduk": len(self.get_positions_by_type(PositionType.DUDUK)),
                "berdiri": len(self.get_positions_by_type(PositionType.BERDIRI)),
                "berbaring": len(self.get_positions_by_type(PositionType.BERBARING)),
                "bersandar": len(self.get_positions_by_type(PositionType.BERSANDAR)),
                "jongkok": len(self.get_positions_by_type(PositionType.JONGKOK)),
                "merangkak": len(self.get_positions_by_type(PositionType.MERANGKAK)),
                "miring": len(self.get_positions_by_type(PositionType.MIRING)),
                "telentang": len(self.get_positions_by_type(PositionType.TELENTANG)),
                "telungkup": len(self.get_positions_by_type(PositionType.TELUNGKUP)),
                "duduk_sila": len(self.get_positions_by_type(PositionType.DUDUK_SILA))
            }
        }


__all__ = ['PositionSystem', 'PositionType']
