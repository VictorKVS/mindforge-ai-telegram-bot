# src/polygon/teacher/knowledge_registry.py

from pathlib import Path
import yaml
from typing import Dict, Optional


KNOWLEDGE_DIR = Path("src/polygon/knowledge")


class KnowledgeRegistry:
    """
    In-memory registry of knowledge blocks.
    Knowledge blocks are loaded from YAML files.
    """

    _registry: Dict[str, dict] = {}

    @classmethod
    def load_all(cls) -> None:
        """
        Load all knowledge blocks from KNOWLEDGE_DIR.
        """
        cls._registry.clear()

        if not KNOWLEDGE_DIR.exists():
            return

        for file in KNOWLEDGE_DIR.glob("*.yaml"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)

                kb_id = data.get("knowledge_block_id")
                if kb_id:
                    cls._registry[kb_id] = data
            except Exception:
                continue

    @classmethod
    def get(cls, knowledge_block_id: str) -> Optional[dict]:
        """
        Get a knowledge block by ID.
        """
        return cls._registry.get(knowledge_block_id)

    @classmethod
    def list_ids(cls) -> list[str]:
        """
        List all loaded knowledge block IDs.
        """
        return list(cls._registry.keys())
