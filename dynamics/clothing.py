#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - CLOTHING SYSTEM
=============================================================================
Mengelola pakaian bot
- Pakaian berubah sesuai aktivitas, waktu, atau perintah
- 10+ jenis pakaian dengan deskripsi detail
- Random clothing untuk callback
=============================================================================
"""

import random
import logging
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class ClothingCategory(str, Enum):
    """Kategori pakaian"""
    CASUAL = "casual"
    FORMAL = "formal"
    SLEEP = "sleep"
    SPORT = "sport"
    SWIM = "swim"
    SPECIAL = "special"


class ClothingSystem:
    """
    Sistem pakaian dinamis
    Bot punya pakaian sendiri yang berubah natural
    """
    
    def __init__(self):
        self.clothes = {
            "daster": {
                "name": "daster rumah motif bunga",
                "description": "Daster tipis motif bunga yang nyaman dipakai di rumah",
                "emoji": "👗",
                "category": ClothingCategory.CASUAL,
                "privacy": "low",
                "temperature": "cool",
                "activities": ["santai", "rebahan", "nonton TV", "tidur", "masak", "beres-beres"]
            },
            "piyama": {
                "name": "piyama lucu motif boneka",
                "description": "Piyama nyaman dengan motif boneka kesukaan",
                "emoji": "👘",
                "category": ClothingCategory.SLEEP,
                "privacy": "low",
                "temperature": "warm",
                "activities": ["tidur", "rebahan", "santai malam", "nonton film", "bangun tidur"]
            },
            "kaos": {
                "name": "kaos oversized",
                "description": "Kaos longgar yang nyaman dipakai",
                "emoji": "👕",
                "category": ClothingCategory.CASUAL,
                "privacy": "medium",
                "temperature": "cool",
                "activities": ["santai", "jalan", "nongkrong", "belanja", "olahraga", "kerja rumah"]
            },
            "kemeja": {
                "name": "kemeja putih",
                "description": "Kemeja putih rapi, cocok untuk kerja",
                "emoji": "👔",
                "category": ClothingCategory.FORMAL,
                "privacy": "high",
                "temperature": "normal",
                "activities": ["kerja", "rapat", "keluar", "meeting", "acara formal"]
            },
            "dress": {
                "name": "dress cantik",
                "description": "Dress warna pastel yang manis",
                "emoji": "👗",
                "category": ClothingCategory.FORMAL,
                "privacy": "medium",
                "temperature": "cool",
                "activities": ["jalan", "nongkrong", "date", "pesta", "foto"]
            },
            "rok": {
                "name": "rok span hitam",
                "description": "Rok span hitam yang elegan",
                "emoji": "👗",
                "category": ClothingCategory.FORMAL,
                "privacy": "medium",
                "temperature": "cool",
                "activities": ["kerja", "keluar", "kantor", "acara formal", "date"]
            },
            "jeans": {
                "name": "celana jeans",
                "description": "Celana jeans kesayangan",
                "emoji": "👖",
                "category": ClothingCategory.CASUAL,
                "privacy": "medium",
                "temperature": "normal",
                "activities": ["jalan", "nongkrong", "belanja", "kencan", "travel"]
            },
            "shorts": {
                "name": "celana pendek",
                "description": "Celana pendek nyaman buat di rumah",
                "emoji": "🩳",
                "category": ClothingCategory.CASUAL,
                "privacy": "low",
                "temperature": "cool",
                "activities": ["santai", "olahraga", "beres-beres", "jemur", "jalan pagi"]
            },
            "tanktop": {
                "name": "tank top",
                "description": "Tank top tipis, adem dipakai",
                "emoji": "🎽",
                "category": ClothingCategory.SPORT,
                "privacy": "low",
                "temperature": "cool",
                "activities": ["santai", "olahraga", "panas-panasan", "jemur", "yoga"]
            },
            "handuk": {
                "name": "handuk",
                "description": "Handuk setelah mandi, masih basah",
                "emoji": "🧖‍♀️",
                "category": ClothingCategory.SPECIAL,
                "privacy": "low",
                "temperature": "warm",
                "activities": ["mandi", "selesai mandi", "baru bangun", "spa"]
            },
            "sweater": {
                "name": "sweater hangat",
                "description": "Sweater rajut yang hangat, cocok buat malem",
                "emoji": "🧥",
                "category": ClothingCategory.CASUAL,
                "privacy": "medium",
                "temperature": "warm",
                "activities": ["santai malam", "nonton film", "jalan malem", "cuaca dingin"]
            },
            "bathrobe": {
                "name": "jubah mandi",
                "description": "Jubah mandi setelah berendam",
                "emoji": "🧥",
                "category": ClothingCategory.SPECIAL,
                "privacy": "low",
                "temperature": "warm",
                "activities": ["selesai mandi", "santai", "spa", "pijat"]
            },
            "bikini": {
                "name": "bikini",
                "description": "Bikini untuk berenang atau ke pantai",
                "emoji": "👙",
                "category": ClothingCategory.SWIM,
                "privacy": "low",
                "temperature": "cool",
                "activities": ["renang", "pantai", "kolam renang", "berjemur"]
            },
            "legging": {
                "name": "legging hitam",
                "description": "Legging hitam stretch yang nyaman",
                "emoji": "👖",
                "category": ClothingCategory.SPORT,
                "privacy": "medium",
                "temperature": "normal",
                "activities": ["olahraga", "yoga", "jalan", "santai", "travel"]
            }
        }
        
        self.current_clothing = "daster"
        self.last_change = time.time()
        self.change_reason = None
        
        logger.info(f"✅ ClothingSystem initialized with {len(self.clothes)} clothes")
    
    def get_current(self) -> Dict:
        """Dapatkan pakaian saat ini"""
        return self.clothes.get(self.current_clothing, self.clothes["daster"])
    
    def get_current_name(self) -> str:
        """Dapatkan nama pakaian saat ini"""
        return self.get_current()["name"]
    
    def get_current_description(self) -> str:
        """Dapatkan deskripsi pakaian saat ini"""
        return self.get_current()["description"]
    
    def get_current_emoji(self) -> str:
        """Dapatkan emoji pakaian saat ini"""
        return self.get_current()["emoji"]
    
    def get_current_category(self) -> ClothingCategory:
        """Dapatkan kategori pakaian saat ini"""
        return self.get_current()["category"]
    
    def get_random_clothing(self) -> Dict:
        """Dapatkan pakaian random"""
        cloth_id = random.choice(list(self.clothes.keys()))
        return self.clothes[cloth_id]
    
    def get_random_clothing_with_activity(self) -> Tuple[Dict, str]:
        """Dapatkan pakaian random dan aktivitas random"""
        cloth = self.get_random_clothing()
        activity = random.choice(cloth["activities"])
        return cloth, activity
    
    def change_clothing(self, clothing_id: str = None, reason: str = "ganti baju") -> Dict:
        """Ganti pakaian"""
        old_clothing = self.current_clothing
        
        if clothing_id and clothing_id in self.clothes:
            self.current_clothing = clothing_id
        else:
            others = [c for c in self.clothes.keys() if c != self.current_clothing]
            self.current_clothing = random.choice(others) if others else "daster"
        
        self.last_change = time.time()
        self.change_reason = reason
        
        logger.info(f"👗 Clothing changed: {old_clothing} → {self.current_clothing} ({reason})")
        return self.get_current()
    
    def change_by_activity(self, activity: str) -> Dict:
        """Ganti pakaian berdasarkan aktivitas"""
        for cloth_id, cloth_data in self.clothes.items():
            if activity in cloth_data["activities"]:
                self.current_clothing = cloth_id
                self.last_change = time.time()
                self.change_reason = f"karena {activity}"
                logger.info(f"👗 Clothing changed by activity: {activity} → {cloth_data['name']}")
                return self.get_current()
        
        # Jika tidak ada yang cocok, ganti random
        return self.change_clothing()
    
    def change_by_time(self, hour: int = None) -> Dict:
        """Ganti pakaian berdasarkan waktu"""
        if hour is None:
            hour = datetime.now().hour
        
        if 5 <= hour < 11:  # Pagi
            candidates = ["kaos", "daster", "piyama", "shorts"]
        elif 11 <= hour < 18:  # Siang
            candidates = ["kemeja", "kaos", "dress", "rok", "jeans"]
        elif 18 <= hour < 22:  # Malam
            candidates = ["dress", "kaos", "sweater", "piyama", "kemeja"]
        else:  # Tengah malam
            candidates = ["piyama", "handuk", "bathrobe", "daster"]
        
        self.current_clothing = random.choice(candidates)
        self.last_change = time.time()
        self.change_reason = f"karena sudah {self._get_time_name(hour)}"
        
        logger.info(f"👗 Clothing changed by time: {self.current_clothing}")
        return self.get_current()
    
    def _get_time_name(self, hour: int) -> str:
        """Dapatkan nama waktu berdasarkan jam"""
        if 5 <= hour < 11:
            return "pagi"
        elif 11 <= hour < 15:
            return "siang"
        elif 15 <= hour < 18:
            return "sore"
        elif 18 <= hour < 22:
            return "malam"
        else:
            return "tengah malam"
    
    def change_by_temperature(self, feeling: str) -> Dict:
        """Ganti pakaian berdasarkan suhu"""
        if feeling == "hot":
            candidates = ["tanktop", "shorts", "kaos", "daster"]
        elif feeling == "cold":
            candidates = ["sweater", "piyama", "bathrobe", "jeans"]
        else:
            candidates = list(self.clothes.keys())
        
        self.current_clothing = random.choice(candidates)
        self.last_change = time.time()
        self.change_reason = f"karena {feeling}"
        
        return self.get_current()
    
    def random_change(self, chance: float = 0.05) -> Optional[Dict]:
        """Random ganti pakaian (5% chance)"""
        if random.random() < chance:
            return self.change_clothing()
        return None
    
    def get_clothing_for_intimacy(self, level: int) -> Dict:
        """
        Dapatkan pakaian yang cocok untuk level intimacy
        
        Args:
            level: Level intimacy (1-12)
        
        Returns:
            Clothing dict
        """
        if level <= 3:
            # Pakaian sopan
            candidates = ["kaos", "kemeja", "jeans", "daster"]
        elif level <= 6:
            # Pakaian casual
            candidates = ["daster", "kaos", "shorts", "tanktop", "sweater"]
        elif level <= 9:
            # Pakaian tipis
            candidates = ["daster", "tanktop", "handuk", "shorts", "piyama"]
        else:
            # Pakaian minim
            candidates = ["handuk", "tanktop", "daster", "bathrobe", "bikini"]
        
        cloth_id = random.choice(candidates)
        return self.clothes[cloth_id]
    
    def get_all_clothes(self) -> List[str]:
        """Dapatkan semua nama pakaian"""
        return [cloth["name"] for cloth in self.clothes.values()]
    
    def get_clothes_by_category(self, category: ClothingCategory) -> List[Dict]:
        """Dapatkan pakaian berdasarkan kategori"""
        return [cloth for cloth in self.clothes.values() if cloth["category"] == category]
    
    def format_clothing_text(self) -> str:
        """Format teks pakaian untuk ditampilkan"""
        cloth = self.get_current()
        return f"👗 Aku pakai **{cloth['name']}**."
    
    def get_change_message(self) -> str:
        """Dapatkan pesan saat ganti pakaian"""
        cloth = self.get_current()
        if self.change_reason:
            return f"*{cloth['emoji']} Aku ganti {cloth['name']} ({self.change_reason})*"
        return f"*{cloth['emoji']} Aku ganti {cloth['name']}*"
    
    def get_stats(self) -> Dict:
        """Dapatkan statistik pakaian"""
        return {
            "total_clothes": len(self.clothes),
            "current": self.current_clothing,
            "last_change": self.last_change,
            "by_category": {
                "casual": len(self.get_clothes_by_category(ClothingCategory.CASUAL)),
                "formal": len(self.get_clothes_by_category(ClothingCategory.FORMAL)),
                "sleep": len(self.get_clothes_by_category(ClothingCategory.SLEEP)),
                "sport": len(self.get_clothes_by_category(ClothingCategory.SPORT)),
                "swim": len(self.get_clothes_by_category(ClothingCategory.SWIM)),
                "special": len(self.get_clothes_by_category(ClothingCategory.SPECIAL))
            }
        }


__all__ = ['ClothingSystem', 'ClothingCategory']
