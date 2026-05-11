"""
Tests for AliasForge.
"""

import pytest
import tempfile
from pathlib import Path

from aliasforge.core.database import Database
from aliasforge.core.alias_manager import AliasManager
from aliasforge.core.stats import StatsManager


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)
    
    db = Database(db_path)
    yield db
    
    db.close()
    db_path.unlink(missing_ok=True)


@pytest.fixture
def manager(temp_db):
    """Create an AliasManager with temporary database."""
    return AliasManager(temp_db)


class TestDatabase:
    """Tests for Database class."""
    
    def test_add_alias(self, temp_db):
        """Test adding an alias."""
        alias_id = temp_db.add_alias("gs", "git status", "Show git status")
        assert alias_id > 0
        
        alias = temp_db.get_alias("gs")
        assert alias is not None
        assert alias["name"] == "gs"
        assert alias["command"] == "git status"
        assert alias["description"] == "Show git status"
    
    def test_get_all_aliases(self, temp_db):
        """Test getting all aliases."""
        temp_db.add_alias("gs", "git status")
        temp_db.add_alias("gp", "git push")
        
        aliases = temp_db.get_all_aliases()
        assert len(aliases) == 2
    
    def test_update_alias(self, temp_db):
        """Test updating an alias."""
        temp_db.add_alias("gs", "git status")
        
        success = temp_db.update_alias("gs", command="git status -s")
        assert success
        
        alias = temp_db.get_alias("gs")
        assert alias["command"] == "git status -s"
    
    def test_delete_alias(self, temp_db):
        """Test deleting an alias."""
        temp_db.add_alias("gs", "git status")
        
        success = temp_db.delete_alias("gs")
        assert success
        
        alias = temp_db.get_alias("gs")
        assert alias is None
    
    def test_search_aliases(self, temp_db):
        """Test searching aliases."""
        temp_db.add_alias("gs", "git status")
        temp_db.add_alias("gp", "git push")
        temp_db.add_alias("ls", "ls -la")
        
        results = temp_db.search_aliases("git")
        assert len(results) == 2


class TestAliasManager:
    """Tests for AliasManager class."""
    
    def test_add_alias(self, manager):
        """Test adding an alias through manager."""
        alias = manager.add("gs", "git status", description="Show git status")
        assert alias["name"] == "gs"
    
    def test_list_aliases(self, manager):
        """Test listing aliases."""
        manager.add("gs", "git status")
        manager.add("gp", "git push")
        
        aliases = manager.list()
        assert len(aliases) == 2
    
    def test_search(self, manager):
        """Test searching aliases."""
        manager.add("gs", "git status")
        manager.add("gp", "git push")
        manager.add("ls", "ls -la")
        
        results = manager.search("git")
        assert len(results) == 2
    
    def test_get_groups(self, manager):
        """Test getting groups."""
        manager.add("gs", "git status", group="git")
        manager.add("gp", "git push", group="git")
        manager.add("ls", "ls -la", group="system")
        
        groups = manager.get_groups()
        assert "git" in groups
        assert "system" in groups
    
    def test_export_import(self, manager):
        """Test export and import."""
        manager.add("gs", "git status")
        manager.add("gp", "git push")
        
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as f:
            export_path = Path(f.name)
        
        try:
            # Export
            manager.export_to_file(export_path)
            assert export_path.exists()
            
            # Clear and import
            manager.delete("gs")
            manager.delete("gp")
            
            count = manager.import_from_file(export_path)
            assert count == 2
            
            aliases = manager.list()
            assert len(aliases) == 2
        finally:
            export_path.unlink(missing_ok=True)


class TestStatsManager:
    """Tests for StatsManager class."""
    
    def test_record_usage(self, temp_db):
        """Test recording usage."""
        temp_db.add_alias("gs", "git status")
        
        stats = StatsManager(temp_db)
        stats.record_usage("gs")
        
        summary = stats.get_summary()
        assert summary["total_usage"] == 1
    
    def test_get_summary(self, manager):
        """Test getting usage summary."""
        manager.add("gs", "git status")
        
        stats = StatsManager(manager.db)
        summary = stats.get_summary()
        
        assert "total_usage" in summary
        assert "total_aliases" in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
