"""File Handling and JSON Example

Demonstrates:
- Reading and writing text files
- JSON serialization/deserialization
- CSV file handling
- File paths and directories
- Context managers and error handling
"""
import json
import csv
import os
from pathlib import Path
from typing import List, Dict, Any

def demonstrate_basic_file_operations():
    """Show basic file read/write operations"""
    print("=== Basic File Operations ===")
    
    # Write to a text file
    filename = "sample.txt"
    content = """Hello, World!
This is a sample text file.
It contains multiple lines.
We can read and write it with Python."""
    
    # Writing file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Written content to {filename}")
    
    # Reading file
    with open(filename, 'r', encoding='utf-8') as f:
        read_content = f.read()
    
    print("📖 File content:")
    print(read_content)
    
    # Reading line by line
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"📝 File has {len(lines)} lines:")
    for i, line in enumerate(lines, 1):
        print(f"  Line {i}: {line.strip()}")
    
    # Clean up
    os.remove(filename)
    print(f"🗑️ Cleaned up {filename}")
    print()

def demonstrate_json_operations():
    """Show JSON serialization and deserialization"""
    print("=== JSON Operations ===")
    
    # Sample data
    data = {
        "users": [
            {"id": 1, "name": "Alice", "age": 30, "active": True},
            {"id": 2, "name": "Bob", "age": 25, "active": False},
            {"id": 3, "name": "Charlie", "age": 35, "active": True}
        ],
        "metadata": {
            "version": "1.0",
            "created": "2024-01-01",
            "total_users": 3
        }
    }
    
    json_filename = "users.json"
    
    # Write JSON to file
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Written JSON data to {json_filename}")
    
    # Read JSON from file
    with open(json_filename, 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)
    
    print("📖 Loaded JSON data:")
    print(f"  Total users: {loaded_data['metadata']['total_users']}")
    for user in loaded_data['users']:
        status = "Active" if user['active'] else "Inactive"
        print(f"  - {user['name']} (ID: {user['id']}, Age: {user['age']}) - {status}")
    
    # JSON string operations
    json_string = json.dumps(data, indent=2)
    print(f"JSON as string (first 100 chars): {json_string[:100]}...")
    
    parsed_from_string = json.loads(json_string)
    print(f"Parsed from string - version: {parsed_from_string['metadata']['version']}")
    
    # Clean up
    os.remove(json_filename)
    print(f"🗑️ Cleaned up {json_filename}")
    print()

def demonstrate_csv_operations():
    """Show CSV file handling"""
    print("=== CSV Operations ===")
    
    csv_filename = "employees.csv"
    
    # Sample CSV data
    employees = [
        {"name": "Alice Johnson", "department": "IT", "salary": 75000, "years": 3},
        {"name": "Bob Smith", "department": "HR", "salary": 65000, "years": 5},
        {"name": "Charlie Brown", "department": "Finance", "salary": 80000, "years": 2},
        {"name": "Diana Prince", "department": "IT", "salary": 70000, "years": 4}
    ]
    
    # Write CSV
    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        if employees:
            fieldnames = employees[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(employees)
    
    print(f"✅ Written CSV data to {csv_filename}")
    
    # Read CSV
    with open(csv_filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        loaded_employees = list(reader)
    
    print("📖 Loaded CSV data:")
    for emp in loaded_employees:
        print(f"  - {emp['name']}: {emp['department']}, ${emp['salary']}, {emp['years']} years")
    
    # CSV with custom operations
    print("\nFiltered data (IT department only):")
    it_employees = [emp for emp in loaded_employees if emp['department'] == 'IT']
    for emp in it_employees:
        print(f"  - {emp['name']}: ${emp['salary']}")
    
    # Clean up
    os.remove(csv_filename)
    print(f"🗑️ Cleaned up {csv_filename}")
    print()

def demonstrate_path_operations():
    """Show file path and directory operations"""
    print("=== Path and Directory Operations ===")
    
    # Current directory
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Path manipulation
    file_path = Path("data") / "subfolder" / "file.txt"
    print(f"Constructed path: {file_path}")
    print(f"Parent directory: {file_path.parent}")
    print(f"Filename: {file_path.name}")
    print(f"File extension: {file_path.suffix}")
    print(f"Stem (name without extension): {file_path.stem}")
    
    # Create directory structure
    test_dir = Path("test_directory")
    sub_dir = test_dir / "subdirectory"
    
    sub_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created directory: {sub_dir}")
    
    # Create a test file
    test_file = sub_dir / "test_file.txt"
    test_file.write_text("This is a test file.", encoding='utf-8')
    print(f"✅ Created file: {test_file}")
    
    # List directory contents
    print(f"Contents of {test_dir}:")
    for item in test_dir.rglob("*"):
        if item.is_file():
            print(f"  📄 File: {item}")
        elif item.is_dir():
            print(f"  📁 Directory: {item}")
    
    # File properties
    if test_file.exists():
        stat = test_file.stat()
        print(f"File size: {stat.st_size} bytes")
        print(f"File exists: {test_file.exists()}")
        print(f"Is file: {test_file.is_file()}")
    
    # Clean up
    test_file.unlink()  # Delete file
    sub_dir.rmdir()     # Delete empty directory
    test_dir.rmdir()    # Delete empty directory
    print(f"🗑️ Cleaned up test directories")
    print()

def demonstrate_error_handling():
    """Show file operation error handling"""
    print("=== Error Handling ===")
    
    # File not found
    try:
        with open("nonexistent_file.txt", 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ File not found error handled")
    
    # Permission errors (simulated)
    try:
        # Try to write to a read-only file (if we could create one)
        readonly_file = "readonly_test.txt"
        
        # Create and immediately try to open in conflicting modes
        with open(readonly_file, 'w') as f:
            f.write("test")
        
        # This should work fine, but demonstrates the pattern
        with open(readonly_file, 'r') as f:
            content = f.read()
            print(f"✅ Successfully read: '{content}'")
        
        os.remove(readonly_file)
        
    except PermissionError:
        print("❌ Permission error handled")
    except Exception as e:
        print(f"❌ Other error handled: {e}")
    
    # JSON decode error
    try:
        invalid_json = '{"name": "Alice", "age": 30,}'  # Invalid trailing comma
        data = json.loads(invalid_json)
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error handled: {e}")
    
    print()

class FileManager:
    """Utility class for file operations"""
    
    def __init__(self, base_directory: str = "."):
        self.base_dir = Path(base_directory)
        self.base_dir.mkdir(exist_ok=True)
    
    def save_json(self, filename: str, data: Any) -> bool:
        """Save data as JSON file"""
        try:
            file_path = self.base_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving JSON: {e}")
            return False
    
    def load_json(self, filename: str) -> Any:
        """Load data from JSON file"""
        try:
            file_path = self.base_dir / filename
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading JSON: {e}")
            return None
    
    def save_csv(self, filename: str, data: List[Dict[str, Any]]) -> bool:
        """Save list of dictionaries as CSV"""
        try:
            if not data:
                return False
            
            file_path = self.base_dir / filename
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
            return False
    
    def load_csv(self, filename: str) -> List[Dict[str, Any]]:
        """Load CSV as list of dictionaries"""
        try:
            file_path = self.base_dir / filename
            with open(file_path, 'r', encoding='utf-8') as f:
                return list(csv.DictReader(f))
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            return []
    
    def list_files(self, pattern: str = "*") -> List[Path]:
        """List files matching pattern"""
        return list(self.base_dir.glob(pattern))

def demonstrate_file_manager():
    """Show usage of FileManager class"""
    print("=== FileManager Class Demo ===")
    
    fm = FileManager("temp_files")
    
    # Save and load JSON
    sample_data = {"name": "Test", "items": [1, 2, 3], "active": True}
    
    if fm.save_json("test.json", sample_data):
        print("✅ JSON saved successfully")
        
        loaded = fm.load_json("test.json")
        if loaded:
            print(f"📖 Loaded JSON: {loaded}")
    
    # Save and load CSV
    csv_data = [
        {"id": 1, "name": "Item1", "price": 10.99},
        {"id": 2, "name": "Item2", "price": 15.50}
    ]
    
    if fm.save_csv("items.csv", csv_data):
        print("✅ CSV saved successfully")
        
        loaded_csv = fm.load_csv("items.csv")
        if loaded_csv:
            print(f"📖 Loaded CSV ({len(loaded_csv)} rows)")
    
    # List files
    files = fm.list_files()
    print(f"📁 Files in temp directory: {[f.name for f in files]}")
    
    # Clean up
    for file in files:
        file.unlink()
    fm.base_dir.rmdir()
    print("🗑️ Cleaned up temp files")
    print()

if __name__ == '__main__':
    print("📁 FILE HANDLING & JSON EXAMPLES 📁")
    print("=" * 50)
    
    demonstrate_basic_file_operations()
    demonstrate_json_operations()
    demonstrate_csv_operations()
    demonstrate_path_operations()
    demonstrate_error_handling()
    demonstrate_file_manager()
    
    print("✅ File handling examples completed!")