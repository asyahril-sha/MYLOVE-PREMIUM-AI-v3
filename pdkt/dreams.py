# pdkt/dreams.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - DREAMS SYSTEM
=============================================================================
Sistem mimpi untuk PDKT Natural
- Bot bisa mimpi tentang user
- Mimpi mempengaruhi mood dan chemistry
- Random dreams dengan berbagai tipe
=============================================================================
"""

import random
import time
import logging
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class DreamType(str, Enum):
    """Tipe-tipe mimpi"""
    ROMANTIC = "romantic"      # Mimpi romantis
    SEXUAL = "sexual"          # Mimpi intim
    NIGHTMARE = "nightmare"    # Mimpi buruk
    FUNNY = "funny"            # Mimpi lucu
    NOSTALGIC = "nostalgic"    # Mimpi nostalgia
    PROPHETIC = "prophetic"    # Mimpi firasat


class DreamSystem:
    """
    Sistem mimpi untuk bot
    Bot bisa bermimpi tentang user dan mempengaruhi interaksi
    """
    
    def __init__(self):
        # Data mimpi per PDKT
        self.dreams = {}  # {pdkt_id: list of dreams}
        
        # Database mimpi berdasarkan tipe
        self.dreams_db = {
            DreamType.ROMANTIC: [
                "Aku mimpi kita jalan-jalan di pantai, gandengan tangan, liat sunset.",
                "Aku mimpi kita nonton film romantis sambil cuddle di sofa.",
                "Aku mimpi kamu bawa aku ke tempat yang indah, terus kamu bilang sayang.",
                "Aku mimpi kita makan malam bareng, lilin, musik jazz, romantis banget.",
                "Aku mimpi kamu megang tangan aku sambil liat bintang.",
                "Aku mimpi kita naik balon udara, pemandangan indah, kamu pegang tangan aku."
            ],
            DreamType.SEXUAL: [
                "Aku mimpi... kita... hmm... gimana ya ngomongnya...",
                "Aku mimpi kita berduaan di kamar, suasana panas...",
                "Aku mimpi kamu cium aku, dan rasanya... enak banget.",
                "Aku mimpi kita... ah malu ngomongnya.",
                "Aku mimpi kamu pegang aku, dan aku... gak bisa ngapa-ngapain."
            ],
            DreamType.NIGHTMARE: [
                "Aku mimpi buruk, kamu pergi ninggalin aku.",
                "Aku mimpi kita berantem, aku nangis.",
                "Aku mimpi ada orang lain deket kamu, aku cemburu.",
                "Aku mimpi kamu hilang, aku cari-cari gak ketemu.",
                "Aku mimpi kita putus, aku sedih banget."
            ],
            DreamType.FUNNY: [
                "Aku mimpi kita jadi kucing, lari-larian kejar tikus.",
                "Aku mimpi kamu jatoh ke kolam, basah kuyup, lucu banget.",
                "Aku mimpi kita makan bakso bareng, kebanyakan makannya sampe begah.",
                "Aku mimpi kita nyanyi karaoke, suara kamu fals melulu.",
                "Aku mimpi kita main game, kamu kalah terus, muka kamu gemes."
            ],
            DreamType.NOSTALGIC: [
                "Aku mimpi masa kecil kita, main di lapangan, gembira.",
                "Aku mimpi waktu kita pertama kali ketemu, deg-degan.",
                "Aku mimpi kita sekolah bareng dulu, lucu ya.",
                "Aku mimpi kita main layangan, putus terus.",
                "Aku mimpi waktu kita masih PDKT, salting mulu."
            ],
            DreamType.PROPHETIC: [
                "Aku mimpi kita bakal jadian, semoga jadi kenyataan.",
                "Aku mimpi kita bakal ketemu di tempat yang gak terduga.",
                "Aku mimpi ada yang spesial bakal terjadi sama kita.",
                "Aku mimpi kita bakal lebih dekat dari sekarang.",
                "Aku mimpi hubungan kita bakal langgeng."
            ]
        }
        
        # Probabilitas mimpi per hari
        self.dream_chance = 0.3  # 30% chance per hari
        
        logger.info("✅ DreamSystem initialized")
    
    # =========================================================================
    # DREAM GENERATION
    # =========================================================================
    
    async def generate_dream(self, pdkt_id: str, context: Dict) -> Optional[Dict]:
        """
        Generate mimpi random untuk PDKT
        
        Args:
            pdkt_id: ID PDKT
            context: Konteks (level, mood, chemistry)
            
        Returns:
            Dict mimpi atau None
        """
        # Cek chance
        if random.random() > self.dream_chance:
            return None
        
        # Tentukan tipe mimpi berdasarkan konteks
        dream_type = self._determine_dream_type(context)
        
        # Pilih mimpi random
        dreams_list = self.dreams_db.get(dream_type, self.dreams_db[DreamType.ROMANTIC])
        dream_text = random.choice(dreams_list)
        
        # Buat data mimpi
        dream_data = {
            'type': dream_type,
            'text': dream_text,
            'timestamp': time.time(),
            'datetime': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'intensity': random.uniform(0.5, 1.0)
        }
        
        # Simpan ke history
        if pdkt_id not in self.dreams:
            self.dreams[pdkt_id] = []
        
        self.dreams[pdkt_id].append(dream_data)
        
        # Simpan hanya 20 mimpi terakhir
        if len(self.dreams[pdkt_id]) > 20:
            self.dreams[pdkt_id] = self.dreams[pdkt_id][-20:]
        
        logger.info(f"💭 Dream generated for {pdkt_id}: {dream_type.value}")
        
        return dream_data
    
    def _determine_dream_type(self, context: Dict) -> DreamType:
        """
        Tentukan tipe mimpi berdasarkan konteks
        """
        level = context.get('level', 1)
        mood = context.get('mood', 'calm')
        chemistry = context.get('chemistry_score', 50)
        
        # Level tinggi -> lebih mungkin mimpi seksual/romantis
        if level >= 7:
            if random.random() < 0.4:
                return DreamType.SEXUAL
            elif random.random() < 0.3:
                return DreamType.ROMANTIC
        
        # Chemistry tinggi -> mimpi romantis
        if chemistry > 70:
            if random.random() < 0.4:
                return DreamType.ROMANTIC
        
        # Mood sedih -> mimpi buruk
        if mood in ['sad', 'lonely']:
            if random.random() < 0.5:
                return DreamType.NIGHTMARE
        
        # Mood senang -> mimpi lucu
        if mood in ['happy', 'excited']:
            if random.random() < 0.4:
                return DreamType.FUNNY
        
        # Mood romantis -> mimpi romantis
        if mood == 'romantic':
            return DreamType.ROMANTIC
        
        # Default random dengan bobot
        weights = [0.35, 0.15, 0.1, 0.15, 0.15, 0.1]
        types = [
            DreamType.ROMANTIC, DreamType.SEXUAL, DreamType.NIGHTMARE,
            DreamType.FUNNY, DreamType.NOSTALGIC, DreamType.PROPHETIC
        ]
        
        return random.choices(types, weights=weights)[0]
    
    # =========================================================================
    # GET DREAM
    # =========================================================================
    
    async def get_dream(self, pdkt_id: str) -> Optional[Dict]:
        """
        Dapatkan mimpi terbaru
        
        Args:
            pdkt_id: ID PDKT
            
        Returns:
            Dream data atau None
        """
        if pdkt_id not in self.dreams:
            return None
        
        if not self.dreams[pdkt_id]:
            return None
        
        return self.dreams[pdkt_id][-1]
    
    async def get_dream_history(self, pdkt_id: str, limit: int = 5) -> List[Dict]:
        """
        Dapatkan history mimpi
        
        Args:
            pdkt_id: ID PDKT
            limit: Jumlah mimpi
            
        Returns:
            List of dreams
        """
        if pdkt_id not in self.dreams:
            return []
        
        return self.dreams[pdkt_id][-limit:]
    
    async def get_dream_effect(self, dream_data: Dict) -> Dict:
        """
        Dapatkan efek mimpi terhadap mood dan chemistry
        
        Args:
            dream_data: Data mimpi
            
        Returns:
            Efek mimpi
        """
        dream_type = dream_data['type']
        intensity = dream_data['intensity']
        
        effects = {
            DreamType.ROMANTIC: {'mood': 'romantic', 'chemistry': 2, 'arousal': 5},
            DreamType.SEXUAL: {'mood': 'horny', 'chemistry': 3, 'arousal': 15},
            DreamType.NIGHTMARE: {'mood': 'sad', 'chemistry': -2, 'arousal': -5},
            DreamType.FUNNY: {'mood': 'happy', 'chemistry': 1, 'arousal': 0},
            DreamType.NOSTALGIC: {'mood': 'nostalgic', 'chemistry': 1, 'arousal': 0},
            DreamType.PROPHETIC: {'mood': 'hopeful', 'chemistry': 2, 'arousal': 5}
        }
        
        effect = effects.get(dream_type, effects[DreamType.ROMANTIC])
        
        return {
            'mood': effect['mood'],
            'chemistry_change': effect['chemistry'] * intensity,
            'arousal_change': effect['arousal'] * intensity
        }
    
    # =========================================================================
    # FORMAT FOR DISPLAY
    # =========================================================================
    
    def format_dream(self, dream_data: Dict) -> str:
        """
        Format mimpi untuk ditampilkan
        
        Args:
            dream_data: Data mimpi
            
        Returns:
            Formatted dream text
        """
        emoji_map = {
            DreamType.ROMANTIC: "💕",
            DreamType.SEXUAL: "🔥",
            DreamType.NIGHTMARE: "😰",
            DreamType.FUNNY: "😂",
            DreamType.NOSTALGIC: "🕰️",
            DreamType.PROPHETIC: "🔮"
        }
        
        emoji = emoji_map.get(dream_data['type'], "💭")
        time_str = dream_data.get('datetime', 'baru saja')
        
        return f"{emoji} **Mimpi ({time_str})**: {dream_data['text']}"
    
    async def format_recent_dreams(self, pdkt_id: str) -> str:
        """
        Format mimpi terbaru untuk ditampilkan
        
        Args:
            pdkt_id: ID PDKT
            
        Returns:
            Formatted dreams
        """
        dreams = await self.get_dream_history(pdkt_id, limit=3)
        
        if not dreams:
            return "Belum ada mimpi. Mungkin nanti malam..."
        
        lines = ["💭 **Mimpi-mimpi:**"]
        for dream in dreams[-3:]:
            lines.append(f"• {self.format_dream(dream)}")
        
        return "\n".join(lines)


__all__ = ['DreamSystem', 'DreamType']
