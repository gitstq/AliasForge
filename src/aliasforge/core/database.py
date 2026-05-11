"""
Core database module for AliasForge.
Provides SQLite-based storage for aliases and statistics.
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any


class Database:
    """Lightweight SQLite database manager for aliases."""
    
    DEFAULT_DB_PATH = Path.home() / ".aliasforge" / "aliases.db"
    
    def __init__(self, db_path: Optional[Path] = None):
        """Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file. Defaults to ~/.aliasforge/aliases.db
        """
        self.db_path = Path(db_path) if db_path else self.DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None
        self._init_db()
    
    @property
    def conn(self) -> sqlite3.Connection:
        """Get database connection."""
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.row_factory = sqlite3.Row
        return self._conn
    
    def _init_db(self) -> None:
        """Initialize database schema."""
        cursor = self.conn.cursor()
        
        # Aliases table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aliases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                command TEXT NOT NULL,
                description TEXT DEFAULT '',
                tags TEXT DEFAULT '[]',
                shell TEXT DEFAULT 'all',
                group_name TEXT DEFAULT 'default',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                is_active INTEGER DEFAULT 1
            )
        """)
        
        # Usage statistics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usage_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alias_id INTEGER NOT NULL,
                used_at TEXT NOT NULL,
                FOREIGN KEY (alias_id) REFERENCES aliases(id)
            )
        """)
        
        # Backups table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_aliases_name ON aliases(name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_aliases_group ON aliases(group_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_usage_alias ON usage_stats(alias_id)")
        
        self.conn.commit()
    
    def close(self) -> None:
        """Close database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None
    
    # ==================== Alias Operations ====================
    
    def add_alias(
        self,
        name: str,
        command: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        shell: str = "all",
        group: str = "default"
    ) -> int:
        """Add a new alias.
        
        Args:
            name: Alias name
            command: Command to execute
            description: Optional description
            tags: Optional list of tags
            shell: Target shell (bash/zsh/fish/all)
            group: Group name for organization
            
        Returns:
            ID of the newly created alias
        """
        now = datetime.now().isoformat()
        tags_json = json.dumps(tags or [])
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO aliases (name, command, description, tags, shell, group_name, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, command, description, tags_json, shell, group, now, now))
        
        self.conn.commit()
        self._create_backup("auto", f"Added alias: {name}")
        return cursor.lastrowid
    
    def get_alias(self, name: str) -> Optional[Dict[str, Any]]:
        """Get alias by name.
        
        Args:
            name: Alias name
            
        Returns:
            Alias dict or None if not found
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM aliases WHERE name = ? AND is_active = 1", (name,))
        row = cursor.fetchone()
        
        if row:
            return self._row_to_dict(row)
        return None
    
    def get_all_aliases(
        self,
        group: Optional[str] = None,
        shell: Optional[str] = None,
        tag: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all aliases with optional filters.
        
        Args:
            group: Filter by group
            shell: Filter by shell
            tag: Filter by tag
            
        Returns:
            List of alias dicts
        """
        cursor = self.conn.cursor()
        query = "SELECT * FROM aliases WHERE is_active = 1"
        params = []
        
        if group:
            query += " AND group_name = ?"
            params.append(group)
        
        if shell and shell != "all":
            query += " AND (shell = ? OR shell = 'all')"
            params.append(shell)
        
        query += " ORDER BY name"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        aliases = [self._row_to_dict(row) for row in rows]
        
        # Filter by tag if specified
        if tag:
            aliases = [a for a in aliases if tag in a.get("tags", [])]
        
        return aliases
    
    def update_alias(
        self,
        name: str,
        command: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        shell: Optional[str] = None,
        group: Optional[str] = None
    ) -> bool:
        """Update an existing alias.
        
        Args:
            name: Alias name to update
            command: New command (optional)
            description: New description (optional)
            tags: New tags (optional)
            shell: New shell target (optional)
            group: New group (optional)
            
        Returns:
            True if updated, False if not found
        """
        alias = self.get_alias(name)
        if not alias:
            return False
        
        updates = []
        params = []
        
        if command is not None:
            updates.append("command = ?")
            params.append(command)
        
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        
        if tags is not None:
            updates.append("tags = ?")
            params.append(json.dumps(tags))
        
        if shell is not None:
            updates.append("shell = ?")
            params.append(shell)
        
        if group is not None:
            updates.append("group_name = ?")
            params.append(group)
        
        if not updates:
            return True
        
        updates.append("updated_at = ?")
        params.append(datetime.now().isoformat())
        params.append(name)
        
        cursor = self.conn.cursor()
        cursor.execute(
            f"UPDATE aliases SET {', '.join(updates)} WHERE name = ?",
            params
        )
        
        self.conn.commit()
        self._create_backup("auto", f"Updated alias: {name}")
        return True
    
    def delete_alias(self, name: str) -> bool:
        """Delete an alias (soft delete).
        
        Args:
            name: Alias name to delete
            
        Returns:
            True if deleted, False if not found
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE aliases SET is_active = 0, updated_at = ? WHERE name = ?",
            (datetime.now().isoformat(), name)
        )
        
        if cursor.rowcount > 0:
            self.conn.commit()
            self._create_backup("auto", f"Deleted alias: {name}")
            return True
        return False
    
    def search_aliases(self, query: str) -> List[Dict[str, Any]]:
        """Search aliases by name, command, or description.
        
        Args:
            query: Search query
            
        Returns:
            List of matching aliases
        """
        cursor = self.conn.cursor()
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT * FROM aliases 
            WHERE is_active = 1 
            AND (name LIKE ? OR command LIKE ? OR description LIKE ?)
            ORDER BY name
        """, (search_pattern, search_pattern, search_pattern))
        
        return [self._row_to_dict(row) for row in cursor.fetchall()]
    
    # ==================== Statistics Operations ====================
    
    def record_usage(self, alias_name: str) -> None:
        """Record alias usage.
        
        Args:
            alias_name: Name of the alias used
        """
        alias = self.get_alias(alias_name)
        if not alias:
            return
        
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO usage_stats (alias_id, used_at) VALUES (?, ?)",
            (alias["id"], datetime.now().isoformat())
        )
        self.conn.commit()
    
    def get_usage_stats(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get usage statistics for the past N days.
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of stats dicts with alias info and usage count
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT a.name, a.command, COUNT(u.id) as usage_count
            FROM aliases a
            LEFT JOIN usage_stats u ON a.id = u.alias_id
                AND u.used_at >= datetime('now', ?)
            WHERE a.is_active = 1
            GROUP BY a.id
            ORDER BY usage_count DESC
        """, (f"-{days} days",))
        
        return [
            {"name": row[0], "command": row[1], "usage_count": row[2]}
            for row in cursor.fetchall()
        ]
    
    # ==================== Backup Operations ====================
    
    def _create_backup(self, backup_type: str, description: str = "") -> int:
        """Create a backup of current aliases.
        
        Args:
            backup_type: Type of backup (auto/manual)
            description: Backup description
            
        Returns:
            Backup ID
        """
        aliases = self.get_all_aliases()
        content = json.dumps(aliases, ensure_ascii=False, indent=2)
        
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO backups (name, content, created_at) VALUES (?, ?, ?)",
            (f"{backup_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}", content, datetime.now().isoformat())
        )
        
        self.conn.commit()
        return cursor.lastrowid
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all backups.
        
        Returns:
            List of backup dicts
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, created_at FROM backups ORDER BY created_at DESC LIMIT 20")
        
        return [
            {"id": row[0], "name": row[1], "created_at": row[2]}
            for row in cursor.fetchall()
        ]
    
    def restore_backup(self, backup_id: int) -> bool:
        """Restore from a backup.
        
        Args:
            backup_id: ID of the backup to restore
            
        Returns:
            True if restored successfully
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT content FROM backups WHERE id = ?", (backup_id,))
        row = cursor.fetchone()
        
        if not row:
            return False
        
        aliases = json.loads(row[0])
        
        # Clear current aliases
        cursor.execute("UPDATE aliases SET is_active = 0")
        
        # Restore aliases
        for alias in aliases:
            self.add_alias(
                name=alias["name"],
                command=alias["command"],
                description=alias.get("description", ""),
                tags=alias.get("tags", []),
                shell=alias.get("shell", "all"),
                group=alias.get("group_name", "default")
            )
        
        self.conn.commit()
        return True
    
    # ==================== Import/Export ====================
    
    def export_aliases(self, format: str = "yaml") -> str:
        """Export aliases to YAML or JSON format.
        
        Args:
            format: Export format (yaml/json)
            
        Returns:
            Exported content string
        """
        aliases = self.get_all_aliases()
        
        if format == "json":
            return json.dumps({"aliases": aliases}, ensure_ascii=False, indent=2)
        else:
            # YAML format
            lines = ["# AliasForge Export", f"# Generated: {datetime.now().isoformat()}", ""]
            
            for alias in aliases:
                lines.append(f"- name: {alias['name']}")
                lines.append(f"  command: {alias['command']}")
                if alias.get("description"):
                    lines.append(f"  description: {alias['description']}")
                if alias.get("tags"):
                    lines.append(f"  tags: {alias['tags']}")
                if alias.get("shell") and alias["shell"] != "all":
                    lines.append(f"  shell: {alias['shell']}")
                if alias.get("group_name") and alias["group_name"] != "default":
                    lines.append(f"  group: {alias['group_name']}")
                lines.append("")
            
            return "\n".join(lines)
    
    def import_aliases(self, content: str, format: str = "yaml") -> int:
        """Import aliases from YAML or JSON content.
        
        Args:
            content: Content to import
            format: Import format (yaml/json)
            
        Returns:
            Number of aliases imported
        """
        if format == "json":
            data = json.loads(content)
            aliases = data.get("aliases", [])
        else:
            # Simple YAML parsing
            aliases = self._parse_yaml_aliases(content)
        
        count = 0
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()
        
        for alias in aliases:
            # Support both 'group' and 'group_name' keys
            group = alias.get("group") or alias.get("group_name", "default")
            name = alias["name"]
            command = alias["command"]
            description = alias.get("description", "")
            tags_json = json.dumps(alias.get("tags", []))
            shell = alias.get("shell", "all")
            
            # Use INSERT OR REPLACE to handle both new and existing (including soft-deleted)
            cursor.execute("""
                INSERT OR REPLACE INTO aliases 
                (name, command, description, tags, shell, group_name, created_at, updated_at, is_active)
                VALUES (?, ?, ?, ?, ?, ?, 
                    COALESCE((SELECT created_at FROM aliases WHERE name = ?), ?),
                    ?,
                    1
                    )
            """, (name, command, description, tags_json, shell, group, name, now, now))
            count += 1
        
        self.conn.commit()
        self._create_backup("auto", f"Imported {count} aliases")
        return count
    
    def _parse_yaml_aliases(self, content: str) -> List[Dict[str, Any]]:
        """Parse YAML content into aliases list."""
        aliases = []
        current = {}
        
        for line in content.split("\n"):
            line = line.rstrip()
            if not line or line.startswith("#"):
                continue
            
            if line.startswith("- name:"):
                if current:
                    aliases.append(current)
                current = {"name": line.split(":", 1)[1].strip()}
            elif line.startswith("  command:"):
                current["command"] = line.split(":", 1)[1].strip()
            elif line.startswith("  description:"):
                current["description"] = line.split(":", 1)[1].strip()
            elif line.startswith("  tags:"):
                tags_str = line.split(":", 1)[1].strip()
                current["tags"] = [t.strip() for t in tags_str.strip("[]").split(",") if t.strip()]
            elif line.startswith("  shell:"):
                current["shell"] = line.split(":", 1)[1].strip()
            elif line.startswith("  group:"):
                current["group"] = line.split(":", 1)[1].strip()
        
        if current:
            aliases.append(current)
        
        return aliases
    
    # ==================== Groups ====================
    
    def get_groups(self) -> List[str]:
        """Get all group names.
        
        Returns:
            List of group names
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT group_name FROM aliases WHERE is_active = 1 ORDER BY group_name")
        return [row[0] for row in cursor.fetchall()]
    
    # ==================== Helpers ====================
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Convert database row to dict."""
        return {
            "id": row["id"],
            "name": row["name"],
            "command": row["command"],
            "description": row["description"],
            "tags": json.loads(row["tags"]),
            "shell": row["shell"],
            "group_name": row["group_name"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "is_active": row["is_active"]
        }
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
