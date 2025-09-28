#!/usr/bin/env python3
"""
Startup script for the job scheduler.

This script demonstrates how to initialize and start the scheduler
with proper dependency injection following SOLID principles.
"""

import asyncio
import signal
import sys
from pathlib import Path

# Add src to Python path for development
sys.path.insert(0, str(Path(__file__).parent / "src"))

from background_job_scheduler.config.settings import get_settings
from background_job_scheduler.infrastructure.database.connection import DatabaseConnection
from background_job_scheduler.infrastructure.database.repositories.mysql_job_repository import (
    MySQLJobRepository,
    MySQLJobExecutionRepository,
)
from background_job_scheduler.domain.services.job_service import JobDomainService


class JobSchedulerApp:
    """
    Main application class that orchestrates the job scheduler.
    
    This class follows the Dependency Inversion Principle by depending
    on abstractions rather than concrete implementations.
    """
    
    def __init__(self) -> None:
        """Initialize the application."""
        self.settings = get_settings()
        self.db_connection: DatabaseConnection | None = None
        self.job_service: JobDomainService | None = None
        self._running = False
    
    async def initialize(self) -> None:
        """Initialize application dependencies."""
        print("🔧 Initializing job scheduler...")
        
        # Initialize database connection
        self.db_connection = DatabaseConnection(self.settings.database)
        await self.db_connection.initialize()
        
        # Initialize repositories
        job_repository = MySQLJobRepository(self.db_connection)
        execution_repository = MySQLJobExecutionRepository(self.db_connection)
        
        # Initialize domain service
        self.job_service = JobDomainService(job_repository, execution_repository)
        
        print("✅ Job scheduler initialized successfully!")
    
    async def start(self) -> None:
        """Start the job scheduler."""
        await self.initialize()
        
        print("🚀 Starting job scheduler...")
        self._running = True
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Main scheduler loop
        try:
            while self._running:
                await self._scheduler_tick()
                await asyncio.sleep(self.settings.app.scheduler_interval)
        
        except KeyboardInterrupt:
            print("\n⚠️ Received interrupt signal")
        finally:
            await self.shutdown()
    
    async def _scheduler_tick(self) -> None:
        """Execute one scheduler iteration."""
        try:
            print("⏰ Checking for due jobs...")
            
            # Get jobs due for execution
            if self.job_service:
                due_jobs = await self.job_service.get_jobs_due_for_execution()
                
                if due_jobs:
                    print(f"📋 Found {len(due_jobs)} job(s) due for execution")
                    
                    for job in due_jobs:
                        print(f"🎯 Job '{job.name}' is due - would execute now")
                        # TODO: Implement actual job execution
                        
                        # Mark job as executed (placeholder)
                        job.mark_as_executed()
                        # TODO: Update job in repository
                else:
                    print("😴 No jobs due for execution")
        
        except Exception as e:
            print(f"❌ Error during scheduler tick: {e}")
    
    async def shutdown(self) -> None:
        """Shutdown the scheduler gracefully."""
        print("🛑 Shutting down job scheduler...")
        self._running = False
        
        if self.db_connection:
            await self.db_connection.close()
        
        print("✅ Job scheduler stopped!")
    
    def _signal_handler(self, signum: int, frame) -> None:
        """Handle shutdown signals."""
        print(f"\n📡 Received signal {signum}")
        self._running = False


async def main() -> None:
    """Main entry point."""
    app = JobSchedulerApp()
    
    try:
        await app.start()
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Run the application
    asyncio.run(main())