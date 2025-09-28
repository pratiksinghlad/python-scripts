"""
Job domain service.

This module provides domain-level business logic for job management operations.
It orchestrates between entities and maintains business rules while remaining
independent of infrastructure concerns.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, Sequence
from uuid import UUID

from ..entities.job import Job, JobStatus
from ..entities.execution import JobExecution, ExecutionStatus
from ..interfaces.job_repository import (
    JobRepositoryInterface,
    JobExecutionRepositoryInterface,
)


class JobDomainService:
    """
    Job domain service that handles job-related business logic.
    
    This service follows the Single Responsibility Principle by focusing
    on job management operations and business rules enforcement.
    """
    
    def __init__(
        self,
        job_repository: JobRepositoryInterface,
        execution_repository: JobExecutionRepositoryInterface,
    ) -> None:
        """
        Initialize the job domain service.
        
        Args:
            job_repository: Job repository implementation.
            execution_repository: Job execution repository implementation.
        """
        self._job_repository = job_repository
        self._execution_repository = execution_repository
    
    async def create_job(
        self,
        name: str,
        cron_expression: str,
        command: str,
        description: str = "",
        timeout_seconds: int = 300,
        max_retries: int = 3,
        retry_delay_seconds: int = 60,
        environment_variables: Optional[dict[str, str]] = None,
        tags: Optional[list[str]] = None,
    ) -> Job:
        """
        Create a new job with business rule validation.
        
        Args:
            name: Job name (must be unique).
            cron_expression: Cron expression for scheduling.
            command: Command to execute.
            description: Optional job description.
            timeout_seconds: Job execution timeout.
            max_retries: Maximum retry attempts.
            retry_delay_seconds: Delay between retries.
            environment_variables: Optional environment variables.
            tags: Optional job tags.
            
        Returns:
            Created job entity.
            
        Raises:
            ValueError: If validation fails.
            BusinessRuleError: If business rules are violated.
        """
        # Business rule: Job name must be unique
        existing_job = await self._job_repository.get_by_name(name)
        if existing_job is not None:
            raise ValueError(f"Job with name '{name}' already exists")
        
        # Create job entity (will validate cron expression)
        job = Job(
            name=name,
            cron_expression=cron_expression,
            command=command,
            description=description,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
            retry_delay_seconds=retry_delay_seconds,
            environment_variables=environment_variables or {},
            tags=tags or [],
        )
        
        # Persist the job
        return await self._job_repository.create(job)
    
    async def update_job(
        self,
        job_id: int,
        name: Optional[str] = None,
        cron_expression: Optional[str] = None,
        command: Optional[str] = None,
        description: Optional[str] = None,
        timeout_seconds: Optional[int] = None,
        max_retries: Optional[int] = None,
        retry_delay_seconds: Optional[int] = None,
    ) -> Job:
        """
        Update an existing job with validation.
        
        Args:
            job_id: Job ID to update.
            name: New job name (optional).
            cron_expression: New cron expression (optional).
            command: New command (optional).
            description: New description (optional).
            timeout_seconds: New timeout (optional).
            max_retries: New max retries (optional).
            retry_delay_seconds: New retry delay (optional).
            
        Returns:
            Updated job entity.
            
        Raises:
            NotFoundError: If job doesn't exist.
            ValueError: If validation fails.
            BusinessRuleError: If business rules are violated.
        """
        job = await self._job_repository.get_by_id(job_id)
        if job is None:
            raise ValueError(f"Job with ID {job_id} not found")
        
        # Business rule: If changing name, ensure it's unique
        if name is not None and name != job.name:
            existing_job = await self._job_repository.get_by_name(name)
            if existing_job is not None:
                raise ValueError(f"Job with name '{name}' already exists")
            job.name = name
        
        # Update fields if provided
        if cron_expression is not None:
            job.cron_expression = cron_expression
            job.validate_cron_expression()  # Validate new expression
            job.calculate_next_run()  # Recalculate next run time
        
        if command is not None:
            job.command = command
        
        if description is not None:
            job.description = description
        
        if timeout_seconds is not None:
            if timeout_seconds <= 0:
                raise ValueError("Timeout must be positive")
            job.timeout_seconds = timeout_seconds
        
        if max_retries is not None:
            if max_retries < 0:
                raise ValueError("Max retries cannot be negative")
            job.max_retries = max_retries
        
        if retry_delay_seconds is not None:
            if retry_delay_seconds < 0:
                raise ValueError("Retry delay cannot be negative")
            job.retry_delay_seconds = retry_delay_seconds
        
        job.updated_at = datetime.utcnow()
        
        return await self._job_repository.update(job)
    
    async def get_jobs_due_for_execution(
        self,
        current_time: Optional[datetime] = None,
    ) -> Sequence[Job]:
        """
        Get jobs that are due for execution based on business rules.
        
        Args:
            current_time: Current time for comparison.
            
        Returns:
            Sequence of jobs due for execution.
        """
        if current_time is None:
            current_time = datetime.utcnow()
        
        due_jobs = await self._job_repository.get_due_jobs(current_time)
        
        # Apply business rules for execution eligibility
        eligible_jobs = []
        for job in due_jobs:
            if await self._is_job_eligible_for_execution(job, current_time):
                eligible_jobs.append(job)
        
        return eligible_jobs
    
    async def create_job_execution(
        self,
        job: Job,
        scheduled_time: Optional[datetime] = None,
    ) -> JobExecution:
        """
        Create a new job execution record.
        
        Args:
            job: Job to execute.
            scheduled_time: When the job was scheduled to run.
            
        Returns:
            Created job execution entity.
        """
        if scheduled_time is None:
            scheduled_time = datetime.utcnow()
        
        execution = JobExecution(
            job_id=job.id,
            job_uuid=job.uuid,
            scheduled_time=scheduled_time,
            environment_variables=job.environment_variables.copy(),
        )
        
        return await self._execution_repository.create(execution)
    
    async def should_retry_execution(
        self,
        execution: JobExecution,
        job: Job,
    ) -> bool:
        """
        Determine if a failed execution should be retried based on business rules.
        
        Args:
            execution: Failed job execution.
            job: Associated job entity.
            
        Returns:
            True if execution should be retried.
        """
        # Business rule: Don't retry if max retries exceeded
        if execution.retry_count >= job.max_retries:
            return False
        
        # Business rule: Only retry certain failure types
        if not execution.can_retry:
            return False
        
        # Business rule: Don't retry if job is no longer active
        if job.status != JobStatus.ACTIVE:
            return False
        
        return True
    
    async def calculate_retry_time(
        self,
        execution: JobExecution,
        job: Job,
        base_time: Optional[datetime] = None,
    ) -> datetime:
        """
        Calculate when a failed execution should be retried.
        
        Args:
            execution: Failed job execution.
            job: Associated job entity.
            base_time: Base time for calculation.
            
        Returns:
            DateTime when retry should occur.
        """
        if base_time is None:
            base_time = datetime.utcnow()
        
        # Business rule: Exponential backoff with base delay
        retry_delay = job.retry_delay_seconds * (2 ** execution.retry_count)
        
        # Business rule: Cap the maximum retry delay at 1 hour
        max_delay = 3600  # 1 hour
        retry_delay = min(retry_delay, max_delay)
        
        return base_time + timedelta(seconds=retry_delay)
    
    async def cleanup_old_executions(
        self,
        retention_days: int = 30,
        keep_per_job: int = 10,
    ) -> int:
        """
        Clean up old execution records based on retention policy.
        
        Args:
            retention_days: Keep executions newer than this many days.
            keep_per_job: Minimum number of executions to keep per job.
            
        Returns:
            Number of executions cleaned up.
        """
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        
        return await self._execution_repository.delete_old_executions(
            older_than=cutoff_date,
            keep_count=keep_per_job,
        )
    
    async def get_job_statistics(self, job_id: int) -> dict[str, any]:
        """
        Get statistics for a specific job.
        
        Args:
            job_id: Job ID to get statistics for.
            
        Returns:
            Dictionary containing job statistics.
        """
        job = await self._job_repository.get_by_id(job_id)
        if job is None:
            raise ValueError(f"Job with ID {job_id} not found")
        
        executions = await self._execution_repository.get_by_job_id(job_id)
        
        # Calculate statistics
        total_executions = len(executions)
        successful_executions = sum(
            1 for e in executions if e.status == ExecutionStatus.SUCCESS
        )
        failed_executions = sum(
            1 for e in executions if e.status == ExecutionStatus.FAILED
        )
        
        success_rate = (
            (successful_executions / total_executions * 100)
            if total_executions > 0 else 0
        )
        
        # Calculate average duration for successful executions
        successful_durations = [
            e.duration_seconds
            for e in executions
            if e.is_successful and e.duration_seconds is not None
        ]
        avg_duration = (
            sum(successful_durations) / len(successful_durations)
            if successful_durations else 0
        )
        
        return {
            "job_name": job.name,
            "job_status": job.status.value,
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": failed_executions,
            "success_rate_percent": round(success_rate, 2),
            "average_duration_seconds": round(avg_duration, 2),
            "last_execution": job.last_run.isoformat() if job.last_run else None,
            "next_execution": job.next_run.isoformat() if job.next_run else None,
        }
    
    async def _is_job_eligible_for_execution(
        self,
        job: Job,
        current_time: datetime,
    ) -> bool:
        """
        Check if a job is eligible for execution based on business rules.
        
        Args:
            job: Job to check.
            current_time: Current time.
            
        Returns:
            True if job is eligible for execution.
        """
        # Business rule: Only active jobs can be executed
        if job.status != JobStatus.ACTIVE:
            return False
        
        # Business rule: Job must be due
        if not job.is_due(current_time):
            return False
        
        # Business rule: Don't execute if there's already a running execution
        # (This would be checked in the application layer with the executor)
        
        return True