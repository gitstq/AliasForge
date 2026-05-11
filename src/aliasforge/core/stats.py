"""
Statistics module for AliasForge.
Provides usage tracking and analysis.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from aliasforge.core.database import Database


class StatsManager:
    """Manage alias usage statistics."""
    
    def __init__(self, db: Optional[Database] = None):
        """Initialize stats manager.
        
        Args:
            db: Database instance
        """
        self.db = db or Database()
    
    def record_usage(self, alias_name: str) -> None:
        """Record alias usage."""
        self.db.record_usage(alias_name)
    
    def get_top_aliases(self, limit: int = 10, days: int = 30) -> List[Dict[str, Any]]:
        """Get most used aliases.
        
        Args:
            limit: Maximum number of results
            days: Number of days to analyze
            
        Returns:
            List of top aliases with usage counts
        """
        stats = self.db.get_usage_stats(days)
        return stats[:limit]
    
    def get_usage_trend(self, alias_name: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get usage trend for a specific alias.
        
        Args:
            alias_name: Alias name
            days: Number of days to analyze
            
        Returns:
            List of daily usage counts
        """
        # This would require more complex SQL queries
        # For now, return a simplified version
        alias = self.db.get_alias(alias_name)
        if not alias:
            return []
        
        # Get total usage in the period
        stats = self.db.get_usage_stats(days)
        for stat in stats:
            if stat["name"] == alias_name:
                return [{"total": stat["usage_count"]}]
        
        return [{"total": 0}]
    
    def get_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get overall usage summary.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Summary dict with statistics
        """
        stats = self.db.get_usage_stats(days)
        
        total_usage = sum(s["usage_count"] for s in stats)
        unique_aliases = len([s for s in stats if s["usage_count"] > 0])
        
        return {
            "period_days": days,
            "total_usage": total_usage,
            "unique_aliases_used": unique_aliases,
            "total_aliases": len(self.db.get_all_aliases()),
            "top_aliases": stats[:5]
        }
    
    def get_unused_aliases(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get aliases that haven't been used recently.
        
        Args:
            days: Number of days to check
            
        Returns:
            List of unused aliases
        """
        stats = self.db.get_usage_stats(days)
        used_names = {s["name"] for s in stats if s["usage_count"] > 0}
        
        all_aliases = self.db.get_all_aliases()
        return [a for a in all_aliases if a["name"] not in used_names]
