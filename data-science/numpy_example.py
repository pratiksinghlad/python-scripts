"""NumPy Example - Numerical Computing

Demonstrates:
- Array creation and manipulation
- Mathematical operations
- Array reshaping and indexing
- Broadcasting and vectorization
"""
import numpy as np

def demonstrate_array_creation():
    """Show different ways to create NumPy arrays"""
    print("=== Array Creation ===")
    
    # From lists
    arr1 = np.array([1, 2, 3, 4, 5])
    print(f"From list: {arr1}")
    
    # 2D array
    arr2d = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"2D array:\n{arr2d}")
    
    # Special arrays
    zeros = np.zeros((3, 3))
    ones = np.ones((2, 4))
    identity = np.eye(3)
    
    print(f"Zeros (3x3):\n{zeros}")
    print(f"Ones (2x4):\n{ones}")
    print(f"Identity (3x3):\n{identity}")
    
    # Range arrays
    range_arr = np.arange(0, 10, 2)
    linspace_arr = np.linspace(0, 1, 5)
    
    print(f"Range (0 to 10, step 2): {range_arr}")
    print(f"Linspace (0 to 1, 5 points): {linspace_arr}")
    
    # Random arrays
    np.random.seed(42)
    random_arr = np.random.random((2, 3))
    random_int = np.random.randint(1, 10, (2, 3))
    
    print(f"Random floats (0-1):\n{random_arr}")
    print(f"Random integers (1-9):\n{random_int}")
    print()

def demonstrate_array_properties():
    """Show array properties and attributes"""
    print("=== Array Properties ===")
    
    arr = np.random.randint(1, 100, (3, 4, 2))
    
    print(f"Array:\n{arr}")
    print(f"Shape: {arr.shape}")
    print(f"Size: {arr.size}")
    print(f"Dimensions: {arr.ndim}")
    print(f"Data type: {arr.dtype}")
    print(f"Memory usage: {arr.nbytes} bytes")
    print()

def demonstrate_array_operations():
    """Show mathematical operations on arrays"""
    print("=== Array Operations ===")
    
    a = np.array([1, 2, 3, 4])
    b = np.array([5, 6, 7, 8])
    
    print(f"Array a: {a}")
    print(f"Array b: {b}")
    
    # Arithmetic operations
    print(f"a + b = {a + b}")
    print(f"a * b = {a * b}")
    print(f"a ** 2 = {a ** 2}")
    print(f"sqrt(a) = {np.sqrt(a)}")
    
    # Statistical operations
    print(f"Sum of a: {np.sum(a)}")
    print(f"Mean of a: {np.mean(a)}")
    print(f"Max of a: {np.max(a)}")
    print(f"Standard deviation: {np.std(a)}")
    
    # Matrix operations
    matrix_a = np.array([[1, 2], [3, 4]])
    matrix_b = np.array([[5, 6], [7, 8]])
    
    print(f"Matrix A:\n{matrix_a}")
    print(f"Matrix B:\n{matrix_b}")
    print(f"Matrix multiplication:\n{np.dot(matrix_a, matrix_b)}")
    print(f"Element-wise multiplication:\n{matrix_a * matrix_b}")
    print()

def demonstrate_indexing_slicing():
    """Show array indexing and slicing"""
    print("=== Indexing and Slicing ===")
    
    arr = np.arange(20).reshape(4, 5)
    print(f"Original array:\n{arr}")
    
    # Basic indexing
    print(f"Element at [1, 2]: {arr[1, 2]}")
    print(f"First row: {arr[0, :]}")
    print(f"Last column: {arr[:, -1]}")
    
    # Slicing
    print(f"First 2 rows, first 3 columns:\n{arr[:2, :3]}")
    
    # Boolean indexing
    mask = arr > 10
    print(f"Elements > 10: {arr[mask]}")
    
    # Fancy indexing
    rows = [0, 2]
    cols = [1, 3]
    print(f"Elements at positions (0,1) and (2,3): {arr[rows, cols]}")
    print()

def demonstrate_array_manipulation():
    """Show array reshaping and manipulation"""
    print("=== Array Manipulation ===")
    
    arr = np.arange(12)
    print(f"Original: {arr}")
    
    # Reshaping
    reshaped = arr.reshape(3, 4)
    print(f"Reshaped (3x4):\n{reshaped}")
    
    # Transpose
    transposed = reshaped.T
    print(f"Transposed:\n{transposed}")
    
    # Flattening
    flattened = reshaped.flatten()
    print(f"Flattened: {flattened}")
    
    # Concatenation
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([4, 5, 6])
    concatenated = np.concatenate([arr1, arr2])
    print(f"Concatenated: {concatenated}")
    
    # Stacking
    stacked_v = np.vstack([arr1, arr2])
    stacked_h = np.hstack([arr1, arr2])
    print(f"Vertical stack:\n{stacked_v}")
    print(f"Horizontal stack: {stacked_h}")
    print()

def demonstrate_broadcasting():
    """Show NumPy broadcasting"""
    print("=== Broadcasting ===")
    
    # Broadcasting with scalars
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"Original array:\n{arr}")
    print(f"Add 10:\n{arr + 10}")
    
    # Broadcasting with arrays of different shapes
    row_vector = np.array([1, 2, 3])
    col_vector = np.array([[10], [20]])
    
    print(f"Row vector: {row_vector}")
    print(f"Column vector:\n{col_vector}")
    print(f"Broadcasting addition:\n{row_vector + col_vector}")
    print()

def demonstrate_advanced_operations():
    """Show advanced NumPy operations"""
    print("=== Advanced Operations ===")
    
    # Linear algebra
    A = np.random.random((3, 3))
    b = np.random.random(3)
    
    print("Linear algebra:")
    print(f"Determinant: {np.linalg.det(A):.4f}")
    print(f"Eigenvalues: {np.linalg.eigvals(A)}")
    
    # Solve system Ax = b
    try:
        x = np.linalg.solve(A, b)
        print(f"Solution to Ax=b: {x}")
    except np.linalg.LinAlgError:
        print("Matrix is singular, cannot solve")
    
    # Statistics
    data = np.random.normal(0, 1, 1000)
    print(f"\nStatistics (1000 normal samples):")
    print(f"Mean: {np.mean(data):.4f}")
    print(f"Std: {np.std(data):.4f}")
    print(f"25th percentile: {np.percentile(data, 25):.4f}")
    print(f"75th percentile: {np.percentile(data, 75):.4f}")
    
    # Fourier transform (if scipy not available, basic example)
    t = np.linspace(0, 1, 100)
    signal = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 10 * t)
    fft = np.fft.fft(signal)
    print(f"\nFFT of sine wave - first 5 coefficients:")
    print(f"Real parts: {np.real(fft[:5])}")
    print()

def demonstrate_performance():
    """Show performance comparison: NumPy vs pure Python"""
    print("=== Performance Comparison ===")
    
    import time
    
    # Pure Python
    python_list = list(range(1000000))
    
    start = time.time()
    python_result = [x ** 2 for x in python_list]
    python_time = time.time() - start
    
    # NumPy
    numpy_array = np.arange(1000000)
    
    start = time.time()
    numpy_result = numpy_array ** 2
    numpy_time = time.time() - start
    
    print(f"Squaring 1,000,000 numbers:")
    print(f"Pure Python time: {python_time:.4f} seconds")
    print(f"NumPy time: {numpy_time:.4f} seconds")
    print(f"NumPy is {python_time/numpy_time:.1f}x faster")
    print()

if __name__ == '__main__':
    print("🔢 NUMPY EXAMPLES 🔢")
    print("=" * 50)
    
    try:
        demonstrate_array_creation()
        demonstrate_array_properties()
        demonstrate_array_operations()
        demonstrate_indexing_slicing()
        demonstrate_array_manipulation()
        demonstrate_broadcasting()
        demonstrate_advanced_operations()
        demonstrate_performance()
    except ImportError:
        print("❌ NumPy not installed. Install with: pip install numpy")
    except Exception as e:
        print(f"❌ Error: {e}")