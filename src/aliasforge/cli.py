"""
AliasForge CLI - Main entry point.
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

from aliasforge import __version__
from aliasforge.core.database import Database
from aliasforge.core.alias_manager import AliasManager
from aliasforge.core.stats import StatsManager

console = Console()


def print_version(ctx, param, value):
    """Print version and exit."""
    if not value or ctx.resilient_parsing:
        return
    console.print(f"[bold cyan]AliasForge[/] version [green]{__version__}[/]")
    ctx.exit()


@click.group()
@click.option("--version", "-v", is_flag=True, callback=print_version, expose_value=False, is_eager=True,
              help="Show version and exit.")
@click.pass_context
def cli(ctx):
    """
    ⚡ AliasForge - Lightweight Terminal Command Alias Intelligent Manager
    
    A powerful CLI tool for managing shell aliases with intelligent features.
    
    \b
    Examples:
        af add gs "git status" --desc "Show git status"
        af list
        af search git
        af sync
    """
    ctx.ensure_object(dict)
    ctx.obj["db"] = Database()
    ctx.obj["manager"] = AliasManager(ctx.obj["db"])
    ctx.obj["stats"] = StatsManager(ctx.obj["db"])


# ==================== Add Command ====================
@cli.command()
@click.argument("name")
@click.argument("command")
@click.option("--desc", "-d", default="", help="Alias description.")
@click.option("--tag", "-t", multiple=True, help="Tags for the alias (can be used multiple times).")
@click.option("--shell", "-s", default="all", type=click.Choice(["bash", "zsh", "fish", "all"]),
              help="Target shell.")
@click.option("--group", "-g", default="default", help="Group name for organization.")
@click.pass_context
def add(ctx, name, command, desc, tag, shell, group):
    """
    ➕ Add a new alias.
    
    \b
    Examples:
        af add gs "git status"
        af add ll "ls -la" --desc "List all files with details"
        af add gp "git push" --tag git --tag push
    """
    manager = ctx.obj["manager"]
    
    try:
        alias = manager.add(
            name=name,
            command=command,
            description=desc,
            tags=list(tag) if tag else None,
            shell=shell,
            group=group
        )
        
        console.print(Panel(
            f"[green]✓[/] Alias [cyan]{name}[/] added successfully!\n\n"
            f"  [dim]Command:[/] {command}\n"
            f"  [dim]Shell:[/] {shell}\n"
            f"  [dim]Group:[/] {group}",
            title="Alias Added",
            border_style="green"
        ))
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")


# ==================== List Command ====================
@cli.command("list")
@click.option("--group", "-g", default=None, help="Filter by group.")
@click.option("--shell", "-s", default=None, type=click.Choice(["bash", "zsh", "fish", "all"]),
              help="Filter by shell.")
@click.option("--tag", "-t", default=None, help="Filter by tag.")
@click.option("--all", "-a", "show_all", is_flag=True, help="Show all details including description.")
@click.pass_context
def list_aliases(ctx, group, shell, tag, show_all):
    """
    📋 List all aliases.
    
    \b
    Examples:
        af list
        af list --group git
        af list --tag docker
    """
    manager = ctx.obj["manager"]
    aliases = manager.list(group=group, shell=shell, tag=tag)
    
    if not aliases:
        console.print("[yellow]No aliases found.[/]")
        return
    
    table = Table(title=f"📋 Aliases ({len(aliases)} total)", show_header=True, header_style="bold cyan")
    table.add_column("Name", style="green")
    table.add_column("Command", style="white")
    
    if show_all:
        table.add_column("Description", style="dim")
        table.add_column("Tags", style="yellow")
        table.add_column("Shell", style="blue")
        table.add_column("Group", style="magenta")
    
    for alias in aliases:
        if show_all:
            table.add_row(
                alias["name"],
                alias["command"][:40] + ("..." if len(alias["command"]) > 40 else ""),
                alias.get("description", "")[:30],
                ", ".join(alias.get("tags", [])),
                alias.get("shell", "all"),
                alias.get("group_name", "default")
            )
        else:
            table.add_row(
                alias["name"],
                alias["command"][:50] + ("..." if len(alias["command"]) > 50 else "")
            )
    
    console.print(table)


# ==================== Show Command ====================
@cli.command()
@click.argument("name")
@click.pass_context
def show(ctx, name):
    """
    🔍 Show alias details.
    
    \b
    Examples:
        af show gs
    """
    manager = ctx.obj["manager"]
    alias = manager.get(name)
    
    if not alias:
        console.print(f"[red]Error:[/] Alias [cyan]{name}[/] not found.")
        return
    
    panel_content = f"""
[bold]Name:[/] [cyan]{alias['name']}[/]
[bold]Command:[/] [green]{alias['command']}[/]
[bold]Description:[/] {alias.get('description', '[dim]No description[/]')}
[bold]Tags:[/] {', '.join(alias.get('tags', [])) or '[dim]None[/]'}
[bold]Shell:[/] [blue]{alias.get('shell', 'all')}[/]
[bold]Group:[/] [magenta]{alias.get('group_name', 'default')}[/]
[bold]Created:[/] [dim]{alias.get('created_at', 'N/A')}[/]
[bold]Updated:[/] [dim]{alias.get('updated_at', 'N/A')}[/]
"""
    
    console.print(Panel(panel_content.strip(), title=f"🔍 Alias: {name}", border_style="cyan"))


# ==================== Edit Command ====================
@cli.command()
@click.argument("name")
@click.option("--command", "-c", default=None, help="New command.")
@click.option("--desc", "-d", default=None, help="New description.")
@click.option("--tag", "-t", multiple=True, help="New tags (replaces existing).")
@click.option("--shell", "-s", default=None, type=click.Choice(["bash", "zsh", "fish", "all"]),
              help="New shell target.")
@click.option("--group", "-g", default=None, help="New group.")
@click.pass_context
def edit(ctx, name, command, desc, tag, shell, group):
    """
    ✏️ Edit an existing alias.
    
    \b
    Examples:
        af edit gs --command "git status -s"
        af edit ll --desc "List files with details"
    """
    manager = ctx.obj["manager"]
    
    if not manager.get(name):
        console.print(f"[red]Error:[/] Alias [cyan]{name}[/] not found.")
        return
    
    success = manager.update(
        name=name,
        command=command,
        description=desc,
        tags=list(tag) if tag else None,
        shell=shell,
        group=group
    )
    
    if success:
        console.print(f"[green]✓[/] Alias [cyan]{name}[/] updated successfully!")
    else:
        console.print(f"[red]Error:[/] Failed to update alias.")


# ==================== Delete Command ====================
@cli.command()
@click.argument("name")
@click.option("--force", "-f", is_flag=True, help="Skip confirmation.")
@click.pass_context
def delete(ctx, name, force):
    """
    🗑️ Delete an alias.
    
    \b
    Examples:
        af delete gs
        af delete gs --force
    """
    manager = ctx.obj["manager"]
    
    if not manager.get(name):
        console.print(f"[red]Error:[/] Alias [cyan]{name}[/] not found.")
        return
    
    if not force:
        if not click.confirm(f"Delete alias '{name}'?", default=False):
            console.print("[yellow]Cancelled.[/]")
            return
    
    success = manager.delete(name)
    
    if success:
        console.print(f"[green]✓[/] Alias [cyan]{name}[/] deleted successfully!")
    else:
        console.print(f"[red]Error:[/] Failed to delete alias.")


# ==================== Search Command ====================
@cli.command()
@click.argument("query")
@click.pass_context
def search(ctx, query):
    """
    🔎 Search aliases.
    
    \b
    Examples:
        af search git
        af search docker
    """
    manager = ctx.obj["manager"]
    results = manager.search(query)
    
    if not results:
        console.print(f"[yellow]No results found for '[cyan]{query}[/]'.[/]")
        return
    
    table = Table(title=f"🔎 Search Results for '{query}'", show_header=True, header_style="bold cyan")
    table.add_column("Name", style="green")
    table.add_column("Command", style="white")
    table.add_column("Description", style="dim")
    
    for alias in results:
        table.add_row(
            alias["name"],
            alias["command"][:40] + ("..." if len(alias["command"]) > 40 else ""),
            alias.get("description", "")[:30]
        )
    
    console.print(table)


# ==================== Sync Command ====================
@cli.command()
@click.option("--shell", "-s", default=None, type=click.Choice(["bash", "zsh", "fish"]),
              help="Target shell (default: auto-detect).")
@click.pass_context
def sync(ctx, shell):
    """
    🔄 Sync aliases to shell config.
    
    This command writes all aliases to your shell configuration file.
    
    \b
    Examples:
        af sync
        af sync --shell zsh
    """
    manager = ctx.obj["manager"]
    shell = shell or manager.detect_current_shell()
    
    try:
        manager.sync_to_shell(shell)
        config_path = manager.get_shell_config_path(shell)
        
        console.print(Panel(
            f"[green]✓[/] Aliases synced to [cyan]{shell}[/] config!\n\n"
            f"  [dim]Config file:[/] {config_path}\n\n"
            f"  [dim]Run this to apply:[/] [yellow]source {config_path}[/]",
            title="Sync Complete",
            border_style="green"
        ))
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")


# ==================== Export Command ====================
@cli.command()
@click.argument("file", type=click.Path(), default="aliases.yaml")
@click.option("--format", "-f", "fmt", default="yaml", type=click.Choice(["yaml", "json"]),
              help="Export format.")
@click.pass_context
def export(ctx, file, fmt):
    """
    📤 Export aliases to file.
    
    \b
    Examples:
        af export aliases.yaml
        af export aliases.json --format json
    """
    from pathlib import Path
    
    manager = ctx.obj["manager"]
    file_path = Path(file)
    
    # Adjust extension if needed
    if fmt == "json" and not file_path.suffix:
        file_path = file_path.with_suffix(".json")
    elif fmt == "yaml" and not file_path.suffix:
        file_path = file_path.with_suffix(".yaml")
    
    success = manager.export_to_file(file_path, fmt)
    
    if success:
        console.print(f"[green]✓[/] Exported aliases to [cyan]{file_path}[/]")
    else:
        console.print(f"[red]Error:[/] Failed to export.")


# ==================== Import Command ====================
@cli.command("import")
@click.argument("file", type=click.Path(exists=True))
@click.pass_context
def import_aliases(ctx, file):
    """
    📥 Import aliases from file.
    
    Supports both YAML and JSON formats (auto-detected by file extension).
    
    \b
    Examples:
        af import aliases.yaml
        af import aliases.json
    """
    from pathlib import Path
    
    manager = ctx.obj["manager"]
    file_path = Path(file)
    
    count = manager.import_from_file(file_path)
    
    console.print(f"[green]✓[/] Imported [cyan]{count}[/] aliases from [cyan]{file_path}[/]")


# ==================== Groups Command ====================
@cli.command()
@click.pass_context
def groups(ctx):
    """
    📁 List all groups.
    
    \b
    Examples:
        af groups
    """
    manager = ctx.obj["manager"]
    groups_list = manager.get_groups()
    
    if not groups_list:
        console.print("[yellow]No groups found.[/]")
        return
    
    table = Table(title="📁 Groups", show_header=True, header_style="bold cyan")
    table.add_column("Group Name", style="green")
    table.add_column("Alias Count", style="white")
    
    for group in groups_list:
        count = len(manager.list(group=group))
        table.add_row(group, str(count))
    
    console.print(table)


# ==================== Tags Command ====================
@cli.command()
@click.pass_context
def tags(ctx):
    """
    🏷️ List all tags.
    
    \b
    Examples:
        af tags
    """
    manager = ctx.obj["manager"]
    tags_list = manager.get_tags()
    
    if not tags_list:
        console.print("[yellow]No tags found.[/]")
        return
    
    console.print(Panel(
        " ".join(f"[yellow]{t}[/]" for t in tags_list),
        title="🏷️ Tags",
        border_style="yellow"
    ))


# ==================== Stats Command ====================
@cli.command()
@click.option("--days", "-d", default=30, help="Number of days to analyze.")
@click.pass_context
def stats(ctx, days):
    """
    📊 Show usage statistics.
    
    \b
    Examples:
        af stats
        af stats --days 7
    """
    stats_manager = ctx.obj["stats"]
    summary = stats_manager.get_summary(days)
    
    panel_content = f"""
[bold]Period:[/] Last {summary['period_days']} days
[bold]Total Usage:[/] [green]{summary['total_usage']}[/]
[bold]Unique Aliases Used:[/] [cyan]{summary['unique_aliases_used']}[/]
[bold]Total Aliases:[/] [magenta]{summary['total_aliases']}[/]

[bold]Top 5 Used Aliases:[/]
"""
    
    for i, alias in enumerate(summary["top_aliases"], 1):
        panel_content += f"\n  {i}. [cyan]{alias['name']}[/] - [green]{alias['usage_count']}[/] uses"
    
    console.print(Panel(panel_content.strip(), title="📊 Usage Statistics", border_style="blue"))


# ==================== Backup Command ====================
@cli.group()
@click.pass_context
def backup(ctx):
    """
    💾 Backup management.
    
    \b
    Examples:
        af backup create
        af backup list
        af backup restore 1
    """
    pass


@backup.command("create")
@click.option("--desc", "-d", default="", help="Backup description.")
@click.pass_context
def create_backup(ctx, desc):
    """Create a manual backup."""
    manager = ctx.obj["manager"]
    backup_id = manager.create_backup(desc)
    console.print(f"[green]✓[/] Backup created with ID: [cyan]{backup_id}[/]")


@backup.command("list")
@click.pass_context
def list_backups(ctx):
    """List all backups."""
    manager = ctx.obj["manager"]
    backups = manager.list_backups()
    
    if not backups:
        console.print("[yellow]No backups found.[/]")
        return
    
    table = Table(title="💾 Backups", show_header=True, header_style="bold cyan")
    table.add_column("ID", style="green")
    table.add_column("Name", style="white")
    table.add_column("Created At", style="dim")
    
    for backup in backups:
        table.add_row(str(backup["id"]), backup["name"], backup["created_at"])
    
    console.print(table)


@backup.command("restore")
@click.argument("backup_id", type=int)
@click.option("--force", "-f", is_flag=True, help="Skip confirmation.")
@click.pass_context
def restore_backup(ctx, backup_id, force):
    """Restore from a backup."""
    manager = ctx.obj["manager"]
    
    if not force:
        if not click.confirm(f"Restore from backup #{backup_id}? This will replace all current aliases.", default=False):
            console.print("[yellow]Cancelled.[/]")
            return
    
    success = manager.restore_backup(backup_id)
    
    if success:
        console.print(f"[green]✓[/] Restored from backup [cyan]#{backup_id}[/]")
    else:
        console.print(f"[red]Error:[/] Backup not found or restore failed.")


# ==================== Suggest Command ====================
@cli.command()
@click.option("--min-count", "-m", default=3, help="Minimum occurrence count to suggest.")
@click.pass_context
def suggest(ctx, min_count):
    """
    💡 Suggest aliases from command history.
    
    Analyzes your shell history to find frequently used commands
    that could benefit from aliases.
    
    \b
    Examples:
        af suggest
        af suggest --min-count 5
    """
    from pathlib import Path
    
    manager = ctx.obj["manager"]
    
    # Try to read shell history
    shell = manager.detect_current_shell()
    history_paths = {
        "bash": Path.home() / ".bash_history",
        "zsh": Path.home() / ".zsh_history",
        "fish": Path.home() / ".local/share/fish/fish_history"
    }
    
    history_path = history_paths.get(shell)
    
    if not history_path or not history_path.exists():
        console.print(f"[yellow]Warning:[/] Could not find history file for {shell}")
        console.print("[dim]Supported shells: bash, zsh, fish[/]")
        return
    
    try:
        history_content = history_path.read_text()
        history_lines = history_content.split("\n")
        
        suggestions = manager.suggest_from_history(history_lines, min_count)
        
        if not suggestions:
            console.print("[yellow]No suggestions found. Try lowering --min-count.[/]")
            return
        
        table = Table(title="💡 Suggested Aliases", show_header=True, header_style="bold cyan")
        table.add_column("Suggested Name", style="green")
        table.add_column("Command", style="white")
        table.add_column("Usage Count", style="yellow")
        table.add_column("Reason", style="dim")
        
        for s in suggestions:
            table.add_row(
                s["suggested_name"],
                s["command"],
                str(s["usage_count"]),
                s["reason"]
            )
        
        console.print(table)
        console.print("\n[dim]Use 'af add <name> <command>' to create an alias.[/]")
        
    except Exception as e:
        console.print(f"[red]Error reading history:[/] {e}")


def main():
    """Main entry point."""
    cli(obj={})


if __name__ == "__main__":
    main()
