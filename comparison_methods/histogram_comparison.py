# comparison_methods/histogram_comparison.py
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from .base_comparison import ComparisonMethod

class HistogramComparison(ComparisonMethod):
    """Generates histograms for each metric to show their distribution.

    Attributes:
        name (str): The name of the comparison method.
        description (str): A brief description of what this comparison does.

    Methods:
        compare(data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
            Generates histograms for the specified metrics and saves them to the output directory.
            Returns a dictionary containing the generated plots."""
    def __init__(self):
        """
    Initializes a HistogramComparison object with the name 'HistogramComparison' and a description that explains its purpose of generating histograms for each metric to visualize their distribution.
        """
        super().__init__("HistogramComparison", "Generates histograms for each metric to show their distribution.")

    def compare(self, data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
        """Generates histograms for the specified numeric metrics in the input DataFrame and saves them to the output directory.

    Parameters:
    - data (pd.DataFrame): The input DataFrame containing the data to analyze.
    - metrics_to_measure (list[str]): A list of metric names to create histograms for. These should be present as columns in the DataFrame.
    - output_dir (str): The directory where the histogram plots will be saved.

    Returns:
    - dict: A dictionary containing a key 'plots' with a value being a dictionary mapping plot titles to matplotlib figure objects."""
        print(f"  Performing HistogramComparison on metrics: {metrics_to_measure}")

        plots = {}

        # Iterate through each metric to create a histogram
        for metric in metrics_to_measure:
            if metric not in data.columns or not pd.api.types.is_numeric_dtype(data[metric]):
                print(f"  Skipping histogram for non-numeric or missing metric: {metric}")
                continue
            
            # Filter out NaN values for plotting
            plot_data = data[metric].dropna()

            if plot_data.empty:
                print(f"  Skipping histogram for {metric}: No valid data after dropping NaNs.")
                continue

            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Adjust bin count based on data range or use a default
            num_bins = min(50, int(len(plot_data)**0.5)) # Simple heuristic for bin count
            ax.hist(plot_data, bins=num_bins, color='#6750A4', edgecolor='#D0BCFF', alpha=0.8) # Primary & on_primary_container
            
            ax.set_title(f'Distribution of {metric.replace("_", " ").title()}', color='#E6E1E5') # on_surface
            ax.set_xlabel(metric.replace("_", " ").title(), color='#CAC4D0') # on_surface_variant
            ax.set_ylabel('Frequency', color='#CAC4D0') # on_surface_variant
            
            ax.tick_params(axis='x', colors='#938F99') # outline
            ax.tick_params(axis='y', colors='#938F99') # outline
            
            ax.set_facecolor('#1C1B1F') # surface
            fig.patch.set_facecolor('#1C1B1F') # background for the whole figure

            ax.grid(True, linestyle='--', alpha=0.6, color='#49454F') # surface_variant for grid

            plt.tight_layout()

            plot_filename = os.path.join(output_dir, f"{metric}_histogram.png")
            fig.savefig(plot_filename, facecolor=fig.get_facecolor())
            plt.close(fig)
            print(f"  Generated histogram for {metric}: {plot_filename}")
            plots[f"Histogram: {metric.replace('_', ' ').title()}"] = fig

        return {"plots": plots}