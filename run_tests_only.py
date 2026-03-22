#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - RUN TESTS ONLY
=============================================================================
Jalankan semua test tanpa menjalankan bot
=============================================================================
"""

import sys
import asyncio
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)


def run_all():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║     🧪 MYLOVE PREMIUM AI V3 - TEST SUITE                        ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    from tests.run_all_tests import TestRunner
    runner = TestRunner()
    
    # Run unit tests
    logger.info("Running unit tests...")
    unit_ok = runner.run_all_unit_tests()
    
    # Run integration tests
    logger.info("\nRunning integration tests...")
    int_ok = runner.run_all_integration_tests()
    
    # Run simulations (optional)
    sim_input = input("\nRun simulations? (y/n) [n]: ").strip().lower()
    if sim_input == 'y':
        asyncio.run(runner.run_all_simulations())
    
    # Summary
    print("\n" + "=" * 60)
    if unit_ok and int_ok:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️ SOME TESTS FAILED. Check logs above.")
    print("=" * 60)


if __name__ == "__main__":
    run_all()
