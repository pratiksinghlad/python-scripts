"""Pandas Example - Data Analysis and Manipulation

Demonstrates:
- Creating DataFrames
- Data manipulation and filtering
- Reading/writing CSV files
- Basic statistics and operations
"""
import pandas as pd
import numpy as np
import os

def create_sample_data():
    """Create sample dataset"""
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'age': [25, 30, 35, 28, 32],
        'salary': [50000, 60000, 70000, 55000, 65000],
        'department': ['IT', 'HR', 'Finance', 'IT', 'Marketing'],
        'join_date': ['2020-01-15', '2019-05-20', '2018-03-10', '2021-07-01', '2020-11-30']
    }
    return pd.DataFrame(data)

def demonstrate_dataframe_operations():
    """Show basic DataFrame operations"""
    print("=== DataFrame Operations ===")
    
    # Create DataFrame
    df = create_sample_data()
    print("Original DataFrame:")
    print(df)
    print()
    
    # Basic info
    print("DataFrame Info:")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print()
    
    # Data selection
    print("IT Department employees:")
    it_employees = df[df['department'] == 'IT']
    print(it_employees)
    print()
    
    # Statistics
    print("Salary statistics:")
    print(df['salary'].describe())
    print()
    
    # Group by operations
    print("Average salary by department:")
    avg_salary = df.groupby('department')['salary'].mean()
    print(avg_salary)
    print()
    
    return df

def demonstrate_data_manipulation():
    """Show data manipulation techniques"""
    print("=== Data Manipulation ===")
    
    df = create_sample_data()
    
    # Convert join_date to datetime
    df['join_date'] = pd.to_datetime(df['join_date'])
    
    # Add new column
    df['salary_category'] = df['salary'].apply(
        lambda x: 'High' if x >= 60000 else 'Medium' if x >= 55000 else 'Low'
    )
    
    # Sort by salary
    df_sorted = df.sort_values('salary', ascending=False)
    print("Employees sorted by salary (highest first):")
    print(df_sorted[['name', 'salary', 'salary_category']])
    print()
    
    # Filter and transform
    high_earners = df[df['salary'] >= 60000].copy()
    high_earners['bonus'] = high_earners['salary'] * 0.1
    print("High earners with bonus (10% of salary):")
    print(high_earners[['name', 'salary', 'bonus']])
    print()

def demonstrate_file_operations():
    """Show CSV reading and writing"""
    print("=== File Operations ===")
    
    df = create_sample_data()
    csv_file = 'sample_employees.csv'
    
    # Write to CSV
    df.to_csv(csv_file, index=False)
    print(f"Data saved to {csv_file}")
    
    # Read from CSV
    df_loaded = pd.read_csv(csv_file)
    print("Data loaded from CSV:")
    print(df_loaded.head())
    print()
    
    # Clean up
    if os.path.exists(csv_file):
        os.remove(csv_file)
        print(f"Cleaned up {csv_file}")

def demonstrate_advanced_operations():
    """Show more advanced pandas operations"""
    print("=== Advanced Operations ===")
    
    # Create larger dataset
    np.random.seed(42)
    large_data = {
        'product': ['A', 'B', 'C'] * 100,
        'sales': np.random.randint(100, 1000, 300),
        'region': ['North', 'South', 'East', 'West'] * 75,
        'quarter': ['Q1', 'Q2', 'Q3', 'Q4'] * 75
    }
    df_sales = pd.DataFrame(large_data)
    
    # Pivot table
    pivot = pd.pivot_table(df_sales, 
                          values='sales', 
                          index='product', 
                          columns='region', 
                          aggfunc='sum')
    print("Sales by Product and Region (Pivot Table):")
    print(pivot)
    print()
    
    # Cross-tabulation
    crosstab = pd.crosstab(df_sales['product'], df_sales['quarter'])
    print("Product counts by Quarter:")
    print(crosstab)
    print()

if __name__ == '__main__':
    print("🐼 PANDAS EXAMPLES 🐼")
    print("=" * 50)
    
    try:
        demonstrate_dataframe_operations()
        demonstrate_data_manipulation()
        demonstrate_file_operations()
        demonstrate_advanced_operations()
    except ImportError:
        print("❌ pandas not installed. Install with: pip install pandas")
    except Exception as e:
        print(f"❌ Error: {e}")