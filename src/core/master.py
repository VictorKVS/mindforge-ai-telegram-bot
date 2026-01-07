"""
File: src/core/agents/master.py

Purpose:
Master agent for MindForge DEMO.

Responsibilities:
- Receive access requests from store agents
- Apply UAG-style decision logic
- Emit decisions to system chat
- Write audit events (ALLOW / DENY)
- Orchestrate scenario flow

This agent contains SIMPLE decision logic for DEMO.
Real policies will be plugged later via UAG engine.
"""

from src.core.agents.base import AgentBase
from src.core.agents.registry import AGENTS


class MasterAgent(AgentBase):
    """
    Master (orchestrator / decision-maker) agent.
    """

    def __init__(
        self,
        *,
        agent_id: str,
        display_name: str = "Master Agent",
    ) -> None:
        super().__init__(
            agent_id=agent_id,
            role="master",
            display_name=display_name,
        )

    # ------------------------------------------------------------------
    # Decision logic (DEMO UAG)
    # ------------------------------------------------------------------
    def evaluate_access(
        self,
        *,
        store_id: str,
        resource: str,
    ) -> None:
        """
        Evaluate access request from a store agent.
        """

        if not self.is_running:
            self.say("Cannot evaluate request: master is offline")
            return

        store = AGENTS.get(store_id)

        if not store:
            self.say(f"Unknown store agent: {store_id}")
            return

        self.say(
            f"Evaluating access request from {store_id} "
            f"for resource `{resource}`"
        )

        # -----------------------------
        # DEMO policy logic
        # -----------------------------
        if resource == "inventory_api":
            decision = "ALLOW"
            policy = "UAG-DEMO-ALLOW-001"
            reason = "Inventory access allowed for store agents"
        else:
            decision = "DENY"
            policy = "UAG-DEMO-DENY-001"
            reason = f"Access to {resource} is not permitted"

        # -----------------------------
        # Emit decision
        # -----------------------------
        self.say(
            f"Decision for {store_id}: {decision} "
            f"(policy={policy})"
        )

        self.audit(
            action="access_decision",
            decision=decision,
            policy=policy,
            reason=reason,
        )

        # -----------------------------
        # Apply decision
        # -----------------------------
        if decision == "ALLOW":
            store.perform_action(f"access:{resource}")
        else:
            store.say(
                f"Access denied by master "
                f"(policy={policy})"
            )
