import asyncio
import os
import sys
from dotenv import load_dotenv


load_dotenv()

# Now it is safe to import the manager
from manager import run_collaboration

if __name__ == "__main__":
    if not os.environ.get("GOOGLE_API_KEY"):
        print("ERROR: Google API Key not found in .env")
        print("Please check your .env file.")
        sys.exit(1)

    # Launch the Team Lead
    asyncio.run(run_collaboration())