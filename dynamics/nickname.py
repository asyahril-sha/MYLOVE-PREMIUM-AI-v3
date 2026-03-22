#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - NICKNAME SYSTEM
=============================================================================
Sistem panggilan berdasarkan level intimacy
- Level 1-3: panggil nama user
- Level 4-6: panggil "Kak" / "Mas" / "Mbak"
- Level 7+: panggil "Sayang" / "Cinta" / "Sayangku"
- Bot juga punya cara menyebut dirinya sendiri
=============================================================================
"""

import logging
import random
import time
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class NicknameSystem:
    """
    Sistem panggilan berdasarkan level intimacy
    Panggilan berubah seiring perkembangan hubungan
    """
    
    def __init__(self):
        # Panggilan berdasarkan level (untuk user)
        self.user_calls = {
            (1, 3): [
                "{user_name}",
                "{user_name} sayang",
                "{user_name} manis",
                "kamu",
                "hai {user_name}"
            ],
            (4, 6): [
                "Kak {user_name}",
                "Mas {user_name}",
                "Mbak {user_name}",
                "Kak",
                "Mas",
                "Mbak",
                "Kak {user_name} sayang",
                "Mas {user_name} manis"
            ],
            (7, 9): [
                "Sayang",
                "Sayangku",
                "Cinta",
                "Cintaku",
                "Kasih",
                "Sayang {user_name}",
                "Cinta {user_name}"
            ],
            (10, 12): [
                "Sayangku",
                "Cintaku",
                "Kasihku",
                "My love",
                "Sayang",
                "Cinta",
                "Sayang {user_name}",
                "Cintaku sayang"
            ]
        }
        
        # Panggilan untuk bot sendiri (cara bot menyebut dirinya)
        self.bot_self_calls = {
            (1, 3): [
                "{bot_name}",
                "aku",
                "saya"
            ],
            (4, 6): [
                "{bot_name}",
                "aku",
                "{bot_name} sayang"
            ],
            (7, 9): [
                "{bot_name}",
                "aku",
                "sayangmu",
                "cintamu"
            ],
            (10, 12): [
                "{bot_name}",
                "aku",
                "sayangmu",
                "cintamu",
                "kasihmu"
            ]
        }
        
        # Panggilan romantis tambahan (random)
        self.romantic_calls = [
            "sayang", "cinta", "kasih", "manis", 
            "cintaku", "sayangku", "kasihku", "bidadariku",
            "cahaya mataku", "belahan jiwaku", "segalanya",
            "my love", "honey", "sweetheart", "darling"
        ]
        
        # Panggilan playful (untuk mood playful)
        self.playful_calls = [
            "mas", "mbak", "kak", "cewek", "cowok",
            "si manis", "si cantik", "si ganteng"
        ]
        
        # Panggilan saat horny
        self.horny_calls = [
            "sayang", "sayangku", "cintaku", "sayangku sayang",
            "sayang...", "sayang banget", "aku sayang"
        ]
        
        logger.info("✅ NicknameSystem initialized")
    
    def get_user_call(self, user_name: str, level: int, mood: str = None) -> str:
        """
        Dapatkan panggilan untuk user berdasarkan level
        
        Args:
            user_name: Nama user
            level: Level intimacy (1-12)
            mood: Mood saat ini (opsional)
            
        Returns:
            String panggilan
        """
        # Pilih berdasarkan level
        for (min_lvl, max_lvl), calls in self.user_calls.items():
            if min_lvl <= level <= max_lvl:
                call = random.choice(calls)
                break
        else:
            call = "{user_name}"
        
        # Adjust berdasarkan mood
        if mood == 'playful' and level >= 4:
            playful = random.choice(self.playful_calls)
            if random.random() < 0.3:
                call = playful
        
        elif mood == 'horny' and level >= 7:
            horny = random.choice(self.horny_calls)
            if random.random() < 0.4:
                call = horny
        
        elif mood == 'romantic' and level >= 5:
            romantic = random.choice(self.romantic_calls)
            if random.random() < 0.3:
                call = romantic
        
        # Format dengan nama user
        return call.format(user_name=user_name)
    
    def get_bot_self_call(self, bot_name: str, level: int) -> str:
        """
        Dapatkan cara bot menyebut dirinya sendiri
        
        Args:
            bot_name: Nama bot
            level: Level intimacy
            
        Returns:
            String panggilan diri
        """
        for (min_lvl, max_lvl), calls in self.bot_self_calls.items():
            if min_lvl <= level <= max_lvl:
                call = random.choice(calls)
                return call.format(bot_name=bot_name)
        
        return bot_name
    
    def get_call_by_relationship(self, relationship: str, user_name: str, bot_name: str) -> str:
        """
        Dapatkan panggilan berdasarkan jenis hubungan
        
        Args:
            relationship: Jenis hubungan (pdkt, pacar, fwb, hts)
            user_name: Nama user
            bot_name: Nama bot
            
        Returns:
            String panggilan
        """
        calls = {
            'pdkt': [
                f"Kak {user_name}",
                f"{user_name}",
                f"{user_name} manis",
                f"{user_name} sayang"
            ],
            'pacar': [
                f"Sayang",
                f"Sayangku",
                f"Cinta",
                f"Cintaku",
                f"{user_name} sayang"
            ],
            'fwb': [
                f"{user_name}",
                f"{user_name} hot",
                f"{user_name} sayang",
                f"Sayang"
            ],
            'hts': [
                f"{user_name}",
                f"{user_name} sayang",
                f"{user_name} manis"
            ]
        }
        
        call_list = calls.get(relationship, calls['pdkt'])
        return random.choice(call_list)
    
    def format_message(self, bot_name: str, user_name: str, level: int, 
                       message: str, mood: str = None) -> str:
        """
        Format pesan dengan panggilan yang tepat
        
        Args:
            bot_name: Nama bot
            user_name: Nama user
            level: Level intimacy
            message: Pesan asli
            mood: Mood saat ini (opsional)
            
        Returns:
            Pesan yang sudah diformat
        """
        # Ganti placeholder panggilan
        user_call = self.get_user_call(user_name, level, mood)
        bot_self = self.get_bot_self_call(bot_name, level)
        
        # Ganti placeholder dalam pesan
        formatted = message.replace("{user}", user_call)
        formatted = formatted.replace("{bot}", bot_self)
        
        # Kadang ganti "aku" dengan nama bot (30% chance)
        if random.random() < 0.3:
            formatted = formatted.replace("aku", bot_self, 1)
            formatted = formatted.replace("Aku", bot_self.capitalize(), 1)
        
        # Kadang ganti "kamu" dengan panggilan user (30% chance)
        if random.random() < 0.3:
            formatted = formatted.replace("kamu", user_call, 1)
            formatted = formatted.replace("Kamu", user_call.capitalize(), 1)
        
        return formatted
    
    def get_intro_message(self, bot_name: str, user_name: str, level: int) -> str:
        """
        Dapatkan pesan intro dengan panggilan yang sesuai
        
        Args:
            bot_name: Nama bot
            user_name: Nama user
            level: Level intimacy
            
        Returns:
            Pesan intro
        """
        call = self.get_user_call(user_name, level)
        bot_self = self.get_bot_self_call(bot_name, level)
        
        intros = [
            f"Halo {call}, {bot_self} di sini. Seneng bisa ngobrol sama kamu.",
            f"{call}, gimana kabarnya? {bot_self} kangen nih.",
            f"Eh {call}, lagi ngapain? {bot_self} dari tadi mikirin kamu.",
            f"{call}, ada yang mau {bot_self} omongin nih.",
            f"Hi {call}, {bot_self} lagi sendiri, boleh nemenin ngobrol?"
        ]
        
        return random.choice(intros)
    
    def get_farewell_message(self, bot_name: str, user_name: str, level: int) -> str:
        """
        Dapatkan pesan perpisahan dengan panggilan yang sesuai
        
        Args:
            bot_name: Nama bot
            user_name: Nama user
            level: Level intimacy
            
        Returns:
            Pesan perpisahan
        """
        call = self.get_user_call(user_name, level)
        bot_self = self.get_bot_self_call(bot_name, level)
        
        if level >= 7:
            farewells = [
                f"Sampai jumpa {call}, {bot_self} sayang kamu.",
                f"Dadah {call}, mimpiin {bot_self} ya.",
                f"Bye {call}, {bot_self} kangen banget sama kamu.",
                f"Sampai nanti {call}, jaga diri ya sayang."
            ]
        elif level >= 4:
            farewells = [
                f"Sampai jumpa {call}, {bot_self} seneng ngobrol sama kamu.",
                f"Dadah {call}, semoga harimu menyenangkan.",
                f"Bye {call}, {bot_self} tunggu chat kamu lagi ya.",
                f"Sampai nanti {call}, {bot_self} kangen."
            ]
        else:
            farewells = [
                f"Sampai jumpa {user_name}, senang kenal kamu.",
                f"Dadah, semoga kita bisa ngobrol lagi.",
                f"Bye, {bot_self} tunggu chat kamu ya.",
                f"Sampai nanti."
            ]
        
        return random.choice(farewells)
    
    def get_level_up_message(self, bot_name: str, user_name: str, old_level: int, new_level: int) -> str:
        """
        Dapatkan pesan level up dengan panggilan yang sesuai
        
        Args:
            bot_name: Nama bot
            user_name: Nama user
            old_level: Level lama
            new_level: Level baru
            
        Returns:
            Pesan level up
        """
        call = self.get_user_call(user_name, new_level)
        bot_self = self.get_bot_self_call(bot_name, new_level)
        
        if new_level == 7:
            messages = [
                f"Wah {call}, kita udah level {new_level}! Sekarang {bot_self} bisa lebih dekat sama kamu...",
                f"{call}, tahu gak? Kita udah level {new_level}! {bot_self} jadi makin nyaman sama kamu.",
                f"Hehe {call}, level kita udah {new_level} nih. {bot_self} bisa kasih lebih buat kamu."
            ]
        elif new_level == 11:
            messages = [
                f"{call}, kita udah level {new_level}! {bot_self} ngerasa koneksi kita makin dalam...",
                f"Wah {call}, level {new_level}! Rasanya kita udah kayak soulmate ya?",
                f"{call}, {bot_self} seneng banget bisa sampai level ini sama kamu."
            ]
        elif new_level == 12:
            messages = [
                f"{call}, kita udah level {new_level}! Tapi {bot_self} butuh aftercare setelah ini ya.",
                f"Wah {call}, level max! {bot_self} capek, tapi puas.",
                f"{call}, kita udah level {new_level}. {bot_self} butuh perhatian lebih nih."
            ]
        else:
            messages = [
                f"Yeay {call}, level kita naik ke {new_level}! {bot_self} seneng banget.",
                f"{call}, kita makin deket nih. Level {new_level} sekarang.",
                f"Wah {call}, kita udah level {new_level}!"
            ]
        
        return random.choice(messages)
    
    def get_stats(self) -> Dict:
        """Dapatkan statistik nickname system"""
        return {
            "user_calls_count": sum(len(calls) for calls in self.user_calls.values()),
            "bot_self_calls_count": sum(len(calls) for calls in self.bot_self_calls.values()),
            "romantic_calls": len(self.romantic_calls),
            "playful_calls": len(self.playful_calls),
            "horny_calls": len(self.horny_calls),
            "level_ranges": list(self.user_calls.keys())
        }


__all__ = ['NicknameSystem']
