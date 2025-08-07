# comparison_methods/line_chart_comparison.py
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from .base_comparison import ComparisonMethod

class LineChartComparison(ComparisonMethod):
    """A class to generate line charts that illustrate metric trends across parameter combinations.

    Parameters:
    - name (str): The name of the comparison method.
    - description (str): A brief description of the functionality of the method.

    Methods:
    - __init__(): Initializes the LineChartComparison class with a name and description.
    - compare(data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
        Compares data to generate line charts for specified metrics. It aggregates data by parameter combinations,
        sorts it, and creates line charts for each metric. The method handles missing or non-numeric data and warnings
        for the presence of 'param_combination' column. Each chart is saved in the specified output directory."""
    def __init__(self):
        """
    Initializes a LineChartComparison object with a description and title.

    Parameters:
    - self: The instance of the class.
    """

    def __init__(self):
        super().__init__("LineChartComparison", "Generates line charts showing metric trends across parameter combinations.")

    def compare(self, data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
        """Compares and generates line charts for the specified metrics across different parameter combinations.

    Parameters:
    - data (pd.DataFrame): The input DataFrame containing necessary columns such as 'param_combination'.
    - metrics_to_measure (list[str]): A list of metric names to be compared.
    - output_dir (str): The directory where generated line chart images will be saved.

    Returns:
    - dict: A dictionary containing the plot objects with keys like "Line Chart: Metric Name"."""
        print(f"  Performing LineChartComparison on metrics: {metrics_to_measure}")

        if 'param_combination' not in data.columns:
            print("  Warning: 'param_combination' column not found. Line charts will not show parameter variations.")
            data['param_combination'] = 'default_params'

        plots = {}

        # Aggregate data by parameter combination, taking the mean of each metric
        # Sort by param_combination to ensure consistent plotting order, or by a specific feature if only one is varied
        aggregated_data = data.groupby('param_combination')[metrics_to_measure].mean().reset_index()
        
        # Attempt to sort by a numeric feature if only one is present and numeric
        numeric_features = [col for col in data.columns if col not in ['prompt', 'iteration', 'model', 'generated_text', 'error', 'param_combination'] and pd.api.types.is_numeric_dtype(data[col]) and data[col].nunique() > 1]
        
        if len(numeric_features) == 1:
            sort_by_feature = numeric_features[0]
            # Merge the feature value back for sorting, then drop duplicates
            temp_data = data[['param_combination', sort_by_feature]].drop_duplicates()
            aggregated_data = pd.merge(aggregated_data, temp_data, on='param_combination', how='left')
            aggregated_data = aggregated_data.sort_values(by=sort_by_feature)
            # Remove the temporary feature column if it's not a metric
            if sort_by_feature not in metrics_to_measure:
                aggregated_data = aggregated_data.drop(columns=[sort_by_feature])
        else:
            # Fallback to sorting by param_combination string if no single numeric feature is clear
            aggregated_data = aggregated_data.sort_values(by='param_combination')


        # Iterate through each metric to create a line chart
        for metric in metrics_to_measure:
            if metric not in aggregated_data.columns or not pd.api.types.is_numeric_dtype(aggregated_data[metric]):
                print(f"  Skipping line chart for non-numeric or missing metric: {metric}")
                continue
            
            plot_data = aggregated_data.dropna(subset=[metric])

            if plot_data.empty:
                print(f"  Skipping line chart for {metric}: No valid data after dropping NaNs.")
                continue

            fig, ax = plt.subplots(figsize=(12, 7))
            
            ax.plot(plot_data['param_combination'], plot_data[metric], marker='o', linestyle='-', color='#D0BCFF') # M3 Primary color
            
            ax.set_title(f'Average {metric.replace("_", " ").title()} Across Parameter Combinations', color='#E6E1E5') # on_surface
            ax.set_xlabel('Parameter Combination', color='#CAC4D0') # on_surface_variant
            ax.set_ylabel(metric.replace("_", " ").title(), color='#CAC4D0') # on_surface_variant
            
            ax.tick_params(axis='x', rotation=45, colors='#938F99') # outline
            ax.tick_params(axis='y', colors='#938F99') # outline
            
            ax.set_facecolor('#1C1B1F') # surface
            fig.patch.set_facecolor('#1C1B1F') # background for the whole figure

            ax.grid(True, linestyle='--', alpha=0.6, color='#49454F') # surface_variant for grid

            plt.tight_layout()

            plot_filename = os.path.join(output_dir, f"{metric}_line_chart.png")
            fig.savefig(plot_filename, facecolor=fig.get_facecolor()) # Save with correct background
            plt.close(fig)
            print(f"  Generated line chart for {metric}: {plot_filename}")
            plots[f"Line Chart: {metric.replace('_', ' ').title()}"] = fig

        return {"plots": plots}