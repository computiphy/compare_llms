# comparison_methods/pie_chart_comparison.py
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from .base_comparison import ComparisonMethod

class PieChartComparison(ComparisonMethod):
    """Generates a pie chart to visualize categorical distributions of data.

    This class is designed to compare and analyze categorical data, particularly in scenarios where traditional bar charts
    may not be suitable due to the limited applicability of pie charts. It uses `matplotlib` for plotting and assumes that
    categorical data can be represented as integer categories or strings.

    Attributes:
        name (str): The name of the comparison method.
        description (str): A brief description of the comparison method's purpose and limitations.

    Methods:
        compare(data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
            Compares the provided data against predefined metrics and generates a pie chart for categorical distributions.
            Returns a dictionary containing generated plots with their filenames as keys."""
    def __init__(self):
        """Initializes an instance of the PieChartComparison class.

    The constructor sets up the chart with the following properties:
    - title: "PieChartComparison"
    - description: "Generates a pie chart (limited applicability for this data)."
    
    This class is designed to create pie charts, but it may not be suitable for all datasets."""
        super().__init__("PieChartComparison", "Generates a pie chart (limited applicability for this data).")

    def compare(self, data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
        """Generates a PieChartComparison based on the 'quality_score' metric in the provided DataFrame.
    
    This function prints a message about the limited applicability of pie charts for this type of data and proceeds to create a pie chart
    if the 'quality_score' column exists and is numeric. The resulting plot is saved to the specified output directory with a unique filename.
    
    Parameters:
    - data (pd.DataFrame): The DataFrame containing the dataset to analyze.
    - metrics_to_measure (list[str]): A list of metric names to measure, although this function currently focuses on 'quality_score'.
    - output_dir (str): The directory where the generated plot will be saved.

    Returns:
    - dict: A dictionary containing a single key-value pair with the plot type as the key and the Matplotlib figure object as the value."""
        print(f"  Performing PieChartComparison. Note: Pie charts have limited applicability for this type of data.")

        plots = {}
        
        # Example: Mocking a categorical quality distribution
        # In a real scenario, you'd categorize a metric or use actual categorical data.
        if 'quality_score' in data.columns and pd.api.types.is_numeric_dtype(data['quality_score']):
            # Bin quality scores into categories for demonstration
            bins = [0, 20, 50, 100] # Example bins for quality score
            labels = ['Low Quality', 'Medium Quality', 'High Quality']
            data['quality_category'] = pd.cut(data['quality_score'], bins=bins, labels=labels, right=False)
            
            category_counts = data['quality_category'].value_counts().sort_index()

            if not category_counts.empty:
                fig, ax = plt.subplots(figsize=(8, 8))
                
                # M3 inspired colors for categories (using secondary, tertiary, primary containers)
                colors = ['#4A4458', '#633B48', '#4F378B'] 
                
                ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=colors,
                       textprops={'color': '#E6E1E5'}) # on_background for text
                ax.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
                
                ax.set_title('Distribution of Response Quality Categories', color='#E6E1E5')
                fig.patch.set_facecolor('#1C1B1F')

                plt.tight_layout()
                plot_filename = os.path.join(output_dir, "quality_category_pie_chart.png")
                fig.savefig(plot_filename, facecolor=fig.get_facecolor())
                plt.close(fig)
                print(f"  Generated pie chart for quality categories: {plot_filename}")
                plots["Pie Chart: Response Quality Categories"] = fig
            else:
                print("  No valid quality score data to categorize for pie chart.")
        else:
            print("  'quality_score' metric not found or not numeric for pie chart example.")

        return {"plots": plots}