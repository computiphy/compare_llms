# comparison_methods/treemap_comparison.py
import pandas as pd
import matplotlib.pyplot as plt
import squarify # A good library for treemaps
import os
import numpy as np
from .base_comparison import ComparisonMethod

class TreemapComparison(ComparisonMethod):
    """Generates a treemap comparison plot for hierarchical data. 
    This class is designed to visualize the proportion of total duration by parameter combination, 
    using a mock hierarchical structure due to the limitations of its data structure.

    Attributes:
        name (str): The name of the comparison method.
        description (str): A brief description of the comparison method.
    """

    def __init__(self):
        super().__init__("TreemapComparison", "Generates a treemap (mock example due to data structure).")

    def compare(self, data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
        """
        Compares and visualizes the hierarchical data using a treemap.

        Parameters:
            data (pd.DataFrame): The input DataFrame containing the data for comparison.
            metrics_to_measure (list[str]): A list of metrics to measure in the comparison.
            output_dir (str): The directory where the generated plots will be saved.

        Returns:
            dict: A dictionary containing the generated plots."""
    def __init__(self):
        """Initializes the TreemapComparison class with specific names and descriptions.
    
    Parameters:
    - name: A string that represents the title or purpose of the class. Default is "TreemapComparison".
    - description: A string providing a brief description of what the class does. Default is "Generates a treemap (mock example due to data structure)."""
        super().__init__("TreemapComparison", "Generates a treemap (mock example due to data structure).")

    def compare(self, data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
        """Perform a TreemapComparison on the given DataFrame.

    This function generates a visual representation of hierarchical data using a treemap. It is particularly useful for demonstrating how to visualize proportions or values in a hierarchical structure when the data lacks clear hierarchy. The function aggregates the specified metrics and creates a treemap based on the average duration of each parameter combination, which is then saved as a PNG image in the specified output directory.

    Args:
        data (pd.DataFrame): The input DataFrame containing the necessary columns for visualization.
        metrics_to_measure (list[str]): A list of column names to include in the comparison. In this case, it should include 'total_duration_s' and 'param_combination'.
        output_dir (str): The directory where the generated treemap image will be saved.

    Returns:
        dict: A dictionary containing a single key-value pair, where the key is "plots" and the value is a dictionary with the treemap figure as its value."""
        print(f"  Performing TreemapComparison. Note: Treemaps are best for hierarchical data, which is mocked here.")

        plots = {}

        # Mock hierarchical data for demonstration
        # Let's say we want to visualize the proportion of 'total_duration_s' for each param_combination
        # This isn't strictly hierarchical but can be represented as a flat treemap
        if 'total_duration_s' in data.columns and 'param_combination' in data.columns:
            # Aggregate total_duration_s by param_combination
            agg_duration = data.groupby('param_combination')['total_duration_s'].mean().reset_index()
            agg_duration = agg_duration.dropna(subset=['total_duration_s'])

            if not agg_duration.empty:
                # Sort for better visual grouping in treemap
                agg_duration = agg_duration.sort_values(by='total_duration_s', ascending=False)
                
                sizes = agg_duration['total_duration_s'].tolist()
                labels = [f"{row['param_combination']}\n({row['total_duration_s']:.2f}s)" for index, row in agg_duration.iterrows()]
                
                # M3 inspired color palette for treemap
                colors = ['#4F378B', '#633B48', '#4A4458', '#D0BCFF', '#CCC2DC', '#EFB8C8'] * (len(sizes) // 6 + 1)
                colors = colors[:len(sizes)] # Ensure colors match size of data

                fig, ax = plt.subplots(figsize=(12, 8))
                
                # Create the treemap
                squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.8,
                              text_kwargs={'color': '#E6E1E5', 'fontsize': 9, 'wrap': True},
                              ax=ax)
                
                ax.set_title('Treemap of Average Total Duration by Parameter Combination', color='#E6E1E5')
                ax.axis('off') # Hide axes for a cleaner treemap
                fig.patch.set_facecolor('#1C1B1F')

                plt.tight_layout()
                plot_filename = os.path.join(output_dir, "total_duration_treemap.png")
                fig.savefig(plot_filename, facecolor=fig.get_facecolor())
                plt.close(fig)
                print(f"  Generated treemap for total duration: {plot_filename}")
                plots["Treemap: Average Total Duration"] = fig
            else:
                print("  No valid data for treemap generation.")
        else:
            print("  'total_duration_s' or 'param_combination' not found for treemap example.")

        return {"plots": plots}