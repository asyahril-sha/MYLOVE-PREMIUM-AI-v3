#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - RUN SIMULATION ONLY
=============================================================================
Jalankan simulasi percakapan untuk role tertentu
=============================================================================
"""

import sys
import asyncio
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def main():
    parser = argparse.ArgumentParser(description="MYLOVE V3 Conversation Simulator")
    parser.add_argument("--role", "-r", type=str, default="ipar",
                        help="Role to simulate (ipar, teman_kantor, janda, pelakor, istri_orang, pdkt, sepupu, teman_sma, mantan)")
    parser.add_argument("--all", "-a", action="store_true",
                        help="Simulate all roles")
    
    args = parser.parse_args()
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║     🎭 MYLOVE PREMIUM AI V3 - CONVERSATION SIMULATOR            ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    if args.all:
        from tests.simulate_conversation import simulate_all_roles
        asyncio.run(simulate_all_roles())
    else:
        from tests.simulate_conversation import simulate_single_role
        print(f"Simulating role: {args.role}")
        print("=" * 60)
        asyncio.run(simulate_single_role(args.role))
    
    print("\n✅ Simulation completed!")


if __name__ == "__main__":
    main()
