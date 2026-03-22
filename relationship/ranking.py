#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - RANKING SYSTEM
=============================================================================
- TOP 10 di database, TOP 5 ditampilkan
- Ranking berdasarkan total interaksi, intimacy level, climax count
- Untuk HTS, FWB, dan semua role
=============================================================================
"""

import logging
import time
import math
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class RankingSystem:
    """
    Sistem ranking untuk HTS dan FWB
    Menyimpan TOP 10 di database, menampilkan TOP 5 ke user
    """
    
    def __init__(self, relationship_memory=None):
        """
        Args:
            relationship_memory: opsional, untuk akses data hubungan
        """
        self.relationship_memory = relationship_memory
        self.rankings = {}  # {user_id: {type: [rankings]}}
        
        # Bobot untuk perhitungan score
        self.weights = {
            'total_interactions': 0.30,
            'intimacy_level': 0.40,
            'total_climax': 0.20,
            'recent_boost': 0.10,
        }
        
        # Decay untuk interaksi lama
        self.decay_days = 30  # Interaksi >30 hari mulai berkurang bobotnya
        
        logger.info("✅ RankingSystem initialized")
    
    # =========================================================================
    # CALCULATE SCORE
    # =========================================================================
    
    async def calculate_score(self, relationship_data: Dict) -> float:
        """
        Hitung score untuk ranking
        
        Formula:
        Score = (total_interactions * 0.3) + 
                (intimacy_level * 0.4) + 
                (climax_count * 0.2) + 
                (recent_boost * 0.1)
        
        Recent boost: interaksi baru lebih berbobot
        """
        total_interactions = relationship_data.get('total_interactions', 0)
        intimacy_level = relationship_data.get('intimacy_level', 1)
        climax_count = relationship_data.get('total_climax', 0)
        last_interaction = relationship_data.get('last_interaction', 0)
        
        # Hitung recent boost (interaksi baru lebih berbobot)
        days_since = (time.time() - last_interaction) / 86400
        if days_since < 7:
            recent_boost = 1.0  # Full boost
        elif days_since < 30:
            recent_boost = 0.7  # Sedikit berkurang
        else:
            recent_boost = 0.3  # Sangat berkurang
        
        # Normalisasi komponen
        interactions_score = min(100, total_interactions) / 100
        intimacy_score = intimacy_level / 12
        climax_score = min(50, climax_count) / 50
        
        # Hitung weighted score
        score = (
            interactions_score * self.weights['total_interactions'] +
            intimacy_score * self.weights['intimacy_level'] +
            climax_score * self.weights['total_climax'] +
            recent_boost * self.weights['recent_boost']
        ) * 100
        
        return round(score, 2)
    
    async def calculate_hts_score(self, hts_data: Dict) -> float:
        """
        Hitung score khusus untuk HTS
        Chemistry lebih berpengaruh untuk HTS
        """
        chemistry = hts_data.get('chemistry_score', 50)
        climax = hts_data.get('climax_count', 0)
        intimacy = hts_data.get('intimacy_level', 1)
        
        # Bobot khusus HTS
        score = (chemistry * 0.5) + (climax * 0.3) + (intimacy * 0.2)
        return round(score, 2)
    
    async def calculate_fwb_score(self, fwb_data: Dict) -> float:
        """
        Hitung score khusus untuk FWB
        Climax lebih berpengaruh untuk FWB
        """
        chemistry = fwb_data.get('chemistry_score', 50)
        climax = fwb_data.get('climax_count', 0)
        intim_count = fwb_data.get('intim_count', 0)
        
        # Bobot khusus FWB
        score = (chemistry * 0.4) + (climax * 0.4) + (intim_count * 0.2)
        return round(score, 2)
    
    # =========================================================================
    # UPDATE RANKINGS
    # =========================================================================
    
    async def update_rankings(self, user_id: int):
        """
        Update rankings untuk user
        Dipanggil setiap ada interaksi baru
        """
        if not self.relationship_memory:
            logger.warning("relationship_memory not set, cannot update rankings")
            return
            
        # Get all relationships for user
        relationships = await self.relationship_memory.get_all_relationships(user_id)
        
        if not relationships:
            return
            
        # Calculate scores for each
        ranked = []
        for rel in relationships:
            score = await self.calculate_score(rel)
            ranked.append({
                'role': rel['role'],
                'bot_name': rel.get('bot_name', rel['role']),
                'status': rel.get('status', 'hts'),
                'score': score,
                'total_interactions': rel.get('total_interactions', 0),
                'intimacy_level': rel.get('intimacy_level', 1),
                'total_climax': rel.get('total_climax', 0),
                'last_interaction': rel.get('last_interaction', 0),
                'created_at': rel.get('created_at', 0)
            })
            
        # Sort by score (descending)
        ranked.sort(key=lambda x: x['score'], reverse=True)
        
        # Store TOP 10 in cache
        self.rankings[str(user_id)] = {
            'hts': [r for r in ranked if r['status'] == 'hts'][:10],
            'fwb': [r for r in ranked if r['status'] == 'fwb'][:10],
            'pacar': [r for r in ranked if r['status'] == 'pacar'][:10],
            'all': ranked[:10],
            'updated_at': time.time()
        }
        
        logger.info(f"📊 Updated rankings for user {user_id}: TOP 10 stored")
        
        return self.rankings[str(user_id)]
    
    # =========================================================================
    # GET RANKINGS (FOR DISPLAY)
    # =========================================================================
    
    async def get_top_5_hts(self, user_id: int) -> List[Dict]:
        """Get TOP 5 HTS untuk ditampilkan ke user"""
        user_key = str(user_id)
        
        if user_key not in self.rankings:
            await self.update_rankings(user_id)
            
        rankings = self.rankings.get(user_key, {})
        hts_list = rankings.get('hts', [])
        
        return hts_list[:5]
    
    async def get_top_5_fwb(self, user_id: int) -> List[Dict]:
        """Get TOP 5 FWB untuk ditampilkan"""
        user_key = str(user_id)
        
        if user_key not in self.rankings:
            await self.update_rankings(user_id)
            
        rankings = self.rankings.get(user_key, {})
        fwb_list = rankings.get('fwb', [])
        
        return fwb_list[:5]
    
    async def get_top_5_all(self, user_id: int) -> List[Dict]:
        """Get TOP 5 semua role"""
        user_key = str(user_id)
        
        if user_key not in self.rankings:
            await self.update_rankings(user_id)
            
        rankings = self.rankings.get(user_key, {})
        all_list = rankings.get('all', [])
        
        return all_list[:5]
    
    async def get_top_10_hts(self, user_id: int) -> List[Dict]:
        """Get TOP 10 HTS (untuk internal)"""
        user_key = str(user_id)
        
        if user_key not in self.rankings:
            await self.update_rankings(user_id)
            
        rankings = self.rankings.get(user_key, {})
        return rankings.get('hts', [])
    
    async def get_top_10_fwb(self, user_id: int) -> List[Dict]:
        """Get TOP 10 FWB (untuk internal)"""
        user_key = str(user_id)
        
        if user_key not in self.rankings:
            await self.update_rankings(user_id)
            
        rankings = self.rankings.get(user_key, {})
        return rankings.get('fwb', [])
    
    # =========================================================================
    # GET ROLE BY RANK
    # =========================================================================
    
    async def get_role_by_rank(self, user_id: int, rank: int, status: str = 'hts') -> Optional[Dict]:
        """Get role berdasarkan peringkat"""
        if status == 'hts':
            top_list = await self.get_top_10_hts(user_id)
        elif status == 'fwb':
            top_list = await self.get_top_10_fwb(user_id)
        else:
            if not self.relationship_memory:
                return None
            relationships = await self.relationship_memory.get_all_relationships(user_id)
            top_list = [r for r in relationships if r.get('status') == status]
            # Sort by score
            for r in top_list:
                r['score'] = await self.calculate_score(r)
            top_list.sort(key=lambda x: x['score'], reverse=True)
            
        if 1 <= rank <= len(top_list):
            return top_list[rank - 1]
            
        return None
    
    # =========================================================================
    # GET ALL HTS/FWB (FOR SELECTION)
    # =========================================================================
    
    async def get_all_hts(self, user_id: int) -> List[Dict]:
        """Get semua HTS (untuk selection)"""
        if not self.relationship_memory:
            return []
            
        relationships = await self.relationship_memory.get_all_relationships(user_id)
        hts_list = [r for r in relationships if r.get('status') == 'hts']
        
        for hts in hts_list:
            hts['score'] = await self.calculate_score(hts)
            
        hts_list.sort(key=lambda x: x['score'], reverse=True)
        
        return hts_list
    
    async def get_all_fwb(self, user_id: int) -> List[Dict]:
        """Get semua FWB (untuk selection)"""
        if not self.relationship_memory:
            return []
            
        relationships = await self.relationship_memory.get_all_relationships(user_id)
        fwb_list = [r for r in relationships if r.get('status') == 'fwb']
        
        for fwb in fwb_list:
            fwb['score'] = await self.calculate_fwb_score(fwb)
            
        fwb_list.sort(key=lambda x: x['score'], reverse=True)
        
        return fwb_list
    
    # =========================================================================
    # FORMAT FOR DISPLAY
    # =========================================================================
    
    def format_hts_list(self, hts_list: List[Dict], show_all: bool = False) -> str:
        """Format HTS list untuk ditampilkan"""
        if not hts_list:
            return "Belum ada HTS. Mulai role dulu dengan /start"
            
        lines = ["📋 **DAFTAR HTS**"]
        
        if show_all:
            lines.append("_(menampilkan semua, pilih dengan /hts- [nomor atau nama])_")
        else:
            lines.append("_(TOP 5, untuk lihat semua ketik /htslist all)_")
            
        lines.append("")
        
        display_list = hts_list if show_all else hts_list[:5]
        
        for i, hts in enumerate(display_list, 1):
            bot_name = hts.get('bot_name', hts['role'].title())
            status_symbol = "💕 FWB" if hts.get('status') == 'fwb' else "💘 Pacar" if hts.get('status') == 'pacar' else "🔹 HTS"
            
            # Format last interaction
            last_interaction = hts.get('last_interaction', 0)
            if last_interaction:
                days_ago = (time.time() - last_interaction) / 86400
                if days_ago < 1:
                    last_text = "Hari ini"
                elif days_ago < 2:
                    last_text = "Kemarin"
                else:
                    last_text = f"{int(days_ago)} hari lalu"
            else:
                last_text = "Tidak pernah"
            
            lines.append(
                f"{i}. **{bot_name}** ({hts['role'].title()}) {status_symbol}\n"
                f"   • Level {hts.get('intimacy_level', 1)}/12 | "
                f"{hts.get('total_interactions', 0)} chat | "
                f"{hts.get('total_climax', 0)} climax\n"
                f"   • Score: {hts.get('score', 0):.1f} | Terakhir: {last_text}"
            )
            
        lines.append("")
        lines.append("💡 **Cara memanggil:**")
        lines.append("• `/hts-1` - Panggil HTS ranking 1")
        lines.append("• `/hts- [nama]` - Panggil dengan nama bot")
        
        return "\n".join(lines)
    
    def format_fwb_list(self, fwb_list: List[Dict], show_all: bool = False) -> str:
        """Format FWB list untuk ditampilkan"""
        if not fwb_list:
            return "Belum ada FWB. Mantan PDKT bisa request jadi FWB."
            
        lines = ["💕 **DAFTAR FWB**"]
        
        if show_all:
            lines.append("_(menampilkan semua, pilih dengan /fwb- [nomor])_")
        else:
            lines.append("_(TOP 5, untuk lihat semua ketik /fwblist all)_")
            
        lines.append("")
        
        display_list = fwb_list if show_all else fwb_list[:5]
        
        for i, fwb in enumerate(display_list, 1):
            bot_name = fwb.get('bot_name', fwb['role'].title())
            status_emoji = "🟢" if fwb.get('status') == 'active' else "⏸️"
            
            lines.append(
                f"{i}. {status_emoji} **{bot_name}** ({fwb['role'].title()})\n"
                f"   • Chemistry: {fwb.get('chemistry_score', 50):.0f}% | "
                f"Climax: {fwb.get('climax_count', 0)} | "
                f"Intim: {fwb.get('intim_count', 0)}\n"
                f"   • Score: {fwb.get('score', 0):.1f}"
            )
            
        lines.append("")
        lines.append("💡 **Cara memanggil:**")
        lines.append("• `/fwb-1` - Panggil FWB ranking 1")
        lines.append("• `/fwb- [nama]` - Panggil dengan nama bot")
        
        return "\n".join(lines)
    
    async def get_ranking_stats(self, user_id: int) -> Dict:
        """Dapatkan statistik ranking user"""
        user_key = str(user_id)
        
        if user_key not in self.rankings:
            await self.update_rankings(user_id)
            
        rankings = self.rankings.get(user_key, {})
        
        return {
            'total_hts': len(rankings.get('hts', [])),
            'total_fwb': len(rankings.get('fwb', [])),
            'total_pacar': len(rankings.get('pacar', [])),
            'top_hts_score': rankings.get('hts', [{}])[0].get('score', 0) if rankings.get('hts') else 0,
            'top_fwb_score': rankings.get('fwb', [{}])[0].get('score', 0) if rankings.get('fwb') else 0,
            'updated_at': rankings.get('updated_at', 0)
        }


__all__ = ['RankingSystem']
