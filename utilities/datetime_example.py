"""DateTime Example - Date and Time Handling

Demonstrates:
- Creating and formatting dates/times
- Date arithmetic and comparisons
- Timezones and UTC
- Parsing strings to dates
- Working with time periods
"""
from datetime import datetime, date, time, timedelta, timezone
import time as time_module

def demonstrate_basic_datetime():
    """Show basic date and time operations"""
    print("=== Basic DateTime Operations ===")
    
    # Current date and time
    now = datetime.now()
    today = date.today()
    current_time = datetime.now().time()
    
    print(f"Current datetime: {now}")
    print(f"Today's date: {today}")
    print(f"Current time: {current_time}")
    
    # Creating specific dates
    specific_date = date(2024, 12, 25)  # Christmas 2024
    specific_datetime = datetime(2024, 12, 25, 10, 30, 0)
    specific_time = time(14, 30, 45)
    
    print(f"Christmas 2024: {specific_date}")
    print(f"Specific datetime: {specific_datetime}")
    print(f"Specific time: {specific_time}")
    print()

def demonstrate_formatting():
    """Show date/time formatting"""
    print("=== Date/Time Formatting ===")
    
    now = datetime.now()
    
    # Common formatting patterns
    formats = [
        ("%Y-%m-%d", "ISO date"),
        ("%Y-%m-%d %H:%M:%S", "ISO datetime"),
        ("%B %d, %Y", "Long date"),
        ("%A, %B %d, %Y", "Full date"),
        ("%I:%M %p", "12-hour time"),
        ("%H:%M:%S", "24-hour time"),
        ("%Y-%m-%d %I:%M %p", "Date with 12-hour time")
    ]
    
    print(f"Current datetime: {now}")
    print("Formatted outputs:")
    for fmt, description in formats:
        formatted = now.strftime(fmt)
        print(f"  {description}: {formatted}")
    print()

def demonstrate_parsing():
    """Show parsing strings to datetime objects"""
    print("=== Parsing Strings to DateTime ===")
    
    date_strings = [
        ("2024-03-15", "%Y-%m-%d"),
        ("March 15, 2024", "%B %d, %Y"),
        ("15/03/2024", "%d/%m/%Y"),
        ("2024-03-15 14:30:00", "%Y-%m-%d %H:%M:%S"),
        ("Mar 15 2024 2:30 PM", "%b %d %Y %I:%M %p")
    ]
    
    for date_str, fmt in date_strings:
        try:
            parsed = datetime.strptime(date_str, fmt)
            print(f"'{date_str}' -> {parsed}")
        except ValueError as e:
            print(f"Failed to parse '{date_str}': {e}")
    print()

def demonstrate_arithmetic():
    """Show date/time arithmetic"""
    print("=== Date/Time Arithmetic ===")
    
    now = datetime.now()
    print(f"Starting datetime: {now}")
    
    # Adding/subtracting time
    one_hour_later = now + timedelta(hours=1)
    one_day_ago = now - timedelta(days=1)
    one_week_later = now + timedelta(weeks=1)
    mixed_delta = now + timedelta(days=5, hours=3, minutes=30)
    
    print(f"One hour later: {one_hour_later}")
    print(f"One day ago: {one_day_ago}")
    print(f"One week later: {one_week_later}")
    print(f"5 days, 3 hours, 30 minutes later: {mixed_delta}")
    
    # Difference between dates
    future_date = datetime(2025, 1, 1)
    difference = future_date - now
    
    print(f"Days until 2025: {difference.days}")
    print(f"Total seconds until 2025: {difference.total_seconds()}")
    print()

def demonstrate_comparisons():
    """Show date/time comparisons"""
    print("=== Date/Time Comparisons ===")
    
    date1 = datetime(2024, 1, 1)
    date2 = datetime(2024, 6, 1)
    date3 = datetime(2024, 1, 1)
    
    print(f"Date1: {date1}")
    print(f"Date2: {date2}")
    print(f"Date3: {date3}")
    
    print(f"date1 < date2: {date1 < date2}")
    print(f"date1 == date3: {date1 == date3}")
    print(f"date2 > date1: {date2 > date1}")
    
    # Finding min/max dates
    dates = [date1, date2, date3, datetime.now()]
    print(f"Earliest date: {min(dates)}")
    print(f"Latest date: {max(dates)}")
    print()

def demonstrate_timezones():
    """Show timezone handling"""
    print("=== Timezone Handling ===")
    
    # UTC timezone
    utc_now = datetime.now(timezone.utc)
    print(f"Current UTC time: {utc_now}")
    
    # Custom timezone offset
    custom_tz = timezone(timedelta(hours=5, minutes=30))  # +5:30 (India)
    custom_time = datetime.now(custom_tz)
    print(f"Time in +5:30 timezone: {custom_time}")
    
    # Converting between timezones
    utc_time = datetime.now(timezone.utc)
    local_time = utc_time.replace(tzinfo=None)  # Remove timezone info
    
    print(f"UTC time: {utc_time}")
    print(f"As local time: {local_time}")
    
    try:
        import zoneinfo  # Python 3.9+
        ny_tz = zoneinfo.ZoneInfo("America/New_York")
        ny_time = utc_time.astimezone(ny_tz)
        print(f"New York time: {ny_time}")
    except ImportError:
        print("zoneinfo not available (Python 3.9+)")
    
    print()

def demonstrate_timestamps():
    """Show Unix timestamp handling"""
    print("=== Unix Timestamps ===")
    
    now = datetime.now()
    timestamp = now.timestamp()
    
    print(f"Current datetime: {now}")
    print(f"Unix timestamp: {timestamp}")
    
    # Convert timestamp back to datetime
    from_timestamp = datetime.fromtimestamp(timestamp)
    print(f"From timestamp: {from_timestamp}")
    
    # UTC timestamp
    utc_timestamp = datetime.utcnow().timestamp()
    from_utc_timestamp = datetime.utcfromtimestamp(utc_timestamp)
    
    print(f"UTC timestamp: {utc_timestamp}")
    print(f"From UTC timestamp: {from_utc_timestamp}")
    print()

def demonstrate_performance_timing():
    """Show how to measure execution time"""
    print("=== Performance Timing ===")
    
    # Using time module
    start_time = time_module.time()
    # Simulate some work
    sum([i**2 for i in range(100000)])
    end_time = time_module.time()
    
    execution_time = end_time - start_time
    print(f"Execution time (time module): {execution_time:.4f} seconds")
    
    # Using datetime
    start_datetime = datetime.now()
    # Simulate some work
    sum([i**3 for i in range(100000)])
    end_datetime = datetime.now()
    
    duration = end_datetime - start_datetime
    print(f"Execution time (datetime): {duration.total_seconds():.4f} seconds")
    print()

class DateTimeHelper:
    """Utility class for common datetime operations"""
    
    @staticmethod
    def age_in_years(birth_date: date) -> int:
        """Calculate age in years"""
        today = date.today()
        age = today.year - birth_date.year
        # Adjust if birthday hasn't occurred this year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        return age
    
    @staticmethod
    def days_between(date1: date, date2: date) -> int:
        """Calculate days between two dates"""
        return abs((date2 - date1).days)
    
    @staticmethod
    def next_weekday(target_weekday: int) -> date:
        """Find next occurrence of a weekday (0=Monday, 6=Sunday)"""
        today = date.today()
        days_ahead = target_weekday - today.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return today + timedelta(days_ahead)
    
    @staticmethod
    def quarter_start(dt: date) -> date:
        """Get the start date of the quarter for given date"""
        quarter_starts = {
            1: (1, 1), 2: (1, 1), 3: (1, 1),  # Q1
            4: (4, 1), 5: (4, 1), 6: (4, 1),  # Q2
            7: (7, 1), 8: (7, 1), 9: (7, 1),  # Q3
            10: (10, 1), 11: (10, 1), 12: (10, 1)  # Q4
        }
        month, day = quarter_starts[dt.month]
        return date(dt.year, month, day)

def demonstrate_utility_class():
    """Show usage of datetime utility class"""
    print("=== DateTime Utility Class ===")
    
    # Age calculation
    birth_date = date(1990, 5, 15)
    age = DateTimeHelper.age_in_years(birth_date)
    print(f"Birth date: {birth_date}")
    print(f"Age: {age} years")
    
    # Days between dates
    date1 = date(2024, 1, 1)
    date2 = date(2024, 12, 31)
    days = DateTimeHelper.days_between(date1, date2)
    print(f"Days between {date1} and {date2}: {days}")
    
    # Next weekday
    next_friday = DateTimeHelper.next_weekday(4)  # Friday is 4
    print(f"Next Friday: {next_friday}")
    
    # Quarter start
    today = date.today()
    quarter_start = DateTimeHelper.quarter_start(today)
    print(f"Current quarter started: {quarter_start}")
    print()

if __name__ == '__main__':
    print("📅 DATETIME EXAMPLES 📅")
    print("=" * 50)
    
    demonstrate_basic_datetime()
    demonstrate_formatting()
    demonstrate_parsing()
    demonstrate_arithmetic()
    demonstrate_comparisons()
    demonstrate_timezones()
    demonstrate_timestamps()
    demonstrate_performance_timing()
    demonstrate_utility_class()
    
    print("✅ DateTime examples completed!")