import platform
import re
import sys
from typing import Optional
from urllib.parse import urljoin, parse_qs

from . import __version__


def camel_case(string: str) -> str:
    first, *others = string.split('_')
    return ''.join([first.lower(), *map(str.title, others)])


def snake_case(string: str) -> str:
    return re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))').sub(r'_\1', string).lower()


def get_user_agent(prefix: Optional[str] = None, suffix: Optional[str] = None) -> str:
    """Construct the user-agent header with the package info,
    Python version and OS version.

    Args:
        prefix: Text to be displayed before user agent
        suffix: Text to be displayed after user agent

    Returns:
        The user agent string.
        e.g. 'Python/3.8.3 DixaClient/0.1.0 Darwin/20.3.0'
    """

    client = f"DixaClient/{__version__}"
    python_version = "Python/{v.major}.{v.minor}.{v.micro}".format(v=sys.version_info)
    system_info = f"{platform.system()}/{platform.release()}"
    user_agent_string = " ".join([python_version, client, system_info])
    prefix = f"{prefix} " if prefix else ""
    suffix = f" {suffix}" if suffix else ""
    return prefix + user_agent_string + suffix


def _next_cursor_is_present(data: dict) -> bool:
    """Determine if the response contains 'next' and 'next' is not null.

    Returns:
        A boolean value.
    """

    return "meta" in data and data.get("meta") is not None and data["meta"].get("next") is not None


def _previous_cursor_is_present(data: dict) -> bool:
    """Determine if the response contains 'previous' and 'previous' is not null.

    Returns:
        A boolean value.
    """

    return "meta" in data and data.get("meta") is not None and data["meta"].get("previous") is not None


def _get_params(url: str):
    return parse_qs(url.split("?")[1])


def _get_url(base_url: str, api_version: str, endpoint: str) -> str:
    """Joins the base Dixa URL and an API method to form an absolute URL.

    Args:
        base_url (str): The base URL
        api_version: Dixa API version. e.g. "v1"
        endpoint (str): The Dixa API method. e.g. 'endusers'

    Returns:
        The absolute API URL.
            e.g. 'https://api.dixa.io/v1/endusers'
    """

    url_path = f"{api_version}/{endpoint if not endpoint.startswith('/') else endpoint[1:]}"
    return urljoin(base_url, url_path)
