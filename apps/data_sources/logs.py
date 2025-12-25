# apps/control_app/data_sources/logs.py

def load_runtime_metrics():
    """
    Load runtime metrics (latency, throughput, errors).

    Placeholder for:
    - log parsing
    - Prometheus
    - OpenTelemetry
    """
    return {
        "avg_latency_ms": 120,
        "p95_latency_ms": 240,
        "errors": 0,
    }
