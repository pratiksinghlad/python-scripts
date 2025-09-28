"""
Database connection management.

This module provides database connection and connection pool management
using MySQL Connector/Python with proper resource management and error handling.
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional, Any
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector import Error as MySQLError
import structlog

from ...config.settings import DatabaseSettings


logger = structlog.get_logger(__name__)


class DatabaseConnectionError(Exception):
    """Raised when database connection operations fail."""
    pass


class DatabaseConnection:
    """
    Database connection manager with connection pooling.
    
    This class follows the Single Responsibility Principle by focusing
    solely on database connection management and provides a clean interface
    for database operations.
    """
    
    def __init__(self, settings: DatabaseSettings) -> None:
        """
        Initialize the database connection manager.
        
        Args:
            settings: Database configuration settings.
        """
        self._settings = settings
        self._pool: Optional[MySQLConnectionPool] = None
        self._is_initialized = False
    
    async def initialize(self) -> None:
        """
        Initialize the connection pool.
        
        Raises:
            DatabaseConnectionError: If initialization fails.
        """
        if self._is_initialized:
            return
        
        try:
            # Create connection pool configuration
            pool_config = {
                'pool_name': 'job_scheduler_pool',
                'pool_size': self._settings.pool_size,
                'pool_reset_session': True,
                'host': self._settings.host,
                'port': self._settings.port,
                'database': self._settings.name,
                'user': self._settings.user,
                'password': self._settings.password,
                'charset': 'utf8mb4',
                'collation': 'utf8mb4_unicode_ci',
                'autocommit': False,
                'time_zone': '+00:00',  # Use UTC
                'sql_mode': 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO',
            }
            
            # Create connection pool
            self._pool = MySQLConnectionPool(**pool_config)
            
            # Test connection
            await self._test_connection()
            
            self._is_initialized = True
            logger.info("Database connection pool initialized", pool_size=self._settings.pool_size)
            
        except MySQLError as e:
            logger.error("Failed to initialize database connection pool", error=str(e))
            raise DatabaseConnectionError(f"Database initialization failed: {e}") from e
    
    async def close(self) -> None:
        """Close all connections in the pool."""
        if self._pool is not None:
            try:
                # MySQL Connector/Python doesn't provide explicit pool closure
                # The pool will be garbage collected
                self._pool = None
                self._is_initialized = False
                logger.info("Database connection pool closed")
            except Exception as e:
                logger.error("Error closing database connection pool", error=str(e))
    
    @asynccontextmanager
    async def get_connection(self) -> AsyncIterator[mysql.connector.MySQLConnection]:
        """
        Get a database connection from the pool.
        
        Yields:
            MySQL database connection.
            
        Raises:
            DatabaseConnectionError: If connection cannot be obtained.
        """
        if not self._is_initialized or self._pool is None:
            raise DatabaseConnectionError("Database connection pool not initialized")
        
        connection = None
        try:
            # Get connection from pool
            connection = self._pool.get_connection()
            
            # Ensure connection is valid
            if not connection.is_connected():
                connection.reconnect()
            
            yield connection
            
        except MySQLError as e:
            logger.error("Database connection error", error=str(e))
            if connection:
                try:
                    connection.rollback()
                except MySQLError:
                    pass  # Ignore rollback errors
            raise DatabaseConnectionError(f"Database operation failed: {e}") from e
        
        finally:
            if connection and connection.is_connected():
                try:
                    connection.close()
                except MySQLError as e:
                    logger.error("Error closing database connection", error=str(e))
    
    async def execute_migration(self, migration_sql: str) -> None:
        """
        Execute a database migration script.
        
        Args:
            migration_sql: SQL migration script to execute.
            
        Raises:
            DatabaseConnectionError: If migration fails.
        """
        async with self.get_connection() as connection:
            try:
                cursor = connection.cursor()
                
                # Split SQL into individual statements
                statements = [stmt.strip() for stmt in migration_sql.split(';') if stmt.strip()]
                
                for statement in statements:
                    cursor.execute(statement)
                
                connection.commit()
                logger.info("Database migration executed successfully")
                
            except MySQLError as e:
                logger.error("Database migration failed", error=str(e))
                connection.rollback()
                raise DatabaseConnectionError(f"Migration failed: {e}") from e
            finally:
                cursor.close()
    
    async def check_health(self) -> dict[str, Any]:
        """
        Check database connection health.
        
        Returns:
            Dictionary containing health information.
        """
        try:
            async with self.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT 1 as health_check")
                result = cursor.fetchone()
                cursor.close()
                
                return {
                    "healthy": True,
                    "database": self._settings.name,
                    "host": self._settings.host,
                    "port": self._settings.port,
                    "pool_size": self._settings.pool_size,
                    "test_query_result": result[0] if result else None,
                }
                
        except Exception as e:
            logger.error("Database health check failed", error=str(e))
            return {
                "healthy": False,
                "error": str(e),
                "database": self._settings.name,
                "host": self._settings.host,
                "port": self._settings.port,
            }
    
    async def _test_connection(self) -> None:
        """
        Test database connection.
        
        Raises:
            DatabaseConnectionError: If connection test fails.
        """
        try:
            async with self.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                cursor.close()
                
                logger.info("Database connection test successful", mysql_version=version[0])
                
        except Exception as e:
            raise DatabaseConnectionError(f"Database connection test failed: {e}") from e
    
    @property
    def is_initialized(self) -> bool:
        """Check if the connection pool is initialized."""
        return self._is_initialized