"""
File: src/core/training/training_module.py

Purpose:
Training / knowledge extension module.

Used by TrainerAgent to:
- Explain unknown materials
- Simulate learning process
"""

class TrainingModule:
    def __init__(self) -> None:
        self._materials_knowledge = {
            "brick": {
                "description": "Кирпич строительный ГОСТ 530-2012",
                "sizes": "250×120×65 мм",
                "usage": "Фундаменты лёгких сооружений",
            }
        }

    def has_material(self, material: str) -> bool:
        return material in self._materials_knowledge

    def explain_material(self, material: str) -> str:
        data = self._materials_knowledge.get(material)

        if not data:
            return (
                f"Материал '{material}' неизвестен.\n"
                "Рекомендуется дообучение агента."
            )

        return (
            f"📘 Материал: {material}\n"
            f"Описание: {data['description']}\n"
            f"Размеры: {data['sizes']}\n"
            f"Применение: {data['usage']}"
        )
