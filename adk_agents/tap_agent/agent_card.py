from a2a.types import AgentCard, AgentCapabilities

agent_card = AgentCard(
    name="tap_attack_agent",
    title="TAP Attack Agent",
    description="Tree of Attacks with Pruning. An evolutionary attack that branches multiple prompts.",
    icon_emoji="🌳",
    version="0.1.0",
    url="http://localhost/tap",
    capabilities=AgentCapabilities(),
    skills=[], 
    defaultInputModes=["text"],
    defaultOutputModes=["text"]
)