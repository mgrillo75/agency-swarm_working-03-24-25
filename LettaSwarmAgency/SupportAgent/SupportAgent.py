from agency_swarm.agents import Agent
from .tools.LettaClientAgentInitializer import LettaClientAgentInitializer
from .tools.LettaMessageHandler import LettaMessageHandler


class SupportAgent(Agent):
    def __init__(self):
        super().__init__(
            name="SupportAgent",
            description="The Support Agent within the LettaSwarmAgency communicates with the Lead Agent and the Letta Framework Agent. It is equipped with tools for Letta agent initialization and message handling.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[LettaClientAgentInitializer, LettaMessageHandler],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
            #model="o3-mini"
        )
        
        # Initialize the Letta Memory agent on startup
        letta_initializer = LettaClientAgentInitializer(
            agent_name="LettaMemoryAgent",
            persona="""My name is LettaMemoryAgent. I am a specialized memory manager in Letta's framework, optimizing memory operations and facilitating smooth 
                    interaction with users. I ensure efficient memory utilization and effective collaboration with users to store important information.""",
            human_name="LeadAgent"
        )
        init_result = letta_initializer.run()
        print(f"Letta Memory Agent Initialization: {init_result}")

    def response_validator(self, message):
        letta_agent_id = self._shared_state.get("LettaAgentID")
        if not letta_agent_id:
            return "Error: Letta agent not initialized. Please ensure initialization is complete."
        return message
