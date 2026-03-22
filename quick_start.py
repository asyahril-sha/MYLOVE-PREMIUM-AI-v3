#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI V3 - QUICK START
=============================================================================
Setup cepat untuk pemula: install dependencies, setup .env, dan start bot
=============================================================================
"""

import os
import sys
import subprocess
from pathlib import Path

print("""
╔══════════════════════════════════════════════════════════════════╗
║     🚀 MYLOVE PREMIUM AI V3 - QUICK START                       ║
║                                                                  ║
║     This script will:                                           ║
║     1. Install dependencies                                     ║
║     2. Setup .env file                                          ║
║     3. Run database migration                                   ║
║     4. Start the bot                                            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")


def install_dependencies():
    """Install dependencies from requirements.txt"""
    print("\n📦 Installing dependencies...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("✅ Dependencies installed")
        return True
    else:
        print("❌ Failed to install dependencies")
        print(result.stderr)
        return False


def setup_env():
    """Setup .env file"""
    print("\n🔧 Setting up .env file...")
    
    if Path(".env").exists():
        print("⚠️ .env already exists. Do you want to overwrite?")
        response = input("Overwrite? (y/n) [n]: ").strip().lower()
        if response != 'y':
            print("Skipping .env setup")
            return True
    
    print("\nPlease enter your credentials:")
    telegram_token = input("Telegram Bot Token (from @BotFather): ").strip()
    deepseek_key = input("DeepSeek API Key: ").strip()
    admin_id = input("Admin Telegram ID: ").strip()
    
    with open(".env", "w") as f:
        f.write(f"""# MYLOVE PREMIUM AI - Environment Variables
TELEGRAM_TOKEN={telegram_token}
DEEPSEEK_API_KEY={deepseek_key}
ADMIN_ID={admin_id}

# Database
DB_PATH=data/mylove.db

# AI Configuration
AI_TEMPERATURE=0.9
AI_MAX_TOKENS=2000

# Feature Toggles
SEXUAL_CONTENT_ENABLED=true
MEMORY_ENABLED=true
EMOTIONAL_FLOW_ENABLED=true
SPATIAL_AWARENESS_ENABLED=true
ROLE_BEHAVIOR_ENABLED=true
""")
    
    print("✅ .env file created")
    return True


def run_migration():
    """Run database migration"""
    print("\n🗄️ Running database migration...")
    try:
        from database.migrate import migrate
        migrate()
        print("✅ Migration completed")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False


def start_bot():
    """Start the bot"""
    print("\n🚀 Starting bot...")
    print("Press Ctrl+C to stop\n")
    
    try:
        from run_bot_simple import main
        main()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    print("\n" + "=" * 60)
    print("QUICK START SETUP")
    print("=" * 60)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed. Please install dependencies manually:")
        print("   pip install -r requirements.txt")
        return
    
    # Step 2: Setup .env
    if not setup_env():
        print("\n❌ Setup failed. Please create .env manually")
        return
    
    # Step 3: Run migration
    if not run_migration():
        print("\n⚠️ Migration failed, but continuing...")
    
    # Step 4: Start bot
    start_bot()


if __name__ == "__main__":
    main()
