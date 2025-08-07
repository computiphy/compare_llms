import argparse
import pandas as pd
import importlib
import os
import time
import ollama
import re
import jinja2
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np  # <-- Added numpy for np.nan
from itertools import product # <-- Added for parameter combinations
import json # <-- Added for parsing JSON feature values

# --- Project-specific Imports (assuming they exist in their respective modules) ---
# from features.abstract_feature import LLMFeature # Keep if you plan to use it for custom feature extraction
from comparison_methods.base_comparison import ComparisonMethod
# from data_collection.ollama_client import OllamaClient # The client is directly imported via 'ollama' now
# from data_collection.metrics import calculate_metrics # Metrics are calculated inline for now
from system_monitor.cpu_collector import CPUCollector
from system_monitor.ram_collector import RAMCollector
from system_monitor.gpu_collector import GPUCollector
from data_collection.metrics import calculate_metrics

# Function to sanitize string for use in file paths
def sanitize_filename(name: str) -> str:
    """Replaces characters that are invalid in Windows file paths with underscores."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name

def camel_to_snake(name: str) -> str:
    """Converts a PascalCase string to snake_case."""
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def load_class(module_path: str, class_name: str):
    """Dynamically loads a class from a given module path and class name."""
    try:
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Could not load class '{class_name}' from module '{module_path}': {e}")

def main():
    parser = argparse.ArgumentParser(
        description="compare_lms: A hyper-modular tool for comparing Ollama LLM features and metrics."
    )

    parser.add_argument("--model", type=str, required=True,
                        help="The Ollama model to compare (e.g., 'llama3.2:latest', 'phi3').")

    # --- UPDATED ARGUMENTS ---
    # We no longer need --features separately if we read them from the JSON file keys, 
    # but we can keep it if the user wants to filter which ones to run. 
    # For simplicity, we'll read all features from the JSON file.
    
    parser.add_argument("--feature_config_file", type=str, required=True, # <-- New required argument for the JSON file path
                        help="Path to a JSON file containing LLM generation parameters and their values (e.g., 'feature_config.json').")
    parser.add_argument("--metrics", type=str, default="cpu_percent_eval_avg, cpu_percent_eval_max, total_ram_gb_eval_avg, total_ram_gb_eval_max, used_ram_gb_eval_avg, used_ram_gb_eval_max, response_quality,latency,tokens_per_second",
                        help="Comma-separated list of metrics to measure (e.g., 'response_quality,latency').")
    parser.add_argument("--prompts_file", type=str, default="prompts.txt",
                        help="Path to a file containing prompts, one per line.")
    parser.add_argument("--iterations", type=int, default=1,
                        help="Number of times to run each prompt for each unique feature combination.")
    parser.add_argument("--output_dir", type=str, default="results",
                        help="Directory to save comparison results.")
    parser.add_argument("--comparison_methods", type=str, default="TableComparison,BarChartComparison,LineChartComparison,HistogramComparison," \
                        "BoxPlotComparison,ScatterPlotComparison,CorrelationHeatmapComparison,ParallelCoordinatesComparison",
                        help="Comma-separated list of comparison method classes to use.")

    args = parser.parse_args()

    # --- Load Feature Configuration from JSON File ---
    feature_params = {}
    try:
        with open(args.feature_config_file, 'r') as f:
            feature_params = json.load(f)
        
        # Verify that feature_params is a dictionary and contains lists for values
        if not isinstance(feature_params, dict) or not all(isinstance(v, list) for v in feature_params.values()):
            raise ValueError("JSON file must contain a dictionary where keys are feature names and values are lists of settings.")

        print(f"Loaded LLM parameter configuration from: {args.feature_config_file}")
        print(f"Features to vary: {list(feature_params.keys())}")

    except FileNotFoundError:
        print(f"Error: Feature configuration file '{args.feature_config_file}' not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from '{args.feature_config_file}': {e}")
        return
    except ValueError as e:
        print(f"Configuration file error: {e}")
        return

    # Generate all combinations of feature parameters
    feature_keys = list(feature_params.keys())
    # Note: If feature_params is empty (e.g., empty JSON), product(*[]) would raise an error.
    # We should only proceed if feature_keys is not empty, otherwise we're not running a parameter sweep.
    if not feature_keys:
        print("Warning: No features found in the configuration file. Running a single default configuration.")
        feature_value_combinations = [()]
    else:
        feature_value_combinations = list(product(*feature_params.values()))


    # --- Setup Output Directory ---
    sanitized_model_name = sanitize_filename(args.model)
    output_path = os.path.join(args.output_dir, f"{sanitized_model_name}_comparison_{time.strftime('%Y%m%d_%H%M%S')}")
    os.makedirs(output_path, exist_ok=True)
    print(f"Results will be saved to: {output_path}")

    # --- Initialize Ollama Client ---
    client = ollama.Client()

    # --- Load Prompts ---
    prompts = []
    try:
        with open(args.prompts_file, 'r', encoding='utf-8') as f:
            prompts = [line.strip() for line in f if line.strip()]
        if not prompts:
            print("No prompts found in prompts.txt. Exiting.")
            return
    except FileNotFoundError:
        print(f"Error: Prompts file '{args.prompts_file}' not found.")
        return

    # --- Metric Mapping (Remains the same) ---
    metric_column_map = {
        # ... (Your existing metric mapping) ...
        'response_quality': 'quality_score',
        'latency': 'total_duration_s',
        'token_count': 'completion_tokens', 
        'tokens_per_second': 'tokens_per_second',
        'response_length': 'response_length',
        'prompt_tokens': 'prompt_tokens',
        'completion_tokens': 'completion_tokens', 
        'total_duration_s': 'total_duration_s',
        'load_duration_s': 'load_duration_s',
        'eval_duration_s': 'eval_duration_s',
        'quality_score': 'quality_score',
        'cpu_percent_eval_avg': 'cpu_percent_eval_avg',
        'cpu_percent_eval_max': 'cpu_percent_eval_max',
        'total_ram_gb_eval_avg': 'total_ram_gb_eval_avg',
        'total_ram_gb_eval_max': 'total_ram_gb_eval_max',
        'used_ram_gb_eval_avg': 'used_ram_gb_eval_avg',
        'used_ram_gb_eval_max': 'used_ram_gb_eval_max',
    }

    requested_metrics = [m.strip() for m in args.metrics.split(',')]
    metrics_to_measure = [metric_column_map.get(m, m) for m in requested_metrics]
    print(f"Metrics to measure (mapped to DataFrame columns): {metrics_to_measure}")

    # --- Load Comparison Methods (Remains the same) ---
    comparison_method_instances = []
    for method_name in [m.strip() for m in args.comparison_methods.split(',')]:
        try:
            module_name_snake_case = camel_to_snake(method_name)
            method_class = load_class(f"comparison_methods.{module_name_snake_case}", method_name)
            instance = method_class() 

            if not isinstance(instance, ComparisonMethod):
                raise TypeError(f"Loaded class {method_name} is not an instance of ComparisonMethod.")
            comparison_method_instances.append(instance)
            print(f"Loaded comparison method: {method_name}")
        except Exception as e:
            print(f"Skipping comparison method '{method_name}': {e}")


    if not comparison_method_instances:
        print("No valid comparison methods loaded. Exiting.")
        return

    # --- Data Collection (Remains similar, adjusted for feature_keys handling) ---
    all_results = []

    for param_combo_values in feature_value_combinations:
        current_params = {}
        
        # Populate current_params dictionary from the combination and feature keys
        if feature_keys: 
            for i, key in enumerate(feature_keys):
                current_params[key] = param_combo_values[i]
        
        # Create a unique label for this parameter combination for the DataFrame
        param_label = "_".join([f"{k}_{v}" for k,v in current_params.items()]) if current_params else "default_params"
        print(f"\n--- Running with parameters: {current_params if current_params else 'Default'} ---")

        for prompt_idx, prompt in enumerate(prompts):
            print(f"\nProcessing Prompt {prompt_idx + 1}/{len(prompts)}: '{prompt}'")
            for i in range(args.iterations):
                print(f"  Iteration {i + 1}/{args.iterations}")

                try:
                    # Prepare the generation options for Ollama.
                    ollama_options = {}
                    if current_params:
                        for param_name, param_value in current_params.items():
                            # Map your custom feature names to Ollama's `options` keys
                            # Ensure correct types (int/float)
                            if param_name in ["temperature", "top_p", "repeat_penalty"]:
                                ollama_options[param_name] = float(param_value)
                            elif param_name in ["top_k", "num_ctx", "num_predict"]:
                                ollama_options[param_name] = int(param_value)
                            # Add more mappings as needed (e.g., stop sequences, etc.)
                            # Note: Ollama expects many parameters inside the 'options' dictionary.

                    

                    # Initialize collectors
                    cpu_collector = CPUCollector()
                    ram_collector = RAMCollector()
                    gpu_collector = GPUCollector() 

                    # Start collectors
                    cpu_collector.start()
                    ram_collector.start()
                    gpu_collector.start()

                    response = client.generate(model=args.model, prompt=prompt, stream=False, options=ollama_options)
                    generated_text = response['response']
                    total_duration = response['total_duration'] / 1e9 # Convert ns to seconds
                    load_duration = response['load_duration'] / 1e9
                    prompt_eval_count = response['prompt_eval_count']
                    eval_count = response['eval_count']
                    eval_duration = response['eval_duration'] / 1e9

                    # Stop and summarize system metrics
                    cpu_data = cpu_collector.stop()
                    ram_data = ram_collector.stop()
                    # gpu_data = gpu_collector.stop()

                    cpu_summary = cpu_collector.get_summary()
                    ram_summary = ram_collector.get_summary()
                    # gpu_summary = gpu_collector.get_summary()

                    # Combine all system metrics
                    system_metrics = {}
                    system_metrics.update(cpu_summary)
                    system_metrics.update(ram_summary)
                    # system_metrics.update(gpu_summary)

                    # Now calculate and merge final metrics
                    metrics = calculate_metrics(
                        full_response_content=generated_text,
                        raw_duration=total_duration,
                        first_token_duration=load_duration,
                        tokens_generated=eval_count,
                        system_metrics=system_metrics
                    )

                    result = {
                        'prompt': prompt,
                        'iteration': i + 1,
                        'model': args.model,
                        'generated_text': generated_text,
                        'total_duration_s': total_duration,
                        'load_duration_s': load_duration,
                        'prompt_tokens': prompt_eval_count,
                        'completion_tokens': eval_count,
                        'eval_duration_s': eval_duration,
                        'tokens_per_second': eval_count / eval_duration if eval_duration > 0 else 0,
                        'response_length': len(generated_text),
                        'quality_score': (len(generated_text) / 100.0) * (total_duration / 5.0) if total_duration > 0 else 0.0, # Mock score
                        'param_combination': param_label # Add the label for this combination
                    }

                    # Add current LLM parameters to the result dict for traceability
                    result.update(current_params)

                    result.update(metrics)

                    all_results.append(result)

                    

                except ollama.ResponseError as e:
                    print(f"Ollama Error for model '{args.model}' with params {current_params}: {e}")
                    # ... (error handling remains the same) ...
                    error_entry = {
                        'prompt': prompt, 'iteration': i + 1, 'model': args.model, 'error': str(e),
                        'generated_text': '', 'total_duration_s': np.nan, 'load_duration_s': np.nan,
                        'prompt_tokens': np.nan, 'completion_tokens': np.nan, 'eval_duration_s': np.nan,
                        'tokens_per_second': np.nan, 'response_length': np.nan, 'quality_score': np.nan,
                        'param_combination': param_label
                    }
                    error_entry.update(current_params) 
                    all_results.append(error_entry)
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    # ... (error handling remains the same) ...
                    error_entry = {
                        'prompt': prompt, 'iteration': i + 1, 'model': args.model, 'error': str(e),
                        'generated_text': '', 'total_duration_s': np.nan, 'load_duration_s': np.nan,
                        'prompt_tokens': np.nan, 'completion_tokens': np.nan, 'eval_duration_s': np.nan,
                        'tokens_per_second': np.nan, 'response_length': np.nan, 'quality_score': np.nan,
                        'param_combination': param_label
                    }
                    error_entry.update(current_params) 
                    all_results.append(error_entry)


    if not all_results:
        print("No results collected for comparison. Exiting.")
        return

    results_df = pd.DataFrame(all_results)
    # Ensure numeric columns that were None are now NaN and correctly typed
    for col in metrics_to_measure: # Only convert actual metrics to numeric
        if col in results_df.columns:
            results_df[col] = pd.to_numeric(results_df[col], errors='coerce')

    print("\nDataFrame Info:")
    results_df.info()
    print("\nDataFrame Head:")
    print(results_df.head())
    results_csv_path = os.path.join(output_path, 'raw_results.csv')
    results_df.to_csv(results_csv_path, index=False)
    print(f"Raw results saved to {results_csv_path}")

    # --- Generate Report Data ---
    report_data = {
        'model_name': args.model,
        'generation_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'features_varied': feature_params, # Store the actual features (LLM parameters) varied
        'metrics_measured': metrics_to_measure, # Store the mapped metrics
        'prompts_used': prompts,
        'raw_data_html': results_df.to_html(classes='dataframe', index=False),
        'comparison_results': {}
    }

    # --- Run Comparison Methods and Collect Report Data (Remains the same) ---
    for method_instance in comparison_method_instances:
        # ... (Comparison method execution and HTML report generation remains the same as before) ...
        method_name = method_instance.__class__.__name__
        print(f"\nRunning comparison method: {method_name}")
        method_output_dir = os.path.join(output_path, camel_to_snake(method_name))
        os.makedirs(method_output_dir, exist_ok=True)

        try:
            # Pass the mapped metrics (metrics_to_measure) to the compare method
            method_result = method_instance.compare(results_df.copy(), metrics_to_measure, method_output_dir)
            
            # ... (Rest of the comparison result processing) ...
            report_method_data = {}
            if 'aggregated_data' in method_result and method_result['aggregated_data'] is not None:
                if isinstance(method_result['aggregated_data'], pd.DataFrame):
                    report_method_data['aggregated_data_html'] = method_result['aggregated_data'].to_html(classes='dataframe', index=False)
                else:
                    report_method_data['aggregated_data_html'] = f"<pre>{method_result['aggregated_data']}</pre>"
            else:
                report_method_data['aggregated_data_html'] = "No aggregated data available for this method."

            report_method_data['plots'] = []
            if 'plots' in method_result and method_result['plots']:
                for plot_title, fig in method_result['plots'].items():
                    if fig is not None:
                        buf = BytesIO()
                        fig.savefig(buf, format='png', bbox_inches='tight')
                        plt.close(fig)
                        image_base64 = base64.b64encode(buf.getvalue()).decode('ascii')
                        report_method_data['plots'].append({
                            'title': plot_title,
                            'image_base64': image_base64
                        })
            if 'sample_outputs' in method_result:
                report_method_data['sample_outputs'] = method_result['sample_outputs']

            report_data['comparison_results'][method_name] = report_method_data

        except Exception as e:
            print(f"Error running comparison method {method_name}: {e}")
            report_data['comparison_results'][method_name] = {
                'error': f"Error running comparison: {e}"
            }

    # --- Generate HTML Report ---
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
    template = env.get_template('report_template.html')

    html_report = template.render(report_data)

    report_html_path = os.path.join(output_path, 'comparison_report.html')
    with open(report_html_path, 'w', encoding='utf-8') as f:
        f.write(html_report)
    print(f"\nHTML report generated at: {report_html_path}")

if __name__ == "__main__":
    main()