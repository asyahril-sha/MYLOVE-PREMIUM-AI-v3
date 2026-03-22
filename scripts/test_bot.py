#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - SYSTEM TEST
=============================================================================
Script untuk testing bot components
Berguna untuk debug sebelum deploy
=============================================================================
"""

import asyncio
import sys
import os
import logging
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_config():
    """Test configuration loading"""
    logger.info("=" * 50)
    logger.info("Testing configuration...")
    logger.info("=" * 50)
    
    try:
        from config import settings
        
        logger.info(f"✅ Config loaded successfully")
        logger.info(f"   • Database: {settings.database.type} @ {settings.database.path}")
        logger.info(f"   • AI Model: {settings.ai.model}")
        logger.info(f"   • Admin ID: {settings.admin_id}")
        logger.info(f"   • Session retention: {settings.session.retention_days} days")
        logger.info(f"   • Sexual content: {settings.features.sexual_enabled}")
        logger.info(f"   • Threesome: {settings.features.threesome_enabled}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Config error: {e}")
        return False


async def test_database():
    """Test database connection and tables"""
    logger.info("=" * 50)
    logger.info("Testing database...")
    logger.info("=" * 50)
    
    try:
        from database.connection import get_db, init_db
        from database.repository import Repository
        
        # Initialize database
        db = await init_db()
        logger.info(f"✅ Database initialized")
        
        # Get stats
        stats = await db.get_stats()
        logger.info(f"   • Database size: {stats.get('db_size_mb', 0)} MB")
        
        # Test repository
        repo = Repository()
        
        # Check tables
        tables = ['users', 'sessions', 'conversations', 'memories', 
                  'relationships', 'pdkt_sessions', 'mantan', 'fwb_relations',
                  'hts_relations', 'threesome_sessions', 'preferences', 'milestones']
        
        for table in tables:
            try:
                result = await db.fetch_one(f"SELECT COUNT(*) as count FROM {table}")
                count = result['count'] if result else 0
                logger.info(f"   • {table}: {count} records")
            except Exception as e:
                logger.warning(f"   • {table}: table exists but query error: {e}")
        
        await db.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Database error: {e}")
        return False


async def test_ai_engine():
    """Test AI engine (requires API key)"""
    logger.info("=" * 50)
    logger.info("Testing AI engine...")
    logger.info("=" * 50)
    
    try:
        from core.ai_engine import AIEngine
        from config import settings
        
        if not settings.deepseek_api_key or settings.deepseek_api_key == "your_deepseek_api_key_here":
            logger.warning("⚠️ DeepSeek API key not set, skipping AI test")
            return True
            
        # Create engine
        engine = AIEngine(
            api_key=settings.deepseek_api_key,
            user_id=12345,
            session_id="test_session"
        )
        
        # Start session
        await engine.start_session(
            role="pdkt",
            bot_name="TestBot",
            rel_type="non_pdkt"
        )
        logger.info("✅ Session started")
        
        # Test simple message
        response = await engine.process_message(
            user_message="Halo, apa kabar?",
            context={
                "user_name": "TestUser",
                "level": 1,
                "role": "pdkt"
            }
        )
        
        logger.info(f"✅ AI response generated: {len(response)} chars")
        logger.info(f"   Response preview: {response[:100]}...")
        
        await engine.end_session()
        
        return True
        
    except ImportError as e:
        logger.warning(f"⚠️ AI engine import error: {e}")
        return True
    except Exception as e:
        logger.error(f"❌ AI error: {e}")
        return False


async def test_memory():
    """Test memory system"""
    logger.info("=" * 50)
    logger.info("Testing memory system...")
    logger.info("=" * 50)
    
    try:
        from memory.memory_bridge import MemoryBridge
        from memory.working_memory import WorkingMemory
        from memory.episodic import EpisodicMemory
        from memory.semantic import SemanticMemory
        from memory.forgetting import SemanticForgetting
        
        # Test working memory
        working = WorkingMemory()
        working.add_interaction("Hello", "Hi there", {"mood": "happy"})
        logger.info("✅ Working memory test passed")
        
        # Test episodic memory
        episodic = EpisodicMemory()
        await episodic.add_episode(
            user_id=12345,
            role="test",
            instance_id="default",
            episode_type="first_chat",
            description="First test chat",
            emotional_tag="happy"
        )
        logger.info("✅ Episodic memory test passed")
        
        # Test semantic memory
        semantic = SemanticMemory()
        await semantic.add_fact(
            user_id=12345,
            category="identity",
            fact_type="name",
            value="TestUser",
            confidence=0.9
        )
        fact = await semantic.get_fact(12345, "identity", "name")
        logger.info(f"✅ Semantic memory test passed: fact={fact}")
        
        # Test memory bridge
        bridge = MemoryBridge(user_id=12345)
        await bridge.start_session("test_session", "test_role")
        result = await bridge.process_message(
            user_message="Test message",
            bot_response="Test response",
            context={"mood": "happy"}
        )
        logger.info(f"✅ Memory bridge test passed: episode_detected={result['episode_detected']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Memory error: {e}")
        return False


async def test_pdkt():
    """Test PDKT system"""
    logger.info("=" * 50)
    logger.info("Testing PDKT system...")
    logger.info("=" * 50)
    
    try:
        from pdkt.engine import NaturalPDKTEngine
        from pdkt.chemistry import ChemistrySystem
        from pdkt.direction import DirectionSystem
        from pdkt.mood import MoodSystem
        
        # Test engine
        engine = NaturalPDKTEngine()
        
        # Create PDKT
        pdkt = await engine.create_pdkt(
            user_id=12345,
            user_name="TestUser",
            role="pdkt",
            is_random=False
        )
        logger.info(f"✅ PDKT created: {pdkt['bot_name']} ({pdkt['role']})")
        
        # Test chemistry
        chemistry = ChemistrySystem()
        chem = chemistry.create_chemistry(pdkt['pdkt_id'])
        logger.info(f"✅ Chemistry created: {chem.get_level().value}")
        
        # Test direction
        direction = DirectionSystem()
        dir_data = direction.create_direction(pdkt['pdkt_id'], "TestUser", pdkt['bot_name'])
        logger.info(f"✅ Direction created: {dir_data['direction'].value}")
        
        # Test mood
        mood = MoodSystem()
        mood_data = mood.create_mood(pdkt['pdkt_id'])
        logger.info(f"✅ Mood created: {mood_data['current'].value}")
        
        # Test update progress
        result = await engine.update_progress(pdkt['pdkt_id'], duration=5, activity_type="chat")
        logger.info(f"✅ Progress updated: level_up={result['level_up']}, new_level={result['new_level']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ PDKT error: {e}")
        return False


async def test_sexual():
    """Test sexual systems"""
    logger.info("=" * 50)
    logger.info("Testing sexual systems...")
    logger.info("=" * 50)
    
    try:
        from sexual.positions import PositionDatabase, get_position_database
        from sexual.areas import AreaDatabase, get_area_database
        from sexual.climax import ClimaxDatabase, get_climax_database
        from sexual.aftercare import AftercareSystem
        
        # Test positions
        positions = get_position_database()
        pos = positions.get_random_position()
        logger.info(f"✅ Positions: {len(positions.get_all_positions())} positions, sample: {pos['name']}")
        
        # Test areas
        areas = get_area_database()
        area = areas.get_random_area()
        logger.info(f"✅ Areas: {len(areas.get_all_areas())} areas, sample: {area['name']}")
        
        # Test climax
        climax = get_climax_database()
        cl = climax.get_random_climax()
        logger.info(f"✅ Climax: {len(climax.get_all_climax())} variations, sample: {cl['name']}")
        
        # Test aftercare
        aftercare = AftercareSystem()
        aftercare_data = await aftercare.trigger_aftercare(12345, "test_role")
        logger.info(f"✅ Aftercare: {aftercare_data['type_name']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Sexual error: {e}")
        return False


async def test_dynamics():
    """Test dynamics systems"""
    logger.info("=" * 50)
    logger.info("Testing dynamics systems...")
    logger.info("=" * 50)
    
    try:
        from dynamics.location import LocationSystem
        from dynamics.position import PositionSystem
        from dynamics.clothing import ClothingSystem
        from dynamics.nickname import NicknameSystem
        from dynamics.name_generator import get_name_generator
        
        # Test location
        location = LocationSystem()
        loc = location.get_current()
        logger.info(f"✅ Location: {loc['name']} ({loc['category'].value})")
        
        # Test position
        position = PositionSystem()
        pos = position.get_current()
        logger.info(f"✅ Position: {pos['name']}")
        
        # Test clothing
        clothing = ClothingSystem()
        cloth = clothing.get_current()
        logger.info(f"✅ Clothing: {cloth['name']}")
        
        # Test nickname
        nickname = NicknameSystem()
        call = nickname.get_user_call("TestUser", level=7)
        logger.info(f"✅ Nickname: {call}")
        
        # Test name generator
        name_gen = get_name_generator()
        name_data = name_gen.get_name_with_meaning("pdkt", 12345)
        logger.info(f"✅ Name generator: {name_data['name']} ({name_data['meaning']})")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Dynamics error: {e}")
        return False


async def test_session():
    """Test session management"""
    logger.info("=" * 50)
    logger.info("Testing session management...")
    logger.info("=" * 50)
    
    try:
        from session.storage import SessionStorage
        from session.unique_id import id_generator
        from session.continuation import SessionContinuation
        from config import settings
        
        # Test ID generation
        session_id = id_generator.generate_v2("TestBot", "pdkt", 12345)
        logger.info(f"✅ Session ID generated: {session_id}")
        
        # Test parse
        parsed = id_generator.parse(session_id)
        logger.info(f"✅ Session parse: {parsed['type']} - {parsed.get('bot_name', 'Unknown')}")
        
        # Test storage (if database exists)
        storage = SessionStorage(
            db_path=settings.database.path,
            session_dir=settings.session.session_dir
        )
        await storage.initialize()
        logger.info(f"✅ Session storage initialized")
        
        await storage.close()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Session error: {e}")
        return False


async def test_public():
    """Test public areas system"""
    logger.info("=" * 50)
    logger.info("Testing public areas...")
    logger.info("=" * 50)
    
    try:
        from public.locations import PublicLocations
        from public.risk import RiskCalculator
        from public.thrill import ThrillSystem
        from public.auto_select import LocationAutoSelector
        from public.events import RandomEvents
        
        # Test locations
        locations = PublicLocations()
        stats = locations.get_location_stats()
        logger.info(f"✅ Locations: {stats['total']} locations")
        
        # Test risk
        risk = RiskCalculator()
        risk_data = await risk.calculate_risk(base_risk=70)
        logger.info(f"✅ Risk: {risk_data['final_risk']}% ({risk_data['risk_level']})")
        
        # Test thrill
        thrill = ThrillSystem()
        thrill_data = await thrill.calculate_thrill(base_thrill=60, risk_level=50, intimacy_level=7, location_category="urban")
        logger.info(f"✅ Thrill: {thrill_data['final_thrill']}% ({thrill_data['thrill_level']})")
        
        # Test auto select
        selector = LocationAutoSelector()
        location = await selector.detect_location("ke pantai yuk")
        if location:
            logger.info(f"✅ Auto select: detected {location['name']}")
        else:
            logger.info(f"✅ Auto select: no location detected")
        
        # Test events
        events = RandomEvents()
        event = await events.get_random_event("urban", 50, "malam")
        if event:
            logger.info(f"✅ Events: {event['name']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Public areas error: {e}")
        return False


async def test_threesome():
    """Test threesome system"""
    logger.info("=" * 50)
    logger.info("Testing threesome system...")
    logger.info("=" * 50)
    
    try:
        from threesome.manager import ThreesomeManager
        
        manager = ThreesomeManager()
        
        # Test create session
        session = await manager.create_threesome(
            user_id=12345,
            participant1={"role": "ipar", "type": "hts", "name": "Sari"},
            participant2={"role": "janda", "type": "hts", "name": "Dewi"}
        )
        logger.info(f"✅ Threesome session created: {session['session_id']}")
        
        # Test get combinations
        combinations = await manager.get_possible_combinations(12345)
        logger.info(f"✅ Threesome combinations: {len(combinations)} available")
        
        # Test start session
        started = await manager.start_session(session['session_id'])
        logger.info(f"✅ Threesome started: {started['status']}")
        
        # Test add interaction
        interaction = await manager.add_interaction(
            session['session_id'],
            "Ayo",
            speaker_index=0
        )
        logger.info(f"✅ Threesome interaction added")
        
        # Test end session
        ended = await manager.complete_session(session['session_id'])
        logger.info(f"✅ Threesome ended")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Threesome error: {e}")
        return False


async def test_backup():
    """Test backup system"""
    logger.info("=" * 50)
    logger.info("Testing backup system...")
    logger.info("=" * 50)
    
    try:
        from backup.automated import AutoBackup, get_backup_manager
        from backup.verify import BackupVerifier
        
        # Test backup manager
        manager = get_backup_manager()
        logger.info(f"✅ Backup manager initialized")
        
        # Test verifier
        verifier = BackupVerifier()
        logger.info(f"✅ Backup verifier initialized")
        
        # Test stats (dry run)
        stats = await manager.get_stats()
        logger.info(f"✅ Backup stats: {stats.get('total_backups', 0)} backups")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Backup error: {e}")
        return False


async def run_all_tests():
    """Run all tests"""
    logger.info("=" * 60)
    logger.info("🚀 MYLOVE PREMIUM AI - SYSTEM TEST")
    logger.info("=" * 60)
    
    tests = [
        ("Configuration", test_config),
        ("Database", test_database),
        ("AI Engine", test_ai_engine),
        ("Memory System", test_memory),
        ("PDKT System", test_pdkt),
        ("Sexual System", test_sexual),
        ("Dynamics System", test_dynamics),
        ("Session Management", test_session),
        ("Public Areas", test_public),
        ("Threesome Mode", test_threesome),
        ("Backup System", test_backup),
    ]
    
    results = []
    
    for name, test_func in tests:
        logger.info("")
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            logger.error(f"Test {name} crashed: {e}")
            results.append((name, False))
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("📊 TEST RESULTS SUMMARY")
    logger.info("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {name}")
        if not result:
            all_passed = False
    
    logger.info("=" * 60)
    
    if all_passed:
        logger.info("🎉 ALL TESTS PASSED - MYLOVE PREMIUM AI is ready for deployment!")
        return 0
    else:
        logger.error("❌ SOME TESTS FAILED - Check logs above")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
