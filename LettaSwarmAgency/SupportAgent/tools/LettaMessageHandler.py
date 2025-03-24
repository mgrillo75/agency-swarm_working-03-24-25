from agency_swarm.tools import BaseTool
from pydantic import Field
from letta import create_client

class LettaMessageHandler(BaseTool):
    message: str = Field(..., description="The message to be sent to the Letta agent.")

    def run(self):
        try:
            # Create or retrieve the Letta client
            client = create_client()
            
            # Get the agent ID using correct method
            agent_id = self._shared_state.get("LettaAgentID")
            
            if not agent_id:
                return "No Letta agent ID found. Please initialize the Letta agent first."
                
            response = client.send_message(agent_id=agent_id, message=self.message, role="user")
            
            if response and response.messages:
                return f"Response from Letta agent: {response}"
            else:
                return "No response received from the Letta agent."
                
        except Exception as e:
            return f"Communication error: {str(e)}"
