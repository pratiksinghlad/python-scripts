"""
Job executor interface.

This module defines the abstract interface for job execution operations.
Following the Single Responsibility Principle, this interface is focused
solely on job execution concerns.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from ..entities.job import Job
from ..entities.execution import JobExecution


class JobExecutorInterface(ABC):
    """
    Abstract interface for job execution operations.
    
    This interface defines the contract for executing jobs,
    allowing different execution strategies (subprocess, container, etc.)
    to be used interchangeably (Liskov Substitution Principle).
    """
    
    @abstractmethod
    async def execute_job(
        self,
        job: Job,
        execution: Optional[JobExecution] = None,
    ) -> JobExecution:
        """
        Execute a job and return the execution result.
        
        Args:
            job: Job entity to execute.
            execution: Optional existing execution entity to update.
            
        Returns:
            Job execution entity with results.
            
        Raises:
            ExecutionError: If execution fails.
        """
        pass
    
    @abstractmethod
    async def cancel_execution(self, execution_id: int) -> bool:
        """
        Cancel a running job execution.
        
        Args:
            execution_id: Execution ID to cancel.
            
        Returns:
            True if cancellation was successful.
            
        Raises:
            ExecutionError: If cancellation fails.
        """
        pass
    
    @abstractmethod
    async def get_running_executions(self) -> list[int]:
        """
        Get list of currently running execution IDs.
        
        Returns:
            List of running execution IDs.
            
        Raises:
            ExecutionError: If retrieval fails.
        """
        pass
    
    @abstractmethod
    async def is_execution_running(self, execution_id: int) -> bool:
        """
        Check if a specific execution is currently running.
        
        Args:
            execution_id: Execution ID to check.
            
        Returns:
            True if execution is running.
            
        Raises:
            ExecutionError: If check fails.
        """
        pass
    
    @abstractmethod
    async def cleanup_finished_executions(self) -> int:
        """
        Clean up finished execution processes and resources.
        
        Returns:
            Number of executions cleaned up.
            
        Raises:
            ExecutionError: If cleanup fails.
        """
        pass