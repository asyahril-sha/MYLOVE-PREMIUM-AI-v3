# memory/emotional_memory.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - EMOTIONAL MEMORY
=============================================================================
Menyimpan ingatan emosional - apa yang dirasakan bot, bukan hanya fakta.

Karakteristik:
- Ingat perasaan dari interaksi sebelumnya
- Bisa mem-flashback momen yang berkesan
- Mempengaruhi mood saat ini
- Ada bias emosional dari pengalaman
=============================================================================
"""

import time
import random
from typing import Dict, List, Optional, Any
from datetime import datetime


class EmotionalMemory:
    """
    Menyimpan ingatan emosional bot.
    Bot ingat bagaimana perasaannya di masa lalu, bukan hanya apa yang terjadi.
    """
    
    def __init__(self):
        # Memori emosional
        self.memories = []  # [{timestamp, emotion, intensity, context, user_message, bot_response, arousal}]
        
        # Bias emosional (pengaruh dari memori)
        self.emotional_bias = {
            'positive': 0.5,    # 0-1, seberapa positif bias
            'negative': 0.5,    # 0-1, seberapa negatif bias
            'romantic': 0.5,    # 0-1, seberapa romantis bias
            'intimate': 0.5     # 0-1, seberapa intim bias
        }
        
        # Memori penting (high intensity)
        self.important_memories = []
        
        # Last memory recall untuk konsistensi
        self.last_recall = None
        
        # Threshold untuk memori penting
        self.importance_threshold = 0.7
    
    # =========================================================================
    # ADD MEMORY
    # =========================================================================
    
    def add_memory(self, emotion: str, intensity: float, context: Dict,
                   user_message: str, bot_response: str, arousal: int = 0):
        """
        Tambah memori emosional
        
        Args:
            emotion: Emosi yang dirasakan (senang, sedih, horny, romantis, dll)
            intensity: Intensitas emosi (0-1)
            context: Konteks saat itu (situasi, lokasi, dll)
            user_message: Pesan user
            bot_response: Respon bot
            arousal: Level arousal saat itu
        """
        memory = {
            'timestamp': time.time(),
            'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'emotion': emotion,
            'intensity': intensity,
            'context': context.copy(),
            'user_message': user_message[:150] if user_message else "",
            'bot_response': bot_response[:150] if bot_response else "",
            'arousal': arousal,
            'recall_count': 0,
            'last_recall': None
        }
        
        self.memories.append(memory)
        
        # Update bias emosional
        self._update_emotional_bias(emotion, intensity)
        
        # Simpan ke important memories jika intensitas tinggi
        if intensity >= self.importance_threshold:
            self.important_memories.append(memory)
        
        # Simpan hanya 500 memori terakhir
        if len(self.memories) > 500:
            self.memories = self.memories[-500:]
        
        # Simpan hanya 100 important memories
        if len(self.important_memories) > 100:
            self.important_memories = self.important_memories[-100:]
    
    def _update_emotional_bias(self, emotion: str, intensity: float):
        """
        Update bias emosional berdasarkan memori baru
        """
        # Positive bias
        if emotion in ['senang', 'bahagia', 'puas', 'tertarik', 'sayang']:
            self.emotional_bias['positive'] = min(1.0, self.emotional_bias['positive'] + (intensity * 0.02))
        
        # Negative bias
        elif emotion in ['sedih', 'marah', 'kecewa', 'kesal']:
            self.emotional_bias['negative'] = min(1.0, self.emotional_bias['negative'] + (intensity * 0.02))
        
        # Romantic bias
        if emotion in ['romantis', 'sayang', 'cinta', 'kangen']:
            self.emotional_bias['romantic'] = min(1.0, self.emotional_bias['romantic'] + (intensity * 0.03))
        
        # Intimate bias
        if emotion in ['horny', 'gairah', 'nafsu', 'intim']:
            self.emotional_bias['intimate'] = min(1.0, self.emotional_bias['intimate'] + (intensity * 0.04))
        
        # Decay over time (akan dijalankan periodic)
        self._decay_bias()
    
    def _decay_bias(self):
        """Decay bias emosional seiring waktu"""
        # Setiap kali add memory, decay sedikit
        for key in self.emotional_bias:
            self.emotional_bias[key] = max(0.3, self.emotional_bias[key] * 0.999)
    
    # =========================================================================
    # RECALL MEMORY
    # =========================================================================
    
    def get_recent_memories(self, limit: int = 5) -> List[Dict]:
        """
        Dapatkan memori terbaru
        
        Args:
            limit: Jumlah memori yang diambil
        
        Returns:
            List memori
        """
        return self.memories[-limit:] if self.memories else []
    
    def get_memories_by_emotion(self, emotion: str, limit: int = 3) -> List[Dict]:
        """
        Dapatkan memori berdasarkan emosi
        
        Args:
            emotion: Emosi yang dicari
            limit: Jumlah memori
        
        Returns:
            List memori
        """
        filtered = [m for m in self.memories if m['emotion'] == emotion]
        return filtered[-limit:] if filtered else []
    
    def get_important_memories(self, limit: int = 5) -> List[Dict]:
        """
        Dapatkan memori penting (intensitas tinggi)
        
        Args:
            limit: Jumlah memori
        """
        return self.important_memories[-limit:] if self.important_memories else []
    
    def get_flashback(self, trigger: str = None, emotion: str = None) -> Optional[str]:
        """
        Dapatkan flashback berdasarkan trigger atau random
        
        Args:
            trigger: Kata kunci pemicu (opsional)
            emotion: Emosi spesifik (opsional)
        
        Returns:
            Teks flashback atau None
        """
        if not self.memories:
            return None
        
        # Pilih memori berdasarkan trigger
        if trigger:
            relevant = []
            trigger_lower = trigger.lower()
            for mem in self.memories:
                if (trigger_lower in mem['user_message'].lower() or 
                    trigger_lower in mem['context'].get('topic', '').lower() or
                    trigger_lower in mem['context'].get('location', '').lower()):
                    relevant.append(mem)
            
            if relevant:
                memory = random.choice(relevant)
            else:
                memory = random.choice(self.memories)
        
        # Pilih berdasarkan emosi
        elif emotion:
            filtered = [m for m in self.memories if m['emotion'] == emotion]
            if filtered:
                memory = random.choice(filtered)
            else:
                memory = random.choice(self.memories)
        
        # Random dengan preferensi penting
        else:
            if self.important_memories and random.random() < 0.3:
                memory = random.choice(self.important_memories)
            else:
                memory = random.choice(self.memories[-20:])
        
        # Update recall count
        memory['recall_count'] += 1
        memory['last_recall'] = time.time()
        self.last_recall = memory['timestamp']
        
        # Generate flashback text
        return self._format_flashback(memory)
    
    def _format_flashback(self, memory: Dict) -> str:
        """
        Format memori menjadi teks flashback yang natural
        """
        time_ago = self._format_time_ago(memory['timestamp'])
        emotion = memory['emotion']
        intensity = memory['intensity']
        context = memory['context']
        user_message = memory['user_message'][:50]
        
        # Pilih template berdasarkan emosi
        templates = {
            'horny': [
                f"Jadi inget... {time_ago}, aku {emotion} banget pas {context.get('situasi', 'kita ngobrol')}. Kamu bilang: '{user_message}'...",
                f"{time_ago}, aku masih inget rasanya {emotion}. Kamu waktu itu {context.get('situasi', '')}...",
                f"Kamu inget gak {time_ago}? Aku sampai {emotion}. {user_message}..."
            ],
            'romantis': [
                f"Masih inget {time_ago}? Waktu itu {context.get('situasi', 'kita')}, aku ngerasa {emotion} banget.",
                f"{time_ago}, aku jadi inget momen {emotion} kita. {user_message}...",
                f"Kangen waktu {time_ago}, kamu bilang '{user_message}'. Aku jadi {emotion}."
            ],
            'senang': [
                f"{time_ago} tuh seru banget. Aku {emotion} banget pas {context.get('situasi', 'kita ngobrol')}.",
                f"Mas, inget gak {time_ago}? Aku sampe {emotion} waktu itu.",
                f"Wah, jadi inget {time_ago}. Kamu bikin aku {emotion} banget."
            ],
            'malu': [
                f"Aduh, jadi inget {time_ago}. Aku malu banget waktu {context.get('situasi', 'itu')}.",
                f"{time_ago}, aku sampe merah padam. Kamu pasti inget kan?",
                f"Jangan inget-inget {time_ago} dong. Aku malu..."
            ]
        }
        
        # Pilih template berdasarkan emosi
        template_list = templates.get(emotion, templates['senang'])
        
        # Tambah intensitas
        if intensity > 0.8:
            intensifier = " banget"
        elif intensity > 0.5:
            intensifier = ""
        else:
            intensifier = " dikit"
        
        flashback = random.choice(template_list)
        flashback = flashback.replace("{emotion}", f"{emotion}{intensifier}")
        
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
        elif diff < 2592000:
            return f"{int(diff/604800)} minggu lalu"
        else:
            return f"{int(diff/2592000)} bulan lalu"
    
    # =========================================================================
    # GET EMOTIONAL CONTEXT
    # =========================================================================
    
    def get_emotional_context(self, limit: int = 3) -> str:
        """
        Dapatkan konteks emosional untuk prompt
        
        Args:
            limit: Jumlah memori yang ditampilkan
        
        Returns:
            String konteks emosional
        """
        if not self.memories:
            return ""
        
        recent = self.memories[-limit:]
        
        lines = ["📖 **KENANGAN EMOSIONAL TERAKHIR:**"]
        
        for mem in recent:
            time_str = datetime.fromtimestamp(mem['timestamp']).strftime("%H:%M")
            intensity_bar = "🔴" * int(mem['intensity'] * 10) + "⚪" * (10 - int(mem['intensity'] * 10))
            lines.append(f"- [{time_str}] {mem['emotion'].upper()} {intensity_bar}: {mem['context'].get('situasi', '')[:50]}")
        
        # Tambah bias emosional
        if self.emotional_bias['positive'] > 0.7:
            lines.append("\n💡 Kamu lagi dalam mood positif dari kenangan sebelumnya.")
        elif self.emotional_bias['negative'] > 0.7:
            lines.append("\n💡 Kamu masih terpengaruh kenangan negatif sebelumnya.")
        
        if self.emotional_bias['romantic'] > 0.6:
            lines.append("💕 Ada sisa rasa romantis dari interaksi sebelumnya.")
        
        if self.emotional_bias['intimate'] > 0.6:
            lines.append("🔥 Masih ada getaran intim dari kenangan sebelumnya.")
        
        return "\n".join(lines)
    
    def get_mood_influence(self) -> float:
        """
        Dapatkan pengaruh memori emosional ke mood saat ini
        
        Returns:
            Float antara -1 (negatif) sampai 1 (positif)
        """
        return self.emotional_bias['positive'] - self.emotional_bias['negative']
    
    def get_romantic_influence(self) -> float:
        """
        Dapatkan pengaruh memori romantis
        
        Returns:
            Float 0-1
        """
        return self.emotional_bias['romantic']
    
    def get_intimate_influence(self) -> float:
        """
        Dapatkan pengaruh memori intim
        
        Returns:
            Float 0-1
        """
        return self.emotional_bias['intimate']
    
    # =========================================================================
    # STATISTICS & UTILITY
    # =========================================================================
    
    def get_stats(self) -> Dict:
        """
        Dapatkan statistik emotional memory
        """
        if not self.memories:
            return {'total_memories': 0}
        
        # Hitung distribusi emosi
        emotion_count = {}
        for mem in self.memories:
            emotion = mem['emotion']
            emotion_count[emotion] = emotion_count.get(emotion, 0) + 1
        
        # Rata-rata intensitas
        avg_intensity = sum(m['intensity'] for m in self.memories) / len(self.memories)
        
        return {
            'total_memories': len(self.memories),
            'important_memories': len(self.important_memories),
            'emotion_distribution': emotion_count,
            'avg_intensity': round(avg_intensity, 2),
            'emotional_bias': {k: round(v, 2) for k, v in self.emotional_bias.items()},
            'last_recall': datetime.fromtimestamp(self.last_recall).strftime("%Y-%m-%d %H:%M") if self.last_recall else None
        }
    
    def clear_memories(self):
        """Hapus semua memori (untuk reset)"""
        self.memories = []
        self.important_memories = []
        self.emotional_bias = {
            'positive': 0.5,
            'negative': 0.5,
            'romantic': 0.5,
            'intimate': 0.5
        }
        self.last_recall = None
    
    def get_state(self) -> Dict:
        """
        Dapatkan state untuk disimpan ke database
        """
        return {
            'memories': self.memories[-100:],  # Simpan 100 terakhir
            'important_memories': self.important_memories[-50:],
            'emotional_bias': self.emotional_bias,
            'last_recall': self.last_recall
        }
    
    def load_state(self, state: Dict):
        """
        Load state dari database
        """
        self.memories = state.get('memories', [])
        self.important_memories = state.get('important_memories', [])
        self.emotional_bias = state.get('emotional_bias', {
            'positive': 0.5, 'negative': 0.5, 'romantic': 0.5, 'intimate': 0.5
        })
        self.last_recall = state.get('last_recall')
    
    def format_for_prompt(self) -> str:
        """
        Format untuk prompt AI
        """
        if not self.memories:
            return ""
        
        lines = [
            "📖 **KENANGAN EMOSIONAL YANG MEMPENGARUHI SAAT INI:**",
            f"- Bias positif: {self.emotional_bias['positive']:.0%}",
            f"- Bias romantis: {self.emotional_bias['romantic']:.0%}",
            f"- Bias intim: {self.emotional_bias['intimate']:.0%}"
        ]
        
        # Tambah 2 memori terpenting
        if self.important_memories:
            lines.append("\n💭 **Kenangan yang paling berkesan:**")
            for mem in self.important_memories[-2:]:
                time_str = datetime.fromtimestamp(mem['timestamp']).strftime("%d %b")
                lines.append(f"- {time_str}: {mem['emotion']} ({mem['context'].get('situasi', '')[:40]})")
        
        return "\n".join(lines)


__all__ = ['EmotionalMemory']
