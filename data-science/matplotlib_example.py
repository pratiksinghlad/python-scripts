"""Matplotlib Example - Data Visualization

Demonstrates:
- Basic plotting (line, scatter, bar)
- Subplots and multiple axes
- Customization (colors, labels, styles)
- Different plot types
- Saving plots to files
"""
import numpy as np

def demonstrate_basic_plotting():
    """Show basic line plots"""
    print("=== Basic Line Plotting ===")
    
    try:
        import matplotlib.pyplot as plt
        
        # Generate sample data
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)
        
        # Create basic line plot
        plt.figure(figsize=(10, 6))
        plt.plot(x, y1, label='sin(x)', color='blue', linewidth=2)
        plt.plot(x, y2, label='cos(x)', color='red', linestyle='--', linewidth=2)
        
        plt.title('Sine and Cosine Functions')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save plot
        plt.savefig('basic_plot.png', dpi=150, bbox_inches='tight')
        print("✅ Basic plot saved as 'basic_plot.png'")
        plt.close()
        
    except ImportError:
        print("❌ matplotlib not installed. Install with: pip install matplotlib")
        print("Showing plotting concepts without actual visualization...")

def demonstrate_scatter_plots():
    """Show scatter plots"""
    print("=== Scatter Plots ===")
    
    try:
        import matplotlib.pyplot as plt
        
        # Generate random data
        np.random.seed(42)
        n_points = 100
        x = np.random.normal(0, 1, n_points)
        y = 2 * x + np.random.normal(0, 0.5, n_points)
        colors = np.random.rand(n_points)
        sizes = 1000 * np.random.rand(n_points)
        
        plt.figure(figsize=(8, 6))
        scatter = plt.scatter(x, y, c=colors, s=sizes, alpha=0.6, cmap='viridis')
        
        plt.title('Scatter Plot with Color and Size Variations')
        plt.xlabel('X values')
        plt.ylabel('Y values')
        plt.colorbar(scatter, label='Color Scale')
        plt.grid(True, alpha=0.3)
        
        plt.savefig('scatter_plot.png', dpi=150, bbox_inches='tight')
        print("✅ Scatter plot saved as 'scatter_plot.png'")
        plt.close()
        
    except ImportError:
        print("Scatter plot example (matplotlib required)")

def demonstrate_bar_charts():
    """Show bar charts"""
    print("=== Bar Charts ===")
    
    try:
        import matplotlib.pyplot as plt
        
        # Sample data
        categories = ['A', 'B', 'C', 'D', 'E']
        values = [23, 45, 56, 78, 32]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Vertical bar chart
        bars1 = ax1.bar(categories, values, color=colors)
        ax1.set_title('Vertical Bar Chart')
        ax1.set_xlabel('Categories')
        ax1.set_ylabel('Values')
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height}', ha='center', va='bottom')
        
        # Horizontal bar chart
        bars2 = ax2.barh(categories, values, color=colors)
        ax2.set_title('Horizontal Bar Chart')
        ax2.set_xlabel('Values')
        ax2.set_ylabel('Categories')
        
        plt.tight_layout()
        plt.savefig('bar_charts.png', dpi=150, bbox_inches='tight')
        print("✅ Bar charts saved as 'bar_charts.png'")
        plt.close()
        
    except ImportError:
        print("Bar chart example (matplotlib required)")

def demonstrate_subplots():
    """Show multiple subplots"""
    print("=== Subplots ===")
    
    try:
        import matplotlib.pyplot as plt
        
        # Create data for different plots
        x = np.linspace(0, 2*np.pi, 100)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('Multiple Subplots Example', fontsize=16)
        
        # Plot 1: Sine wave
        axes[0, 0].plot(x, np.sin(x), 'b-')
        axes[0, 0].set_title('Sine Wave')
        axes[0, 0].grid(True)
        
        # Plot 2: Cosine wave
        axes[0, 1].plot(x, np.cos(x), 'r-')
        axes[0, 1].set_title('Cosine Wave')
        axes[0, 1].grid(True)
        
        # Plot 3: Histogram
        np.random.seed(42)
        data = np.random.normal(0, 1, 1000)
        axes[1, 0].hist(data, bins=30, color='green', alpha=0.7)
        axes[1, 0].set_title('Histogram')
        axes[1, 0].set_xlabel('Value')
        axes[1, 0].set_ylabel('Frequency')
        
        # Plot 4: Scatter plot
        x_scatter = np.random.randn(50)
        y_scatter = np.random.randn(50)
        axes[1, 1].scatter(x_scatter, y_scatter, alpha=0.6)
        axes[1, 1].set_title('Scatter Plot')
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig('subplots.png', dpi=150, bbox_inches='tight')
        print("✅ Subplots saved as 'subplots.png'")
        plt.close()
        
    except ImportError:
        print("Subplots example (matplotlib required)")

def demonstrate_advanced_plotting():
    """Show advanced plot types"""
    print("=== Advanced Plot Types ===")
    
    try:
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 1. Box plot
        np.random.seed(42)
        data_box = [np.random.normal(0, std, 100) for std in range(1, 4)]
        axes[0, 0].boxplot(data_box, labels=['Group 1', 'Group 2', 'Group 3'])
        axes[0, 0].set_title('Box Plot')
        axes[0, 0].set_ylabel('Values')
        
        # 2. Pie chart
        sizes = [30, 25, 20, 15, 10]
        labels = ['A', 'B', 'C', 'D', 'E']
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        wedges, texts, autotexts = axes[0, 1].pie(sizes, labels=labels, colors=colors, 
                                                  autopct='%1.1f%%', startangle=90)
        axes[0, 1].set_title('Pie Chart')
        
        # 3. Heatmap (using imshow)
        data_heat = np.random.rand(10, 10)
        im = axes[1, 0].imshow(data_heat, cmap='YlOrRd', interpolation='nearest')
        axes[1, 0].set_title('Heatmap')
        plt.colorbar(im, ax=axes[1, 0], fraction=0.046, pad=0.04)
        
        # 4. Area plot (fill_between)
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)
        axes[1, 1].fill_between(x, y1, alpha=0.5, label='sin(x)')
        axes[1, 1].fill_between(x, y2, alpha=0.5, label='cos(x)')
        axes[1, 1].set_title('Area Plot')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('advanced_plots.png', dpi=150, bbox_inches='tight')
        print("✅ Advanced plots saved as 'advanced_plots.png'")
        plt.close()
        
    except ImportError:
        print("Advanced plots example (matplotlib required)")

def demonstrate_styling():
    """Show plot styling and customization"""
    print("=== Plot Styling ===")
    
    try:
        import matplotlib.pyplot as plt
        
        # Available styles
        print(f"Available styles: {plt.style.available[:5]}...")  # Show first 5
        
        # Use a specific style
        plt.style.use('seaborn-v0_8' if 'seaborn-v0_8' in plt.style.available else 'default')
        
        # Create styled plot
        x = np.linspace(0, 10, 50)
        y = np.sin(x)
        
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, linewidth=3, color='#2E86C1', marker='o', markersize=8, 
                markerfacecolor='#F39C12', markeredgecolor='#E74C3C', markeredgewidth=2)
        
        plt.title('Styled Plot Example', fontsize=20, fontweight='bold', color='#2C3E50')
        plt.xlabel('X Values', fontsize=14, fontweight='bold')
        plt.ylabel('Y Values', fontsize=14, fontweight='bold')
        
        # Customize grid
        plt.grid(True, linestyle='--', alpha=0.7, color='#BDC3C7')
        
        # Customize spines
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#34495E')
        ax.spines['bottom'].set_color('#34495E')
        
        plt.tight_layout()
        plt.savefig('styled_plot.png', dpi=150, bbox_inches='tight')
        print("✅ Styled plot saved as 'styled_plot.png'")
        plt.close()
        
        # Reset style
        plt.style.use('default')
        
    except ImportError:
        print("Styling example (matplotlib required)")

class PlotGenerator:
    """Utility class for generating common plots"""
    
    def __init__(self, style='default', figsize=(10, 6)):
        self.style = style
        self.figsize = figsize
        
        try:
            import matplotlib.pyplot as plt
            self.plt = plt
            if style in plt.style.available:
                plt.style.use(style)
        except ImportError:
            self.plt = None
    
    def line_plot(self, x_data, y_data, title="Line Plot", xlabel="X", ylabel="Y", 
                  save_as=None):
        """Generate a line plot"""
        if not self.plt:
            print("matplotlib not available")
            return
        
        self.plt.figure(figsize=self.figsize)
        self.plt.plot(x_data, y_data, linewidth=2)
        self.plt.title(title)
        self.plt.xlabel(xlabel)
        self.plt.ylabel(ylabel)
        self.plt.grid(True, alpha=0.3)
        
        if save_as:
            self.plt.savefig(save_as, dpi=150, bbox_inches='tight')
            print(f"✅ Plot saved as '{save_as}'")
        
        self.plt.close()
    
    def comparison_plot(self, data_dict, title="Comparison Plot", save_as=None):
        """Generate a comparison plot with multiple series"""
        if not self.plt or not data_dict:
            print("matplotlib not available or no data")
            return
        
        self.plt.figure(figsize=self.figsize)
        
        for label, (x, y) in data_dict.items():
            self.plt.plot(x, y, label=label, linewidth=2, marker='o', markersize=4)
        
        self.plt.title(title)
        self.plt.xlabel("X")
        self.plt.ylabel("Y")
        self.plt.legend()
        self.plt.grid(True, alpha=0.3)
        
        if save_as:
            self.plt.savefig(save_as, dpi=150, bbox_inches='tight')
            print(f"✅ Comparison plot saved as '{save_as}'")
        
        self.plt.close()

def demonstrate_plot_generator():
    """Show usage of PlotGenerator class"""
    print("=== PlotGenerator Class Demo ===")
    
    pg = PlotGenerator()
    
    # Simple line plot
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x)
    pg.line_plot(x, y, "Sine Wave", "Angle (radians)", "sin(x)", "generator_sine.png")
    
    # Comparison plot
    comparison_data = {
        "sin(x)": (x, np.sin(x)),
        "cos(x)": (x, np.cos(x)),
        "sin(2x)": (x, np.sin(2*x))
    }
    pg.comparison_plot(comparison_data, "Trigonometric Functions", "generator_comparison.png")

def clean_up_files():
    """Clean up generated plot files"""
    import os
    
    plot_files = [
        'basic_plot.png', 'scatter_plot.png', 'bar_charts.png', 'subplots.png',
        'advanced_plots.png', 'styled_plot.png', 'generator_sine.png', 'generator_comparison.png'
    ]
    
    cleaned = 0
    for file in plot_files:
        if os.path.exists(file):
            os.remove(file)
            cleaned += 1
    
    if cleaned > 0:
        print(f"🗑️ Cleaned up {cleaned} plot files")

if __name__ == '__main__':
    print("📊 MATPLOTLIB EXAMPLES 📊")
    print("=" * 50)
    
    try:
        demonstrate_basic_plotting()
        demonstrate_scatter_plots()
        demonstrate_bar_charts()
        demonstrate_subplots()
        demonstrate_advanced_plotting()
        demonstrate_styling()
        demonstrate_plot_generator()
        
        print("\n✅ Matplotlib examples completed!")
        print("📁 Generated plot files (PNG format)")
        
        # Optionally clean up files
        import os
        response = input("\nClean up generated plot files? (y/N): ").lower().strip()
        if response in ['y', 'yes']:
            clean_up_files()
        
    except Exception as e:
        print(f"❌ Error in matplotlib examples: {e}")
        clean_up_files()  # Clean up any partial files