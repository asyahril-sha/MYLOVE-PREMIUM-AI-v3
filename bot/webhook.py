#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - WEBHOOK MANAGER
=============================================================================
- Setup webhook dengan retry mechanism
- Fallback ke polling jika webhook gagal
- Health check endpoint
=============================================================================
"""

import os
import asyncio
import logging
from typing import Optional
from telegram import Update
from telegram.ext import Application

from config import settings

logger = logging.getLogger(__name__)


def setup_webhook_sync(app: Application) -> bool:
    """
    Setup webhook synchronously (untuk main.py)
    
    Args:
        app: Application instance
        
    Returns:
        True if webhook setup successful
    """
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(_setup_webhook_async(app))
    except Exception as e:
        logger.error(f"Webhook setup failed: {e}")
        return False


async def _setup_webhook_async(app: Application) -> bool:
    """Setup webhook asynchronously"""
    # Dapatkan URL webhook
    railway_url = os.getenv('RAILWAY_PUBLIC_DOMAIN') or os.getenv('RAILWAY_STATIC_URL')
    
    if railway_url:
        webhook_url = f"https://{railway_url}/webhook"
    elif settings.webhook.url:
        webhook_url = settings.webhook.url.rstrip('/') + '/webhook'
    else:
        logger.warning("No webhook URL configured, using polling mode")
        return False
    
    logger.info(f"🔗 Setting webhook to: {webhook_url}")
    
    try:
        # Delete existing webhook
        await app.bot.delete_webhook(drop_pending_updates=True)
        
        # Set new webhook
        await app.bot.set_webhook(
            url=webhook_url,
            allowed_updates=['message', 'callback_query', 'inline_query'],
            drop_pending_updates=True,
            max_connections=40,
            timeout=30
        )
        
        # Verify
        info = await app.bot.get_webhook_info()
        if info.url == webhook_url:
            logger.info(f"✅ Webhook set successfully: {info.url}")
            return True
        else:
            logger.error(f"Webhook verification failed: {info.url}")
            return False
            
    except Exception as e:
        logger.error(f"Webhook setup failed: {e}")
        return False


async def check_webhook_status(app: Application) -> dict:
    """Check current webhook status"""
    try:
        info = await app.bot.get_webhook_info()
        return {
            "url": info.url,
            "pending_updates": info.pending_update_count,
            "last_error": info.last_error_message,
            "last_error_date": info.last_error_date,
            "max_connections": info.max_connections,
            "allowed_updates": info.allowed_updates
        }
    except Exception as e:
        return {"error": str(e)}


async def reset_webhook(app: Application, url: Optional[str] = None):
    """Reset webhook (delete then set new)"""
    try:
        await app.bot.delete_webhook(drop_pending_updates=True)
        logger.info("✅ Existing webhook deleted")
        
        if url:
            await app.bot.set_webhook(url=url)
            logger.info(f"✅ New webhook set: {url}")
    except Exception as e:
        logger.error(f"Error resetting webhook: {e}")


__all__ = ['setup_webhook_sync', 'check_webhook_status', 'reset_webhook']
