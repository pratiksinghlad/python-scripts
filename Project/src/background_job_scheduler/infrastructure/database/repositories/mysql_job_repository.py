"""
MySQL job repository implementation.

This module implements the job repository interface using MySQL as the
persistence layer. It follows the Repository pattern and implements
the JobRepositoryInterface contract.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Optional, Sequence
from uuid import UUID
import mysql.connector
from mysql.connector import Error as MySQLError
import structlog

from ....domain.entities.job import Job, JobStatus
from ....domain.entities.execution import JobExecution, ExecutionStatus
from ....domain.interfaces.job_repository import (
    JobRepositoryInterface,
    JobExecutionRepositoryInterface,
)
from ..connection import DatabaseConnection


logger = structlog.get_logger(__name__)


class RepositoryError(Exception):
    """Base repository error."""
    pass


class NotFoundError(RepositoryError):
    """Raised when a resource is not found."""
    pass


class MySQLJobRepository(JobRepositoryInterface):
    """
    MySQL implementation of the job repository.
    
    This class implements the JobRepositoryInterface, allowing it to be used
    interchangeably with other repository implementations (Liskov Substitution).
    """
    
    def __init__(self, db_connection: DatabaseConnection) -> None:
        """
        Initialize the MySQL job repository.
        
        Args:
            db_connection: Database connection manager.
        """
        self._db = db_connection
    
    async def create(self, job: Job) -> Job:
        """Create a new job in the database."""
        query = """
            INSERT INTO jobs (
                uuid, name, cron_expression, command, description,
                status, timeout_seconds, max_retries, retry_delay_seconds,
                environment_variables, tags, next_run
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        
        try:
            async with self._db.get_connection() as connection:
                cursor = connection.cursor()
                
                cursor.execute(query, (
                    str(job.uuid),
                    job.name,
                    job.cron_expression,
                    job.command,
                    job.description,
                    job.status.value,
                    job.timeout_seconds,
                    job.max_retries,
                    job.retry_delay_seconds,
                    json.dumps(job.environment_variables),
                    json.dumps(job.tags),
                    job.next_run,
                ))
                
                job.id = cursor.lastrowid
                connection.commit()
                cursor.close()
                
                logger.info("Job created", job_id=job.id, job_name=job.name)
                return job
                
        except MySQLError as e:
            logger.error("Failed to create job", error=str(e), job_name=job.name)
            raise RepositoryError(f"Failed to create job: {e}") from e
    
    async def get_by_id(self, job_id: int) -> Optional[Job]:
        """Retrieve a job by ID."""
        query = "SELECT * FROM jobs WHERE id = %s AND status != 'deleted'"
        
        try:
            async with self._db.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, (job_id,))
                row = cursor.fetchone()
                cursor.close()
                
                return self._row_to_job(row) if row else None
                
        except MySQLError as e:
            logger.error("Failed to get job by ID", error=str(e), job_id=job_id)
            raise RepositoryError(f"Failed to get job: {e}") from e
    
    async def get_by_uuid(self, job_uuid: UUID) -> Optional[Job]:
        """Retrieve a job by UUID."""
        query = "SELECT * FROM jobs WHERE uuid = %s AND status != 'deleted'"
        
        try:
            async with self._db.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, (str(job_uuid),))
                row = cursor.fetchone()
                cursor.close()
                
                return self._row_to_job(row) if row else None
                
        except MySQLError as e:
            logger.error("Failed to get job by UUID", error=str(e), job_uuid=str(job_uuid))
            raise RepositoryError(f"Failed to get job: {e}") from e
    
    async def get_by_name(self, name: str) -> Optional[Job]:
        """Retrieve a job by name."""
        query = "SELECT * FROM jobs WHERE name = %s AND status != 'deleted'"
        
        try:
            async with self._db.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, (name,))
                row = cursor.fetchone()
                cursor.close()
                
                return self._row_to_job(row) if row else None
                
        except MySQLError as e:
            logger.error("Failed to get job by name", error=str(e), job_name=name)
            raise RepositoryError(f"Failed to get job: {e}") from e
    
    async def get_all(
        self,
        status: Optional[JobStatus] = None,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> Sequence[Job]:
        """Retrieve jobs with optional filtering and pagination."""
        query = "SELECT * FROM jobs WHERE status != 'deleted'"
        params = []
        
        if status:
            query += " AND status = %s"
            params.append(status.value)
        
        query += " ORDER BY created_at DESC"
        
        if limit:
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])
        
        try:
            async with self._db.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, params)
                rows = cursor.fetchall()
                cursor.close()
                
                return [self._row_to_job(row) for row in rows]
                
        except MySQLError as e:
            logger.error("Failed to get jobs", error=str(e))
            raise RepositoryError(f"Failed to get jobs: {e}") from e
    
    async def get_due_jobs(self, current_time: Optional[datetime] = None) -> Sequence[Job]:
        """Retrieve jobs that are due for execution."""
        if current_time is None:
            current_time = datetime.utcnow()
        
        query = """
            SELECT * FROM jobs 
            WHERE status = 'active' 
            AND next_run IS NOT NULL 
            AND next_run <= %s
            ORDER BY next_run ASC
        """
        
        try:
            async with self._db.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, (current_time,))
                rows = cursor.fetchall()
                cursor.close()
                
                return [self._row_to_job(row) for row in rows]
                
        except MySQLError as e:
            logger.error("Failed to get due jobs", error=str(e))
            raise RepositoryError(f"Failed to get due jobs: {e}") from e
    
    async def get_by_tags(self, tags: Sequence[str]) -> Sequence[Job]:
        """Retrieve jobs that have any of the specified tags."""
        if not tags:
            return []
        
        # Build query for JSON array contains any of the tags
        tag_conditions = []
        params = []
        
        for tag in tags:
            tag_conditions.append("JSON_CONTAINS(tags, %s)")
            params.append(json.dumps(tag))
        
        query = f"""
            SELECT * FROM jobs 
            WHERE status != 'deleted' 
            AND ({' OR '.join(tag_conditions)})
            ORDER BY created_at DESC
        """
        
        try:
            async with self._db.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, params)
                rows = cursor.fetchall()
                cursor.close()
                
                return [self._row_to_job(row) for row in rows]
                
        except MySQLError as e:
            logger.error("Failed to get jobs by tags", error=str(e), tags=tags)
            raise RepositoryError(f"Failed to get jobs by tags: {e}") from e
    
    async def update(self, job: Job) -> Job:
        """Update an existing job."""
        query = """
            UPDATE jobs SET
                name = %s, cron_expression = %s, command = %s,
                description = %s, status = %s, updated_at = %s,
                last_run = %s, next_run = %s, timeout_seconds = %s,
                max_retries = %s, retry_delay_seconds = %s,
                environment_variables = %s, tags = %s
            WHERE id = %s
        """
        
        try:
            async with self._db.get_connection() as connection:
                cursor = connection.cursor()
                
                cursor.execute(query, (
                    job.name,
                    job.cron_expression,
                    job.command,
                    job.description,
                    job.status.value,
                    job.updated_at,
                    job.last_run,
                    job.next_run,
                    job.timeout_seconds,
                    job.max_retries,
                    job.retry_delay_seconds,
                    json.dumps(job.environment_variables),
                    json.dumps(job.tags),
                    job.id,
                ))
                
                if cursor.rowcount == 0:
                    raise NotFoundError(f"Job with ID {job.id} not found")
                
                connection.commit()
                cursor.close()
                
                logger.info("Job updated", job_id=job.id, job_name=job.name)
                return job
                
        except MySQLError as e:
            logger.error("Failed to update job", error=str(e), job_id=job.id)
            raise RepositoryError(f"Failed to update job: {e}") from e
    
    async def delete(self, job_id: int) -> bool:
        """Delete a job (hard delete)."""
        query = "DELETE FROM jobs WHERE id = %s"
        
        try:
            async with self._db.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (job_id,))
                
                deleted = cursor.rowcount > 0
                connection.commit()
                cursor.close()
                
                if deleted:
                    logger.info("Job deleted", job_id=job_id)
                
                return deleted
                
        except MySQLError as e:
            logger.error("Failed to delete job", error=str(e), job_id=job_id)
            raise RepositoryError(f"Failed to delete job: {e}") from e
    
    async def count(self, status: Optional[JobStatus] = None) -> int:
        """Count jobs with optional status filter."""
        query = "SELECT COUNT(*) FROM jobs WHERE status != 'deleted'"
        params = []
        
        if status:
            query += " AND status = %s"
            params.append(status.value)
        
        try:
            async with self._db.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, params)
                count = cursor.fetchone()[0]
                cursor.close()
                
                return count
                
        except MySQLError as e:
            logger.error("Failed to count jobs", error=str(e))
            raise RepositoryError(f"Failed to count jobs: {e}") from e
    
    async def exists(self, job_id: int) -> bool:
        """Check if a job exists."""
        query = "SELECT 1 FROM jobs WHERE id = %s AND status != 'deleted'"
        
        try:
            async with self._db.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (job_id,))
                exists = cursor.fetchone() is not None
                cursor.close()
                
                return exists
                
        except MySQLError as e:
            logger.error("Failed to check job existence", error=str(e), job_id=job_id)
            raise RepositoryError(f"Failed to check job existence: {e}") from e
    
    async def bulk_update_status(
        self,
        job_ids: Sequence[int],
        status: JobStatus,
    ) -> int:
        """Update status for multiple jobs."""
        if not job_ids:
            return 0
        
        placeholders = ','.join(['%s'] * len(job_ids))
        query = f"""
            UPDATE jobs SET status = %s, updated_at = %s
            WHERE id IN ({placeholders})
        """
        
        try:
            async with self._db.get_connection() as connection:
                cursor = connection.cursor()
                
                params = [status.value, datetime.utcnow()] + list(job_ids)
                cursor.execute(query, params)
                
                updated_count = cursor.rowcount
                connection.commit()
                cursor.close()
                
                logger.info("Bulk status update completed", 
                          updated_count=updated_count, 
                          status=status.value)
                
                return updated_count
                
        except MySQLError as e:
            logger.error("Failed to bulk update job status", error=str(e))
            raise RepositoryError(f"Failed to bulk update jobs: {e}") from e
    
    def _row_to_job(self, row: dict[str, any]) -> Job:
        """Convert database row to Job entity."""
        return Job(
            id=row['id'],
            uuid=UUID(row['uuid']),
            name=row['name'],
            cron_expression=row['cron_expression'],
            command=row['command'],
            description=row['description'],
            status=JobStatus(row['status']),
            created_at=row['created_at'],
            updated_at=row['updated_at'],
            last_run=row['last_run'],
            next_run=row['next_run'],
            timeout_seconds=row['timeout_seconds'],
            max_retries=row['max_retries'],
            retry_delay_seconds=row['retry_delay_seconds'],
            environment_variables=json.loads(row['environment_variables']) if row['environment_variables'] else {},
            tags=json.loads(row['tags']) if row['tags'] else [],
        )


class MySQLJobExecutionRepository(JobExecutionRepositoryInterface):
    """
    MySQL implementation of the job execution repository.
    
    This class implements the JobExecutionRepositoryInterface following
    the Interface Segregation Principle.
    """
    
    def __init__(self, db_connection: DatabaseConnection) -> None:
        """
        Initialize the MySQL job execution repository.
        
        Args:
            db_connection: Database connection manager.
        """
        self._db = db_connection
    
    async def create(self, execution: JobExecution) -> JobExecution:
        """Create a new job execution record."""
        query = """
            INSERT INTO job_executions (
                uuid, job_id, job_uuid, status, scheduled_time,
                retry_count, environment_variables, execution_metadata
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        
        try:
            async with self._db.get_connection() as connection:
                cursor = connection.cursor()
                
                cursor.execute(query, (
                    str(execution.uuid),
                    execution.job_id,
                    str(execution.job_uuid),
                    execution.status.value,
                    execution.scheduled_time,
                    execution.retry_count,
                    json.dumps(execution.environment_variables),
                    json.dumps(execution.execution_metadata),
                ))
                
                execution.id = cursor.lastrowid
                connection.commit()
                cursor.close()
                
                logger.info("Job execution created", 
                          execution_id=execution.id, 
                          job_id=execution.job_id)
                return execution
                
        except MySQLError as e:
            logger.error("Failed to create job execution", 
                        error=str(e), 
                        job_id=execution.job_id)
            raise RepositoryError(f"Failed to create job execution: {e}") from e
    
    async def get_by_id(self, execution_id: int) -> Optional[JobExecution]:
        """Retrieve a job execution by ID."""
        query = "SELECT * FROM job_executions WHERE id = %s"
        
        try:
            async with self._db.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, (execution_id,))
                row = cursor.fetchone()
                cursor.close()
                
                return self._row_to_execution(row) if row else None
                
        except MySQLError as e:
            logger.error("Failed to get job execution by ID", 
                        error=str(e), 
                        execution_id=execution_id)
            raise RepositoryError(f"Failed to get job execution: {e}") from e
    
    async def get_by_job_id(
        self,
        job_id: int,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> Sequence[JobExecution]:
        """Retrieve executions for a specific job."""
        query = "SELECT * FROM job_executions WHERE job_id = %s ORDER BY scheduled_time DESC"
        params = [job_id]
        
        if limit:
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])
        
        try:
            async with self._db.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, params)
                rows = cursor.fetchall()
                cursor.close()
                
                return [self._row_to_execution(row) for row in rows]
                
        except MySQLError as e:
            logger.error("Failed to get job executions", 
                        error=str(e), 
                        job_id=job_id)
            raise RepositoryError(f"Failed to get job executions: {e}") from e
    
    async def update(self, execution: JobExecution) -> JobExecution:
        """Update an existing job execution."""
        query = """
            UPDATE job_executions SET
                status = %s, started_at = %s, finished_at = %s,
                exit_code = %s, stdout = %s, stderr = %s,
                error_message = %s, retry_count = %s,
                execution_metadata = %s
            WHERE id = %s
        """
        
        try:
            async with self._db.get_connection() as connection:
                cursor = connection.cursor()
                
                cursor.execute(query, (
                    execution.status.value,
                    execution.started_at,
                    execution.finished_at,
                    execution.exit_code,
                    execution.stdout,
                    execution.stderr,
                    execution.error_message,
                    execution.retry_count,
                    json.dumps(execution.execution_metadata),
                    execution.id,
                ))
                
                if cursor.rowcount == 0:
                    raise NotFoundError(f"Job execution with ID {execution.id} not found")
                
                connection.commit()
                cursor.close()
                
                return execution
                
        except MySQLError as e:
            logger.error("Failed to update job execution", 
                        error=str(e), 
                        execution_id=execution.id)
            raise RepositoryError(f"Failed to update job execution: {e}") from e
    
    async def delete_old_executions(
        self,
        older_than: datetime,
        keep_count: Optional[int] = None,
    ) -> int:
        """Delete old execution records."""
        if keep_count:
            # Complex query to keep minimum number per job
            query = """
                DELETE e1 FROM job_executions e1
                LEFT JOIN (
                    SELECT id FROM (
                        SELECT id, 
                               ROW_NUMBER() OVER (PARTITION BY job_id ORDER BY scheduled_time DESC) as rn
                        FROM job_executions
                        WHERE scheduled_time > %s OR 
                              ROW_NUMBER() OVER (PARTITION BY job_id ORDER BY scheduled_time DESC) <= %s
                    ) ranked
                    WHERE rn <= %s
                ) e2 ON e1.id = e2.id
                WHERE e1.scheduled_time < %s AND e2.id IS NULL
            """
            params = [older_than, keep_count, keep_count, older_than]
        else:
            # Simple deletion by date
            query = "DELETE FROM job_executions WHERE scheduled_time < %s"
            params = [older_than]
        
        try:
            async with self._db.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, params)
                
                deleted_count = cursor.rowcount
                connection.commit()
                cursor.close()
                
                logger.info("Old job executions deleted", deleted_count=deleted_count)
                return deleted_count
                
        except MySQLError as e:
            logger.error("Failed to delete old job executions", error=str(e))
            raise RepositoryError(f"Failed to delete old executions: {e}") from e
    
    def _row_to_execution(self, row: dict[str, any]) -> JobExecution:
        """Convert database row to JobExecution entity."""
        return JobExecution(
            id=row['id'],
            uuid=UUID(row['uuid']),
            job_id=row['job_id'],
            job_uuid=UUID(row['job_uuid']),
            status=ExecutionStatus(row['status']),
            scheduled_time=row['scheduled_time'],
            started_at=row['started_at'],
            finished_at=row['finished_at'],
            exit_code=row['exit_code'],
            stdout=row['stdout'] or "",
            stderr=row['stderr'] or "",
            error_message=row['error_message'] or "",
            retry_count=row['retry_count'],
            environment_variables=json.loads(row['environment_variables']) if row['environment_variables'] else {},
            execution_metadata=json.loads(row['execution_metadata']) if row['execution_metadata'] else {},
        )