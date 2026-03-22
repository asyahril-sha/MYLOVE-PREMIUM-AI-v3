# dynamics/gesture_db.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - GESTURE DATABASE
=============================================================================
Database lengkap gesture untuk setiap situasi, posisi, dan emosi.

Karakteristik:
- Gesture dibagi berdasarkan kategori (posisi, aktivitas, emosi)
- Setiap gesture punya deskripsi yang natural
- Bisa dipanggil berdasarkan kombinasi situasi
- Support untuk berbagai tingkat arousal
=============================================================================
"""

import random
from typing import Dict, List, Optional


# =============================================================================
# GESTURE BERDASARKAN POSISI
# =============================================================================

POSITION_GESTURES = {
    'duduk_di_antara_kaki': {
        'description': 'Duduk di antara kaki user',
        'gestures': [
            "*membelai lembut paha user dengan ujung jari*",
            "*menatap ke atas ke arah user sambil tersenyum*",
            "*menyandarkan kepala di dada user, mendengar detak jantung*",
            "*tangan meraih tangan user, menggenggam erat*",
            "*mendekatkan wajah, napas terasa hangat di leher user*",
            "*memutar badan sedikit, membelai punggung user*",
            "*menggigit bibir bawah, menatap user dengan mata sayu*",
            "*telapak tangan menempel di perut user, merasakan kehangatan*",
            "*kepala menengadah, menatap user dari bawah*",
            "*jari-jari bergerak naik turun di paha user*"
        ]
    },
    
    'duduk_di_pangkuan': {
        'description': 'Duduk di pangkuan user',
        'gestures': [
            "*memeluk leher user, wajah menempel di dada*",
            "*menyandarkan kepala di bahu user, mata terpejam*",
            "*mencium pipi user cepat, lalu tersenyum malu*",
            "*memainkan rambut user dengan jari-jari*",
            "*berbisik di telinga user, suara pelan*",
            "*menggoyangkan tubuh kecil, bergeser lebih dekat*",
            "*menatap mata user dari jarak sangat dekat*",
            "*tangan melingkar di pinggang user, menarik lebih dekat*",
            "*menyender, bersandar penuh di dada user*",
            "*mencium leher user pelan-pelan*"
        ]
    },
    
    'di_belakang': {
        'description': 'Di belakang user',
        'gestures': [
            "*memeluk user dari belakang, tangan melingkar di pinggang*",
            "*mencium bahu user pelan, bibir menyentuh kulit*",
            "*berbisik di telinga user, suara hangat*",
            "*menyandarkan dagu di bahu user, menatap ke samping*",
            "*tangan memegang pinggang user, menarik lebih dekat*",
            "*mengusap punggung user dengan lembut*",
            "*menyandarkan seluruh tubuh ke punggung user*",
            "*tangan merambat dari pinggang ke perut user*",
            "*mencium belakang telinga user, bisik-bisik*",
            "*tangan menggenggam tangan user dari belakang*"
        ]
    },
    
    'bersebelahan': {
        'description': 'Bersebelahan dengan user',
        'gestures': [
            "*menyandarkan kepala ke bahu user, mata setengah terpejam*",
            "*menggenggam tangan user, jari-jari saling mengunci*",
            "*mencolek pinggang user, lalu tertawa kecil*",
            "*mengusap punggung tangan user dengan ibu jari*",
            "*bersandar lebih dekat, bahu bersentuhan*",
            "*menatap user sekilas, lalu tersenyum*",
            "*kaki bergeser, menyentuh kaki user*",
            "*tangan meraih tangan user, menggenggam erat*",
            "*menunduk, pipi memerah, bersandar ke user*",
            "*menepuk paha user pelan-pelan*"
        ]
    },
    
    'berhadapan': {
        'description': 'Berhadapan dengan user',
        'gestures': [
            "*menatap mata user dalam-dalam, mencari sesuatu*",
            "*mengusap pipi user dengan punggung tangan*",
            "*mencium kening user lembut*",
            "*mendekatkan wajah, jarak hanya beberapa senti*",
            "*menyentuh hidung user dengan ujung jari*",
            "*tersenyum kecil, mata berbinar*",
            "*menjilat bibir, menatap user*",
            "*tangan menyentuh dada user, merasakan detak jantung*",
            "*mendekat, dahi hampir bersentuhan*",
            "*berbisik, napas terasa hangat di wajah user*"
        ]
    },
    
    'di_depan': {
        'description': 'Di depan user',
        'gestures': [
            "*menatap mata user, tersenyum manis*",
            "*mengusap lengan user pelan*",
            "*mendekat, berdiri di depan user*",
            "*menjulurkan tangan, menggoda user*",
            "*menunduk malu, sesekali menatap user*",
            "*memainkan ujung baju, gugup*",
            "*melangkah mundur, memanggil user*",
            "*menyilangkan tangan di dada, tersenyum*"
        ]
    }
}


# =============================================================================
# GESTURE BERDASARKAN AKTIVITAS
# =============================================================================

ACTIVITY_GESTURES = {
    'memijat': {
        'description': 'Saat memijat',
        'gestures': [
            "*jari-jari menekan lembut punggung, bergerak memutar*",
            "*tangan berhenti sebentar, lalu lanjut dengan tekanan lebih dalam*",
            "*ibu jari menguleni area yang tegang, perlahan*",
            "*telapak tangan menekan lembut, merasakan kehangatan*",
            "*jari-jari bergerak turun ke pinggang, lalu naik lagi*",
            "*tangan gemetar sedikit, napas mulai tidak teratur*",
            "*menekan lebih dalam, lalu mengusap pelan*",
            "*jari-jari merambat ke area yang lebih sensitif*",
            "*berhenti di tengah jalan, napas tertahan*",
            "*tangan bergerak lebih lambat, sengaja memperlambat*"
        ]
    },
    
    'nonton_film': {
        'description': 'Saat nonton film bareng',
        'gestures': [
            "*mata tertuju pada layar, tapi sesekali melirik ke user*",
            "*tersenyum kecil saat adegan lucu, sesekali tertawa*",
            "*menutup mata saat adegan serem, bersandar ke user*",
            "*menelan ludah saat adegan panas, tangan mengepal*",
            "*tanpa sadar tubuh bergeser lebih dekat ke user*",
            "*tangan di pangkuan mulai gemetar kecil*",
            "*memegang erat lengan user saat adegan tegang*",
            "*menyandarkan kepala ke bahu user, mata sayu*",
            "*berbisik, mengomentari adegan yang sedang berlangsung*",
            "*tangan tanpa sadar meraih tangan user*"
        ]
    },
    
    'masak_bareng': {
        'description': 'Saat masak bareng',
        'gestures': [
            "*berdiri di samping user, sesekali tangan bersentuhan*",
            "*meminta user mengajari, sengaja mendekat*",
            "*tersenyum saat user membimbing tangan*",
            "*mencicipi masakan, lalu meminta user mencoba*",
            "*sengaja menyenggol user, tertawa kecil*",
            "*melihat user dengan mata berbinar*",
            "*mengambil bahan masakan, sengaja menyentuh user*",
            "*berdiri di belakang user, mengintip dari balik bahu*"
        ]
    },
    
    'main_game': {
        'description': 'Saat main game bareng',
        'gestures': [
            "*duduk dekat, sesekali senggol bahu*",
            "*teriak kaget, pegang lengan user*",
            "*tersenyum lebar saat menang, tos dengan user*",
            "*menggerutu saat kalah, memukul bantal*",
            "*minta diajarin, duduk lebih dekat*",
            "*sengaja menyentuh tangan user saat ambil controller*"
        ]
    },
    
    'berjalan_bareng': {
        'description': 'Saat jalan bareng',
        'gestures': [
            "*berjalan berdampingan, sesekali bahu bersentuhan*",
            "*tangan tanpa sadar bergandengan*",
            "*berhenti, melihat sesuatu, lalu menarik tangan user*",
            "*berbisik, menunjuk sesuatu di kejauhan*",
            "*berlari kecil, memegang tangan user*"
        ]
    }
}


# =============================================================================
# GESTURE BERDASARKAN EMOSI
# =============================================================================

EMOTION_GESTURES = {
    'malu': {
        'description': 'Saat merasa malu',
        'gestures': [
            "*menunduk, pipi memerah*",
            "*memainkan ujung baju, gugup*",
            "*menutup wajah dengan tangan*",
            "*menatap ke samping, menghindari tatapan*",
            "*tersenyum kecil, tidak berani menatap*",
            "*kaki menggeser-geser, gelisah*",
            "*memeluk bantal atau benda di dekatnya*"
        ]
    },
    
    'berani': {
        'description': 'Saat mulai berani',
        'gestures': [
            "*menatap langsung ke mata user*",
            "*mendekat, mengambil inisiatif*",
            "*tersenyum genit, mata berbinar*",
            "*menyentuh user lebih lama*",
            "*berbisik, suara lebih rendah*",
            "*meraih tangan user lebih dulu*",
            "*duduk lebih dekat, tidak malu-malu*"
        ]
    },
    
    'horny': {
        'description': 'Saat terangsang',
        'gestures': [
            "*napas memburu, dada naik turun*",
            "*tangan gemetar saat menyentuh*",
            "*menggigit bibir, menahan sesuatu*",
            "*tubuh bergeser lebih dekat, hampir menempel*",
            "*mata setengah terpejam, fokus pada user*",
            "*suara bergetar saat bicara*",
            "*telapak tangan berkeringat*",
            "*tubuh sedikit menegang, lalu rileks*",
            "*menjilat bibir, menatap user*",
            "*tangan mencengkeram erat sesuatu*"
        ]
    },
    
    'climax': {
        'description': 'Saat mencapai climax',
        'gestures': [
            "*tubuh gemetar hebat, tangan mencengkeram erat*",
            "*mata terpejam rapat, napas tersengal*",
            "*suara erangan tertahan, patah-patah*",
            "*badan lemas, bersandar ke user*",
            "*diam sejenak, mencoba mengatur napas*",
            "*kaki gemetar, tidak bisa berdiri*",
            "*tangan menggenggam erat baju user*",
            "*mata berkaca-kaca, napas belum stabil*"
        ]
    },
    
    'lemas': {
        'description': 'Saat lemas setelah climax',
        'gestures': [
            "*badan lemas, bersandar di user*",
            "*mata setengah terpejam, masih mengatur napas*",
            "*tangan masih gemetar kecil*",
            "*tersenyum lemas, tidak bisa bicara*",
            "*menyandarkan kepala di dada user*",
            "*diam, menikmati keheningan*",
            "*masih memeluk user, tidak mau lepas*"
        ]
    },
    
    'senang': {
        'description': 'Saat senang',
        'gestures': [
            "*tersenyum lebar, mata berbinar*",
            "*melompat kecil, bertepuk tangan*",
            "*memeluk user erat, tidak mau lepas*",
            "*tertawa kecil, bahu bergoyang*",
            "*menari-nari kecil, ceria*",
            "*memegang tangan user, menggoyangkan*"
        ]
    },
    
    'penasaran': {
        'description': 'Saat penasaran',
        'gestures': [
            "*mendekat, menatap user dengan seksama*",
            "*miringkan kepala, berpikir*",
            "*menanyakan sesuatu dengan suara penasaran*",
            "*mengamati user dari dekat*",
            "*tersenyum kecil, ingin tahu lebih banyak*"
        ]
    }
}


# =============================================================================
# GESTURE BERDASARKAN AROUSAL LEVEL
# =============================================================================

AROUSAL_GESTURES = {
    'very_low': {  # 0-20
        'gestures': [
            "*santai, bersandar*",
            "*tersenyum biasa*",
            "*melihat sekeliling*",
            "*menghela napas ringan*",
            "*duduk dengan nyaman*"
        ]
    },
    'low': {  # 20-40
        'gestures': [
            "*mulai deg-degan*",
            "*memainkan rambut, gelisah*",
            "*melirik user sekilas*",
            "*tersenyum kecil, malu-malu*",
            "*menunduk, tersenyum*"
        ]
    },
    'medium': {  # 40-60
        'gestures': [
            "*jantung berdebar, tangan mengepal*",
            "*pipi merona, menunduk*",
            "*menelan ludah, gugup*",
            "*mendekat perlahan*",
            "*tangan mulai gemetar sedikit*"
        ]
    },
    'high': {  # 60-80
        'gestures': [
            "*napas memburu, dada naik turun*",
            "*tangan gemetar saat menyentuh*",
            "*tubuh bergeser lebih dekat*",
            "*menggigit bibir, menahan sesuatu*",
            "*telapak tangan berkeringat*"
        ]
    },
    'very_high': {  # 80-100
        'gestures': [
            "*napas tersengal-sengal*",
            "*tubuh gemetar, tidak bisa diam*",
            "*mata setengah terpejam, fokus pada user*",
            "*suara bergetar, patah-patah*",
            "*tangan mencengkeram erat*"
        ]
    }
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_gesture(position: str = None, activity: str = None, 
                emotion: str = None, arousal: int = None) -> str:
    """
    Dapatkan gesture berdasarkan kombinasi situasi
    
    Args:
        position: Nama posisi (duduk_di_antara_kaki, di_belakang, dll)
        activity: Nama aktivitas (memijat, nonton_film, dll)
        emotion: Nama emosi (malu, horny, climax, dll)
        arousal: Level arousal (0-100) untuk variasi
    
    Returns:
        Gesture string
    """
    # Prioritas: arousal > position > activity > emotion > default
    
    # 1. Jika arousal diberikan, prioritaskan berdasarkan arousal
    if arousal is not None:
        if arousal >= 80:
            level = 'very_high'
        elif arousal >= 60:
            level = 'high'
        elif arousal >= 40:
            level = 'medium'
        elif arousal >= 20:
            level = 'low'
        else:
            level = 'very_low'
        
        gestures = AROUSAL_GESTURES.get(level, {}).get('gestures', [])
        if gestures:
            return random.choice(gestures)
    
    # 2. Berdasarkan posisi
    if position and position in POSITION_GESTURES:
        gestures = POSITION_GESTURES[position]['gestures']
        if gestures:
            return random.choice(gestures)
    
    # 3. Berdasarkan aktivitas
    if activity and activity in ACTIVITY_GESTURES:
        gestures = ACTIVITY_GESTURES[activity]['gestures']
        if gestures:
            return random.choice(gestures)
    
    # 4. Berdasarkan emosi
    if emotion and emotion in EMOTION_GESTURES:
        gestures = EMOTION_GESTURES[emotion]['gestures']
        if gestures:
            return random.choice(gestures)
    
    # 5. Default gesture
    default_gestures = [
        "*tersenyum kecil*",
        "*menatap user*",
        "*mendekat sedikit*",
        "*menghela napas*",
        "*memainkan ujung baju*",
        "*menunduk malu*",
        "*melihat sekilas*"
    ]
    return random.choice(default_gestures)


def get_gesture_by_combination(position: str = None, activity: str = None,
                               emotion: str = None, arousal: int = None) -> str:
    """
    Dapatkan gesture dengan kombinasi yang lebih spesifik
    
    Args:
        position: Posisi saat ini
        activity: Aktivitas saat ini
        emotion: Emosi saat ini
        arousal: Level arousal
    
    Returns:
        Gesture yang paling sesuai
    """
    # Coba kombinasi position + emotion
    if position and emotion:
        combined_key = f"{position}_{emotion}"
        # Bisa ditambahkan kombinasi spesifik jika diperlukan
        
    # Default
    return get_gesture(position=position, activity=activity, 
                      emotion=emotion, arousal=arousal)


def get_all_gesture_categories() -> Dict:
    """
    Dapatkan semua kategori gesture beserta jumlahnya
    """
    return {
        'positions': {k: len(v['gestures']) for k, v in POSITION_GESTURES.items()},
        'activities': {k: len(v['gestures']) for k, v in ACTIVITY_GESTURES.items()},
        'emotions': {k: len(v['gestures']) for k, v in EMOTION_GESTURES.items()},
        'arousal_levels': {k: len(v['gestures']) for k, v in AROUSAL_GESTURES.items()}
    }


def get_random_gesture() -> str:
    """
    Dapatkan gesture random dari semua database
    """
    all_gestures = []
    
    for pos in POSITION_GESTURES.values():
        all_gestures.extend(pos['gestures'])
    for act in ACTIVITY_GESTURES.values():
        all_gestures.extend(act['gestures'])
    for emo in EMOTION_GESTURES.values():
        all_gestures.extend(emo['gestures'])
    for aro in AROUSAL_GESTURES.values():
        all_gestures.extend(aro['gestures'])
    
    return random.choice(all_gestures) if all_gestures else "*tersenyum kecil*"


__all__ = [
    'POSITION_GESTURES',
    'ACTIVITY_GESTURES', 
    'EMOTION_GESTURES',
    'AROUSAL_GESTURES',
    'get_gesture',
    'get_gesture_by_combination',
    'get_all_gesture_categories',
    'get_random_gesture'
]
