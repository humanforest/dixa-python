"""A Python module for interacting and consuming responses from Dixa."""
import logging
from typing import Union

import requests
from pydantic import BaseModel, Field, PrivateAttr, SecretStr
from requests import Response, Request

from . import errors as e
from .utils import get_user_agent, _get_url


class BaseClient(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    api_key: Union[SecretStr, str]
    base_url: str
    api_version: str = Field(default="v1")
    timeout: int = Field(default=30)
    headers: dict = Field(default={"User-Agent": get_user_agent()})
    _logger: logging.Logger = PrivateAttr(default=logging.getLogger(__name__))
    _session: requests.Session = PrivateAttr(default=requests.Session())

    def api_call(self,
                 endpoint: str = None,
                 method: str = "GET",
                 json: dict = None,
                 params: dict = None,
                 headers: dict = None,
                 pagination: bool = False,
                 return_data: bool = True
                 ) -> Union[dict, list, Response]:
        """Send an api call to Dixa API.

        Args:
            endpoint: The target Dixa API endpoint.
            method: HTTP verb. e.g. "POST"
            json: JSON for the body to attach to the request.
                This will append "Content-Type": "application/json" to the headers.
            params: The URL parameters to append to the URL.
                e.g. {"key1": "value1", "key2": "value2"}
            headers: Additional request headers
            pagination: Used for recursive functions to paginate between pages.
            return_data: If True (default) will return the dictionary from the data key,
                otherwise will return the Response object.

        Returns:
            Response: The successful response from the Dixa API.

        Raises:
            DixaApiError: The request to the Dixa API failed.
        """

        api_url = _get_url(self.base_url, "" if pagination else self.api_version, endpoint)
        headers = headers or {}
        headers.update(self.headers)
        headers["Authorization"] = self.api_key.get_secret_value()
        params = params or {}

        prepped = Request(method=method, url=api_url, headers=headers, json=json, params=params).prepare()
        response = self._session.send(prepped, timeout=self.timeout)

        if response.ok:
            if self._logger.level <= logging.DEBUG:
                debug_text = "Received the following response\n" \
                             f"status: {response.status_code}\n" \
                             f"headers: {response.headers}\n" \
                             f"body: {response.text}"
                self._logger.debug(debug_text)

            if return_data and "application/json" in response.headers.get("Content-Type"):
                return response.json().get("data")
            return response

        error_message = f"The request to the Dixa API failed.\n" \
                        f"Error {response.status_code}: {response.reason}\n" \
                        f"Message: {response.text}"
        raise e.DixaApiError(message=error_message, response=response)
