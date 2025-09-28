#!/usr/bin/env python3
"""
Example job script for testing the scheduler.

This script demonstrates what a typical scheduled job might look like.
It performs some work and outputs results that can be captured by the scheduler.
"""

import sys
import time
import json
import random
from datetime import datetime
from pathlib import Path


def main() -> None:
    """Main job function."""
    print(f"Job started at {datetime.now().isoformat()}")
    
    # Simulate some work
    work_duration = random.uniform(1, 5)  # 1-5 seconds
    print(f"Performing work for {work_duration:.2f} seconds...")
    
    for i in range(int(work_duration)):
        print(f"Step {i+1}: Processing data...")
        time.sleep(1)
    
    # Generate some results
    results = {
        "execution_time": datetime.now().isoformat(),
        "work_duration": work_duration,
        "processed_items": random.randint(10, 100),
        "success": True,
    }
    
    print("Results:")
    print(json.dumps(results, indent=2))
    
    # Sometimes simulate failure
    if random.random() < 0.1:  # 10% chance of failure
        print("ERROR: Simulated failure occurred!", file=sys.stderr)
        sys.exit(1)
    
    print(f"Job completed successfully at {datetime.now().isoformat()}")
    sys.exit(0)


if __name__ == "__main__":
    main()