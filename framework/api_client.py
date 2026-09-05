import logging
import time
from pathlib import Path

import requests

from framework.config import Config


BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "api.log"


logger = logging.getLogger("api_client")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


class APIClient:

    MAX_RETRIES = 3

    def __init__(self):
        self.session = requests.Session()

        if hasattr(Config, "API_TOKEN") and Config.API_TOKEN:
            self.session.headers.update({
                "Authorization": f"Bearer {Config.API_TOKEN}"
            })

    def get(self, url, **kwargs):
        return self._request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self._request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self._request("PUT", url, **kwargs)

    def delete(self, url, **kwargs):
        return self._request("DELETE", url, **kwargs)

    def _request(self, method, url, **kwargs):

        logger.info(
            f"REQUEST | {method} | {url}"
        )

        if "json" in kwargs:
            logger.info(
                f"REQUEST BODY | {kwargs['json']}"
            )

        for attempt in range(1, self.MAX_RETRIES + 1):

            try:
                response = self.session.request(
                    method,
                    url,
                    timeout=Config.API_TIMEOUT,
                    **kwargs
                )

                logger.info(
                    f"RESPONSE | Status: {response.status_code}"
                )

                try:
                    logger.info(
                        f"RESPONSE BODY | {response.json()}"
                    )
                except ValueError:
                    logger.info(
                        f"RESPONSE BODY | {response.text}"
                    )

                if response.status_code != 429:
                    return response

                logger.warning(
                    f"RATE LIMITED | "
                    f"Attempt {attempt}/{self.MAX_RETRIES}"
                )

                if attempt < self.MAX_RETRIES:
                    logger.info(
                        "RETRYING | Waiting 2 seconds"
                    )

                    time.sleep(2)

            except requests.RequestException as error:
                logger.error(
                    f"REQUEST ERROR | {error}"
                )
                raise

        return response