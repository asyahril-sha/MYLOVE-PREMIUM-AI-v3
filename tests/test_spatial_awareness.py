# tests/test_spatial_awareness.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - SPATIAL AWARENESS UNIT TEST
=============================================================================
Test untuk memastikan spatial awareness bekerja dengan benar
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

from dynamics.spatial_awareness import SpatialAwareness


class TestSpatialAwareness(unittest.TestCase):
    """Unit test untuk SpatialAwareness"""
    
    def setUp(self):
        """Setup sebelum setiap test"""
        self.spatial = SpatialAwareness()
    
    def test_parse_duduk_di_antara_kaki(self):
        """Test parsing posisi duduk di antara kaki"""
        messages = [
            "duduk di antara kakimu",
            "ayo duduk di antara kaki aku",
            "duduk di sela kakiku",
            "di antara pahamu dong"
        ]
        
        for msg in messages:
            result = self.spatial.parse(msg)
            self.assertTrue(result['found'], f"Failed for: {msg}")
            self.assertEqual(result['position_type'], 'duduk_di_antara_kaki')
    
    def test_parse_duduk_di_pangkuan(self):
        """Test parsing posisi duduk di pangkuan"""
        messages = [
            "duduk di pangkuanku",
            "ayo duduk dipangkuan",
            "duduk di atas paha aku"
        ]
        
        for msg in messages:
            result = self.spatial.parse(msg)
            self.assertTrue(result['found'], f"Failed for: {msg}")
            self.assertEqual(result['position_type'], 'duduk_di_pangkuan')
    
    def test_parse_di_belakang(self):
        """Test parsing posisi di belakang"""
        messages = [
            "di belakang aku",
            "berdiri di belakangku",
            "dibelakang kamu",
            "dari belakang"
        ]
        
        for msg in messages:
            result = self.spatial.parse(msg)
            self.assertTrue(result['found'], f"Failed for: {msg}")
            self.assertEqual(result['position_type'], 'di_belakang')
    
    def test_parse_bersebelahan(self):
        """Test parsing posisi bersebelahan"""
        messages = [
            "duduk bersebelahan",
            "di samping aku",
            "berdampingan",
            "duduk disamping"
        ]
        
        for msg in messages:
            result = self.spatial.parse(msg)
            self.assertTrue(result['found'], f"Failed for: {msg}")
            self.assertEqual(result['position_type'], 'bersebelahan')
    
    def test_parse_berhadapan(self):
        """Test parsing posisi berhadapan"""
        messages = [
            "duduk berhadapan",
            "saling berhadapan",
            "menghadap aku"
        ]
        
        for msg in messages:
            result = self.spatial.parse(msg)
            self.assertTrue(result['found'], f"Failed for: {msg}")
            self.assertEqual(result['position_type'], 'berhadapan')
    
    def test_parse_di_depan(self):
        """Test parsing posisi di depan"""
        messages = [
            "di depan aku",
            "didepan kamu",
            "berdiri di depan"
        ]
        
        for msg in messages:
            result = self.spatial.parse(msg)
            self.assertTrue(result['found'], f"Failed for: {msg}")
            self.assertEqual(result['position_type'], 'di_depan')
    
    def test_parse_no_position(self):
        """Test pesan tanpa posisi"""
        messages = [
            "hai apa kabar",
            "lagi ngapain",
            "makan yuk"
        ]
        
        for msg in messages:
            result = self.spatial.parse(msg)
            self.assertFalse(result['found'])
    
    def test_get_gesture(self):
        """Test mendapatkan gesture berdasarkan posisi"""
        # Test dengan posisi yang ada
        self.spatial.current['position_type'] = 'duduk_di_antara_kaki'
        gesture = self.spatial.get_gesture()
        
        self.assertIsInstance(gesture, str)
        self.assertGreater(len(gesture), 0)
        self.assertTrue(gesture.startswith('*') and gesture.endswith('*'))
    
    def test_get_gesture_by_arousal(self):
        """Test gesture berdasarkan arousal"""
        # Arousal tinggi
        gesture_high = self.spatial.get_gesture_by_arousal(80)
        self.assertIsInstance(gesture_high, str)
        
        # Arousal rendah
        gesture_low = self.spatial.get_gesture_by_arousal(20)
        self.assertIsInstance(gesture_low, str)
        
        # Seharusnya berbeda
        # Note: Bisa sama karena random, tapi kemungkinan kecil
        # Tidak assert berbeda karena random
    
    def test_get_context_for_prompt(self):
        """Test mendapatkan konteks untuk prompt"""
        # Tanpa posisi
        context = self.spatial.get_context_for_prompt()
        self.assertEqual(context, "")
        
        # Dengan posisi
        self.spatial.parse("duduk di antara kakimu")
        context = self.spatial.get_context_for_prompt()
        
        self.assertIsInstance(context, str)
        self.assertIn("POSISI SAAT INI", context)
        self.assertIn("di antara kaki user", context)
    
    def test_update_position(self):
        """Test update posisi manual"""
        self.spatial.update_position('di_belakang', 'di belakang user')
        
        self.assertEqual(self.spatial.current['position_type'], 'di_belakang')
        self.assertEqual(self.spatial.current['relative'], 'di belakang user')
    
    def test_add_body_contact(self):
        """Test menambah kontak fisik"""
        self.spatial.add_body_contact('tangan di pinggang')
        self.assertIn('tangan di pinggang', self.spatial.current['body_contact'])
        
        # Test tidak duplikat
        self.spatial.add_body_contact('tangan di pinggang')
        self.assertEqual(len(self.spatial.current['body_contact']), 1)
    
    def test_clear_position(self):
        """Test reset posisi"""
        self.spatial.parse("duduk di antara kakimu")
        self.assertTrue(self.spatial.has_position())
        
        self.spatial.clear_position()
        self.assertFalse(self.spatial.has_position())
        self.assertIsNone(self.spatial.current['position_type'])
    
    def test_has_position(self):
        """Test has_position method"""
        self.assertFalse(self.spatial.has_position())
        
        self.spatial.parse("duduk di antara kakimu")
        self.assertTrue(self.spatial.has_position())
    
    def test_get_state_and_load_state(self):
        """Test save dan load state"""
        self.spatial.parse("duduk di antara kakimu")
        self.spatial.add_body_contact('tangan di paha')
        
        state = self.spatial.get_state()
        
        new_spatial = SpatialAwareness()
        new_spatial.load_state(state)
        
        self.assertEqual(new_spatial.current['position_type'], self.spatial.current['position_type'])
        self.assertEqual(new_spatial.current['relative'], self.spatial.current['relative'])
        self.assertIn('tangan di paha', new_spatial.current['body_contact'])


class TestSpatialAwarenessEdgeCases(unittest.TestCase):
    """Edge cases untuk SpatialAwareness"""
    
    def setUp(self):
        self.spatial = SpatialAwareness()
    
    def test_mixed_case_message(self):
        """Test pesan dengan huruf campuran"""
        result = self.spatial.parse("DuDuK Di AnTaRa KaKiMu")
        self.assertTrue(result['found'])
        self.assertEqual(result['position_type'], 'duduk_di_antara_kaki')
    
    def test_message_with_typo(self):
        """Test pesan dengan typo minor"""
        # Typo kecil masih bisa terdeteksi
        result = self.spatial.parse("dduk di antara kakimu")
        # Mungkin tidak terdeteksi karena typo, tapi tidak error
        # Assert tidak error
        self.assertIsNotNone(result)
    
    def test_multiple_positions_in_one_message(self):
        """Test pesan dengan multiple posisi"""
        result = self.spatial.parse("duduk di pangkuan lalu pindah di belakang")
        # Seharusnya mendeteksi posisi pertama
        self.assertTrue(result['found'])
    
    def test_gesture_consistency(self):
        """Test konsistensi gesture untuk posisi yang sama"""
        self.spatial.current['position_type'] = 'duduk_di_antara_kaki'
        
        gestures = set()
        for _ in range(10):
            gesture = self.spatial.get_gesture()
            gestures.add(gesture)
        
        # Seharusnya ada variasi gesture
        self.assertGreater(len(gestures), 1)
    
    def test_get_gesture_without_position(self):
        """Test gesture tanpa posisi"""
        gesture = self.spatial.get_gesture()
        self.assertIsInstance(gesture, str)
        self.assertGreater(len(gesture), 0)


class TestSpatialAwarenessIntegration(unittest.TestCase):
    """Integration test untuk SpatialAwareness"""
    
    def setUp(self):
        self.spatial = SpatialAwareness()
    
    def test_continuous_position_tracking(self):
        """Test tracking posisi berkelanjutan"""
        # Scene 1
        self.spatial.parse("duduk di antara kakimu")
        self.assertEqual(self.spatial.current['position_type'], 'duduk_di_antara_kaki')
        
        # Scene 2 - pindah posisi
        self.spatial.parse("pindah di belakang")
        self.assertEqual(self.spatial.current['position_type'], 'di_belakang')
        
        # Scene 3 - kembali
        self.spatial.parse("balik lagi ke depan")
        self.assertEqual(self.spatial.current['position_type'], 'di_depan')
    
    def test_body_contact_accumulation(self):
        """Test akumulasi kontak fisik"""
        self.spatial.add_body_contact('tangan di pinggang')
        self.spatial.add_body_contact('kaki bersentuhan')
        self.spatial.add_body_contact('dada menempel')
        
        self.assertEqual(len(self.spatial.current['body_contact']), 3)
    
    def test_get_gesture_with_arousal(self):
        """Test gesture dengan arousal"""
        # Test berbagai level arousal
        for arousal in [20, 40, 60, 80, 95]:
            gesture = self.spatial.get_gesture_by_arousal(arousal)
            self.assertIsInstance(gesture, str)
            self.assertGreater(len(gesture), 0)


def run_tests():
    """Jalankan semua test"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSpatialAwareness))
    suite.addTest(unittest.makeSuite(TestSpatialAwarenessEdgeCases))
    suite.addTest(unittest.makeSuite(TestSpatialAwarenessIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
