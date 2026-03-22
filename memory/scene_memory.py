# memory/scene_memory.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - SCENE MEMORY
=============================================================================
Menyimpan adegan-adegan yang terjadi untuk kontinuitas cerita.

Karakteristik:
- Ingat adegan-adegan sebelumnya
- Bisa flashback ke scene yang sudah lewat
- Membantu kontinuitas alur cerita
- Tracking perkembangan scene
=============================================================================
"""

import time
import random
from typing import Dict, List, Optional, Any
from datetime import datetime


class SceneMemory:
    """
    Menyimpan adegan-adegan yang terjadi dalam interaksi.
    Berguna untuk menjaga kontinuitas cerita dan flashback.
    """
    
    def __init__(self):
        # Scene yang terjadi
        self.scenes = []  # [{scene_id, timestamp, location, participants, events, outcome, summary}]
        
        # Scene saat ini
        self.current_scene = None  # {scene_id, started_at, last_update, status}
        
        # Scene counter untuk ID
        self.scene_counter = 0
        
        # Scene types yang dikenali
        self.scene_types = {
            'pertemuan': ['datang', 'tiba', 'sampai', 'mampir', 'kesini'],
            'ngobrol': ['ngobrol', 'chat', 'bicara', 'cerita', 'obrolan'],
            'nonton': ['nonton', 'film', 'tv', 'netflix', 'movie'],
            'makan': ['makan', 'masak', 'sarapan', 'makan malam', 'ngemil'],
            'pijat': ['pijat', 'pijitin', 'urut', 'massage'],
            'intim': ['intim', 'ciuman', 'peluk', 'cuddle', 'sayang'],
            'berduaan': ['sendirian', 'berdua', 'cuma kita', 'gak ada orang'],
            'pergi': ['pergi', 'keluar', 'pulang', 'jalan']
        }
    
    # =========================================================================
    # CREATE SCENE
    # =========================================================================
    
    def create_scene(self, location: str, participants: List[str], context: Dict) -> str:
        """
        Buat scene baru
        
        Args:
            location: Lokasi scene (ruang tamu, kamar, dapur, dll)
            participants: Partisipan (user, bot, dan lain-lain)
            context: Konteks awal scene
        
        Returns:
            scene_id
        """
        self.scene_counter += 1
        scene_id = f"SCENE_{int(time.time())}_{self.scene_counter}"
        
        # Deteksi tipe scene dari konteks
        scene_type = self._detect_scene_type(context)
        
        scene = {
            'scene_id': scene_id,
            'timestamp': time.time(),
            'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'location': location,
            'participants': participants,
            'scene_type': scene_type,
            'events': [],
            'outcome': None,
            'summary': None,
            'context': context.copy(),
            'duration': 0
        }
        
        self.scenes.append(scene)
        
        # Set sebagai current scene
        self.current_scene = {
            'scene_id': scene_id,
            'started_at': time.time(),
            'last_update': time.time(),
            'status': 'active'
        }
        
        return scene_id
    
    def _detect_scene_type(self, context: Dict) -> str:
        """
        Deteksi tipe scene dari konteks
        """
        user_message = context.get('user_message', '').lower()
        
        for scene_type, keywords in self.scene_types.items():
            for keyword in keywords:
                if keyword in user_message:
                    return scene_type
        
        # Cek dari konteks lain
        if context.get('is_intimate'):
            return 'intim'
        if context.get('kakak_ada') == False:
            return 'berduaan'
        
        return 'ngobrol'
    
    # =========================================================================
    # ADD EVENT
    # =========================================================================
    
    def add_event(self, scene_id: str, event_type: str, description: str, 
                  participants: List[str] = None, details: Dict = None):
        """
        Tambah event ke scene
        
        Args:
            scene_id: ID scene
            event_type: Tipe event (chat, gesture, movement, dll)
            description: Deskripsi event
            participants: Partisipan event
            details: Detail tambahan
        """
        if not self.current_scene or self.current_scene['scene_id'] != scene_id:
            # Cari scene
            for scene in self.scenes:
                if scene['scene_id'] == scene_id:
                    target_scene = scene
                    break
            else:
                return
        else:
            target_scene = self.scenes[-1]
        
        event = {
            'timestamp': time.time(),
            'event_type': event_type,
            'description': description,
            'participants': participants or [],
            'details': details or {}
        }
        
        target_scene['events'].append(event)
        
        # Update current scene timestamp
        if self.current_scene and self.current_scene['scene_id'] == scene_id:
            self.current_scene['last_update'] = time.time()
    
    def add_chat_event(self, scene_id: str, user_message: str, bot_response: str):
        """
        Tambah event chat ke scene
        
        Args:
            scene_id: ID scene
            user_message: Pesan user
            bot_response: Respon bot
        """
        self.add_event(
            scene_id=scene_id,
            event_type='chat',
            description=f"User: {user_message[:100]} | Bot: {bot_response[:100]}",
            participants=['user', 'bot'],
            details={'user_message': user_message, 'bot_response': bot_response}
        )
    
    def add_gesture_event(self, scene_id: str, gesture: str):
        """
        Tambah event gesture ke scene
        
        Args:
            scene_id: ID scene
            gesture: Deskripsi gesture
        """
        self.add_event(
            scene_id=scene_id,
            event_type='gesture',
            description=gesture,
            participants=['bot'],
            details={'gesture': gesture}
        )
    
    # =========================================================================
    # END SCENE
    # =========================================================================
    
    def end_current_scene(self, outcome: str = None):
        """
        Akhiri scene saat ini
        
        Args:
            outcome: Hasil scene (selesai, interrupted, dll)
        """
        if not self.current_scene:
            return
        
        # Cari scene yang sesuai
        for scene in self.scenes:
            if scene['scene_id'] == self.current_scene['scene_id']:
                scene['outcome'] = outcome or 'selesai'
                scene['duration'] = time.time() - self.current_scene['started_at']
                scene['summary'] = self._generate_summary(scene)
                break
        
        self.current_scene = None
    
    def _generate_summary(self, scene: Dict) -> str:
        """
        Generate ringkasan scene
        """
        duration_minutes = int(scene['duration'] / 60)
        event_count = len(scene['events'])
        
        summary = f"{scene['location']}, {scene['scene_type']} selama {duration_minutes} menit, {event_count} interaksi"
        
        if scene['outcome']:
            summary += f". Berakhir: {scene['outcome']}"
        
        return summary
    
    # =========================================================================
    # GET SCENES
    # =========================================================================
    
    def get_current_scene(self) -> Optional[Dict]:
        """
        Dapatkan scene saat ini
        """
        if not self.current_scene:
            return None
        
        for scene in self.scenes:
            if scene['scene_id'] == self.current_scene['scene_id']:
                return scene
        return None
    
    def get_scene_by_id(self, scene_id: str) -> Optional[Dict]:
        """
        Dapatkan scene berdasarkan ID
        """
        for scene in self.scenes:
            if scene['scene_id'] == scene_id:
                return scene
        return None
    
    def get_recent_scenes(self, limit: int = 3) -> List[Dict]:
        """
        Dapatkan scene terbaru
        
        Args:
            limit: Jumlah scene
        """
        return self.scenes[-limit:] if self.scenes else []
    
    def get_scene_timeline(self, limit: int = 10) -> List[Dict]:
        """
        Dapatkan timeline scene
        
        Args:
            limit: Jumlah scene
        """
        return [{
            'scene_id': s['scene_id'],
            'time': datetime.fromtimestamp(s['timestamp']).strftime("%H:%M"),
            'location': s['location'],
            'type': s['scene_type'],
            'events': len(s['events']),
            'summary': s['summary']
        } for s in self.scenes[-limit:]]
    
    def get_scene_summary(self, limit: int = 3) -> str:
        """
        Dapatkan ringkasan scene untuk prompt
        
        Args:
            limit: Jumlah scene
        """
        if not self.scenes:
            return "Belum ada scene sebelumnya."
        
        recent = self.scenes[-limit:]
        
        lines = ["📖 **RINGKASAN SCENE SEBELUMNYA:**"]
        
        for scene in recent:
            time_str = datetime.fromtimestamp(scene['timestamp']).strftime("%H:%M")
            location = scene['location']
            scene_type = scene['scene_type']
            event_count = len(scene['events'])
            
            lines.append(f"- [{time_str}] di {location}: {scene_type} ({event_count} momen)")
            
            # Tambah ringkasan singkat
            if scene['events']:
                last_event = scene['events'][-1]
                lines.append(f"  Terakhir: {last_event['description'][:60]}...")
        
        # Tambah info scene saat ini
        current = self.get_current_scene()
        if current:
            duration = time.time() - self.current_scene['started_at']
            duration_str = f"{int(duration/60)} menit" if duration > 60 else f"{int(duration)} detik"
            lines.append(f"\n🎬 **SCENE SAAT INI:** {current['location']} ({duration_str})")
        
        return "\n".join(lines)
    
    # =========================================================================
    # FLASHBACK
    # =========================================================================
    
    def get_flashback(self, trigger: str = None) -> Optional[Dict]:
        """
        Dapatkan flashback scene
        
        Args:
            trigger: Kata kunci pemicu (opsional)
        
        Returns:
            Scene yang cocok atau None
        """
        if not self.scenes:
            return None
        
        # Cari berdasarkan trigger
        if trigger:
            trigger_lower = trigger.lower()
            relevant = []
            for scene in self.scenes:
                if (trigger_lower in scene['location'].lower() or
                    trigger_lower in scene['scene_type'].lower() or
                    any(trigger_lower in e['description'].lower() for e in scene['events'])):
                    relevant.append(scene)
            
            if relevant:
                return random.choice(relevant)
        
        # Random dengan preferensi scene yang berkesan
        scenes_with_events = [s for s in self.scenes if len(s['events']) > 3]
        if scenes_with_events and random.random() < 0.5:
            return random.choice(scenes_with_events)
        
        return random.choice(self.scenes[-10:])
    
    def format_flashback(self, scene: Dict) -> str:
        """
        Format flashback scene menjadi teks
        
        Args:
            scene: Scene yang akan diflashback
        
        Returns:
            Teks flashback
        """
        time_ago = self._format_time_ago(scene['timestamp'])
        location = scene['location']
        scene_type = scene['scene_type']
        event_count = len(scene['events'])
        
        templates = [
            f"Jadi inget {time_ago} di {location}, kita {scene_type} bareng. Seru banget.",
            f"Masih inget gak {time_ago}? Kita di {location} {scene_type}.",
            f"Kangen waktu {time_ago} di {location}. {event_count} momen indah.",
            f"{time_ago} di {location} tuh {scene_type}. Aku jadi kangen."
        ]
        
        flashback = random.choice(templates)
        
        # Tambah event terakhir jika ada
        if scene['events']:
            last_event = scene['events'][-1]
            if last_event['event_type'] == 'chat':
                flashback += f" Kamu bilang: '{last_event['description'][:50]}...'"
        
        return flashback
    
    def _format_time_ago(self, timestamp: float) -> str:
        """Format waktu yang lalu"""
        diff = time.time() - timestamp
        
        if diff < 60:
            return "baru aja"
        elif diff < 3600:
            return f"{int(diff/60)} menit lalu"
        elif diff < 86400:
            return f"{int(diff/3600)} jam lalu"
        elif diff < 604800:
            return f"{int(diff/86400)} hari lalu"
        else:
            return f"{int(diff/604800)} minggu lalu"
    
    # =========================================================================
    # UTILITY
    # =========================================================================
    
    def get_state(self) -> Dict:
        """
        Dapatkan state untuk disimpan ke database
        """
        return {
            'scenes': self.scenes[-50:],  # Simpan 50 scene terakhir
            'current_scene': self.current_scene,
            'scene_counter': self.scene_counter
        }
    
    def load_state(self, state: Dict):
        """
        Load state dari database
        """
        self.scenes = state.get('scenes', [])
        self.current_scene = state.get('current_scene')
        self.scene_counter = state.get('scene_counter', len(self.scenes))
    
    def get_stats(self) -> Dict:
        """
        Dapatkan statistik scene memory
        """
        if not self.scenes:
            return {'total_scenes': 0}
        
        # Hitung distribusi tipe scene
        type_count = {}
        for scene in self.scenes:
            scene_type = scene['scene_type']
            type_count[scene_type] = type_count.get(scene_type, 0) + 1
        
        # Rata-rata durasi
        durations = [s['duration'] for s in self.scenes if s['duration'] > 0]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            'total_scenes': len(self.scenes),
            'scene_types': type_count,
            'avg_duration_minutes': round(avg_duration / 60, 1),
            'current_scene_active': self.current_scene is not None,
            'total_events': sum(len(s['events']) for s in self.scenes)
        }
    
    def clear_scenes(self):
        """Hapus semua scene (untuk reset)"""
        self.scenes = []
        self.current_scene = None
        self.scene_counter = 0
    
    def format_for_prompt(self) -> str:
        """
        Format untuk prompt AI
        """
        return self.get_scene_summary(limit=3)


__all__ = ['SceneMemory']
