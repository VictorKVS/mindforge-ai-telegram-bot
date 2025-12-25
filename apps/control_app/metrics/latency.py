# apps/control_app/metrics/latency.py

def latency_stats(runtime_metrics):
    return {
        "avg_ms": runtime_metrics.get("avg_latency_ms"),
        "p95_ms": runtime_metrics.get("p95_latency_ms"),
    }
