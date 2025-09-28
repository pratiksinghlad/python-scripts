"""
Unit tests for Job domain entity.

These tests verify the business logic and behavior of the Job entity
without dependencies on external systems.
"""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from background_job_scheduler.domain.entities.job import Job, JobStatus


class TestJob:
    """Test cases for Job entity."""
    
    def test_job_creation_with_valid_cron(self) -> None:
        """Test creating a job with valid cron expression."""
        job = Job(
            name="test_job",
            cron_expression="0 2 * * *",  # Daily at 2 AM
            command="python test.py",
            description="Test job",
        )
        
        assert job.name == "test_job"
        assert job.cron_expression == "0 2 * * *"
        assert job.command == "python test.py"
        assert job.status == JobStatus.ACTIVE
        assert job.next_run is not None
    
    def test_job_creation_with_invalid_cron(self) -> None:
        """Test creating a job with invalid cron expression raises ValueError."""
        with pytest.raises(ValueError, match="Invalid cron expression"):
            Job(
                name="invalid_job",
                cron_expression="invalid cron",
                command="python test.py",
            )
    
    def test_job_is_due_when_time_passed(self) -> None:
        """Test that job is due when next_run time has passed."""
        past_time = datetime.utcnow() - timedelta(minutes=1)
        
        job = Job(
            name="due_job",
            cron_expression="* * * * *",  # Every minute
            command="python test.py",
        )
        job.next_run = past_time
        
        assert job.is_due() is True
    
    def test_job_is_not_due_when_time_not_passed(self) -> None:
        """Test that job is not due when next_run time hasn't passed."""
        future_time = datetime.utcnow() + timedelta(minutes=1)
        
        job = Job(
            name="not_due_job",
            cron_expression="* * * * *",
            command="python test.py",
        )
        job.next_run = future_time
        
        assert job.is_due() is False
    
    def test_job_is_not_due_when_inactive(self) -> None:
        """Test that inactive job is never due."""
        past_time = datetime.utcnow() - timedelta(minutes=1)
        
        job = Job(
            name="inactive_job",
            cron_expression="* * * * *",
            command="python test.py",
            status=JobStatus.INACTIVE,
        )
        job.next_run = past_time
        
        assert job.is_due() is False
    
    def test_mark_as_executed_updates_times(self) -> None:
        """Test that marking job as executed updates last_run and next_run."""
        job = Job(
            name="executed_job",
            cron_expression="0 2 * * *",  # Daily at 2 AM
            command="python test.py",
        )
        
        execution_time = datetime.utcnow()
        original_next_run = job.next_run
        
        job.mark_as_executed(execution_time)
        
        assert job.last_run == execution_time
        assert job.next_run != original_next_run
        assert job.next_run > execution_time
    
    def test_pause_and_resume_job(self) -> None:
        """Test pausing and resuming a job."""
        job = Job(
            name="pausable_job",
            cron_expression="0 2 * * *",
            command="python test.py",
        )
        
        # Pause the job
        job.pause()
        assert job.status == JobStatus.PAUSED
        
        # Resume the job
        job.resume()
        assert job.status == JobStatus.ACTIVE
    
    def test_add_and_remove_tags(self) -> None:
        """Test adding and removing job tags."""
        job = Job(
            name="tagged_job",
            cron_expression="0 2 * * *",
            command="python test.py",
        )
        
        # Add tags
        job.add_tag("backup")
        job.add_tag("important")
        
        assert "backup" in job.tags
        assert "important" in job.tags
        assert len(job.tags) == 2
        
        # Remove tag
        job.remove_tag("backup")
        
        assert "backup" not in job.tags
        assert "important" in job.tags
        assert len(job.tags) == 1
    
    def test_set_environment_variables(self) -> None:
        """Test setting job environment variables."""
        job = Job(
            name="env_job",
            cron_expression="0 2 * * *",
            command="python test.py",
        )
        
        job.set_environment_variable("DATABASE_URL", "mysql://localhost")
        job.set_environment_variable("DEBUG", "true")
        
        assert job.environment_variables["DATABASE_URL"] == "mysql://localhost"
        assert job.environment_variables["DEBUG"] == "true"
        
        # Remove variable
        job.remove_environment_variable("DEBUG")
        assert "DEBUG" not in job.environment_variables
        assert "DATABASE_URL" in job.environment_variables
    
    def test_job_to_dict(self) -> None:
        """Test converting job to dictionary."""
        job = Job(
            name="dict_job",
            cron_expression="0 2 * * *",
            command="python test.py",
            description="Test description",
        )
        job.id = 123
        
        job_dict = job.to_dict()
        
        assert job_dict["id"] == 123
        assert job_dict["name"] == "dict_job"
        assert job_dict["cron_expression"] == "0 2 * * *"
        assert job_dict["command"] == "python test.py"
        assert job_dict["description"] == "Test description"
        assert job_dict["status"] == "active"
        assert "uuid" in job_dict
        assert "created_at" in job_dict
    
    def test_job_string_representations(self) -> None:
        """Test job string representations."""
        job = Job(
            name="string_job",
            cron_expression="0 2 * * *",
            command="python test.py",
        )
        
        str_repr = str(job)
        assert "string_job" in str_repr
        assert "0 2 * * *" in str_repr
        assert "active" in str_repr
        
        repr_str = repr(job)
        assert "Job(" in repr_str
        assert "string_job" in repr_str