#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE PREMIUM AI - ADVANCED LOGGING SYSTEM
=============================================================================
"""

import sys
from pathlib import Path
from loguru import logger as loguru_logger

try:
    from config import settings
except ImportError:
    settings = None

logger = loguru_logger


def setup_logging(module_name: str = "MYLOVE-PREMIUM-AI"):
    """Setup logging system"""
    
    if settings and hasattr(settings, 'logging') and hasattr(settings.logging, 'log_dir'):
        log_dir = Path(settings.logging.log_dir)
    else:
        log_dir = Path("data/logs")
    
    log_dir.mkdir(exist_ok=True, parents=True)
    
    logger.remove()
    
    console_level = settings.logging.level if settings and hasattr(settings, 'logging') else "INFO"
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=console_level,
        colorize=True,
        enqueue=True,
        backtrace=True,
        diagnose=True
    )
    
    log_file = log_dir / f"{module_name}.log"
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="50 MB",
        retention="30 days",
        compression="zip",
        enqueue=True,
        backtrace=True,
        diagnose=True
    )
    
    error_file = log_dir / f"{module_name}_error.log"
    logger.add(
        error_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="50 MB",
        retention="90 days",
        compression="zip",
        enqueue=True,
        backtrace=True,
        diagnose=True
    )
    
    json_log = log_dir / f"{module_name}_json.log"
    logger.add(
        json_log,
        format="{time} | {level} | {name} | {message}",
        level="INFO",
        rotation="100 MB",
        serialize=True,
        enqueue=True
    )
    
    logger.info("=" * 70)
    logger.info("📝 MYLOVE PREMIUM AI - Logging System Initialized")
    logger.info(f"   • Log file: {log_file}")
    logger.info(f"   • Error file: {error_file}")
    logger.info(f"   • JSON log: {json_log}")
    logger.info(f"   • Log level: {console_level}")
    logger.info("=" * 70)
    
    return logger


def get_logger(name: str = None):
    """
    Get logger instance (alias untuk compatibility)
    
    Args:
        name: Nama logger (optional)
        
    Returns:
        Logger instance
    """
    if name:
        return logger.bind(name=name)
    return logger


__all__ = ['setup_logging', 'get_logger', 'logger']
