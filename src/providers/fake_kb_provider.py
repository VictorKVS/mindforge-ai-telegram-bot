# src/providers/fake_kb_provider.py

from typing import List, Dict, Optional


class FakeKBProvider:
    """
    Fake Knowledge Base Provider (L2)
    --------------------------------
    - sandbox-only
    - read-only
    - no access logic
    - no reasoning
    - contract-driven
    """

    def __init__(self):
        # Static, versioned, audit-friendly dataset
        self._documents: List[Dict[str, str]] = [
            {
                "document_id": "return_policy_v3",
                "title": "Политика возврата",
                "content": "Товар можно вернуть в течение 14 дней при наличии чека.",
                "source": "kb_public",
                "version": "3.0",
                "scope": "public",
            },
            {
                "document_id": "delivery_terms_v1",
                "title": "Условия доставки",
                "content": "Доставка осуществляется в течение 3–5 рабочих дней.",
                "source": "kb_public",
                "version": "1.0",
                "scope": "public",
            },
            {
                "document_id": "internal_discount_rules_v2",
                "title": "Внутренние правила скидок",
                "content": "Скидки применяются по согласованию с менеджером.",
                "source": "kb_restricted",
                "version": "2.0",
                "scope": "restricted",
            },
        ]

    # -------------------------
    # Public API (called by UAG)
    # -------------------------

    def query(
        self,
        scope: str,
        query: str
    ) -> List[Dict[str, str]]:
        """
        knowledge_query
        Simple substring matching.
        No ranking, no reasoning.
        """
        query_lower = query.lower()

        results = []
        for doc in self._documents:
            if doc["scope"] != scope:
                continue

            if (
                query_lower in doc["title"].lower()
                or query_lower in doc["content"].lower()
            ):
                results.append(self._format_doc(doc))

        return results

    def retrieve(
        self,
        scope: str,
        document_id: str
    ) -> Optional[Dict[str, str]]:
        """
        document_retrieve
        """
        for doc in self._documents:
            if doc["scope"] != scope:
                continue

            if doc["document_id"] == document_id:
                return self._format_doc(doc)

        return None

    # -------------------------
    # Internal helpers
    # -------------------------

    def _format_doc(self, doc: Dict[str, str]) -> Dict[str, str]:
        """
        Ensure strict response schema
        """
        return {
            "document_id": doc["document_id"],
            "title": doc["title"],
            "content": doc["content"],
            "source": doc["source"],
            "version": doc["version"],
        }
