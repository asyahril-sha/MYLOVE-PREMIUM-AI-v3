#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - WEBHOOK SETUP SCRIPT
=============================================================================
Script untuk setup webhook manual
Berguna untuk debugging webhook issues
=============================================================================
"""

import asyncio
import os
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from telegram import Bot
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


async def check_webhook():
    """Check current webhook status"""
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logger.error("❌ TELEGRAM_TOKEN not found in .env")
        return None
        
    bot = Bot(token=token)
    
    # Get webhook info
    info = await bot.get_webhook_info()
    
    logger.info("=" * 50)
    logger.info("📡 WEBHOOK STATUS")
    logger.info("=" * 50)
    logger.info(f"URL: {info.url}")
    logger.info(f"Pending updates: {info.pending_update_count}")
    logger.info(f"Last error date: {info.last_error_date}")
    logger.info(f"Last error message: {info.last_error_message}")
    logger.info(f"Max connections: {info.max_connections}")
    logger.info(f"Allowed updates: {info.allowed_updates}")
    logger.info("=" * 50)
    
    return info


async def set_webhook():
    """Set webhook manually"""
    token = os.getenv("TELEGRAM_TOKEN")
    railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    custom_url = os.getenv("WEBHOOK_URL")
    
    if not token:
        logger.error("❌ TELEGRAM_TOKEN not found")
        return False
        
    # Determine webhook URL
    if custom_url:
        webhook_url = custom_url.rstrip('/') + '/webhook'
    elif railway_domain:
        webhook_url = f"https://{railway_domain}/webhook"
    else:
        logger.error("❌ No webhook URL found. Set WEBHOOK_URL or RAILWAY_PUBLIC_DOMAIN in .env")
        return False
    
    bot = Bot(token=token)
    
    logger.info(f"🔗 Setting webhook to: {webhook_url}")
    
    try:
        # Set webhook
        await bot.set_webhook(
            url=webhook_url,
            allowed_updates=['message', 'callback_query', 'inline_query'],
            drop_pending_updates=True,
            max_connections=40,
            timeout=30
        )
        logger.info("✅ Webhook set successfully")
        
        # Verify
        info = await bot.get_webhook_info()
        if info.url == webhook_url:
            logger.info(f"✅ Webhook verified: {info.url}")
            logger.info(f"   Pending updates: {info.pending_update_count}")
            return True
        else:
            logger.error(f"❌ Webhook verification failed: {info.url}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Webhook setup failed: {e}")
        return False


async def delete_webhook():
    """Delete webhook (fallback to polling)"""
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logger.error("❌ TELEGRAM_TOKEN not found")
        return False
        
    bot = Bot(token=token)
    
    logger.info("🗑️ Deleting webhook...")
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("✅ Webhook deleted successfully")
        
        # Verify
        info = await bot.get_webhook_info()
        logger.info(f"   Webhook URL now: {info.url}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Webhook deletion failed: {e}")
        return False


async def test_webhook():
    """Test webhook by sending a test request"""
    token = os.getenv("TELEGRAM_TOKEN")
    railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    custom_url = os.getenv("WEBHOOK_URL")
    
    if not token:
        logger.error("❌ TELEGRAM_TOKEN not found")
        return False
        
    if custom_url:
        webhook_url = custom_url.rstrip('/') + '/webhook/test'
    elif railway_domain:
        webhook_url = f"https://{railway_domain}/webhook/test"
    else:
        logger.error("❌ No webhook URL found")
        return False
    
    import aiohttp
    
    logger.info(f"🔍 Testing webhook at: {webhook_url}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(webhook_url, timeout=10) as response:
                if response.status == 200:
                    text = await response.text()
                    logger.info(f"✅ Webhook test successful: {text[:200]}")
                    return True
                else:
                    logger.error(f"❌ Webhook test failed: HTTP {response.status}")
                    return False
    except asyncio.TimeoutError:
        logger.error("❌ Webhook test timeout - server not responding")
        return False
    except Exception as e:
        logger.error(f"❌ Webhook test error: {e}")
        return False


async def get_bot_info():
    """Get bot information"""
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logger.error("❌ TELEGRAM_TOKEN not found")
        return None
        
    bot = Bot(token=token)
    
    try:
        me = await bot.get_me()
        logger.info("=" * 50)
        logger.info("🤖 BOT INFORMATION")
        logger.info("=" * 50)
        logger.info(f"Name: {me.first_name}")
        logger.info(f"Username: @{me.username}")
        logger.info(f"ID: {me.id}")
        logger.info(f"Can join groups: {me.can_join_groups}")
        logger.info(f"Can read messages: {me.can_read_all_group_messages}")
        logger.info("=" * 50)
        return me
    except Exception as e:
        logger.error(f"❌ Failed to get bot info: {e}")
        return None


async def get_updates():
    """Get pending updates (for debugging)"""
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logger.error("❌ TELEGRAM_TOKEN not found")
        return None
        
    bot = Bot(token=token)
    
    try:
        updates = await bot.get_updates(limit=10, timeout=5)
        logger.info(f"📨 Found {len(updates)} pending updates")
        
        for i, update in enumerate(updates, 1):
            logger.info(f"   {i}. Update ID: {update.update_id}")
            if update.message:
                logger.info(f"      Message: {update.message.text}")
            elif update.callback_query:
                logger.info(f"      Callback: {update.callback_query.data}")
                
        return updates
    except Exception as e:
        logger.error(f"❌ Failed to get updates: {e}")
        return None


async def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MYLOVE PREMIUM AI - Webhook Manager")
    parser.add_argument("action", choices=["check", "set", "delete", "test", "info", "updates"], 
                       help="Action to perform")
    parser.add_argument("--url", help="Custom webhook URL (optional)")
    
    args = parser.parse_args()
    
    # Override webhook URL if provided
    if args.url:
        os.environ["WEBHOOK_URL"] = args.url
    
    if args.action == "check":
        await check_webhook()
    elif args.action == "set":
        await set_webhook()
        await check_webhook()
    elif args.action == "delete":
        await delete_webhook()
        await check_webhook()
    elif args.action == "test":
        await test_webhook()
    elif args.action == "info":
        await get_bot_info()
    elif args.action == "updates":
        await get_updates()


if __name__ == "__main__":
    asyncio.run(main())
