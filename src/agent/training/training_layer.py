import json
import os
from typing import Dict, Any

# Используем относительный путь от текущего файла
RULES_FILE = os.path.join(os.path.dirname(__file__), "rules.json")

class TrainingLayer:
    """
    Internal learning layer for an agent.
    Responsible for:
    - analyzing events
    - applying training rules
    - updating skills/services/inventory
    - preparing agent for next-level progression
    """

    def __init__(self):
        from agent.profile.profile_loader import load_profile
        self.profile = load_profile()
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict[str, Any]:
        """Load training rules from JSON."""
        try:
            with open(RULES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("[TRAINING] rules.json not found. Using empty ruleset.")
            return {"training_events": []}

    def apply_event(self, event: Dict[str, Any]):
        """
        Main entrypoint.
        Called when agent receives an event:
        - successful order
        - interaction with another agent
        - new skill usage
        - user feedback
        - violation caught by security
        """
        event_type = event.get("type")
        print(f"[TRAINING] Event received: {event_type}")

        for rule in self.rules.get("training_events", []):
            if rule["trigger"] == event_type:
                self._apply_rule(rule, event)

    def _apply_rule(self, rule: Dict[str, Any], event: Dict[str, Any]):
        """Apply a specific training rule."""
        print(f"[TRAINING] Applying rule: {rule.get('name')}")

        # Add new skill
        if "add_skill" in rule:
            skill = rule["add_skill"]
            if "skills" not in self.profile:
                self.profile["skills"] = []
            if skill not in self.profile["skills"]:
                self.profile["skills"].append(skill)
                print(f"[TRAINING] Skill added: {skill}")

        # Add new service
        if "add_service" in rule:
            name = rule["add_service"]["name"]
            price = rule["add_service"]["price"]
            if "services" not in self.profile:
                self.profile["services"] = {}
            self.profile["services"][name] = price
            print(f"[TRAINING] New service added: {name} → {price}")

        # Improve service price
        if "adjust_price" in rule:
            service = rule["adjust_price"]["service"]
            delta = rule["adjust_price"]["delta"]
            if "services" in self.profile and service in self.profile["services"]:
                self.profile["services"][service] += delta
                print(f"[TRAINING] Service price adjusted: {service} → {self.profile['services'][service]}")

        # Inventory update based on event
        if "update_inventory" in rule:
            inv_name = rule["update_inventory"]["item"]
            inv_delta = rule["update_inventory"]["delta"]
            if "inventory" not in self.profile:
                self.profile["inventory"] = {}
            self.profile["inventory"][inv_name] = (
                self.profile["inventory"].get(inv_name, 0) + inv_delta
            )
            print(f"[TRAINING] Updated inventory: {inv_name} → {self.profile['inventory'][inv_name]}")

        # Save updated profile to disk
        self._save_profile()

    def _save_p