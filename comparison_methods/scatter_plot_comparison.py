# comparison_methods/scatter_plot_comparison.py
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from itertools import product # To get all combinations
from .base_comparison import ComparisonMethod

class ScatterPlotComparison(ComparisonMethod):
    """Generates scatter plots for all combinations of features against metrics.

    The class performs the following actions:
    - Identifies numeric feature columns that are not part of standard non-parameter columns or metrics.
    - Heuristically determines feature columns based on numeric data types and excludes standard or metric columns.
    - Creates a list of all possible pairs of features and metrics to plot, including additional useful metric vs. metric plots if applicable.
    - Generates scatter plots for each pair using the `matplotlib` library.
    - Optionally colors points by parameter combinations if available.
    - Saves each plot as a PNG file in the specified output directory and returns a dictionary containing all generated plots."""
    def __init__(self):
        """Initializes a ScatterPlotComparison object with the name "ScatterPlotComparison".
    
    This constructor creates a new instance of ScatterPlotComparison, which is designed to generate 
    scatter plots for each combination of features versus various metrics. The default name for this 
    visualization tool is "ScatterPlotComparison"."""
        super().__init__("ScatterPlotComparison", "Generates scatter plots for all combinations of features vs. metrics.")

    def compare(self, data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
        """Perform scatter plot comparisons between LLM generation parameters and metrics.

    This function generates scatter plots for each feature-metric combination specified in `metrics_to_measure`.
    It includes additional heuristic checks to determine which columns are considered as LLM parameters
    (numeric columns that are not standard metrics or fixed identifiers).

    If there are no suitable features or metrics, the function skips generating scatter plots and returns an empty dictionary.

    Parameters:
        data (pd.DataFrame): The input DataFrame containing the dataset.
        metrics_to_measure (list[str]): A list of metric names to include in the scatter plots.
        output_dir (str): The directory where generated scatter plot images will be saved.

    Returns:
        dict: A dictionary containing the generated scatter plots, indexed by plot titles.

    Notes:
        - If 'param_combination' is a column and has multiple unique values, it uses a colormap to differentiate
          between different parameter sets.
        - The function also checks for missing data and invalid numeric types before generating plots.
        - Scatter plots are saved with appropriate file names in the specified output directory."""
        print(f"  Performing ScatterPlotComparison for all feature-metric combinations.")

        plots = {}

        # Identify actual feature columns (LLM generation parameters)
        # These are numeric columns that are NOT part of the standard metrics or fixed identifiers
        standard_non_param_cols = ['prompt', 'iteration', 'model', 'generated_text', 'error', 'param_combination'] + metrics_to_measure
        
        # Heuristically determine feature columns: numeric columns not in standard or metrics list
        feature_cols = [col for col in data.columns if pd.api.types.is_numeric_dtype(data[col]) and col not in standard_non_param_cols]

        if not feature_cols:
            print("  Warning: No numeric features (LLM parameters) found to plot against metrics. Skipping feature vs. metric scatter plots.")
        
        if not metrics_to_measure:
            print("  Warning: No metrics specified for scatter plots. Skipping feature vs. metric scatter plots.")
        
        # Generate all combinations of (feature, metric)
        # We also want to include metric vs metric plots if desired
        plot_pairs = []
        for feature in feature_cols:
            for metric in metrics_to_measure:
                plot_pairs.append((feature, metric))
        
        # Add a few useful metric vs metric plots as well (can be customized)
        # Ensure these are only added if both metrics exist
        if 'total_duration_s' in metrics_to_measure and 'tokens_per_second' in metrics_to_measure:
            plot_pairs.append(('total_duration_s', 'tokens_per_second'))
        if 'response_length' in metrics_to_measure and 'quality_score' in metrics_to_measure:
            plot_pairs.append(('response_length', 'quality_score'))

        if not plot_pairs:
            print("  No suitable feature-metric or metric-metric pairs found for scatter plots.")
            return {"plots": {}}

        for x_var, y_var in plot_pairs:
            # Check if both variables exist in the DataFrame and are numeric
            if x_var not in data.columns or y_var not in data.columns or \
               not pd.api.types.is_numeric_dtype(data[x_var]) or not pd.api.types.is_numeric_dtype(data[y_var]):
                print(f"  Skipping scatter plot for {x_var} vs {y_var}: One or both variables are missing or not numeric.")
                continue
            
            plot_data = data.dropna(subset=[x_var, y_var])

            if plot_data.empty:
                print(f"  Skipping scatter plot for {x_var} vs {y_var}: No valid data after dropping NaNs.")
                continue

            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Use param_combination for coloring if available and meaningful
            # This allows seeing how different parameter sets cluster
            if 'param_combination' in plot_data.columns and plot_data['param_combination'].nunique() > 1:
                unique_combinations = plot_data['param_combination'].unique()
                colors = plt.cm.viridis(np.linspace(0, 1, len(unique_combinations))) # Use a colormap
                color_map = dict(zip(unique_combinations, colors))
                plot_data['color'] = plot_data['param_combination'].map(color_map)
                ax.scatter(plot_data[x_var], plot_data[y_var], c=plot_data['color'], alpha=0.7, s=50, edgecolor='none')
                
                # Add a legend for parameter combinations
                legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=combo,
                                              markerfacecolor=color_map[combo], markersize=10)
                                   for combo in unique_combinations]
                # Place legend outside to avoid overlap with plot
                ax.legend(handles=legend_elements, title="Parameter Combo", bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False, labelcolor='#CAC4D0', title_fontsize='medium')
                plt.subplots_adjust(right=0.75) # Adjust layout to make space for legend
            else:
                # Default color if no parameter combinations to differentiate
                ax.scatter(plot_data[x_var], plot_data[y_var], color='#D0BCFF', alpha=0.7, s=50, edgecolor='none') # M3 Primary color

            ax.set_title(f'{x_var.replace("_", " ").title()} vs {y_var.replace("_", " ").title()}', color='#E6E1E5') # on_surface
            ax.set_xlabel(x_var.replace("_", " ").title(), color='#CAC4D0') # on_surface_variant
            ax.set_ylabel(y_var.replace("_", " ").title(), color='#CAC4D0') # on_surface_variant
            
            ax.tick_params(axis='x', colors='#938F99') # outline
            ax.tick_params(axis='y', colors='#938F99') # outline
            
            ax.set_facecolor('#1C1B1F') # surface
            fig.patch.set_facecolor('#1C1B1F') # background for the whole figure

            ax.grid(True, linestyle='--', alpha=0.6, color='#49454F') # surface_variant for grid

            plt.tight_layout()

            plot_filename = os.path.join(output_dir, f"{x_var}_vs_{y_var}_scatterplot.png")
            fig.savefig(plot_filename, facecolor=fig.get_facecolor())
            plt.close(fig)
            print(f"  Generated scatter plot for {x_var} vs {y_var}: {plot_filename}")
            plots[f"Scatter Plot: {x_var.replace('_', ' ').title()} vs {y_var.replace('_', ' ').title()}"] = fig

        return {"plots": plots}