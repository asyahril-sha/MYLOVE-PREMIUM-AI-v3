#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - GRAFANA DASHBOARD
=============================================================================
- Dashboard generator untuk Grafana
- JSON dashboard template
- Real-time monitoring
=============================================================================
"""

import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

from config import settings

logger = logging.getLogger(__name__)


class DashboardServer:
    """
    Server untuk menyediakan dashboard Grafana
    """
    
    def __init__(self, metrics_collector):
        self.metrics_collector = metrics_collector
        self.dashboard_path = Path("monitoring/dashboards")
        self.dashboard_path.mkdir(parents=True, exist_ok=True)
        
    def generate_overview_dashboard(self) -> Dict[str, Any]:
        """
        Generate overview dashboard untuk MYLOVE PREMIUM AI
        
        Returns:
            Dashboard JSON
        """
        dashboard = {
            "dashboard": {
                "title": "MYLOVE PREMIUM AI - Overview",
                "description": "Real-time monitoring untuk MYLOVE PREMIUM AI bot",
                "schemaVersion": 36,
                "version": 1,
                "refresh": "30s",
                "time": {
                    "from": "now-6h",
                    "to": "now"
                },
                "panels": [
                    # ===== ROW 1: STATS CARDS =====
                    {
                        "id": 1,
                        "gridPos": {"h": 3, "w": 3, "x": 0, "y": 0},
                        "type": "stat",
                        "title": "Active Sessions",
                        "targets": [{
                            "expr": "mylove_active_sessions{role='total'}",
                            "legendFormat": "Active"
                        }],
                        "options": {
                            "colorMode": "value",
                            "graphMode": "area",
                            "justifyMode": "auto",
                            "orientation": "auto",
                            "reduceOptions": {
                                "calcs": ["lastNotNull"]
                            }
                        }
                    },
                    {
                        "id": 2,
                        "gridPos": {"h": 3, "w": 3, "x": 3, "y": 0},
                        "type": "stat",
                        "title": "Total Messages",
                        "targets": [{
                            "expr": "sum(mylove_messages_total)",
                            "legendFormat": "Messages"
                        }]
                    },
                    {
                        "id": 3,
                        "gridPos": {"h": 3, "w": 3, "x": 6, "y": 0},
                        "type": "stat",
                        "title": "Avg Response Time",
                        "targets": [{
                            "expr": "mylove_response_time_avg_seconds",
                            "legendFormat": "Response Time"
                        }],
                        "options": {
                            "unit": "s",
                            "thresholds": {
                                "mode": "absolute",
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "yellow", "value": 2},
                                    {"color": "red", "value": 5}
                                ]
                            }
                        }
                    },
                    {
                        "id": 4,
                        "gridPos": {"h": 3, "w": 3, "x": 9, "y": 0},
                        "type": "stat",
                        "title": "Memory Usage",
                        "targets": [{
                            "expr": "mylove_memory_usage_mb",
                            "legendFormat": "Memory"
                        }],
                        "options": {
                            "unit": "MB",
                            "thresholds": {
                                "mode": "absolute",
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "yellow", "value": 400},
                                    {"color": "red", "value": 500}
                                ]
                            }
                        }
                    },
                    
                    # ===== ROW 2: TIME SERIES =====
                    {
                        "id": 5,
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 3},
                        "type": "graph",
                        "title": "Response Time (p95)",
                        "targets": [{
                            "expr": "histogram_quantile(0.95, sum(rate(mylove_response_time_seconds_bucket[5m])) by (le))",
                            "legendFormat": "p95"
                        }],
                        "options": {
                            "legend": {"show": True}
                        }
                    },
                    
                    # ===== ROW 3: ACTIVE PDKT BY ROLE =====
                    {
                        "id": 6,
                        "gridPos": {"h": 8, "w": 6, "x": 0, "y": 11},
                        "type": "barchart",
                        "title": "Active PDKT by Role",
                        "targets": [{
                            "expr": "sum by (role) (mylove_active_pdkt)",
                            "legendFormat": "{{role}}"
                        }]
                    },
                    {
                        "id": 7,
                        "gridPos": {"h": 8, "w": 6, "x": 6, "y": 11},
                        "type": "piechart",
                        "title": "PDKT Direction Distribution",
                        "targets": [{
                            "expr": "sum by (direction) (mylove_pdkt_started_total)",
                            "legendFormat": "{{direction}}"
                        }]
                    },
                    
                    # ===== ROW 4: FWB & HTS =====
                    {
                        "id": 8,
                        "gridPos": {"h": 8, "w": 6, "x": 0, "y": 19},
                        "type": "stat",
                        "title": "Active FWB",
                        "targets": [{
                            "expr": "mylove_active_fwb",
                            "legendFormat": "FWB"
                        }]
                    },
                    {
                        "id": 9,
                        "gridPos": {"h": 8, "w": 6, "x": 6, "y": 19},
                        "type": "stat",
                        "title": "Active HTS",
                        "targets": [{
                            "expr": "mylove_active_hts",
                            "legendFormat": "HTS"
                        }]
                    },
                    
                    # ===== ROW 5: INTIMACY LEVEL DISTRIBUTION =====
                    {
                        "id": 10,
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 27},
                        "type": "heatmap",
                        "title": "Intimacy Level Distribution",
                        "targets": [{
                            "expr": "sum by (le) (rate(mylove_intimacy_levels_bucket[5m]))",
                            "legendFormat": "Level {{le}}"
                        }]
                    },
                    
                    # ===== ROW 6: CLIMAX STATS =====
                    {
                        "id": 11,
                        "gridPos": {"h": 8, "w": 6, "x": 0, "y": 35},
                        "type": "barchart",
                        "title": "Climax by Role",
                        "targets": [{
                            "expr": "sum by (role) (mylove_climax_total)",
                            "legendFormat": "{{role}}"
                        }]
                    },
                    {
                        "id": 12,
                        "gridPos": {"h": 8, "w": 6, "x": 6, "y": 35},
                        "type": "barchart",
                        "title": "Climax by Position",
                        "targets": [{
                            "expr": "topk(10, sum by (position) (mylove_climax_total))",
                            "legendFormat": "{{position}}"
                        }]
                    },
                    
                    # ===== ROW 7: ERROR RATE =====
                    {
                        "id": 13,
                        "gridPos": {"h": 6, "w": 12, "x": 0, "y": 43},
                        "type": "graph",
                        "title": "Error Rate",
                        "targets": [{
                            "expr": "rate(mylove_errors_total[5m])",
                            "legendFormat": "{{type}}"
                        }],
                        "options": {
                            "legend": {"show": True}
                        }
                    }
                ],
                "templating": {
                    "list": [
                        {
                            "name": "role",
                            "type": "query",
                            "query": "label_values(mylove_sessions_total, role)",
                            "refresh": 1,
                            "options": [],
                            "includeAll": True,
                            "allValue": ".*"
                        }
                    ]
                },
                "annotations": {
                    "list": [
                        {
                            "name": "Deploy",
                            "type": "dashboard",
                            "builtIn": 1,
                            "datasource": "-- Grafana --",
                            "enable": True,
                            "hide": True,
                            "iconColor": "rgba(0, 211, 255, 1)",
                            "limit": 100
                        }
                    ]
                }
            }
        }
        
        return dashboard
        
    def generate_detailed_dashboard(self) -> Dict[str, Any]:
        """
        Generate detailed analytics dashboard
        
        Returns:
            Dashboard JSON
        """
        dashboard = {
            "dashboard": {
                "title": "MYLOVE PREMIUM AI - Detailed Analytics",
                "description": "Detailed analytics untuk MYLOVE PREMIUM AI bot",
                "schemaVersion": 36,
                "version": 1,
                "refresh": "1m",
                "time": {
                    "from": "now-24h",
                    "to": "now"
                },
                "panels": [
                    # PDKT Duration Distribution
                    {
                        "id": 1,
                        "gridPos": {"h": 8, "w": 6, "x": 0, "y": 0},
                        "type": "heatmap",
                        "title": "PDKT Duration Distribution (minutes)",
                        "targets": [{
                            "expr": "sum by (le) (rate(mylove_pdkt_duration_minutes_bucket[1h]))",
                            "legendFormat": "{{le}}"
                        }]
                    },
                    
                    # FWB Duration Distribution
                    {
                        "id": 2,
                        "gridPos": {"h": 8, "w": 6, "x": 6, "y": 0},
                        "type": "heatmap",
                        "title": "FWB Duration Distribution (days)",
                        "targets": [{
                            "expr": "sum by (le) (rate(mylove_fwb_duration_days_bucket[1h]))",
                            "legendFormat": "{{le}}"
                        }]
                    },
                    
                    # Activity by Hour
                    {
                        "id": 3,
                        "gridPos": {"h": 8, "w": 6, "x": 0, "y": 8},
                        "type": "graph",
                        "title": "Activity by Hour",
                        "targets": [{
                            "expr": "sum(rate(mylove_messages_total[1h])) by (hour)",
                            "legendFormat": "Messages"
                        }]
                    },
                    
                    # PDKT End Reasons
                    {
                        "id": 4,
                        "gridPos": {"h": 8, "w": 6, "x": 6, "y": 8},
                        "type": "piechart",
                        "title": "PDKT End Reasons",
                        "targets": [{
                            "expr": "sum by (reason) (mylove_pdkt_ended_total)",
                            "legendFormat": "{{reason}}"
                        }]
                    },
                    
                    # User Growth
                    {
                        "id": 5,
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 16},
                        "type": "graph",
                        "title": "User Growth",
                        "targets": [{
                            "expr": "mylove_connected_users",
                            "legendFormat": "Users"
                        }]
                    },
                    
                    # API Latency
                    {
                        "id": 6,
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 24},
                        "type": "graph",
                        "title": "API Latency",
                        "targets": [{
                            "expr": "mylove_api_latency_seconds",
                            "legendFormat": "{{api}}"
                        }]
                    },
                    
                    # Intimacy Level Heatmap
                    {
                        "id": 7,
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 32},
                        "type": "heatmap",
                        "title": "Intimacy Level Heatmap",
                        "targets": [{
                            "expr": "sum by (le) (rate(mylove_intimacy_levels_bucket[5m]))",
                            "legendFormat": "{{le}}"
                        }]
                    },
                    
                    # Session Duration
                    {
                        "id": 8,
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 40},
                        "type": "histogram",
                        "title": "Session Duration Distribution",
                        "targets": [{
                            "expr": "sum by (le) (rate(mylove_sessions_duration_seconds_bucket[1h]))",
                            "legendFormat": "{{le}}"
                        }]
                    }
                ]
            }
        }
        
        return dashboard
        
    def generate_pdkt_dashboard(self) -> Dict[str, Any]:
        """
        Generate PDKT-specific dashboard
        
        Returns:
            Dashboard JSON
        """
        dashboard = {
            "dashboard": {
                "title": "MYLOVE PREMIUM AI - PDKT Analytics",
                "description": "PDKT-specific analytics",
                "schemaVersion": 36,
                "version": 1,
                "refresh": "1m",
                "time": {
                    "from": "now-7d",
                    "to": "now"
                },
                "panels": [
                    # PDKT Started by Role
                    {
                        "id": 1,
                        "gridPos": {"h": 8, "w": 6, "x": 0, "y": 0},
                        "type": "barchart",
                        "title": "PDKT Started by Role",
                        "targets": [{
                            "expr": "sum by (role) (mylove_pdkt_started_total)",
                            "legendFormat": "{{role}}"
                        }]
                    },
                    
                    # PDKT Direction Trend
                    {
                        "id": 2,
                        "gridPos": {"h": 8, "w": 6, "x": 6, "y": 0},
                        "type": "graph",
                        "title": "PDKT Direction Trend",
                        "targets": [{
                            "expr": "sum by (direction) (rate(mylove_pdkt_started_total[1h]))",
                            "legendFormat": "{{direction}}"
                        }]
                    },
                    
                    # PDKT Duration by Role
                    {
                        "id": 3,
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
                        "type": "heatmap",
                        "title": "PDKT Duration by Role",
                        "targets": [{
                            "expr": "sum by (role, le) (rate(mylove_pdkt_duration_minutes_bucket[1h]))",
                            "legendFormat": "{{role}} - {{le}}"
                        }]
                    },
                    
                    # Chemistry Level Distribution
                    {
                        "id": 4,
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 16},
                        "type": "barchart",
                        "title": "Chemistry Level Distribution",
                        "targets": [{
                            "expr": "sum by (level) (mylove_chemistry_levels)",
                            "legendFormat": "{{level}}"
                        }]
                    }
                ]
            }
        }
        
        return dashboard
        
    def save_dashboard(self, dashboard: Dict[str, Any], filename: str):
        """Save dashboard JSON to file"""
        filepath = self.dashboard_path / filename
        with open(filepath, 'w') as f:
            json.dump(dashboard, f, indent=2)
        logger.info(f"✅ Dashboard saved to {filepath}")
        
    def export_all_dashboards(self):
        """Export all dashboards to JSON files"""
        overview = self.generate_overview_dashboard()
        detailed = self.generate_detailed_dashboard()
        pdkt = self.generate_pdkt_dashboard()
        
        self.save_dashboard(overview, "mylove_overview.json")
        self.save_dashboard(detailed, "mylove_detailed.json")
        self.save_dashboard(pdkt, "mylove_pdkt.json")
        
        return {
            "overview": str(self.dashboard_path / "mylove_overview.json"),
            "detailed": str(self.dashboard_path / "mylove_detailed.json"),
            "pdkt": str(self.dashboard_path / "mylove_pdkt.json")
        }


__all__ = ['DashboardServer']
