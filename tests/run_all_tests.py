# tests/run_all_tests.py
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - RUN ALL TESTS
=============================================================================
Script untuk menjalankan semua unit test dan simulasi.
Berguna untuk memastikan semua komponen V3 berfungsi dengan baik.
=============================================================================
"""

import asyncio
import sys
import os
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import setup_logging, logger


class TestRunner:
    """
    Runner untuk semua test V3
    """
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.results = {
            'unit_tests': [],
            'simulations': [],
            'integration': []
        }
        self.test_dir = Path(__file__).parent
    
    def _print_header(self, title: str):
        """Print header section"""
        logger.info("\n" + "=" * 70)
        logger.info(f"  {title}")
        logger.info("=" * 70)
    
    def _print_result(self, name: str, passed: bool, duration: float, details: str = ""):
        """Print hasil test"""
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{status} - {name} ({duration:.2f}s)")
        if details:
            logger.info(f"     {details}")
    
    # =========================================================================
    # UNIT TESTS
    # =========================================================================
    
    def run_unit_test(self, test_name: str, test_file: str) -> bool:
        """
        Jalankan unit test file
        """
        test_path = self.test_dir / test_file
        
        if not test_path.exists():
            logger.warning(f"Test file not found: {test_file}")
            return False
        
        start = time.time()
        
        try:
            # Jalankan unittest dengan subprocess
            result = subprocess.run(
                [sys.executable, str(test_path)],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            duration = time.time() - start
            passed = result.returncode == 0
            
            self.results['unit_tests'].append({
                'name': test_name,
                'passed': passed,
                'duration': duration,
                'output': result.stdout,
                'error': result.stderr
            })
            
            self._print_result(test_name, passed, duration)
            
            if not passed and result.stderr:
                logger.error(f"     Error: {result.stderr[:200]}")
            
            return passed
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start
            self.results['unit_tests'].append({
                'name': test_name,
                'passed': False,
                'duration': duration,
                'output': "",
                'error': "Timeout"
            })
            self._print_result(test_name, False, duration, "Timeout")
            return False
        
        except Exception as e:
            duration = time.time() - start
            self.results['unit_tests'].append({
                'name': test_name,
                'passed': False,
                'duration': duration,
                'output': "",
                'error': str(e)
            })
            self._print_result(test_name, False, duration, str(e))
            return False
    
    def run_all_unit_tests(self) -> bool:
        """
        Jalankan semua unit test
        """
        self._print_header("RUNNING UNIT TESTS")
        
        tests = [
            ("Emotional Flow", "test_emotional_flow.py"),
            ("Spatial Awareness", "test_spatial_awareness.py"),
            ("Role Behavior", "test_role_behavior.py")
        ]
        
        all_passed = True
        
        for name, file in tests:
            if not self.run_unit_test(name, file):
                all_passed = False
        
        return all_passed
    
    # =========================================================================
    # SIMULATIONS
    # =========================================================================
    
    async def run_simulation(self, role: str) -> bool:
        """
        Jalankan simulasi untuk role tertentu
        """
        start = time.time()
        
        try:
            from simulate_conversation import simulate_single_role
            
            logger.info(f"\n📋 Simulating role: {role}")
            await simulate_single_role(role)
            
            duration = time.time() - start
            self.results['simulations'].append({
                'role': role,
                'passed': True,
                'duration': duration,
                'error': None
            })
            self._print_result(f"Simulation - {role}", True, duration)
            return True
            
        except Exception as e:
            duration = time.time() - start
            self.results['simulations'].append({
                'role': role,
                'passed': False,
                'duration': duration,
                'error': str(e)
            })
            self._print_result(f"Simulation - {role}", False, duration, str(e))
            return False
    
    async def run_all_simulations(self) -> bool:
        """
        Jalankan semua simulasi
        """
        self._print_header("RUNNING SIMULATIONS")
        
        roles = ['ipar', 'teman_kantor', 'janda', 'pelakor', 
                 'istri_orang', 'pdkt', 'sepupu', 'teman_sma', 'mantan']
        
        all_passed = True
        
        for role in roles:
            if not await self.run_simulation(role):
                all_passed = False
            await asyncio.sleep(2)  # Jeda antar simulasi
        
        return all_passed
    
    # =========================================================================
    # INTEGRATION TESTS
    # =========================================================================
    
    def check_config(self) -> bool:
        """
        Cek konfigurasi
        """
        start = time.time()
        
        try:
            from config import settings
            
            # Cek API key
            if not settings.deepseek_api_key or settings.deepseek_api_key == "your_deepseek_api_key_here":
                raise ValueError("DeepSeek API key not configured")
            
            if not settings.telegram_token or settings.telegram_token == "your_telegram_bot_token_here":
                raise ValueError("Telegram token not configured")
            
            if settings.admin_id == 0:
                raise ValueError("Admin ID not configured")
            
            duration = time.time() - start
            self.results['integration'].append({
                'name': 'Config',
                'passed': True,
                'duration': duration,
                'details': f"API Key OK, Telegram OK, Admin ID: {settings.admin_id}"
            })
            self._print_result("Config Check", True, duration, "Configuration valid")
            return True
            
        except Exception as e:
            duration = time.time() - start
            self.results['integration'].append({
                'name': 'Config',
                'passed': False,
                'duration': duration,
                'details': str(e)
            })
            self._print_result("Config Check", False, duration, str(e))
            return False
    
    def check_imports(self) -> bool:
        """
        Cek semua import
        """
        start = time.time()
        failed_imports = []
        
        modules_to_check = [
            # Core
            'core.ai_engine',
            'core.prompt_builder',
            'core.context_analyzer',
            'core.intent_analyzer',
            'core.name_detector',
            
            # Dynamics
            'dynamics.role_behavior',
            'dynamics.ipar_behavior',
            'dynamics.teman_kantor_behavior',
            'dynamics.janda_behavior',
            'dynamics.pelakor_behavior',
            'dynamics.istri_orang_behavior',
            'dynamics.pdkt_behavior',
            'dynamics.sepupu_behavior',
            'dynamics.teman_sma_behavior',
            'dynamics.mantan_behavior',
            'dynamics.emotional_flow',
            'dynamics.spatial_awareness',
            'dynamics.gesture_db',
            
            # Memory
            'memory.emotional_memory',
            'memory.scene_memory',
            'memory.memory_bridge',
            'memory.working_memory',
            'memory.episodic',
            'memory.semantic',
            
            # Config
            'config.role_behavior_config',
            'config.gesture_config'
        ]
        
        for module_name in modules_to_check:
            try:
                __import__(module_name)
            except ImportError as e:
                failed_imports.append(f"{module_name}: {e}")
        
        duration = time.time() - start
        passed = len(failed_imports) == 0
        
        self.results['integration'].append({
            'name': 'Imports',
            'passed': passed,
            'duration': duration,
            'details': f"{len(modules_to_check)} modules checked, {len(failed_imports)} failed" if not passed else "All imports successful"
        })
        
        self._print_result("Import Check", passed, duration, 
                          f"{len(failed_imports)} failed" if not passed else "All OK")
        
        if failed_imports:
            for imp in failed_imports[:5]:
                logger.error(f"     {imp}")
        
        return passed
    
    def check_directory_structure(self) -> bool:
        """
        Cek struktur direktori
        """
        start = time.time()
        missing_dirs = []
        
        required_dirs = [
            'data',
            'data/logs',
            'data/backups',
            'data/sessions',
            'data/vector_db',
            'data/memory'
        ]
        
        base_dir = Path(__file__).parent.parent
        
        for dir_path in required_dirs:
            full_path = base_dir / dir_path
            if not full_path.exists():
                missing_dirs.append(dir_path)
            else:
                # Coba buat jika belum ada
                full_path.mkdir(parents=True, exist_ok=True)
        
        duration = time.time() - start
        passed = len(missing_dirs) == 0
        
        self.results['integration'].append({
            'name': 'Directory Structure',
            'passed': passed,
            'duration': duration,
            'details': f"Missing: {missing_dirs}" if missing_dirs else "All directories exist"
        })
        
        self._print_result("Directory Check", passed, duration,
                          f"{len(missing_dirs)} missing" if not passed else "All OK")
        
        return passed
    
    def run_all_integration_tests(self) -> bool:
        """
        Jalankan semua integration test
        """
        self._print_header("RUNNING INTEGRATION TESTS")
        
        config_ok = self.check_config()
        imports_ok = self.check_imports()
        dirs_ok = self.check_directory_structure()
        
        return config_ok and imports_ok and dirs_ok
    
    # =========================================================================
    # REPORT
    # =========================================================================
    
    def print_report(self):
        """
        Print laporan hasil test
        """
        self._print_header("TEST REPORT")
        
        # Summary
        unit_passed = sum(1 for t in self.results['unit_tests'] if t['passed'])
        unit_total = len(self.results['unit_tests'])
        
        sim_passed = sum(1 for t in self.results['simulations'] if t['passed'])
        sim_total = len(self.results['simulations'])
        
        int_passed = sum(1 for t in self.results['integration'] if t['passed'])
        int_total = len(self.results['integration'])
        
        logger.info("\n📊 SUMMARY:")
        logger.info(f"  Unit Tests:     {unit_passed}/{unit_total} passed")
        logger.info(f"  Simulations:    {sim_passed}/{sim_total} passed")
        logger.info(f"  Integration:    {int_passed}/{int_total} passed")
        
        total_passed = unit_passed + sim_passed + int_passed
        total_tests = unit_total + sim_total + int_total
        logger.info(f"\n  TOTAL: {total_passed}/{total_tests} passed ({total_passed/total_tests*100:.1f}%)")
        
        # Duration
        total_duration = sum(t.get('duration', 0) for t in self.results['unit_tests']) + \
                        sum(t.get('duration', 0) for t in self.results['simulations']) + \
                        sum(t.get('duration', 0) for t in self.results['integration'])
        
        logger.info(f"\n  Total duration: {total_duration:.2f} seconds")
        
        # Failed details
        failed_units = [t for t in self.results['unit_tests'] if not t['passed']]
        failed_sims = [t for t in self.results['simulations'] if not t['passed']]
        failed_ints = [t for t in self.results['integration'] if not t['passed']]
        
        if failed_units:
            logger.info("\n❌ FAILED UNIT TESTS:")
            for t in failed_units:
                logger.info(f"  - {t['name']}: {t.get('error', 'Unknown error')[:100]}")
        
        if failed_sims:
            logger.info("\n❌ FAILED SIMULATIONS:")
            for t in failed_sims:
                logger.info(f"  - {t['role']}: {t.get('error', 'Unknown error')[:100]}")
        
        if failed_ints:
            logger.info("\n❌ FAILED INTEGRATION TESTS:")
            for t in failed_ints:
                logger.info(f"  - {t['name']}: {t.get('details', 'Unknown error')[:100]}")
        
        # Overall status
        overall_passed = unit_passed == unit_total and sim_passed == sim_total and int_passed == int_total
        
        logger.info("\n" + "=" * 70)
        if overall_passed:
            logger.info("🎉 ALL TESTS PASSED! MYLOVE PREMIUM AI V3 IS READY FOR DEPLOYMENT! 🎉")
        else:
            logger.info("⚠️ SOME TESTS FAILED. PLEASE CHECK THE ERRORS ABOVE. ⚠️")
        logger.info("=" * 70)
    
    # =========================================================================
    # MAIN
    # =========================================================================
    
    async def run_all(self):
        """
        Jalankan semua test
        """
        self.start_time = time.time()
        
        logger.info("=" * 70)
        logger.info("🚀 MYLOVE PREMIUM AI V3 - TEST SUITE")
        logger.info(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 70)
        
        # 1. Unit Tests
        unit_ok = self.run_all_unit_tests()
        
        # 2. Integration Tests
        integration_ok = self.run_all_integration_tests()
        
        # 3. Simulations (only if unit tests pass and API key is configured)
        sim_ok = True
        if unit_ok and integration_ok:
            sim_ok = await self.run_all_simulations()
        else:
            logger.warning("\n⚠️ Skipping simulations due to failed unit/integration tests")
        
        self.end_time = time.time()
        
        # Report
        self.print_report()
        
        return unit_ok and integration_ok and sim_ok


async def main():
    """
    Main function
    """
    # Setup logging
    setup_logging("TEST_RUNNER")
    
    runner = TestRunner()
    success = await runner.run_all()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
