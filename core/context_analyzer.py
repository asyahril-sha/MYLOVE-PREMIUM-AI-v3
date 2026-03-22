# core/context_analyzer.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - CONTEXT ANALYZER (VIRTUAL HUMAN)
=============================================================================
Menganalisis dan menggabungkan semua konteks percakapan dengan kemampuan V3:
- Menggabungkan data dari semua sistem (memory, leveling, dynamics, dll)
- Analisis situasi (kakak ada/tidak, suami ada/tidak, kantor sepi, dll)
- Analisis posisi dari narasi user
- Analisis sentimen dan intent
- Analisis emosi user
- Menyediakan konteks lengkap untuk generate respons
=============================================================================
"""

import time
import logging
import random
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class ContextAnalyzer:
    """
    Menganalisis dan menggabungkan semua konteks percakapan dengan kemampuan V3
    """
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 300  # 5 menit
        
        # Database pola deteksi situasi
        self.situasi_patterns = {
            'kakak_ada': [
                r'istriku\s+ada', r'kakakku\s+ada', r'istri\s+lagi\s+di', r'kakak\s+lagi\s+di',
                r'istriku\s+di\s+rumah', r'kakakku\s+di\s+rumah'
            ],
            'kakak_tidak_ada': [
                r'istriku\s+pergi', r'kakakku\s+pergi', r'istriku\s+keluar', r'kakakku\s+keluar',
                r'istriku\s+tidak\s+ada', r'kakakku\s+tidak\s+ada', r'istriku\s+sedang\s+keluar'
            ],
            'kakak_tidur': [
                r'istriku\s+tidur', r'kakakku\s+tidur', r'istri\s+lagi\s+tidur', r'kakak\s+lagi\s+tidur'
            ],
            'suami_ada': [
                r'suamiku\s+ada', r'suami\s+lagi\s+di', r'suami\s+di\s+rumah'
            ],
            'suami_tidak_ada': [
                r'suamiku\s+pergi', r'suamiku\s+keluar', r'suami\s+tidak\s+ada', r'suami\s+sedang\s+keluar'
            ],
            'suami_tidur': [
                r'suamiku\s+tidur', r'suami\s+lagi\s+tidur'
            ],
            'kantor_sepi': [
                r'kantor\s+sepi', r'kantor\s+kosong', r'tidak\s+ada\s+orang', r'sendirian\s+di\s+kantor'
            ],
            'lembur_malam': [
                r'lembur', r'lembur\s+malam', r'kerja\s+malam', r'kantor\s+malam'
            ],
            'orang_tua_ada': [
                r'orang\s+tua\s+ada', r'ibu\s+ada', r'ayah\s+ada', r'ortu\s+ada'
            ],
            'orang_tua_tidak_ada': [
                r'orang\s+tua\s+pergi', r'orang\s+tua\s+keluar', r'ortu\s+pergi'
            ],
            'berduaan': [
                r'sendirian', r'cuma\s+berdua', r'kita\s+aja', r'tidak\s+ada\s+orang', r'berdua\s+aja'
            ]
        }
        
        # Database pola deteksi posisi
        self.posisi_patterns = [
            (r'duduk\s+di\s+antara\s+kaki', 'duduk_di_antara_kaki', 'di antara kaki user'),
            (r'di\s+antara\s+kaki', 'duduk_di_antara_kaki', 'di antara kaki user'),
            (r'duduk\s+di\s+pangkuan', 'duduk_di_pangkuan', 'di pangkuan user'),
            (r'di\s+pangkuan', 'duduk_di_pangkuan', 'di pangkuan user'),
            (r'di\s+belakang', 'di_belakang', 'di belakang user'),
            (r'dibelakang', 'di_belakang', 'di belakang user'),
            (r'bersebelahan', 'bersebelahan', 'di samping user'),
            (r'berdampingan', 'bersebelahan', 'di samping user'),
            (r'di\s+samping', 'bersebelahan', 'di samping user'),
            (r'berhadapan', 'berhadapan', 'berhadapan dengan user'),
            (r'menghadap', 'berhadapan', 'berhadapan dengan user'),
            (r'di\s+depan', 'di_depan', 'di depan user'),
            (r'didepan', 'di_depan', 'di depan user')
        ]
        
        # Database emosi user
        self.emosi_patterns = {
            'senang': ['senang', 'bahagia', 'happy', 'gembira', 'ceria'],
            'sedih': ['sedih', 'kecewa', 'sad', 'down', 'galau'],
            'marah': ['marah', 'kesal', 'betek', 'geram', 'sebal'],
            'horny': ['horny', 'sange', 'nafsu', 'pengen', 'hot', 'panas'],
            'romantis': ['sayang', 'cinta', 'romantis', 'kangen', 'rindu'],
            'malu': ['malu', 'gugup', 'deg-degan', 'salah tingkah'],
            'capek': ['capek', 'lelah', 'lemas', 'ngantuk']
        }
        
        logger.info("✅ ContextAnalyzer V3 initialized")
    
    async def analyze(self,
                     user_id: int,
                     session_id: str,
                     user_message: str,
                     role: str,
                     bot_name: str,
                     user_name: str,
                     
                     # ===== DATA DARI SISTEM LAIN =====
                     intimacy_data: Optional[Dict] = None,
                     mood_data: Optional[Dict] = None,
                     chemistry_data: Optional[Dict] = None,
                     direction_data: Optional[Dict] = None,
                     location_data: Optional[Dict] = None,
                     clothing_data: Optional[Dict] = None,
                     physical_attrs: Optional[Dict] = None,
                     user_preferences: Optional[Dict] = None,
                     memories: Optional[List[Dict]] = None,
                     story_data: Optional[Dict] = None,
                     intent_data: Optional[Dict] = None,
                     dominance_mode: str = "normal",
                     conversation_history: Optional[List[Dict]] = None,
                     
                     # ===== V3 ADDITIONS =====
                     emotional_state: Optional[Dict] = None,
                     spatial_info: Optional[Dict] = None,
                     
                     # ===== METADATA =====
                     metadata: Optional[Dict] = None) -> Dict:
        """
        Analisis lengkap semua konteks dengan kemampuan V3
        """
        
        # Cek cache
        cache_key = f"{session_id}:{user_message[:50]}"
        if cache_key in self.cache:
            cache_age = time.time() - self.cache[cache_key]['timestamp']
            if cache_age < self.cache_ttl:
                logger.debug(f"Context cache hit for: {user_message[:30]}...")
                return self.cache[cache_key]['data']
        
        # ===== 1. KONTEKS DASAR =====
        context = {
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'time_of_day': self._get_time_of_day(),
            'day_of_week': datetime.now().strftime('%A'),
            
            'user': {
                'id': user_id,
                'name': user_name,
                'message': user_message,
                'message_length': len(user_message)
            },
            
            'bot': {
                'name': bot_name,
                'role': role,
                'dominance_mode': dominance_mode
            },
            
            'session': {
                'id': session_id,
                'duration': 0
            }
        }
        
        # ===== 2. INTIMACY DATA =====
        if intimacy_data:
            context['intimacy'] = {
                'level': intimacy_data.get('level', 1),
                'level_name': intimacy_data.get('level_name', 'Malu-malu'),
                'can_intim': intimacy_data.get('can_intim', False),
                'progress': intimacy_data.get('progress', 0),
                'next_level_in': intimacy_data.get('next_level_in', 0),
                'total_duration': intimacy_data.get('total_duration', 0),
                'effective_duration': intimacy_data.get('effective_duration', 0)
            }
        else:
            context['intimacy'] = {
                'level': 1,
                'level_name': 'Malu-malu',
                'can_intim': False,
                'progress': 0,
                'next_level_in': 0,
                'total_duration': 0,
                'effective_duration': 0
            }
        
        # ===== 3. MOOD DATA =====
        if mood_data:
            context['mood'] = {
                'current': mood_data.get('current', 'calm'),
                'emoji': mood_data.get('emoji', '😐'),
                'description': mood_data.get('description', 'netral'),
                'intensity': mood_data.get('intensity', 0.5),
                'factor': mood_data.get('factor', 1.0),
                'secondary': mood_data.get('secondary')
            }
        else:
            context['mood'] = {
                'current': 'calm',
                'emoji': '😐',
                'description': 'netral',
                'intensity': 0.5,
                'factor': 1.0
            }
        
        # ===== 4. CHEMISTRY DATA =====
        if chemistry_data:
            context['chemistry'] = {
                'level': chemistry_data.get('level', 'biasa'),
                'score': chemistry_data.get('score', 50),
                'vibe': chemistry_data.get('vibe', '😐'),
                'description': chemistry_data.get('description', ''),
                'trend': chemistry_data.get('trend', 'stabil')
            }
        else:
            context['chemistry'] = {
                'level': 'biasa',
                'score': 50,
                'vibe': '😐',
                'description': 'Chemistry biasa',
                'trend': 'stabil'
            }
        
        # ===== 5. DIRECTION DATA =====
        if direction_data:
            context['direction'] = {
                'who': direction_data.get('who', 'user_ke_bot'),
                'text': direction_data.get('text', ''),
                'hint': direction_data.get('hint', ''),
                'intensity': direction_data.get('intensity', 5)
            }
        
        # ===== 6. LOKASI & PAKAIAN =====
        if location_data:
            context['location'] = {
                'name': location_data.get('name', 'Tempat tidak diketahui'),
                'description': location_data.get('description', ''),
                'category': location_data.get('category', 'urban'),
                'base_risk': location_data.get('base_risk', 50),
                'base_thrill': location_data.get('base_thrill', 50),
                'activities': location_data.get('activities', [])
            }
        else:
            context['location'] = {
                'name': 'Tempat tidak diketahui',
                'description': '',
                'category': 'unknown',
                'base_risk': 50,
                'base_thrill': 50,
                'activities': []
            }
        
        if clothing_data:
            context['clothing'] = {
                'description': clothing_data.get('description', 'Pakaian biasa'),
                'type': clothing_data.get('type', 'casual'),
                'color': clothing_data.get('color', ''),
                'category': clothing_data.get('category', 'casual')
            }
        else:
            context['clothing'] = {
                'description': 'Pakaian biasa',
                'type': 'casual',
                'category': 'casual'
            }
        
        # ===== 7. ATRIBUT FISIK BOT =====
        if physical_attrs:
            context['physical'] = {
                'age': physical_attrs.get('age', 22),
                'height': physical_attrs.get('height', 165),
                'weight': physical_attrs.get('weight', 52),
                'chest': physical_attrs.get('chest', '34B'),
                'hair': physical_attrs.get('hair', 'hitam panjang'),
                'eyes': physical_attrs.get('eyes', 'coklat'),
                'skin': physical_attrs.get('skin', 'sawo matang')
            }
        
        # ===== 8. PREFERENSI USER =====
        if user_preferences:
            context['preferences'] = {
                'positions': user_preferences.get('positions', [])[:3],
                'areas': user_preferences.get('areas', [])[:3],
                'activities': user_preferences.get('activities', [])[:3],
                'locations': user_preferences.get('locations', [])[:3],
                'foreplay': user_preferences.get('foreplay', [])[:3],
                'aftercare': user_preferences.get('aftercare', [])[:3]
            }
        
        # ===== 9. MEMORI RELEVAN =====
        if memories:
            context['memories'] = []
            for mem in memories[:5]:
                context['memories'].append({
                    'content': mem.get('content', '')[:100],
                    'emotion': mem.get('emotional_tag', 'netral'),
                    'time_ago': self._format_time_ago(mem.get('timestamp', time.time())),
                    'importance': mem.get('importance', 0.5)
                })
        
        # ===== 10. STORY ARC =====
        if story_data:
            context['story'] = {
                'current_arc': story_data.get('current_arc', 'get_to_know'),
                'description': story_data.get('description', ''),
                'recommended_scene': story_data.get('recommended_scene', ''),
                'progression': story_data.get('progression', [])
            }
        
        # ===== 11. INTENT USER =====
        if intent_data:
            context['intent'] = {
                'primary': intent_data.get('primary_intent', 'chit_chat'),
                'all': [i.value for i in intent_data.get('all_intents', [])] if intent_data.get('all_intents') else [],
                'sentiment': intent_data.get('sentiment', 'neutral'),
                'is_question': intent_data.get('is_question', False),
                'needs': intent_data.get('needs', []),
                'has_emoji': intent_data.get('has_emoji', False)
            }
        else:
            context['intent'] = {
                'primary': 'chit_chat',
                'sentiment': 'neutral',
                'is_question': False,
                'needs': []
            }
        
        # ===== 12. HISTORY PERCAKAPAN =====
        if conversation_history:
            context['history'] = []
            for msg in conversation_history[-5:]:
                context['history'].append({
                    'role': msg.get('role', 'user'),
                    'content': msg.get('content', '')[:100],
                    'time_ago': self._format_time_ago(msg.get('timestamp', time.time()))
                })
        
        # ===== 13. V3: ANALISIS SITUASI =====
        situasi = self._analyze_situasi(user_message)
        context['situasi'] = situasi
        
        # ===== 14. V3: ANALISIS POSISI =====
        posisi = self._analyze_posisi(user_message)
        context['posisi'] = posisi
        
        # ===== 15. V3: ANALISIS EMOSI USER =====
        user_emotion = self._analyze_user_emotion(user_message)
        context['user_emotion'] = user_emotion
        
        # ===== 16. V3: ANALISIS AROUSAL USER =====
        user_arousal = self._analyze_user_arousal(user_message)
        context['user_arousal'] = user_arousal
        
        # ===== 17. V3: EMOTIONAL STATE =====
        if emotional_state:
            context['bot_emotional_state'] = emotional_state
        
        # ===== 18. V3: SPATIAL INFO =====
        if spatial_info:
            context['spatial_info'] = spatial_info
        
        # ===== 19. HITUNGAN TAMBAHAN =====
        context['calculations'] = {
            'idle_minutes': await self._get_idle_minutes(session_id),
            'conversation_tone': self._analyze_tone(user_message),
            'message_sentiment_score': self._calculate_sentiment_score(user_message),
            'user_arousal_score': user_arousal
        }
        
        # Simpan ke cache
        self.cache[cache_key] = {
            'timestamp': time.time(),
            'data': context
        }
        
        # Bersihkan cache lama
        self._cleanup_cache()
        
        logger.debug(f"Context analyzed for session {session_id}")
        
        return context
    
    # =========================================================================
    # V3: ANALISIS SITUASI
    # =========================================================================
    
    def _analyze_situasi(self, user_message: str) -> Dict:
        """
        Analisis situasi dari pesan user
        """
        message_lower = user_message.lower()
        
        situasi = {
            'kakak_ada': True,
            'kakak_tidur': False,
            'suami_ada': True,
            'suami_tidur': False,
            'kantor_sepi': False,
            'lembur_malam': False,
            'orang_tua_ada': True,
            'berduaan': False
        }
        
        # Deteksi menggunakan regex patterns
        for key, patterns in self.situasi_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    if key == 'kakak_ada':
                        situasi['kakak_ada'] = True
                    elif key == 'kakak_tidak_ada':
                        situasi['kakak_ada'] = False
                    elif key == 'kakak_tidur':
                        situasi['kakak_tidur'] = True
                    elif key == 'suami_ada':
                        situasi['suami_ada'] = True
                    elif key == 'suami_tidak_ada':
                        situasi['suami_ada'] = False
                    elif key == 'suami_tidur':
                        situasi['suami_tidur'] = True
                    elif key == 'kantor_sepi':
                        situasi['kantor_sepi'] = True
                    elif key == 'lembur_malam':
                        situasi['lembur_malam'] = True
                    elif key == 'orang_tua_ada':
                        situasi['orang_tua_ada'] = True
                    elif key == 'orang_tua_tidak_ada':
                        situasi['orang_tua_ada'] = False
                    elif key == 'berduaan':
                        situasi['berduaan'] = True
        
        # Deteksi tambahan dari kata kunci sederhana
        if any(w in message_lower for w in ['sendirian', 'cuma berdua', 'kita aja', 'tidak ada orang']):
            situasi['berduaan'] = True
        
        return situasi
    
    def _analyze_posisi(self, user_message: str) -> Dict:
        """
        Analisis posisi dari pesan user
        """
        message_lower = user_message.lower()
        
        for pattern, pos_type, relative in self.posisi_patterns:
            if re.search(pattern, message_lower):
                return {
                    'found': True,
                    'type': pos_type,
                    'relative': relative,
                    'raw': pattern
                }
        
        return {'found': False}
    
    def _analyze_user_emotion(self, user_message: str) -> Dict:
        """
        Analisis emosi user dari pesan
        """
        message_lower = user_message.lower()
        
        emotions = {}
        for emotion, keywords in self.emosi_patterns.items():
            count = sum(1 for k in keywords if k in message_lower)
            if count > 0:
                emotions[emotion] = count
        
        if not emotions:
            return {'primary': 'netral', 'intensity': 0.5}
        
        # Ambil emosi dengan skor tertinggi
        primary = max(emotions, key=emotions.get)
        intensity = min(1.0, emotions[primary] / 5)
        
        return {
            'primary': primary,
            'intensity': intensity,
            'all': emotions
        }
    
    def _analyze_user_arousal(self, user_message: str) -> float:
        """
        Analisis arousal user dari pesan
        """
        message_lower = user_message.lower()
        arousal = 0.0
        
        high_words = ['horny', 'sange', 'nafsu', 'pengen', 'hot', 'panas', 'intim', 'seksi']
        medium_words = ['deg-degan', 'gugup', 'malu', 'berani', 'dekat']
        low_words = ['enak', 'nyaman', 'santai']
        
        for word in high_words:
            if word in message_lower:
                arousal += 0.3
        for word in medium_words:
            if word in message_lower:
                arousal += 0.15
        for word in low_words:
            if word in message_lower:
                arousal += 0.05
        
        # Deteksi dari gesture/deskripsi
        if '*' in user_message or '(' in user_message or '[' in user_message:
            arousal += 0.1
        
        return min(1.0, arousal)
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def _get_time_of_day(self) -> str:
        """Dapatkan waktu saat ini"""
        hour = datetime.now().hour
        if 5 <= hour < 11:
            return "pagi"
        elif 11 <= hour < 15:
            return "siang"
        elif 15 <= hour < 18:
            return "sore"
        elif 18 <= hour < 22:
            return "malam"
        else:
            return "tengah malam"
    
    async def _get_idle_minutes(self, session_id: str) -> float:
        """Dapatkan berapa menit user diam"""
        return 0
    
    def _analyze_tone(self, message: str) -> str:
        """Analisis nada percakapan"""
        message_lower = message.lower()
        
        positive_words = ['senang', 'bahagia', 'suka', 'cinta', 'sayang', '❤️', '😊', '🥰', '😍']
        negative_words = ['sedih', 'marah', 'kecewa', 'benci', '😢', '😠', '💔', '😭']
        intimate_words = ['intim', 'ml', 'sex', 'tidur', '🔥', '💦', '😏', 'horny', 'sange']
        playful_words = ['lucu', 'haha', 'wkwk', 'ngakak', 'jail', 'goda', '😜', '😝']
        
        pos_count = sum(1 for w in positive_words if w in message_lower)
        neg_count = sum(1 for w in negative_words if w in message_lower)
        int_count = sum(1 for w in intimate_words if w in message_lower)
        play_count = sum(1 for w in playful_words if w in message_lower)
        
        if int_count > 0:
            return "intimate"
        elif play_count > 0:
            return "playful"
        elif pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"
    
    def _calculate_sentiment_score(self, message: str) -> float:
        """Hitung skor sentimen"""
        message_lower = message.lower()
        
        positive_words = ['senang', 'bahagia', 'suka', 'cinta', 'sayang', 'nikmat', 'enak', 'nyaman', 'baik']
        negative_words = ['sedih', 'marah', 'kecewa', 'benci', 'sakit', 'payah', 'jelek', 'buruk']
        
        score = 0
        for word in positive_words:
            if word in message_lower:
                score += 0.1
        for word in negative_words:
            if word in message_lower:
                score -= 0.1
        
        return max(-1.0, min(1.0, score))
    
    def _format_time_ago(self, timestamp: float) -> str:
        """Format waktu yang lalu"""
        diff = time.time() - timestamp
        
        if diff < 60:
            return "baru saja"
        elif diff < 3600:
            return f"{int(diff / 60)} menit lalu"
        elif diff < 86400:
            return f"{int(diff / 3600)} jam lalu"
        else:
            return f"{int(diff / 86400)} hari lalu"
    
    def _cleanup_cache(self):
        """Bersihkan cache yang sudah expired"""
        now = time.time()
        expired = []
        
        for key, data in self.cache.items():
            if now - data['timestamp'] > self.cache_ttl:
                expired.append(key)
        
        for key in expired:
            del self.cache[key]
    
    def get_summary(self, context: Dict) -> str:
        """Dapatkan ringkasan konteks"""
        lines = [
            f"📊 Context Summary:",
            f"• User: {context['user']['name']}",
            f"• Bot: {context['bot']['name']} ({context['bot']['role']})",
            f"• Level: {context['intimacy']['level']} | Mood: {context['mood']['emoji']}",
            f"• Chemistry: {context['chemistry']['level']} ({context['chemistry']['score']}%)",
            f"• Location: {context['location']['name']}",
            f"• Intent: {context.get('intent', {}).get('primary', 'unknown')}",
            f"• Tone: {context.get('calculations', {}).get('conversation_tone', 'neutral')}"
        ]
        
        # V3 additions
        if context.get('situasi'):
            if context['situasi'].get('berduaan'):
                lines.append(f"• Situasi: Berduaan")
            if context['situasi'].get('kantor_sepi'):
                lines.append(f"• Situasi: Kantor sepi")
        
        if context.get('user_emotion'):
            lines.append(f"• Emosi user: {context['user_emotion'].get('primary', 'netral')}")
        
        if context.get('user_arousal'):
            lines.append(f"• Arousal user: {context['user_arousal']:.0%}")
        
        return "\n".join(lines)
    
    def format_for_display(self, context: Dict) -> str:
        """Format konteks untuk ditampilkan (debug)"""
        lines = [
            "=" * 50,
            "📊 KONTEKS PERCAKAPAN (V3)",
            "=" * 50,
            f"👤 User: {context['user']['name']}",
            f"🤖 Bot: {context['bot']['name']} ({context['bot']['role']})",
            f"📈 Level: {context['intimacy']['level']}/12",
            f"🎭 Mood: {context['mood']['emoji']} {context['mood']['description']}",
            f"🔥 Chemistry: {context['chemistry']['vibe']} {context['chemistry']['level']}",
            f"📍 Lokasi: {context['location']['name']}",
            f"👗 Pakaian: {context['clothing']['description']}",
            f"🎯 Intent: {context['intent']['primary']}",
        ]
        
        # V3 additions
        if context.get('situasi'):
            lines.append(f"🏠 Situasi: {context['situasi']}")
        
        if context.get('posisi', {}).get('found'):
            lines.append(f"📍 Posisi: {context['posisi'].get('relative', '?')}")
        
        if context.get('user_emotion'):
            lines.append(f"😊 Emosi user: {context['user_emotion'].get('primary', '?')}")
        
        if context.get('user_arousal'):
            lines.append(f"🔥 Arousal user: {context['user_arousal']:.0%}")
        
        lines.append(f"💬 Pesan: {context['user']['message'][:100]}...")
        lines.append("=" * 50)
        
        return "\n".join(lines)


__all__ = ['ContextAnalyzer']
