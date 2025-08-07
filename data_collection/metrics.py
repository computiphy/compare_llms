def calculate_metrics(
    full_response_content: str,
    raw_duration: float,
    first_token_duration: float,
    tokens_generated: int,
    system_metrics: dict = None
) -> dict:
    """
    Calculates performance and quality metrics from raw experiment data,
    including optional system performance metrics.
    """
    metrics = {
        "TotalDuration": raw_duration,
        "FirstTokenLatency": first_token_duration,
        "TokensGenerated": tokens_generated,
    }

    # Calculate Tokens Per Second (after first token)
    generation_duration = raw_duration - first_token_duration
    if tokens_generated > 0 and generation_duration > 0:
        metrics["TokensPerSecond"] = tokens_generated / generation_duration
    else:
        metrics["TokensPerSecond"] = 0.0

    # Example: Unique words / total words ratio
    words = full_response_content.lower().split()
    metrics["UniqueWordsRatio"] = len(set(words)) / len(words) if words else 0.0

    # Integrate system metrics if provided
    if system_metrics:
        metrics.update(system_metrics)

    return metrics
