import math

class SecurityFilter:
    blocked_keywords = [
        "ignore previous instructions",
        "jailbreak",
        "do anything now"
    ]

    def check(self, text: str) -> bool:
        lowered = text.lower()

        # 1. Jailbreak detection
        for bad in self.blocked_keywords:
            if bad in lowered:
                return False

        # 2. Entropy detection — усилили порог
        if self._entropy(text) > 3.3:   # ↓ threshold for test
            return False

        return True

    def _entropy(self, text: str) -> float:
        if not text:
            return 0.0

        freq = {c: text.count(c) for c in set(text)}
        length = len(text)

        return -sum((count/length) * math.log2(count/length) for count in freq.values())
