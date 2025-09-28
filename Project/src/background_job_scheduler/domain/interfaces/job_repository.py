"""
Job repository interface.

This module defines the abstract interface for job data persistence.
Following the Dependency Inversion Principle, this allows the domain layer
to remain independent of infrastructure concerns.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Sequence
from uuid import UUID

from ..entities.job import Job, JobStatus


class JobRepositoryInterface(ABC):
    """
    Abstract interface for job repository operations.
    
    This interface defines the contract for job persistence operations,
    allowing different implementations (MySQL, PostgreSQL, etc.) to be
    used interchangeably (Liskov Substitution Principle).
    """
    
    @abstractmethod
    async def create(self, job: Job) -> Job:
        """
        Create a new job in the repository.
        
        Args:
            job: Job entity to create.
            
        Returns:
            The created job with assigned ID.
            
        Raises:
            RepositoryError: If creation fails.
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, job_id: int) -> Optional[Job]:
        """
        Retrieve a job by its ID.
        
        Args:
            job_id: Job ID to retrieve.
            
        Returns:
            Job entity if found, None otherwise.
            
        Raises:
            RepositoryError: If retrieval fails.
        """
        pass
    
    @abstractmethod
    async def get_by_uuid(self, job_uuid: UUID) -> Optional[Job]:
        """
        Retrieve a job by its UUID.
        
        Args:
            job_uuid: Job UUID to retrieve.
            
        Returns:
            Job entity if found, None otherwise.
            
        Raises:
            RepositoryError: If retrieval fails.
        """
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Job]:
        """
        Retrieve a job by its name.
        
        Args:
            name: Job name to retrieve.
            
        Returns:
            Job entity if found, None otherwise.
            
        Raises:
            RepositoryError: If retrieval fails.
        """
        pass
    
    @abstractmethod
    async def get_all(
        self,
        status: Optional[JobStatus] = None,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> Sequence[Job]:
        """
        Retrieve jobs with optional filtering and pagination.
        
        Args:
            status: Optional status filter.
            limit: Maximum number of jobs to return.
            offset: Number of jobs to skip.
            
        Returns:
            Sequence of job entities.
            
        Raises:
            RepositoryError: If retrieval fails.
        """
        pass
    
    @abstractmethod
    async def get_due_jobs(self, current_time: Optional[datetime] = None) -> Sequence[Job]:
        """
        Retrieve jobs that are due for execution.
        
        Args:
            current_time: Current time for comparison (defaults to UTC now).
            
        Returns:
            Sequence of jobs due for execution.
            
        Raises:
            RepositoryError: If retrieval fails.
        """
        pass
    
    @abstractmethod
    async def get_by_tags(self, tags: Sequence[str]) -> Sequence[Job]:
        """
        Retrieve jobs that have any of the specified tags.
        
        Args:
            tags: Tags to search for.
            
        Returns:
            Sequence of jobs with matching tags.
            
        Raises:
            RepositoryError: If retrieval fails.
        """
        pass
    
    @abstractmethod
    async def update(self, job: Job) -> Job:
        """
        Update an existing job in the repository.
        
        Args:
            job: Job entity to update.
            
        Returns:
            The updated job entity.
            
        Raises:
            RepositoryError: If update fails.
            NotFoundError: If job doesn't exist.
        """
        pass
    
    @abstractmethod
    async def delete(self, job_id: int) -> bool:
        """
        Delete a job from the repository.
        
        Args:
            job_id: Job ID to delete.
            
        Returns:
            True if deleted successfully.
            
        Raises:
            RepositoryError: If deletion fails.
            NotFoundError: If job doesn't exist.
        """
        pass
    
    @abstractmethod
    async def count(self, status: Optional[JobStatus] = None) -> int:
        """
        Count jobs with optional status filter.
        
        Args:
            status: Optional status filter.
            
        Returns:
            Number of jobs matching the criteria.
            
        Raises:
            RepositoryError: If counting fails.
        """
        pass
    
    @abstractmethod
    async def exists(self, job_id: int) -> bool:
        """
        Check if a job exists.
        
        Args:
            job_id: Job ID to check.
            
        Returns:
            True if job exists.
            
        Raises:
            RepositoryError: If check fails.
        """
        pass
    
    @abstractmethod
    async def bulk_update_status(
        self,
        job_ids: Sequence[int],
        status: JobStatus,
    ) -> int:
        """
        Update status for multiple jobs.
        
        Args:
            job_ids: Job IDs to update.
            status: New status to set.
            
        Returns:
            Number of jobs updated.
            
        Raises:
            RepositoryError: If update fails.
        """
        pass


class JobExecutionRepositoryInterface(ABC):
    """
    Abstract interface for job execution repository operations.
    
    This interface follows the Interface Segregation Principle by separating
    job execution persistence from job persistence operations.
    """
    
    @abstractmethod
    async def create(self, execution: 'JobExecution') -> 'JobExecution':
        """
        Create a new job execution record.
        
        Args:
            execution: Job execution entity to create.
            
        Returns:
            The created execution with assigned ID.
            
        Raises:
            RepositoryError: If creation fails.
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, execution_id: int) -> Optional['JobExecution']:
        """
        Retrieve a job execution by its ID.
        
        Args:
            execution_id: Execution ID to retrieve.
            
        Returns:
            Job execution entity if found, None otherwise.
            
        Raises:
            RepositoryError: If retrieval fails.
        """
        pass
    
    @abstractmethod
    async def get_by_job_id(
        self,
        job_id: int,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> Sequence['JobExecution']:
        """
        Retrieve executions for a specific job.
        
        Args:
            job_id: Job ID to retrieve executions for.
            limit: Maximum number of executions to return.
            offset: Number of executions to skip.
            
        Returns:
            Sequence of job execution entities.
            
        Raises:
            RepositoryError: If retrieval fails.
        """
        pass
    
    @abstractmethod
    async def update(self, execution: 'JobExecution') -> 'JobExecution':
        """
        Update an existing job execution.
        
        Args:
            execution: Job execution entity to update.
            
        Returns:
            The updated execution entity.
            
        Raises:
            RepositoryError: If update fails.
            NotFoundError: If execution doesn't exist.
        """
        pass
    
    @abstractmethod
    async def delete_old_executions(
        self,
        older_than: datetime,
        keep_count: Optional[int] = None,
    ) -> int:
        """
        Delete old execution records.
        
        Args:
            older_than: Delete executions older than this date.
            keep_count: Minimum number of executions to keep per job.
            
        Returns:
            Number of executions deleted.
            
        Raises:
            RepositoryError: If deletion fails.
        """
        pass