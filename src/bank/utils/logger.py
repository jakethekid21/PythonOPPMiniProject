from __future__ import annotations

import logging
from pathlib import Path


def setup_logging() -> None:
    """
    Configure logging:
    - Console: INFO
    - logs/app.log: INFO
    - logs/errors.log: WARNINGs
    """
    Path("logs").mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Handlers 
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    app_file_handler = logging.FileHandler("logs/app.log")
    app_file_handler.setLevel(logging.INFO)
    app_file_handler.setFormatter(formatter)

    err_file_handler = logging.FileHandler("logs/errors.log")
    err_file_handler.setLevel(logging.WARNING)
    err_file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(app_file_handler)
    logger.addHandler(err_file_handler)