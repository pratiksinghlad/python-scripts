"""
Application settings and configuration.

This module defines the application configuration using Pydantic settings
for type safety and validation. It follows the Open/Closed Principle by
allowing configuration extension without modification.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, validator
from pydantic_settings import BaseSettings as PydanticBaseSettings


class DatabaseSettings(PydanticBaseSettings):
    """Database configuration settings."""
    
    host: str = "localhost"
    port: int = 3306
    name: str = "job_scheduler"
    user: str = "root"
    password: str = ""
    pool_size: int = 10
    max_overflow: int = 20
    
    class Config:
        env_prefix = "DB_"
        case_sensitive = False


class ApplicationSettings(PydanticBaseSettings):
    """Application configuration settings."""
    
    debug: bool = False
    testing: bool = False
    log_level: str = "INFO"
    max_concurrent_jobs: int = 5
    job_timeout: int = 300
    scheduler_interval: int = 30
    secret_key: Optional[str] = None
    
    @validator('log_level')
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        if v.upper() not in valid_levels:
            raise ValueError(f'Log level must be one of {valid_levels}')
        return v.upper()
    
    @validator('max_concurrent_jobs')
    def validate_max_concurrent_jobs(cls, v):
        """Validate max concurrent jobs."""
        if v <= 0:
            raise ValueError('Max concurrent jobs must be positive')
        return v
    
    @validator('job_timeout')
    def validate_job_timeout(cls, v):
        """Validate job timeout."""
        if v <= 0:
            raise ValueError('Job timeout must be positive')
        return v
    
    @validator('scheduler_interval')
    def validate_scheduler_interval(cls, v):
        """Validate scheduler interval."""
        if v <= 0:
            raise ValueError('Scheduler interval must be positive')
        return v
    
    class Config:
        env_prefix = ""
        case_sensitive = False


class Settings:
    """
    Main settings class that aggregates all configuration.
    
    This class follows the Single Responsibility Principle by focusing
    on configuration management and providing a centralized access point
    for all application settings.
    """
    
    def __init__(self, env_file: Optional[Path] = None) -> None:
        """
        Initialize settings.
        
        Args:
            env_file: Optional path to .env file.
        """
        # Load environment variables from .env file if it exists
        if env_file is None:
            env_file = Path(".env")
        
        self._env_file = env_file
        self._load_env_file()
        
        # Initialize settings sections
        self.database = DatabaseSettings()
        self.app = ApplicationSettings()
    
    def _load_env_file(self) -> None:
        """Load environment variables from .env file."""
        if self._env_file.exists():
            from dotenv import load_dotenv
            load_dotenv(self._env_file)
    
    def get_database_url(self) -> str:
        """
        Get database connection URL.
        
        Returns:
            Database connection URL string.
        """
        return (
            f"mysql://{self.database.user}:{self.database.password}"
            f"@{self.database.host}:{self.database.port}/{self.database.name}"
        )
    
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.app.debug
    
    def is_testing(self) -> bool:
        """Check if running in testing mode."""
        return self.app.testing
    
    def to_dict(self) -> dict[str, any]:
        """
        Convert settings to dictionary (excluding sensitive data).
        
        Returns:
            Dictionary representation of settings.
        """
        return {
            "database": {
                "host": self.database.host,
                "port": self.database.port,
                "name": self.database.name,
                "user": self.database.user,
                "pool_size": self.database.pool_size,
                "max_overflow": self.database.max_overflow,
                # Exclude password for security
            },
            "application": {
                "debug": self.app.debug,
                "testing": self.app.testing,
                "log_level": self.app.log_level,
                "max_concurrent_jobs": self.app.max_concurrent_jobs,
                "job_timeout": self.app.job_timeout,
                "scheduler_interval": self.app.scheduler_interval,
                # Exclude secret_key for security
            },
        }


# Global settings instance
_settings: Optional[Settings] = None


def get_settings(env_file: Optional[Path] = None) -> Settings:
    """
    Get the global settings instance.
    
    This function implements the Singleton pattern to ensure consistent
    configuration throughout the application.
    
    Args:
        env_file: Optional path to .env file.
        
    Returns:
        Settings instance.
    """
    global _settings
    
    if _settings is None:
        _settings = Settings(env_file)
    
    return _settings


def reset_settings() -> None:
    """Reset the global settings instance (mainly for testing)."""
    global _settings
    _settings = None