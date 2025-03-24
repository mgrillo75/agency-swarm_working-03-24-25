from agency_swarm.agents import Agent

class LeadAgent(Agent):
    def __init__(self):
        super().__init__(
            name="LeadAgent",
            description="The Lead Agent is the primary communicator with the user and the Support Agent within the LettaSwarmAgency. It initiates communication with the Support Agent and ensures effective data exchange.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],  # No tools for LeadAgent; it delegates tasks to SupportAgent
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
            #model="o3-mini"
        )

    def response_validator(self, message):
        if "delegate_to_support" in message:
            letta_agent_id = self._shared_state.get("LettaAgentID")
            if not letta_agent_id:
                return "Error: Letta agent not initialized. Please coordinate with SupportAgent for initialization."
        return message
