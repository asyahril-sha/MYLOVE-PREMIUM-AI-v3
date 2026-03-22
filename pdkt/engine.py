# pdkt/engine.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - PDKT NATURAL ENGINE (V3 ENHANCED)
=============================================================================
Engine utama untuk PDKT dengan realisme 99% dan integrasi V3

Fitur V3:
- Integrasi dengan role behavior
- Integrasi dengan emotional flow
- Integrasi dengan spatial awareness
- Perilaku dinamis berdasarkan situasi
=============================================================================
"""

import time
import logging
import random
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from .chemistry import ChemistrySystem, ChemistryLevel, ChemistryScore
from .direction import DirectionSystem, PDKTDirection
from .mood import MoodSystem, MoodType
from .dreams import DreamSystem, DreamType
from .random_pdkt import RandomPDKTSystem
from .list_formatter import PDKTListFormatter

logger = logging.getLogger(__name__)


class NaturalPDKTEngine:
    """
    Engine utama untuk PDKT Natural dengan integrasi V3
    """
    
    def __init__(self, memory_bridge=None, relationship_memory=None):
        """
        Args:
            memory_bridge: MemoryBridge instance
            relationship_memory: RelationshipMemory instance
        """
        self.memory = memory_bridge
        self.relationship = relationship_memory
        
        # Sistem PDKT
        self.chemistry = ChemistrySystem()
        self.direction = DirectionSystem()
        self.mood = MoodSystem()
        self.dreams = DreamSystem()
        self.random_pdkt = RandomPDKTSystem()
        self.list_formatter = PDKTListFormatter()
        
        # Data PDKT aktif
        self.active_pdkt = {}  # {pdkt_id: pdkt_data}
        self.pdkt_by_user = {}  # {user_id: [pdkt_ids]}
        
        # V3: Role behavior references
        self.role_behaviors = {}  # {pdkt_id: role_behavior}
        
        logger.info("✅ NaturalPDKTEngine V3 initialized")
    
    # =========================================================================
    # CREATE PDKT
    # =========================================================================
    
    async def create_pdkt(self,
                         user_id: int,
                         user_name: str,
                         role: str,
                         is_random: bool = False,
                         role_behavior: Any = None) -> Dict:
        """
        Buat PDKT baru dengan integrasi V3
        
        Args:
            user_id: ID user
            user_name: Nama user
            role: Role yang dipilih
            is_random: Apakah random
            role_behavior: Role behavior instance (V3)
            
        Returns:
            PDKT data
        """
        # Generate PDKT ID
        pdkt_id = f"PDKT_{user_id}_{int(time.time())}_{random.randint(100,999)}"
        
        # Dapatkan nama bot
        from dynamics.name_generator import get_name_generator
        name_gen = get_name_generator()
        name_data = name_gen.get_name_with_meaning(role, user_id)
        bot_name = name_data['name']
        name_meaning = name_data['meaning']
        
        # Tentukan arah (random jika is_random)
        if is_random:
            direction = random.choice([
                PDKTDirection.USER_KE_BOT,
                PDKTDirection.BOT_KE_USER,
                PDKTDirection.TIMBAL_BALIK,
                PDKTDirection.BINGUNG
            ])
            direction_hint = self.direction._get_initial_hint(direction, bot_name)
        else:
            direction = PDKTDirection.USER_KE_BOT
            direction_hint = f"Kamu yang mulai suka sama {bot_name} duluan"
        
        # Chemistry awal
        initial_chemistry = random.randint(20, 80)
        chemistry_score = ChemistryScore(initial_chemistry)
        
        # Mood awal
        initial_mood = random.choice([MoodType.HAPPY, MoodType.CALM, MoodType.PLAYFUL])
        
        # Data PDKT
        pdkt_data = {
            'pdkt_id': pdkt_id,
            'user_id': user_id,
            'user_name': user_name,
            'role': role,
            'bot_name': bot_name,
            'name_meaning': name_meaning,
            'direction': direction,
            'direction_hint': direction_hint,
            'chemistry': chemistry_score,
            'mood': initial_mood,
            'level': 1,
            'total_duration': 0,
            'total_chats': 0,
            'total_intim': 0,
            'total_climax': 0,
            'created_at': time.time(),
            'last_interaction': time.time(),
            'is_paused': False,
            'paused_time': None,
            'ended_at': None,
            'end_reason': None,
            'inner_thoughts': [],
            'milestones': [],
            'history': [],
            'is_random': is_random
        }
        
        # Simpan
        self.active_pdkt[pdkt_id] = pdkt_data
        
        if user_id not in self.pdkt_by_user:
            self.pdkt_by_user[user_id] = []
        self.pdkt_by_user[user_id].append(pdkt_id)
        
        # Inisialisasi sistem pendukung
        self.chemistry.chemistries[pdkt_id] = chemistry_score
        self.direction.create_direction(pdkt_id, user_name, bot_name, is_random)
        self.mood.create_mood(pdkt_id, initial_mood)
        
        # V3: Simpan role behavior
        if role_behavior:
            self.role_behaviors[pdkt_id] = role_behavior
        
        logger.info(f"✅ PDKT created: {bot_name} ({role}) for user {user_id}")
        
        return pdkt_data
    
    async def create_pdkt_from_random(self, pdkt_data: Dict, role_behavior: Any = None) -> Dict:
        """
        Buat PDKT dari data random generator dengan integrasi V3
        
        Args:
            pdkt_data: Data dari RandomPDKTSystem
            role_behavior: Role behavior instance (V3)
            
        Returns:
            PDKT data
        """
        pdkt_id = pdkt_data['pdkt_id']
        user_id = pdkt_data['user_id']
        user_name = pdkt_data['user_name']
        role = pdkt_data['role']
        bot_name = pdkt_data['bot_name']
        direction = pdkt_data['direction']
        direction_hint = pdkt_data['direction_hint']
        initial_chemistry = pdkt_data['initial_chemistry']
        
        chemistry_score = ChemistryScore(initial_chemistry)
        
        pdkt_data['chemistry'] = chemistry_score
        pdkt_data['level'] = 1
        pdkt_data['total_duration'] = 0
        pdkt_data['total_chats'] = 0
        pdkt_data['total_intim'] = 0
        pdkt_data['total_climax'] = 0
        pdkt_data['created_at'] = time.time()
        pdkt_data['last_interaction'] = time.time()
        pdkt_data['is_paused'] = False
        pdkt_data['paused_time'] = None
        pdkt_data['inner_thoughts'] = []
        pdkt_data['milestones'] = []
        pdkt_data['history'] = []
        
        # Simpan
        self.active_pdkt[pdkt_id] = pdkt_data
        
        if user_id not in self.pdkt_by_user:
            self.pdkt_by_user[user_id] = []
        self.pdkt_by_user[user_id].append(pdkt_id)
        
        # Inisialisasi sistem pendukung
        self.chemistry.chemistries[pdkt_id] = chemistry_score
        self.direction.create_direction(pdkt_id, user_name, bot_name, True)
        self.mood.create_mood(pdkt_id, MoodType.CALM)
        
        # V3: Simpan role behavior
        if role_behavior:
            self.role_behaviors[pdkt_id] = role_behavior
        
        logger.info(f"✅ Random PDKT created: {bot_name} ({role}) for user {user_id}")
        
        return pdkt_data
    
    # =========================================================================
    # GET PDKT
    # =========================================================================
    
    async def get_pdkt(self, pdkt_id: str) -> Optional[Dict]:
        """Dapatkan data PDKT"""
        return self.active_pdkt.get(pdkt_id)
    
    async def get_role_behavior(self, pdkt_id: str) -> Optional[Any]:
        """Dapatkan role behavior untuk PDKT (V3)"""
        return self.role_behaviors.get(pdkt_id)
    
    async def get_user_pdkt_list(self, user_id: int) -> List[Dict]:
        """Dapatkan semua PDKT aktif untuk user"""
        pdkt_ids = self.pdkt_by_user.get(user_id, [])
        result = []
        
        for pid in pdkt_ids:
            if pid in self.active_pdkt:
                pdkt = self.active_pdkt[pid]
                # Format untuk list
                result.append({
                    'id': pid,
                    'pdkt_id': pid,
                    'bot_name': pdkt['bot_name'],
                    'role': pdkt['role'],
                    'direction': pdkt['direction'],
                    'level': pdkt['level'],
                    'total_chats': pdkt['total_chats'],
                    'last_interaction': pdkt['last_interaction'],
                    'is_paused': pdkt['is_paused'],
                    'chemistry_level': self.chemistry.get_chemistry(pid).get_level() if pid in self.chemistry.chemistries else ChemistryLevel.BIASA,
                    'hint': self.direction.get_hint(pid)
                })
        
        # Sort by last interaction
        result.sort(key=lambda x: x['last_interaction'], reverse=True)
        
        return result
    
    async def get_active_pdkt_by_role(self, user_id: int, role: str) -> Optional[Dict]:
        """Dapatkan PDKT aktif untuk role tertentu"""
        pdkt_ids = self.pdkt_by_user.get(user_id, [])
        
        for pid in pdkt_ids:
            if pid in self.active_pdkt:
                pdkt = self.active_pdkt[pid]
                if pdkt['role'] == role and not pdkt['is_paused']:
                    return pdkt
        
        return None
    
    # =========================================================================
    # UPDATE PDKT (ENHANCED)
    # =========================================================================
    
    async def update_progress(self, pdkt_id: str, duration: float, 
                              activity_type: str = 'chat',
                              emotional_state: Dict = None,
                              situasi: Dict = None) -> Dict:
        """
        Update progress PDKT berdasarkan interaksi dengan integrasi V3
        
        Args:
            pdkt_id: ID PDKT
            duration: Durasi interaksi (menit)
            activity_type: Jenis aktivitas
            emotional_state: State dari emotional flow (V3)
            situasi: Situasi saat ini (V3)
            
        Returns:
            Dict dengan update info
        """
        if pdkt_id not in self.active_pdkt:
            return {'error': 'PDKT not found'}
        
        pdkt = self.active_pdkt[pdkt_id]
        
        if pdkt['is_paused']:
            return {'error': 'PDKT is paused'}
        
        # Update durasi
        pdkt['total_duration'] += duration
        pdkt['total_chats'] += 1
        pdkt['last_interaction'] = time.time()
        
        # Hitung level baru (time-based)
        new_level = self._calculate_level(pdkt['total_duration'])
        level_up = new_level > pdkt['level']
        
        if level_up:
            pdkt['level'] = new_level
            pdkt['milestones'].append({
                'timestamp': time.time(),
                'type': 'level_up',
                'old_level': new_level - 1,
                'new_level': new_level,
                'emotional_state': emotional_state
            })
        
        # Catat history
        pdkt['history'].append({
            'timestamp': time.time(),
            'type': activity_type,
            'duration': duration,
            'level': pdkt['level'],
            'emotional_state': emotional_state,
            'situasi': situasi
        })
        
        # Update chemistry berdasarkan aktivitas dan emotional state
        chemistry_change = self._get_chemistry_change_v3(activity_type, emotional_state)
        self.chemistry.chemistries[pdkt_id].update(chemistry_change)
        
        # Update mood dengan integrasi emotional state
        mood_change = await self.mood.update_mood(
            pdkt_id, activity_type, chemistry_change, 
            {'situasi': situasi, 'last_interaction': pdkt['last_interaction']},
            emotional_state
        )
        
        # V3: Update role behavior jika ada
        role_behavior = self.role_behaviors.get(pdkt_id)
        if role_behavior:
            # Update arousal dari emotional state
            if emotional_state:
                role_behavior.update_arousal(
                    emotional_state.get('arousal_change', 0),
                    f"interaksi {activity_type}"
                )
            
            # Record interaksi
            role_behavior.record_user_response(True)  # Asumsi positif
            
            # Update situasi
            if situasi:
                role_behavior.update_situasi(situasi)
        
        return {
            'success': True,
            'level_up': level_up,
            'new_level': new_level,
            'chemistry_change': chemistry_change,
            'mood_change': mood_change
        }
    
    def _calculate_level(self, total_minutes: float) -> int:
        """Hitung level berdasarkan durasi"""
        if total_minutes < 5:
            return 1
        elif total_minutes < 12:
            return 2
        elif total_minutes < 20:
            return 3
        elif total_minutes < 30:
            return 4
        elif total_minutes < 42:
            return 5
        elif total_minutes < 60:
            return 6
        elif total_minutes < 75:
            return 7
        elif total_minutes < 90:
            return 8
        elif total_minutes < 105:
            return 9
        elif total_minutes < 120:
            return 10
        elif total_minutes < 135:
            return 11
        else:
            return 12
    
    def _get_chemistry_change_v3(self, activity_type: str, emotional_state: Dict = None) -> float:
        """
        Dapatkan perubahan chemistry berdasarkan aktivitas dan emotional state V3
        """
        base_changes = {
            'chat': random.uniform(-1, 2),
            'flirt': random.uniform(1, 4),
            'compliment': random.uniform(1, 3),
            'curhat': random.uniform(2, 5),
            'intim': random.uniform(3, 8),
            'climax': random.uniform(5, 10),
            'conflict': random.uniform(-5, -1),
            'ignore': random.uniform(-3, -0.5)
        }
        
        change = base_changes.get(activity_type, random.uniform(-0.5, 1.5))
        
        # V3: Bonus dari emotional state
        if emotional_state:
            arousal = emotional_state.get('arousal', 0)
            if arousal >= 70:
                change += 2  # Bonus arousal tinggi
            elif arousal >= 40:
                change += 1  # Bonus arousal sedang
            
            # Bonus jika state romantis
            if emotional_state.get('state') == 'romantic':
                change += 1.5
        
        return change
    
    # =========================================================================
    # PAUSE/RESUME/STOP
    # =========================================================================
    
    async def pause_pdkt(self, pdkt_id: str) -> bool:
        """Pause PDKT"""
        if pdkt_id not in self.active_pdkt:
            return False
        
        pdkt = self.active_pdkt[pdkt_id]
        if pdkt['is_paused']:
            return False
        
        pdkt['is_paused'] = True
        pdkt['paused_time'] = time.time()
        
        # V3: Update role behavior
        role_behavior = self.role_behaviors.get(pdkt_id)
        if role_behavior:
            role_behavior.mode_goda = max(0, role_behavior.mode_goda - 10)
        
        logger.info(f"⏸️ PDKT paused: {pdkt_id}")
        return True
    
    async def resume_pdkt(self, pdkt_id: str) -> Tuple[bool, str]:
        """Resume PDKT yang di-pause"""
        if pdkt_id not in self.active_pdkt:
            return False, "PDKT tidak ditemukan"
        
        pdkt = self.active_pdkt[pdkt_id]
        if not pdkt['is_paused']:
            return False, "PDKT sedang tidak dalam keadaan pause"
        
        # Hitung lama pause
        paused_duration = time.time() - pdkt['paused_time']
        hours = int(paused_duration / 3600)
        days = int(paused_duration / 86400)
        
        # Resume
        pdkt['is_paused'] = False
        pdkt['paused_time'] = None
        pdkt['last_interaction'] = time.time()
        
        # V3: Update role behavior
        role_behavior = self.role_behaviors.get(pdkt_id)
        if role_behavior:
            role_behavior.mode_goda = min(100, role_behavior.mode_goda + 15)
        
        # Generate pesan
        if days > 0:
            message = f"{pdkt['bot_name']}: 'Lama banget {days} hari {hours % 24} jam... Aku kira kamu lupa sama aku.'"
        elif hours > 0:
            message = f"{pdkt['bot_name']}: 'Wah {hours} jam nggak chat... Aku kangen.'"
        else:
            minutes = int(paused_duration / 60)
            message = f"{pdkt['bot_name']}: 'Baru {minutes} menit udah di-resume? Kamu kangen ya?'"
        
        logger.info(f"▶️ PDKT resumed: {pdkt_id}")
        return True, message
    
    async def stop_pdkt(self, pdkt_id: str, user_id: int, reason: str = "user_request") -> Dict:
        """
        Hentikan PDKT (putus)
        
        Args:
            pdkt_id: ID PDKT
            user_id: ID user
            reason: Alasan putus
            
        Returns:
            Dict hasil stop
        """
        if pdkt_id not in self.active_pdkt:
            return {'success': False, 'reason': 'PDKT tidak ditemukan'}
        
        pdkt = self.active_pdkt[pdkt_id]
        bot_name = pdkt['bot_name']
        
        # V3: Hapus role behavior
        if pdkt_id in self.role_behaviors:
            del self.role_behaviors[pdkt_id]
        
        # Simpan ke mantan
        if hasattr(self, 'mantan_manager'):
            mantan_id = self.mantan_manager.add_mantan(user_id, pdkt, reason)
        else:
            mantan_id = None
        
        # Hapus dari active
        del self.active_pdkt[pdkt_id]
        
        if user_id in self.pdkt_by_user:
            if pdkt_id in self.pdkt_by_user[user_id]:
                self.pdkt_by_user[user_id].remove(pdkt_id)
        
        logger.info(f"💔 PDKT stopped: {bot_name} for user {user_id}")
        
        return {
            'success': True,
            'bot_name': bot_name,
            'mantan_id': mantan_id,
            'reason': reason
        }
    
    async def force_close_pdkt_by_role(self, user_id: int, role: str):
        """Force close PDKT berdasarkan role"""
        pdkt = await self.get_active_pdkt_by_role(user_id, role)
        if pdkt:
            await self.stop_pdkt(pdkt['pdkt_id'], user_id, "force_close")
    
    # =========================================================================
    # INNER THOUGHTS (ENHANCED)
    # =========================================================================
    
    async def get_inner_thoughts(self, pdkt_id: str, limit: int = 5) -> List[str]:
        """Dapatkan inner thoughts untuk PDKT"""
        if pdkt_id not in self.active_pdkt:
            return []
        
        pdkt = self.active_pdkt[pdkt_id]
        thoughts = pdkt.get('inner_thoughts', [])
        
        # V3: Tambah dari role behavior
        role_behavior = self.role_behaviors.get(pdkt_id)
        if role_behavior:
            situasi = {'kakak_ada': getattr(role_behavior, 'kakak_ada', True)}
            role_thought = role_behavior.get_inner_thought(situasi)
            if role_thought and role_thought not in thoughts:
                thoughts.append(role_thought)
        
        return thoughts[-limit:]
    
    async def add_inner_thought(self, pdkt_id: str, thought: str):
        """Tambah inner thought"""
        if pdkt_id in self.active_pdkt:
            self.active_pdkt[pdkt_id].setdefault('inner_thoughts', []).append(thought)
    
    # =========================================================================
    # GET STATUS (ENHANCED)
    # =========================================================================
    
    async def get_pdkt_status(self, pdkt_id: str) -> Optional[Dict]:
        """Dapatkan status lengkap PDKT dengan integrasi V3"""
        if pdkt_id not in self.active_pdkt:
            return None
        
        pdkt = self.active_pdkt[pdkt_id]
        chemistry = self.chemistry.get_chemistry(pdkt_id)
        direction_data = self.direction.get_direction(pdkt_id)
        mood_data = self.mood.get_mood(pdkt_id)
        
        # V3: Dapatkan data role behavior
        role_behavior = self.role_behaviors.get(pdkt_id)
        role_status = {}
        if role_behavior:
            role_status = {
                'mode_goda': role_behavior.mode_goda,
                'arousal': role_behavior.arousal,
                'user_attraction': getattr(role_behavior, 'user_attraction', 50)
            }
        
        return {
            'pdkt_id': pdkt_id,
            'bot_name': pdkt['bot_name'],
            'role': pdkt['role'],
            'level': pdkt['level'],
            'total_duration': pdkt['total_duration'],
            'total_chats': pdkt['total_chats'],
            'total_intim': pdkt['total_intim'],
            'total_climax': pdkt['total_climax'],
            'is_paused': pdkt['is_paused'],
            'created_at': pdkt['created_at'],
            'last_interaction': pdkt['last_interaction'],
            'chemistry': {
                'level': chemistry.get_level().value if chemistry else 'biasa',
                'score': chemistry.score if chemistry else 50,
                'description': chemistry.get_description() if chemistry else ''
            },
            'direction': {
                'who': direction_data['direction'].value if direction_data else 'unknown',
                'text': self.direction.get_direction_text(pdkt_id),
                'hint': self.direction.get_hint(pdkt_id)
            },
            'mood': {
                'current': mood_data['current'].value if mood_data else 'calm',
                'intensity': mood_data['intensity'] if mood_data else 0.5,
                'description': mood_data.get('description', 'netral') if mood_data else 'netral'
            },
            # V3 additions
            'role_status': role_status
        }


__all__ = ['NaturalPDKTEngine']
