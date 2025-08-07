# comparison_methods/network_graph_comparison.py
import matplotlib.pyplot as plt
import os
from .base_comparison import ComparisonMethod

class NetworkGraphComparison(ComparisonMethod):
    """This class provides a placeholder for performing network graph comparisons. 
    It is not applicable to LLM performance comparison data and serves as a note that this method is typically used for relational data (e.g., social networks, dependencies), not direct LLM performance metrics.
    The compare function generates a static plot illustrating the concept of network graphs but does not perform any actual graph analysis on the input data. This placeholder allows users to visualize the potential use case when working with network-based data.
    
    Parameters:
    - data (pd.DataFrame): The dataset containing the relational or dependency information.
    - metrics_to_measure: A list of strings specifying the metrics to be measured.
    - output_dir (str): The directory where the plot will be saved.
    
    Returns:
    - dict: A dictionary containing a single key-value pair, with 'Network Graph (Placeholder)' as the key and the matplotlib figure object as the value."""
    def __init__(self):
        """Initializes a new instance of the `NetworkGraphComparison` class.
    
    This method serves as a placeholder and is not intended to be used for LLM performance comparison data.
    
    Args:
        name (str): The name of the object being initialized. In this case, it is "NetworkGraphComparison".
        description (str): A brief description of what the method does. It states that this method is generally not applicable
                         for LLM performance comparison data and should be used as a placeholder."""
        super().__init__("NetworkGraphComparison", "This method is generally not applicable for LLM performance comparison data. Placeholder only.")

    def compare(self, data: pd.DataFrame, metrics_to_measure: list[str], output_dir: str) -> dict:
        """Performs a network graph comparison for the given dataset.

    Note: This method is typically used for relational data (e.g., social networks,
          dependencies), not direct LLM performance metrics. The function generates
          a placeholder network graph image since it's not applicable to the provided data.
          If you have specific relational or interaction data, this functionality can be
          extended to generate meaningful network graphs.

    Parameters:
        - data: A pandas DataFrame containing the dataset for comparison.
        - metrics_to_measure: A list of strings specifying the metrics to evaluate.
        - output_dir: The directory where plot files will be saved.

    Returns:
        A dictionary containing a single plot named "Network Graph (Placeholder)" with
        a description that explains its inapplicability to the provided dataset."""
        print(f"  Performing NetworkGraphComparison. Note: This method is typically used for relational data (e.g., social networks, dependencies), not direct LLM performance metrics.")
        
        plots = {}
        # This is a placeholder as network graphs are not directly applicable.
        # If you had, for example, a graph of how different prompts relate to each other
        # or how models interact in a multi-agent system, then it would be relevant.

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, "Network Graph Not Applicable for this Data", 
                horizontalalignment='center', verticalalignment='center', 
                transform=ax.transAxes, fontsize=12, color='#F2B8B5') # error color
        
        ax.set_title("Network Graph (Not Applicable)", color='#E6E1E5')
        ax.set_facecolor('#1C1B1F')
        fig.patch.set_facecolor('#1C1B1F')
        ax.axis('off') # Hide axes

        plot_filename = os.path.join(output_dir, "network_graph_placeholder.png")
        fig.savefig(plot_filename, facecolor=fig.get_facecolor())
        plt.close(fig)
        plots["Network Graph (Placeholder)"] = fig

        return {"plots": plots}