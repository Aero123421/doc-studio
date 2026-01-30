"""
Doc Studio Skill - Core Module
Enterprise document generation for AI coding assistants
"""

__version__ = "1.0.0"
__author__ = "Doc Studio Team"

from .generator import DocumentGenerator
from .template import TemplateManager
from .preflight import PreflightChecker
from .config import ConfigManager

__all__ = [
    "DocumentGenerator",
    "TemplateManager",
    "PreflightChecker",
    "ConfigManager",
]
