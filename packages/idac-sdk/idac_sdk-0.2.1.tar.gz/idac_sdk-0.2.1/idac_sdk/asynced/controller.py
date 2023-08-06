from typing import Dict, Optional, Tuple, Union
import ujson
import httpx
from base64 import b64encode
import warnings

from idac_sdk.config import have_config, load_config
from idac_sdk.types import IDACAuthType
from . import DEFAULT_USER_AGENT
from idac_sdk.errors import (
    IncorrectControllerProtoError,
    IncorrectControllerURLError,
    NoAuth,
    NoAuthTokenInResponse,
    NoIDACConfig,
    NoIdError,
)


class IDACController:
    proto: str
    url: str
    api_version: str
    auth_type: IDACAuthType
    auth: Optional[str]
    user_agent: str

    def __init__(
        self,
        proto: Optional[str] = None,
        url: Optional[str] = None,
        api_version: Optional[str] = None,
        auth_type: Optional[IDACAuthType] = None,
        auth: Optional[Union[str, Tuple[str, str]]] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """
        IDACController Object

        IDACController describes iDAC controller instance.
        Handles generation of API URLs and Auth Headers required for authentication.

        Args:
            proto (str, optional): `http` or `https`.
            url (str, optional): URL of the controller.
            api_version (str, optional): API version.
            auth_type (IDACAuthType, optional): Type of authentication.
            auth (Union[str, Tuple[str, str]], optional): Authentication data. Usually a token. If
                BASIC auth type is set, can be specified as a tuple in format [username, password]
                which will be automatically encoded in base64. Defaults to None.
            user_agent (Optional[str]): User-Agent string.

        Returns:
            None

        Raises:
            IncorrectControllerProtoError: Raised if incorrect proto provided
            IncorrectControllerURLError: Raised if no URL provided
        """
        if not have_config():
            warnings.warn("iDAC config not found", NoIDACConfig)

        cfg = load_config()

        self.proto = proto if proto else cfg.defaults.idac_proto
        if proto != "http" and proto != "https":
            raise IncorrectControllerProtoError(f"Unsupported proto: {proto}")

        self.url = url if url else cfg.defaults.idac_fqdn
        if not self.url:
            raise IncorrectControllerURLError("Controller URL not provided")

        self.user_agent = user_agent if user_agent else DEFAULT_USER_AGENT
        self.api_version = api_version if api_version else cfg.defaults.api_version

        self.auth_type = auth_type if auth_type else IDACAuthType[cfg.defaults.auth_type]
        if auth_type == IDACAuthType.BASIC and isinstance(auth, list):
            # auth is [username, password], encode and store Base64
            if isinstance(auth, list):
                self.auth = b64encode(bytes(f"{auth[0]}:{auth[1]}", "utf-8")).decode("utf-8")
            else:
                self.auth = auth if auth else cfg.defaults.auth
        else:
            self.auth = auth if auth and isinstance(auth, str) else cfg.defaults.auth

    def api_string(self, api: str) -> str:
        """Generate full URL for an API

        Args:
          api (str): API

        Returns:
          str: Full API URL
        """
        result = f"{self.proto}://{self.url}"
        if not result.endswith("/"):
            result = result + "/"
        return result + f"api/v{self.api_version}/{api}"

    def auth_headers(self) -> Dict[str, str]:
        """Generates Authorization headers required for APIs

        Returns:
          Dict[str, str]: Headers
        """
        if self.auth_type == IDACAuthType.NONE:
            return {}

        if not self.auth:
            raise NoAuth("No authentication data")

        if self.auth_type == IDACAuthType.BASIC:
            return {"Authorization": f"Basic {self.auth}"}

        if self.auth_type == IDACAuthType.BEARER:
            return {"Authorization": f"Bearer {self.auth}"}

        if self.auth_type == IDACAuthType.DCLOUD_SESSION:
            return {"Authorization": f"Bearer {self.auth}"}

        return {}

    def with_auth(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Adds auth headers to `headers` param. Also returns that dictionary.

        Example:
        ```
        h = {"Accept": "application/json"}
        idac_controller.with_auth(h)
        ```

        Args:
          headers (Dict[str, str]): Dictionary where headers should be added

        Returns:
          Dict[str, str]: Updated dictionary
        """
        if self.auth_type == IDACAuthType.NONE:
            return headers

        if not isinstance(headers, dict):
            raise Exception("Headers not provided")

        headers.update(self.auth_headers())
        return headers

    def api_create_stateless(self) -> Tuple[str, str]:
        """Generate URL for "Create Stateless Request" API

        Returns:
          Tuple[str, str]: [URL, Method]
        """
        return self.api_string("request/stateless/0"), "GET"

    def api_create_stateful(self) -> Tuple[str, str]:
        """Generate URL for "Create Stateful Request" API

        Returns:
          Tuple[str, str]: [URL, Method]
        """
        return self.api_string("request/stateful/0"), "GET"

    def api_create(self) -> Tuple[str, str]:
        """Generate URL for "Create Request" API

        Returns:
          Tuple[str, str]: [URL, Method]
        """
        return self.api_string("request/0"), "POST"

    def api_get_state(self, id: str) -> Tuple[str, str]:
        """Generate URL for "Get Request State" API

        Args:
          id (str): ID of a request

        Returns:
          Tuple[str, str]: [URL, Method]
        """
        if not id:
            raise NoIdError("No ID provided for API")
        return self.api_string(f"request/{id}"), "GET"

    def api_restart(self, id: str) -> Tuple[str, str]:
        """Generate URL for "Restart Request" API

        Args:
          id (str): ID of a request

        Returns:
          Tuple[str, str]: [URL, Method]
        """
        if not id:
            raise NoIdError("No ID provided for API")
        return self.api_string(f"request/restart/{id}"), "POST"

    def api_cleanup(self, id: str) -> Tuple[str, str]:
        """Generate URL for "Cleanup Request" API

        Args:
          id (str): ID of a request

        Returns:
          Tuple[str, str]: [URL, Method]
        """
        if not id:
            raise NoIdError("No ID provided for API")
        return self.api_string(f"request/cleanup/{id}"), "POST"

    def api_extend(self, id: str, minutes: int) -> Tuple[str, str]:
        """Generate URL to extend request by `minutes` minutes

        Args:
            id (str): ID of a request
            minutes (int): amount of minutes

        Raises:
            NoIdError: Raised if no ID provided

        Returns:
            Tuple[str, str]: [URL, method]
        """
        if not id:
            raise NoIdError("No ID provided for API")
        return self.api_string(f"request/extend/{minutes}/{id}"), "POST"

    def api_force_cleanup(self, id: str) -> Tuple[str, str]:
        """Generate URL for "Force Cleanup Request" API

        Args:
          id (str): ID of a request

        Returns:
          Tuple[str, str]: [URL, Method]
        """
        if not id:
            raise NoIdError("No ID provided for API")
        return self.api_string(f"request/forcecleanup/{id}"), "POST"

    def drop_auth(self) -> None:
        """Resets Auth"""
        self.auth = None

    async def get_auth_token(self, creds: str, datacenter: str, use_as_auth: bool = True) -> str:
        """Requests auth token from controller. Required for DCLOUD_SESSION auth type

        Args:
            creds (str): `creds` token from session.xml dCloud file
            datacenter (str): dCloud datacenter where session runs
            use_as_auth (bool, optional): If True, response will be used as `auth` for
                `auth_headers` & `with_auth` methods. Defaults to True.

        Raises:
            NoAuthTokenInResponse: Raised if no token received in response

        Returns:
            str: Auth token
        """
        if self.auth:
            return self.auth

        api = self.api_string("auth/token")
        headers = {"Content-Type": "application/json"}
        data = {
            "token": creds,
            "datacenter": datacenter,
        }

        async with httpx.AsyncClient() as client:
            client.headers.update({"User-Agent": self.user_agent})
            response = await client.post(api, headers=headers, json=data)
            response.raise_for_status()
            json_body = ujson.loads(response.text)
            if isinstance(json_body, dict) and json_body.get("token", None):
                if use_as_auth:
                    self.auth = json_body["token"]
                return json_body["token"]
            raise NoAuthTokenInResponse("Didn't receive auth token from controller")
