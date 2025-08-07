# comparison_methods/correlation_heatmap_comparison.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns # Seaborn is great for heatmaps
import os
import numpy as np
from .base_comparison import ComparisonMethod

class CorrelationHeatmapComparison(ComparisonMethod):
    """Class for generating a heatmap showing correlations between all numeric features and metrics.

    This method calculates the correlation matrix of numeric columns in the input DataFrame and generates a heatmap
    using a diverging colormap to visualize the relationships between different features. The heatmap includes annotations
    for each cell, formatted with two decimal places, and has customized tick labels and color bar settings to ensure it
    looks good on dark backgrounds.
    """

    def __init__(self):
        super().__init__("CorrelationHeatmapComparison", "Generates a heatmap showing correlations between all numeric features and metrics.")

    def compare(self, data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
        """
        Compares the input DataFrame by generating a correlation heatmap.

        Parameters:
            data (pd.DataFrame): The DataFrame containing the dataset.
            metrics_to_measure (list[str]): A list of metric names to measure against numeric features.
            output_dir (str): The directory where the generated plots will be saved.

        Returns:
            dict: A dictionary containing the name and plot object of the generated heatmap."""
    def __init__(self):
        """Initializes the CorrelationHeatmapComparison class, which generates a heatmap comparing the correlations between all numeric features and metrics.
    
    Args:
        name (str): The name of the chart to be generated. Defaults to "CorrelationHeatmapComparison".
        description (str): A brief description of what the chart represents. Defaults to "Generates a heatmap showing correlations between all numeric features and metrics."""
        super().__init__("CorrelationHeatmapComparison", "Generates a heatmap showing correlations between all numeric features and metrics.")

    def compare(self, data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
        """Perform a correlation heatmap comparison on the given DataFrame.

    This function calculates and visualizes the correlation matrix of numeric columns in the DataFrame.
    It generates a heatmap that annotates each cell with the correlation coefficient and uses a diverging colormap
    to represent positive and negative correlations. The plot is saved to the specified output directory.

    Parameters:
    - data (pd.DataFrame): The input dataset containing numerical features and metrics.
    - metrics_to_measure (list[str]): A list of column names for which the correlation heatmap should be generated.
    - output_dir (str): The directory where the heatmap image will be saved.

    Returns:
    - dict: A dictionary containing a single plot entry with the title 'Correlation Heatmap'."""
        print(f"  Performing CorrelationHeatmapComparison.")

        plots = {}

        # Identify all numeric columns that could be features or metrics
        numeric_cols = [col for col in data.columns if pd.api.types.is_numeric_dtype(data[col])]
        
        if len(numeric_cols) < 2:
            print("  Skipping correlation heatmap: Not enough numeric columns to calculate correlations.")
            return {"plots": {}}

        # Calculate the correlation matrix
        correlation_matrix = data[numeric_cols].corr()

        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Use a diverging colormap for correlations (e.g., 'coolwarm', 'vlag', 'RdBu')
        # Customize for dark mode: use a colormap that looks good on dark backgrounds
        cmap = sns.diverging_palette(240, 10, as_cmap=True, s=80, l=70) # Blue to Red, M3 inspired
        
        sns.heatmap(correlation_matrix, annot=True, cmap=cmap, fmt=".2f", linewidths=.5, linecolor='#49454F', ax=ax,
                    cbar_kws={'label': 'Correlation Coefficient', 'shrink': .75})

        ax.set_title('Correlation Heatmap of Features and Metrics', color='#E6E1E5')
        # CORRECTED LINE: Removed 'ha='right'' as it's not a valid keyword for tick_params
        ax.tick_params(axis='x', rotation=45, colors='#CAC4D0') 
        ax.tick_params(axis='y', rotation=0, colors='#CAC4D0')
        
        ax.set_facecolor('#1C1B1F')
        fig.patch.set_facecolor('#1C1B1F')

        # Customize color bar for dark mode
        cbar = ax.collections[0].colorbar
        cbar.ax.yaxis.set_tick_params(colors='#CAC4D0')
        cbar.set_label('Correlation Coefficient', color='#CAC4D0')

        plt.tight_layout()

        plot_filename = os.path.join(output_dir, "correlation_heatmap.png")
        fig.savefig(plot_filename, facecolor=fig.get_facecolor())
        plt.close(fig)
        print(f"  Generated correlation heatmap: {plot_filename}")
        plots["Correlation Heatmap"] = fig

        return {"plots": plots}