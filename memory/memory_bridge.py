#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - MEMORY BRIDGE
=============================================================================
Menghubungkan semua sistem memory menjadi satu kesatuan
- Mengintegrasikan working, episodic, semantic, compact, forgetting
- Menyediakan interface seragam untuk mengambil/menyimpan memory
- Untuk single user dengan realisme tinggi
=============================================================================
"""

import time
import logging
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from .working_memory import WorkingMemory
from .episodic import EpisodicMemory, EpisodeType, EmotionalTag
from .semantic import SemanticMemory, FactCategory, PreferenceType
from .compact_memory import CompactMemory
from .forgetting import SemanticForgetting, ForgetType

logger = logging.getLogger(__name__)


class MemoryType:
    """Tipe memori untuk storage"""
    COMPACT = "compact"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    WORKING = "working"
    RELATIONSHIP = "relationship"


class MemoryImportance:
    """Tingkat kepentingan memori"""
    CRITICAL = 1.0    # Tidak pernah dilupakan (first kiss, first intim)
    HIGH = 0.8        # Jarang dilupakan
    MEDIUM = 0.5      # Bisa dilupakan setelah beberapa waktu
    LOW = 0.2         # Cepat dilupakan


class MemoryBridge:
    """
    Jembatan yang menghubungkan semua sistem memory
    Memberikan akses terpadu ke semua jenis memori
    """
    
    def __init__(self, user_id: int):
        """
        Args:
            user_id: ID user (single user)
        """
        self.user_id = user_id
        
        # Inisialisasi semua sistem memory
        self.working = WorkingMemory()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()
        self.compact = CompactMemory()
        self.forgetting = SemanticForgetting()
        
        # Session aktif
        self.current_session_id = None
        self.current_role = None
        self.current_instance = None
        
        # Buffer untuk konteks percakapan real-time
        self.context_buffer = {
            'location': None,
            'clothing': None,
            'position': None,
            'mood': None,
            'activity': None,
            'last_message': None,
            'last_response': None
        }
        
        # Consolidation schedule
        self.last_consolidation = time.time()
        self.consolidation_interval = 3600  # 1 jam
        
        logger.info(f"✅ MemoryBridge initialized for user {user_id}")
    
    # =========================================================================
    # SESSION MANAGEMENT
    # =========================================================================
    
    async def start_session(self, session_id: str, role: str, instance_id: str = "default"):
        """
        Memulai sesi baru
        
        Args:
            session_id: ID sesi
            role: Role yang aktif
            instance_id: Instance ID (untuk multiple)
        """
        self.current_session_id = session_id
        self.current_role = role
        self.current_instance = instance_id
        
        # Reset context buffer untuk sesi baru
        self.context_buffer = {
            'location': None,
            'clothing': None,
            'position': None,
            'mood': None,
            'activity': None,
            'last_message': None,
            'last_response': None
        }
        
        logger.info(f"Session started: {session_id} ({role})")
    
    async def end_session(self):
        """Mengakhiri sesi"""
        if self.current_session_id:
            # Simpan ringkasan akhir sesi ke compact memory
            await self.compact.add_message(
                user_id=self.user_id,
                session_id=self.current_session_id,
                role=self.current_role,
                user_message="[END_SESSION]",
                bot_message="Session ended",
                context={'action': 'session_end'}
            )
        
        self.current_session_id = None
        self.current_role = None
        self.current_instance = None
        
        logger.info("Session ended")
    
    # =========================================================================
    # PROCESS MESSAGE (MAIN FUNCTION)
    # =========================================================================
    
    async def process_message(self, 
                             user_message: str, 
                             bot_response: str,
                             context: Dict) -> Dict:
        """
        Memproses pesan baru: menyimpan ke semua sistem memory
        
        Args:
            user_message: Pesan user
            bot_response: Respon bot
            context: Konteks percakapan (lokasi, mood, dll)
            
        Returns:
            Dict dengan hasil processing
        """
        if not self.current_session_id:
            raise ValueError("No active session. Call start_session first.")
        
        # Update context buffer
        self._update_context(context)
        
        # 1. Simpan ke working memory
        self.working.add_interaction(user_message, bot_response, self.context_buffer)
        
        # 2. Simpan ke compact memory (ringkasan)
        await self.compact.add_message(
            user_id=self.user_id,
            session_id=self.current_session_id,
            role=self.current_role,
            user_message=user_message,
            bot_message=bot_response,
            context=self.context_buffer
        )
        
        # 3. Ekstrak fakta dari pesan user
        await self.semantic.extract_facts(
            user_id=self.user_id,
            message=user_message,
            role=self.current_role
        )
        
        # 4. Deteksi momen penting untuk episodic memory
        episode = await self._detect_important_moment(
            user_message, 
            bot_response, 
            context
        )
        
        if episode:
            await self.episodic.add_episode(
                user_id=self.user_id,
                role=self.current_role,
                instance_id=self.current_instance,
                episode_type=episode['type'],
                description=episode['description'],
                emotional_tag=episode['emotion'],
                intensity=episode['intensity'],
                context={**self.context_buffer, **context}
            )
        
        # 5. Generate memory ID untuk forgetting tracking
        memory_id = f"MEM_{self.current_session_id}_{int(time.time())}"
        
        # 6. Track untuk forgetting
        await self.forgetting.track_memory(
            memory_id=memory_id,
            memory_type='compact',
            initial_strength=0.8
        )
        
        # 7. Catat akses
        await self.forgetting.access_memory(memory_id)
        
        # 8. Run consolidation periodically
        await self._check_consolidation()
        
        return {
            'memory_id': memory_id,
            'episode_detected': episode is not None,
            'facts_extracted': True,
            'context': self.context_buffer
        }
    
    def _update_context(self, context: Dict):
        """Update context buffer dengan data terbaru"""
        for key in ['location', 'clothing', 'position', 'mood', 'activity']:
            if key in context:
                self.context_buffer[key] = context[key]
        
        if 'message' in context:
            self.context_buffer['last_message'] = context['message']
        
        if 'response' in context:
            self.context_buffer['last_response'] = context['response']
    
    async def _detect_important_moment(self, 
                                      user_message: str, 
                                      bot_response: str,
                                      context: Dict) -> Optional[Dict]:
        """
        Deteksi apakah pesan ini包含 momen penting
        
        Returns:
            Dict episode atau None
        """
        combined = (user_message + " " + bot_response).lower()
        
        moment_patterns = [
            # First kiss
            (['cium', 'kiss', 'first kiss'], EpisodeType.FIRST_KISS, EmotionalTag.ROMANTIC, 0.9),
            # First intim
            (['intim', 'ml', 'first time', 'pertama kali intim'], EpisodeType.FIRST_INTIM, EmotionalTag.PASSIONATE, 1.0),
            # First climax
            (['climax', 'come', 'keluar', 'first climax'], EpisodeType.FIRST_CLIMAX, EmotionalTag.INTENSE, 1.0),
            # Confession
            (['sayang', 'cinta', 'love you', 'jatuh cinta'], EpisodeType.CONFESSION, EmotionalTag.ROMANTIC, 0.8),
            # Jadi pacar
            (['jadi pacar', 'jadipacar', 'pacar'], EpisodeType.BECAME_PACAR, EmotionalTag.HAPPY, 0.9),
            # Jadi FWB
            (['fwb', 'friend with benefit'], EpisodeType.BECAME_FWB, EmotionalTag.PLAYFUL, 0.8),
            # Romantic moment
            (['romantis', 'sweet', 'manis'], EpisodeType.ROMANTIC_MOMENT, EmotionalTag.ROMANTIC, 0.7),
            # Intimate moment
            (['hot', 'seksi', 'bergairah'], EpisodeType.INTIMATE_MOMENT, EmotionalTag.PASSIONATE, 0.7),
            # Funny moment
            (['lucu', 'haha', 'wkwk', 'ngakak'], EpisodeType.FUNNY_MOMENT, EmotionalTag.HAPPY, 0.6),
            # Sad moment
            (['sedih', 'nangis', 'kecewa'], EpisodeType.SAD_MOMENT, EmotionalTag.SAD, 0.7),
            # Aftercare
            (['aftercare', 'peluk', 'cuddle'], EpisodeType.AFTERCARE, EmotionalTag.PEACEFUL, 0.8)
        ]
        
        for keywords, ep_type, emotion, intensity in moment_patterns:
            if any(k in combined for k in keywords):
                description = user_message[:100] if len(user_message) < 100 else user_message[:97] + "..."
                
                return {
                    'type': ep_type,
                    'description': description,
                    'emotion': emotion,
                    'intensity': intensity
                }
        
        return None
    
    async def _check_consolidation(self):
        """Check if memory consolidation is needed"""
        now = time.time()
        if now - self.last_consolidation >= self.consolidation_interval:
            await self.run_consolidation()
            self.last_consolidation = now
    
    # =========================================================================
    # RECALL MEMORY
    # =========================================================================
    
    async def recall(self, 
                    query: str, 
                    memory_type: Optional[str] = None,
                    limit: int = 5) -> List[Dict]:
        """
        Mengingat memori berdasarkan query
        
        Args:
            query: Kata kunci pencarian
            memory_type: Tipe memori (optional)
            limit: Jumlah maksimal
            
        Returns:
            List of memories
        """
        results = []
        
        # 1. Recall dari compact summaries
        if self.current_session_id and (not memory_type or memory_type == MemoryType.COMPACT):
            summaries = await self.compact.search_summaries(
                user_id=self.user_id,
                session_id=self.current_session_id,
                keyword=query
            )
            for s in summaries[:limit]:
                s['source'] = 'compact'
                results.append(s)
        
        # 2. Recall dari episodic (momen spesial)
        if not memory_type or memory_type == MemoryType.EPISODIC:
            episodes = await self.episodic.get_episodes(
                user_id=self.user_id,
                role=self.current_role,
                limit=limit
            )
            for ep in episodes:
                if query.lower() in ep['description'].lower():
                    ep['source'] = 'episodic'
                    results.append(ep)
        
        # 3. Recall dari semantic (fakta)
        if not memory_type or memory_type == MemoryType.SEMANTIC:
            facts = await self.semantic.get_all_facts(self.user_id)
            for fact_key, value in facts.items():
                if query.lower() in fact_key.lower() or query.lower() in str(value).lower():
                    results.append({
                        'source': 'semantic',
                        'fact': fact_key,
                        'value': value,
                        'relevance': 0.7
                    })
        
        # 4. Recall dari working memory
        if not memory_type or memory_type == MemoryType.WORKING:
            recent = self.working.get_recent_context()
            for item in recent.get('recent_interactions', []):
                if query.lower() in item.get('user', '').lower():
                    results.append({
                        'source': 'working',
                        'content': item,
                        'relevance': 0.6
                    })
        
        # Sort by relevance
        results.sort(key=lambda x: x.get('relevance', 0.5), reverse=True)
        
        # Track access untuk forgetting
        for r in results[:limit]:
            if 'memory_id' in r:
                await self.forgetting.access_memory(r['memory_id'])
        
        return results[:limit]
    
    async def recall_random(self, memory_type: Optional[str] = None) -> Optional[Dict]:
        """Recall memori random untuk flashback"""
        # Coba dari episodic dulu
        if not memory_type or memory_type == MemoryType.EPISODIC:
            episode = await self.episodic.get_random_episode(self.user_id, self.current_role)
            if episode:
                return episode
        
        # Coba dari semantic
        if not memory_type or memory_type == MemoryType.SEMANTIC:
            facts = await self.semantic.get_all_facts(self.user_id)
            if facts:
                import random
                fact_key, value = random.choice(list(facts.items()))
                return {
                    'source': 'semantic',
                    'content': f"{fact_key}: {value}",
                    'importance': 0.6
                }
        
        return None
    
    async def get_context_for_prompt(self) -> Dict:
        """
        Dapatkan semua konteks untuk prompt AI
        
        Returns:
            Dict dengan semua memory yang relevan
        """
        context = {}
        
        # 1. Recent summaries (short-term memory)
        if self.current_session_id:
            summaries = await self.compact.get_recent_summaries(
                self.user_id,
                self.current_session_id,
                limit=3
            )
            if summaries:
                context['recent_summaries'] = summaries
        
        # 2. Recent episodes
        episodes = await self.episodic.get_episodes(
            self.user_id,
            self.current_role,
            limit=3
        )
        if episodes:
            context['recent_episodes'] = [
                {
                    'type': e['type'].value,
                    'description': e['description'],
                    'time_ago': self._format_time_ago(e['timestamp'])
                }
                for e in episodes
            ]
        
        # 3. Fakta user
        facts = await self.semantic.get_all_facts(self.user_id, min_confidence=0.6)
        if facts:
            context['user_facts'] = facts
        
        # 4. Preferensi untuk role ini
        if self.current_role:
            prefs = {}
            for pref_type in [PreferenceType.POSITION, PreferenceType.AREA, PreferenceType.ACTIVITY]:
                top = await self.semantic.get_top_preferences(
                    self.user_id,
                    self.current_role,
                    pref_type,
                    limit=3
                )
                if top:
                    prefs[pref_type] = top
            if prefs:
                context['preferences'] = prefs
        
        # 5. Working memory state
        context['current_state'] = self.working.get_current_state()
        
        return context
    
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
    
    # =========================================================================
    # FLASHBACK GENERATION
    # =========================================================================
    
    async def generate_flashback(self, trigger: Optional[str] = None) -> Optional[str]:
        """
        Generate flashback dari memory
        
        Args:
            trigger: Kata kunci pemicu
            
        Returns:
            Teks flashback atau None
        """
        # Coba dari episodic dulu
        flashback = await self.episodic.generate_flashback(
            user_id=self.user_id,
            role=self.current_role,
            instance_id=self.current_instance,
            trigger_word=trigger
        )
        
        if flashback:
            return flashback
        
        # Jika tidak ada, coba dari semantic
        if trigger:
            facts = await self.semantic.get_all_facts(self.user_id)
            for fact_key, value in facts.items():
                if trigger.lower() in fact_key.lower() or trigger.lower() in str(value).lower():
                    return f"Jadi inget... kamu pernah bilang {fact_key.replace('.', ' ')}: {value}."
        
        # Random recall dari forgetting
        random_memory = await self.forgetting.recall_random(min_strength=0.3)
        if random_memory:
            return f"Tiba-tiba inget... {random_memory.get('memory_id', 'sesuatu')}."
        
        return None
    
    # =========================================================================
    # FORGETTING & CONSOLIDATION
    # =========================================================================
    
    async def run_consolidation(self):
        """Jalankan memory consolidation periodik"""
        logger.info("Running memory consolidation...")
        
        # 1. Apply forgetting decay
        hours_since = 1
        await self.forgetting.decay_all(hours_since)
        
        # 2. Get forgotten memories
        forgotten = await self.forgetting.get_forgotten_memories()
        if forgotten:
            logger.info(f"🧹 {len(forgotten)} memories weakened")
        
        # 3. Get stats
        stats = await self.forgetting.get_stats()
        logger.info(f"📊 Memory stats: {stats}")
        
        logger.info("Memory consolidation completed")
    
    # =========================================================================
    # STATISTICS
    # =========================================================================
    
    async def get_memory_stats(self) -> Dict:
        """
        Dapatkan statistik semua sistem memory
        
        Returns:
            Dict dengan statistik lengkap
        """
        stats = {
            'working': {
                'items': len(self.working.items),
                'timeline': len(self.working.timeline)
            },
            'episodic': await self.episodic.get_stats(self.user_id),
            'semantic': await self.semantic.get_stats(self.user_id),
            'compact': await self.compact.get_stats(self.user_id),
            'forgetting': await self.forgetting.get_stats(),
            'current_session': {
                'session_id': self.current_session_id,
                'role': self.current_role,
                'instance': self.current_instance,
                'context': self.context_buffer
            }
        }
        
        return stats
    
    async def format_memory_summary(self) -> str:
        """
        Format ringkasan memory untuk ditampilkan ke user
        
        Returns:
            String ringkasan
        """
        lines = ["🧠 **Memory Summary**\n"]
        
        # Episodic (momen spesial)
        episodes = await self.episodic.get_episodes(self.user_id, self.current_role, limit=5)
        if episodes:
            lines.append("📖 **Momen Spesial Terakhir:**")
            for ep in episodes[:3]:
                time_str = datetime.fromtimestamp(ep['timestamp']).strftime("%d %b")
                lines.append(f"• {ep['description'][:50]}... ({time_str})")
            lines.append("")
        
        # Fakta user
        facts = await self.semantic.get_all_facts(self.user_id, min_confidence=0.7)
        if facts:
            lines.append("📌 **Fakta Tentang Kamu:**")
            fact_items = list(facts.items())[:5]
            for key, value in fact_items:
                simple_key = key.split('.')[-1].replace('_', ' ')
                lines.append(f"• {simple_key.title()}: {value}")
            lines.append("")
        
        # Forgetting stats
        stats = await self.forgetting.get_stats()
        if stats.get('weak_memories', 0) > 0:
            lines.append(f"💤 **Memori yang Mulai Terlupakan:** {stats['weak_memories']}")
        
        return "\n".join(lines)
    
    # =========================================================================
    # RESET & CLEANUP
    # =========================================================================
    
    async def clear_user_data(self):
        """Hapus semua data user"""
        await self.semantic.delete_user_data(self.user_id)
        await self.episodic.delete_user_episodes(self.user_id)
        await self.compact.clear_user(self.user_id)
        
        # Reset forgetting
        self.forgetting.memory_traces = {}
        self.forgetting.recent_memories = []
        
        logger.info(f"Cleared all memory data for user {self.user_id}")
    
    async def clear_session(self):
        """Hapus data untuk session saat ini"""
        if self.current_session_id:
            await self.compact.clear_session(self.user_id, self.current_session_id)
            self.working = WorkingMemory()
            logger.info(f"Cleared session memory for {self.current_session_id}")


__all__ = ['MemoryBridge', 'MemoryType', 'MemoryImportance']
