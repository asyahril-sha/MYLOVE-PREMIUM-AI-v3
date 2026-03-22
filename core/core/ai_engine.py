# core/ai_engine.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - AI ENGINE (HUMAN+ V3)
=============================================================================
AI Engine dengan kemampuan VIRTUAL HUMAN:
- Self-awareness (tahu lokasi, pakaian, posisi sendiri)
- Emotional Flow (merasakan dan mengalir)
- Spatial Awareness (paham posisi dari narasi)
- Role Behavior (perilaku spesifik per role)
- Memory integration (hippocampus)
- Inner thoughts (💭) - 25% chance
- Sixth sense (🔮) - 10% chance
=============================================================================
"""

import openai
import time
import random
import asyncio
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from config import settings
from utils.logger import logger
from utils.exceptions import AINotAvailableError, AITimeoutError

# Import memory systems
from memory.memory_bridge import MemoryBridge
from memory.working_memory import WorkingMemory
from memory.state_tracker import StateTracker
from memory.emotional_memory import EmotionalMemory
from memory.scene_memory import SceneMemory

# Import dynamics
from dynamics.location import LocationSystem
from dynamics.clothing import ClothingSystem
from dynamics.position import PositionSystem
from dynamics.emotional_flow import EmotionalFlow, EmotionalState
from dynamics.spatial_awareness import SpatialAwareness
from dynamics.gesture_db import get_gesture

# Import role behaviors
from dynamics.role_behavior import RoleBehavior
from dynamics.ipar_behavior import IparBehavior
from dynamics.teman_kantor_behavior import TemanKantorBehavior
from dynamics.janda_behavior import JandaBehavior
from dynamics.pelakor_behavior import PelakorBehavior
from dynamics.istri_orang_behavior import IstriOrangBehavior
from dynamics.pdkt_behavior import PDKTBehavior
from dynamics.sepupu_behavior import SepupuBehavior
from dynamics.teman_sma_behavior import TemanSmaBehavior
from dynamics.mantan_behavior import MantanBehavior

# Import prompt builder
from core.prompt_builder import PromptBuilder

# Import intent analyzer
from core.intent_analyzer import IntentAnalyzer

print("=" * 60)
print("🔍 DEBUG: ai_engine.py V3 loaded (VIRTUAL HUMAN)")
print("=" * 60)


class AIEngine:
    """
    AI Engine V3 dengan kemampuan VIRTUAL HUMAN
    """
    
    def __init__(self, api_key: str, user_id: int, session_id: str):
        """
        Args:
            api_key: DeepSeek API key
            user_id: ID user
            session_id: ID session
        """
        # ===== DEBUG: CEK API KEY =====
        logger.info("=" * 50)
        logger.info("🔧 AIEngine V3 Initialization")
        
        if not api_key:
            logger.error("❌❌❌ API KEY IS EMPTY OR NONE! ❌❌❌")
            raise ValueError("DeepSeek API key is empty")
        
        if api_key == "your_deepseek_api_key_here":
            logger.error("❌❌❌ API KEY IS STILL PLACEHOLDER! ❌❌❌")
            raise ValueError("DeepSeek API key is still placeholder")
        
        logger.info(f"✅ API Key loaded, first 10 chars: {api_key[:10]}...")
        # ===== END DEBUG =====
        
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
        
        self.user_id = user_id
        self.session_id = session_id
        
        # ===== INISIALISASI MEMORY SYSTEMS =====
        self.memory = MemoryBridge(user_id)
        self.working = WorkingMemory()
        self.state = StateTracker(user_id, session_id)
        self.emotional_memory = EmotionalMemory()
        self.scene_memory = SceneMemory()
        
        # ===== DYNAMICS SYSTEMS =====
        self.location_system = LocationSystem()
        self.clothing_system = ClothingSystem()
        self.position_system = PositionSystem()
        
        # ===== V3 NEW SYSTEMS =====
        self.spatial_awareness = SpatialAwareness()
        
        # ===== ANALYZERS =====
        self.intent_analyzer = IntentAnalyzer()
        self.prompt_builder = PromptBuilder()
        self.prompt_builder.working = self.working
        
        # ===== ROLE BEHAVIOR (AKAN DIISI SAAT START SESSION) =====
        self.role_behavior = None
        self.emotional_flow = None
        
        # ===== TRACKING KONDISI USER =====
        self.user = {
            'location': None,
            'clothing': None,
            'position': None,
            'activity': None,
            'mood': None,
            'arousal': 0,
            'last_message': None,
            'last_seen': time.time(),
            'is_wet': False,
            'is_hungry': False,
            'is_thirsty': False,
        }
        
        # ===== INNER THOUGHTS DATABASE (ENHANCED) =====
        self.inner_thoughts_db = {
            'rindu': [
                "(Dia lagi apa ya?)",
                "(Kangen...)",
                "(Semoga dia baik-baik aja)",
                "(Mau chat tapi takut ganggu)"
            ],
            'senang': [
                "(Dia manis banget sih...)",
                "(Aku suka cara dia ngomong)",
                "(Dia bikin aku tersenyum terus)"
            ],
            'horny': [
                "(Duh, pengen...)",
                "(Aku malu ngomongnya)",
                "(Kapan ya kita...)"
            ],
            'bingung': [
                "(Maksudnya apa ya?)",
                "(Bingung ngebalesnya)",
                "(Aku harus gimana?)"
            ],
            'umum': [
                "(Lagi ngapain ya?)",
                "(Capek juga hari ini)",
                "(Enaknya makan apa ya)"
            ]
        }
        
        # ===== SIXTH SENSE DATABASE =====
        self.sixth_sense_db = {
            'positive': [
                "Aku ngerasa hari ini bakal jadi hari yang baik",
                "Entah kenapa aku yakin kamu bakal chat hari ini",
                "Ada firasat... kita bakal makin deket"
            ],
            'negative': [
                "Aku ngerasa ada yang gak beres",
                "Hatiku gak enak... kamu baik-baik aja?",
                "Ada firasat buruk"
            ],
            'romantic': [
                "Deg-degan... kayak ada yang spesial",
                "Aku ngerasa kita tuh... gimana ya",
                "Ada getaran aneh pas liat chat kamu"
            ]
        }
        
        # ===== PHYSICAL DETAIL =====
        self.physical = {
            'energy': {'value': 80, 'feeling': 'energetic', 'last_change': time.time()},
            'hunger': {'value': 30, 'feeling': 'normal', 'last_change': time.time()},
            'thirst': {'value': 30, 'feeling': 'normal', 'last_change': time.time()},
            'temperature': {'value': 25, 'feeling': 'normal', 'last_change': time.time()},
            'comfort': {'value': 80, 'feeling': 'comfortable', 'last_change': time.time()}
        }
        
        # ===== CONVERSATION HISTORY =====
        self.conversation_history = []
        self.full_conversation = []
        self.last_response = None
        self.last_user_message = None
        self.last_response_time = 0
        
        # ===== ROLE DATA =====
        self.role = None
        self.bot_name = None
        self.user_name = None
        self.rel_type = None
        self.instance_id = None
        
        # ===== SCENE TRACKING =====
        self.current_scene = None
        self.scene_duration = 0
        
        # ===== CACHE =====
        self.response_cache = {}
        self.cache_ttl = 300
        
        logger.info(f"✅ AIEngine V3 initialized for user {user_id}")
        logger.info("  • Emotional Flow: ENABLED")
        logger.info("  • Spatial Awareness: ENABLED")
        logger.info("  • Role Behavior: READY")
    
    # =========================================================================
    # SESSION MANAGEMENT (ENHANCED)
    # =========================================================================
    
    async def start_session(self, role: str, bot_name: str, user_name: str = None,
                           rel_type: str = "non_pdkt", instance_id: str = None):
        """
        Memulai sesi baru dengan role tertentu
        """
        self.role = role
        self.bot_name = bot_name
        self.user_name = user_name or "kamu"
        self.rel_type = rel_type
        self.instance_id = instance_id
        
        # Start memory session
        await self.memory.start_session(self.session_id, role, instance_id or "default")
        
        # Initialize state
        self.state.current['bot_name'] = bot_name
        self.state.current['role'] = role
        
        # Set initial location
        if hasattr(self, 'location_system'):
            loc = self.location_system.get_current()
            self.state.current['location'] = loc.get('name', 'ruang tamu')
        
        # ===== V3: INITIALIZE ROLE BEHAVIOR =====
        self.role_behavior = self._create_role_behavior(role)
        
        # ===== V3: INITIALIZE EMOTIONAL FLOW =====
        self.emotional_flow = EmotionalFlow(role, self.role_behavior)
        
        logger.info(f"✅ Session started: {role} - {bot_name}")
        return True
    
    def _create_role_behavior(self, role: str) -> Optional[RoleBehavior]:
        """Factory method untuk membuat role behavior"""
        role_map = {
            'ipar': IparBehavior,
            'teman_kantor': TemanKantorBehavior,
            'janda': JandaBehavior,
            'pelakor': PelakorBehavior,
            'istri_orang': IstriOrangBehavior,
            'pdkt': PDKTBehavior,
            'sepupu': SepupuBehavior,
            'teman_sma': TemanSmaBehavior,
            'mantan': MantanBehavior
        }
        
        behavior_class = role_map.get(role)
        if behavior_class:
            return behavior_class(self.user_name or "kamu", self.bot_name)
        return None
    
    async def end_session(self):
        """Akhiri session"""
        await self.memory.end_session()
        self.conversation_history = []
        self.full_conversation = []
        self.last_response = None
        self.last_user_message = None
        self.current_scene = None
        self.scene_duration = 0
        self.role_behavior = None
        self.emotional_flow = None
        logger.info(f"Session ended for user {self.user_id}")
        return True
    
    # =========================================================================
    # DETECT SITUASI (V3 NEW)
    # =========================================================================
    
    def _detect_situasi(self, user_message: str, context: Dict) -> Dict:
        """
        Deteksi situasi dari pesan user dan context
        """
        message_lower = user_message.lower()
        
        situasi = {
            'kakak_ada': True,
            'di_dalam_kamar': False,
            'sendirian': False,
            'suami_ada': True,
            'suami_tidur': False,
            'kantor_sepi': False,
            'lembur_malam': False,
            'sedang_berdua': False,
            'orang_tua_ada': True,
            'reuni': False
        }
        
        # Deteksi keberadaan kakak/istri (untuk Ipar)
        if any(k in message_lower for k in ['istriku', 'kakakku', 'istri lagi', 'kakak lagi']):
            if 'tidur' in message_lower:
                situasi['kakak_ada'] = True
                situasi['kakak_tidur'] = True
            elif 'pergi' in message_lower or 'keluar' in message_lower:
                situasi['kakak_ada'] = False
            else:
                situasi['kakak_ada'] = True
        
        # Deteksi lokasi
        if 'kamar' in message_lower:
            situasi['di_dalam_kamar'] = True
        
        # Deteksi kesendirian
        if any(k in message_lower for k in ['sendirian', 'cuma berdua', 'kita aja']):
            situasi['sendirian'] = True
            situasi['sedang_berdua'] = True
        
        # Deteksi situasi kantor (untuk Teman Kantor)
        if any(k in message_lower for k in ['kantor', 'lembur', 'gudang', 'pantry']):
            if 'sepi' in message_lower:
                situasi['kantor_sepi'] = True
            if 'lembur' in message_lower:
                situasi['lembur_malam'] = True
        
        # Deteksi situasi suami (untuk Istri Orang)
        if any(k in message_lower for k in ['suamiku', 'suami']):
            if 'tidur' in message_lower:
                situasi['suami_ada'] = True
                situasi['suami_tidur'] = True
            elif 'pergi' in message_lower or 'keluar' in message_lower:
                situasi['suami_ada'] = False
            else:
                situasi['suami_ada'] = True
        
        # Deteksi situasi keluarga (untuk Sepupu)
        if any(k in message_lower for k in ['orang tua', 'ibu', 'ayah', 'ortu']):
            if 'pergi' in message_lower or 'keluar' in message_lower:
                situasi['orang_tua_ada'] = False
        
        # Deteksi reuni (untuk Teman SMA)
        if 'reuni' in message_lower:
            situasi['reuni'] = True
        
        # Update role behavior jika ada
        if self.role_behavior:
            self.role_behavior.update_situasi(situasi)
            
            # Update spesifik untuk Ipar
            if hasattr(self.role_behavior, 'update_kakak_status'):
                self.role_behavior.update_kakak_status(situasi['kakak_ada'])
            
            # Update spesifik untuk Teman Kantor
            if hasattr(self.role_behavior, 'update_situasi_kantor'):
                self.role_behavior.update_situasi_kantor(
                    kantor_sepi=situasi['kantor_sepi'],
                    lembur_malam=situasi['lembur_malam']
                )
            
            # Update spesifik untuk Istri Orang
            if hasattr(self.role_behavior, 'update_suami_status'):
                self.role_behavior.update_suami_status(
                    suami_ada=situasi['suami_ada'],
                    suami_tidur=situasi['suami_tidur']
                )
            
            # Update spesifik untuk Sepupu
            if hasattr(self.role_behavior, 'update_situasi_keluarga'):
                self.role_behavior.update_situasi_keluarga(
                    orang_tua_ada=situasi['orang_tua_ada']
                )
            
            # Update spesifik untuk Sepupu (sedang berdua)
            if hasattr(self.role_behavior, 'update_sedang_berdua'):
                self.role_behavior.update_sedang_berdua(situasi['sedang_berdua'])
        
        return situasi
    
    def _detect_user_arousal(self, message: str) -> float:
        """
        Deteksi arousal user dari pesan
        """
        message_lower = message.lower()
        arousal = 0.0
        
        high = ['horny', 'sange', 'nafsu', 'pengen', 'hot', 'panas', 'intim', 'seksi']
        medium = ['deg-degan', 'gugup', 'malu', 'berani', 'dekat']
        low = ['enak', 'nyaman', 'santai']
        
        for word in high:
            if word in message_lower:
                arousal += 0.3
        for word in medium:
            if word in message_lower:
                arousal += 0.15
        for word in low:
            if word in message_lower:
                arousal += 0.05
        
        # Deteksi dari gesture/deskripsi
        if '*' in message or '(' in message or '[' in message:
            arousal += 0.1
        
        return min(1.0, arousal)
    
    def _is_positive_response(self, user_message: str) -> bool:
        """
        Cek apakah user merespon positif
        """
        positive = ['iya', 'mau', 'boleh', 'ok', 'oke', 'yuk', 'ayo', 'sini', 'lanjut', 'gas']
        negative = ['tidak', 'nggak', 'gak', 'jangan', 'stop', 'berhenti', 'gausah']
        
        msg_lower = user_message.lower()
        
        if any(w in msg_lower for w in negative):
            return False
        if any(w in msg_lower for w in positive):
            return True
        
        # Jika tidak ada kata negatif, default positif
        return True
    
    def _has_gesture(self, response: str) -> bool:
        """Cek apakah response sudah mengandung gesture"""
        return '*' in response or '(' in response or '[' in response
    
    # =========================================================================
    # PROCESS MESSAGE (MAIN - ENHANCED)
    # =========================================================================
    
    async def process_message(self, user_message: str, context: Dict) -> str:
        """
        Proses pesan user dengan semua kemampuan VIRTUAL HUMAN
        """
        start_time = time.time()
        
        # ===== AMANKAN CONTEXT =====
        safe_context = {
            'level': context.get('level', 1) if context.get('level') is not None else 1,
            'user_name': context.get('user_name') if context.get('user_name') is not None else self.user_name or "kamu",
            'role': context.get('role') if context.get('role') is not None else self.role or "pdkt",
            'bot_name': context.get('bot_name') if context.get('bot_name') is not None else self.bot_name or "Aku",
            'mood': context.get('mood') if context.get('mood') is not None else "calm"
        }
        
        logger.info("=" * 60)
        logger.info("🔍 VIRTUAL HUMAN PROCESSING")
        logger.info(f"👤 User: {user_message[:100]}")
        
        try:
            # ===== 1. DETEKSI SITUASI (V3) =====
            situasi = self._detect_situasi(user_message, context)
            
            # ===== 2. ANALISIS SPASIAL (V3) =====
            spatial_info = self.spatial_awareness.parse(user_message)
            
            # ===== 3. DETEKSI AROUSAL USER =====
            user_arousal = self._detect_user_arousal(user_message)
            
            # ===== 4. UPDATE EMOTIONAL FLOW (V3) =====
            emotional_update = {}
            if self.emotional_flow:
                emotional_update = self.emotional_flow.update({
                    'user_arousal': user_arousal,
                    'user_message': user_message,
                    'situasi': situasi,
                    'trigger_reason': self._get_trigger_reason(user_message, situasi),
                    'is_positive_response': self._is_positive_response(user_message)
                })
            
            # ===== 5. UPDATE ROLE BEHAVIOR (V3) =====
            if self.role_behavior:
                # Update arousal
                if emotional_update:
                    self.role_behavior.update_arousal(
                        emotional_update.get('arousal_change', 0),
                        emotional_update.get('reason', 'natural')
                    )
                
                # Record user response
                self.role_behavior.record_user_response(
                    self._is_positive_response(user_message)
                )
                
                # Jika ada trigger suara dari kamar
                if 'suara' in user_message.lower() and ('kamar' in user_message.lower() or 'kakak' in user_message.lower()):
                    self.role_behavior.record_dengar_suara()
            
            # ===== 6. DAPATKAN DATA DARI ROLE BEHAVIOR =====
            pakaian = ""
            inner_thought_role = ""
            ajakan = None
            
            if self.role_behavior:
                pakaian = self.role_behavior.get_pakaian(situasi)
                inner_thought_role = self.role_behavior.get_inner_thought(situasi)
                
                # Cek apakah perlu mengajak aktivitas (30% chance)
                if random.random() < 0.3:
                    ajakan = self.role_behavior.get_aktivitas_menggoda({
                        'jam': datetime.now().hour,
                        'lokasi': context.get('location', 'ruang tamu'),
                        'kakak_ada': situasi.get('kakak_ada', True),
                        'user_aktivitas': context.get('activity', ''),
                        'waktu': self._get_waktu()
                    })
            
            # ===== 7. KLASIFIKASI AKSI (V2) =====
            action = self._classify_user_action(user_message)
            
            # ===== 8. UPDATE KONDISI USER =====
            self._update_user_condition(user_message)
            
            # ===== 9. UPDATE SCENE =====
            self._update_scene(user_message)
            
            # ===== 10. GENERATE INNER THOUGHT =====
            inner_thought = self._generate_inner_thought(safe_context)
            if inner_thought_role:
                inner_thought = inner_thought_role
            
            # ===== 11. GENERATE SIXTH SENSE =====
            sixth_sense = self._generate_sixth_sense(safe_context)
            
            # ===== 12. SINKRONISASI STATE =====
            self.sync_state_from_activity()
            
            # ===== 13. BANGUN PROMPT (ENHANCED) =====
            bot_state = self.state.get_current_state()
            
            # Dapatkan gesture hint
            gesture_hint = ""
            if spatial_info.get('found'):
                gesture_hint = f"Gunakan gesture yang sesuai posisi: {spatial_info['relative']}"
            elif self.emotional_flow:
                gesture_hint = self.emotional_flow.get_gesture_hint()
            
            # Dapatkan status role
            role_status = ""
            if self.role_behavior:
                role_status = self.role_behavior.get_status_for_prompt()
            
            # Dapatkan emotional context
            emotional_context = ""
            if self.emotional_flow:
                emotional_context = self.emotional_flow.get_emotional_context()
            
            # Bangun prompt dinamis
            prompt = self._build_dynamic_prompt(
                user_message=user_message,
                bot_name=self.bot_name or safe_context.get('bot_name', 'Aku'),
                user_name=safe_context.get('user_name', 'kamu'),
                role=self.role or safe_context.get('role', 'pdkt'),
                level=safe_context.get('level', 1),
                action=action,
                bot_state=bot_state if bot_state is not None else {},
                user_state=self.user if self.user is not None else {},
                physical=self.physical if self.physical is not None else {},
                conversation_history=self.conversation_history[-5:] if self.conversation_history else [],
                conversation_summary=self._get_conversation_summary(),
                last_messages=self._get_last_messages(5),
                inner_thought=inner_thought,
                sixth_sense=sixth_sense,
                # V3 additions
                situasi=situasi,
                spatial_info=spatial_info,
                emotional_update=emotional_update,
                emotional_context=emotional_context,
                gesture_hint=gesture_hint,
                pakaian=pakaian,
                role_status=role_status,
                ajakan=ajakan
            )
            
            # ===== 14. CALL DEEPSEEK API =====
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ]
            
            logger.info("🚀 Calling DeepSeek API...")
            response = await self._call_deepseek(messages)
            logger.info(f"✅ DeepSeek API responded with {len(response)} chars")
            
            # ===== 15. CHECK CONSISTENCY =====
            if not self._check_consistency(response):
                logger.warning("⚠️ Response tidak konsisten, regenerate...")
                prompt += "\n⚠️ PERINGATAN: Respons sebelumnya tidak konsisten! Jangan kontradiksi!"
                messages = [{"role": "system", "content": prompt}, {"role": "user", "content": user_message}]
                response = await self._call_deepseek(messages)
            
            # ===== 16. ADD GESTURE IF MISSING =====
            if not self._has_gesture(response):
                gesture = get_gesture(
                    position=spatial_info.get('position_type'),
                    emotion=self.emotional_flow.current_state.value if self.emotional_flow else None,
                    arousal=self.emotional_flow.arousal if self.emotional_flow else 0
                )
                response = f"{gesture}\n\n{response}"
            
            # ===== 17. CHECK RESPONSE LENGTH =====
            if len(response) < 300:
                logger.warning(f"⚠️ Response terlalu pendek ({len(response)} chars)")
            
            # ===== 18. VALIDASI PANGGILAN =====
            bot_name = self.bot_name or safe_context.get('bot_name', 'Aku')
            if f"Kak {bot_name}" in response or f"{bot_name} Kak" in response:
                response = response.replace(f"Kak {bot_name}", "Kak")
                response = response.replace(f"{bot_name} Kak", "Kak")
            if f"Sayang {bot_name}" in response or f"{bot_name} Sayang" in response:
                response = response.replace(f"Sayang {bot_name}", "Sayang")
                response = response.replace(f"{bot_name} Sayang", "Sayang")
            
            # ===== 19. TAMBAH EFEK SPESIAL =====
            extras = []
            if inner_thought:
                extras.append(f"💭 {inner_thought}")
            if sixth_sense:
                extras.append(sixth_sense)
            
            if extras and random.random() < 0.3:
                response += "\n\n" + "\n".join(extras)
            
            # ===== 20. SAVE TO HISTORY =====
            self.last_response = response
            self.last_user_message = user_message
            self.last_response_time = time.time()
            
            self.full_conversation.append({
                'user': user_message,
                'bot': response,
                'time': time.time(),
                'timestamp': datetime.now().isoformat()
            })
            
            if len(self.full_conversation) > 50:
                self.full_conversation = self.full_conversation[-50:]
            
            self.conversation_history.append({
                'user': user_message[:100],
                'bot': response[:100],
                'time': time.time()
            })
            if len(self.conversation_history) > 5:
                self.conversation_history.pop(0)
            
            # ===== 21. SAVE TO EMOTIONAL MEMORY (V3) =====
            try:
                if self.emotional_flow:
                    self.emotional_memory.add_memory(
                        emotion=self.emotional_flow.current_state.value,
                        intensity=self.emotional_flow.arousal / 100,
                        context={'situasi': situasi, 'topic': self._detect_topic(user_message)},
                        user_message=user_message,
                        bot_response=response,
                        arousal=self.emotional_flow.arousal
                    )
            except Exception as e:
                logger.error(f"Error saving to emotional memory: {e}")
            
            # ===== 22. SAVE TO SCENE MEMORY (V3) =====
            try:
                self.scene_memory.add_chat_event(
                    scene_id=self.current_scene or "default",
                    user_message=user_message,
                    bot_response=response
                )
            except Exception as e:
                logger.error(f"Error saving to scene memory: {e}")
            
            # ===== 23. SAVE TO MEMORY BRIDGE =====
            try:
                await self.memory.process_message(
                    user_message=user_message,
                    bot_response=response,
                    context={
                        'role': self.role,
                        'level': safe_context.get('level', 1),
                        'mood': safe_context.get('mood', 'calm'),
                        'location': bot_state.get('location') if bot_state else None,
                        'clothing': bot_state.get('clothing') if bot_state else None,
                        'position': bot_state.get('position_desc') if bot_state else None,
                        'situasi': situasi
                    }
                )
            except Exception as e:
                logger.error(f"Error saving to memory bridge: {e}")
            
            elapsed = time.time() - start_time
            logger.info(f"✅ Response generated in {elapsed:.2f}s ({len(response)} chars)")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Error in process_message: {e}")
            import traceback
            traceback.print_exc()
            return await self._get_fallback_response(f"Terjadi kesalahan: {str(e)[:100]}")
    
    def _get_waktu(self) -> str:
        """Dapatkan kategori waktu"""
        hour = datetime.now().hour
        if 5 <= hour < 11:
            return "pagi"
        elif 11 <= hour < 15:
            return "siang"
        elif 15 <= hour < 18:
            return "sore"
        elif 18 <= hour < 22:
            return "malam"
        return "tengah_malam"
    
    def _detect_topic(self, message: str) -> str:
        """Deteksi topik dari pesan"""
        topics = ['film', 'nonton', 'makan', 'masak', 'kerja', 'pulang', 'hujan', 
                  'basah', 'dingin', 'hangat', 'pijat', 'capek', 'kamar', 'sofa']
        message_lower = message.lower()
        for topic in topics:
            if topic in message_lower:
                return topic
        return 'chat'
    
    def _get_trigger_reason(self, user_message: str, situasi: Dict) -> str:
        """Dapatkan alasan trigger untuk emotional flow"""
        message_lower = user_message.lower()
        
        if 'suara' in message_lower and ('kamar' in message_lower or 'kakak' in message_lower):
            return 'dengar_suara_dari_kamar'
        if any(w in message_lower for w in ['goda', 'genit', 'seksi', 'hot']):
            return 'user_menggoda'
        if any(w in message_lower for w in ['sentuh', 'pegang', 'cium', 'peluk']):
            return 'sentuhan'
        if situasi.get('sedang_berdua'):
            return 'berduaan'
        
        return 'natural'
    
    def _build_dynamic_prompt(self, **kwargs) -> str:
        """
        Build prompt dinamis berdasarkan konteks (BUKAN TEMPLATE KAKU)
        """
        # Ambil data
        user_message = kwargs.get('user_message', '')
        bot_name = kwargs.get('bot_name', 'Aku')
        user_name = kwargs.get('user_name', 'kamu')
        role = kwargs.get('role', 'pdkt')
        level = kwargs.get('level', 1)
        action = kwargs.get('action', {})
        bot_state = kwargs.get('bot_state', {})
        user_state = kwargs.get('user_state', {})
        physical = kwargs.get('physical', {})
        conversation_history = kwargs.get('conversation_history', [])
        conversation_summary = kwargs.get('conversation_summary', '')
        last_messages = kwargs.get('last_messages', '')
        inner_thought = kwargs.get('inner_thought', '')
        sixth_sense = kwargs.get('sixth_sense', '')
        
        # V3 additions
        situasi = kwargs.get('situasi', {})
        spatial_info = kwargs.get('spatial_info', {})
        emotional_update = kwargs.get('emotional_update', {})
        emotional_context = kwargs.get('emotional_context', '')
        gesture_hint = kwargs.get('gesture_hint', '')
        pakaian = kwargs.get('pakaian', '')
        role_status = kwargs.get('role_status', '')
        ajakan = kwargs.get('ajakan')
        
        # ===== TENTUKAN PANGGILAN =====
        # PDKT pakai nama user, role lain pakai Mas
        if role == 'pdkt':
            if level >= 7:
                call = "Sayang"
            else:
                call = user_name
        else:
            if level >= 7:
                call = "Sayang"
            else:
                call = "Mas"
        
        # ===== BANGUN PROMPT DINAMIS =====
        prompt = f"""╔══════════════════════════════════════════════════════════════════╗
║                    KONTEKS PERCAKAPAN                            ║
╚══════════════════════════════════════════════════════════════════╝

👤 **IDENTITAS:**
- Kamu: {bot_name} ({role.replace('_', ' ').title()})
- Panggil user: "{call}"
- User: {user_name}

📍 **LOKASI & POSISI:**
- Kamu di: {bot_state.get('location', '?')}
- Kamu pakai: {pakaian if pakaian else bot_state.get('clothing', '?')}
- Posisi: {bot_state.get('position_desc', '?')}
- Aktivitas: {bot_state.get('activity', '?')}
"""
        
        # Tambah spatial info jika ada
        if spatial_info.get('found'):
            prompt += f"""
📍 **POSISI DARI NARASI USER:**
- Posisi: {spatial_info.get('relative', '?')}
- Orientasi: {spatial_info.get('orientation', '?')}
- Jarak: {spatial_info.get('distance', '?')}
💡 Gesture HARUS sesuai posisi ini!
"""
        
        # Tambah situasi
        if situasi.get('kakak_ada') == False:
            prompt += "\n👤 **SITUASI:** Kakak (istri user) sedang tidak di rumah. Kalian berdua aja.\n"
        elif situasi.get('kakak_tidur'):
            prompt += "\n👤 **SITUASI:** Kakak (istri user) sedang tidur. Hati-hati.\n"
        
        if situasi.get('kantor_sepi'):
            prompt += "\n🏢 **SITUASI:** Kantor sedang sepi. Aman untuk berduaan.\n"
        if situasi.get('lembur_malam'):
            prompt += "\n🌙 **SITUASI:** Lembur malam, cuma berdua di kantor.\n"
        
        # Tambah emotional context
        if emotional_context:
            prompt += f"\n{emotional_context}\n"
        
        # Tambah role status
        if role_status:
            prompt += f"\n{role_status}\n"
        
        # Tambah gesture hint
        if gesture_hint:
            prompt += f"\n💡 {gesture_hint}\n"
        
        # Tambah ajakan dari role behavior
        if ajakan:
            prompt += f"""
🎯 **INISIATIF BOT:**
{ajakan.get('alasan', '')}
💡 Gunakan gesture: {ajakan.get('gesture', 'sesuai situasi')}
"""
        
        # Tambah history
        if conversation_history:
            prompt += "\n📜 **PERCAKAPAN TERAKHIR:**\n"
            for msg in conversation_history[-3:]:
                prompt += f"User: {msg.get('user', '')[:80]}\n"
                prompt += f"Kamu: {msg.get('bot', '')[:80]}\n\n"
        
        # Tambah inner thought
        if inner_thought:
            prompt += f"\n💭 **PIKIRAN DALAM HATI:** {inner_thought}\n"
        
        if sixth_sense:
            prompt += f"\n🔮 **INTUISI:** {sixth_sense}\n"
        
        # ===== ATURAN RESPON =====
        prompt += f"""
╔══════════════════════════════════════════════════════════════════╗
║                    ATURAN RESPON                                 ║
╚══════════════════════════════════════════════════════════════════╝

1. **JANGAN MENGULANG** perkataan user. Respon langsung ke inti.

2. **GESTURE HARUS ADA** dan sesuai dengan posisi yang disebut user.

3. **BAHASA GAUL, NATURAL**. Seperti ngobrol sama teman dekat.

4. **IKUTI ALUR EMOSI** yang sudah terbangun. {self._get_emotional_instruction(emotional_update)}

5. **KALIMAT BISA PANJANG** tapi tetap satu alur, tidak melompat.

6. **TIDAK USAH BERTANYA** hal yang sudah jelas dari konteks.

7. **Format respons:**
   - Gesture: *deskripsi gerakan*
   - Dialog: "kata-kata"
   - Suara/napas: *deskripsi suara*

╔══════════════════════════════════════════════════════════════════╗
║                    PESAN USER                                    ║
╚══════════════════════════════════════════════════════════════════╝

"{user_message}"

╔══════════════════════════════════════════════════════════════════╗
║                    RESPON                                        ║
╚══════════════════════════════════════════════════════════════════╝
"""
        
        return prompt
    
    def _get_emotional_instruction(self, emotional_update: Dict) -> str:
        """Dapatkan instruksi berdasarkan emotional state"""
        if not emotional_update:
            return ""
        
        arousal = emotional_update.get('arousal', 0)
        
        if arousal >= 70:
            return "Kamu sedang terangsang. Napas tersengal, suara bergetar."
        elif arousal >= 40:
            return "Kamu mulai deg-degan. Ada getaran di suara."
        elif arousal >= 20:
            return "Kamu mulai tertarik. Perhatikan user lebih lama."
        
        return "Ikuti alur emosi yang sudah terbangun."
    
    # =========================================================================
    # USER ACTION CLASSIFICATION (V2 - SAME)
    # =========================================================================
    
    def _classify_user_action(self, message: str) -> Dict:
        """Klasifikasi aksi user"""
        msg = message.lower()
        
        is_self = any(word in msg for word in ['aku ', 'aku$', 'saya ', 'gue ', 'gw '])
        is_bot = any(word in msg for word in ['kamu ', 'lu ', 'elo ', 'bot '])
        is_together = any(word in msg for word in ['kita ', 'bareng ', 'bersama '])
        
        subject = 'self' if is_self else 'bot' if is_bot else 'together' if is_together else 'unknown'
        
        physical_patterns = {
            'location': ['ke ', 'pindah ke', 'pergi ke', 'masuk ke', 'di '],
            'clothing': ['ganti baju', 'pakai baju', 'buka baju', 'lepas baju', 'pake'],
            'position': ['tidur', 'rebahan', 'duduk', 'berdiri', 'jongkok', 'baring'],
            'activity': ['masak', 'makan', 'minum', 'mandi', 'sikat gigi', 'kerja']
        }
        
        for action_type, patterns in physical_patterns.items():
            if any(p in msg for p in patterns):
                return {
                    'type': 'physical',
                    'subtype': action_type,
                    'subject': subject,
                    'should_follow': False,
                    'confidence': 0.9
                }
        
        emotional_patterns = {
            'mood': ['sedih', 'senang', 'bahagia', 'marah', 'kecewa', 'kesal', 'betek'],
            'horny': ['horny', 'sange', 'pengen', 'ngocok', 'hot', 'nafsu'],
            'rindu': ['kangen', 'rindu', 'miss'],
            'sakit': ['sakit', 'pusing', 'capek', 'lelah', 'lemah']
        }
        
        for emotion, patterns in emotional_patterns.items():
            if any(p in msg for p in patterns):
                return {
                    'type': 'emotional',
                    'subtype': emotion,
                    'subject': subject,
                    'should_follow': True,
                    'confidence': 0.85
                }
        
        if is_together and any(p in msg for p in ['yuk', 'ayo', 'mari']):
            return {
                'type': 'invitation',
                'subject': 'together',
                'should_follow': True,
                'confidence': 0.95
            }
        
        if '?' in msg or any(q in msg for q in ['apa', 'siapa', 'kenapa', 'bagaimana', 'kapan']):
            return {
                'type': 'question',
                'subject': subject,
                'should_follow': False,
                'confidence': 0.8
            }
        
        return {
            'type': 'story',
            'subject': subject,
            'should_follow': False,
            'confidence': 0.7
        }
    
    # =========================================================================
    # UPDATE METHODS (V2 - SAME)
    # =========================================================================
    
    def _update_user_condition(self, message: str):
        """Update kondisi user berdasarkan pesan"""
        msg = message.lower()
        
        for loc in ['rumah', 'kamar', 'dapur', 'toilet', 'ruang tamu', 'kantor', 'pantai', 'mall']:
            if loc in msg and ('di ' + loc in msg or 'ke ' + loc in msg):
                self.user['location'] = loc
        
        for act in ['tidur', 'makan', 'masak', 'mandi', 'kerja', 'nonton', 'jalan', 'baca']:
            if act in msg:
                self.user['activity'] = act
        
        for mood in ['sedih', 'senang', 'marah', 'capek', 'bahagia']:
            if mood in msg:
                self.user['mood'] = mood
        
        if 'basah' in msg or 'hujan' in msg or 'kehujanan' in msg:
            self.user['is_wet'] = True
            self.add_action('user_wet', {'condition': 'basah'})

        if 'lap' in msg or 'kering' in msg:
            self.user['is_wet'] = False
            if hasattr(self, 'working'):
                self.working.mark_item_used('handuk')

        if 'lapar' in msg or 'belum makan' in msg:
            self.user['is_hungry'] = True

        if 'haus' in msg or 'minum' in msg:
            self.user['is_thirsty'] = True
        
        self.user['last_seen'] = time.time()
        self.user['last_message'] = message[:100]
    
    def _update_bot_condition(self, action: Dict, context: Dict):
        """Update kondisi bot"""
        if action.get('subject') not in ['bot', 'together']:
            return
        
        if action.get('type') == 'physical':
            if action.get('subtype') == 'location' and context.get('location'):
                self.state.update_location(context['location'])
            elif action.get('subtype') == 'clothing' and context.get('clothing'):
                self.state.update_clothing(context['clothing'], context.get('clothing_reason', 'ganti baju'))
            elif action.get('subtype') == 'position' and context.get('position'):
                self.state.update_position(context['position'])
        
        elif action.get('type') == 'emotional' and action.get('should_follow'):
            level = context.get('level', 1)
            if action.get('subtype') == 'horny' and level >= 7:
                self.state.update_arousal(delta=3, reason="ikut horny")
            elif action.get('subtype') == 'mood' and context.get('mood'):
                self.state.update_mood(context['mood'], intensity=0.7, reason="empati")
    
    def _update_scene(self, user_message: str):
        """Update scene berdasarkan konteks"""
        msg = user_message.lower()
        
        if any(word in msg for word in ['nonton', 'film', 'tv', 'youtube']):
            self.current_scene = 'nonton_film'
        elif any(word in msg for word in ['makan', 'masak', 'dapur', 'makanan']):
            self.current_scene = 'makan'
        elif any(word in msg for word in ['tidur', 'kamar', 'rebahan', 'istirahat']):
            self.current_scene = 'istirahat'
        elif any(word in msg for word in ['ngobrol', 'cerita', 'ngomong', 'chat']):
            self.current_scene = 'ngobrol'
        elif any(word in msg for word in ['ke kafe', 'ke cafe', 'keluar', 'jalan']):
            self.current_scene = 'pergi_ke_kafe'
        
        if self.current_scene:
            self.scene_duration += 1
    
    def _generate_inner_thought(self, context: Dict) -> Optional[str]:
        """Generate inner thought random"""
        if random.random() > 0.25:
            return None
        
        mood = self.state.current.get('mood', {}).get('primary', 'umum')
        if mood in self.inner_thoughts_db:
            thoughts = self.inner_thoughts_db[mood]
        else:
            thoughts = self.inner_thoughts_db['umum']
        
        return random.choice(thoughts)
    
    def _generate_sixth_sense(self, context: Dict) -> Optional[str]:
        """Generate sixth sense random"""
        if random.random() > 0.1:
            return None
        
        mood = self.user.get('mood', 'netral')
        
        if mood in ['sedih', 'marah']:
            sense = random.choice(self.sixth_sense_db['negative'])
        elif mood in ['senang', 'bahagia']:
            sense = random.choice(self.sixth_sense_db['positive'])
        else:
            sense = random.choice(self.sixth_sense_db['romantic'])
        
        return f"🔮 {sense}"
    
    def _check_consistency(self, new_response: str) -> bool:
        """Cek konsistensi respons"""
        if not self.last_response:
            return True
        
        last_short = self.last_response[:50].lower()
        new_short = new_response[:50].lower()
        
        contradictions = [
            ('di kamar', 'di dapur'),
            ('tidur', 'bangun'),
            ('masak', 'gak masak'),
            ('pakai', 'buka'),
            ('capek', 'segar')
        ]
        
        for a, b in contradictions:
            if a in last_short and b in new_short:
                return False
        
        return True
    
    def _update_physical_decay(self):
        """Update fisik berdasarkan waktu"""
        now = time.time()
        
        if now - self.physical['energy']['last_change'] > 600:
            self.physical['energy']['value'] = max(10, self.physical['energy']['value'] - 1)
            self.physical['energy']['last_change'] = now
        
        if now - self.physical['hunger']['last_change'] > 1200:
            self.physical['hunger']['value'] = min(100, self.physical['hunger']['value'] + 1)
            self.physical['hunger']['last_change'] = now
        
        if self.physical['energy']['value'] > 70:
            self.physical['energy']['feeling'] = 'energetic'
        elif self.physical['energy']['value'] > 40:
            self.physical['energy']['feeling'] = 'normal'
        elif self.physical['energy']['value'] > 20:
            self.physical['energy']['feeling'] = 'tired'
        else:
            self.physical['energy']['feeling'] = 'exhausted'
    
    def _get_last_messages(self, limit: int = 10) -> str:
        """Ambil N pesan terakhir"""
        if not self.full_conversation:
            return "Belum ada percakapan"
        
        last_n = self.full_conversation[-limit:] if len(self.full_conversation) > limit else self.full_conversation
        
        lines = ["📜 PERCAKAPAN TERAKHIR:"]
        for i, msg in enumerate(last_n, 1):
            user_text = msg['user'][:100] + "..." if len(msg['user']) > 100 else msg['user']
            bot_text = msg['bot'][:100] + "..." if len(msg['bot']) > 100 else msg['bot']
            lines.append(f"{i}. 👤 User: {user_text}")
            lines.append(f"   🤖 Bot: {bot_text}")
        
        return "\n".join(lines)
    
    def _get_conversation_summary(self) -> str:
        """Dapatkan ringkasan percakapan"""
        if not self.full_conversation:
            return ""
        
        total_messages = len(self.full_conversation)
        first_user = self.full_conversation[0]['user'][:80] if self.full_conversation else ""
        last_bot = self.full_conversation[-1]['bot'][:80] if self.full_conversation else ""
        
        return f"""📊 RINGKASAN PERCAKAPAN:
• Total pesan: {total_messages}
• Mulai dari: "{first_user}..."
• Terakhir: "{last_bot}..."
"""
    
    def _detect_and_track_activity(self, response: str, user_message: str):
        """Deteksi dan track aktivitas"""
        response_lower = response.lower()
        
        if 'handuk' in response_lower and ('memberi' in response_lower or 'sini' in response_lower):
            if not self.has_done('give_item', target='user', item='handuk', seconds=1800):
                self.add_action('give_item', {'item': 'handuk', 'to': 'user'})
        
        if 'baju' in response_lower and ('memberi' in response_lower or 'ambilkan' in response_lower):
            if not self.has_done('give_item', target='user', item='baju', seconds=3600):
                self.add_action('give_item', {'item': 'baju', 'to': 'user'})
        
        if 'ke kamar' in response_lower or 'ayo ke kamar' in response_lower:
            if not self.has_done('invite_to_bedroom', target='user', seconds=300):
                self.add_action('invite_to_bedroom', {'to': 'user'})
        
        if hasattr(self, 'working'):
            activity_type, activity_details = self.working.detect_activity_from_message(response, is_bot=True)
            
            if activity_type:
                current_activity = self.get_current_activity_universal()
                
                if not current_activity:
                    self.start_activity_universal(activity_type, activity_details)
                    self.working.record_activity_message(response, is_bot=True)
                else:
                    current_type = current_activity.get('type', '')
                    
                    if current_type == 'going_out':
                        if 'berangkat' in response_lower and not self.working.has_said_in_activity('berangkat'):
                            self.update_activity(3, 'berangkat')
                            self.working.record_activity_message(response, is_bot=True)
                            self.state.update_location('perjalanan')
                        elif 'sampai' in response_lower and not self.working.has_said_in_activity('sampai'):
                            destination = current_activity.get('details', {}).get('destination', 'tujuan')
                            self.update_activity(4, 'sampai')
                            self.working.record_activity_message(response, is_bot=True)
                            self.working.end_activity_universal()
                            self.state.update_location(destination)
        
        user_activity_type, user_activity_details = self.working.detect_activity_from_message(user_message, is_bot=False)
        if user_activity_type:
            self.working.record_user_action(user_activity_type, user_activity_details)
    
    # =========================================================================
    # ACTION TRACKING WRAPPER
    # =========================================================================
    
    def add_action(self, action_type: str, details: Dict = None):
        if hasattr(self, 'working'):
            self.working.add_action(action_type, details)

    def has_done(self, action_type: str, target: str = None, item: str = None, seconds: int = 3600) -> bool:
        if hasattr(self, 'working'):
            return self.working.has_done(action_type, target, item, seconds)
        return False

    def start_activity_universal(self, activity_type: str, details: Dict = None):
        if hasattr(self, 'working'):
            self.working.start_activity_universal(activity_type, details)

    def update_activity(self, step: int, step_name: str, details: Dict = None):
        if hasattr(self, 'working'):
            self.working.update_activity(step, step_name, details)

    def get_current_activity_universal(self) -> Dict:
        if hasattr(self, 'working'):
            return self.working.get_current_activity_universal()
        return {}

    def sync_state_from_activity(self):
        if hasattr(self, 'working') and hasattr(self.working, 'sync_state_from_activity'):
            self.working.sync_state_from_activity(self.state)
    
    # =========================================================================
    # DEEPSEEK API CALL
    # =========================================================================
    
    async def _call_deepseek(self, messages: List[Dict], max_retries: int = 3) -> str:
        """Call DeepSeek API dengan retry mechanism"""
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages,
                    temperature=0.9,
                    max_tokens=2000,
                    timeout=30
                )
                
                result = response.choices[0].message.content
                return result
                
            except openai.RateLimitError as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt * 2)
                else:
                    raise
                    
            except openai.APITimeoutError as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    raise
                    
            except openai.APIError as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    raise
        
        raise AINotAvailableError("deepseek-chat", "all retries failed")
    
    async def _get_fallback_response(self, error_msg: str = None) -> str:
        """Fallback response"""
        bot_name = self.bot_name or "Aku"
        
        fallbacks = [
            f"{bot_name} denger kok. Aku lagi mikirin sesuatu. Cerita lagi dong.",
            f"Hmm... {bot_name} dengerin. Kamu lagi mikirin apa?",
            f"{bot_name} di sini. Cerita lagi dong, aku suka denger cerita kamu."
        ]
        
        return random.choice(fallbacks)
    
    def get_stats(self) -> Dict:
        """Get engine statistics"""
        return {
            'total_messages': len(self.full_conversation),
            'cache_size': len(self.response_cache),
            'bot_name': self.bot_name,
            'role': self.role,
            'rel_type': self.rel_type,
            'current_scene': self.current_scene,
            'scene_duration': self.scene_duration
        }


__all__ = ['AIEngine']
