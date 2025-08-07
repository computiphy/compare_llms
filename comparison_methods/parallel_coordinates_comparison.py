# comparison_methods/parallel_coordinates_comparison.py
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates # Specific plot type
import os
import numpy as np
from .base_comparison import ComparisonMethod

class ParallelCoordinatesComparison(ComparisonMethod):
    """A comparison method that generates parallel coordinates plots for multi-dimensional comparison of features and metrics.

    The class performs the following steps:
    - Identifies numeric columns (features and metrics) from the input data.
    - Excludes 'iteration' as it is not a feature or metric of interest.
    - Normalizes data to a 0-1 range for better visualization in parallel coordinates plots.
    - Generates parallel coordinates plots with parameter combinations as colors, using Matplotlib's `parallel_coordinates` function.
    - Saves the generated plot as an image file and returns the plot information.
    """

    def __init__(self):
        super().__init__("ParallelCoordinatesComparison", "Generates parallel coordinates plots for multi-dimensional comparison of features and metrics.")

    def compare(self, data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
        """
        Generates a parallel coordinates plot comparing features and metrics by parameter combination.

        Parameters:
        - data (pd.DataFrame): The input dataset containing feature and metric data.
        - metrics_to_measure (list[str]): A list of column names for metrics to be compared.
        - output_dir (str): The directory where the generated plot will be saved.

        Returns:
        - dict: A dictionary containing information about the generated plots, including the path to the saved image file."""
    def __init__(self):
        """Initializes a ParallelCoordinatesComparison object, which generates parallel coordinates plots
    to facilitate the visual comparison of multiple dimensions in feature and metric analysis."""
        super().__init__("ParallelCoordinatesComparison", "Generates parallel coordinates plots for multi-dimensional comparison of features and metrics.")

    def compare(self, data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
        """Generates a Parallel Coordinates Plot of features and metrics by parameter combination.

    Parameters:
        - data (pd.DataFrame): The dataset to analyze.
        - metrics_to_measure (list[str]): A list of columns that are metrics to include in the plot.
        - output_dir (str): Directory where plots will be saved.

    Returns:
        dict: A dictionary containing the generated plot(s)."""
        print(f"  Performing ParallelCoordinatesComparison.")

        plots = {}

        # Identify all numeric columns (features and metrics) for the plot
        # Exclude 'iteration' as it's not a feature or metric of interest for PC plot
        numeric_cols = [col for col in data.columns if pd.api.types.is_numeric_dtype(data[col]) and col != 'iteration']
        
        # Also include individual feature columns that were added from the config
        # These are columns that are not standard result columns or metrics
        standard_non_param_cols = ['prompt', 'iteration', 'model', 'generated_text', 'error', 'param_combination'] + metrics_to_measure
        llm_param_cols = [col for col in data.columns if col not in standard_non_param_cols and pd.api.types.is_numeric_dtype(data[col])]

        plot_cols = sorted(list(set(llm_param_cols + metrics_to_measure))) # Combine and sort

        if len(plot_cols) < 2:
            print("  Skipping parallel coordinates plot: Not enough numeric features/metrics to plot.")
            return {"plots": {}}

        # For parallel coordinates, it's often best to normalize data
        # Let's create a copy and normalize numeric columns
        plot_data = data[plot_cols + ['param_combination']].dropna() # Drop rows with NaNs in relevant columns

        if plot_data.empty:
            print(f"  Skipping parallel coordinates plot: No valid data after dropping NaNs.")
            return {"plots": {}}

        # Normalize data to a 0-1 range for better visualization in parallel coordinates
        for col in plot_cols:
            min_val = plot_data[col].min()
            max_val = plot_data[col].max()
            if max_val != min_val: # Avoid division by zero
                plot_data[col] = (plot_data[col] - min_val) / (max_val - min_val)
            else:
                plot_data[col] = 0.5 # Set to middle if all values are the same

        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Use param_combination for coloring
        # Matplotlib's parallel_coordinates needs the class_column
        
        # Generate a colormap for the parameter combinations
        unique_combinations = plot_data['param_combination'].unique()
        colors = plt.cm.viridis(np.linspace(0, 1, len(unique_combinations)))
        color_map = dict(zip(unique_combinations, colors))
        
        # Ensure the 'class_column' is the last column for parallel_coordinates
        temp_df = plot_data[plot_cols + ['param_combination']]
        
        parallel_coordinates(temp_df, 'param_combination', ax=ax, colormap='viridis', alpha=0.7)

        ax.set_title('Parallel Coordinates of Features and Metrics by Parameter Combination', color='#E6E1E5')
        # CORRECTED LINE: Removed 'ha='right'' as it's not a valid keyword for tick_params
        ax.tick_params(axis='x', rotation=45, colors='#CAC4D0') 
        ax.tick_params(axis='y', colors='#938F99')
        
        ax.set_facecolor('#1C1B1F')
        fig.patch.set_facecolor('#1C1B1F')

        ax.legend(title="Parameter Combo", bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False, labelcolor='#CAC4D0', title_fontsize='medium')
        plt.subplots_adjust(right=0.75) # Adjust layout to make space for legend

        plt.tight_layout()

        plot_filename = os.path.join(output_dir, "parallel_coordinates.png")
        fig.savefig(plot_filename, facecolor=fig.get_facecolor())
        plt.close(fig)
        print(f"  Generated parallel coordinates plot: {plot_filename}")
        plots["Parallel Coordinates Plot"] = fig

        return {"plots": plots}