from agency_swarm import Agency, set_openai_key, set_openai_client
from SupportAgent import SupportAgent
from LeadAgent import LeadAgent
import os

#set_openai_key("sk-svcacct-wd2Pp8NBcGK4KFTzDRV1Yw2_VOUqnRn57YT0o_mNl8udHX_xBmaOS_wO9Hb3cT3BlbkFJX1L8NbuuDMOUZ3BsdN-J_92nJy6XwAG1tKNoswcc1pIK45zRXDNJogZST8hygA")  # Replace with your actual OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Error: No OPENAI_API_KEY found in environment. Please set a valid key.")

def main():
    # Create agents
    lead_agent = LeadAgent()
    support_agent = SupportAgent()
    
    # Define the agency
    agency = Agency([lead_agent, [lead_agent, support_agent]],
        shared_instructions='./agency_manifesto.md',
        max_prompt_tokens=25000,
        temperature=0.3
    )
    
    # Run the agency demo
    agency.demo_gradio()

if __name__ == '__main__':
    main()
