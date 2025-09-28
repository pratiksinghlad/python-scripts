"""
Background Job Scheduler

A modern Python 3.13 background job scheduler with MySQL database integration,
cron expression support, and clean architecture following SOLID principles.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .domain.entities.job import Job, JobStatus
from .domain.entities.execution import JobExecution, ExecutionStatus

__all__ = [
    "Job",
    "JobStatus", 
    "JobExecution",
    "ExecutionStatus",
]