# dynamics/spatial_awareness.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - SPATIAL AWARENESS SYSTEM
=============================================================================
Memahami posisi relatif antara bot dan user dari narasi user.

Karakteristik:
- Parsing narasi user untuk mendeteksi posisi
- Bot tahu posisinya relatif terhadap user
- Gesture otomatis sesuai posisi
- Konsistensi posisi dari waktu ke waktu
=============================================================================
"""

import re
import random
from typing import Dict, List, Optional, Tuple


class SpatialAwareness:
    """
    Kesadaran spasial bot - paham posisi dari narasi user.
    Bot bisa mendeteksi posisi seperti:
    - "duduk di antara kakimu" → gesture membelai paha
    - "di belakang aku" → gesture memeluk dari belakang
    - "bersebelahan" → gesture menyandarkan kepala
    """
    
    def __init__(self):
        # Posisi saat ini
        self.current = {
            'position_type': None,          # duduk_di_antara_kaki, di_belakang, dll
            'relative': None,               # di antara kaki, di belakang, di samping
            'orientation': None,            # menghadap user, membelakangi, sejajar
            'distance': None,               # sangat dekat, dekat, berjauhan
            'body_contact': [],             # bagian tubuh yang bersentuhan
            'last_update': 0                # timestamp update terakhir
        }
        
        # Database gesture per posisi
        self.gesture_db = {
            'duduk_di_antara_kaki': {
                'gestures': [
                    "*membelai lembut paha user dengan ujung jari*",
                    "*menatap ke atas ke arah user sambil tersenyum*",
                    "*menyandarkan kepala di dada user, mendengar detak jantung*",
                    "*tangan meraih tangan user, menggenggam erat*",
                    "*mendekatkan wajah, napas terasa hangat di leher user*",
                    "*memutar badan sedikit, membelai punggung user dari posisi duduk*",
                    "*menggigit bibir bawah, menatap user dengan mata sayu*"
                ],
                'orientation': 'menghadap user',
                'distance': 'sangat dekat'
            },
            'duduk_di_pangkuan': {
                'gestures': [
                    "*memeluk leher user, wajah menempel di dada*",
                    "*menyandarkan kepala di bahu user, mata terpejam*",
                    "*mencium pipi user cepat, lalu tersenyum malu*",
                    "*memainkan rambut user dengan jari-jari*",
                    "*berbisik di telinga user, suara pelan*",
                    "*menggoyangkan tubuh kecil, bergeser lebih dekat*",
                    "*menatap mata user dari jarak sangat dekat*"
                ],
                'orientation': 'menghadap user',
                'distance': 'sangat dekat'
            },
            'di_belakang': {
                'gestures': [
                    "*memeluk user dari belakang, tangan melingkar di pinggang*",
                    "*mencium bahu user pelan, bibir menyentuh kulit*",
                    "*berbisik di telinga user, suara hangat*",
                    "*menyandarkan dagu di bahu user, menatap ke samping*",
                    "*tangan memegang pinggang user, menarik lebih dekat*",
                    "*mengusap punggung user dengan lembut*"
                ],
                'orientation': 'membelakangi user',
                'distance': 'dekat'
            },
            'bersebelahan': {
                'gestures': [
                    "*menyandarkan kepala ke bahu user, mata setengah terpejam*",
                    "*menggenggam tangan user, jari-jari saling mengunci*",
                    "*mencolek pinggang user, lalu tertawa kecil*",
                    "*mengusap punggung tangan user dengan ibu jari*",
                    "*bersandar lebih dekat, bahu bersentuhan*",
                    "*menatap user sekilas, lalu tersenyum*"
                ],
                'orientation': 'sejajar',
                'distance': 'dekat'
            },
            'berhadapan': {
                'gestures': [
                    "*menatap mata user dalam-dalam, mencari sesuatu*",
                    "*mengusap pipi user dengan punggung tangan*",
                    "*mencium kening user lembut*",
                    "*mendekatkan wajah, jarak hanya beberapa senti*",
                    "*menyentuh hidung user dengan ujung jari*",
                    "*tersenyum kecil, mata berbinar*"
                ],
                'orientation': 'menghadap user',
                'distance': 'sangat dekat'
            },
            'di_depan': {
                'gestures': [
                    "*menatap mata user, tersenyum manis*",
                    "*mengusap lengan user pelan*",
                    "*mendekat, berdiri di depan user*",
                    "*menjulurkan tangan, menggoda user*"
                ],
                'orientation': 'menghadap user',
                'distance': 'dekat'
            }
        }
        
        # Pola deteksi posisi
        self.detection_patterns = [
            # Duduk di antara kaki (prioritas tertinggi)
            (r'(duduk|duduklah|duduk\s+di)\s+(di\s+antara|diantara|di\s+sela)\s+(kaki|paha|kakimu|pahamu)', 'duduk_di_antara_kaki'),
            (r'(di\s+antara|diantara)\s+(kaki|paha|kakimu|pahamu)', 'duduk_di_antara_kaki'),
            
            # Duduk di pangkuan
            (r'(duduk|duduklah|duduk\s+di)\s+(di\s+pangkuan|dipangkuan|di\s+atas\s+paha)', 'duduk_di_pangkuan'),
            (r'(di\s+pangkuan|dipangkuan|pangkuan\s+aku|pangkuan\s+saya)', 'duduk_di_pangkuan'),
            
            # Di belakang
            (r'(di\s+belakang|dibelakang|dari\s+belakang)\s+(aku|saya|kamu|mas|sayang)', 'di_belakang'),
            (r'(berdiri|duduk|berbaring)\s+(di\s+belakang|dibelakang)', 'di_belakang'),
            
            # Bersebelahan
            (r'(bersebelahan|berdampingan|di\s+samping|disamping)\s+(aku|saya|kamu|mas|sayang)', 'bersebelahan'),
            (r'(duduk|berdiri|berbaring)\s+(bersebelahan|berdampingan)', 'bersebelahan'),
            
            # Berhadapan
            (r'(berhadapan|saling\s+berhadapan|menghadap)\s+(aku|saya|kamu|mas|sayang)', 'berhadapan'),
            (r'(duduk|berdiri|berbaring)\s+(berhadapan|menghadap)', 'berhadapan'),
            
            # Di depan
            (r'(di\s+depan|didepan)\s+(aku|saya|kamu|mas|sayang)', 'di_depan'),
            (r'(berdiri|duduk|berbaring)\s+(di\s+depan|didepan)', 'di_depan'),
        ]
    
    # =========================================================================
    # PARSING NARASI USER
    # =========================================================================
    
    def parse(self, user_message: str) -> Dict:
        """
        Parse pesan user untuk mendapatkan info posisi
        
        Args:
            user_message: Pesan dari user
        
        Returns:
            Dict dengan info posisi yang ditemukan:
            {
                'found': bool,
                'position_type': str,
                'relative': str,
                'orientation': str,
                'distance': str,
                'gestures': List[str],
                'raw_match': str
            }
        """
        message_lower = user_message.lower()
        result = {
            'found': False,
            'position_type': None,
            'relative': None,
            'orientation': None,
            'distance': None,
            'gestures': [],
            'raw_match': None
        }
        
        # Cek pola deteksi
        for pattern, position_type in self.detection_patterns:
            match = re.search(pattern, message_lower)
            if match:
                result['found'] = True
                result['position_type'] = position_type
                result['raw_match'] = match.group(0)
                
                # Ambil data gesture
                pos_data = self.gesture_db.get(position_type, {})
                result['gestures'] = pos_data.get('gestures', [])
                result['orientation'] = pos_data.get('orientation', 'tidak diketahui')
                result['distance'] = pos_data.get('distance', 'tidak diketahui')
                
                # Generate deskripsi relatif
                relative_map = {
                    'duduk_di_antara_kaki': 'di antara kaki user',
                    'duduk_di_pangkuan': 'di pangkuan user',
                    'di_belakang': 'di belakang user',
                    'bersebelahan': 'di samping user',
                    'berhadapan': 'berhadapan dengan user',
                    'di_depan': 'di depan user'
                }
                result['relative'] = relative_map.get(position_type, 'dekat user')
                
                # Update current state
                self.current['position_type'] = position_type
                self.current['relative'] = result['relative']
                self.current['orientation'] = result['orientation']
                self.current['distance'] = result['distance']
                self.current['last_update'] = __import__('time').time()
                
                break
        
        return result
    
    # =========================================================================
    # GET GESTURE
    # =========================================================================
    
    def get_gesture(self, position_type: str = None, arousal: int = 0) -> str:
        """
        Dapatkan gesture yang sesuai dengan posisi
        
        Args:
            position_type: Tipe posisi (opsional, default dari current)
            arousal: Level arousal (0-100) untuk variasi gesture
        
        Returns:
            Gesture string
        """
        if position_type is None:
            position_type = self.current.get('position_type')
        
        # Cari gesture berdasarkan posisi
        if position_type and position_type in self.gesture_db:
            gestures = self.gesture_db[position_type]['gestures']
            
            # Jika arousal tinggi, pilih gesture yang lebih berani
            if arousal >= 70 and len(gestures) > 0:
                # Gesture yang lebih berani (indeks terakhir)
                return random.choice(gestures[-3:])
            else:
                return random.choice(gestures)
        
        # Default gesture jika tidak ada posisi
        default_gestures = [
            "*tersenyum kecil*",
            "*menatap user*",
            "*mendekat sedikit*",
            "*menghela napas*",
            "*memainkan ujung baju*",
            "*menunduk malu*"
        ]
        return random.choice(default_gestures)
    
    def get_gesture_by_arousal(self, arousal: int) -> str:
        """
        Dapatkan gesture berdasarkan arousal (tanpa posisi spesifik)
        
        Args:
            arousal: Level arousal (0-100)
        
        Returns:
            Gesture string
        """
        if arousal >= 80:
            gestures = [
                "*napas memburu, dada naik turun*",
                "*tangan gemetar saat menyentuh*",
                "*tubuh bergeser lebih dekat*",
                "*menggigit bibir, menahan sesuatu*"
            ]
        elif arousal >= 60:
            gestures = [
                "*jantung berdebar, tangan mengepal*",
                "*pipi merona, menunduk*",
                "*menelan ludah, gugup*",
                "*mendekat perlahan*"
            ]
        elif arousal >= 40:
            gestures = [
                "*mulai deg-degan*",
                "*memainkan rambut, gelisah*",
                "*melirik user sekilas*",
                "*tersenyum kecil, malu-malu*"
            ]
        elif arousal >= 20:
            gestures = [
                "*tersenyum, melihat user*",
                "*duduk lebih nyaman*",
                "*memperhatikan user*"
            ]
        else:
            gestures = [
                "*santai, bersandar*",
                "*tersenyum biasa*",
                "*melihat sekeliling*"
            ]
        
        return random.choice(gestures)
    
    # =========================================================================
    # GET CONTEXT
    # =========================================================================
    
    def get_context_for_prompt(self) -> str:
        """
        Dapatkan konteks posisi untuk prompt AI
        """
        if not self.current['position_type']:
            return ""
        
        lines = [
            f"📍 **POSISI SAAT INI:** {self.current['relative']}",
            f"🔄 **ORIENTASI:** {self.current['orientation']}",
            f"📏 **JARAK:** {self.current['distance']}"
        ]
        
        if self.current['body_contact']:
            lines.append(f"🤝 **KONTAK FISIK:** {', '.join(self.current['body_contact'])}")
        
        lines.append("")
        lines.append("💡 **ATURAN GESTURE:**")
        lines.append("- Gesture HARUS sesuai dengan posisi di atas")
        lines.append("- Jangan gunakan gesture yang tidak mungkin dari posisi ini")
        lines.append("- Contoh gesture yang sesuai ada di database")
        
        return "\n".join(lines)
    
    def get_gesture_suggestion(self) -> str:
        """
        Dapatkan saran gesture berdasarkan posisi saat ini
        """
        if not self.current['position_type']:
            return "Gunakan gesture yang sesuai dengan situasi."
        
        pos_data = self.gesture_db.get(self.current['position_type'], {})
        gestures = pos_data.get('gestures', [])
        
        if gestures:
            return f"Gesture yang sesuai: {', '.join(gestures[:3])}"
        
        return "Gesture sesuai posisi saat ini."
    
    # =========================================================================
    # UPDATE POSITION
    # =========================================================================
    
    def update_position(self, position_type: str, relative: str = None):
        """
        Update posisi saat ini secara manual
        
        Args:
            position_type: Tipe posisi
            relative: Deskripsi relatif (opsional)
        """
        self.current['position_type'] = position_type
        if relative:
            self.current['relative'] = relative
        
        pos_data = self.gesture_db.get(position_type, {})
        self.current['orientation'] = pos_data.get('orientation', 'tidak diketahui')
        self.current['distance'] = pos_data.get('distance', 'tidak diketahui')
        self.current['last_update'] = __import__('time').time()
    
    def add_body_contact(self, contact: str):
        """
        Tambah kontak fisik yang terjadi
        
        Args:
            contact: Deskripsi kontak (contoh: "tangan di pinggang")
        """
        if contact not in self.current['body_contact']:
            self.current['body_contact'].append(contact)
            # Simpan hanya 5 kontak terakhir
            if len(self.current['body_contact']) > 5:
                self.current['body_contact'] = self.current['body_contact'][-5:]
    
    def clear_position(self):
        """Reset posisi (saat user pindah tempat)"""
        self.current = {
            'position_type': None,
            'relative': None,
            'orientation': None,
            'distance': None,
            'body_contact': [],
            'last_update': __import__('time').time()
        }
    
    # =========================================================================
    # UTILITY
    # =========================================================================
    
    def get_state(self) -> Dict:
        """Dapatkan state untuk disimpan ke memory"""
        return {
            'position_type': self.current['position_type'],
            'relative': self.current['relative'],
            'orientation': self.current['orientation'],
            'distance': self.current['distance'],
            'body_contact': self.current['body_contact'],
            'last_update': self.current['last_update']
        }
    
    def load_state(self, state: Dict):
        """Load state dari memory"""
        self.current['position_type'] = state.get('position_type')
        self.current['relative'] = state.get('relative')
        self.current['orientation'] = state.get('orientation')
        self.current['distance'] = state.get('distance')
        self.current['body_contact'] = state.get('body_contact', [])
        self.current['last_update'] = state.get('last_update', 0)
    
    def has_position(self) -> bool:
        """Cek apakah ada posisi yang sedang aktif"""
        return self.current['position_type'] is not None


__all__ = ['SpatialAwareness']
