# comparison_methods/box_plot_comparison.py
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from .base_comparison import ComparisonMethod

class BoxPlotComparison(ComparisonMethod):
    """Generates box plots to compare metric distributions across parameter combinations.

    Attributes:
        method_name (str): The name of the comparison method.
        description (str): A brief description of the functionality of the class.
        
    Methods:
        __init__(): Initializes a new instance of BoxPlotComparison.
        compare(data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
            Compares metric distributions across parameter combinations and generates box plots.
            Saves each plot as a PNG file in the specified directory and returns a dictionary
            containing the generated figures."""
    def __init__(self):
        """__init__ method of BoxPlotComparison class.
This initializer sets the name and description for the plot generation functionality within the class. The plot generates box plots to compare metric distributions across different parameter combinations."""
        super().__init__("BoxPlotComparison", "Generates box plots to compare metric distributions across parameter combinations.")

    def compare(self, data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
        """Generate box plots for specified metrics in the provided DataFrame.

    Parameters:
        - data (pd.DataFrame): The input DataFrame containing data.
        - metrics_to_measure (list[str]): A list of metric names to generate box plots for.
        - output_dir (str): Directory where generated box plot images will be saved.

    Returns:
        dict: A dictionary containing the generated box plots as Matplotlib figures."""
        print(f"  Performing BoxPlotComparison on metrics: {metrics_to_measure}")

        if 'param_combination' not in data.columns:
            print("  Warning: 'param_combination' column not found. Box plots will not group by parameters.")
            data['param_combination'] = 'default_params'

        plots = {}

        # Iterate through each metric to create a box plot
        for metric in metrics_to_measure:
            if metric not in data.columns or not pd.api.types.is_numeric_dtype(data[metric]):
                print(f"  Skipping box plot for non-numeric or missing metric: {metric}")
                continue
            
            # Filter out rows where the metric value is NaN for plotting
            plot_data = data.dropna(subset=[metric])

            if plot_data.empty or plot_data['param_combination'].nunique() < 2:
                print(f"  Skipping box plot for {metric}: Not enough valid data or parameter combinations to compare distributions.")
                continue

            fig, ax = plt.subplots(figsize=(12, 7))
            
            # Use a list of data for each group for boxplot
            groups = plot_data['param_combination'].unique()
            data_to_plot = [plot_data[plot_data['param_combination'] == g][metric].values for g in groups]

            # Customizing box plot elements for dark mode and M3 feel
            box_props = dict(facecolor='#4F378B', edgecolor='#D0BCFF', linewidth=1.5) # primary_container, primary
            median_props = dict(color='#CCC2DC', linewidth=2) # secondary
            whisker_props = dict(color='#938F99', linewidth=1.5, linestyle='--') # outline
            cap_props = dict(color='#938F99', linewidth=1.5) # outline
            flier_props = dict(marker='o', markerfacecolor='#EFB8C8', markersize=6, linestyle='none', markeredgecolor='#EFB8C8') # tertiary

            ax.boxplot(data_to_plot, labels=groups, patch_artist=True,
                       boxprops=box_props, medianprops=median_props,
                       whiskerprops=whisker_props, capprops=cap_props,
                       flierprops=flier_props)
            
            ax.set_title(f'Distribution of {metric.replace("_", " ").title()} by Parameter Combination', color='#E6E1E5')
            ax.set_xlabel('Parameter Combination', color='#CAC4D0')
            ax.set_ylabel(metric.replace("_", " ").title(), color='#CAC4D0')
            
            ax.tick_params(axis='x', rotation=45, colors='#938F99')
            ax.tick_params(axis='y', colors='#938F99')
            
            ax.set_facecolor('#1C1B1F')
            fig.patch.set_facecolor('#1C1B1F')

            ax.grid(True, linestyle='--', alpha=0.6, color='#49454F')

            plt.tight_layout()

            plot_filename = os.path.join(output_dir, f"{metric}_boxplot.png")
            fig.savefig(plot_filename, facecolor=fig.get_facecolor())
            plt.close(fig)
            print(f"  Generated box plot for {metric}: {plot_filename}")
            plots[f"Box Plot: {metric.replace('_', ' ').title()}"] = fig

        return {"plots": plots}