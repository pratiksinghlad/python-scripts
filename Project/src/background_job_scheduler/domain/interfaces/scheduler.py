"""
Scheduler interface.

This module defines the abstract interface for job scheduling operations.
Following the Dependency Inversion Principle, this allows different
scheduling implementations to be used interchangeably.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Optional, Any

from ..entities.job import Job


class SchedulerInterface(ABC):
    """
    Abstract interface for job scheduling operations.
    
    This interface defines the contract for scheduling jobs,
    allowing different implementations (APScheduler, Celery, etc.)
    to be used interchangeably (Liskov Substitution Principle).
    """
    
    @abstractmethod
    async def start(self) -> None:
        """
        Start the scheduler.
        
        Raises:
            SchedulerError: If starting fails.
        """
        pass
    
    @abstractmethod
    async def stop(self) -> None:
        """
        Stop the scheduler.
        
        Raises:
            SchedulerError: If stopping fails.
        """
        pass
    
    @abstractmethod
    async def pause(self) -> None:
        """
        Pause the scheduler.
        
        Raises:
            SchedulerError: If pausing fails.
        """
        pass
    
    @abstractmethod
    async def resume(self) -> None:
        """
        Resume the scheduler.
        
        Raises:
            SchedulerError: If resuming fails.
        """
        pass
    
    @abstractmethod
    async def schedule_job(
        self,
        job: Job,
        executor_func: Callable[[Job], Any],
    ) -> bool:
        """
        Schedule a job for execution.
        
        Args:
            job: Job entity to schedule.
            executor_func: Function to execute the job.
            
        Returns:
            True if scheduled successfully.
            
        Raises:
            SchedulerError: If scheduling fails.
        """
        pass
    
    @abstractmethod
    async def unschedule_job(self, job_id: int) -> bool:
        """
        Remove a job from the schedule.
        
        Args:
            job_id: Job ID to unschedule.
            
        Returns:
            True if unscheduled successfully.
            
        Raises:
            SchedulerError: If unscheduling fails.
        """
        pass
    
    @abstractmethod
    async def reschedule_job(
        self,
        job: Job,
        executor_func: Callable[[Job], Any],
    ) -> bool:
        """
        Reschedule an existing job with updated parameters.
        
        Args:
            job: Updated job entity.
            executor_func: Function to execute the job.
            
        Returns:
            True if rescheduled successfully.
            
        Raises:
            SchedulerError: If rescheduling fails.
        """
        pass
    
    @abstractmethod
    async def is_job_scheduled(self, job_id: int) -> bool:
        """
        Check if a job is currently scheduled.
        
        Args:
            job_id: Job ID to check.
            
        Returns:
            True if job is scheduled.
            
        Raises:
            SchedulerError: If check fails.
        """
        pass
    
    @abstractmethod
    async def get_scheduled_jobs_count(self) -> int:
        """
        Get the number of currently scheduled jobs.
        
        Returns:
            Number of scheduled jobs.
            
        Raises:
            SchedulerError: If counting fails.
        """
        pass
    
    @abstractmethod
    async def get_running_jobs_count(self) -> int:
        """
        Get the number of currently running jobs.
        
        Returns:
            Number of running jobs.
            
        Raises:
            SchedulerError: If counting fails.
        """
        pass
    
    @property
    @abstractmethod
    def is_running(self) -> bool:
        """
        Check if the scheduler is running.
        
        Returns:
            True if scheduler is running.
        """
        pass
    
    @property
    @abstractmethod
    def is_paused(self) -> bool:
        """
        Check if the scheduler is paused.
        
        Returns:
            True if scheduler is paused.
        """
        pass