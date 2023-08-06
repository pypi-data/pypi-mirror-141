import logging
import os
import re
import sys
from typing import Optional
from enum import Enum

import zhipuai

zhipuai_LOG = os.environ.get("zhipuai_LOG")

logger = logging.getLogger("zhipuai")

__all__ = [
    "log_info",
    "log_debug",
    "log_warn",
    "logfmt",
]

api_key_to_header = lambda api, key: {"Authorization": f"Bearer {key}"} if api == ApiType.ZHIPU_AI else {"api-key": f"{key}"}

class ApiType(Enum):
    # AZURE = 1
    # OPEN_AI = 2
    ZHIPU_AI = 1

    @staticmethod
    def from_str(label):
        # if label.lower() == 'azure':
        #     return ApiType.AZURE
        # elif label.lower() in ('open_ai', 'zhipuai'):
        #     return ApiType.OPEN_AI
        if label.lower() in ('zhipu_ai', 'zhipuai'):
            return  ApiType.ZHIPU_AI
        else:
            raise zhipuai.error.InvalidAPIType("The API type provided in invalid. Please select one of the supported API types: 'azure', 'open_ai'")    


def _console_log_level():
    if zhipuai.log in ["debug", "info"]:
        return zhipuai.log
    elif zhipuai_LOG in ["debug", "info"]:
        return zhipuai_LOG
    else:
        return None


def log_debug(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() == "debug":
        print(msg, file=sys.stderr)
    logger.debug(msg)


def log_info(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() in ["debug", "info"]:
        print(msg, file=sys.stderr)
    logger.info(msg)


def log_warn(message, **params):
    msg = logfmt(dict(message=message, **params))
    print(msg, file=sys.stderr)
    logger.warn(msg)


def logfmt(props):
    def fmt(key, val):
        # Handle case where val is a bytes or bytesarray
        if hasattr(val, "decode"):
            val = val.decode("utf-8")
        # Check if val is already a string to avoid re-encoding into ascii.
        if not isinstance(val, str):
            val = str(val)
        if re.search(r"\s", val):
            val = repr(val)
        # key should already be a string
        if re.search(r"\s", key):
            key = repr(key)
        return "{key}={val}".format(key=key, val=val)

    return " ".join([fmt(key, val) for key, val in sorted(props.items())])


def get_object_classes():
    # This is here to avoid a circular dependency
    from zhipuai.object_classes import OBJECT_CLASSES

    return OBJECT_CLASSES


def convert_to_zhipuai_object(
    resp,
    api_key=None,
    api_version=None,
    organization=None,
    engine=None,
    plain_old_data=False,
):
    # If we get a zhipuaiResponse, we'll want to return a zhipuaiObject.

    response_ms: Optional[int] = None
    if isinstance(resp, zhipuai.zhipuai_response.zhipuaiResponse):
        organization = resp.organization
        response_ms = resp.response_ms
        resp = resp.data

    if plain_old_data:
        return resp
    elif isinstance(resp, list):
        return [
            convert_to_zhipuai_object(
                i, api_key, api_version, organization, engine=engine
            )
            for i in resp
        ]
    elif isinstance(resp, dict) and not isinstance(
        resp, zhipuai.zhipuai_object.zhipuaiObject
    ):
        resp = resp.copy()
        klass_name = resp.get("object")
        if isinstance(klass_name, str):
            klass = get_object_classes().get(
                klass_name, zhipuai.zhipuai_object.zhipuaiObject
            )
        else:
            klass = zhipuai.zhipuai_object.zhipuaiObject

        return klass.construct_from(
            resp,
            api_key=api_key,
            api_version=api_version,
            organization=organization,
            response_ms=response_ms,
            engine=engine,
        )
    else:
        return resp


def convert_to_dict(obj):
    """Converts a zhipuaiObject back to a regular dict.

    Nested zhipuaiObjects are also converted back to regular dicts.

    :param obj: The zhipuaiObject to convert.

    :returns: The zhipuaiObject as a dict.
    """
    if isinstance(obj, list):
        return [convert_to_dict(i) for i in obj]
    # This works by virtue of the fact that zhipuaiObjects _are_ dicts. The dict
    # comprehension returns a regular dict and recursively applies the
    # conversion to each value.
    elif isinstance(obj, dict):
        return {k: convert_to_dict(v) for k, v in obj.items()}
    else:
        return obj


def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def default_api_key() -> str:
    if zhipuai.api_key_path:
        with open(zhipuai.api_key_path, "rt") as k:
            api_key = k.read().strip()
            if not api_key.startswith("sk-"):
                raise ValueError(f"Malformed API key in {zhipuai.api_key_path}.")
            return api_key
    elif zhipuai.api_key is not None:
        return zhipuai.api_key
    else:
        raise zhipuai.error.AuthenticationError(
            "No API key provided. You can set your API key in code using 'zhipuai.api_key = <API-KEY>', or you can set the environment variable zhipuai_API_KEY=<API-KEY>). If your API key is stored in a file, you can point the zhipuai module at it with 'zhipuai.api_key_path = <PATH>'. You can generate API keys in the zhipuai web interface. See https://onboard.zhipuai.com for details, or email support@zhipuai.com if you have any questions."
        )

def default_api_version() ->str:
    return zhipuai.api_version 
