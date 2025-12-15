
import os
import json
import requests
import mimetypes
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

# Centralized Configuration
TARGET_BASE_URL = os.getenv("TARGET_BASE_URL", "http://localhost:8080")
HEADERS = {}
if os.getenv("CLOUDFLARE_CLIENT_ID"):
    HEADERS["CF-Access-Client-Id"] = os.getenv("CLOUDFLARE_CLIENT_ID")
    HEADERS["CF-Access-Client-Secret"] = os.getenv("CLOUDFLARE_CLIENT_SECRET")

# --- GLOBAL SESSION STATE ---
SESSION = requests.Session()
SESSION.headers.update(HEADERS)

# --- TOOLS ---

def send_message(message: str) -> str:
    """Sends a message maintaining conversation state."""
    url = f"{TARGET_BASE_URL}/chat"
    try:
        response = SESSION.post(url, json={"prompt": message})
        response.raise_for_status()
        return json.dumps(response.json())
    except Exception as e:
        return json.dumps({"error": f"Connection failed: {str(e)}"})


def send_batch_messages(messages: list | str) -> str:
    """
    Sends a BATCH of prompts to the target.
    
    Args:
        messages: Either a list of strings, or a JSON string containing a list.
                  Can also handle list of dicts with 'payload' field.
    
    Returns:
        JSON string containing list of responses.
    """
    url = f"{TARGET_BASE_URL}/chat"
    results = []
    
    # --- ROBUST INPUT PARSING ---
    prompts = []
    
    # Case 1: Already a list
    if isinstance(messages, list):
        prompts = messages
    
    # Case 2: JSON string - needs parsing
    elif isinstance(messages, str):
        try:
            # Clean up common issues
            cleaned = messages.strip()
            
            # Try direct parse
            parsed = json.loads(cleaned)
            
            if isinstance(parsed, list):
                prompts = parsed
            else:
                prompts = [parsed]
                
        except json.JSONDecodeError as e:
            # Try to extract payloads using regex as fallback
            import re
            payload_matches = re.findall(r'"payload"\s*:\s*"((?:[^"\\]|\\.)*)"', messages)
            if payload_matches:
                # Unescape the payloads
                prompts = [p.replace('\\n', '\n').replace('\\"', '"') for p in payload_matches]
            else:
                return json.dumps([f"Batch Error: Could not parse messages - {e}"])
    
    else:
        return json.dumps([f"Batch Error: Invalid input type {type(messages)}"])
    
    # --- EXTRACT PAYLOADS IF NEEDED ---
    # Handle list of dicts with 'payload' field
    clean_prompts = []
    for p in prompts:
        if isinstance(p, dict):
            # Extract payload from dict
            payload = p.get('payload', p.get('message', str(p)))
            clean_prompts.append(str(payload))
        elif isinstance(p, str):
            clean_prompts.append(p)
        else:
            clean_prompts.append(str(p))
    
    # --- SEND EACH PROMPT ---
    print(f"[Delivery] Sending {len(clean_prompts)} messages to {url}")
    
    for i, prompt in enumerate(clean_prompts):
        try:
            # Clean up any remaining escape sequences
            prompt = prompt.replace('\\n', '\n').replace('\\"', '"')
            
            print(f"[Delivery] Message {i+1}: {prompt[:80]}...")
            
            res = SESSION.post(url, json={"prompt": prompt}, timeout=30)
            res.raise_for_status()
            
            response_data = res.json()
            response_text = response_data.get("response", str(response_data))
            results.append(response_text)
            
            print(f"[Delivery] Response {i+1}: {response_text[:80]}...")
            
        except requests.Timeout:
            results.append("Error: Request timed out")
        except Exception as e:
            results.append(f"Error: {e}")
    
    return json.dumps(results)


def upload_file(file_path: str, context_prompt: str) -> str:
    """Uploads a file maintaining conversation state."""
    url = f"{TARGET_BASE_URL}/chat_with_file"
    try:
        if not os.path.exists(file_path):
            return json.dumps({"error": f"File not found: {file_path}"})
            
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            if file_path.endswith(".pdf"):
                mime_type = "application/pdf"
            elif file_path.endswith(".docx"):
                mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            else:
                mime_type = "application/octet-stream"

        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, mime_type)}
            data = {'prompt': context_prompt}
            response = SESSION.post(url, files=files, data=data)
            return json.dumps(response.json())
    except Exception as e:
        return json.dumps({"error": f"Upload failed: {str(e)}"})


def reset_conversation() -> str:
    """Clears all cookies and conversation state."""
    global SESSION
    SESSION.cookies.clear()
    SESSION.headers.update(HEADERS) 
    try:
        # Also hit the reset endpoint if available
        SESSION.post(f"{TARGET_BASE_URL}/reset", timeout=5)
    except:
        pass
    return json.dumps({"result": "Conversation history and cookies cleared."})


# --- THE AGENT FACTORY ---

def create_delivery_agent() -> LlmAgent:
    return LlmAgent(
        name="DeliveryAgent",
        model=LiteLlm("gemini/gemini-2.5-flash"), 
        description="Connects to the chatbot. Maintains persistent state (cookies).",
        tools=[send_message, send_batch_messages, upload_file, reset_conversation],
        instruction="""
        You are the network interface.
        1. Receive a request.
        2. Execute it using the persistent session.
        3. Return the raw JSON.
        """
    )