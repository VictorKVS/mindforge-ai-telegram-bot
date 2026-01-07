"""
File: src/core/training/module.py

Purpose:
Canonical Training Module abstraction.

TrainingModule defines:
- what tasks an agent CAN do
- what tasks REQUIRE upgrade
"""

from typing import Set


class TrainingModule:
    """
    Base training module.

    Used by AgentBase to decide:
    - ALLOW
    - DENY (upgrade required)
    """

    def __init__(
        self,
        *,
        module_id: str,
        description: str,
        allowed_tasks: Set[str],
        upgrade_tasks: Set[str] | None = None,
    ):
        self.module_id = module_id
        self.description = description
        self.allowed_tasks = allowed_tasks
        self.upgrade_tasks = upgrade_tasks or set()

    def can_handle(self, task: str) -> bool:
        """
        Return True if task is fully supported.
        """
        return task in self.allowed_tasks

    def requires_upgrade(self, task: str) -> bool:
        """
        Return True if task exists but requires upgrade.
        """
        return task in self.upgrade_tasks
