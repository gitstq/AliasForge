"""
AliasForge - Lightweight Terminal Command Alias Intelligent Manager CLI
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"

from aliasforge.core.database import Database
from aliasforge.core.alias_manager import AliasManager
from aliasforge.core.stats import StatsManager

__all__ = [
    "Database",
    "AliasManager", 
    "StatsManager",
    "__version__",
]
