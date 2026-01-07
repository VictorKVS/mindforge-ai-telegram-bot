# src/core/training/module.py
class TrainingModule:
    def __init__(
        self,
        module_id: str,
        version: str,
        title: str,
        scope: list[str],
        limitations: list[str],
        vendor: str = "MindForge",
    ):
        self.module_id = module_id
        self.version = version
        self.title = title
        self.scope = scope
        self.limitations = limitations
        self.vendor = vendor
