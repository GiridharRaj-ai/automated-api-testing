import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL = os.getenv(
        "BASE_URL",
        "https://dummyjson.com"
    )

    API_TIMEOUT = int(
        os.getenv("API_TIMEOUT", "10")
    )

    API_TOKEN = os.getenv(
        "API_TOKEN",
        ""
    )