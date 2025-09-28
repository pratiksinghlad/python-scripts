-- Initial database schema for the job scheduler
-- This creates the necessary tables for jobs and job executions

-- Jobs table
CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uuid CHAR(36) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL UNIQUE,
    cron_expression VARCHAR(100) NOT NULL,
    command TEXT NOT NULL,
    description TEXT DEFAULT '',
    status ENUM('active', 'inactive', 'paused', 'deleted') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_run TIMESTAMP NULL,
    next_run TIMESTAMP NULL,
    timeout_seconds INT DEFAULT 300,
    max_retries INT DEFAULT 3,
    retry_delay_seconds INT DEFAULT 60,
    environment_variables JSON DEFAULT '{}',
    tags JSON DEFAULT '[]',
    
    INDEX idx_status (status),
    INDEX idx_next_run (next_run),
    INDEX idx_name (name),
    INDEX idx_uuid (uuid),
    INDEX idx_created_at (created_at),
    INDEX idx_status_next_run (status, next_run)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Job executions table
CREATE TABLE IF NOT EXISTS job_executions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uuid CHAR(36) NOT NULL UNIQUE,
    job_id INT NOT NULL,
    job_uuid CHAR(36) NOT NULL,
    status ENUM('pending', 'running', 'success', 'failed', 'timeout', 'cancelled', 'retrying') DEFAULT 'pending',
    scheduled_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP NULL,
    finished_at TIMESTAMP NULL,
    exit_code INT NULL,
    stdout LONGTEXT DEFAULT '',
    stderr LONGTEXT DEFAULT '',
    error_message TEXT DEFAULT '',
    retry_count INT DEFAULT 0,
    environment_variables JSON DEFAULT '{}',
    execution_metadata JSON DEFAULT '{}',
    
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    
    INDEX idx_job_id (job_id),
    INDEX idx_job_uuid (job_uuid),
    INDEX idx_status (status),
    INDEX idx_scheduled_time (scheduled_time),
    INDEX idx_job_id_scheduled (job_id, scheduled_time DESC),
    INDEX idx_status_scheduled (status, scheduled_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;