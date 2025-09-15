




import uvicorn
import os
import sys
from pathlib import Path

# Add parent directory to path to allow importing from app
sys.path.append(str(Path(__file__).parent))

from app.utils.init_data import init_sample_data

if __name__ == "__main__":
    # Initialize sample data
    init_sample_data()
    
    # Run the application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=51209,  # Using the port provided in the runtime information
        reload=True,
        log_level="info"
    )




