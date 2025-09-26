"""Logging Example

Demonstrates:
- Different log levels
- File and console logging
- Custom formatters
- Logger configuration
"""
import logging
import os
from datetime import datetime

def setup_basic_logging():
    """Basic logging setup"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def demonstrate_log_levels():
    """Show different logging levels"""
    print("=== Log Levels Demo ===")
    
    logger = logging.getLogger('demo_logger')
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    print()

def setup_file_logging():
    """Setup logging to file"""
    print("=== File Logging Demo ===")
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure file handler
    file_handler = logging.FileHandler('logs/application.log')
    file_handler.setLevel(logging.INFO)
    
    # Configure console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Get logger and add handlers
    logger = logging.getLogger('file_logger')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Test logging
    logger.info("Application started")
    logger.warning("This warning goes to both file and console")
    logger.error("An error occurred")
    
    print("Check logs/application.log for file output")
    print()

def demonstrate_custom_logger():
    """Create custom logger with specific configuration"""
    print("=== Custom Logger Demo ===")
    
    class ColoredFormatter(logging.Formatter):
        """Custom formatter with colors"""
        
        COLORS = {
            'DEBUG': '\033[36m',    # Cyan
            'INFO': '\033[32m',     # Green
            'WARNING': '\033[33m',  # Yellow
            'ERROR': '\033[31m',    # Red
            'CRITICAL': '\033[35m', # Magenta
            'RESET': '\033[0m'      # Reset
        }
        
        def format(self, record):
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"
            return super().format(record)
    
    # Create custom logger
    custom_logger = logging.getLogger('custom')
    custom_logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers
    for handler in custom_logger.handlers[:]:
        custom_logger.removeHandler(handler)
    
    # Create handler with custom formatter
    handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%H:%M:%S'
    )
    handler.setFormatter(formatter)
    custom_logger.addHandler(handler)
    
    # Test custom logger
    custom_logger.debug("Debug message with color")
    custom_logger.info("Info message with color")
    custom_logger.warning("Warning message with color")
    custom_logger.error("Error message with color")
    print()

def demonstrate_exception_logging():
    """Show how to log exceptions"""
    print("=== Exception Logging Demo ===")
    
    logger = logging.getLogger('exception_logger')
    
    try:
        # Simulate an error
        result = 10 / 0
    except ZeroDivisionError:
        logger.exception("Division by zero occurred!")
        # Alternative ways to log exceptions:
        logger.error("Division error", exc_info=True)
    
    try:
        # Another error
        data = {'key': 'value'}
        value = data['missing_key']
    except KeyError as e:
        logger.error(f"Key error: {e}")
    
    print()

def demonstrate_structured_logging():
    """Show structured logging with extra fields"""
    print("=== Structured Logging Demo ===")
    
    logger = logging.getLogger('structured')
    
    # Log with extra context
    logger.info("User logged in", extra={
        'user_id': 12345,
        'ip_address': '192.168.1.100',
        'action': 'login'
    })
    
    # Simulate application events
    events = [
        ('User action', {'user_id': 123, 'action': 'view_page', 'page': '/dashboard'}),
        ('Database query', {'table': 'users', 'duration_ms': 45}),
        ('API call', {'endpoint': '/api/data', 'status_code': 200})
    ]
    
    for message, context in events:
        logger.info(message, extra=context)
    
    print()

class ApplicationLogger:
    """Example of a logger class for an application"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.setup_logger()
    
    def setup_logger(self):
        """Setup logger configuration"""
        if not self.logger.handlers:  # Avoid duplicate handlers
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def log_operation(self, operation: str, success: bool, **kwargs):
        """Log an operation result"""
        level = logging.INFO if success else logging.ERROR
        status = "SUCCESS" if success else "FAILED"
        message = f"Operation '{operation}' {status}"
        
        if kwargs:
            context = ", ".join(f"{k}={v}" for k, v in kwargs.items())
            message += f" - {context}"
        
        self.logger.log(level, message)

def demonstrate_application_logger():
    """Show application logger usage"""
    print("=== Application Logger Demo ===")
    
    app_logger = ApplicationLogger('MyApp')
    
    # Simulate application operations
    app_logger.log_operation('user_registration', True, user_id=456, email='user@example.com')
    app_logger.log_operation('database_backup', True, size_mb=150, duration_sec=45)
    app_logger.log_operation('payment_processing', False, amount=99.99, error='insufficient_funds')
    
    print()

if __name__ == '__main__':
    print("📝 LOGGING EXAMPLES 📝")
    print("=" * 50)
    
    setup_basic_logging()
    
    demonstrate_log_levels()
    setup_file_logging()
    demonstrate_custom_logger()
    demonstrate_exception_logging()
    demonstrate_structured_logging()
    demonstrate_application_logger()
    
    print("✅ Logging examples completed!")