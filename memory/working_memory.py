#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - WORKING MEMORY (VERSI HUMAN+)
=============================================================================
Ingatan jangka pendek SUPER MANUSIA (24 jam):
- Menyimpan 20±5 item terakhir (lebih banyak dari manusia)
- State saat ini (lokasi, baju, mood, aktivitas)
- Auto-expire setelah waktu tertentu
- Tracking aktivitas berkelanjutan
- Multiple state parallel (bisa ingat beberapa hal sekaligus)
=============================================================================
"""

import time
import logging
from typing import Dict, List, Optional, Any, Union
from collections import deque
from datetime import datetime

logger = logging.getLogger(__name__)


class WorkingMemory:
    """
    Working memory - ingatan jangka pendek SUPER MANUSIA
    Kapasitas lebih besar, expire lebih lama, tracking lebih detail
    """
    
    def __init__(self, capacity: int = 20, expire_seconds: int = 86400):
        """
        Args:
            capacity: Jumlah item yang bisa diingat (default 20, manusia 7±2)
            expire_seconds: Waktu expire dalam detik (default 24 jam)
        """
        self.capacity = capacity
        self.expire_seconds = expire_seconds
        
        # ===== ITEMS DALAM WORKING MEMORY =====
        self.items = deque(maxlen=capacity)
        
        # ===== STATE SAAT INI (SELALU DIINGAT) =====
        self.current_state = {
            # ===== LOKASI =====
            'location': None,
            'location_history': [],
            'last_location_change': 0,
            'location_category': None,
            
            # ===== PAKAIAN =====
            'clothing': None,
            'clothing_history': [],
            'last_clothing_change': 0,
            'clothing_reason': None,
            
            # ===== POSISI TUBUH =====
            'position': None,
            'position_history': [],
            'last_position_change': 0,
            'position_description': None,
            
            # ===== AKTIVITAS =====
            'activity': None,
            'activity_history': [],
            'activity_start_time': None,
            'activity_details': {},
            
            # ===== MOOD & PERASAAN =====
            'mood': 'netral',
            'mood_history': [],
            'mood_intensity': 0.5,
            'mood_reason': None,
            
            # ===== GAIRAH =====
            'arousal_level': 0,
            'arousal_history': [],
            'last_arousal_change': 0,
            'is_intimate': False,
            'intimate_start_time': None,
            
            # ===== INTERAKSI =====
            'last_user_message': None,
            'last_bot_response': None,
            'last_response_time': 0,
            'last_interaction': time.time(),
            'total_messages_today': 0,
            
            # ===== KONTEKS =====
            'with_user': True,
            'privacy_level': 1.0,  # 0 (rame) - 1 (sepi)
            'time_of_day': None,
            
            # ===== IDENTITAS BOT =====
            'bot_name': None,
            'role': None,
            'rel_type': None,
            'instance_id': None,
            
            # ===== AKTIVITAS BERKELANJUTAN =====
            'current_activity': {
                'name': None,
                'details': {},
                'start_time': None,
                'last_update': None,
                'progress': None,
                'status': 'idle'  # idle, active, paused, completed
            },

            # ===== UNIVERSAL ACTIVITY TRACKER =====
            'current_activity_universal': None,
            'activity_history': [],
        }
        
        # ===== TIMELINE =====
        self.timeline = deque(maxlen=50)
        
        # ===== DAFTAR SEMUA AKTIVITAS =====
        self.ACTIVITY_TYPES = {
            'going_out': {'name': 'pergi', 'steps': ['bersiap', 'ganti_baju', 'berangkat', 'di_jalan', 'sampai']},
            'preparing': {'name': 'persiapan', 'steps': ['mulai', 'sedang', 'hampir_selesai', 'selesai']},
            'eating': {'name': 'makan', 'steps': ['masak', 'siap_saji', 'makan', 'selesai']},
            'drinking': {'name': 'minum', 'steps': ['buat', 'saji', 'minum', 'habis']},
            'sleeping': {'name': 'tidur', 'steps': ['mau_tidur', 'tidur', 'bangun']},
            'working': {'name': 'kerja', 'steps': ['mulai_kerja', 'sedang_kerja', 'istirahat', 'selesai']},
            'studying': {'name': 'belajar', 'steps': ['mulai_belajar', 'sedang_belajar', 'selesai']},
            'cleaning': {'name': 'bersih-bersih', 'steps': ['mulai', 'sedang', 'selesai']},
            'entertainment': {'name': 'hiburan', 'steps': ['mulai', 'sedang', 'selesai']},
            'intimate': {'name': 'intim', 'steps': ['mulai', 'foreplay', 'main', 'climax', 'aftercare']},
            'waiting': {'name': 'menunggu', 'steps': ['mulai_menunggu', 'menunggu', 'selesai']},
            'traveling': {'name': 'perjalanan', 'steps': ['berangkat', 'di_jalan', 'hampir_sampai', 'sampai']}
        }
        
        # ===== ACTION TRACKING =====
        self.action_timeline = deque(maxlen=50)
        
        logger.info(f"✅ WorkingMemory HUMAN+ initialized (capacity: {capacity}, expire: {expire_seconds}s)")
    
    # =========================================================================
    # METHOD UNTUK AKTIVITAS BERKELANJUTAN
    # =========================================================================
    
    def start_activity(self, activity: str, details: Optional[Dict] = None):
        """
        Mulai aktivitas baru
        """
        now = time.time()
        
        # Simpan aktivitas sebelumnya ke history
        if self.current_state['current_activity']['name']:
            self.current_state['activity_history'].append({
                'name': self.current_state['current_activity']['name'],
                'details': self.current_state['current_activity']['details'],
                'start_time': self.current_state['current_activity']['start_time'],
                'end_time': now,
                'duration': now - (self.current_state['current_activity']['start_time'] or now)
            })
        
        # Push ke stack
        if self.current_state['current_activity']['name']:
            self.current_state['activity_stack'].append(
                self.current_state['current_activity'].copy()
            )
        
        # Set aktivitas baru
        self.current_state['current_activity'] = {
            'name': activity,
            'details': details or {},
            'start_time': now,
            'last_update': now,
            'progress': None,
            'status': 'active'
        }
        
        # Update juga field activity
        self.current_state['activity'] = activity
        self.current_state['activity_details'] = details or {}
        self.current_state['activity_start_time'] = now
        
        # Catat di timeline
        self._add_to_timeline('activity_start', f"Mulai {activity}")
        
        logger.debug(f"🎯 Activity started: {activity}")
    
    def pause_activity(self, reason: str = "pause"):
        """
        Pause aktivitas saat ini
        """
        if self.current_state['current_activity']['name']:
            self.current_state['current_activity']['status'] = 'paused'
            self.current_state['current_activity']['last_update'] = time.time()
            self.current_state['current_activity']['pause_reason'] = reason
            
            self.current_state['paused_activities'].append(
                self.current_state['current_activity'].copy()
            )
            
            self._add_to_timeline('activity_pause', 
                                 f"Pause {self.current_state['current_activity']['name']}")
            
            logger.debug(f"⏸️ Activity paused: {self.current_state['current_activity']['name']}")
    
    def resume_activity(self) -> bool:
        """
        Resume aktivitas terakhir yang di-pause
        """
        if self.current_state['paused_activities']:
            last = self.current_state['paused_activities'].pop()
            last['status'] = 'active'
            last['last_update'] = time.time()
            last['resumed_at'] = time.time()
            
            self.current_state['current_activity'] = last
            
            self._add_to_timeline('activity_resume', 
                                 f"Resume {last['name']}")
            
            logger.debug(f"▶️ Activity resumed: {last['name']}")
            return True
        
        elif self.current_state['activity_stack']:
            # Kembali ke aktivitas sebelumnya di stack
            last = self.current_state['activity_stack'].pop()
            last['status'] = 'active'
            last['last_update'] = time.time()
            
            self.current_state['current_activity'] = last
            
            self._add_to_timeline('activity_resume', 
                                 f"Kembali ke {last['name']}")
            
            logger.debug(f"↩️ Returned to activity: {last['name']}")
            return True
        
        return False
    
    def end_activity(self, completed: bool = True):
        """
        Akhiri aktivitas saat ini
        """
        if self.current_state['current_activity']['name']:
            activity = self.current_state['current_activity']['name']
            duration = time.time() - (self.current_state['current_activity']['start_time'] or time.time())
            
            # Catat ke history
            self.current_state['activity_history'].append({
                'name': activity,
                'details': self.current_state['current_activity']['details'],
                'start_time': self.current_state['current_activity']['start_time'],
                'end_time': time.time(),
                'duration': duration,
                'completed': completed
            })
            
            # Reset current activity
            self.current_state['current_activity'] = {
                'name': None,
                'details': {},
                'start_time': None,
                'last_update': None,
                'progress': None,
                'status': 'idle'
            }
            
            self.current_state['activity'] = None
            self.current_state['activity_details'] = {}
            self.current_state['activity_start_time'] = None
            
            status = "selesai" if completed else "dibatalkan"
            self._add_to_timeline('activity_end', f"{activity} {status}")
            
            logger.debug(f"🏁 Activity ended: {activity}")
    
    def update_activity_progress(self, progress: str, details: Optional[Dict] = None):
        """
        Update progress aktivitas
        """
        if self.current_state['current_activity']['name']:
            self.current_state['current_activity']['progress'] = progress
            self.current_state['current_activity']['last_update'] = time.time()
            
            if details:
                self.current_state['current_activity']['details'].update(details)
    
    def get_current_activity(self) -> Optional[Dict]:
        """
        Dapatkan aktivitas saat ini
        """
        if self.current_state['current_activity']['name']:
            activity = self.current_state['current_activity'].copy()
            if activity['start_time']:
                activity['duration'] = time.time() - activity['start_time']
            return activity
        return None
    
    # =========================================================================
    # METHOD UNTUK PARALLEL STATE TRACKING
    # =========================================================================
    
    def set_parallel_state(self, category: str, key: str, value: Any):
        """
        Set state paralel (untuk tracking beberapa hal sekaligus)
        """
        if category not in self.current_state['parallel_states']:
            self.current_state['parallel_states'][category] = {}
        
        self.current_state['parallel_states'][category][key] = {
            'value': value,
            'timestamp': time.time()
        }
    
    def get_parallel_state(self, category: str, key: str) -> Optional[Any]:
        """
        Get state paralel
        """
        if category in self.current_state['parallel_states']:
            if key in self.current_state['parallel_states'][category]:
                return self.current_state['parallel_states'][category][key]['value']
        return None
    
    def get_all_parallel(self, category: str) -> Dict:
        """
        Get semua state dalam kategori paralel
        """
        return self.current_state['parallel_states'].get(category, {})
    
    # =========================================================================
    # UPDATE METHODS UNTUK SETIAP ASPEK
    # =========================================================================
    
    def update_location(self, location: str, category: str = "private"):
        """Update lokasi dan catat history"""
        old_location = self.current_state['location']
        
        self.current_state['location'] = location
        self.current_state['location_category'] = category
        self.current_state['last_location_change'] = time.time()
        
        # Simpan ke history
        self.current_state['location_history'].append({
            'time': time.time(),
            'from': old_location,
            'to': location,
            'category': category
        })
        
        # Update privacy level
        if category == 'intimate':
            self.current_state['privacy_level'] = 0.9
        elif category == 'public':
            self.current_state['privacy_level'] = 0.3
        else:
            self.current_state['privacy_level'] = 0.6
        
        # Catat di timeline
        self._add_to_timeline('location_change', f"{old_location} → {location}")
        
        logger.debug(f"📍 Location updated: {old_location} → {location}")
    
    def update_clothing(self, clothing: str, reason: str = "ganti baju"):
        """Update pakaian dan catat history"""
        old_clothing = self.current_state['clothing']
        
        self.current_state['clothing'] = clothing
        self.current_state['clothing_reason'] = reason
        self.current_state['last_clothing_change'] = time.time()
        
        # Simpan ke history
        self.current_state['clothing_history'].append({
            'time': time.time(),
            'from': old_clothing,
            'to': clothing,
            'reason': reason
        })
        
        # Catat di timeline
        self._add_to_timeline('clothing_change', f"{old_clothing} → {clothing} ({reason})")
        
        logger.debug(f"👗 Clothing updated: {old_clothing} → {clothing}")
    
    def update_position(self, position: str, description: str = ""):
        """Update posisi tubuh"""
        old_position = self.current_state['position']
        
        self.current_state['position'] = position
        self.current_state['position_description'] = description or position
        self.current_state['last_position_change'] = time.time()
        
        # Simpan ke history
        self.current_state['position_history'].append({
            'time': time.time(),
            'from': old_position,
            'to': position,
            'description': description
        })
        
        self._add_to_timeline('position_change', f"{old_position} → {position}")
        
        logger.debug(f"🧍 Position updated: {old_position} → {position}")
    
    def update_mood(self, mood: str, intensity: float = 0.5, reason: str = ""):
        """Update mood"""
        old_mood = self.current_state['mood']
        
        self.current_state['mood'] = mood
        self.current_state['mood_intensity'] = intensity
        self.current_state['mood_reason'] = reason
        
        self.current_state['mood_history'].append({
            'time': time.time(),
            'from': old_mood,
            'to': mood,
            'intensity': intensity,
            'reason': reason
        })
        
        self._add_to_timeline('mood_change', f"{old_mood} → {mood}")
        
        logger.debug(f"🎭 Mood updated: {old_mood} → {mood}")
    
    def update_arousal(self, delta: int, reason: str = ""):
        """Update level gairah"""
        old_arousal = self.current_state['arousal_level']
        new_arousal = max(0, min(10, old_arousal + delta))
        
        self.current_state['arousal_level'] = new_arousal
        self.current_state['last_arousal_change'] = time.time()
        
        self.current_state['arousal_history'].append({
            'time': time.time(),
            'from': old_arousal,
            'to': new_arousal,
            'delta': delta,
            'reason': reason
        })
        
        if abs(new_arousal - old_arousal) >= 2:
            self._add_to_timeline('arousal_change', f"{old_arousal} → {new_arousal}")
        
        logger.debug(f"🔥 Arousal updated: {old_arousal} → {new_arousal}")
    
    def start_intimacy(self):
        """Mulai sesi intim"""
        self.current_state['is_intimate'] = True
        self.current_state['intimate_start_time'] = time.time()
        self.current_state['arousal_level'] = max(7, self.current_state['arousal_level'])
        
        self._add_to_timeline('intimacy_start', 'Mulai intim')
        logger.info("💕 Intimacy started")
    
    def end_intimacy(self):
        """Akhiri sesi intim"""
        self.current_state['is_intimate'] = False
        self.current_state['intimate_start_time'] = None
        
        self._add_to_timeline('intimacy_end', 'Selesai intim')
        logger.info("💕 Intimacy ended")
    
    def add_interaction(self, user_message: str, bot_response: str, context: Dict):
        """Simpan interaksi ke working memory"""
        now = time.time()
        
        self.current_state['last_user_message'] = user_message
        self.current_state['last_bot_response'] = bot_response
        self.current_state['last_response_time'] = now
        self.current_state['last_interaction'] = now
        self.current_state['total_messages_today'] += 1
        
        self.items.append({
            'time': now,
            'user': user_message[:100],
            'bot': bot_response[:100],
            'context': context
        })
        
        self._add_to_timeline('interaction', f"User: {user_message[:50]}...")
    
    def set_last_bot_response(self, response: str):
        """Simpan respons terakhir"""
        self.current_state['last_bot_response'] = response
        self.current_state['last_response_time'] = time.time()
    
    def get_last_bot_response(self) -> Optional[str]:
        """Dapatkan respons terakhir"""
        return self.current_state.get('last_bot_response')
    
    # =========================================================================
    # TIMELINE MANAGEMENT
    # =========================================================================
    
    def _add_to_timeline(self, event_type: str, data: str):
        """Tambahkan ke timeline"""
        self.timeline.append({
            'time': time.time(),
            'type': event_type,
            'data': data
        })
    
    def get_timeline(self, limit: int = 20) -> List[Dict]:
        """Dapatkan timeline"""
        return list(self.timeline)[-limit:]
    
    # =========================================================================
    # GET RECENT CONTEXT
    # =========================================================================
    
    def get_recent_context(self, seconds: int = 43200) -> Dict:
        """
        Dapatkan konteks dari beberapa detik terakhir
        Default: 12 jam (43200 detik)
        
        Args:
            seconds: Jumlah detik ke belakang (default 12 jam)
        
        Returns:
            Dict berisi konteks recent
        """
        cutoff = time.time() - seconds
        recent_items = [i for i in self.items if i['time'] > cutoff]
        recent_timeline = [t for t in self.timeline if t['time'] > cutoff]
        
        current_activity = self.get_current_activity()
        
        return {
            'current_state': self.get_current_state(),
            'recent_interactions': len(recent_items),
            'recent_timeline': recent_timeline[-10:],
            'current_activity': current_activity,
            'location': self.current_state['location'],
            'clothing': self.current_state['clothing'],
            'mood': self.current_state['mood'],
            'arousal': self.current_state['arousal_level'],
            'is_intimate': self.current_state['is_intimate']
        }
    
    def get_current_state(self) -> Dict:
        """Dapatkan semua state saat ini"""
        # Update time of day
        hour = datetime.now().hour
        if 5 <= hour < 11:
            self.current_state['time_of_day'] = 'pagi'
        elif 11 <= hour < 15:
            self.current_state['time_of_day'] = 'siang'
        elif 15 <= hour < 18:
            self.current_state['time_of_day'] = 'sore'
        else:
            self.current_state['time_of_day'] = 'malam'
        
        return self.current_state.copy()
    
    # =========================================================================
    # FORGETTING
    # =========================================================================
    
    def forget_old_memories(self):
        """Lupakan ingatan yang terlalu lama"""
        cutoff = time.time() - self.expire_seconds
        
        # Bersihkan items
        self.items = deque(
            [i for i in self.items if i['time'] > cutoff],
            maxlen=self.capacity
        )
        
        # Bersihkan timeline
        self.timeline = deque(
            [t for t in self.timeline if t['time'] > cutoff],
            maxlen=50
        )
        
        # Bersihkan history
        for hist in ['location_history', 'clothing_history', 'position_history', 
                    'activity_history', 'mood_history', 'arousal_history']:
            self.current_state[hist] = [
                h for h in self.current_state[hist] 
                if h['time'] > cutoff
            ]
        
        logger.debug(f"Forgot memories older than {self.expire_seconds}s")
    
    # =========================================================================
    # FORMAT UNTUK PROMPT
    # =========================================================================
    
    def format_for_prompt(self) -> str:
        """Format working memory untuk prompt"""
        state = self.get_current_state()
        activity = self.get_current_activity()
        
        lines = [
            "🧠 **WORKING MEMORY (24 jam):**",
            f"📍 Lokasi: {state['location'] or '?'}",
            f"👕 Pakaian: {state['clothing'] or '?'}",
            f"🧍 Posisi: {state['position_description'] or state['position'] or '?'}",
            f"🎭 Mood: {state['mood']} ({state['mood_intensity']:.0%})",
            f"🔥 Gairah: {state['arousal_level']}/10",
            f"💕 Lagi intim: {'Ya' if state['is_intimate'] else 'Tidak'}",
            f"🕐 Waktu: {state['time_of_day']}",
        ]
        
        if activity:
            duration = time.time() - (activity['start_time'] or time.time())
            duration_str = f"{int(duration/60)} menit" if duration > 60 else f"{int(duration)} detik"
            lines.append(f"🎯 Aktivitas: {activity['name']} ({duration_str})")
            if activity['details']:
                for key, value in activity['details'].items():
                    lines.append(f"   • {key}: {value}")
        
        lines.append("")
        lines.append("**Timeline terakhir:**")
        for t in list(self.timeline)[-5:]:
            time_str = datetime.fromtimestamp(t['time']).strftime("%H:%M")
            lines.append(f"• [{time_str}] {t['data']}")
        
        return "\n".join(lines)
    
    # =========================================================================
    # UNIVERSAL ACTIVITY TRACKER - BARU
    # =========================================================================
    
    def start_activity_universal(self, activity_type: str, details: Dict = None):
        """Mulai aktivitas baru (pergi, makan, tidur, dll)"""
        if activity_type not in self.ACTIVITY_TYPES:
            activity_type = 'preparing'
        
        activity_info = self.ACTIVITY_TYPES[activity_type]
        
        self.current_state['current_activity_universal'] = {
            'type': activity_type,
            'name': activity_info['name'],
            'details': details or {},
            'started_at': time.time(),
            'last_update': time.time(),
            'step': 0,
            'step_name': 'mulai',
            'steps': activity_info['steps'],
            'messages_sent': [],
            'user_actions': [],
            'status': 'active'
        }
        
        self._add_to_timeline('activity_start', f"{activity_info['name']}: {details}")
        logger.info(f"🎬 Activity started: {activity_type}")

    def update_activity(self, step: int, step_name: str, details: Dict = None):
        """Update progress aktivitas"""
        if 'current_activity_universal' in self.current_state:
            act = self.current_state['current_activity_universal']
            act['step'] = step
            act['step_name'] = step_name
            act['last_update'] = time.time()
            if details:
                act['details'].update(details)
            self._add_to_timeline('activity_update', f"Step {step}: {step_name}")

    def end_activity_universal(self, completed: bool = True):
        """Akhiri aktivitas"""
        if 'current_activity_universal' in self.current_state:
            act = self.current_state['current_activity_universal']
            act['status'] = 'completed' if completed else 'cancelled'
            act['ended_at'] = time.time()
            self._add_to_timeline('activity_end', f"{act['name']} selesai")
            self.current_state['activity_history'].append(act)
            del self.current_state['current_activity_universal']
            logger.info(f"🎬 Activity ended: {act['name']}")

    def get_current_activity_universal(self) -> Dict:
        """Dapatkan aktivitas yang sedang berlangsung"""
        return self.current_state.get('current_activity_universal', {})

    def record_activity_message(self, message: str, is_bot: bool = True):
        """Catat pesan dalam aktivitas"""
        act = self.get_current_activity_universal()
        if act:
            if 'messages_sent' not in act:
                act['messages_sent'] = []
            act['messages_sent'].append({
                'timestamp': time.time(),
                'is_bot': is_bot,
                'message': message[:100]
            })

    def record_user_action(self, action: str, details: Dict = None):
        """Catat aksi user"""
        act = self.get_current_activity_universal()
        if act:
            if 'user_actions' not in act:
                act['user_actions'] = []
            act['user_actions'].append({
                'timestamp': time.time(),
                'action': action,
                'details': details or {}
            })

    def has_said_in_activity(self, keyword: str) -> bool:
        """Cek apakah sudah bilang kata kunci dalam aktivitas ini"""
        act = self.get_current_activity_universal()
        if not act:
            return False
        for msg in act.get('messages_sent', []):
            if msg['is_bot'] and keyword in msg['message'].lower():
                return True
        return False

    def get_activity_progress_text(self) -> str:
        """Dapatkan teks progress aktivitas untuk prompt AI"""
        act = self.get_current_activity_universal()
        if not act:
            return ""
        
        activity_type = act.get('type', '')
        activity_name = act.get('name', 'aktivitas')
        step = act.get('step', 0)
        step_name = act.get('step_name', '')
        steps = act.get('steps', [])
        details = act.get('details', {})
        
        lines = [f"\n📋 **AKTIVITAS BERLANGSUNG:**"]
        lines.append(f"• Kamu sedang {activity_name}")
        
        if activity_type == 'going_out':
            destination = details.get('destination', 'tujuan')
            lines.append(f"• Tujuan: {destination}")
        
        elif activity_type == 'eating':
            food = details.get('food', 'makanan')
            lines.append(f"• Makanan: {food}")
        
        elif activity_type == 'intimate':
            lines.append(f"• Tahap: {step_name}")
        
        if steps:
            total = len(steps)
            lines.append(f"• Progress: {step}/{total} - {step_name}")
        
        # Cek kata yang sudah diucapkan
        kata_terucap = []
        for kata in ['siap', 'ganti', 'berangkat', 'tunggu', 'masak', 'makan']:
            if self.has_said_in_activity(kata):
                kata_terucap.append(kata)
        
        if kata_terucap:
            lines.append(f"• ✅ Sudah bilang: {', '.join(kata_terucap)}")
            lines.append("⚠️ **JANGAN ULANG** pesan yang sudah dikatakan!")
        
        if step < len(steps) - 1:
            next_step = steps[step + 1]
            lines.append(f"• 🔜 Selanjutnya: {next_step}")
        
        return "\n".join(lines)
    
    def detect_activity_from_message(self, message: str, is_bot: bool = False) -> tuple:
        """Deteksi jenis aktivitas dari pesan"""
        msg = message.lower()
        
        # Pergi
        if any(k in msg for k in ['ke kafe', 'ke rumah', 'ke mall', 'pergi ke', 'berangkat']):
            dest = 'kafe'
            if 'rumah' in msg: dest = 'rumah'
            elif 'mall' in msg: dest = 'mall'
            return ('going_out', {'destination': dest})
        
        # Persiapan
        if any(k in msg for k in ['siap-siap', 'ganti baju', 'mandi', 'persiapkan']):
            return ('preparing', {'action': 'bersiap'})
        
        # Makan
        if any(k in msg for k in ['masak', 'makan', 'makanan', 'sarapan']):
            return ('eating', {'food': 'makanan'})
        
        # Minum
        if any(k in msg for k in ['minum', 'kopi', 'teh', 'air']):
            return ('drinking', {'drink': 'minuman'})
        
        # Tidur
        if any(k in msg for k in ['tidur', 'ngantuk', 'mau tidur']):
            return ('sleeping', {})
        
        # Kerja
        if any(k in msg for k in ['kerja', 'bekerja', 'meeting']):
            return ('working', {})
        
        # Intim
        if any(k in msg for k in ['ke kamar', 'ayo ke kamar', 'cuddle']):
            return ('intimate', {})
        
        # Menunggu
        if any(k in msg for k in ['tunggu', 'wait', 'sebentar']):
            return ('waiting', {})
        
        return (None, None)
        
    # =========================================================================
    # ACTION TRACKING METHODS (untuk cegah pengulangan)
    # =========================================================================
    
    def add_action(self, action_type: str, details: Dict = None):
        """Catat tindakan yang sudah dilakukan"""
        now = time.time()
        
        action = {
            'type': action_type,
            'details': details or {},
            'timestamp': now,
            'expire_at': now + 3600
        }
        
        self.action_timeline.append(action)
        
        # Catat juga di timeline utama
        item = details.get('item', '') if details else ''
        target = details.get('to', '') if details else ''
        self._add_to_timeline('action', f"{action_type}: {item} ke {target}")
        
        logger.debug(f"📝 Action recorded: {action_type}")

    def has_done(self, action_type: str, target: str = None, item: str = None, seconds: int = 3600) -> bool:
        """Cek apakah sudah melakukan tindakan dalam N detik"""
        now = time.time()
        batas_waktu = now - seconds
        
        for aksi in self.action_timeline:
            if aksi['timestamp'] < batas_waktu:
                continue
            if aksi['type'] != action_type:
                continue
            if target:
                if aksi['details'].get('to', '') != target:
                    continue
            if item:
                if aksi['details'].get('item', '') != item:
                    continue
            return True
        
        return False

    def get_actions_summary(self, seconds: int = 3600) -> str:
        """Buat ringkasan tindakan untuk dikasih tahu ke AI"""
        now = time.time()
        batas_waktu = now - seconds
        aksi_terbaru = [a for a in self.action_timeline if a['timestamp'] > batas_waktu]
        
        if not aksi_terbaru:
            return ""
        
        hasil = ["📋 **TINDAKAN YANG SUDAH DILAKUKAN (JANGAN ULANGI):**"]
        
        for aksi in aksi_terbaru:
            if aksi['type'] == 'give_item':
                barang = aksi['details'].get('item', 'sesuatu')
                target = aksi['details'].get('to', 'user')
                hasil.append(f"• Kamu SUDAH memberikan {barang} ke {target}")
            
            elif aksi['type'] == 'offer_food':
                target = aksi['details'].get('to', 'user')
                hasil.append(f"• Kamu SUDAH menawarkan makanan ke {target}")
            
            elif aksi['type'] == 'invite_to_bedroom':
                hasil.append(f"• Kamu SUDAH mengajak ke kamar")
            
            elif aksi['type'] == 'aftercare_done':
                hasil.append(f"• Kamu SUDAH memberikan aftercare")
        
        hasil.append("\n⚠️ **PENTING:** Jika situasi berubah (basah lagi, lapar lagi), BOLEH memberikan barang yang sama!")
        
        return "\n".join(hasil)

    def mark_item_used(self, item: str):
        """Tandai barang sudah dipakai"""
        for aksi in reversed(self.action_timeline):
            if aksi['details'].get('item') == item:
                aksi['details']['used'] = True
                break

__all__ = ['WorkingMemory']
