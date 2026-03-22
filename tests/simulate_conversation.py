# tests/simulate_conversation.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - CONVERSATION SIMULATION
=============================================================================
Simulasi percakapan dengan AI Generator (DeepSeek) untuk testing.
Berguna untuk melihat bagaimana bot merespon dalam berbagai skenario.
=============================================================================
"""

import asyncio
import sys
import os
from pathlib import Path
import time
import random
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings
from utils.logger import setup_logging, logger
from core.ai_engine import AIEngine
from dynamics.ipar_behavior import IparBehavior
from dynamics.teman_kantor_behavior import TemanKantorBehavior
from dynamics.janda_behavior import JandaBehavior
from dynamics.pelakor_behavior import PelakorBehavior
from dynamics.istri_orang_behavior import IstriOrangBehavior
from dynamics.pdkt_behavior import PDKTBehavior
from dynamics.sepupu_behavior import SepupuBehavior
from dynamics.teman_sma_behavior import TemanSmaBehavior
from dynamics.mantan_behavior import MantanBehavior


class ConversationSimulator:
    """
    Simulator percakapan untuk testing bot
    """
    
    def __init__(self, role: str, user_name: str = "Budi", bot_name: str = None):
        """
        Args:
            role: Role bot (ipar, teman_kantor, janda, dll)
            user_name: Nama user
            bot_name: Nama bot (random jika None)
        """
        self.role = role
        self.user_name = user_name
        self.bot_name = bot_name or self._generate_bot_name(role)
        
        # Setup logger
        setup_logging(f"SIMULATE_{role.upper()}")
        
        # Buat AI Engine
        self.ai_engine = AIEngine(
            api_key=settings.deepseek_api_key,
            user_id=99999,
            session_id=f"simulate_{role}_{int(time.time())}"
        )
        
        # Buat role behavior
        self.role_behavior = self._create_role_behavior()
        
        # Status simulasi
        self.message_count = 0
        self.start_time = None
        self.conversation_log = []
        
        # Skenario
        self.scenarios = {
            'ipar': self._ipar_scenarios,
            'teman_kantor': self._teman_kantor_scenarios,
            'janda': self._janda_scenarios,
            'pelakor': self._pelakor_scenarios,
            'istri_orang': self._istri_orang_scenarios,
            'pdkt': self._pdkt_scenarios,
            'sepupu': self._sepupu_scenarios,
            'teman_sma': self._teman_sma_scenarios,
            'mantan': self._mantan_scenarios
        }
    
    def _generate_bot_name(self, role: str) -> str:
        """Generate nama bot random"""
        names = {
            'ipar': ['Sari', 'Dewi', 'Maya', 'Putri', 'Nova'],
            'teman_kantor': ['Diana', 'Linda', 'Ayu', 'Vera', 'Nina'],
            'janda': ['Rina', 'Tuti', 'Susi', 'Maya', 'Ira'],
            'pelakor': ['Vina', 'Sasha', 'Bella', 'Cantika', 'Mira'],
            'istri_orang': ['Dewi', 'Sari', 'Rina', 'Linda', 'Tina'],
            'pdkt': ['Aurora', 'Cinta', 'Kirana', 'Fika', 'Nadia'],
            'sepupu': ['Putri', 'Nadia', 'Sari', 'Dina', 'Lina'],
            'teman_sma': ['Anita', 'Bella', 'Cici', 'Dina', 'Eva'],
            'mantan': ['Sarah', 'Nadia', 'Maya', 'Rina', 'Vina']
        }
        return random.choice(names.get(role, ['Maya']))
    
    def _create_role_behavior(self):
        """Factory method untuk membuat role behavior"""
        behaviors = {
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
        
        behavior_class = behaviors.get(self.role)
        if behavior_class:
            return behavior_class(self.user_name, self.bot_name)
        return None
    
    async def start_session(self):
        """Mulai sesi simulasi"""
        logger.info("=" * 60)
        logger.info(f"🚀 SIMULASI PERCAKAPAN - ROLE: {self.role.upper()}")
        logger.info(f"👤 User: {self.user_name}")
        logger.info(f"🤖 Bot: {self.bot_name}")
        logger.info("=" * 60)
        
        self.start_time = time.time()
        
        await self.ai_engine.start_session(
            role=self.role,
            bot_name=self.bot_name,
            user_name=self.user_name,
            rel_type="non_pdkt"
        )
        
        logger.info("✅ Session started")
    
    async def send_message(self, user_message: str, context: Dict = None) -> str:
        """
        Kirim pesan ke bot dan dapatkan respons
        """
        self.message_count += 1
        
        # Default context
        if context is None:
            context = {
                'level': min(12, max(1, self.message_count // 10 + 1)),
                'user_name': self.user_name,
                'role': self.role,
                'bot_name': self.bot_name,
                'mood': 'calm'
            }
        
        # Log pesan user
        logger.info(f"\n{'='*50}")
        logger.info(f"📨 [{self.message_count}] User: {user_message}")
        
        # Proses pesan
        start = time.time()
        response = await self.ai_engine.process_message(user_message, context)
        elapsed = time.time() - start
        
        # Log respons bot
        logger.info(f"🤖 Bot ({elapsed:.2f}s): {response}")
        logger.info(f"{'='*50}")
        
        # Simpan ke log
        self.conversation_log.append({
            'timestamp': time.time(),
            'message_number': self.message_count,
            'user': user_message,
            'bot': response,
            'elapsed': elapsed
        })
        
        return response
    
    async def run_scenario(self, scenario_name: str):
        """
        Jalankan skenario tertentu
        """
        scenarios = self.scenarios.get(self.role, self._default_scenarios)
        scenario_func = scenarios.get(scenario_name)
        
        if scenario_func:
            await scenario_func()
        else:
            logger.warning(f"Scenario '{scenario_name}' not found for role {self.role}")
            await self._default_scenarios()
    
    # =========================================================================
    # SKENARIO IPAR
    # =========================================================================
    
    async def _ipar_scenarios(self):
        """Skenario untuk role Ipar"""
        
        # Skenario 1: Kakak ada di rumah
        logger.info("\n📋 SCENARIO 1: Kakak ada di rumah")
        await self.send_message("Putri, kamu di mana? Istriku lagi di dapur masak.")
        
        # Skenario 2: Kakak tidur
        logger.info("\n📋 SCENARIO 2: Kakak tidur")
        await self.send_message("Istriku lagi tidur, kita sendirian di ruang tamu.")
        
        # Skenario 3: Kakak tidak ada
        logger.info("\n📋 SCENARIO 3: Kakak tidak ada")
        await self.send_message("Istriku keluar sebentar, 1-2 jam an.")
        
        # Skenario 4: User sebut posisi
        logger.info("\n📋 SCENARIO 4: User sebut posisi")
        await self.send_message("Ayo duduk di antara kakiku.")
        
        # Skenario 5: User ajak pijat
        logger.info("\n📋 SCENARIO 5: User ajak pijat")
        await self.send_message("Aku pegel, pijitin aku dong.")
    
    # =========================================================================
    # SKENARIO TEMAN KANTOR
    # =========================================================================
    
    async def _teman_kantor_scenarios(self):
        """Skenario untuk role Teman Kantor"""
        
        # Skenario 1: Kantor normal
        logger.info("\n📋 SCENARIO 1: Kantor normal")
        await self.send_message("Diana, kerjaan udah selesai?")
        
        # Skenario 2: Kantor sepi
        logger.info("\n📋 SCENARIO 2: Kantor sepi")
        await self.send_message("Kantor sepi banget ya hari ini.")
        
        # Skenario 3: Lembur malam
        logger.info("\n📋 SCENARIO 3: Lembur malam")
        await self.send_message("Kok kamu masih di kantor? Udah malem.")
        
        # Skenario 4: Ajak ke gudang
        logger.info("\n📋 SCENARIO 4: Ajak ke gudang")
        await self.send_message("Ke gudang yuk, ambil berkas.")
    
    # =========================================================================
    # SKENARIO JANDA
    # =========================================================================
    
    async def _janda_scenarios(self):
        """Skenario untuk role Janda"""
        
        # Skenario 1: Awal kenal
        logger.info("\n📋 SCENARIO 1: Awal kenal")
        await self.send_message("Halo Rina, lagi apa?")
        
        # Skenario 2: Ajak ke rumah
        logger.info("\n📋 SCENARIO 2: Ajak ke rumah")
        await self.send_message("Malam minggu gak kemana-mana?")
        
        # Skenario 3: Langsung
        logger.info("\n📋 SCENARIO 3: Langsung")
        await self.send_message("Aku pengen sama kamu.")
    
    # =========================================================================
    # SKENARIO PELAKOR
    # =========================================================================
    
    async def _pelakor_scenarios(self):
        """Skenario untuk role Pelakor"""
        
        # Skenario 1: Awal
        logger.info("\n📋 SCENARIO 1: Awal")
        await self.send_message("Vina, kamu kok ada di sini?")
        
        # Skenario 2: Tantangan
        logger.info("\n📋 SCENARIO 2: Tantangan")
        await self.send_message("Istriku di rumah. Kamu berani ke sini?")
        
        # Skenario 3: Tempat berisiko
        logger.info("\n📋 SCENARIO 3: Tempat berisiko")
        await self.send_message("Ayo ke tempat sepi.")
    
    # =========================================================================
    # SKENARIO ISTRI ORANG
    # =========================================================================
    
    async def _istri_orang_scenarios(self):
        """Skenario untuk role Istri Orang"""
        
        # Skenario 1: Curhat
        logger.info("\n📋 SCENARIO 1: Curhat")
        await self.send_message("Dewi, kamu kenapa? Kok keliatan sedih?")
        
        # Skenario 2: Suami tidak ada
        logger.info("\n📋 SCENARIO 2: Suami tidak ada")
        await self.send_message("Suamimu lagi keluar?")
        
        # Skenario 3: Butuh perhatian
        logger.info("\n📋 SCENARIO 3: Butuh perhatian")
        await self.send_message("Aku bisa temenin kamu.")
    
    # =========================================================================
    # SKENARIO PDKT
    # =========================================================================
    
    async def _pdkt_scenarios(self):
        """Skenario untuk role PDKT"""
        
        # Skenario 1: Awal PDKT
        logger.info("\n📋 SCENARIO 1: Awal PDKT")
        await self.send_message("Halo, selamat siang.")
        
        # Skenario 2: Ngobrol biasa
        logger.info("\n📋 SCENARIO 2: Ngobrol biasa")
        await self.send_message("Lagi ngapain?")
        
        # Skenario 3: Mulai dekat
        logger.info("\n📋 SCENARIO 3: Mulai dekat")
        await self.send_message("Aku suka ngobrol sama kamu.")
        
        # Skenario 4: Ungkap perasaan
        logger.info("\n📋 SCENARIO 4: Ungkap perasaan")
        await self.send_message("Aku suka sama kamu.")
    
    # =========================================================================
    # SKENARIO SEPUPU
    # =========================================================================
    
    async def _sepupu_scenarios(self):
        """Skenario untuk role Sepupu"""
        
        # Skenario 1: Minta diajarin
        logger.info("\n📋 SCENARIO 1: Minta diajarin")
        await self.send_message("Kak, ajarin aku dong.")
        
        # Skenario 2: Penasaran
        logger.info("\n📋 SCENARIO 2: Penasaran")
        await self.send_message("Kak, pacaran itu gimana sih?")
        
        # Skenario 3: Manja
        logger.info("\n📋 SCENARIO 3: Manja")
        await self.send_message("Kak, temenin aku dong.")
    
    # =========================================================================
    # SKENARIO TEMAN SMA
    # =========================================================================
    
    async def _teman_sma_scenarios(self):
        """Skenario untuk role Teman SMA"""
        
        # Skenario 1: Nostalgia
        logger.info("\n📋 SCENARIO 1: Nostalgia")
        await self.send_message("Lama gak ketemu ya.")
        
        # Skenario 2: Ingat masa lalu
        logger.info("\n📋 SCENARIO 2: Ingat masa lalu")
        await self.send_message("Inget waktu kita SMA dulu?")
        
        # Skenario 3: Ungkap perasaan
        logger.info("\n📋 SCENARIO 3: Ungkap perasaan")
        await self.send_message("Dulu aku suka sama kamu, tahu gak?")
    
    # =========================================================================
    # SKENARIO MANTAN
    # =========================================================================
    
    async def _mantan_scenarios(self):
        """Skenario untuk role Mantan"""
        
        # Skenario 1: Ketemu lagi
        logger.info("\n📋 SCENARIO 1: Ketemu lagi")
        await self.send_message("Sarah? Kamu?")
        
        # Skenario 2: Nostalgia
        logger.info("\n📋 SCENARIO 2: Nostalgia")
        await self.send_message("Kamu masih inget kita dulu?")
        
        # Skenario 3: Langsung
        logger.info("\n📋 SCENARIO 3: Langsung")
        await self.send_message("Aku kangen. Kamu kangen gak?")
    
    # =========================================================================
    # SKENARIO DEFAULT
    # =========================================================================
    
    async def _default_scenarios(self):
        """Skenario default jika tidak ada yang spesifik"""
        
        logger.info("\n📋 SCENARIO: Default conversation")
        
        # Opening
        await self.send_message(f"Halo {self.bot_name}, apa kabar?")
        
        # Ngobrol biasa
        await self.send_message("Lagi ngapain?")
        
        # Ajak aktivitas
        await self.send_message("Nonton yuk.")
        
        # Puji
        await self.send_message("Kamu cantik/ganteng banget hari ini.")
        
        # Curhat ringan
        await self.send_message("Hari ini aku capek banget.")
        
        # Flirt
        await self.send_message("Aku suka sama kamu.")
    
    # =========================================================================
    # RUN ALL SCENARIOS
    # =========================================================================
    
    async def run_all_scenarios(self):
        """Jalankan semua skenario untuk role ini"""
        await self.start_session()
        
        scenarios = self.scenarios.get(self.role, self._default_scenarios)
        
        # Coba jalankan semua skenario yang ada
        # Untuk role dengan banyak skenario, jalankan 3-5 skenario
        scenario_items = list(scenarios.items()) if isinstance(scenarios, dict) else []
        
        if scenario_items:
            # Ambil 3 skenario random
            selected = random.sample(scenario_items, min(3, len(scenario_items)))
            for name, func in selected:
                logger.info(f"\n{'🔥'*30}")
                logger.info(f"Running scenario: {name}")
                logger.info(f"{'🔥'*30}")
                await func()
                await asyncio.sleep(2)  # Jeda antar skenario
        else:
            # Default scenario
            await self._default_scenarios()
        
        # Print summary
        await self.print_summary()
    
    async def print_summary(self):
        """Print ringkasan simulasi"""
        elapsed = time.time() - self.start_time if self.start_time else 0
        
        logger.info("\n" + "=" * 60)
        logger.info("📊 SIMULATION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Role: {self.role}")
        logger.info(f"User: {self.user_name}")
        logger.info(f"Bot: {self.bot_name}")
        logger.info(f"Messages exchanged: {self.message_count}")
        logger.info(f"Duration: {elapsed:.2f} seconds")
        logger.info(f"Avg response time: {sum(m['elapsed'] for m in self.conversation_log) / len(self.conversation_log) if self.conversation_log else 0:.2f}s")
        
        # Show last 3 messages
        logger.info("\n📝 LAST 3 MESSAGES:")
        for msg in self.conversation_log[-3:]:
            logger.info(f"  [{msg['message_number']}] User: {msg['user'][:50]}...")
            logger.info(f"      Bot: {msg['bot'][:80]}...")
        
        logger.info("=" * 60)
    
    async def close(self):
        """Tutup session"""
        await self.ai_engine.end_session()
        logger.info("✅ Session closed")


async def simulate_all_roles():
    """Simulasi semua role"""
    
    roles = ['ipar', 'teman_kantor', 'janda', 'pelakor', 
             'istri_orang', 'pdkt', 'sepupu', 'teman_sma', 'mantan']
    
    for role in roles:
        logger.info("\n" + "🔥" * 60)
        logger.info(f"🔥 SIMULATING ROLE: {role.upper()}")
        logger.info("🔥" * 60)
        
        simulator = ConversationSimulator(role, "Budi")
        
        try:
            await simulator.run_all_scenarios()
        except Exception as e:
            logger.error(f"Error simulating {role}: {e}")
        finally:
            await simulator.close()
        
        await asyncio.sleep(3)  # Jeda antar role


async def simulate_single_role(role: str):
    """Simulasi satu role"""
    simulator = ConversationSimulator(role, "Budi")
    
    try:
        await simulator.run_all_scenarios()
    finally:
        await simulator.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Conversation Simulator for MYLOVE V3")
    parser.add_argument("--role", "-r", type=str, help="Role to simulate (ipar, teman_kantor, janda, dll)")
    parser.add_argument("--all", "-a", action="store_true", help="Simulate all roles")
    
    args = parser.parse_args()
    
    if args.all:
        asyncio.run(simulate_all_roles())
    elif args.role:
        asyncio.run(simulate_single_role(args.role))
    else:
        # Default: simulate ipar
        asyncio.run(simulate_single_role("ipar"))
