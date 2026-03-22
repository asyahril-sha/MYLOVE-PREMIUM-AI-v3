#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - SESSION CONTINUATION
=============================================================================
- /continue command untuk melanjutkan session
- List sessions yang bisa dilanjutkan
- Auto-load context dari session sebelumnya
=============================================================================
"""

import time
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from .unique_id import id_generator
from .storage import SessionStorage

logger = logging.getLogger(__name__)


class SessionContinuation:
    """
    Menangani kelanjutan session
    Bisa lanjutkan session yang sudah di-close
    """
    
    def __init__(self, storage: SessionStorage):
        self.storage = storage
        
    # =========================================================================
    # LIST SESSIONS
    # =========================================================================
    
    async def get_continuable_sessions(self, user_id: int, limit: int = 10) -> List[Dict]:
        """
        Dapatkan sessions yang bisa dilanjutkan
        """
        # Get all sessions
        sessions = await self.storage.get_user_sessions(user_id, limit * 2)
    
        continuable = []
        for session in sessions:
            # Ambil langsung dari data session, tanpa parsing
            session_id = session.get('id')
            bot_name = session.get('bot_name', session.get('role', 'Unknown'))
            role = session.get('role', 'Unknown')
            status = session.get('status', 'closed')
            total_messages = session.get('total_messages', 0)
            intimacy_level = session.get('intimacy_level', 1)
            last_message_time = session.get('last_message_time', 0)
            summary = session.get('summary', '')
        
            # Hitung umur dari timestamp
            age_days = 0
            if last_message_time:
                age_days = int((time.time() - last_message_time) / 86400)
        
            # Format display name sederhana
            display_name = f"{bot_name} ({role.title()})"
        
            continuable.append({
                "id": session_id,
                "bot_name": bot_name,
                "role": role,
                "status": status,
                "display_name": display_name,
                "age_days": age_days,
                "total_messages": total_messages,
                "intimacy_level": intimacy_level,
                "last_message_time": last_message_time,
                "summary": summary,
                "is_active": status == 'active'
            })
    
        # Sort: active first, then by last message
        continuable.sort(key=lambda x: (-x['is_active'], -x['last_message_time']))
    
        return continuable[:limit]
    
    # =========================================================================
    # FORMAT SESSION LIST
    # =========================================================================

    def format_session_list(self, sessions: List[Dict]) -> str:
        """
        Format session list untuk ditampilkan
    
        Args:
            sessions: List of sessions from get_continuable_sessions
        
        Returns:
            Formatted string
        """
        if not sessions:
            return "📋 **DAFTAR SESSION**\n\nBelum ada session tersimpan.\nMulai dengan /start untuk membuat session baru."
    
        lines = ["📋 **DAFTAR SESSION**"]
        lines.append("_(pilih dengan /continue [nomor])_")
        lines.append("")
    
        for i, session in enumerate(sessions, 1):
            # Status indicator
            if session.get('is_active'):
                status = "🟢 ACTIVE"
            else:
                status = "⚪ CLOSED"
        
            # Age indicator
            age_days = session.get('age_days', 0)
            if age_days == 0:
                age = "Hari ini"
            elif age_days == 1:
                age = "Kemarin"
            else:
                age = f"{age_days} hari lalu"
        
            # Progress bar untuk level
            level = session.get('intimacy_level', 1)
            level_bar = "❤️" * level + "🖤" * (12 - level)
        
            lines.append(
                f"{i}. **{session['bot_name']}** ({session['role'].title()}) {status}\n"
                f"   📈 Level: {level}/12 {level_bar}\n"
                f"   💬 {session.get('total_messages', 0)} pesan\n"
                f"   🕐 {age}\n"
                f"   📝 {session.get('summary', '')[:50]}..."
            )
            lines.append("")
    
        lines.append("💡 **Cara pakai:**")
        lines.append("• `/continue 1` - Lanjut session nomor 1")
        lines.append("• `/continue MYLOVE-PUTRI-IPAR-123-20260322-001` - Pakai ID langsung")
    
        return "\n".join(lines)
    
    # =========================================================================
    # FIND SESSION
    # =========================================================================
    
    async def find_session_by_input(self, user_id: int, input_str: str) -> Optional[Dict]:
        """
        Cari session berdasarkan input user
        
        Args:
            user_id: ID user
            input_str: Bisa nomor (1,2,3) atau ID langsung
            
        Returns:
            Session data or None
        """
        # Cek apakah input adalah ID langsung
        if id_generator.is_valid_format(input_str):
            session = await self.storage.get_full_session(input_str)
            if session and session['user_id'] == user_id:
                return session
                
        # Cek apakah input adalah nomor
        try:
            idx = int(input_str) - 1
            sessions = await self.get_continuable_sessions(user_id, 10)
            
            if 0 <= idx < len(sessions):
                session_id = sessions[idx]['id']
                return await self.storage.get_full_session(session_id)
                
        except ValueError:
            pass
            
        return None
        
    # =========================================================================
    # CONTINUE SESSION
    # =========================================================================

    async def continue_session(self, user_id: int, session_id: str) -> Dict:
        """
        Continue session yang sudah di-close
    
        Args:
            user_id: ID user
            session_id: Session ID
        
        Returns:
            Session data with context
        """
        # Get session
        session = await self.storage.get_full_session(session_id)
    
        if not session:
            raise ValueError(f"Session {session_id} tidak ditemukan")
        
        if session['user_id'] != user_id:
            raise ValueError("Session ini bukan milik kamu")
    
        # Continue (reactivate if closed)
        continued = await self.storage.continue_session(session_id)
    
        # Generate context summary
        context = await self._generate_context_summary(continued)
    
        return {
            "session": continued,
            "context": context,
            "last_messages": continued.get('conversation', [])[-5:]  # Last 5 messages
        }


    async def _generate_context_summary(self, session: Dict) -> str:
        """Generate context summary untuk dilanjutkan"""
    
        parts = []
    
        # Basic info
        bot_name = session.get('bot_name', session['role'].title())
        parts.append(f"Melanjutkan session dengan **{bot_name}** ({session['role'].title()})")
    
        # Intimacy level
        level = session.get('intimacy_level', 1)
        parts.append(f"Intimacy Level: {level}/12")
    
        # Location
        if session.get('location'):
            parts.append(f"Terakhir di: {session['location']}")
        
        # Milestones
        milestones = session.get('milestones', [])
        if milestones:
            recent = milestones[-3:]
            milestone_names = [m['type'] if isinstance(m, dict) else m for m in recent]
            parts.append(f"Milestone: {', '.join(milestone_names)}")
        
        # Last message
        conv = session.get('conversation', [])
        if conv:
            last = conv[-1]
            last_time = datetime.fromtimestamp(last['timestamp']).strftime("%H:%M")
            parts.append(f"\nPesan terakhir ({last_time}):")
            parts.append(f"Kamu: {last['user'][:50]}...")
            parts.append(f"{bot_name}: {last['bot'][:50]}...")
        
        return "\n".join(parts)
    
    # =========================================================================
    # COMMAND HANDLER
    # =========================================================================

    async def handle_continue_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk /continue command
    
        Usage:
            /continue - List sessions
            /continue 1 - Continue session nomor 1
            /continue MYLOVE-PUTRI-IPAR-123-20260322-001 - Continue by ID
        """
        user_id = update.effective_user.id
        args = context.args
    
        # No args -> show list
        if not args:
            sessions = await self.get_continuable_sessions(user_id)
        
            if not sessions:
                await update.message.reply_text(
                    "📋 **DAFTAR SESSION**\n\n"
                    "Belum ada session tersimpan.\n"
                    "Mulai dengan /start untuk membuat session baru.",
                    parse_mode='HTML'
                )
                return
        
            formatted = self.format_session_list(sessions)
            await update.message.reply_text(formatted, parse_mode='HTML')
            return
    
        # Has args -> try to continue
        input_str = ' '.join(args)
    
        try:
            # Find session
            session_data = await self.find_session_by_input(user_id, input_str)
        
            if not session_data:
                await update.message.reply_text(
                    "❌ Session tidak ditemukan.\n"
                    "Ketik /continue untuk lihat daftar session."
                )
                return
        
            # Continue session
            result = await self.continue_session(user_id, session_data['id'])
        
            # Send response
            await update.message.reply_text(
                f"🔄 **Melanjutkan Session**\n\n"
                f"{result['context']}\n\n"
                f"_Ketik pesan untuk melanjutkan cerita..._",
                parse_mode='HTML'
            )
        
            # Store session ID in context for message handler
            context.user_data['current_session'] = session_data['id']
            context.user_data['current_role'] = session_data['role']
            context.user_data['bot_name'] = session_data.get('bot_name', session_data['role'].title())
            context.user_data['intimacy_level'] = session_data.get('intimacy_level', 1)
            context.user_data['total_chats'] = session_data.get('total_messages', 0)
            context.user_data['current_location'] = session_data.get('location', 'ruang tamu')
        
            # Restore relationship status
            rel_status = session_data.get('relationship_status', 'pdkt')
            context.user_data['relationship_status'] = rel_status
        
        except ValueError as e:
            await update.message.reply_text(f"❌ {str(e)}")
        except Exception as e:
            logger.error(f"Error in continue command: {e}")
            await update.message.reply_text(
                "❌ Gagal melanjutkan session. Coba lagi nanti."
            )
    
    # =========================================================================
    # AUTO-SAVE & CONTINUE
    # =========================================================================
    
    async def auto_save_session(self, session_id: str, summary: Optional[str] = None):
        """
        Auto-save session (misal setelah /close atau idle)
        """
        await self.storage.close_session(session_id, summary)
        
    async def get_session_preview(self, session_id: str) -> str:
        """
        Get preview text untuk session
        
        Berguna untuk ditampilkan sebelum continue
        """
        session = await self.storage.get_full_session(session_id)
        if not session:
            return "Session tidak ditemukan"
            
        display = id_generator.format_for_display(session_id)
        conv = session.get('conversation', [])
        
        preview = [
            f"📁 **{display}**",
            f"Role: {session['role'].title()}",
            f"Bot: {session.get('bot_name', session['role'].title())}",
            f"Level: {session.get('intimacy_level', 1)}/12",
            f"Total pesan: {session.get('total_messages', 0)}",
        ]
        
        if conv:
            preview.append("")
            preview.append("**Preview:**")
            for msg in conv[-3:]:
                preview.append(f"Kamu: {msg['user'][:30]}...")
                
        return "\n".join(preview)
    
    # =========================================================================
    # SESSION EXPIRY
    # =========================================================================
    
    async def check_session_expiry(self, user_id: int, current_session_id: str) -> bool:
        """
        Cek apakah session sudah expired (lebih dari 24 jam idle)
        
        Returns:
            True jika masih valid, False jika expired
        """
        session = await self.storage.get_session(current_session_id)
        if not session:
            return False
            
        last_active = session.get('last_message_time', 0)
        idle_hours = (time.time() - last_active) / 3600
        
        if idle_hours > 24:
            # Auto-close expired session
            await self.auto_save_session(
                current_session_id,
                f"Auto-closed after {idle_hours:.0f} hours idle"
            )
            return False
            
        return True
    
    # =========================================================================
    # STATISTICS
    # =========================================================================
    
    async def get_continuation_stats(self, user_id: int) -> Dict:
        """
        Get continuation statistics for user
        
        Args:
            user_id: ID user
            
        Returns:
            Dict with statistics
        """
        sessions = await self.get_continuable_sessions(user_id, 100)
        
        active = [s for s in sessions if s['is_active']]
        closed = [s for s in sessions if not s['is_active']]
        
        return {
            "total_sessions": len(sessions),
            "active_sessions": len(active),
            "closed_sessions": len(closed),
            "avg_messages": sum(s['total_messages'] for s in sessions) / len(sessions) if sessions else 0,
            "avg_level": sum(s['intimacy_level'] for s in sessions) / len(sessions) if sessions else 0,
            "oldest_session": min(s['last_message_time'] for s in sessions) if sessions else 0,
            "newest_session": max(s['last_message_time'] for s in sessions) if sessions else 0
        }


__all__ = ['SessionContinuation']
