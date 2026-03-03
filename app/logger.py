# app/logger.py

import logging
import json
from datetime import datetime

# Configure logger
logger = logging.getLogger("gateway_logger")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


def log_event(event: dict):
    """
    Logs structured JSON events.
    """
    event["timestamp"] = datetime.utcnow().isoformat()
    logger.info(json.dumps(event))
