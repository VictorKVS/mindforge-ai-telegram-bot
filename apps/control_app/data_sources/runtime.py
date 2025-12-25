"""
apps/control_app/data_sources/runtime.py

Read-only adapter for runtime state.
"""

from src.core.runtime_state import STATE


async def load_runtime_state():
    return await STATE.snapshot()
