# Compare\_LLMs

## Overview

**Compare\_LLMs** is a modular and extensible Python-based framework for comparing the performance and behavior of different Large Language Models (LLMs). It collects both runtime performance metrics (e.g., latency, throughput, token generation) and system-level metrics (e.g., CPU, GPU, RAM usage) to help users understand model efficiency under various scenarios. It supports various visual comparison methods such as scatter plots, bar charts, box plots, and correlation heatmaps, and is fully configurable via a JSON configuration file.

---

## Features

* Prompt-driven evaluation of models via local backends (like Ollama).
* System performance monitoring (CPU, RAM, GPU).
* Token generation timing.
* Extensible visual analytics for performance data.
* Configurable via a `feature_config.json` file.

---

## Folder Structure

```
compare_lms/
├── comparison_methods/         # Various visualization classes for comparing metrics
│   ├── abstract_comparison.py     # Abstract base class for all comparison methods
│   ├── base_comparison.py         # Core interface used by visual comparison modules
│   ├── bar_chart_comparison.py    # Bar chart visualization
│   ├── box_plot_comparison.py     # Box plot visualization
│   ├── correlation_heatmap_comparison.py # Correlation heatmap
│   ├── histogram_comparison.py    # Histogram visualization
│   ├── line_chart_comparison.py   # Line chart visualization
│   ├── network_graph_comparison.py# Graph-based model comparisons
│   ├── parallel_coordinates_comparison.py # High-dimensional feature visualization
│   ├── pie_chart_comparison.py    # Pie chart for categorical distributions
│   ├── scatter_plot_comparison.py # Scatter plots for feature correlation
│   ├── table_comparison.py        # Tabular comparison display
│   ├── treemap_comparison.py      # Tree map for hierarchical data
│   └── __init__.py
│
├── config.py                    # Global and runtime configuration manager
│
├── data_collection/            # Code related to prompt processing and metric logging
│   ├── metrics.py                 # Function to calculate key metrics like latency, etc.
│   ├── ollama_client.py           # Connects to and queries models via Ollama
│   └── __init__.py
│
├── feature_config.json         # Defines model parameters, prompts, features, and active comparison methods
│
├── features/                   # Feature extractors for generation/system level attributes
│   ├── abstract_feature.py        # Abstract base class for features
│   ├── generation_params.py       # Extracts generation-specific metrics (e.g., tokens/sec)
│   ├── system_params.py           # Interfaces with system_monitor to extract hardware metrics
│   └── __init__.py
│
├── main.py                     # Main entry point to run model comparisons and save outputs
│
├── prompts.txt                 # Contains prompts to be passed to the models
│
├── results/                    # (Git-ignored) Stores generated CSVs and HTML outputs
│
├── system_monitor/            # System performance monitoring modules
│   ├── base_metric_collector.py   # Base class for all system collectors
│   ├── cpu_collector.py           # Uses `psutil` to collect CPU usage and temperature
│   ├── gpu_collector.py           # Uses `pynvml` to collect GPU load/memory
│   ├── ram_collector.py           # Uses `psutil` for RAM utilization
│
├── templates/                 # HTML templates for generating visual reports
│   └── report_template.html
```

---

## How it Works

1. **Prompt Collection**:

   * Reads prompts from `prompts.txt`.

2. **Model Execution**:

   * Each prompt is passed to one or more LLMs via `ollama_client.py`.
   * Timing begins before and ends after token generation for accurate performance stats.

3. **System Monitoring**:

   * Collectors in `system_monitor/` track CPU, GPU, and RAM stats during execution.
   * These metrics are passed to `metrics.py` for aggregation.

4. **Feature Extraction**:

   * Generation features (e.g., response length, latency, tokens/sec) and system features are extracted via modules in `features/`.

5. **Metrics Aggregation**:

   * All metrics are processed by `calculate_metrics()` and stored.

6. **Comparison Visualization**:

   * Configured comparison methods (e.g., bar, box, scatter plots) are executed based on `feature_config.json`.
   * Visuals are saved to the `results/` folder.

---

## Usage

### Prerequisites

* Python 3.8+

Make sure you have the following packages:

* `psutil`
* `pynvml`
* `matplotlib`, `seaborn`, `plotly`, `pandas`, etc.
* A running local Ollama backend or replace `ollama_client.py` with your own model client.

### Run the Framework

```bash
python main.py --model llama3.2:latest --feature_config_file feature_config.json --prompts_file prompts.txt --iterations 1
```

---

---

## Notes

* GPU monitoring requires `pynvml` and an NVIDIA GPU.
* CPU temperature requires OS support and may not be available in virtualized environments.
* The `results/` folder is ignored in `.gitignore` to prevent cluttering your repo.
