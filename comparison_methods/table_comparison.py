import pandas as pd
from .base_comparison import ComparisonMethod
import os
import numpy as np

class TableComparison(ComparisonMethod):
    """Class for comparing LLM performance across different parameters and metrics by generating a summarized table.

    Attributes:
        name (str): The name of the comparison method.
        description (str): A description of what the comparison method does.

    Methods:
        compare(data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
            Compares LLM performance based on specified parameters and metrics, generating a table with aggregated results.

            Args:
                data (pd.DataFrame): The dataset containing performance metrics.
                metrics_to_measure (list[str]): A list of metric names to compare.
                output_dir (str): The directory where the generated table will be saved.

            Returns:
                dict: A dictionary containing the aggregated data and a message indicating the save path."""
    def __init__(self):
        """Initializes a new instance of the TableComparison class.
    
    This object is designed to generate a table that summarizes the performance of Large Language Models (LLMs) 
    across various parameters and metrics. It serves as a reference for comparative analysis and performance evaluation."""
        super().__init__("TableComparison", "Generates a table summarizing LLM performance across different parameters and metrics.")

    def compare(self, data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
        """self,
    data: pd.DataFrame,
    metrics_to_measure: list[str],
    output_dir: str
) -> dict:
    Performs a table comparison on the given DataFrame.

    This function aggregates the provided DataFrame based on specified metrics and parameters. It processes the data to handle missing values, format numeric metrics for better readability, and save the aggregated results to a CSV file in the specified output directory. The function also includes warning messages if certain columns are missing from the DataFrame.

    Parameters:
    - data (pd.DataFrame): The DataFrame containing the dataset to be compared.
    - metrics_to_measure (list[str]): A list of metric names to include in the comparison.
    - output_dir (str): The directory where the aggregated table will be saved.

    Returns:
    dict: A dictionary containing the aggregated DataFrame with formatted numeric metrics.
    """
        print(f"  Performing TableComparison on metrics: {metrics_to_measure}")

        if 'param_combination' not in data.columns:
            print("  Warning: 'param_combination' column not found in data. Table will not group by parameters.")
            data['param_combination'] = 'default_params'
        
        # Get individual feature columns that were added by main.py
        # These are the keys from the feature_params JSON.
        # Filter for actual columns present in the DataFrame
        # A simple way to get them is to find columns that are *not* our standard generated columns
        # and are not the metrics themselves.
        identifying_cols = ['param_combination']
        # Dynamically find columns that seem to be individual LLM parameters
        # by checking columns that were added from `current_params` in main.py
        # and are not the standard result columns (like prompt, iteration, model, etc.)
        standard_non_param_cols = ['prompt', 'iteration', 'model', 'generated_text', 'error'] + metrics_to_measure
        llm_param_cols = [col for col in data.columns if col not in standard_non_param_cols and col not in identifying_cols]
        
        group_cols = identifying_cols + llm_param_cols
        group_cols = sorted(list(set(group_cols))) # Ensure unique and sorted for consistent grouping

        numeric_metrics = [
            m for m in metrics_to_measure
            if m in data.columns and pd.api.types.is_numeric_dtype(data[m])
        ]

        if not numeric_metrics:
            print("  No numeric metrics found for TableComparison.")
            return {"aggregated_data": "No numeric metrics to aggregate."}

        # Aggregate data by the defined grouping columns
        # We need to handle cases where there might be NaNs due to errors. mean() handles NaNs by default.
        aggregated_data = data.groupby(group_cols)[numeric_metrics].mean().reset_index()

        # Rename 'param_combination' for display if it's the only grouping column,
        # or just keep it as is if other feature columns are there.
        # It's generally better to display the individual feature columns rather than just the combined label.
        if 'param_combination' in aggregated_data.columns:
             aggregated_data.rename(columns={'param_combination': 'Param Combination Label'}, inplace=True)

        # Format numeric columns for better display
        for col in numeric_metrics:
            if col in aggregated_data.columns:
                if col.endswith('_s'):
                    aggregated_data[col] = aggregated_data[col].apply(lambda x: f"{x:.3f} s" if not pd.isna(x) else "N/A")
                elif 'tokens' in col or col == 'response_length':
                    aggregated_data[col] = aggregated_data[col].apply(lambda x: int(round(x)) if not pd.isna(x) else "N/A")
                elif col == 'tokens_per_second':
                    aggregated_data[col] = aggregated_data[col].apply(lambda x: f"{x:.2f}" if not pd.isna(x) else "N/A")
                elif col == 'quality_score':
                    aggregated_data[col] = aggregated_data[col].apply(lambda x: f"{x:.2f}" if not pd.isna(x) else "N/A")

        output_csv_path = os.path.join(output_dir, "aggregated_metrics_table.csv")
        aggregated_data.to_csv(output_csv_path, index=False)
        print(f"  Aggregated table saved to {output_csv_path}")

        return {
            "aggregated_data": aggregated_data
        }