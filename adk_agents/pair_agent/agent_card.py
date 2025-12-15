from a2a.types import AgentCard, AgentCapabilities

agent_card = AgentCard(
    name="pair_attack_agent",
    title="PAIR Attack Agent",
    description="A multi-agent system to demonstrate the PAIR (Prompt as an Injected Rapport) attack.",
    icon_emoji="🤝",
    version="0.1.0",
    url="http://localhost/pair",
    capabilities=AgentCapabilities(), 
    skills=[],
    defaultInputModes=["text"],
    defaultOutputModes=["text"]
)