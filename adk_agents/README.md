# AIOPSCell: Adversarial AI Testing Toolkit

**AIOPSCell** is an automated Red Teaming framework built on the Google Agent Development Kit (ADK). It utilizes the **TAP (Tree of Attacks with Pruning)** methodology to systematically test AI models for vulnerabilities.

## 📂 Project Structure

* **`adk_agents/tap_agent/`**: Contains the core logic for the Attacker (TAP) and the BatchHandler.

* **`adk_agents/delivery_agent/`**: Handles the connection to the Target model.

* **`adk_agents/pair_agent/`**: Contains the core logic for the Attacker (PAIR)

* **`main.py`**: The entry point for running the attack simulation.

## 🚀 Installation

1. **Prerequisites**:

   * Python 3.12+

   * An active Google Cloud Project

   * API Keys for Google (Gemini) and Anthropic (optional, if using Claude). Place in .env file

2. **Setup Virtual Environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate

   pip install -r requirements.txt
