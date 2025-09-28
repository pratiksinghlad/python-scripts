"""
Job execution domain entity.

This module defines the JobExecution entity which represents a single execution
of a scheduled job. It tracks execution status, timing, and results.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Any
from uuid import UUID, uuid4


class ExecutionStatus(Enum):
    """Job execution status enumeration."""
    
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


@dataclass
class JobExecution:
    """
    Job execution domain entity.
    
    Represents a single execution instance of a job.
    Follows Single Responsibility Principle - manages execution state and metadata.
    """
    
    job_id: int
    job_uuid: UUID
    status: ExecutionStatus = ExecutionStatus.PENDING
    scheduled_time: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    exit_code: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    error_message: str = ""
    retry_count: int = 0
    environment_variables: dict[str, str] = field(default_factory=dict)
    execution_metadata: dict[str, Any] = field(default_factory=dict)
    id: Optional[int] = None
    uuid: UUID = field(default_factory=uuid4)
    
    @property
    def duration_seconds(self) -> Optional[float]:
        """
        Calculate the execution duration in seconds.
        
        Returns:
            Duration in seconds, or None if not yet finished.
        """
        if self.started_at is None or self.finished_at is None:
            return None
        
        delta = self.finished_at - self.started_at
        return delta.total_seconds()
    
    @property
    def is_completed(self) -> bool:
        """
        Check if the execution has completed (success or failure).
        
        Returns:
            True if execution is in a terminal state.
        """
        return self.status in (
            ExecutionStatus.SUCCESS,
            ExecutionStatus.FAILED,
            ExecutionStatus.TIMEOUT,
            ExecutionStatus.CANCELLED,
        )
    
    @property
    def is_successful(self) -> bool:
        """
        Check if the execution was successful.
        
        Returns:
            True if execution completed successfully.
        """
        return self.status == ExecutionStatus.SUCCESS
    
    @property
    def can_retry(self) -> bool:
        """
        Check if the execution can be retried.
        
        Returns:
            True if execution failed and can be retried.
        """
        return self.status in (ExecutionStatus.FAILED, ExecutionStatus.TIMEOUT)
    
    def start(self, start_time: Optional[datetime] = None) -> None:
        """
        Mark the execution as started.
        
        Args:
            start_time: Start time (defaults to current time).
        """
        if start_time is None:
            start_time = datetime.utcnow()
        
        self.status = ExecutionStatus.RUNNING
        self.started_at = start_time
    
    def complete_success(
        self,
        exit_code: int = 0,
        stdout: str = "",
        finish_time: Optional[datetime] = None,
    ) -> None:
        """
        Mark the execution as successfully completed.
        
        Args:
            exit_code: Process exit code.
            stdout: Standard output from the execution.
            finish_time: Finish time (defaults to current time).
        """
        if finish_time is None:
            finish_time = datetime.utcnow()
        
        self.status = ExecutionStatus.SUCCESS
        self.finished_at = finish_time
        self.exit_code = exit_code
        self.stdout = stdout
    
    def complete_failure(
        self,
        exit_code: Optional[int] = None,
        stderr: str = "",
        error_message: str = "",
        finish_time: Optional[datetime] = None,
    ) -> None:
        """
        Mark the execution as failed.
        
        Args:
            exit_code: Process exit code.
            stderr: Standard error from the execution.
            error_message: Error description.
            finish_time: Finish time (defaults to current time).
        """
        if finish_time is None:
            finish_time = datetime.utcnow()
        
        self.status = ExecutionStatus.FAILED
        self.finished_at = finish_time
        self.exit_code = exit_code
        self.stderr = stderr
        self.error_message = error_message
    
    def timeout(
        self,
        error_message: str = "Execution timed out",
        finish_time: Optional[datetime] = None,
    ) -> None:
        """
        Mark the execution as timed out.
        
        Args:
            error_message: Timeout error message.
            finish_time: Finish time (defaults to current time).
        """
        if finish_time is None:
            finish_time = datetime.utcnow()
        
        self.status = ExecutionStatus.TIMEOUT
        self.finished_at = finish_time
        self.error_message = error_message
    
    def cancel(
        self,
        error_message: str = "Execution was cancelled",
        finish_time: Optional[datetime] = None,
    ) -> None:
        """
        Mark the execution as cancelled.
        
        Args:
            error_message: Cancellation message.
            finish_time: Finish time (defaults to current time).
        """
        if finish_time is None:
            finish_time = datetime.utcnow()
        
        self.status = ExecutionStatus.CANCELLED
        self.finished_at = finish_time
        self.error_message = error_message
    
    def prepare_retry(self) -> None:
        """Prepare the execution for retry."""
        if self.can_retry:
            self.status = ExecutionStatus.RETRYING
            self.retry_count += 1
            # Reset timing information
            self.started_at = None
            self.finished_at = None
            self.exit_code = None
    
    def set_metadata(self, key: str, value: Any) -> None:
        """
        Set execution metadata.
        
        Args:
            key: Metadata key.
            value: Metadata value.
        """
        self.execution_metadata[key] = value
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """
        Get execution metadata.
        
        Args:
            key: Metadata key.
            default: Default value if key not found.
            
        Returns:
            Metadata value or default.
        """
        return self.execution_metadata.get(key, default)
    
    def to_dict(self) -> dict[str, Any]:
        """
        Convert the execution to a dictionary representation.
        
        Returns:
            Dictionary representation of the execution.
        """
        return {
            "id": self.id,
            "uuid": str(self.uuid),
            "job_id": self.job_id,
            "job_uuid": str(self.job_uuid),
            "status": self.status.value,
            "scheduled_time": self.scheduled_time.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "duration_seconds": self.duration_seconds,
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "error_message": self.error_message,
            "retry_count": self.retry_count,
            "environment_variables": self.environment_variables,
            "execution_metadata": self.execution_metadata,
        }
    
    def __str__(self) -> str:
        """String representation of the execution."""
        return f"JobExecution(job_id={self.job_id}, status={self.status.value})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the execution."""
        return (
            f"JobExecution(id={self.id}, uuid={self.uuid}, job_id={self.job_id}, "
            f"status={self.status.value}, retry_count={self.retry_count})"
        )