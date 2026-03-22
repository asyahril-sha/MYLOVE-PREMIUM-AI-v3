#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - STATE TRACKER (VERSI HUMAN+)
=============================================================================
Melacak semua state dinamis dengan detail SUPER MANUSIA:
- Lokasi, pakaian, posisi tubuh
- Mood, gairah, status intim
- Aktivitas saat ini (dengan stack)
- Fisik detail (energi, lapar, haus, suhu)
- Semua perubahan tercatat dengan timestamp
- Multi-layer awareness
=============================================================================
"""

import time
import logging
import random
import math
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class StateType(str, Enum):
    """Tipe state yang dilacak"""
    LOCATION = "location"
    CLOTHING = "clothing"
    POSITION = "position"
    MOOD = "mood"
    AROUSAL = "arousal"
    ACTIVITY = "activity"
    INTIMACY = "intimacy"
    PRIVACY = "privacy"
    PHYSICAL = "physical"


class StateTracker:
    """
    Melacak semua state dinamis dengan kemampuan SUPER MANUSIA
    - Menyimpan history perubahan
    - Multi-layer awareness
    - Validasi perubahan yang masuk akal
    - Activity stack untuk multi-aktivitas
    - Physical tracking (energi, lapar, haus, suhu)
    """
    
    def __init__(self, user_id: int, session_id: str):
        """
        Args:
            user_id: ID user
            session_id: ID session
        """
        self.user_id = user_id
        self.session_id = session_id
        
        # ===== STATE SAAT INI (LENGKAP) =====
        self.current = {
            # ===== LOKASI =====
            'location': {
                'name': None,
                'category': None,
                'privacy_level': 1.0,
                'last_change': 0,
                'visited_before': [],
            },
            
            # ===== PAKAIAN =====
            'clothing': {
                'name': None,
                'category': None,
                'last_change': 0,
                'change_reason': None,
                'worn_before': [],
            },
            
            # ===== POSISI TUBUH =====
            'position': {
                'name': None,
                'description': None,
                'last_change': 0,
                'positions_today': [],
            },
            
            # ===== MOOD (MULTI-LAYER) =====
            'mood': {
                'primary': 'netral',
                'secondary': None,
                'tertiary': None,
                'intensity': 0.5,
                'last_change': 0,
                'history_today': [],
            },
            
            # ===== GAIRAH =====
            'arousal': {
                'level': 0,
                'last_change': 0,
                'peak_level': 0,
                'climax_count': 0,
                'arousal_today': [],
            },
            
            # ===== INTIMASI =====
            'intimacy': {
                'is_active': False,
                'start_time': None,
                'duration': 0,
                'last_activity': None,
                'positions_used': [],
                'climax_count': 0,
                'sessions_today': 0,
            },
            
            # ===== AKTIVITAS (DETAIL) =====
            'activity': {
                'name': None,
                'details': {},
                'start_time': None,
                'last_update': None,
                'progress': None,
                'status': 'idle',
                'interruptions': [],
            },
            
            # ===== ACTIVITY STACK =====
            'activity_stack': [],
            'paused_activities': [],
            
            # ===== FISIK (DETAIL) =====
            'physical': {
                'energy': {
                    'level': 80,
                    'feeling': 'energetic',
                    'last_change': time.time(),
                    'daily_peak': 80,
                    'daily_low': 80,
                },
                'hunger': {
                    'level': 30,
                    'feeling': 'normal',
                    'last_change': time.time(),
                    'last_meal': None,
                },
                'thirst': {
                    'level': 30,
                    'feeling': 'normal',
                    'last_change': time.time(),
                    'last_drink': None,
                },
                'temperature': {
                    'level': 25,
                    'feeling': 'normal',
                    'last_change': time.time(),
                },
                'comfort': {
                    'level': 80,
                    'feeling': 'comfortable',
                    'last_change': time.time(),
                },
            },
            
            # ===== INTERAKSI =====
            'interaction': {
                'last_user_message': None,
                'last_bot_response': None,
                'total_messages': 0,
                'messages_today': 0,
                'last_active': time.time(),
                'daily_active_periods': [],
            },
            
            # ===== AWARENESS =====
            'awareness': {
                'time_of_day': None,
                'day_of_week': None,
                'weather': None,
                'location_crowdedness': 0.5,
                'background_noise': 0.3,
            },
        }
        
        # ===== HISTORY PERUBAHAN =====
        self.history = {
            'location': [],
            'clothing': [],
            'position': [],
            'mood': [],
            'arousal': [],
            'activity': [],
            'intimacy': [],
            'physical': [],
        }
        
        # ===== STATISTIK HARIAN =====
        self.daily_stats = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'mood_distribution': {},
            'arousal_peaks': 0,
            'activity_count': 0,
            'location_changes': 0,
            'clothing_changes': 0,
        }
        
        # ===== RULE VALIDASI =====
        self.validation_rules = self._init_validation_rules()
        
        logger.info(f"✅ StateTracker HUMAN+ initialized for user {user_id}")
    
    def _init_validation_rules(self) -> Dict:
        """Inisialisasi rule validasi"""
        return {
            'location': {
                'min_time_between_change': 60,
                'max_changes_per_day': 20,
            },
            'clothing': {
                'require_reason': True,
                'valid_reasons': ['mandi', 'gerah', 'dingin', 'ganti baju', 'habis mandi', 
                                 'mau tidur', 'bangun tidur', 'buka baju', 'lepas baju',
                                 'olahraga', 'hujan', 'panas'],
                'min_time_between_change': 300,
                'max_changes_per_day': 10,
            },
            'position': {
                'min_time_between_change': 10,
                'max_changes_per_hour': 20,
                'max_changes_per_day': 100,
            },
            'arousal': {
                'max_increase_per_minute': 5,
                'max_decrease_per_minute': 3,
                'climax_cooldown': 300,
                'max_climax_per_day': 5,
            },
            'physical': {
                'energy_decay_per_hour': 5,
                'hunger_increase_per_hour': 3,
                'thirst_increase_per_hour': 2,
                'min_energy_for_activity': 20,
            },
        }
    
    # =========================================================================
    # ACTIVITY MANAGEMENT (MULTI-LAYER)
    # =========================================================================
    
    def start_activity(self, activity: str, details: Optional[Dict] = None):
        """Mulai aktivitas baru (push ke stack)"""
        now = time.time()
        
        # Simpan aktivitas sebelumnya ke stack
        if self.current['activity']['name']:
            self.current['activity_stack'].append({
                'name': self.current['activity']['name'],
                'details': self.current['activity']['details'].copy(),
                'start_time': self.current['activity']['start_time'],
                'progress': self.current['activity']['progress'],
                'interrupted_at': now,
                'reason': 'new_activity'
            })
            
            # Catat interupsi
            self.current['activity']['interruptions'].append({
                'time': now,
                'by': activity,
                'previous_activity': self.current['activity']['name']
            })
        
        # Set aktivitas baru
        old_activity = self.current['activity']['name']
        self.current['activity'] = {
            'name': activity,
            'details': details or {},
            'start_time': now,
            'last_update': now,
            'progress': None,
            'status': 'active',
            'interruptions': []
        }
        
        # Catat history
        self.history['activity'].append({
            'timestamp': now,
            'from': old_activity,
            'to': activity,
            'details': details,
            'type': 'start'
        })
        
        # Update daily stats
        self.daily_stats['activity_count'] += 1
        
        logger.info(f"📌 Activity started: {activity}")
    
    def pause_activity(self, reason: str = "pause"):
        """Pause aktivitas saat ini"""
        if self.current['activity']['name'] and self.current['activity']['status'] == 'active':
            self.current['activity']['status'] = 'paused'
            self.current['activity']['last_update'] = time.time()
            self.current['activity']['pause_reason'] = reason
            
            self.current['paused_activities'].append({
                'name': self.current['activity']['name'],
                'details': self.current['activity']['details'].copy(),
                'start_time': self.current['activity']['start_time'],
                'progress': self.current['activity']['progress'],
                'paused_at': time.time(),
                'reason': reason
            })
            
            self.history['activity'].append({
                'timestamp': time.time(),
                'from': self.current['activity']['name'],
                'to': None,
                'reason': reason,
                'type': 'pause'
            })
            
            logger.info(f"⏸️ Activity paused: {self.current['activity']['name']}")
    
    def resume_activity(self) -> bool:
        """Resume aktivitas terakhir yang di-pause"""
        if self.current['paused_activities']:
            last = self.current['paused_activities'].pop()
            
            pause_duration = time.time() - last['paused_at']
            
            last['status'] = 'active'
            last['last_update'] = time.time()
            last['resumed_at'] = time.time()
            last['pause_duration'] = pause_duration
            del last['paused_at']
            
            self.current['activity'] = last
            
            self.history['activity'].append({
                'timestamp': time.time(),
                'from': None,
                'to': last['name'],
                'type': 'resume',
                'pause_duration': pause_duration
            })
            
            logger.info(f"▶️ Activity resumed: {last['name']} (paused {pause_duration:.0f}s)")
            return True
        
        elif self.current['activity_stack']:
            last = self.current['activity_stack'].pop()
            last['status'] = 'active'
            last['last_update'] = time.time()
            last['resumed_at'] = time.time()
            
            self.current['activity'] = last
            
            self.history['activity'].append({
                'timestamp': time.time(),
                'from': None,
                'to': last['name'],
                'type': 'return_to_stack'
            })
            
            logger.info(f"↩️ Returned to activity: {last['name']}")
            return True
        
        return False
    
    def end_activity(self, completed: bool = True):
        """Akhiri aktivitas saat ini"""
        if self.current['activity']['name']:
            activity = self.current['activity']['name']
            duration = time.time() - (self.current['activity']['start_time'] or time.time())
            
            self.history['activity'].append({
                'timestamp': time.time(),
                'from': activity,
                'to': None,
                'duration': duration,
                'completed': completed,
                'type': 'end'
            })
            
            self.current['activity'] = {
                'name': None,
                'details': {},
                'start_time': None,
                'last_update': None,
                'progress': None,
                'status': 'idle',
                'interruptions': []
            }
            
            status = "selesai" if completed else "dibatalkan"
            logger.info(f"🏁 Activity ended: {activity} ({status})")
    
    def update_activity_progress(self, progress: str, details: Optional[Dict] = None):
        """Update progress aktivitas"""
        if self.current['activity']['name']:
            self.current['activity']['progress'] = progress
            self.current['activity']['last_update'] = time.time()
            
            if details:
                self.current['activity']['details'].update(details)
            
            logger.debug(f"📊 Activity progress: {progress}")
    
    def get_current_activity(self) -> Optional[Dict]:
        """Dapatkan aktivitas saat ini dengan durasi"""
        if self.current['activity']['name']:
            activity = self.current['activity'].copy()
            activity['duration'] = time.time() - (activity['start_time'] or time.time())
            return activity
        return None
    
    # =========================================================================
    # PHYSICAL TRACKING
    # =========================================================================
    
    def update_physical(self, category: str, delta: int, reason: str = ""):
        """Update kondisi fisik"""
        if category not in self.current['physical']:
            return
        
        phys = self.current['physical'][category]
        old_level = phys['level']
        
        if category in ['energy', 'hunger', 'thirst', 'comfort']:
            new_level = max(0, min(100, old_level + delta))
        else:
            new_level = old_level + delta
        
        phys['level'] = new_level
        phys['last_change'] = time.time()
        
        self._update_physical_feeling(category)
        
        if category == 'energy':
            if new_level > phys.get('daily_peak', 0):
                phys['daily_peak'] = new_level
            if new_level < phys.get('daily_low', 100):
                phys['daily_low'] = new_level
        
        self.history['physical'].append({
            'timestamp': time.time(),
            'category': category,
            'from': old_level,
            'to': new_level,
            'delta': delta,
            'reason': reason
        })
        
        logger.debug(f"📊 Physical {category}: {old_level} → {new_level}")
    
    def _update_physical_feeling(self, category: str):
        """Update feeling berdasarkan level"""
        phys = self.current['physical'][category]
        level = phys['level']
        
        if category == 'energy':
            if level > 70:
                phys['feeling'] = 'energetic'
            elif level > 40:
                phys['feeling'] = 'normal'
            elif level > 20:
                phys['feeling'] = 'tired'
            else:
                phys['feeling'] = 'exhausted'
        
        elif category == 'hunger':
            if level > 70:
                phys['feeling'] = 'very_hungry'
            elif level > 40:
                phys['feeling'] = 'hungry'
            else:
                phys['feeling'] = 'normal'
        
        elif category == 'thirst':
            if level > 70:
                phys['feeling'] = 'very_thirsty'
            elif level > 40:
                phys['feeling'] = 'thirsty'
            else:
                phys['feeling'] = 'normal'
        
        elif category == 'temperature':
            if level < 20:
                phys['feeling'] = 'cold'
            elif level > 30:
                phys['feeling'] = 'hot'
            else:
                phys['feeling'] = 'normal'
        
        elif category == 'comfort':
            if level > 70:
                phys['feeling'] = 'comfortable'
            else:
                phys['feeling'] = 'uncomfortable'
    
    def natural_decay(self, hours: float):
        """Natural decay fisik berdasarkan waktu berlalu"""
        decay = hours * self.validation_rules['physical']['energy_decay_per_hour']
        self.update_physical('energy', -decay, 'natural_decay')
        
        increase = hours * self.validation_rules['physical']['hunger_increase_per_hour']
        self.update_physical('hunger', increase, 'natural_decay')
        
        increase = hours * self.validation_rules['physical']['thirst_increase_per_hour']
        self.update_physical('thirst', increase, 'natural_decay')
    
    # =========================================================================
    # LOCATION, CLOTHING, POSITION TRACKING
    # =========================================================================
    
    def update_location(self, name: str, category: str = "private") -> Tuple[bool, str]:
        """Update lokasi saat ini"""
        old_name = self.current['location']['name']
        
        last_change = self.current['location']['last_change']
        if time.time() - last_change < self.validation_rules['location']['min_time_between_change']:
            return False, f"Masih di {old_name}, tunggu bentar"
        
        self.current['location'] = {
            'name': name,
            'category': category,
            'last_change': time.time(),
            'visited_before': self.current['location'].get('visited_before', []) + [name]
        }
        
        if category == 'intimate':
            self.current['location']['privacy_level'] = 0.9
        elif category == 'public':
            self.current['location']['privacy_level'] = 0.3
        else:
            self.current['location']['privacy_level'] = 0.6
        
        self.history['location'].append({
            'timestamp': time.time(),
            'from': old_name,
            'to': name,
            'category': category
        })
        
        self.daily_stats['location_changes'] += 1
        
        logger.debug(f"📍 Location updated: {old_name} → {name}")
        return True, f"Pindah ke {name}"
    
    def update_clothing(self, name: str, reason: str = "ganti baju") -> Tuple[bool, str]:
        """Update pakaian"""
        old_name = self.current['clothing']['name']
        
        if not reason or not any(r in reason.lower() for r in self.validation_rules['clothing']['valid_reasons']):
            return False, "Ganti baju harus ada alasannya"
        
        last_change = self.current['clothing']['last_change']
        if time.time() - last_change < self.validation_rules['clothing']['min_time_between_change']:
            return False, "Baru aja ganti baju"
        
        self.current['clothing'] = {
            'name': name,
            'last_change': time.time(),
            'change_reason': reason,
            'worn_before': self.current['clothing'].get('worn_before', []) + [name]
        }
        
        self.history['clothing'].append({
            'timestamp': time.time(),
            'from': old_name,
            'to': name,
            'reason': reason
        })
        
        self.daily_stats['clothing_changes'] += 1
        
        logger.debug(f"👗 Clothing updated: {old_name} → {name}")
        return True, f"Ganti {name}"
    
    def update_position(self, name: str, description: str = "") -> Tuple[bool, str]:
        """Update posisi tubuh"""
        old_name = self.current['position']['name']
        
        last_change = self.current['position']['last_change']
        if time.time() - last_change < self.validation_rules['position']['min_time_between_change']:
            return False, "Kebanyakan gerak, santai dulu"
        
        last_hour = time.time() - 3600
        changes_last_hour = [h for h in self.history['position'] if h['timestamp'] > last_hour]
        if len(changes_last_hour) > self.validation_rules['position']['max_changes_per_hour']:
            return False, "Sering banget ganti posisi"
        
        self.current['position'] = {
            'name': name,
            'description': description,
            'last_change': time.time(),
            'positions_today': self.current['position'].get('positions_today', []) + [name]
        }
        
        self.history['position'].append({
            'timestamp': time.time(),
            'from': old_name,
            'to': name
        })
        
        return True, f"Ganti posisi jadi {name}"
    
    # =========================================================================
    # MOOD TRACKING
    # =========================================================================
    
    def update_mood(self, primary: str, secondary: Optional[str] = None,
                    tertiary: Optional[str] = None, intensity: float = 0.5,
                    reason: str = ""):
        """Update mood (bisa multi-layer)"""
        old_primary = self.current['mood']['primary']
        
        self.current['mood'] = {
            'primary': primary,
            'secondary': secondary,
            'tertiary': tertiary,
            'intensity': intensity,
            'last_change': time.time(),
            'history_today': self.current['mood'].get('history_today', []) + [primary]
        }
        
        self.history['mood'].append({
            'timestamp': time.time(),
            'from': old_primary,
            'to': primary,
            'secondary': secondary,
            'intensity': intensity,
            'reason': reason
        })
        
        self.daily_stats['mood_distribution'][primary] = \
            self.daily_stats['mood_distribution'].get(primary, 0) + 1
        
        logger.debug(f"🎭 Mood changed: {old_primary} → {primary}")
    
    # =========================================================================
    # AROUSAL TRACKING
    # =========================================================================
    
    def update_arousal(self, delta: int, reason: str = "") -> Tuple[bool, str]:
        """Update level gairah"""
        old_level = self.current['arousal']['level']
        new_level = max(0, min(10, old_level + delta))
        
        if delta < 0 and old_level >= 8:
            last_climax = None
            for h in reversed(self.history['intimacy']):
                if h.get('type') == 'climax':
                    last_climax = h['timestamp']
                    break
            
            if last_climax and time.time() - last_climax < self.validation_rules['arousal']['climax_cooldown']:
                return False, "Selesai climax, butuh istirahat dulu"
        
        if delta >= 3 and old_level >= 7:
            if self.daily_stats['arousal_peaks'] >= self.validation_rules['arousal']['max_climax_per_day']:
                return False, "Hari ini sudah terlalu banyak climax"
        
        self.current['arousal']['level'] = new_level
        self.current['arousal']['last_change'] = time.time()
        
        if new_level > self.current['arousal']['peak_level']:
            self.current['arousal']['peak_level'] = new_level
        
        if delta >= 3 and old_level >= 7:
            self.current['arousal']['climax_count'] += 1
            self.current['intimacy']['climax_count'] += 1
            self.daily_stats['arousal_peaks'] += 1
            
            self.history['intimacy'].append({
                'timestamp': time.time(),
                'type': 'climax',
                'level': old_level,
                'intensity': new_level
            })
        
        if new_level >= 7 and not self.current['intimacy']['is_active']:
            self.start_intimacy()
        elif new_level < 7 and self.current['intimacy']['is_active']:
            self.end_intimacy()
        
        self.current['arousal']['arousal_today'].append({
            'time': time.time(),
            'level': new_level,
            'delta': delta
        })
        
        self.history['arousal'].append({
            'timestamp': time.time(),
            'from': old_level,
            'to': new_level,
            'delta': delta,
            'reason': reason
        })
        
        return True, f"Arousal: {old_level} → {new_level}"
    
    def start_intimacy(self):
        """Mulai sesi intim"""
        if not self.current['intimacy']['is_active']:
            self.current['intimacy']['is_active'] = True
            self.current['intimacy']['start_time'] = time.time()
            self.current['intimacy']['sessions_today'] += 1
            
            self.history['intimacy'].append({
                'timestamp': time.time(),
                'type': 'start'
            })
            
            logger.info("💕 Intimacy started")
    
    def end_intimacy(self):
        """Akhiri sesi intim"""
        if self.current['intimacy']['is_active']:
            duration = time.time() - self.current['intimacy']['start_time']
            self.current['intimacy']['is_active'] = False
            self.current['intimacy']['duration'] += duration
            self.current['intimacy']['start_time'] = None
            
            self.history['intimacy'].append({
                'timestamp': time.time(),
                'type': 'end',
                'duration': duration
            })
            
            logger.info(f"💕 Intimacy ended ({duration:.0f}s)")
    
    def add_intimacy_position(self, position: str):
        """Tambah posisi yang digunakan saat intim"""
        if position not in self.current['intimacy']['positions_used']:
            self.current['intimacy']['positions_used'].append(position)
    
    # =========================================================================
    # INTERACTION TRACKING
    # =========================================================================
    
    def register_interaction(self, user_message: str, bot_response: str):
        """Catat interaksi"""
        now = time.time()
        
        self.current['interaction']['last_user_message'] = user_message
        self.current['interaction']['last_bot_response'] = bot_response
        self.current['interaction']['total_messages'] += 1
        self.current['interaction']['messages_today'] += 1
        self.current['interaction']['last_active'] = now
    
    # =========================================================================
    # GETTERS
    # =========================================================================
    
    def get_current_state(self):
        # Cek tipe data location
        location_data = self.current.get('location')
    
        if isinstance(location_data, dict):
            location_name = location_data.get('name', 'Tidak diketahui')
            location_category = location_data.get('category', 'unknown')
        else:
            # Jika location adalah string, gunakan langsung
            location_name = str(location_data) if location_data else 'Tidak diketahui'
            location_category = 'unknown'
    
        return {
            'location': location_name,
            'location_category': location_category,
            'privacy_level': self.current.get('privacy_level', 0.5),
            'clothing': self.current.get('clothing', {}).get('name') if isinstance(self.current.get('clothing'), dict) else self.current.get('clothing'),
            'position': self.current.get('position', {}).get('name') if isinstance(self.current.get('position'), dict) else self.current.get('position'),
            'position_desc': self.current.get('position', {}).get('description') if isinstance(self.current.get('position'), dict) else str(self.current.get('position')),
            'mood': self.current.get('mood', {}).get('primary') if isinstance(self.current.get('mood'), dict) else self.current.get('mood'),
            'mood_secondary': self.current.get('mood', {}).get('secondary') if isinstance(self.current.get('mood'), dict) else None,
            'mood_intensity': self.current.get('mood', {}).get('intensity', 0.5) if isinstance(self.current.get('mood'), dict) else 0.5,
            'arousal': self.current.get('arousal', {}).get('level', 0) if isinstance(self.current.get('arousal'), dict) else self.current.get('arousal', 0),
            'is_intimate': self.current.get('intimacy', {}).get('is_active', False) if isinstance(self.current.get('intimacy'), dict) else False,
            'activity': self.current.get('activity', {}).get('name') if isinstance(self.current.get('activity'), dict) else self.current.get('activity'),
            'activity_details': self.current.get('activity', {}).get('details', {}) if isinstance(self.current.get('activity'), dict) else {},
            'activity_status': self.current.get('activity', {}).get('status', 'idle') if isinstance(self.current.get('activity'), dict) else 'idle',
            'energy': self.current.get('physical', {}).get('energy', {}).get('feeling', 'normal') if isinstance(self.current.get('physical'), dict) else 'normal',
            'hunger': self.current.get('physical', {}).get('hunger', {}).get('feeling', 'normal') if isinstance(self.current.get('physical'), dict) else 'normal',
            'thirst': self.current.get('physical', {}).get('thirst', {}).get('feeling', 'normal') if isinstance(self.current.get('physical'), dict) else 'normal',
            'temperature': self.current.get('physical', {}).get('temperature', {}).get('feeling', 'normal') if isinstance(self.current.get('physical'), dict) else 'normal',
            'comfort': self.current.get('physical', {}).get('comfort', {}).get('feeling', 'normal') if isinstance(self.current.get('physical'), dict) else 'normal',
            'total_messages': self.current.get('interaction', {}).get('total_messages', 0) if isinstance(self.current.get('interaction'), dict) else 0,
            'idle_seconds': time.time() - self.current.get('interaction', {}).get('last_active', time.time()) if isinstance(self.current.get('interaction'), dict) else 0
        }
    
    def _get_time_of_day(self) -> str:
        """Dapatkan waktu dalam string"""
        hour = datetime.now().hour
        if 5 <= hour < 11:
            return 'pagi'
        elif 11 <= hour < 15:
            return 'siang'
        elif 15 <= hour < 18:
            return 'sore'
        else:
            return 'malam'
    
    def get_state_for_prompt(self) -> str:
        """Format state untuk prompt AI"""
        state = self.get_current_state()
        
        parts = []
        
        if state['location']:
            parts.append(f"di {state['location']}")
        
        if state['clothing']:
            parts.append(f"pakai {state['clothing']}")
        
        if state['position_desc']:
            parts.append(f"lagi {state['position_desc']}")
        
        if state['activity']:
            parts.append(f"sedang {state['activity']}")
        
        parts.append(f"mood {state['mood']}")
        
        if state['energy'] != 'energetic':
            parts.append(f"energi {state['energy']}")
        
        return "lagi " + ", ".join(parts) if parts else "santai"
    
    def get_state_summary(self) -> str:
        """Dapatkan ringkasan state"""
        activity = self.get_current_activity()
        activity_text = f"{activity['name']} ({activity['duration']:.0f}s)" if activity else "tidak ada"
        
        lines = [
            "📊 **STATE SAAT INI:**",
            f"📍 Lokasi: {self.current['location']['name'] or '?'}",
            f"👕 Pakaian: {self.current['clothing']['name'] or '?'}",
            f"🧍 Posisi: {self.current['position']['description'] or self.current['position']['name'] or '?'}",
            f"🎭 Mood: {self.current['mood']['primary']}",
            f"🔥 Gairah: {self.current['arousal']['level']}/10",
            f"💕 Intim: {'Ya' if self.current['intimacy']['is_active'] else 'Tidak'}",
            f"🎯 Aktivitas: {activity_text}",
            f"🔋 Energi: {self.current['physical']['energy']['feeling']}",
            f"🍽️ Lapar: {self.current['physical']['hunger']['feeling']}",
            f"💧 Haus: {self.current['physical']['thirst']['feeling']}",
            f"💬 Total chat: {self.current['interaction']['total_messages']}"
        ]
        
        return "\n".join(lines)
    
    def get_timeline(self, limit: int = 20) -> List[Dict]:
        """Dapatkan timeline semua perubahan"""
        timeline = []
        
        for state_type, events in self.history.items():
            for event in events[-limit:]:
                timeline.append({
                    'time': event['timestamp'],
                    'type': state_type,
                    'data': event
                })
        
        timeline.sort(key=lambda x: x['time'], reverse=True)
        return timeline[:limit]
    
    def format_timeline(self, limit: int = 10) -> str:
        """Format timeline untuk ditampilkan"""
        timeline = self.get_timeline(limit)
        
        if not timeline:
            return "Belum ada perubahan"
        
        lines = ["📜 **TIMELINE PERUBAHAN:**"]
        
        for t in timeline:
            time_str = datetime.fromtimestamp(t['time']).strftime("%H:%M:%S")
            data = t['data']
            
            if t['type'] == 'location':
                lines.append(f"• [{time_str}] Lokasi: {data['from']} → {data['to']}")
            elif t['type'] == 'clothing':
                lines.append(f"• [{time_str}] Baju: {data['from']} → {data['to']} ({data['reason']})")
            elif t['type'] == 'position':
                lines.append(f"• [{time_str}] Posisi: {data['from']} → {data['to']}")
            elif t['type'] == 'mood':
                lines.append(f"• [{time_str}] Mood: {data['from']} → {data['to']}")
            elif t['type'] == 'arousal':
                lines.append(f"• [{time_str}] Gairah: {data['from']} → {data['to']}")
            elif t['type'] == 'activity':
                if data.get('to'):
                    lines.append(f"• [{time_str}] Aktivitas: {data['from']} → {data['to']}")
                else:
                    lines.append(f"• [{time_str}] {data['from']} {data.get('type', '')}")
            elif t['type'] == 'intimacy':
                if data['type'] == 'start':
                    lines.append(f"• [{time_str}] 🔥 Mulai intim")
                elif data['type'] == 'end':
                    lines.append(f"• [{time_str}] 💤 Selesai intim ({data.get('duration', 0):.0f}s)")
                elif data['type'] == 'climax':
                    lines.append(f"• [{time_str}] 💦 Climax!")
        
        return "\n".join(lines)
    
    def reset_daily_stats(self):
        """Reset statistik harian"""
        self.daily_stats = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'mood_distribution': {},
            'arousal_peaks': 0,
            'activity_count': 0,
            'location_changes': 0,
            'clothing_changes': 0,
        }
        logger.info("📅 Daily stats reset")


__all__ = ['StateTracker', 'StateType']
