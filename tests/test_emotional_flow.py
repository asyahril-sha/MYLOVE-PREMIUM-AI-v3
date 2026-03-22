# tests/test_emotional_flow.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - EMOTIONAL FLOW UNIT TEST
=============================================================================
Test untuk memastikan emotional flow bekerja dengan benar
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

from dynamics.emotional_flow import EmotionalFlow, EmotionalState


class TestEmotionalFlow(unittest.TestCase):
    """Unit test untuk EmotionalFlow"""
    
    def setUp(self):
        """Setup sebelum setiap test"""
        self.flow = EmotionalFlow("test_role")
    
    def test_initial_state(self):
        """Test state awal"""
        self.assertEqual(self.flow.current_state, EmotionalState.NETRAL)
        self.assertEqual(self.flow.arousal, 0)
    
    def test_arousal_update_positive(self):
        """Test update arousal positif"""
        stimulus = {
            'user_arousal': 0.5,
            'user_message': 'aku horny',
            'situasi': {'kakak_ada': False},
            'trigger_reason': 'user_menggoda'
        }
        
        result = self.flow.update(stimulus)
        
        self.assertGreater(result['arousal'], 0)
        self.assertIn('arousal_change', result)
    
    def test_arousal_update_negative(self):
        """Test update arousal negatif"""
        # Set arousal tinggi dulu
        self.flow.arousal = 80
        
        stimulus = {
            'user_arousal': 0,
            'user_message': 'tidak',
            'situasi': {},
            'trigger_reason': 'negative_response',
            'is_positive_response': False
        }
        
        result = self.flow.update(stimulus)
        
        # Seharusnya arousal turun
        self.assertLess(result['arousal'], 80)
    
    def test_state_transition_allowed(self):
        """Test transisi state yang diperbolehkan"""
        # Dari NETRAL ke PENASARAN (diperbolehkan)
        self.flow.arousal = 15
        self.flow._get_state_from_arousal = Mock(return_value=EmotionalState.PENASARAN)
        
        result = self.flow.update({'user_arousal': 0.3})
        
        self.assertEqual(result['new_state'], EmotionalState.PENASARAN.value)
    
    def test_state_transition_not_allowed(self):
        """Test transisi state yang tidak diperbolehkan"""
        # Set state ke NETRAL
        self.flow.current_state = EmotionalState.NETRAL
        
        # Coba langsung ke HORNY (tidak diperbolehkan)
        self.flow._get_state_from_arousal = Mock(return_value=EmotionalState.HORNY)
        
        result = self.flow.update({'user_arousal': 0.9})
        
        # Seharusnya tetap di NETRAL
        self.assertEqual(result['new_state'], EmotionalState.NETRAL.value)
    
    def test_arousal_calculation_from_user_message(self):
        """Test perhitungan arousal dari pesan user"""
        stimulus = {
            'user_arousal': 0,
            'user_message': 'aku horny banget, pengen kamu',
            'situasi': {}
        }
        
        delta = self.flow._calculate_arousal_delta(stimulus)
        
        # Seharusnya ada delta positif dari kata kunci
        self.assertGreater(delta, 0)
    
    def test_arousal_calculation_from_situasi(self):
        """Test perhitungan arousal dari situasi"""
        stimulus = {
            'user_arousal': 0,
            'user_message': 'hai',
            'situasi': {'kakak_ada': False, 'di_dalam_kamar': True}
        }
        
        delta = self.flow._calculate_arousal_delta(stimulus)
        
        # Seharusnya ada delta positif dari situasi
        self.assertGreater(delta, 0)
    
    def test_get_description(self):
        """Test deskripsi emotional state"""
        self.flow.arousal = 80
        desc = self.flow.get_description()
        
        self.assertIsInstance(desc, str)
        self.assertGreater(len(desc), 0)
    
    def test_get_gesture_hint(self):
        """Test gesture hint"""
        self.flow.current_state = EmotionalState.HORNY
        hint = self.flow.get_gesture_hint()
        
        self.assertIsInstance(hint, str)
        self.assertGreater(len(hint), 0)
    
    def test_reset(self):
        """Test reset emotional flow"""
        self.flow.arousal = 50
        self.flow.current_state = EmotionalState.HORNY
        
        self.flow.reset()
        
        self.assertEqual(self.flow.arousal, 0)
        self.assertEqual(self.flow.current_state, EmotionalState.NETRAL)
    
    def test_is_horny(self):
        """Test is_horny method"""
        self.flow.current_state = EmotionalState.HORNY
        self.assertTrue(self.flow.is_horny())
        
        self.flow.current_state = EmotionalState.NETRAL
        self.assertFalse(self.flow.is_horny())
    
    def test_is_climax(self):
        """Test is_climax method"""
        self.flow.current_state = EmotionalState.CLIMAX
        self.assertTrue(self.flow.is_climax())
        
        self.flow.current_state = EmotionalState.NETRAL
        self.assertFalse(self.flow.is_climax())
    
    def test_is_aroused(self):
        """Test is_aroused method"""
        self.flow.arousal = 60
        self.assertTrue(self.flow.is_aroused(50))
        
        self.flow.arousal = 30
        self.assertFalse(self.flow.is_aroused(50))
    
    def test_format_for_prompt(self):
        """Test format for prompt"""
        self.flow.arousal = 60
        formatted = self.flow.format_for_prompt()
        
        self.assertIsInstance(formatted, str)
        self.assertIn("EMOSI BOT", formatted)
        self.assertIn(str(self.flow.arousal), formatted)


class TestEmotionalFlowIntegration(unittest.TestCase):
    """Integration test untuk EmotionalFlow dengan RoleBehavior"""
    
    def setUp(self):
        """Setup sebelum setiap test"""
        from dynamics.ipar_behavior import IparBehavior
        
        self.role = IparBehavior("TestUser", "TestBot")
        self.flow = EmotionalFlow("ipar", self.role)
    
    def test_integration_with_role(self):
        """Test integrasi dengan role behavior"""
        stimulus = {
            'user_arousal': 0.5,
            'user_message': 'aku horny',
            'situasi': {'kakak_ada': False},
            'trigger_reason': 'user_menggoda'
        }
        
        result = self.flow.update(stimulus)
        
        # Role behavior harus terupdate
        self.assertGreater(self.role.arousal, 0)
        self.assertGreater(self.role.mode_goda, 0)
    
    def test_emotional_memory_integration(self):
        """Test integrasi dengan emotional memory"""
        from memory.emotional_memory import EmotionalMemory
        
        memory = EmotionalMemory()
        
        # Simulasi update emosi
        self.flow.arousal = 70
        self.flow.current_state = EmotionalState.HORNY
        
        memory.add_memory(
            emotion=self.flow.current_state.value,
            intensity=self.flow.arousal / 100,
            context={'situasi': 'berduaan'},
            user_message="aku horny",
            bot_response="aku juga",
            arousal=self.flow.arousal
        )
        
        memories = memory.get_recent_memories()
        self.assertGreater(len(memories), 0)
        self.assertEqual(memories[0]['emotion'], 'horny')


def run_tests():
    """Jalankan semua test"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestEmotionalFlow))
    suite.addTest(unittest.makeSuite(TestEmotionalFlowIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
