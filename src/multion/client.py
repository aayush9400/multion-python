# This file was auto-generated by Fern from our API Definition.

import os
import typing
import urllib.parse
from json.decoder import JSONDecodeError

import httpx

from .core.api_error import ApiError
from .core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .core.jsonable_encoder import jsonable_encoder
from .core.remove_none_from_dict import remove_none_from_dict
from .core.request_options import RequestOptions
from .core.unchecked_base_model import construct_type
from .environment import MultiOnEnvironment
from .errors.bad_request_error import BadRequestError
from .errors.internal_server_error import InternalServerError
from .errors.unauthorized_error import UnauthorizedError
from .errors.unprocessable_entity_error import UnprocessableEntityError
from .sessions.client import AsyncSessionsClient, SessionsClient
from .types.bad_request_response import BadRequestResponse
from .types.browse_output import BrowseOutput
from .types.http_validation_error import HttpValidationError
from .types.internal_server_error_response import InternalServerErrorResponse
from .types.optional_params import OptionalParams
from .types.unauthorized_response import UnauthorizedResponse

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class MultiOn:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters:
        - base_url: typing.Optional[str]. The base url to use for requests from the client.

        - environment: MultiOnEnvironment. The environment to use for requests from the client. from .environment import MultiOnEnvironment

                                           Defaults to MultiOnEnvironment.DEFAULT

        - api_key: typing.Optional[str].

        - timeout: typing.Optional[float]. The timeout to be used, in seconds, for requests by default the timeout is 60 seconds, unless a custom httpx client is used, in which case a default is not set.

        - follow_redirects: typing.Optional[bool]. Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

        - httpx_client: typing.Optional[httpx.Client]. The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.
    ---
    from multion.client import MultiOn

    client = MultiOn(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: MultiOnEnvironment = MultiOnEnvironment.DEFAULT,
        api_key: typing.Optional[str] = os.getenv("MULTION_API_KEY"),
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.Client] = None,
    ):
        _defaulted_timeout = timeout if timeout is not None else 60 if httpx_client is None else None
        if api_key is None:
            raise ApiError(
                body="The client must be instantiated be either passing in api_key or setting MULTION_API_KEY"
            )
        self._client_wrapper = SyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.Client(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.Client(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.sessions = SessionsClient(client_wrapper=self._client_wrapper)

    def browse(
        self,
        *,
        cmd: str,
        url: typing.Optional[str] = OMIT,
        local: typing.Optional[bool] = OMIT,
        session_id: typing.Optional[str] = OMIT,
        max_steps: typing.Optional[int] = OMIT,
        include_screenshot: typing.Optional[bool] = OMIT,
        optional_params: typing.Optional[OptionalParams] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BrowseOutput:
        """
        Allows for browsing the web using detailed natural language instructions. The function supports multi-step command execution based on the `CONTINUE` status.

        Parameters:
            - cmd: str. A specific natural language instruction for the agent to execute

            - url: typing.Optional[str]. The URL to start or continue browsing from. (Default: google.com)

            - local: typing.Optional[bool]. Boolean flag to indicate if session to be run locally or in the cloud (Default: False)

            - session_id: typing.Optional[str]. Continues the session with session_id if provided.

            - max_steps: typing.Optional[int]. Maximum number of steps to execute. (Default: 20)

            - include_screenshot: typing.Optional[bool]. Boolean flag to include a screenshot of the final page.

            - optional_params: typing.Optional[OptionalParams].

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from multion.client import MultiOn

        client = MultiOn(
            api_key="YOUR_API_KEY",
        )
        client.browse(
            cmd="find the top post on hackernews",
            url="https://news.ycombinator.com/",
        )
        """
        _request: typing.Dict[str, typing.Any] = {"cmd": cmd}
        if url is not OMIT:
            _request["url"] = url
        if local is not OMIT:
            _request["local"] = local
        if session_id is not OMIT:
            _request["session_id"] = session_id
        if max_steps is not OMIT:
            _request["max_steps"] = max_steps
        if include_screenshot is not OMIT:
            _request["include_screenshot"] = include_screenshot
        if optional_params is not OMIT:
            _request["optional_params"] = optional_params
        _response = self._client_wrapper.httpx_client.request(
            method="POST",
            url=urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "browse"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(_request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(_request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return typing.cast(BrowseOutput, construct_type(type_=BrowseOutput, object_=_response.json()))  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(
                typing.cast(BadRequestResponse, construct_type(type_=BadRequestResponse, object_=_response.json()))  # type: ignore
            )
        if _response.status_code == 401:
            raise UnauthorizedError(
                typing.cast(UnauthorizedResponse, construct_type(type_=UnauthorizedResponse, object_=_response.json()))  # type: ignore
            )
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
            )
        if _response.status_code == 500:
            raise InternalServerError(
                typing.cast(InternalServerErrorResponse, construct_type(type_=InternalServerErrorResponse, object_=_response.json()))  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncMultiOn:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters:
        - base_url: typing.Optional[str]. The base url to use for requests from the client.

        - environment: MultiOnEnvironment. The environment to use for requests from the client. from .environment import MultiOnEnvironment

                                           Defaults to MultiOnEnvironment.DEFAULT

        - api_key: typing.Optional[str].

        - timeout: typing.Optional[float]. The timeout to be used, in seconds, for requests by default the timeout is 60 seconds, unless a custom httpx client is used, in which case a default is not set.

        - follow_redirects: typing.Optional[bool]. Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

        - httpx_client: typing.Optional[httpx.AsyncClient]. The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.
    ---
    from multion.client import AsyncMultiOn

    client = AsyncMultiOn(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: MultiOnEnvironment = MultiOnEnvironment.DEFAULT,
        api_key: typing.Optional[str] = os.getenv("MULTION_API_KEY"),
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
    ):
        _defaulted_timeout = timeout if timeout is not None else 60 if httpx_client is None else None
        if api_key is None:
            raise ApiError(
                body="The client must be instantiated be either passing in api_key or setting MULTION_API_KEY"
            )
        self._client_wrapper = AsyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.sessions = AsyncSessionsClient(client_wrapper=self._client_wrapper)

    async def browse(
        self,
        *,
        cmd: str,
        url: typing.Optional[str] = OMIT,
        local: typing.Optional[bool] = OMIT,
        session_id: typing.Optional[str] = OMIT,
        max_steps: typing.Optional[int] = OMIT,
        include_screenshot: typing.Optional[bool] = OMIT,
        optional_params: typing.Optional[OptionalParams] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BrowseOutput:
        """
        Allows for browsing the web using detailed natural language instructions. The function supports multi-step command execution based on the `CONTINUE` status.

        Parameters:
            - cmd: str. A specific natural language instruction for the agent to execute

            - url: typing.Optional[str]. The URL to start or continue browsing from. (Default: google.com)

            - local: typing.Optional[bool]. Boolean flag to indicate if session to be run locally or in the cloud (Default: False)

            - session_id: typing.Optional[str]. Continues the session with session_id if provided.

            - max_steps: typing.Optional[int]. Maximum number of steps to execute. (Default: 20)

            - include_screenshot: typing.Optional[bool]. Boolean flag to include a screenshot of the final page.

            - optional_params: typing.Optional[OptionalParams].

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from multion.client import AsyncMultiOn

        client = AsyncMultiOn(
            api_key="YOUR_API_KEY",
        )
        await client.browse(
            cmd="find the top post on hackernews",
            url="https://news.ycombinator.com/",
        )
        """
        _request: typing.Dict[str, typing.Any] = {"cmd": cmd}
        if url is not OMIT:
            _request["url"] = url
        if local is not OMIT:
            _request["local"] = local
        if session_id is not OMIT:
            _request["session_id"] = session_id
        if max_steps is not OMIT:
            _request["max_steps"] = max_steps
        if include_screenshot is not OMIT:
            _request["include_screenshot"] = include_screenshot
        if optional_params is not OMIT:
            _request["optional_params"] = optional_params
        _response = await self._client_wrapper.httpx_client.request(
            method="POST",
            url=urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "browse"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(_request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(_request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return typing.cast(BrowseOutput, construct_type(type_=BrowseOutput, object_=_response.json()))  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(
                typing.cast(BadRequestResponse, construct_type(type_=BadRequestResponse, object_=_response.json()))  # type: ignore
            )
        if _response.status_code == 401:
            raise UnauthorizedError(
                typing.cast(UnauthorizedResponse, construct_type(type_=UnauthorizedResponse, object_=_response.json()))  # type: ignore
            )
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
            )
        if _response.status_code == 500:
            raise InternalServerError(
                typing.cast(InternalServerErrorResponse, construct_type(type_=InternalServerErrorResponse, object_=_response.json()))  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


def _get_base_url(*, base_url: typing.Optional[str] = None, environment: MultiOnEnvironment) -> str:
    if base_url is not None:
        return base_url
    elif environment is not None:
        return environment.value
    else:
        raise Exception("Please pass in either base_url or environment to construct the client")
