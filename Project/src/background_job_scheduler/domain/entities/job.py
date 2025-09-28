"""
Job domain entity.

This module defines the Job entity which represents a scheduled job in the system.
Following Domain-Driven Design principles, this entity encapsulates business logic
and maintains data integrity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Any
from uuid import UUID, uuid4

from croniter import croniter


class JobStatus(Enum):
    """Job status enumeration."""
    
    ACTIVE = "active"
    INACTIVE = "inactive"
    PAUSED = "paused"
    DELETED = "deleted"


@dataclass
class Job:
    """
    Job domain entity.
    
    Represents a scheduled job with cron expression support.
    Follows Single Responsibility Principle - handles job data and validation.
    """
    
    name: str
    cron_expression: str
    command: str
    description: str = ""
    status: JobStatus = JobStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    timeout_seconds: int = 300
    max_retries: int = 3
    retry_delay_seconds: int = 60
    environment_variables: dict[str, str] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    id: Optional[int] = None
    uuid: UUID = field(default_factory=uuid4)
    
    def __post_init__(self) -> None:
        """Post-initialization validation and setup."""
        self.validate_cron_expression()
        if self.next_run is None:
            self.calculate_next_run()
    
    def validate_cron_expression(self) -> None:
        """
        Validate the cron expression.
        
        Raises:
            ValueError: If the cron expression is invalid.
        """
        try:
            croniter(self.cron_expression)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid cron expression '{self.cron_expression}': {e}") from e
    
    def calculate_next_run(self, base_time: Optional[datetime] = None) -> datetime:
        """
        Calculate the next run time based on the cron expression.
        
        Args:
            base_time: Base time to calculate from (defaults to current time).
            
        Returns:
            The next scheduled run time.
        """
        if base_time is None:
            base_time = datetime.utcnow()
        
        cron = croniter(self.cron_expression, base_time)
        self.next_run = cron.get_next(datetime)
        return self.next_run
    
    def is_due(self, current_time: Optional[datetime] = None) -> bool:
        """
        Check if the job is due for execution.
        
        Args:
            current_time: Current time to compare against (defaults to UTC now).
            
        Returns:
            True if the job should be executed now.
        """
        if current_time is None:
            current_time = datetime.utcnow()
        
        return (
            self.status == JobStatus.ACTIVE
            and self.next_run is not None
            and self.next_run <= current_time
        )
    
    def mark_as_executed(self, execution_time: Optional[datetime] = None) -> None:
        """
        Mark the job as executed and calculate the next run time.
        
        Args:
            execution_time: When the job was executed (defaults to current time).
        """
        if execution_time is None:
            execution_time = datetime.utcnow()
        
        self.last_run = execution_time
        self.updated_at = execution_time
        self.calculate_next_run(execution_time)
    
    def pause(self) -> None:
        """Pause the job execution."""
        if self.status == JobStatus.ACTIVE:
            self.status = JobStatus.PAUSED
            self.updated_at = datetime.utcnow()
    
    def resume(self) -> None:
        """Resume the job execution."""
        if self.status == JobStatus.PAUSED:
            self.status = JobStatus.ACTIVE
            self.updated_at = datetime.utcnow()
            self.calculate_next_run()
    
    def deactivate(self) -> None:
        """Deactivate the job."""
        self.status = JobStatus.INACTIVE
        self.updated_at = datetime.utcnow()
        self.next_run = None
    
    def activate(self) -> None:
        """Activate the job."""
        if self.status in (JobStatus.INACTIVE, JobStatus.PAUSED):
            self.status = JobStatus.ACTIVE
            self.updated_at = datetime.utcnow()
            self.calculate_next_run()
    
    def soft_delete(self) -> None:
        """Soft delete the job."""
        self.status = JobStatus.DELETED
        self.updated_at = datetime.utcnow()
        self.next_run = None
    
    def add_tag(self, tag: str) -> None:
        """
        Add a tag to the job.
        
        Args:
            tag: Tag to add.
        """
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.utcnow()
    
    def remove_tag(self, tag: str) -> None:
        """
        Remove a tag from the job.
        
        Args:
            tag: Tag to remove.
        """
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.utcnow()
    
    def set_environment_variable(self, key: str, value: str) -> None:
        """
        Set an environment variable for the job.
        
        Args:
            key: Environment variable name.
            value: Environment variable value.
        """
        self.environment_variables[key] = value
        self.updated_at = datetime.utcnow()
    
    def remove_environment_variable(self, key: str) -> None:
        """
        Remove an environment variable from the job.
        
        Args:
            key: Environment variable name to remove.
        """
        if key in self.environment_variables:
            del self.environment_variables[key]
            self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> dict[str, Any]:
        """
        Convert the job to a dictionary representation.
        
        Returns:
            Dictionary representation of the job.
        """
        return {
            "id": self.id,
            "uuid": str(self.uuid),
            "name": self.name,
            "cron_expression": self.cron_expression,
            "command": self.command,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat() if self.next_run else None,
            "timeout_seconds": self.timeout_seconds,
            "max_retries": self.max_retries,
            "retry_delay_seconds": self.retry_delay_seconds,
            "environment_variables": self.environment_variables,
            "tags": self.tags,
        }
    
    def __str__(self) -> str:
        """String representation of the job."""
        return f"Job(name='{self.name}', cron='{self.cron_expression}', status={self.status.value})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the job."""
        return (
            f"Job(id={self.id}, uuid={self.uuid}, name='{self.name}', "
            f"cron='{self.cron_expression}', status={self.status.value})"
        )