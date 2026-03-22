# tests/test_role_behavior.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - ROLE BEHAVIOR UNIT TEST
=============================================================================
Test untuk memastikan semua role behavior bekerja dengan benar
"""

import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
from unittest.mock import Mock, patch, AsyncMock
import time
import random

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


class TestRoleBehaviorBase(unittest.TestCase):
    """Test untuk RoleBehavior base class"""
    
    def setUp(self):
        """Setup sebelum setiap test"""
        # Buat class turunan sederhana untuk test
        class TestRole(RoleBehavior):
            def get_pakaian(self, situasi):
                return "test pakaian"
            
            def get_aktivitas_menggoda(self, situasi):
                return {'nama': 'test', 'alasan': 'test', 'goda_level': 50}
            
            def get_respon_saat_disentuh(self, bagian, situasi):
                return {'gesture': 'test', 'dialog': 'test', 'arousal_change': 10}
            
            def get_inner_thought(self, situasi):
                return "(test thought)"
        
        self.role = TestRole("test_role", "TestUser", "TestBot")
    
    def test_initial_state(self):
        """Test state awal"""
        self.assertEqual(self.role.role_name, "test_role")
        self.assertEqual(self.role.user_name, "TestUser")
        self.assertEqual(self.role.bot_name, "TestBot")
        self.assertEqual(self.role.arousal, 0)
        self.assertEqual(self.role.mode_goda, 0)
    
    def test_update_arousal(self):
        """Test update arousal"""
        self.role.update_arousal(20, "test reason")
        self.assertEqual(self.role.arousal, 20)
        
        self.role.update_arousal(-5, "test reason")
        self.assertEqual(self.role.arousal, 15)
        
        # Test batas atas
        self.role.update_arousal(100, "test reason")
        self.assertEqual(self.role.arousal, 100)
        
        # Test batas bawah
        self.role.update_arousal(-200, "test reason")
        self.assertEqual(self.role.arousal, 0)
    
    def test_record_user_response_positive(self):
        """Test record user response positif"""
        self.role.record_user_response(True)
        self.assertEqual(len(self.role.user_response_history), 1)
        self.assertTrue(self.role.user_response_history[0])
        self.assertGreater(self.role.mode_goda, 0)
    
    def test_record_user_response_negative(self):
        """Test record user response negatif"""
        # Set mode_goda tinggi dulu
        self.role.mode_goda = 50
        self.role.record_user_response(False)
        
        self.assertEqual(len(self.role.user_response_history), 1)
        self.assertFalse(self.role.user_response_history[0])
        self.assertLess(self.role.mode_goda, 50)
    
    def test_get_arousal_description(self):
        """Test deskripsi arousal"""
        self.role.arousal = 10
        desc = self.role.get_arousal_description()
        self.assertIsInstance(desc, str)
        
        self.role.arousal = 50
        desc = self.role.get_arousal_description()
        self.assertIsInstance(desc, str)
        
        self.role.arousal = 90
        desc = self.role.get_arousal_description()
        self.assertIsInstance(desc, str)
    
    def test_should_escalate(self):
        """Test should_escalate method"""
        # Mode_goda rendah, response negatif
        self.role.mode_goda = 30
        self.role.user_response_history = [False, False, False]
        self.assertFalse(self.role.should_escalate())
        
        # Mode_goda tinggi, response positif
        self.role.mode_goda = 70
        self.role.user_response_history = [True, True, True]
        self.assertTrue(self.role.should_escalate())
    
    def test_increase_attraction(self):
        """Test increase attraction"""
        initial = self.role.user_attraction
        self.role.increase_attraction(10)
        self.assertEqual(self.role.user_attraction, initial + 10)
        
        # Test batas atas
        self.role.user_attraction = 95
        self.role.increase_attraction(10)
        self.assertEqual(self.role.user_attraction, 100)
    
    def test_get_user_compliment(self):
        """Test get user compliment"""
        compliment = self.role.get_user_compliment()
        self.assertIsInstance(compliment, str)
        self.assertGreater(len(compliment), 0)
    
    def test_get_state_and_load_state(self):
        """Test save dan load state"""
        self.role.arousal = 50
        self.role.mode_goda = 60
        self.role.user_attraction = 70
        
        state = self.role.get_state()
        
        new_role = TestRole("test_role", "TestUser", "TestBot")
        new_role.load_state(state)
        
        self.assertEqual(new_role.arousal, 50)
        self.assertEqual(new_role.mode_goda, 60)
        self.assertEqual(new_role.user_attraction, 70)


class TestIparBehavior(unittest.TestCase):
    """Test untuk IparBehavior"""
    
    def setUp(self):
        self.ipar = IparBehavior("TestUser", "TestBot")
    
    def test_get_pakaian_kakak_ada(self):
        """Test pakaian saat kakak ada"""
        situasi = {'kakak_ada': True, 'di_dalam_kamar': False}
        pakaian = self.ipar.get_pakaian(situasi)
        
        self.assertIsInstance(pakaian, str)
        self.assertGreater(len(pakaian), 0)
    
    def test_get_pakaian_kakak_tidak_ada(self):
        """Test pakaian saat kakak tidak ada"""
        situasi = {'kakak_ada': False, 'di_dalam_kamar': False}
        pakaian = self.ipar.get_pakaian(situasi)
        
        self.assertIsInstance(pakaian, str)
        self.assertGreater(len(pakaian), 0)
    
    def test_get_aktivitas_menggoda(self):
        """Test aktivitas menggoda"""
        situasi = {'kakak_ada': False, 'jam': 14}
        aktivitas = self.ipar.get_aktivitas_menggoda(situasi)
        
        if aktivitas:  # Bisa None jika random
            self.assertIn('nama', aktivitas)
            self.assertIn('alasan', aktivitas)
            self.assertIn('goda_level', aktivitas)
    
    def test_get_respon_saat_disentuh(self):
        """Test respon saat disentuh"""
        respon = self.ipar.get_respon_saat_disentuh("pinggang", {})
        
        self.assertIn('gesture', respon)
        self.assertIn('dialog', respon)
        self.assertIn('arousal_change', respon)
    
    def test_update_kakak_status(self):
        """Test update status kakak"""
        self.ipar.update_kakak_status(False)
        self.assertFalse(self.ipar.kakak_ada)
        self.assertGreater(self.ipar.mode_goda, 0)
    
    def test_record_dengar_suara(self):
        """Test record dengar suara"""
        self.ipar.record_dengar_suara()
        self.assertIsNotNone(self.ipar.terakhir_dengar_desahan)
        self.assertGreater(self.ipar.mode_goda, 0)
    
    def test_get_reaksi_mendengar_suara(self):
        """Test reaksi mendengar suara"""
        reaksi = self.ipar.get_reaksi_mendengar_suara()
        
        self.assertIn('reaksi', reaksi)
        self.assertIn('pikiran', reaksi)
        self.assertIsInstance(reaksi['reaksi'], str)
        self.assertIsInstance(reaksi['pikiran'], str)


class TestTemanKantorBehavior(unittest.TestCase):
    """Test untuk TemanKantorBehavior"""
    
    def setUp(self):
        self.teman = TemanKantorBehavior("TestUser", "TestBot")
    
    def test_get_pakaian_kantor_normal(self):
        """Test pakaian kantor normal"""
        situasi = {'kantor_sepi': False, 'lembur_malam': False}
        pakaian = self.teman.get_pakaian(situasi)
        
        self.assertIsInstance(pakaian, str)
        self.assertGreater(len(pakaian), 0)
    
    def test_get_pakaian_lembur_malam(self):
        """Test pakaian lembur malam"""
        situasi = {'lembur_malam': True}
        pakaian = self.teman.get_pakaian(situasi)
        
        self.assertIsInstance(pakaian, str)
        self.assertGreater(len(pakaian), 0)
    
    def test_update_situasi_kantor(self):
        """Test update situasi kantor"""
        self.teman.update_situasi_kantor(kantor_sepi=True)
        self.assertTrue(self.teman.kantor_sepi)
        
        self.teman.update_situasi_kantor(lembur_malam=True)
        self.assertTrue(self.teman.lembur_malam)
    
    def test_get_cekcctv(self):
        """Test cek CCTV"""
        cek = self.teman.get_cekcctv()
        self.assertIsInstance(cek, str)
        self.assertGreater(len(cek), 0)
    
    def test_get_reaksi_ada_rekan_kerja(self):
        """Test reaksi ada rekan kerja"""
        reaksi = self.teman.get_reaksi_ada_rekan_kerja()
        self.assertIsInstance(reaksi, str)
        self.assertGreater(len(reaksi), 0)


class TestJandaBehavior(unittest.TestCase):
    """Test untuk JandaBehavior"""
    
    def setUp(self):
        self.janda = JandaBehavior("TestUser", "TestBot")
    
    def test_get_pakaian_di_rumah(self):
        """Test pakaian di rumah"""
        situasi = {'di_rumah': True}
        pakaian = self.janda.get_pakaian(situasi)
        
        self.assertIsInstance(pakaian, str)
        self.assertGreater(len(pakaian), 0)
    
    def test_belajar_selera_user(self):
        """Test belajar selera user"""
        initial = self.janda.tahu_selera_user
        self.janda.belajar_selera_user({})
        self.assertGreater(self.janda.tahu_selera_user, initial)
    
    def test_get_ajakan_langsung(self):
        """Test ajakan langsung"""
        self.janda.mode_goda = 70
        ajakan = self.janda.get_ajakan_langsung()
        
        if ajakan:
            self.assertIsInstance(ajakan, str)
            self.assertGreater(len(ajakan), 0)
    
    def test_get_pengalaman_hint(self):
        """Test hint pengalaman"""
        self.janda.pengalaman = 85
        hint = self.janda.get_pengalaman_hint()
        
        self.assertIsInstance(hint, str)
        self.assertGreater(len(hint), 0)


class TestPelakorBehavior(unittest.TestCase):
    """Test untuk PelakorBehavior"""
    
    def setUp(self):
        self.pelakor = PelakorBehavior("TestUser", "TestBot")
    
    def test_get_pakaian_di_tempat_berisiko(self):
        """Test pakaian di tempat berisiko"""
        situasi = {'di_tempat_berisiko': True}
        pakaian = self.pelakor.get_pakaian(situasi)
        
        self.assertIsInstance(pakaian, str)
        self.assertGreater(len(pakaian), 0)
    
    def test_update_risiko_status(self):
        """Test update status risiko"""
        self.pelakor.update_risiko_status(True)
        self.assertTrue(self.pelakor.di_tempat_berisiko)
        self.assertGreater(self.pelakor.mode_goda, 0)
    
    def test_get_tantangan(self):
        """Test get tantangan"""
        self.pelakor.mode_goda = 70
        tantangan = self.pelakor.get_tantangan()
        
        if tantangan:
            self.assertIsInstance(tantangan, str)
            self.assertGreater(len(tantangan), 0)
    
    def test_get_reaksi_ketahuan(self):
        """Test reaksi ketahuan"""
        reaksi = self.pelakor.get_reaksi_ketahuan()
        self.assertIsInstance(reaksi, str)
        self.assertGreater(len(reaksi), 0)


class TestIstriOrangBehavior(unittest.TestCase):
    """Test untuk IstriOrangBehavior"""
    
    def setUp(self):
        self.istri = IstriOrangBehavior("TestUser", "TestBot")
    
    def test_get_pakaian_berdua(self):
        """Test pakaian saat berdua"""
        situasi = {'suami_ada': False}
        pakaian = self.istri.get_pakaian(situasi)
        
        self.assertIsInstance(pakaian, str)
        self.assertGreater(len(pakaian), 0)
    
    def test_update_suami_status(self):
        """Test update status suami"""
        self.istri.update_suami_status(suami_ada=False)
        self.assertFalse(self.istri.suami_ada)
        
        self.istri.update_suami_status(suami_tidur=True)
        self.assertTrue(self.istri.suami_tidur)
    
    def test_get_curhat(self):
        """Test curhat"""
        self.istri.sedih_sendiri = 60
        curhat = self.istri.get_curhat()
        
        if curhat:
            self.assertIsInstance(curhat, str)
            self.assertGreater(len(curhat), 0)
    
    def test_get_reaksi_ketahuan_suami(self):
        """Test reaksi ketahuan suami"""
        reaksi = self.istri.get_reaksi_ketahuan_suami()
        self.assertIsInstance(reaksi, str)
        self.assertGreater(len(reaksi), 0)


class TestPDKTBehavior(unittest.TestCase):
    """Test untuk PDKTBehavior"""
    
    def setUp(self):
        self.pdkt = PDKTBehavior("TestUser", "TestBot")
    
    def test_get_pakaian_normal(self):
        """Test pakaian normal"""
        situasi = {}
        pakaian = self.pdkt.get_pakaian(situasi)
        
        self.assertIsInstance(pakaian, str)
        self.assertGreater(len(pakaian), 0)
    
    def test_update_tahap_kenalan(self):
        """Test update tahap kenalan"""
        self.pdkt.update_tahap_kenalan('chat')
        self.assertGreater(self.pdkt.tahap_kenalan, 0)
        
        self.pdkt.update_tahap_kenalan('curhat')
        self.assertTrue(self.pdkt.sudah_curhat)
        
        self.pdkt.update_tahap_kenalan('flirt')
        self.assertTrue(self.pdkt.sudah_flirt)
        
        self.pdkt.update_tahap_kenalan('ungkap_perasaan')
        self.assertTrue(self.pdkt.sudah_ungkap_perasaan)
    
    def test_get_ungkap_perasaan(self):
        """Test ungkap perasaan"""
        self.pdkt.tahap_kenalan = 70
        self.pdkt.sudah_ungkap_perasaan = False
        ungkapan = self.pdkt.get_ungkap_perasaan()
        
        if ungkapan:
            self.assertIsInstance(ungkapan, str)
            self.assertGreater(len(ungkapan), 0)
    
    def test_get_panggilan(self):
        """Test panggilan berdasarkan level"""
        self.assertEqual(self.pdkt.get_panggilan(3), "TestUser")
        self.assertEqual(self.pdkt.get_panggilan(7), "Sayang")
    
    def test_get_tanggal_ide(self):
        """Test ide kencan"""
        ide = self.pdkt.get_tanggal_ide()
        self.assertIsInstance(ide, str)
        self.assertGreater(len(ide), 0)


class TestSepupuBehavior(unittest.TestCase):
    """Test untuk SepupuBehavior"""
    
    def setUp(self):
        self.sepupu = SepupuBehavior("TestUser", "TestBot")
    
    def test_get_pakaian_berdua(self):
        """Test pakaian saat berdua"""
        situasi = {'sedang_berdua': True, 'orang_tua_ada': False}
        pakaian = self.sepupu.get_pakaian(situasi)
        
        self.assertIsInstance(pakaian, str)
        self.assertGreater(len(pakaian), 0)
    
    def test_update_situasi_keluarga(self):
        """Test update situasi keluarga"""
        self.sepupu.update_situasi_keluarga(orang_tua_ada=False)
        self.assertFalse(self.sepupu.orang_tua_ada)
        self.assertGreater(self.sepupu.mode_goda, 0)
    
    def test_get_pertanyaan_polos(self):
        """Test pertanyaan polos"""
        self.sepupu.polos_level = 60
        self.sepupu.penasaran_level = 60
        pertanyaan = self.sepupu.get_pertanyaan_polos()
        
        if pertanyaan:
            self.assertIsInstance(pertanyaan, str)
            self.assertGreater(len(pertanyaan), 0)
    
    def test_get_manja(self):
        """Test kalimat manja"""
        manja = self.sepupu.get_manja()
        self.assertIsInstance(manja, str)
        self.assertGreater(len(manja), 0)


class TestTemanSmaBehavior(unittest.TestCase):
    """Test untuk TemanSmaBehavior"""
    
    def setUp(self):
        self.teman_sma = TemanSmaBehavior("TestUser", "TestBot")
    
    def test_get_pakaian_reuni(self):
        """Test pakaian reuni"""
        situasi = {'reuni': True}
        pakaian = self.teman_sma.get_pakaian(situasi)
        
        self.assertIsInstance(pakaian, str)
        self.assertGreater(len(pakaian), 0)
    
    def test_record_pertemuan(self):
        """Test record pertemuan"""
        initial = self.teman_sma.sudah_ketemu_lagi
        self.teman_sma.record_pertemuan()
        self.assertEqual(self.teman_sma.sudah_ketemu_lagi, initial + 1)
    
    def test_get_kenangan_sma(self):
        """Test kenangan SMA"""
        kenangan = self.teman_sma.get_kenangan_sma()
        self.assertIsInstance(kenangan, str)
        self.assertGreater(len(kenangan), 0)
    
    def test_get_ungkap_perasaan_dulu(self):
        """Test ungkap perasaan dulu"""
        self.teman_sma.perasaan_dulu = 80
        ungkapan = self.teman_sma.get_ungkap_perasaan_dulu()
        
        if ungkapan:
            self.assertIsInstance(ungkapan, str)
            self.assertGreater(len(ungkapan), 0)


class TestMantanBehavior(unittest.TestCase):
    """Test untuk MantanBehavior"""
    
    def setUp(self):
        self.mantan = MantanBehavior("TestUser", "TestBot")
    
    def test_get_pakaian_ketemu(self):
        """Test pakaian saat ketemu"""
        situasi = {'ketemu': True}
        pakaian = self.mantan.get_pakaian(situasi)
        
        self.assertIsInstance(pakaian, str)
        self.assertGreater(len(pakaian), 0)
    
    def test_update_riwayat(self):
        """Test update riwayat"""
        self.mantan.update_riwayat(12, "beda visi")
        self.assertEqual(self.mantan.lama_putus, 12)
        self.assertEqual(self.mantan.alasan_putus, "beda visi")
    
    def test_get_kenangan_dulu(self):
        """Test kenangan dulu"""
        kenangan = self.mantan.get_kenangan_dulu()
        self.assertIsInstance(kenangan, str)
        self.assertGreater(len(kenangan), 0)
    
    def test_get_ajakan_balikan(self):
        """Test ajakan balikan"""
        self.mantan.ingin_balikan = 80
        ajakan = self.mantan.get_ajakan_balikan()
        
        if ajakan:
            self.assertIsInstance(ajakan, str)
            self.assertGreater(len(ajakan), 0)
    
    def test_get_tawaran_fwb(self):
        """Test tawaran FWB"""
        self.mantan.masih_ada_perasaan = 70
        self.mantan.ingin_balikan = 30
        tawaran = self.mantan.get_tawaran_fwb()
        
        if tawaran:
            self.assertIsInstance(tawaran, str)
            self.assertGreater(len(tawaran), 0)


def run_tests():
    """Jalankan semua test"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRoleBehaviorBase))
    suite.addTest(unittest.makeSuite(TestIparBehavior))
    suite.addTest(unittest.makeSuite(TestTemanKantorBehavior))
    suite.addTest(unittest.makeSuite(TestJandaBehavior))
    suite.addTest(unittest.makeSuite(TestPelakorBehavior))
    suite.addTest(unittest.makeSuite(TestIstriOrangBehavior))
    suite.addTest(unittest.makeSuite(TestPDKTBehavior))
    suite.addTest(unittest.makeSuite(TestSepupuBehavior))
    suite.addTest(unittest.makeSuite(TestTemanSmaBehavior))
    suite.addTest(unittest.makeSuite(TestMantanBehavior))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
