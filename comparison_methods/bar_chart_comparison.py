import pandas as pd
import matplotlib.pyplot as plt
import os
from .base_comparison import ComparisonMethod
import numpy as np

class BarChartComparison(ComparisonMethod):
    """Generates bar charts comparing metrics across different LLM generation parameters.

    Attributes:
        name (str): The unique identifier for this comparison method.
        description (str): A brief description of the comparison method's functionality and purpose.

    Methods:
        __init__():
            Initializes a new instance of BarChartComparison with its unique name and description.

        compare(data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
            Compares the specified metrics across different parameter combinations in the provided data.
            Outputs bar charts to the specified directory."""
    def __init__(self):
        """
    Initializes a new BarChartComparison instance with the title "Bar Chart Comparison" and description 
    "Generates bar charts comparing metrics across different LLM generation parameters."
This concise docstring provides a clear and informative description of what the `__init__` method does, including its purpose and functionality."""
        super().__init__("BarChartComparison", "Generates bar charts comparing metrics across different LLM generation parameters.")

    def compare(self, data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
        """self,
    data: pd.DataFrame,   # The input DataFrame containing comparison data.
    metrics_to_measure: list[str],  # A list of metrics to measure and plot.
    output_dir: str            # Directory where the generated bar charts will be saved.
) -> dict:
    Generates bar charts for each specified metric in the provided DataFrame.

    Parameters:
        - data: pd.DataFrame, the input dataset with columns such as 'param_combination' and metrics to measure.
        - metrics_to_measure: list[str], a list of strings representing the metrics to plot.
        - output_dir: str, directory path where generated bar charts will be saved.

    Returns:
        - dict: A dictionary containing generated plots for each metric.
    """
        print(f"  Performing BarChartComparison on metrics: {metrics_to_measure}")

        if 'param_combination' not in data.columns:
            print("  Warning: 'param_combination' column not found. Bar charts will not show parameter variations.")
            data['param_combination'] = 'default_params'

        plots = {}

        aggregated_data = data.groupby('param_combination')[metrics_to_measure].mean().reset_index()

        for metric in metrics_to_measure:
            if metric not in aggregated_data.columns or not pd.api.types.is_numeric_dtype(aggregated_data[metric]):
                print(f"  Skipping bar chart for non-numeric or missing metric: {metric}")
                continue
            
            plot_data = aggregated_data.dropna(subset=[metric])

            if plot_data.empty:
                print(f"  Skipping bar chart for {metric}: No valid data after dropping NaNs.")
                continue

            fig, ax = plt.subplots(figsize=(10, 6))
            
            plot_data = plot_data.sort_values(by=metric, ascending=False)

            bars = ax.bar(plot_data['param_combination'], plot_data[metric], color='skyblue')
            ax.set_title(f'Average {metric.replace("_", " ").title()} by Parameter Combination')
            ax.set_xlabel('Parameter Combination')
            ax.set_ylabel(metric.replace("_", " ").title())
            
            # --- FIX: Remove ha/va from tick_params and ensure it's on text if needed ---
            # The error explicitly states tick_params keywords.
            # ax.tick_params(axis='x', rotation=45, ha='right') <--- 'ha' is NOT for tick_params!
            # The correct parameter for horizontal alignment of tick labels is `labelrotation` and `labelsize` etc.
            # For the text labels ON the bars, ha/va are correct for ax.text.
            ax.tick_params(axis='x', rotation=45, labelsize=10) # Removed 'ha', added 'labelsize' for clarity
            plt.tight_layout()

            # Add value labels on top of bars
            for bar in bars:
                yval = bar.get_height()
                # Ensure the text function is correctly called
                ax.text(bar.get_x() + bar.get_width()/2, yval, 
                        f'{yval:.2f}', # Format the number directly
                        ha='center', va='bottom', fontsize=9) # Explicitly use ha/va for text

            plot_filename = os.path.join(output_dir, f"{metric}_bar_chart.png")
            fig.savefig(plot_filename)
            plt.close(fig)
            print(f"  Generated bar chart for {metric}: {plot_filename}")
            plots[f"Bar Chart: {metric.replace('_', ' ').title()}"] = fig

        return {"plots": plots}