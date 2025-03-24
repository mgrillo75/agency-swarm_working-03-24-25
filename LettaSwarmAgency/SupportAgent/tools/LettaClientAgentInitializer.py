from agency_swarm.tools import BaseTool
from pydantic import Field
from letta import create_client, LLMConfig, EmbeddingConfig
from letta.schemas.memory import ChatMemory
import os

class LettaClientAgentInitializer(BaseTool):
    """
    A tool to initialize a Letta client and set up an agent with default configurations.
    This tool initializes a Letta client, sets default configurations for LLM and embedding,
    and ensures an agent is created or retrieved with the specified name and memory.
    """
    agent_name: str = Field(
        ..., description="The name of the agent to be created or retrieved within the Letta framework."
    )
    
    persona: str = Field(
        ..., description="The persona for the agent's memory, describing its role and capabilities."
    )
    
    human_name: str = Field(
        ..., description="The human identifier interacting with the agent."
    )

    def run(self):
        """
        Initialize the Letta client and agent with the given configurations, using a valid
        OPENAI_API_KEY from the environment instead of hardcoding it.
        """
        # Read API key from environment, raise an error if not found
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "Error: No OPENAI_API_KEY found in environment. Please set a valid key."

        # Initialize Letta client
        client = create_client()

        # Configure default LLM and embedding settings
        client.set_default_llm_config(LLMConfig.default_config("gpt-4o"))
        client.set_default_embedding_config(EmbeddingConfig.default_config(model_name="text-embedding-ada-002"))

        # Check if the agent already exists
        agent_id = client.get_agent_id(self.agent_name)
        if agent_id:
            self._shared_state.set("LettaAgentID", agent_id)
            return f"Letta agent '{self.agent_name}' already exists with ID: {agent_id}"
        else:
            # Initialize agent with chat memory
            agent_state = client.create_agent(
                name=self.agent_name,
                memory=ChatMemory(
                    persona=self.persona,
                    human=self.human_name
                )
            )
            # client._shared_state.set("LettaAgentID", agent_state.id)            
            self._shared_state.set("LettaAgentID", agent_state.id)
            return f"Letta agent '{self.agent_name}' created successfully with ID: {agent_state.id}"

if __name__ == "__main__":
    # Example usage
    tool = LettaClientAgentInitializer(
        agent_name="LettaMemoryAgent",
        persona="""My name is LettaMemoryAgent. I am a specialized memory manager in Letta's framework, optimizing memory operations and facilitating smooth 
                    interaction with users. I ensure efficient memory utilization and effective collaboration with users to store important information.""",
        human_name="Name: LeadAgent"
    )
    print(tool.run())
