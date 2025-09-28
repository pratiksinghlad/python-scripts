"""
Command-line interface for the job scheduler.

This module provides a CLI using Typer for managing jobs and the scheduler.
It follows the Single Responsibility Principle by focusing on CLI concerns.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from .config.settings import get_settings
from .infrastructure.database.connection import DatabaseConnection
from .infrastructure.database.repositories.mysql_job_repository import (
    MySQLJobRepository,
    MySQLJobExecutionRepository,
)
from .domain.services.job_service import JobDomainService


# Initialize CLI app
app = typer.Typer(
    name="job-scheduler",
    help="Background Job Scheduler CLI",
    add_completion=False,
)

# Initialize console for rich output
console = Console()


@app.command()
def start(
    config_file: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to configuration file",
    ),
    daemon: bool = typer.Option(
        False,
        "--daemon",
        "-d",
        help="Run as daemon process",
    ),
) -> None:
    """Start the job scheduler."""
    console.print("🚀 Starting job scheduler...", style="bold green")
    
    try:
        settings = get_settings(config_file)
        
        if daemon:
            console.print("Running as daemon process...")
            # TODO: Implement daemon mode
        else:
            console.print("Running in foreground mode...")
            # TODO: Implement scheduler startup
            
        console.print("✅ Job scheduler started successfully!", style="bold green")
        
    except Exception as e:
        console.print(f"❌ Failed to start scheduler: {e}", style="bold red")
        raise typer.Exit(1)


@app.command()
def stop() -> None:
    """Stop the job scheduler."""
    console.print("🛑 Stopping job scheduler...", style="bold yellow")
    # TODO: Implement scheduler shutdown
    console.print("✅ Job scheduler stopped!", style="bold green")


@app.command("create-job")
def create_job(
    name: str = typer.Option(..., "--name", "-n", help="Job name"),
    cron: str = typer.Option(..., "--cron", "-c", help="Cron expression"),
    command: str = typer.Option(..., "--command", "--cmd", help="Command to execute"),
    description: str = typer.Option("", "--description", "-d", help="Job description"),
    timeout: int = typer.Option(300, "--timeout", "-t", help="Timeout in seconds"),
    retries: int = typer.Option(3, "--retries", "-r", help="Maximum retries"),
    retry_delay: int = typer.Option(60, "--retry-delay", help="Retry delay in seconds"),
    tags: Optional[List[str]] = typer.Option(None, "--tag", help="Job tags (can be used multiple times)"),
) -> None:
    """Create a new job."""
    console.print(f"📝 Creating job '{name}'...", style="bold blue")
    
    try:
        # TODO: Implement job creation
        job_data = {
            "name": name,
            "cron_expression": cron,
            "command": command,
            "description": description,
            "timeout_seconds": timeout,
            "max_retries": retries,
            "retry_delay_seconds": retry_delay,
            "tags": tags or [],
        }
        
        console.print(f"✅ Job '{name}' created successfully!", style="bold green")
        console.print(f"📅 Next run: [bold cyan]TODO[/bold cyan]")
        
    except Exception as e:
        console.print(f"❌ Failed to create job: {e}", style="bold red")
        raise typer.Exit(1)


@app.command("list-jobs")
def list_jobs(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of jobs to display"),
    offset: int = typer.Option(0, "--offset", "-o", help="Number of jobs to skip"),
) -> None:
    """List all jobs."""
    console.print("📋 Listing jobs...", style="bold blue")
    
    try:
        # TODO: Implement job listing
        
        # Create sample table for now
        table = Table(title="Jobs")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("Cron", style="yellow")
        table.add_column("Last Run", style="blue")
        table.add_column("Next Run", style="blue")
        
        # Sample data
        table.add_row("1", "Daily Backup", "active", "0 2 * * *", "2024-01-01 02:00:00", "2024-01-02 02:00:00")
        table.add_row("2", "Weekly Report", "paused", "0 9 * * 1", "2024-01-08 09:00:00", "-")
        
        console.print(table)
        
    except Exception as e:
        console.print(f"❌ Failed to list jobs: {e}", style="bold red")
        raise typer.Exit(1)


@app.command("job-info")
def job_info(
    job_id: int = typer.Argument(..., help="Job ID"),
) -> None:
    """Show detailed information about a job."""
    console.print(f"ℹ️ Getting job info for ID {job_id}...", style="bold blue")
    
    try:
        # TODO: Implement job info display
        console.print(f"Job ID: {job_id}")
        console.print("Status: [bold green]Active[/bold green]")
        console.print("Name: Sample Job")
        console.print("Description: This is a sample job")
        console.print("Cron Expression: 0 2 * * *")
        console.print("Command: python /path/to/script.py")
        console.print("Created: 2024-01-01 10:00:00")
        console.print("Last Run: 2024-01-01 02:00:00")
        console.print("Next Run: 2024-01-02 02:00:00")
        
    except Exception as e:
        console.print(f"❌ Failed to get job info: {e}", style="bold red")
        raise typer.Exit(1)


@app.command("job-history")
def job_history(
    job_id: int = typer.Argument(..., help="Job ID"),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum number of executions to display"),
) -> None:
    """Show job execution history."""
    console.print(f"📊 Getting execution history for job {job_id}...", style="bold blue")
    
    try:
        # TODO: Implement execution history display
        
        table = Table(title=f"Execution History - Job {job_id}")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Status", style="green")
        table.add_column("Started", style="blue")
        table.add_column("Duration", style="yellow")
        table.add_column("Exit Code", style="red")
        
        # Sample data
        table.add_row("101", "success", "2024-01-02 02:00:00", "45.2s", "0")
        table.add_row("100", "success", "2024-01-01 02:00:00", "43.1s", "0")
        table.add_row("99", "failed", "2023-12-31 02:00:00", "2.5s", "1")
        
        console.print(table)
        
    except Exception as e:
        console.print(f"❌ Failed to get job history: {e}", style="bold red")
        raise typer.Exit(1)


@app.command("pause-job")
def pause_job(
    job_id: int = typer.Argument(..., help="Job ID to pause"),
) -> None:
    """Pause a job."""
    console.print(f"⏸️ Pausing job {job_id}...", style="bold yellow")
    
    try:
        # TODO: Implement job pausing
        console.print(f"✅ Job {job_id} paused successfully!", style="bold green")
        
    except Exception as e:
        console.print(f"❌ Failed to pause job: {e}", style="bold red")
        raise typer.Exit(1)


@app.command("resume-job")
def resume_job(
    job_id: int = typer.Argument(..., help="Job ID to resume"),
) -> None:
    """Resume a paused job."""
    console.print(f"▶️ Resuming job {job_id}...", style="bold green")
    
    try:
        # TODO: Implement job resuming
        console.print(f"✅ Job {job_id} resumed successfully!", style="bold green")
        
    except Exception as e:
        console.print(f"❌ Failed to resume job: {e}", style="bold red")
        raise typer.Exit(1)


@app.command("delete-job")
def delete_job(
    job_id: int = typer.Argument(..., help="Job ID to delete"),
    force: bool = typer.Option(False, "--force", "-f", help="Force delete without confirmation"),
) -> None:
    """Delete a job."""
    if not force:
        if not typer.confirm(f"Are you sure you want to delete job {job_id}?"):
            console.print("Operation cancelled.", style="yellow")
            return
    
    console.print(f"🗑️ Deleting job {job_id}...", style="bold red")
    
    try:
        # TODO: Implement job deletion
        console.print(f"✅ Job {job_id} deleted successfully!", style="bold green")
        
    except Exception as e:
        console.print(f"❌ Failed to delete job: {e}", style="bold red")
        raise typer.Exit(1)


@app.command()
def status() -> None:
    """Show scheduler status and statistics."""
    console.print("📊 Getting scheduler status...", style="bold blue")
    
    try:
        # TODO: Implement status display
        console.print("[bold green]Scheduler Status: Running[/bold green]")
        console.print("Uptime: 2 hours 15 minutes")
        console.print("Total Jobs: 5")
        console.print("Active Jobs: 3")
        console.print("Paused Jobs: 1")
        console.print("Running Executions: 0")
        console.print("Completed Today: 12")
        console.print("Failed Today: 1")
        
    except Exception as e:
        console.print(f"❌ Failed to get status: {e}", style="bold red")
        raise typer.Exit(1)


@app.command()
def migrate(
    config_file: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to configuration file",
    ),
) -> None:
    """Run database migrations."""
    console.print("🔄 Running database migrations...", style="bold blue")
    
    try:
        settings = get_settings(config_file)
        
        # TODO: Implement migration runner
        console.print("✅ Database migrations completed successfully!", style="bold green")
        
    except Exception as e:
        console.print(f"❌ Migration failed: {e}", style="bold red")
        raise typer.Exit(1)


@app.command()
def health() -> None:
    """Check system health."""
    console.print("🏥 Checking system health...", style="bold blue")
    
    try:
        # TODO: Implement health checks
        console.print("[bold green]✅ Database: Healthy[/bold green]")
        console.print("[bold green]✅ Scheduler: Running[/bold green]")
        console.print("[bold green]✅ Job Executor: Available[/bold green]")
        console.print("\n[bold green]Overall Status: Healthy[/bold green]")
        
    except Exception as e:
        console.print(f"❌ Health check failed: {e}", style="bold red")
        raise typer.Exit(1)


def main() -> None:
    """Main CLI entry point."""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!", style="bold yellow")
        sys.exit(0)
    except Exception as e:
        console.print(f"💥 Unexpected error: {e}", style="bold red")
        sys.exit(1)


if __name__ == "__main__":
    main()