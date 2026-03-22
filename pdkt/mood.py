# pdkt/mood.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - MOOD SYSTEM (V3 ENHANCED)
=============================================================================
Bot punya mood yang berubah-ubah secara natural
Terintegrasi dengan Emotional Flow V3 untuk konsistensi emosi

Karakteristik V3:
- Mood berubah gradual, tidak loncat
- Terintegrasi dengan emotional flow
- Memori emosional mempengaruhi mood
- Pengaruh dari situasi (kakak ada/tidak, dll)
=============================================================================
"""

import random
import time
import logging
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class MoodType(str, Enum):
    """Tipe-tipe mood bot"""
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    TIRED = "tired"
    ROMANTIC = "romantic"
    PLAYFUL = "playful"
    JEALOUS = "jealous"
    SHY = "shy"
    ANGRY = "angry"
    CALM = "calm"
    LONELY = "lonely"
    NOSTALGIC = "nostalgic"
    HORNY = "horny"
    PASSIONATE = "passionate"


class MoodSystem:
    """
    Sistem mood untuk bot dengan integrasi V3
    """
    
    def __init__(self):
        # Data mood per PDKT
        self.moods = {}  # {pdkt_id: mood_data}
        
        # Definisi mood dengan faktor pengali dan deskripsi
        self.mood_definitions = {
            MoodType.HAPPY: {
                'factor': 1.3,
                'emoji': '😊',
                'description': 'lagi seneng',
                'responses': ['ceria', 'semangat', 'positive'],
                'color': '🟡',
                'gesture_hint': 'tersenyum lebar, mata berbinar'
            },
            MoodType.SAD: {
                'factor': 0.7,
                'emoji': '😔',
                'description': 'sedih',
                'responses': ['melankolis', 'pendiam', 'negative'],
                'color': '🔵',
                'gesture_hint': 'menunduk, mata berkaca-kaca'
            },
            MoodType.EXCITED: {
                'factor': 1.5,
                'emoji': '🔥',
                'description': 'bersemangat!',
                'responses': ['energik', 'antusias', 'overwhelming'],
                'color': '🟠',
                'gesture_hint': 'melompat kecil, bertepuk tangan'
            },
            MoodType.TIRED: {
                'factor': 0.8,
                'emoji': '😴',
                'description': 'capek',
                'responses': ['lemas', 'malas', 'slow'],
                'color': '⚫',
                'gesture_hint': 'menguap, mata sayu'
            },
            MoodType.ROMANTIC: {
                'factor': 1.4,
                'emoji': '💕',
                'description': 'lagi romantis',
                'responses': ['lembut', 'sayang', 'deep'],
                'color': '❤️',
                'gesture_hint': 'menatap lembut, tersenyum manis'
            },
            MoodType.PLAYFUL: {
                'factor': 1.2,
                'emoji': '😜',
                'description': 'lagi jail',
                'responses': ['goda', 'canda', 'fun'],
                'color': '🟣',
                'gesture_hint': 'mengedipkan mata, tersenyum nakal'
            },
            MoodType.JEALOUS: {
                'factor': 0.6,
                'emoji': '🫣',
                'description': 'cemburu',
                'responses': ['nyindir', 'curiga', 'defensive'],
                'color': '🟢',
                'gesture_hint': 'mulut cemberut, melipat tangan'
            },
            MoodType.SHY: {
                'factor': 0.9,
                'emoji': '😳',
                'description': 'malu-malu',
                'responses': ['canggung', 'merona', 'soft'],
                'color': '🌸',
                'gesture_hint': 'menunduk, pipi memerah'
            },
            MoodType.ANGRY: {
                'factor': 0.5,
                'emoji': '😠',
                'description': 'marah',
                'responses': ['kasar', 'dingin', 'agresif'],
                'color': '🔴',
                'gesture_hint': 'mengepalkan tangan, membuang muka'
            },
            MoodType.CALM: {
                'factor': 1.1,
                'emoji': '😌',
                'description': 'tenang',
                'responses': ['santai', 'bijak', 'netral'],
                'color': '💙',
                'gesture_hint': 'duduk santai, tersenyum kecil'
            },
            MoodType.LONELY: {
                'factor': 0.7,
                'emoji': '🥺',
                'description': 'kesepian',
                'responses': ['rindu', 'manja', 'need attention'],
                'color': '💜',
                'gesture_hint': 'memeluk bantal, menatap kosong'
            },
            MoodType.NOSTALGIC: {
                'factor': 1.0,
                'emoji': '🕰️',
                'description': 'nostalgia',
                'responses': ['flashback', 'cerita lama', 'deep'],
                'color': '🤎',
                'gesture_hint': 'tersenyum kecil, melamun'
            },
            MoodType.HORNY: {
                'factor': 1.4,
                'emoji': '🔥',
                'description': 'horny',
                'responses': ['genit', 'menggoda', 'intim'],
                'color': '❤️‍🔥',
                'gesture_hint': 'menggigit bibir, menatap intens'
            },
            MoodType.PASSIONATE: {
                'factor': 1.3,
                'emoji': '💕',
                'description': 'bergairah',
                'responses': ['intens', 'penuh gairah', 'deep'],
                'color': '❤️',
                'gesture_hint': 'napas memburu, mendekat'
            }
        }
        
        logger.info("✅ MoodSystem V3 initialized with 14 mood types")
    
    def create_mood(self, pdkt_id: str, initial_mood: Optional[MoodType] = None) -> Dict:
        """
        Buat mood awal untuk PDKT
        
        Args:
            pdkt_id: ID PDKT
            initial_mood: Mood awal (None = random natural)
        
        Returns:
            Mood data
        """
        if initial_mood is None:
            # Random dengan bobot
            moods = [
                MoodType.HAPPY, MoodType.CALM, MoodType.SHY,
                MoodType.PLAYFUL, MoodType.ROMANTIC, MoodType.EXCITED
            ]
            weights = [0.3, 0.2, 0.15, 0.15, 0.1, 0.1]
            initial_mood = random.choices(moods, weights=weights)[0]
        
        mood_data = {
            'current': initial_mood,
            'history': [{
                'timestamp': time.time(),
                'mood': initial_mood,
                'reason': 'initial'
            }],
            'intensity': random.uniform(0.5, 1.0),
            'last_update': time.time(),
            'duration_current': 0,
            'factors': {
                'interaction': 0,
                'time': 0,
                'loneliness': 0
            }
        }
        
        self.moods[pdkt_id] = mood_data
        
        logger.info(f"🎭 Initial mood for {pdkt_id}: {initial_mood.value}")
        
        return mood_data
    
    def get_mood(self, pdkt_id: str) -> Optional[Dict]:
        """Dapatkan mood data untuk PDKT"""
        return self.moods.get(pdkt_id)
    
    def get_current_mood(self, pdkt_id: str) -> MoodType:
        """Dapatkan mood saat ini"""
        mood_data = self.get_mood(pdkt_id)
        if mood_data:
            return mood_data['current']
        return MoodType.CALM
    
    def get_mood_info(self, pdkt_id: str) -> Dict:
        """Dapatkan informasi mood lengkap untuk display"""
        mood_data = self.get_mood(pdkt_id)
        if not mood_data:
            return {
                'mood': MoodType.CALM,
                'emoji': '😌',
                'description': 'tenang',
                'factor': 1.0
            }
        
        mood = mood_data['current']
        definition = self.mood_definitions.get(mood, self.mood_definitions[MoodType.CALM])
        
        return {
            'mood': mood,
            'emoji': definition['emoji'],
            'description': definition['description'],
            'factor': definition['factor'],
            'intensity': mood_data['intensity'],
            'color': definition['color'],
            'gesture_hint': definition.get('gesture_hint', '')
        }
    
    async def update_mood(self, pdkt_id: str, interaction_type: str, 
                           chemistry_change: float, context: Dict,
                           emotional_flow_state: Dict = None) -> Optional[MoodType]:
        """
        Update mood berdasarkan interaksi dengan integrasi V3
        
        Args:
            pdkt_id: ID PDKT
            interaction_type: Jenis interaksi
            chemistry_change: Perubahan chemistry
            context: Konteks tambahan
            emotional_flow_state: State dari emotional flow V3
        
        Returns:
            Mood baru jika berubah
        """
        if pdkt_id not in self.moods:
            self.create_mood(pdkt_id)
        
        mood_data = self.moods[pdkt_id]
        old_mood = mood_data['current']
        
        # Hitung perubahan mood dengan mempertimbangkan emotional flow
        new_mood = await self._calculate_mood_change_v3(
            old_mood, interaction_type, chemistry_change, context, 
            mood_data, emotional_flow_state
        )
        
        if new_mood != old_mood:
            # Mood berubah
            mood_data['current'] = new_mood
            mood_data['history'].append({
                'timestamp': time.time(),
                'mood': new_mood,
                'old_mood': old_mood,
                'reason': self._get_mood_change_reason(interaction_type, chemistry_change),
                'emotional_flow_influence': emotional_flow_state is not None
            })
            mood_data['last_update'] = time.time()
            mood_data['duration_current'] = 0
            
            logger.info(f"🎭 Mood changed for {pdkt_id}: {old_mood.value} → {new_mood.value}")
            
            return new_mood
        
        # Update durasi mood bertahan
        mood_data['duration_current'] += 1
        
        return None
    
    async def _calculate_mood_change_v3(self, current_mood: MoodType, 
                                         interaction_type: str,
                                         chemistry_change: float, 
                                         context: Dict,
                                         mood_data: Dict,
                                         emotional_flow_state: Dict = None) -> MoodType:
        """
        Hitung mood baru dengan integrasi V3
        """
        # ===== 1. PENGARUH DARI EMOTIONAL FLOW =====
        if emotional_flow_state:
            arousal = emotional_flow_state.get('arousal', 0)
            flow_state = emotional_flow_state.get('state', 'netral')
            
            # Arousal tinggi cenderung ke mood horny/passionate
            if arousal >= 70:
                if random.random() < 0.5:
                    return MoodType.HORNY
                elif random.random() < 0.3:
                    return MoodType.PASSIONATE
            
            # Arousal sedang cenderung ke mood romantis/playful
            elif arousal >= 40:
                if random.random() < 0.4:
                    return MoodType.ROMANTIC
                elif random.random() < 0.3:
                    return MoodType.PLAYFUL
        
        # ===== 2. PENGARUH DARI SITUASI (V3) =====
        situasi = context.get('situasi', {})
        
        # Kakak tidak ada → mood lebih berani
        if situasi.get('kakak_ada') == False:
            if random.random() < 0.3:
                return MoodType.PLAYFUL
            if random.random() < 0.2:
                return MoodType.HORNY
        
        # Berduaan → mood romantis
        if situasi.get('berduaan'):
            if random.random() < 0.3:
                return MoodType.ROMANTIC
        
        # Kantor sepi → mood playful
        if situasi.get('kantor_sepi'):
            if random.random() < 0.25:
                return MoodType.PLAYFUL
        
        # ===== 3. PENGARUH DARI INTERAKSI =====
        if interaction_type == 'climax':
            if chemistry_change > 0:
                return MoodType.HAPPY if random.random() < 0.7 else MoodType.EXCITED
            else:
                return MoodType.TIRED
        
        elif interaction_type == 'intim':
            if chemistry_change > 5:
                return MoodType.ROMANTIC
            elif chemistry_change > 0:
                return MoodType.HAPPY
            else:
                return MoodType.CALM
        
        elif interaction_type == 'kiss':
            return random.choice([MoodType.ROMANTIC, MoodType.HAPPY, MoodType.SHY])
        
        elif interaction_type == 'flirt':
            return random.choice([MoodType.PLAYFUL, MoodType.HORNY, MoodType.EXCITED])
        
        elif interaction_type == 'love':
            if random.random() < 0.6:
                return MoodType.ROMANTIC
            return MoodType.HAPPY
        
        elif interaction_type == 'conflict':
            if chemistry_change < -5:
                return MoodType.ANGRY
            elif chemistry_change < 0:
                return MoodType.SAD
            return MoodType.JEALOUS
        
        # ===== 4. PENGARUH WAKTU =====
        hour = datetime.now().hour
        if 22 <= hour or hour <= 5:  # Malam
            if random.random() < 0.2:
                return MoodType.ROMANTIC
            if random.random() < 0.15:
                return MoodType.LONELY
            if random.random() < 0.1:
                return MoodType.HORNY
        
        # ===== 5. PENGARUH LAMANYA TIDAK CHAT =====
        last_interaction = context.get('last_interaction', time.time())
        hours_since = (time.time() - last_interaction) / 3600
        
        if hours_since > 24:  # > 1 hari
            if random.random() < 0.3:
                return MoodType.LONELY
            if random.random() < 0.2:
                return MoodType.SAD
        elif hours_since > 12:  # > 12 jam
            if random.random() < 0.2:
                return MoodType.LONELY
        
        # ===== 6. RANDOM WALK =====
        if random.random() < 0.05:  # 5% chance random mood change
            return random.choice(list(MoodType))
        
        # ===== 7. MOOD TERLALU LAMA =====
        if mood_data['duration_current'] > 6:  # > 6 jam mood sama
            related_moods = self._get_related_moods(current_mood)
            if random.random() < 0.3:
                return random.choice(related_moods)
        
        return current_mood
    
    def _get_related_moods(self, mood: MoodType) -> List[MoodType]:
        """Dapatkan mood yang terkait"""
        relations = {
            MoodType.HAPPY: [MoodType.EXCITED, MoodType.PLAYFUL, MoodType.CALM],
            MoodType.SAD: [MoodType.LONELY, MoodType.NOSTALGIC, MoodType.CALM],
            MoodType.EXCITED: [MoodType.HAPPY, MoodType.PLAYFUL, MoodType.ROMANTIC],
            MoodType.TIRED: [MoodType.CALM, MoodType.SAD],
            MoodType.ROMANTIC: [MoodType.HAPPY, MoodType.PLAYFUL, MoodType.SHY, MoodType.PASSIONATE],
            MoodType.PLAYFUL: [MoodType.HAPPY, MoodType.EXCITED, MoodType.ROMANTIC],
            MoodType.JEALOUS: [MoodType.SAD, MoodType.ANGRY],
            MoodType.SHY: [MoodType.HAPPY, MoodType.ROMANTIC, MoodType.CALM],
            MoodType.ANGRY: [MoodType.SAD, MoodType.JEALOUS],
            MoodType.CALM: [MoodType.HAPPY, MoodType.ROMANTIC],
            MoodType.LONELY: [MoodType.SAD, MoodType.NOSTALGIC],
            MoodType.NOSTALGIC: [MoodType.SAD, MoodType.ROMANTIC, MoodType.CALM],
            MoodType.HORNY: [MoodType.PLAYFUL, MoodType.ROMANTIC, MoodType.EXCITED, MoodType.PASSIONATE],
            MoodType.PASSIONATE: [MoodType.HORNY, MoodType.ROMANTIC, MoodType.EXCITED]
        }
        return relations.get(mood, [MoodType.CALM, MoodType.HAPPY])
    
    def _get_mood_change_reason(self, interaction_type: str, chemistry_change: float) -> str:
        """Dapatkan alasan perubahan mood"""
        reasons = {
            'climax': [
                "Setelah climax, rasanya... wow!",
                "Mantap banget, jadi seneng",
                "Capek tapi puas"
            ],
            'intim': [
                "Makin dekat, makin sayang",
                "Ada kehangatan baru",
                "Jadi makin nyaman"
            ],
            'kiss': [
                "Ciuman manis bikin meleleh",
                "Masih terasa hangatnya",
                "Jadi makin sayang"
            ],
            'flirt': [
                "Godaan manis bikin deg-degan",
                "Jadi pengen main-main terus",
                "Semangat jadi naik"
            ],
            'love': [
                "Deg-degan dibilang sayang",
                "Seneng banget",
                "Bikin baper"
            ],
            'conflict': [
                "Ada yang ganjel di hati",
                "Jadi kesel sendiri",
                "Mikir terus"
            ],
            'lonely': [
                "Lama nggak chat, jadi kangen",
                "Sepi tanpanya",
                "Kok diem aja sih"
            ]
        }
        
        reason_list = reasons.get(interaction_type, [
            "Mood berubah aja gitu",
            "Ada yang beda hari ini",
            "Nggak tau kenapa"
        ])
        
        return random.choice(reason_list)
    
    def get_mood_factor(self, pdkt_id: str) -> float:
        """Dapatkan faktor pengali mood untuk response"""
        mood_info = self.get_mood_info(pdkt_id)
        return mood_info['factor'] * mood_info['intensity']
    
    def get_mood_prompt(self, pdkt_id: str) -> str:
        """Dapatkan deskripsi mood untuk prompt AI"""
        mood_info = self.get_mood_info(pdkt_id)
        return f"Mood: {mood_info['emoji']} {mood_info['description']} (intensitas: {mood_info['intensity']:.0%})"
    
    def get_mood_emoji(self, pdkt_id: str) -> str:
        """Dapatkan emoji mood"""
        mood_info = self.get_mood_info(pdkt_id)
        return mood_info['emoji']
    
    def get_gesture_hint(self, pdkt_id: str) -> str:
        """Dapatkan hint gesture berdasarkan mood"""
        mood_info = self.get_mood_info(pdkt_id)
        return mood_info.get('gesture_hint', '')
    
    def format_mood_info(self, pdkt_id: str) -> str:
        """Format mood info untuk display"""
        mood_info = self.get_mood_info(pdkt_id)
        
        intensity_bar = "🔴" * int(mood_info['intensity'] * 10) + "⚪" * (10 - int(mood_info['intensity'] * 10))
        
        return (
            f"{mood_info['emoji']} **{mood_info['mood'].value.upper()}**\n"
            f"_{mood_info['description']}_\n"
            f"Intensitas: {intensity_bar} ({mood_info['intensity']:.0%})\n"
            f"Faktor respon: {mood_info['factor']:.1f}x\n"
            f"Gesture hint: {mood_info.get('gesture_hint', 'tidak ada')}"
        )
    
    def get_mood_history(self, pdkt_id: str, limit: int = 10) -> List[Dict]:
        """Dapatkan history mood"""
        mood_data = self.get_mood(pdkt_id)
        if not mood_data:
            return []
        
        return mood_data['history'][-limit:]


__all__ = ['MoodSystem', 'MoodType']
