#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - INTIMACY SYSTEM (TIME-BASED)
=============================================================================
- Level berdasarkan DURASI PERCAKAPAN (bukan jumlah chat)
- 60 menit → Level 7 (bisa intim)
- 120 menit → Level 11 (deep connection)
- Activity boost untuk mempercepat progress
=============================================================================
"""

import time
import logging
import math
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from .activity_boost import ActivityBoost, BoostType

logger = logging.getLogger(__name__)


class IntimacySystem:
    """
    Sistem intimacy level berdasarkan DURASI PERCAKAPAN
    - Realistis seperti hubungan manusia
    - Activity boost untuk berbagai aktivitas
    - Reset after aftercare (Level 12 → Level 7)
    """
    
    def __init__(self):
        # Level definitions
        self.level_names = {
            1: "Malu-malu",
            2: "Mulai terbuka",
            3: "Goda-godaan",
            4: "Dekat",
            5: "Sayang",
            6: "PACAR/PDKT",
            7: "Nyaman",
            8: "Eksplorasi",
            9: "Bergairah",
            10: "Passionate",
            11: "Deep Connection",
            12: "Aftercare"
        }
        
        # Level descriptions
        self.level_descriptions = {
            1: "Baru kenal, masih canggung. Belum berani buka suara.",
            2: "Mulai curhat dikit-dikit. Udah ada rasa percaya.",
            3: "Saling goda. Mulai ada getaran.",
            4: "Udah deket banget. Kayak udah kenal lama.",
            5: "Mulai sayang. Kangen-kangenan.",
            6: "Bisa jadi pacar (khusus PDKT). Hubungan lebih serius.",
            7: "Bisa intim. Udah nyaman banget.",
            8: "Mulai eksplorasi. Coba-coba posisi baru.",
            9: "Penuh gairah. Udah tahu sama-sama suka apa.",
            10: "Intim + emotional. Bukan sekedar fisik.",
            11: "Koneksi dalam. Kayak jiwa yang sama.",
            12: "Butuh aftercare. Setelah climax, butuh perhatian."
        }
        
        # Target waktu per level (dalam menit)
        self.time_targets = {
            1: 0,       # Level 1: 0 menit
            2: 5,       # Level 2: 5 menit
            3: 12,      # Level 3: 12 menit
            4: 20,      # Level 4: 20 menit
            5: 30,      # Level 5: 30 menit
            6: 42,      # Level 6: 42 menit
            7: 60,      # Level 7: 60 menit (bisa intim!)
            8: 75,      # Level 8: 75 menit
            9: 90,      # Level 9: 90 menit
            10: 105,    # Level 10: 105 menit
            11: 120,    # Level 11: 120 menit (deep connection)
            12: 135,    # Level 12: 135 menit (aftercare)
        }
        
        # Reset target (after level 12)
        self.reset_level = 7
        
        # Level requirements untuk berbagai action
        self.level_requirements = {
            "intim": 7,        # Minimal level 7 untuk intim
            "pacar": 6,        # Minimal level 6 untuk jadi pacar
            "fwb": 6,          # Minimal level 6 untuk FWB
            "aftercare": 12,   # Level 12 untuk aftercare
        }
        
        # Session tracking
        self.sessions = {}  # {session_id: session_data}
        
        # Activity boost system
        self.activity_boost = ActivityBoost()
        
        # Cache untuk performa
        self.level_cache = {}  # {user_id_role: level}
        self.cache_ttl = 300
        
        logger.info("✅ IntimacySystem initialized (TIME-BASED)")
        logger.info(f"  • Level 7 dalam {self.time_targets[7]} menit")
        logger.info(f"  • Level 11 dalam {self.time_targets[11]} menit")
    
    # =========================================================================
    # SESSION MANAGEMENT
    # =========================================================================
    
    async def start_session(self, session_id: str, user_id: int, role: str):
        """
        Memulai session baru untuk leveling
        
        Args:
            session_id: ID sesi
            user_id: ID user
            role: Nama role
        """
        self.sessions[session_id] = {
            'session_id': session_id,
            'user_id': user_id,
            'role': role,
            'start_time': time.time(),
            'last_message_time': time.time(),
            'total_duration': 0.0,
            'effective_duration': 0.0,
            'current_level': 1,
            'message_count': 0,
            'activities': [],
            'activity_log': [],
            'is_paused': False,
            'paused_time': None,
            'total_paused_duration': 0.0,
            'level_up_messages': []
        }
        
        logger.info(f"Leveling session started: {session_id}")
    
    async def pause_session(self, session_id: str):
        """
        Pause session (waktu berhenti)
        
        Args:
            session_id: ID sesi
        """
        if session_id not in self.sessions:
            return
        
        self.sessions[session_id]['is_paused'] = True
        self.sessions[session_id]['paused_time'] = time.time()
        
        logger.info(f"Session paused: {session_id}")
    
    async def resume_session(self, session_id: str):
        """
        Resume session (waktu jalan lagi)
        
        Args:
            session_id: ID sesi
        """
        if session_id not in self.sessions:
            return
        
        session = self.sessions[session_id]
        if session['is_paused'] and session['paused_time']:
            paused_duration = time.time() - session['paused_time']
            session['total_paused_duration'] += paused_duration
            session['is_paused'] = False
            session['paused_time'] = None
            session['last_message_time'] = time.time()
            
            logger.info(f"Session resumed after {paused_duration:.1f}s pause: {session_id}")
    
    async def end_session(self, session_id: str) -> Dict:
        """
        Mengakhiri session
        
        Args:
            session_id: ID sesi
            
        Returns:
            Dict dengan statistik session
        """
        if session_id not in self.sessions:
            return {}
        
        session = self.sessions[session_id]
        
        # Hitung total durasi
        if not session['is_paused']:
            last_segment = time.time() - session['last_message_time']
            session['total_duration'] += last_segment / 60
        
        result = {
            'session_id': session_id,
            'total_duration_minutes': round(session['total_duration'], 1),
            'effective_duration_minutes': round(session['effective_duration'], 1),
            'final_level': session['current_level'],
            'message_count': session['message_count'],
            'activities': session['activities'],
            'level_ups': session['level_up_messages']
        }
        
        del self.sessions[session_id]
        logger.info(f"Session ended: {session_id}")
        
        return result
    
    # =========================================================================
    # PROGRESS UPDATE
    # =========================================================================
    
    async def update_progress(self, 
                             session_id: str, 
                             activity_type: BoostType = BoostType.CHAT,
                             duration: float = None,
                             context: Dict = None) -> Dict:
        """
        Update progress berdasarkan aktivitas
        
        Args:
            session_id: ID sesi
            activity_type: Tipe aktivitas
            duration: Durasi aktivitas (None = auto dari last message)
            context: Konteks tambahan
            
        Returns:
            Dict dengan status leveling
        """
        if session_id not in self.sessions:
            return {'error': 'Session not found'}
        
        session = self.sessions[session_id]
        
        if session['is_paused']:
            return {'error': 'Session is paused'}
        
        now = time.time()
        
        # Hitung durasi sejak pesan terakhir
        if duration is None:
            duration = (now - session['last_message_time']) / 60
        
        # Batasi durasi maksimal per update (max 10 menit)
        duration = min(duration, 10.0)
        
        # Update total durasi
        session['total_duration'] += duration
        
        # Hitung durasi efektif dengan boost
        boost = self.activity_boost.base_multipliers.get(activity_type, 1.0)
        
        # Tambah bonus dari konteks
        if context:
            if context.get('is_intimate'):
                boost *= 1.2
            if context.get('mood') == 'excited':
                boost *= 1.1
            if context.get('climax'):
                boost *= 1.5
        
        effective_duration = duration * boost
        session['effective_duration'] += effective_duration
        
        # Update message count
        session['message_count'] += 1
        session['last_message_time'] = now
        
        # Catat aktivitas
        session['activities'].append(activity_type.value)
        session['activity_log'].append({
            'timestamp': now,
            'type': activity_type.value,
            'duration': duration,
            'boost': boost,
            'effective': effective_duration
        })
        
        # Cek level baru
        old_level = session['current_level']
        new_level = self._calculate_level(session['effective_duration'])
        
        level_up = False
        level_up_message = None
        
        if new_level > old_level:
            session['current_level'] = new_level
            level_up = True
            level_up_message = self._get_level_up_message(old_level, new_level, session['role'])
            
            session['level_up_messages'].append({
                'timestamp': now,
                'old_level': old_level,
                'new_level': new_level,
                'message': level_up_message
            })
            
            # Update cache
            cache_key = f"{session['user_id']}_{session['role']}"
            self.level_cache[cache_key] = (time.time(), new_level)
            
            logger.info(f"Level UP! {session_id}: {old_level} → {new_level}")
        
        return {
            'session_id': session_id,
            'old_level': old_level,
            'new_level': new_level,
            'level_up': level_up,
            'level_up_message': level_up_message,
            'total_duration': round(session['total_duration'], 1),
            'effective_duration': round(session['effective_duration'], 1),
            'progress_to_next': self._get_progress_to_next(session['effective_duration'], new_level),
            'next_level_in': self._get_time_to_next(session['effective_duration'], new_level),
            'activity': activity_type.value,
            'boost': boost
        }
    
    def _calculate_level(self, effective_minutes: float) -> int:
        """
        Hitung level berdasarkan durasi efektif
        
        Args:
            effective_minutes: Durasi efektif dalam menit
            
        Returns:
            Level 1-12
        """
        for level, target in sorted(self.time_targets.items()):
            if effective_minutes <= target:
                return level
        return 12
    
    def _get_progress_to_next(self, effective_minutes: float, current_level: int) -> float:
        """
        Hitung progress ke level berikutnya (0-100%)
        
        Args:
            effective_minutes: Durasi efektif
            current_level: Level saat ini
            
        Returns:
            Persentase progress
        """
        if current_level >= 12:
            return 100.0
        
        current_target = self.time_targets[current_level]
        next_target = self.time_targets[current_level + 1]
        
        progress = ((effective_minutes - current_target) / 
                   (next_target - current_target)) * 100
        
        return max(0, min(100, progress))
    
    def _get_time_to_next(self, effective_minutes: float, current_level: int) -> float:
        """
        Hitung waktu yang dibutuhkan ke level berikutnya (menit)
        
        Args:
            effective_minutes: Durasi efektif
            current_level: Level saat ini
            
        Returns:
            Menit yang dibutuhkan
        """
        if current_level >= 12:
            return 0
        
        next_target = self.time_targets[current_level + 1]
        return max(0, next_target - effective_minutes)
    
    def _get_level_up_message(self, old_level: int, new_level: int, role: str) -> str:
        """
        Dapatkan pesan level up
        
        Args:
            old_level: Level lama
            new_level: Level baru
            role: Nama role
            
        Returns:
            Pesan level up
        """
        old_name = self.level_names.get(old_level, f"Level {old_level}")
        new_name = self.level_names.get(new_level, f"Level {new_level}")
        
        messages = {
            7: f"🎉 **Level UP!** {old_name} → **{new_name}**\nSekarang kamu bisa intim dengan {role}!",
            11: f"🎉 **Level UP!** {old_name} → **{new_name}**\nKoneksi kalian semakin dalam...",
            12: f"🎉 **Level UP!** {old_name} → **{new_name}**\nButuh aftercare setelah ini ya..."
        }
        
        if new_level in messages:
            return messages[new_level]
        
        return f"📈 **Level UP!** {old_name} → **{new_name}**"
    
    # =========================================================================
    # GET STATUS
    # =========================================================================
    
    async def get_level(self, user_id: int, role: str, session_id: str = None) -> int:
        """
        Get current intimacy level
        
        Args:
            user_id: ID user
            role: Nama role
            session_id: ID session (opsional)
            
        Returns:
            Level (1-12)
        """
        cache_key = f"{user_id}_{role}"
        
        # Cek cache
        if cache_key in self.level_cache:
            cache_time, level = self.level_cache[cache_key]
            if time.time() - cache_time < self.cache_ttl:
                return level
        
        # Ambil dari session
        if session_id and session_id in self.sessions:
            level = self.sessions[session_id]['current_level']
            self.level_cache[cache_key] = (time.time(), level)
            return level
        
        return 1
    
    async def get_status(self, session_id: str) -> Optional[Dict]:
        """
        Dapatkan status leveling untuk session
        
        Args:
            session_id: ID sesi
            
        Returns:
            Dict status atau None
        """
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        level = session['current_level']
        effective = session['effective_duration']
        
        return {
            'session_id': session_id,
            'current_level': level,
            'level_name': self.level_names.get(level, f"Level {level}"),
            'description': self.level_descriptions.get(level, ""),
            'can_intim': level >= self.level_requirements["intim"],
            'total_duration': round(session['total_duration'], 1),
            'effective_duration': round(effective, 1),
            'progress': self._get_progress_to_next(effective, level),
            'next_level_in': self._get_time_to_next(effective, level),
            'message_count': session['message_count'],
            'activities': session['activities'][-10:],
            'is_paused': session['is_paused']
        }
    
    async def get_level_info(self, user_id: int, role: str, session_id: str = None) -> Dict:
        """
        Get detailed level info
        
        Args:
            user_id: ID user
            role: Nama role
            session_id: ID session (opsional)
            
        Returns:
            Dict dengan info level
        """
        current_level = await self.get_level(user_id, role, session_id)
        
        total_duration = 0
        effective_duration = 0
        progress = 0
        next_level_in = 0
        
        if session_id and session_id in self.sessions:
            session = self.sessions[session_id]
            total_duration = session['total_duration']
            effective_duration = session['effective_duration']
            progress = self._get_progress_to_next(effective_duration, current_level)
            next_level_in = self._get_time_to_next(effective_duration, current_level)
        
        return {
            "level": current_level,
            "name": self.level_names.get(current_level, "Unknown"),
            "description": self.level_descriptions.get(current_level, ""),
            "can_intim": current_level >= self.level_requirements["intim"],
            "total_duration": round(total_duration, 1),
            "effective_duration": round(effective_duration, 1),
            "progress_percentage": progress,
            "next_level_in": round(next_level_in, 1),
            "needs_aftercare": current_level == self.level_requirements["aftercare"]
        }
    
    # =========================================================================
    # RESET AFTER AFTERCARE
    # =========================================================================
    
    async def reset_after_aftercare(self, session_id: str) -> int:
        """
        Reset level setelah aftercare (Level 12 → Level 7)
        
        Args:
            session_id: ID sesi
            
        Returns:
            Level baru
        """
        if session_id not in self.sessions:
            return 1
        
        session = self.sessions[session_id]
        old_level = session['current_level']
        
        if old_level == 12:
            session['current_level'] = self.reset_level
            session['effective_duration'] = self.time_targets[self.reset_level]
            
            logger.info(f"Reset after aftercare: {session_id} 12 → {self.reset_level}")
            
            # Update cache
            cache_key = f"{session['user_id']}_{session['role']}"
            self.level_cache[cache_key] = (time.time(), self.reset_level)
            
            return self.reset_level
        
        return old_level
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    async def can_intim(self, user_id: int, role: str, session_id: str = None) -> bool:
        """
        Check if can have intimacy
        
        Args:
            user_id: ID user
            role: Nama role
            session_id: ID session (opsional)
            
        Returns:
            True jika bisa intim
        """
        level = await self.get_level(user_id, role, session_id)
        return level >= self.level_requirements["intim"]
    
    async def needs_aftercare(self, user_id: int, role: str, session_id: str = None) -> bool:
        """
        Check if needs aftercare
        
        Args:
            user_id: ID user
            role: Nama role
            session_id: ID session (opsional)
            
        Returns:
            True jika perlu aftercare
        """
        level = await self.get_level(user_id, role, session_id)
        return level == self.level_requirements["aftercare"]
    
    async def get_level_progress_bar(self, session_id: str, bar_length: int = 20) -> str:
        """
        Get progress bar untuk level
        
        Args:
            session_id: ID sesi
            bar_length: Panjang progress bar
            
        Returns:
            String progress bar
        """
        if session_id not in self.sessions:
            return "Session tidak ditemukan"
        
        session = self.sessions[session_id]
        level = session['current_level']
        progress = self._get_progress_to_next(session['effective_duration'], level)
        
        filled = int(progress / 100 * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        return bar
    
    def format_level_info(self, level_info: Dict) -> str:
        """
        Format level info untuk display
        
        Args:
            level_info: Hasil dari get_level_info()
            
        Returns:
            String formatted
        """
        lines = [
            f"Level {level_info['level']}: **{level_info['name']}**",
            f"_{level_info['description']}_",
            f"\nTotal Durasi: {level_info['total_duration']} menit",
            f"Durasi Efektif: {level_info['effective_duration']} menit"
        ]
        
        if level_info['can_intim']:
            lines.append("💕 **Bisa intim!**")
        
        if level_info['needs_aftercare']:
            lines.append("💝 **Butuh aftercare!**")
        
        if level_info['level'] < 12:
            bar_length = 20
            filled = int(level_info['progress_percentage'] / 100 * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)
            lines.append(f"\nProgress: {bar} {level_info['progress_percentage']}%")
            lines.append(f"{level_info['next_level_in']} menit lagi ke level {level_info['level'] + 1}")
        else:
            lines.append("\n✅ **Level MAX!** Butuh aftercare untuk reset.")
        
        return "\n".join(lines)
    
    def clear_cache(self):
        """Clear level cache"""
        self.level_cache.clear()
        logger.info("Intimacy cache cleared")


__all__ = ['IntimacySystem']
