# config/gesture_config.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - GESTURE CONFIGURATION
=============================================================================
Database lengkap gesture untuk setiap situasi, posisi, dan emosi.
Terintegrasi dengan dynamics/gesture_db.py
=============================================================================
"""

# =============================================================================
# GESTURE BERDASARKAN POSISI (LENGKAP)
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
            "*memutar badan sedikit, membelai punggung user dari posisi duduk*",
            "*menggigit bibir bawah, menatap user dengan mata sayu*",
            "*telapak tangan menempel di perut user, merasakan kehangatan*",
            "*kepala menengadah, menatap user dari bawah dengan senyum genit*",
            "*jari-jari bergerak naik turun di paha user pelan-pelan*"
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
            "*mencium leher user pelan-pelan, mata setengah terpejam*"
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
            "*mencium belakang telinga user, bisik-bisik mesra*",
            "*tangan menggenggam tangan user dari belakang, jari-jari mengunci*"
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
            "*menepuk paha user pelan-pelan sambil tersenyum*"
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
            "*mendekat, dahi hampir bersentuhan dengan user*",
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
            "*menyilangkan tangan di dada, tersenyum*",
            "*berjalan perlahan mendekati user*",
            "*menepuk bahu user, lalu tersenyum*"
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
            "*tangan bergerak lebih lambat, sengaja memperlambat ritme*"
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
            "*tangan tanpa sadar meraih tangan user dan menggenggam*"
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
            "*berdiri di belakang user, mengintip dari balik bahu*",
            "*meminta user mengecek rasa, sambil mendekat*",
            "*mencuci piring sambil sesekali melirik user*"
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
            "*sengaja menyentuh tangan user saat ambil controller*",
            "*berteriak heboh, memeluk user tanpa sadar*",
            "*menggeser posisi, bersandar ke user*",
            "*mengajak taruhan dengan hadiah yang menggoda*",
            "*menepuk paha user saat berhasil menang*"
        ]
    },
    
    'jalan_bareng': {
        'description': 'Saat jalan bareng',
        'gestures': [
            "*berjalan berdampingan, sesekali bahu bersentuhan*",
            "*tangan tanpa sadar bergandengan*",
            "*berhenti, melihat sesuatu, lalu menarik tangan user*",
            "*berbisik, menunjuk sesuatu di kejauhan*",
            "*berlari kecil, memegang tangan user*",
            "*bergandengan tangan, berjalan pelan*",
            "*mendekat saat jalan, sengaja menyentuh*",
            "*berhenti di tempat yang sepi, menatap user*",
            "*meminta user menunggu, lalu kembali dengan senyum*"
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
            "*memeluk bantal atau benda di dekatnya*",
            "*menggigit bibir bawah, menahan senyum*",
            "*berpura-pura sibuk dengan HP*",
            "*menyembunyikan wajah di balik tangan*"
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
            "*duduk lebih dekat, tidak malu-malu*",
            "*menggoda dengan tatapan*",
            "*menantang user dengan senyum*",
            "*menggerakkan tubuh mendekat perlahan*"
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
            "*tangan mencengkeram erat sesuatu*",
            "*kaki mengatup, lalu membuka pelan*",
            "*menghela napas panjang dan dalam*"
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
            "*mata berkaca-kaca, napas belum stabil*",
            "*kepala menunduk, badan lunglai*",
            "*diam, hanya napas yang terdengar*"
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
            "*masih memeluk user, tidak mau lepas*",
            "*mata sayu, masih terpengaruh*",
            "*bersandar penuh, tidak punya tenaga*",
            "*diam, hanya merasakan kehangatan*"
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
            "*memegang tangan user, menggoyangkan*",
            "*berputar-putar, bahagia*",
            "*berteriak kecil kegirangan*",
            "*mengedipkan mata, genit*",
            "*bersenandung kecil sambil bergerak*"
        ]
    },
    
    'penasaran': {
        'description': 'Saat penasaran',
        'gestures': [
            "*mendekat, menatap user dengan seksama*",
            "*miringkan kepala, berpikir*",
            "*menanyakan sesuatu dengan suara penasaran*",
            "*mengamati user dari dekat*",
            "*tersenyum kecil, ingin tahu lebih banyak*",
            "*menggerakkan alis, penasaran*",
            "*mendekatkan wajah, mengintip*",
            "*bertanya dengan nada antusias*",
            "*menggigit bibir, penasaran*",
            "*melihat user bolak-balik*"
        ]
    },
    
    'rindu': {
        'description': 'Saat rindu',
        'gestures': [
            "*menatap user lebih lama dari biasanya*",
            "*tersenyum kecil, mata berkaca-kaca*",
            "*mendekat, ingin lebih dekat*",
            "*memegang tangan user lebih erat*",
            "*bersandar, menikmati kebersamaan*",
            "*menghela napas, lega bisa bertemu*",
            "*mengusap lengan user pelan*",
            "*berbisik, 'aku kangen'*",
            "*memeluk erat, tidak mau lepas*",
            "*menyandarkan kepala, menikmati momen*"
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
            "*duduk dengan nyaman*",
            "*memainkan HP sambil tersenyum*",
            "*menguap kecil*",
            "*meregangkan badan*"
        ]
    },
    'low': {  # 20-40
        'gestures': [
            "*mulai deg-degan*",
            "*memainkan rambut, gelisah*",
            "*melirik user sekilas*",
            "*tersenyum kecil, malu-malu*",
            "*menunduk, tersenyum*",
            "*kaki bergerak-gerak gelisah*",
            "*memainkan ujung baju*",
            "*menatap user lebih lama*"
        ]
    },
    'medium': {  # 40-60
        'gestures': [
            "*jantung berdebar, tangan mengepal*",
            "*pipi merona, menunduk*",
            "*menelan ludah, gugup*",
            "*mendekat perlahan*",
            "*tangan mulai gemetar sedikit*",
            "*menarik napas dalam-dalam*",
            "*menggigit bibir bawah*",
            "*tubuh sedikit tegang*",
            "*melihat user dengan mata berbinar*"
        ]
    },
    'high': {  # 60-80
        'gestures': [
            "*napas memburu, dada naik turun*",
            "*tangan gemetar saat menyentuh*",
            "*tubuh bergeser lebih dekat*",
            "*menggigit bibir, menahan sesuatu*",
            "*telapak tangan berkeringat*",
            "*suara bergetar saat bicara*",
            "*tubuh sedikit menegang*",
            "*mata setengah terpejam*",
            "*menjilat bibir, menatap user*"
        ]
    },
    'very_high': {  # 80-100
        'gestures': [
            "*napas tersengal-sengal*",
            "*tubuh gemetar, tidak bisa diam*",
            "*mata setengah terpejam, fokus pada user*",
            "*suara bergetar, patah-patah*",
            "*tangan mencengkeram erat*",
            "*tubuh lemas, bersandar*",
            "*mata berkaca-kaca*",
            "*tidak bisa bicara, hanya erangan*",
            "*kaki gemetar, tidak stabil*",
            "*memeluk erat, menggenggam baju user*"
        ]
    }
}


# =============================================================================
# GESTURE KHUSUS UNTUK SITUASI TERTENTU
# =============================================================================

SPECIAL_SITUATION_GESTURES = {
    'pertama_kali_sentuh': {
        'description': 'Pertama kali disentuh user',
        'gestures': [
            "*tubuh menegang, napas tertahan*",
            "*mata membelalak, kaget*",
            "*pipi memerah, menunduk*",
            "*tangan gemetar, tidak tahu harus bereaksi*",
            "*berdiam diri, merasakan sentuhan*"
        ]
    },
    
    'ditinggal_sendirian': {
        'description': 'Saat ditinggal sendirian oleh user',
        'gestures': [
            "*menatap kepergian user, sedikit kecewa*",
            "*menghela napas panjang*",
            "*duduk termenung, memikirkan user*",
            "*memeluk bantal, membayangkan*",
            "*tersenyum kecil, mengingat momen tadi*"
        ]
    },
    
    'menunggu_user': {
        'description': 'Saat menunggu user datang',
        'gestures': [
            "*melihat jam berulang kali*",
            "*gelisah, mondar-mandir*",
            "*duduk, berdiri, duduk lagi*",
            "*memainkan HP, berharap ada kabar*",
            "*tersenyum sendiri membayangkan user*"
        ]
    },
    
    'kaget_ketahuan': {
        'description': 'Saat hampir ketahuan',
        'gestures': [
            "*membeku, tidak bergerak*",
            "*mata membelalak, jantung berdebar*",
            "*cepat menjauh, berpura-pura sibuk*",
            "*muka pucat, lalu memerah*",
            "*berbisik panik, 'cepat!'*"
        ]
    },
    
    'usai_intim': {
        'description': 'Setelah selesai intim',
        'gestures': [
            "*badan lemas, bersandar di dada user*",
            "*mata terpejam, napas masih tersengal*",
            "*tersenyum puas, tidak bisa bicara*",
            "*memeluk user erat, tidak mau lepas*",
            "*berbisik pelan, 'aku sayang kamu'*"
        ]
    }
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_position_gesture(position: str) -> list:
    """Dapatkan gesture untuk posisi tertentu"""
    return POSITION_GESTURES.get(position, {}).get('gestures', [])


def get_activity_gesture(activity: str) -> list:
    """Dapatkan gesture untuk aktivitas tertentu"""
    return ACTIVITY_GESTURES.get(activity, {}).get('gestures', [])


def get_emotion_gesture(emotion: str) -> list:
    """Dapatkan gesture untuk emosi tertentu"""
    return EMOTION_GESTURES.get(emotion, {}).get('gestures', [])


def get_arousal_gesture(arousal: int) -> list:
    """Dapatkan gesture berdasarkan level arousal"""
    if arousal >= 80:
        return AROUSAL_GESTURES['very_high']['gestures']
    elif arousal >= 60:
        return AROUSAL_GESTURES['high']['gestures']
    elif arousal >= 40:
        return AROUSAL_GESTURES['medium']['gestures']
    elif arousal >= 20:
        return AROUSAL_GESTURES['low']['gestures']
    else:
        return AROUSAL_GESTURES['very_low']['gestures']


def get_special_gesture(situation: str) -> list:
    """Dapatkan gesture untuk situasi khusus"""
    return SPECIAL_SITUATION_GESTURES.get(situation, {}).get('gestures', [])


def get_random_gesture(category: str = None) -> str:
    """
    Dapatkan gesture random dari kategori tertentu
    
    Args:
        category: posisi, aktivitas, emosi, arousal, special
    
    Returns:
        Gesture string
    """
    import random
    
    if category == 'posisi':
        all_gestures = []
        for pos in POSITION_GESTURES.values():
            all_gestures.extend(pos['gestures'])
        return random.choice(all_gestures) if all_gestures else "*tersenyum kecil*"
    
    elif category == 'aktivitas':
        all_gestures = []
        for act in ACTIVITY_GESTURES.values():
            all_gestures.extend(act['gestures'])
        return random.choice(all_gestures) if all_gestures else "*tersenyum kecil*"
    
    elif category == 'emosi':
        all_gestures = []
        for emo in EMOTION_GESTURES.values():
            all_gestures.extend(emo['gestures'])
        return random.choice(all_gestures) if all_gestures else "*tersenyum kecil*"
    
    elif category == 'special':
        all_gestures = []
        for sp in SPECIAL_SITUATION_GESTURES.values():
            all_gestures.extend(sp['gestures'])
        return random.choice(all_gestures) if all_gestures else "*tersenyum kecil*"
    
    else:
        # Semua kategori
        all_gestures = []
        for pos in POSITION_GESTURES.values():
            all_gestures.extend(pos['gestures'])
        for act in ACTIVITY_GESTURES.values():
            all_gestures.extend(act['gestures'])
        for emo in EMOTION_GESTURES.values():
            all_gestures.extend(emo['gestures'])
        for sp in SPECIAL_SITUATION_GESTURES.values():
            all_gestures.extend(sp['gestures'])
        return random.choice(all_gestures) if all_gestures else "*tersenyum kecil*"


__all__ = [
    'POSITION_GESTURES',
    'ACTIVITY_GESTURES',
    'EMOTION_GESTURES',
    'AROUSAL_GESTURES',
    'SPECIAL_SITUATION_GESTURES',
    'get_position_gesture',
    'get_activity_gesture',
    'get_emotion_gesture',
    'get_arousal_gesture',
    'get_special_gesture',
    'get_random_gesture'
]
