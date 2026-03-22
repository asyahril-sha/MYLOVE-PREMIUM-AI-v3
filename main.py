#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - MAIN ENTRY POINT
=============================================================================
"""

import os
import sys
import asyncio
import logging
import signal
from datetime import datetime
from pathlib import Path

from aiohttp import web
from telegram import Update
from telegram.ext import Application, ContextTypes
from telegram.request import HTTPXRequest

# ===== AUTO MIGRATION (FIXED) =====
def run_migration():
    """Run database migration safely"""
    try:
        if os.path.exists("database/migrate.py"):
            print("🔄 Menjalankan auto migration...")
            # Import menggunakan importlib untuk menghindari circular import
            import importlib.util
            spec = importlib.util.spec_from_file_location("migrate_module", "database/migrate.py")
            migrate_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(migrate_module)
            migrate_module.migrate()
            return True
    except Exception as e:
        print(f"⚠️ Auto migration warning: {e}")
        return False

# Run migration before anything else
run_migration()

# Tambahkan path ke root project
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from utils.logger import setup_logging

# Setup logging
logger = setup_logging("MYLOVE-PREMIUM-AI")


class MyLovePremiumBot:
    """
    Main bot class untuk MYLOVE PREMIUM AI
    """
    
    def __init__(self):
        self.start_time = datetime.now()
        self.application = None
        self.is_ready = False
        self._shutdown_flag = False
        
        logger.info("=" * 70)
        logger.info("💕 MYLOVE PREMIUM AI - Initializing...")
        logger.info("=" * 70)
        
    async def init_components(self):
        """Initialize all components"""
        logger.info("🚀 Starting MYLOVE PREMIUM AI...")

        # Database
        try:
            from database.connection import init_db
            await init_db()
            logger.info("✅ Database initialized")
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise

        # Bot application
        try:
            from bot.application import create_application
            self.application = create_application()
            
            await self.application.initialize()
            logger.info("✅ Bot application created")
        except Exception as e:
            logger.error(f"❌ Bot application creation failed: {e}")
            raise

        # Error handler
        self.application.add_error_handler(self.error_handler)
        
        logger.info("🚀 MYLOVE PREMIUM AI is ready!")
        return self.application

    async def error_handler(self, update, context: ContextTypes.DEFAULT_TYPE):
        """Global error handler"""
        logger.error(f"❌ Error: {context.error}", exc_info=True)
        try:
            if update and update.effective_message:
                await update.effective_message.reply_text(
                    "❌ Terjadi error internal. Silakan coba lagi."
                )
        except:
            pass

    async def setup_webhook(self):
        """Setup webhook untuk Telegram"""
        try:
            railway_url = os.getenv('RAILWAY_PUBLIC_DOMAIN') or os.getenv('RAILWAY_STATIC_URL')
            if not railway_url:
                logger.error("❌ RAILWAY_PUBLIC_DOMAIN not set")
                return False
            
            webhook_url = f"https://{railway_url}/webhook"
            logger.info(f"🔗 Setting webhook to: {webhook_url}")

            await self.application.bot.delete_webhook(drop_pending_updates=True)
            logger.info("✅ Old webhook deleted")

            result = await self.application.bot.set_webhook(
                url=webhook_url,
                allowed_updates=['message', 'callback_query'],
                drop_pending_updates=True,
                max_connections=40
            )
            logger.info(f"✅ Webhook set result: {result}")

            webhook_info = await self.application.bot.get_webhook_info()
            if webhook_info.url == webhook_url:
                logger.info(f"✅ Webhook verified: {webhook_info.url}")
                return True
            else:
                logger.error(f"Webhook verification failed: {webhook_info.url}")
                return False

        except Exception as e:
            logger.error(f"❌ Webhook setup failed: {e}")
            return False

    async def webhook_handler(self, request):
        """AIOHTTP webhook handler"""
        if not self.application:
            return web.Response(status=503, text='Bot not ready')

        try:
            update_data = await request.json()
            if not update_data:
                return web.Response(status=400, text='No data')

            update = Update.de_json(update_data, self.application.bot)
            asyncio.create_task(self.application.process_update(update))
            
            logger.debug(f"✅ Processed update: {update.update_id}")
            return web.Response(text='OK')

        except Exception as e:
            logger.error(f"❌ Webhook error: {e}")
            return web.Response(status=500, text=str(e))

    async def health_handler(self, request):
        """Health check endpoint"""
        return web.json_response({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "bot": "MYLOVE PREMIUM AI",
            "version": "2.0.0",
            "bot_ready": self.application is not None,
            "uptime": str(datetime.now() - self.start_time)
        })

    async def root_handler(self, request):
        """Root endpoint"""
        return web.json_response({
            "name": "MYLOVE PREMIUM AI",
            "version": "2.0.0",
            "status": "running",
            "admin_id": str(settings.admin_id),
            "features": [
                "9 Role Eksklusif",
                "PDKT Natural 99%",
                "Leveling Time-Based",
                "Memory Permanen",
                "Threesome Mode",
                "Public Areas",
                "Aftercare System"
            ],
            "uptime": str(datetime.now() - self.start_time)
        })

    async def start(self):
        """Start bot and aiohttp server"""
        try:
            self.print_banner()
            await self.init_components()

            webhook_success = await self.setup_webhook()
            if webhook_success:
                logger.info("✅ Webhook mode activated!")
            else:
                logger.warning("⚠️ Webhook failed - check configuration")

            port = int(os.getenv('PORT', 8080))
            
            app = web.Application()
            app.router.add_post('/webhook', self.webhook_handler)
            app.router.add_get('/health', self.health_handler)
            app.router.add_get('/', self.root_handler)

            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, '0.0.0.0', port)
            await site.start()

            logger.info(f"✅ AIOHTTP server running on port {port}")
            logger.info(f"   • Healthcheck: /health")
            logger.info(f"   • Webhook: /webhook")
            logger.info("✅ MYLOVE PREMIUM AI is running. Press Ctrl+C to stop.")
            
            self.is_ready = True

            while not self._shutdown_flag:
                await asyncio.sleep(1)

        except asyncio.CancelledError:
            logger.info("👋 Bot stopped by user")
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}")
            import traceback
            traceback.print_exc()
            raise
        finally:
            await self.shutdown()

    async def shutdown(self):
        """Graceful shutdown"""
        logger.info("🛑 Shutting down...")
        self._shutdown_flag = True
        
        if self.application:
            try:
                await self.application.stop()
                await self.application.shutdown()
                logger.info("✅ Application stopped")
            except Exception as e:
                logger.error(f"Error stopping application: {e}")

    def print_banner(self):
        """Print startup banner"""
        print("=" * 70)
        print("    💕 MYLOVE PREMIUM AI")
        print("    Premium AI Assistant with Human+ Capabilities")
        print("    Version 2.0.0")
        print("=" * 70)
        
        # Database info
        try:
            db_info = f"SQLite @ {settings.database.path}"
        except:
            db_info = "SQLite"
        print(f"📊 Database: {db_info}")
        
        # AI Model
        try:
            ai_model = getattr(settings.ai, 'model', 'deepseek-chat')
        except:
            ai_model = "deepseek-chat"
        print(f"🤖 AI Model: {ai_model}")
        
        # Admin ID
        print(f"👑 Admin ID: {settings.admin_id}")
        
        # Features
        print(f"🔞 Sexual Content: {'ENABLED' if settings.features.sexual_enabled else 'DISABLED'}")
        print(f"💕 PDKT Natural: ENABLED")
        print(f"🎭 Threesome Mode: ENABLED")
        print(f"🧠 Memory System: HIPPOCAMPUS")
        print(f"📊 Leveling: TIME-BASED (60min → Level 7)")
        
        print("=" * 70)


def signal_handler():
    """Handle shutdown signals"""
    logger.info("Received signal, shutting down...")


async def main():
    """Main entry point"""
    bot = MyLovePremiumBot()
    
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)
    
    try:
        await bot.start()
    except asyncio.CancelledError:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        logger.info("👋 Goodbye from MYLOVE PREMIUM AI!")


if __name__ == "__main__":
    asyncio.run(main())
