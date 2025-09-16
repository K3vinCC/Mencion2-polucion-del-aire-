# run.py
from src.infrastructure.web.app import create_app
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT", 5000))