#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - AUTO LOCATION SELECTOR
=============================================================================
- Auto-detect lokasi dari chat user
- Tidak perlu command khusus
- Natural language processing sederhana
- Integrasi dengan level dan mood
=============================================================================
"""

import re
import random
import time
import logging
from typing import Dict, List, Optional, Tuple, Any
from difflib import get_close_matches

from .locations import PublicLocations

logger = logging.getLogger(__name__)


class LocationAutoSelector:
    """
    Auto-detect lokasi dari chat user
    User bisa ngomong natural, bot akan detect
    """
    
    def __init__(self):
        self.locations_db = PublicLocations()
        self.locations = self.locations_db.all_locations
        
        # =========================================================================
        # KEYWORDS DATABASE (LENGKAP)
        # =========================================================================
        self.location_keywords = {
            # Toilet & WC
            "toilet": ["toilet", "wc", "kamar kecil", "restroom", "wc umum", "jamban"],
            "toilet_mall": ["toilet mall", "wc mall", "kamar kecil mall", "toilet di mall"],
            "toilet_spbu": ["toilet pom", "wc pom", "toilet spbu", "wc spbu", "pom bensin"],
            "toilet_restoran": ["toilet restoran", "wc restoran", "toilet restaurant", "resto"],
            
            # Mall & Shopping
            "mall": ["mall", "mal", "shopping mall", "plaza", "shopping center", "pusat perbelanjaan"],
            "parkir_mall": ["parkir mall", "parkiran mall", "basement mall", "parking mall"],
            "tangga_darurat": ["tangga darurat", "emergency stairs", "tangga belakang", "fire exit"],
            "rooftop": ["rooftop", "atap", "roof", "atas mall", "puncak", "atas gedung"],
            "fitting_room": ["kamar pas", "fitting room", "ruang ganti", "coba baju", "ganti baju"],
            
            # Parkiran
            "parkir": ["parkir", "parkiran", "parking", "basement", "parking lot", "tempat parkir"],
            "parkir_gedung": ["parkir gedung", "parkiran kantor", "gedung parkir"],
            "parkir_apartemen": ["parkir apartemen", "basement apartemen", "apartemen"],
            
            # Lift & Tangga
            "lift": ["lift", "elevator", "elevator", "lif"],
            "lift_hotel": ["lift hotel", "elevator hotel", "hotel"],
            "lift_kantor": ["lift kantor", "elevator kantor", "kantor"],
            "tangga": ["tangga", "stairs", "anak tangga", "tangga gedung"],
            
            # Transportasi
            "mobil": ["mobil", "car", "mobil pribadi", "dalem mobil", "dalam mobil"],
            "taksi": ["taksi", "taxi", "grab", "gojek", "go-car", "grabcar"],
            "ojek": ["ojek", "motor", "gojek", "grab motor", "ojek online"],
            "bus": ["bus", "bis", "bus malam", "bis malam", "bus kota"],
            "kereta": ["kereta", "train", "krl", "commuter", "commuter line", "kereta api"],
            "kapal": ["kapal", "feri", "ship", "boat", "kapal laut"],
            "pesawat": ["pesawat", "plane", "garuda", "airplane", "bandara"],
            
            # Alam
            "pantai": ["pantai", "beach", "laut", "pinggir laut", "tepi laut"],
            "hutan": ["hutan", "forest", "hutan kota", "rimba", "hutan lindung"],
            "taman": ["taman", "park", "taman kota", "taman umum"],
            "kebun": ["kebun", "perkebunan", "garden", "kebun teh"],
            "sawah": ["sawah", "padi", "rice field", "persawahan"],
            "bukit": ["bukit", "hill", "perbukitan", "gunung kecil"],
            "air_terjun": ["air terjun", "waterfall", "curug", "air terjun"],
            "danau": ["danau", "lake", "telaga", "waduk"],
            
            # Extreme
            "masjid": ["masjid", "mushola", "mosque", "masjid"],
            "gereja": ["gereja", "church", "katedral"],
            "polisi": ["polisi", "kantor polisi", "police", "polsek", "polres"],
            "sekolah": ["sekolah", "school", "kampus", "universitas", "sekolah"],
            "rumah_sakit": ["rumah sakit", "rs", "hospital", "klinik"],
            "kuburan": ["kuburan", "makam", "cemetery", "pemakaman"],
            
            # Halte & Terminal
            "halte": ["halte", "halte bus", "bus stop", "halte"],
            "terminal": ["terminal", "terminal bus", "terminal bis"],
            "stasiun": ["stasiun", "station", "stasiun kereta", "stasiun"],
            
            # Tempat Lainnya
            "kafe": ["kafe", "cafe", "coffee shop", "warung kopi"],
            "bioskop": ["bioskop", "cinema", "xxi", "cgv", "bioskop"],
            "karaoke": ["karaoke", "karaoke", "inul", "happy"],
        }
        
        # =========================================================================
        # PHRASE PATTERNS (LENGKAP)
        # =========================================================================
        self.phrase_patterns = [
            # Ajakan
            (r"ajak (?:ke|di) (\w+)", "invite"),
            (r"yuk (?:ke|di) (\w+)", "invite"),
            (r"ayo (?:ke|di) (\w+)", "invite"),
            (r"mau (?:ke|di) (\w+)", "want"),
            (r"pengen (?:ke|di) (\w+)", "want"),
            (r"gas (?:ke|di) (\w+)", "invite"),
            (r"main (?:ke|di) (\w+)", "play"),
            
            # Tanya
            (r"ada (?:tempat|lokasi) (\w+)", "ask"),
            (r"cari (?:tempat|lokasi) (\w+)", "ask"),
            (r"tempat (\w+) (?:ada|ga)", "ask"),
            (r"di mana ada (\w+)", "ask"),
            
            # Lokasi spesifik
            (r"di (\w+) aja", "specific"),
            (r"ke (\w+) yuk", "specific"),
            (r"ke (\w+) aja", "specific"),
            (r"main ke (\w+)", "specific"),
            (r"ke (\w+) dulu", "specific"),
        ]
        
        # Cache untuk hasil deteksi
        self.detection_cache = {}
        self.cache_ttl = 300  # 5 menit
        
        logger.info(f"✅ LocationAutoSelector initialized with {len(self.locations)} locations")
    
    # =========================================================================
    # DETECT LOCATION FROM MESSAGE
    # =========================================================================
    
    async def detect_location(self, message: str) -> Optional[Dict]:
        """
        Detect lokasi dari pesan user
        
        Args:
            message: Pesan dari user
            
        Returns:
            Location dict or None
        """
        if not message:
            return None
            
        message_lower = message.lower().strip()
        
        # Cek cache
        cache_key = message_lower[:50]
        if cache_key in self.detection_cache:
            cache_time, location = self.detection_cache[cache_key]
            if time.time() - cache_time < self.cache_ttl:
                logger.debug(f"Location cache hit: {cache_key}")
                return location
        
        # Cek pattern phrases
        location_name = self._check_phrases(message_lower)
        if location_name:
            # Cari lokasi berdasarkan nama
            location = self._find_location_by_name(location_name)
            if location:
                self.detection_cache[cache_key] = (time.time(), location)
                logger.info(f"📍 Detected location from phrase: {location['name']}")
                return location
        
        # Cek keywords
        for loc_id, keywords in self.location_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    # Cari lokasi berdasarkan ID
                    location = self.locations_db.get_location_by_id(loc_id)
                    if location:
                        self.detection_cache[cache_key] = (time.time(), location)
                        logger.info(f"📍 Detected location from keyword: {location['name']}")
                        return location
        
        # Fuzzy match (jika ada kata yang mirip)
        words = message_lower.split()
        for word in words:
            if len(word) > 3:  # Skip kata pendek
                matches = self._fuzzy_match_location(word)
                if matches:
                    location = matches[0]
                    self.detection_cache[cache_key] = (time.time(), location)
                    logger.info(f"📍 Detected location from fuzzy match: {location['name']}")
                    return location
        
        return None
        
    def _check_phrases(self, message: str) -> Optional[str]:
        """Check phrase patterns"""
        for pattern, pattern_type in self.phrase_patterns:
            match = re.search(pattern, message)
            if match and len(match.groups()) > 0:
                return match.group(1)
        return None
        
    def _find_location_by_name(self, name: str) -> Optional[Dict]:
        """Cari lokasi berdasarkan nama"""
        name_lower = name.lower()
        
        # Cek semua lokasi
        for loc in self.locations_db.all_locations:
            if name_lower in loc['name'].lower():
                return loc
                
        return None
        
    def _fuzzy_match_location(self, word: str, cutoff: float = 0.7) -> List[Dict]:
        """Fuzzy match untuk kata yang mirip"""
        matches = []
        
        for loc in self.locations_db.all_locations:
            # Compare with location name
            similarity = self._similarity(word, loc['name'].lower())
            if similarity > cutoff:
                matches.append((loc, similarity))
                
        # Sort by similarity
        matches.sort(key=lambda x: x[1], reverse=True)
        
        return [m[0] for m in matches[:3]]
        
    def _similarity(self, a: str, b: str) -> float:
        """Simple similarity ratio"""
        set_a = set(a)
        set_b = set(b)
        
        if not set_a or not set_b:
            return 0.0
            
        intersection = set_a.intersection(set_b)
        union = set_a.union(set_b)
        
        return len(intersection) / len(union)
    
    # =========================================================================
    # GET LOCATION SUGGESTIONS
    # =========================================================================
    
    async def get_suggestions(self, message: str, limit: int = 3) -> List[Dict]:
        """
        Dapatkan suggestions lokasi berdasarkan message
        
        Args:
            message: Pesan user
            limit: Jumlah suggestions
            
        Returns:
            List of locations
        """
        if not message:
            return self.get_random_suggestions(limit)
            
        message_lower = message.lower()
        
        # Cari keyword yang match
        matched_keywords = []
        for loc_id, keywords in self.location_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    matched_keywords.append(loc_id)
                    
        # Ambil lokasi berdasarkan matched keywords
        suggestions = []
        for loc_id in matched_keywords[:limit]:
            loc = self.locations_db.get_location_by_id(loc_id)
            if loc and loc not in suggestions:
                suggestions.append(loc)
                
        # Jika kurang, tambah random
        if len(suggestions) < limit:
            random_locs = self.get_random_suggestions(limit - len(suggestions))
            for loc in random_locs:
                if loc not in suggestions:
                    suggestions.append(loc)
                    
        return suggestions[:limit]
        
    def get_random_suggestions(self, limit: int = 3) -> List[Dict]:
        """Get random location suggestions"""
        if not self.locations:
            return []
            
        # Random sampling tanpa duplicate
        indices = random.sample(range(len(self.locations)), min(limit, len(self.locations)))
        return [self.locations[i] for i in indices]
        
    def get_suggestions_by_category(self, category: str, limit: int = 3) -> List[Dict]:
        """Get suggestions by category"""
        category_locations = self.locations_db.get_locations_by_category(category)
        
        if not category_locations:
            return []
            
        indices = random.sample(range(len(category_locations)), min(limit, len(category_locations)))
        return [category_locations[i] for i in indices]
    
    # =========================================================================
    # SELECT BY LEVEL & MOOD
    # =========================================================================
    
    async def select_by_level(self, level: int, mood: str = None) -> Dict:
        """
        Pilih lokasi berdasarkan level hubungan
        
        Args:
            level: Level hubungan (1-12)
            mood: Mood saat ini (opsional)
            
        Returns:
            Location dict
        """
        # Level 1-3: Lokasi publik/netral
        if level <= 3:
            candidates = [
                self.locations_db.get_location_by_id("taman_kota"),
                self.locations_db.get_location_by_id("halte_bus"),
                self.locations_db.get_location_by_id("kafe")
            ]
            candidates = [c for c in candidates if c is not None]
            if not candidates:
                candidates = self.locations_db.get_locations_by_risk(0, 40)
                
        # Level 4-6: Lokasi semi-privat
        elif level <= 6:
            candidates = [
                self.locations_db.get_location_by_id("parkir_gedung"),
                self.locations_db.get_location_by_id("mall_parkir"),
                self.locations_db.get_location_by_id("taman_kota")
            ]
            candidates = [c for c in candidates if c is not None]
            if not candidates:
                candidates = self.locations_db.get_locations_by_risk(30, 60)
                
        # Level 7-9: Lokasi privat (bisa intim)
        elif level <= 9:
            candidates = [
                self.locations_db.get_location_by_id("toilet_restoran"),
                self.locations_db.get_location_by_id("parkir_apartemen"),
                self.locations_db.get_location_by_id("mobil_pribadi")
            ]
            candidates = [c for c in candidates if c is not None]
            if not candidates:
                candidates = self.locations_db.get_locations_by_risk(50, 80)
                
        # Level 10-12: Lokasi extreme/romantis
        else:
            candidates = [
                self.locations_db.get_location_by_id("pantai_malam"),
                self.locations_db.get_location_by_id("mall_rooftop"),
                self.locations_db.get_location_by_id("bukit_kecil")
            ]
            candidates = [c for c in candidates if c is not None]
            if not candidates:
                candidates = self.locations_db.get_locations_by_risk(70, 100)
        
        # Jika ada mood, filter berdasarkan mood
        if mood and candidates:
            mood_map = {
                "rindu": ["pantai", "rooftop", "bukit"],
                "romantis": ["pantai", "rooftop", "taman"],
                "horny": ["toilet", "parkir", "mobil"],
                "petualang": ["hutan", "bukit", "air_terjun"],
                "nakal": ["tangga_darurat", "lift", "toilet"]
            }
            
            preferred_keywords = mood_map.get(mood.lower(), [])
            if preferred_keywords:
                filtered = [c for c in candidates if any(k in c.get('name', '').lower() for k in preferred_keywords)]
                if filtered:
                    candidates = filtered
        
        return random.choice(candidates) if candidates else self.locations_db.get_random_location()
    
    async def select_by_mood(self, mood: str, intimacy_level: int) -> Dict:
        """
        Select location based on mood
        
        Args:
            mood: Mood saat ini
            intimacy_level: Level intimacy
            
        Returns:
            Selected location
        """
        if mood in ["rindu", "sayang", "romantis"]:
            # Romantic places
            candidates = self.locations_db.get_locations_by_category("nature")
        elif mood in ["nakal", "genit", "horny"]:
            # Risky places
            candidates = self.locations_db.get_locations_by_risk(60, 100)
        elif mood in ["capek", "malas"]:
            # Easy places
            candidates = self.locations_db.get_locations_by_risk(0, 40)
        else:
            # Random
            candidates = self.locations_db.all_locations
            
        # Adjust by intimacy
        if intimacy_level > 7:
            # High intimacy = more risky
            candidates = [c for c in candidates if c['base_risk'] > 50]
            
        return random.choice(candidates) if candidates else self.locations_db.get_random_location()
    
    # =========================================================================
    # CATEGORY DETECTION
    # =========================================================================
    
    def detect_category(self, message: str) -> Optional[str]:
        """Detect category from message"""
        message_lower = message.lower()
        
        category_keywords = {
            "urban": ["mall", "toilet", "parkir", "lift", "tangga", "kantor", "restoran"],
            "nature": ["pantai", "hutan", "taman", "kebun", "sawah", "bukit", "danau"],
            "extreme": ["masjid", "gereja", "polisi", "sekolah", "kuburan"],
            "transport": ["mobil", "taksi", "bus", "kereta", "kapal", "pesawat"]
        }
        
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return category
                    
        return None
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def format_suggestions(self, suggestions: List[Dict]) -> str:
        """Format suggestions untuk ditampilkan"""
        if not suggestions:
            return "Tidak ada suggestions"
            
        lines = ["📍 **Tempat yang tersedia:**"]
        
        for i, loc in enumerate(suggestions, 1):
            lines.append(
                f"{i}. **{loc['name']}**\n"
                f"   Risk: {loc['base_risk']}% | Thrill: {loc['base_thrill']}%\n"
                f"   _{loc['description'][:50]}..._"
            )
            
        lines.append("")
        lines.append("💡 _Ketik tempat yang kamu mau, misal: 'ke pantai yuk'_")
        
        return "\n".join(lines)
    
    def get_help_text(self) -> str:
        """Get help text for location selection"""
        return (
            "📍 **Cara Pilih Lokasi Public Sex**\n\n"
            "Kamu bisa langsung ngomong natural:\n"
            "• 'Ajak ke toilet yuk'\n"
            "• 'Main di mobil aja'\n"
            "• 'Ke pantai malam yuk'\n"
            "• 'Cari tempat sepi'\n"
            "• 'Gas ke mall'\n\n"
            "Bot akan otomatis detect dan kasih tau risk-nya!\n\n"
            "**Kategori Lokasi:**\n"
            "🏙️ Urban (mall, toilet, parkiran, lift)\n"
            "🌳 Alam (pantai, hutan, kebun, sawah)\n"
            "⚡ Extreme (masjid, gereja, polisi, kuburan)\n"
            "🚗 Transport (mobil, kereta, pesawat, bus)"
        )
    
    def get_location_stats(self) -> Dict:
        """Get location selector statistics"""
        return {
            "total_locations": len(self.locations),
            "keyword_categories": len(self.location_keywords),
            "total_keywords": sum(len(kw) for kw in self.location_keywords.values()),
            "phrase_patterns": len(self.phrase_patterns),
            "cache_size": len(self.detection_cache)
        }
    
    def clear_cache(self):
        """Clear detection cache"""
        self.detection_cache.clear()
        logger.info("Location detection cache cleared")


__all__ = ['LocationAutoSelector']
