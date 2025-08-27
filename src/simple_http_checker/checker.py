import logging
from typing import Collection

import requests

logger = logging.getLogger(__name__)

def check_urls(urls: Collection[str], timeout: int = 5) -> dict[str, str]:
    """
    Checks a list of URLs and returns their status.

    :param urls: A list of URLs to check.
    :param timeout: Maximum time in seconds to wait for each request. Defaults to 5 seconds.
    :return: A dictionary mapping URLs to their status strings.
    """

    logger.info(f"Checking {len(urls)} URLs with a timeout of {timeout} seconds...")
    results = {}

    for url in urls:
        status = "UNKNOWN"

        try:
            logger.info(f"Checking {url}...")
            response = requests.get(url, timeout=timeout)
            if response.ok:
                status = f"{response.status_code} OK"
            else:
                status = f"{response.status_code} {response.reason}"
        except requests.exceptions.Timeout:
            status = "TIMEOUT"
            logger.warning(f"Request for {url} timed out.")
        except requests.exceptions.ConnectionError:
            status = "CONNECTION_ERROR"
            logger.warning(f"Connection error for {url}.")
        except requests.exceptions.RequestException as e:
            status = f"REQUEST_ERROR: {type(e).__name__}"
            logger.error(f"An unexpected request error for {url}. {e}",
                         exc_info=True)
        results[url] = status
        logger.debug(f"Checked {url:<40} -> {status}")

    logger.info("URL check finished")
    return results



