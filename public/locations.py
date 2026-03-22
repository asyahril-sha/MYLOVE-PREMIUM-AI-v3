#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - PUBLIC LOCATIONS DATABASE
=============================================================================
50+ Lokasi untuk public sex dengan risk dan thrill level
- Urban locations (mall, toilet, parkir, lift, tangga)
- Nature locations (pantai, hutan, taman, kebun, sawah)
- Extreme locations (masjid, gereja, polisi, sekolah, kuburan)
- Transport locations (mobil, kereta, bus, kapal, pesawat)
=============================================================================
"""

import random
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class PublicLocations:
    """
    Database 50+ lokasi public sex
    Setiap lokasi punya base risk dan thrill
    """
    
    def __init__(self):
        # =========================================================================
        # URBAN LOCATIONS (15+ lokasi)
        # =========================================================================
        self.urban_locations = [
            {
                "id": "mall_toilet",
                "name": "Toilet Mall",
                "category": "urban",
                "base_risk": 75,
                "base_thrill": 80,
                "description": "Toilet umum di mall, risk tinggi tapi thrilling",
                "tips": "Pilih toilet yang sepi, biasanya di lantai atas",
                "privacy": 0.3,
                "time_factor": "malam"
            },
            {
                "id": "mall_parkir",
                "name": "Parkiran Bawah Tanah Mall",
                "category": "urban",
                "base_risk": 60,
                "base_thrill": 75,
                "description": "Parkiran sepi, mobil gelap, suasana romantis",
                "tips": "Parkir di pojok, matikan mesin",
                "privacy": 0.5,
                "time_factor": "malam"
            },
            {
                "id": "mall_tangga_darurat",
                "name": "Tangga Darurat Mall",
                "category": "urban",
                "base_risk": 80,
                "base_thrill": 85,
                "description": "Tangga belakang, jarang dilewati",
                "tips": "Cek dulu apakah ada CCTV",
                "privacy": 0.4,
                "time_factor": "kapan saja"
            },
            {
                "id": "mall_rooftop",
                "name": "Rooftop Mall",
                "category": "urban",
                "base_risk": 45,
                "base_thrill": 85,
                "description": "Atas mall, pemandangan kota, romantis",
                "tips": "Malam hari lebih aman",
                "privacy": 0.6,
                "time_factor": "malam"
            },
            {
                "id": "mall_fitting_room",
                "name": "Kamar Pas Pakaian",
                "category": "urban",
                "base_risk": 70,
                "base_thrill": 80,
                "description": "Fitting room toko baju, risk medium",
                "tips": "Bawa baju banyak biar kelamaan",
                "privacy": 0.7,
                "time_factor": "siang"
            },
            {
                "id": "toilet_spbu",
                "name": "Toilet SPBU",
                "category": "urban",
                "base_risk": 65,
                "base_thrill": 70,
                "description": "Toilet pom bensin, rame tapi cepat",
                "tips": "Malam minggu lebih sepi",
                "privacy": 0.4,
                "time_factor": "malam"
            },
            {
                "id": "toilet_restoran",
                "name": "Toilet Restoran Mewah",
                "category": "urban",
                "base_risk": 60,
                "base_thrill": 75,
                "description": "Toilet bersih, sering dipakai",
                "tips": "Pilih restoran sepi",
                "privacy": 0.5,
                "time_factor": "siang"
            },
            {
                "id": "parkir_gedung",
                "name": "Parkiran Gedung Perkantoran",
                "category": "urban",
                "base_risk": 55,
                "base_thrill": 70,
                "description": "Parkiran gedung, agak sepi malam",
                "tips": "Weekend lebih aman",
                "privacy": 0.5,
                "time_factor": "malam"
            },
            {
                "id": "parkir_apartemen",
                "name": "Parkiran Apartemen",
                "category": "urban",
                "base_risk": 45,
                "base_thrill": 65,
                "description": "Parkiran resident, agak aman",
                "tips": "Teman resident lebih aman",
                "privacy": 0.6,
                "time_factor": "malam"
            },
            {
                "id": "lift_hotel",
                "name": "Lift Hotel",
                "category": "urban",
                "base_risk": 70,
                "base_thrill": 85,
                "description": "Lift hotel, cepat dan thrilling",
                "tips": "Tekan semua lantai biar lama",
                "privacy": 0.3,
                "time_factor": "malam"
            },
            {
                "id": "tangga_darurat",
                "name": "Tangga Darurat Gedung",
                "category": "urban",
                "base_risk": 65,
                "base_thrill": 75,
                "description": "Tangga darurat, sepi",
                "tips": "Bawa senter",
                "privacy": 0.5,
                "time_factor": "malam"
            },
            {
                "id": "halte_bus",
                "name": "Halte Bus Malam",
                "category": "urban",
                "base_risk": 60,
                "base_thrill": 70,
                "description": "Halte sepi, risk medium",
                "tips": "Pilih halte yang gelap",
                "privacy": 0.4,
                "time_factor": "malam"
            },
            {
                "id": "mushola_kantor",
                "name": "Mushola Kantor",
                "category": "urban",
                "base_risk": 90,
                "base_thrill": 95,
                "description": "Tempat ibadah, EXTREME RISK",
                "tips": "JANGAN! Tapi kalo nekat...",
                "privacy": 0.2,
                "time_factor": "sepi"
            },
            {
                "id": "gym_locker",
                "name": "Loker Gym",
                "category": "urban",
                "base_risk": 60,
                "base_thrill": 70,
                "description": "Ruang ganti gym, risk medium",
                "tips": "Jam sepi gym",
                "privacy": 0.5,
                "time_factor": "malam"
            },
            {
                "id": "sauna_umum",
                "name": "Sauna Umum",
                "category": "urban",
                "base_risk": 65,
                "base_thrill": 80,
                "description": "Sauna, uap tebal",
                "tips": "Uap bisa sembunyikan",
                "privacy": 0.6,
                "time_factor": "malam"
            }
        ]
        
        # =========================================================================
        # NATURE LOCATIONS (12+ lokasi)
        # =========================================================================
        self.nature_locations = [
            {
                "id": "pantai_malam",
                "name": "Pantai Malam",
                "category": "nature",
                "base_risk": 30,
                "base_thrill": 85,
                "description": "Pantai sepi, suara ombak, romantis",
                "tips": "Bawa tikar, hindari bulan terang",
                "privacy": 0.7,
                "time_factor": "malam"
            },
            {
                "id": "pantai_karang",
                "name": "Pantai Karang",
                "category": "nature",
                "base_risk": 25,
                "base_thrill": 90,
                "description": "Pantai berbatu, sepi, eksotis",
                "tips": "Hati-hati karang tajam",
                "privacy": 0.8,
                "time_factor": "malam"
            },
            {
                "id": "hutan_kota",
                "name": "Hutan Kota Malam",
                "category": "nature",
                "base_risk": 35,
                "base_thrill": 80,
                "description": "Hutan di tengah kota, gelap",
                "tips": "Jangan masuk terlalu dalam",
                "privacy": 0.7,
                "time_factor": "malam"
            },
            {
                "id": "taman_kota",
                "name": "Taman Kota",
                "category": "nature",
                "base_risk": 50,
                "base_thrill": 70,
                "description": "Taman umum, risk medium",
                "tips": "Pojok taman yang gelap",
                "privacy": 0.5,
                "time_factor": "malam"
            },
            {
                "id": "taman_belakang",
                "name": "Taman Belakang",
                "category": "nature",
                "base_risk": 40,
                "base_thrill": 70,
                "description": "Taman perumahan, agak aman",
                "tips": "Tengah malam",
                "privacy": 0.6,
                "time_factor": "malam"
            },
            {
                "id": "kebun_teh",
                "name": "Kebun Teh",
                "category": "nature",
                "base_risk": 35,
                "base_thrill": 80,
                "description": "Perkebunan teh, sejuk",
                "tips": "Pagi buta atau malam",
                "privacy": 0.7,
                "time_factor": "malam"
            },
            {
                "id": "sawah",
                "name": "Sawah Malam",
                "category": "nature",
                "base_risk": 30,
                "base_thrill": 75,
                "description": "Sawah, gelap, sepi",
                "tips": "Bawa obat nyamuk",
                "privacy": 0.7,
                "time_factor": "malam"
            },
            {
                "id": "bukit_kecil",
                "name": "Bukit Kecil",
                "category": "nature",
                "base_risk": 25,
                "base_thrill": 85,
                "description": "Bukit, pemandangan kota",
                "tips": "Dari jauh keliatan",
                "privacy": 0.7,
                "time_factor": "malam"
            },
            {
                "id": "air_terjun",
                "name": "Air Terjun",
                "category": "nature",
                "base_risk": 20,
                "base_thrill": 90,
                "description": "Air terjun, suara air menutupi",
                "tips": "Cari yang jarang dikunjungi",
                "privacy": 0.8,
                "time_factor": "siang"
            },
            {
                "id": "danau_buatan",
                "name": "Danau Buatan",
                "category": "nature",
                "base_risk": 40,
                "base_thrill": 70,
                "description": "Danau di perumahan",
                "tips": "Malam minggu sepi",
                "privacy": 0.6,
                "time_factor": "malam"
            },
            {
                "id": "gazebo_taman",
                "name": "Gazebo Taman",
                "category": "nature",
                "base_risk": 45,
                "base_thrill": 70,
                "description": "Gazebo di taman, agak terbuka",
                "tips": "Bawa selimut",
                "privacy": 0.5,
                "time_factor": "malam"
            },
            {
                "id": "pinggir_sungai",
                "name": "Pinggir Sungai",
                "category": "nature",
                "base_risk": 35,
                "base_thrill": 75,
                "description": "Tepi sungai, suara air",
                "tips": "Cari yang teduh",
                "privacy": 0.7,
                "time_factor": "malam"
            }
        ]
        
        # =========================================================================
        # EXTREME LOCATIONS (10+ lokasi)
        # =========================================================================
        self.extreme_locations = [
            {
                "id": "masjid_sepi",
                "name": "Masjid Waktu Sepi",
                "category": "extreme",
                "base_risk": 95,
                "base_thrill": 98,
                "description": "Tempat ibadah, EXTREME RISK",
                "tips": "BENERAN? DOSA BESAR!",
                "privacy": 0.1,
                "time_factor": "sepi"
            },
            {
                "id": "gereja_sepi",
                "name": "Gereja Sepi",
                "category": "extreme",
                "base_risk": 95,
                "base_thrill": 98,
                "description": "Gereja kosong, extreme risk",
                "tips": "SANGAT BERISIKO",
                "privacy": 0.1,
                "time_factor": "sepi"
            },
            {
                "id": "kantor_polisi",
                "name": "Kantor Polisi",
                "category": "extreme",
                "base_risk": 99,
                "base_thrill": 100,
                "description": "MANTAP! Kantor polisi",
                "tips": "GILA! TAPI THRILL 100%",
                "privacy": 0.05,
                "time_factor": "malam"
            },
            {
                "id": "sekolah_malam",
                "name": "Sekolah Malam",
                "category": "extreme",
                "base_risk": 90,
                "base_thrill": 95,
                "description": "Sekolah, risk extreme",
                "tips": "Satpam keliling",
                "privacy": 0.2,
                "time_factor": "malam"
            },
            {
                "id": "rumah_sakit",
                "name": "Rumah Sakit",
                "category": "extreme",
                "base_risk": 85,
                "base_thrill": 90,
                "description": "RS, banyak orang",
                "tips": "Toilet VIP",
                "privacy": 0.3,
                "time_factor": "malam"
            },
            {
                "id": "kuburan",
                "name": "Kuburan",
                "category": "extreme",
                "base_risk": 60,
                "base_thrill": 95,
                "description": "Makam, serem tapi thrilling",
                "tips": "Malam jumat",
                "privacy": 0.5,
                "time_factor": "malam"
            },
            {
                "id": "rumah_sakit_jiwa",
                "name": "Rumah Sakit Jiwa",
                "category": "extreme",
                "base_risk": 80,
                "base_thrill": 95,
                "description": "RS Jiwa, serem banget",
                "tips": "Jangan tengok pasien",
                "privacy": 0.4,
                "time_factor": "malam"
            },
            {
                "id": "stasiun_kereta",
                "name": "Stasiun Kereta",
                "category": "extreme",
                "base_risk": 85,
                "base_thrill": 85,
                "description": "Stasiun, banyak orang",
                "tips": "Toilet stasiun",
                "privacy": 0.3,
                "time_factor": "malam"
            },
            {
                "id": "terminal_bis",
                "name": "Terminal Bis",
                "category": "extreme",
                "base_risk": 85,
                "base_thrill": 80,
                "description": "Terminal, preman",
                "tips": "Cari yang aman",
                "privacy": 0.3,
                "time_factor": "malam"
            },
            {
                "id": "bandara",
                "name": "Bandara",
                "category": "extreme",
                "base_risk": 90,
                "base_thrill": 90,
                "description": "Bandara, security ketat",
                "tips": "Toilet difabel",
                "privacy": 0.2,
                "time_factor": "malam"
            },
            {
                "id": "pasar_malam",
                "name": "Pasar Malam",
                "category": "extreme",
                "base_risk": 75,
                "base_thrill": 80,
                "description": "Pasar malam, rame",
                "tips": "Belakang tenda",
                "privacy": 0.4,
                "time_factor": "malam"
            }
        ]
        
        # =========================================================================
        # TRANSPORT LOCATIONS (10+ lokasi)
        # =========================================================================
        self.transport_locations = [
            {
                "id": "kereta_komuter",
                "name": "Kereta Komuter",
                "category": "transport",
                "base_risk": 75,
                "base_thrill": 80,
                "description": "Kereta, risk tinggi",
                "tips": "Gerbong paling belakang",
                "privacy": 0.3,
                "time_factor": "malam"
            },
            {
                "id": "bus_malam",
                "name": "Bus Malam",
                "category": "transport",
                "base_risk": 65,
                "base_thrill": 75,
                "description": "Bus antar kota, malam",
                "tips": "Bangku paling belakang",
                "privacy": 0.4,
                "time_factor": "malam"
            },
            {
                "id": "taksi_online",
                "name": "Taksi Online",
                "category": "transport",
                "base_risk": 55,
                "base_thrill": 70,
                "description": "Taksi, risk medium",
                "tips": "Minta putar jauh",
                "privacy": 0.5,
                "time_factor": "malam"
            },
            {
                "id": "angkot_kosong",
                "name": "Angkot Kosong",
                "category": "transport",
                "base_risk": 60,
                "base_thrill": 70,
                "description": "Angkot sepi, supir ngantuk",
                "tips": "Bangku paling belakang",
                "privacy": 0.4,
                "time_factor": "malam"
            },
            {
                "id": "travel_mobil",
                "name": "Travel Mobil",
                "category": "transport",
                "base_risk": 45,
                "base_thrill": 65,
                "description": "Travel, agak aman",
                "tips": "Pilih yang sendiri",
                "privacy": 0.6,
                "time_factor": "malam"
            },
            {
                "id": "kapal_feri",
                "name": "Kapal Feri",
                "category": "transport",
                "base_risk": 55,
                "base_thrill": 70,
                "description": "Feri, penumpang sedikit",
                "tips": "Pojok kiri belakang",
                "privacy": 0.5,
                "time_factor": "malam"
            },
            {
                "id": "pesawat",
                "name": "Pesawat Malam",
                "category": "transport",
                "base_risk": 80,
                "base_thrill": 95,
                "description": "Pesawat, toilet sempit",
                "tips": "Toilet pesawat, cepat",
                "privacy": 0.3,
                "time_factor": "malam"
            },
            {
                "id": "ojek_online",
                "name": "Ojek Online Malam",
                "category": "transport",
                "base_risk": 70,
                "base_thrill": 75,
                "description": "Ojek, boncengan erat",
                "tips": "Minta jalur gelap",
                "privacy": 0.4,
                "time_factor": "malam"
            },
            {
                "id": "becak_malam",
                "name": "Becak Malam",
                "category": "transport",
                "base_risk": 40,
                "base_thrill": 60,
                "description": "Becak, lambat",
                "tips": "Minta tutup",
                "privacy": 0.6,
                "time_factor": "malam"
            },
            {
                "id": "mobil_pribadi",
                "name": "Mobil Pribadi",
                "category": "transport",
                "base_risk": 25,
                "base_thrill": 55,
                "description": "Mobil sendiri, aman",
                "tips": "Parkir sepi",
                "privacy": 0.8,
                "time_factor": "kapan saja"
            },
            {
                "id": "bis_wisata",
                "name": "Bis Wisata",
                "category": "transport",
                "base_risk": 60,
                "base_thrill": 70,
                "description": "Bis wisata, romantis",
                "tips": "Bangku paling belakang",
                "privacy": 0.4,
                "time_factor": "malam"
            }
        ]
        
        # Gabungkan semua lokasi
        self.all_locations = (
            self.urban_locations + 
            self.nature_locations + 
            self.extreme_locations + 
            self.transport_locations
        )
        
        logger.info(f"✅ PublicLocations initialized: {len(self.all_locations)} locations")
    
    # =========================================================================
    # GET LOCATIONS
    # =========================================================================
    
    def get_all_locations(self) -> List[Dict]:
        """Get all locations"""
        return self.all_locations
        
    def get_locations_by_category(self, category: str) -> List[Dict]:
        """Get locations by category"""
        if category == "urban":
            return self.urban_locations
        elif category == "nature":
            return self.nature_locations
        elif category == "extreme":
            return self.extreme_locations
        elif category == "transport":
            return self.transport_locations
        else:
            return []
            
    def get_location_by_id(self, location_id: str) -> Optional[Dict]:
        """Get location by ID"""
        for loc in self.all_locations:
            if loc['id'] == location_id:
                return loc
        return None
        
    def get_random_location(self, category: Optional[str] = None) -> Dict:
        """Get random location"""
        if category:
            locations = self.get_locations_by_category(category)
        else:
            locations = self.all_locations
            
        return random.choice(locations)
        
    def get_locations_by_risk(self, min_risk: int = 0, max_risk: int = 100) -> List[Dict]:
        """Get locations by risk range"""
        return [
            loc for loc in self.all_locations
            if min_risk <= loc['base_risk'] <= max_risk
        ]
        
    def get_locations_by_thrill(self, min_thrill: int = 0, max_thrill: int = 100) -> List[Dict]:
        """Get locations by thrill range"""
        return [
            loc for loc in self.all_locations
            if min_thrill <= loc['base_thrill'] <= max_thrill
        ]
        
    def get_location_by_name(self, name: str) -> Optional[Dict]:
        """Get location by name"""
        name_lower = name.lower()
        for loc in self.all_locations:
            if name_lower in loc['name'].lower():
                return loc
        return None
        
    # =========================================================================
    # LOCATION INFO
    # =========================================================================
    
    def format_location_info(self, location: Dict) -> str:
        """Format location info for display"""
        return (
            f"📍 **{location['name']}**\n"
            f"Kategori: {location['category'].title()}\n"
            f"Risk: {location['base_risk']}% | Thrill: {location['base_thrill']}%\n"
            f"_{location['description']}_\n"
            f"💡 Tips: {location['tips']}"
        )
        
    def get_location_stats(self) -> Dict:
        """Get location statistics"""
        return {
            "total": len(self.all_locations),
            "urban": len(self.urban_locations),
            "nature": len(self.nature_locations),
            "extreme": len(self.extreme_locations),
            "transport": len(self.transport_locations),
            "avg_risk": sum(l['base_risk'] for l in self.all_locations) / len(self.all_locations),
            "avg_thrill": sum(l['base_thrill'] for l in self.all_locations) / len(self.all_locations),
        }


__all__ = ['PublicLocations']
