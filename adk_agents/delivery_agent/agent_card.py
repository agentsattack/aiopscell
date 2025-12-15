from a2a.types import AgentCard, AgentCapabilities
# Remove the import of the agent instance

agent_card = AgentCard(
    name="delivery_agent",
    title="Delivery Agent",
    description="Handles all network communication with the target chatbot.",
    icon_emoji="📡",
    version="0.1.0",
    url="http://localhost/delivery",
    capabilities=AgentCapabilities(),
    skills=[],
    defaultInputModes=["text"],
    defaultOutputModes=["text"]
)