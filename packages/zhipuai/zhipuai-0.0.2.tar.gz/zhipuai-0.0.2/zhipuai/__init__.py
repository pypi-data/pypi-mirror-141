# zhipuai Python bindings.
#
# Originally forked from the MIT-licensed Stripe Python bindings.

import os
from typing import Optional

from zhipuai.api_resources import (
    # Answer,
    # Classification,
    Completion,
    # Embedding,
    # Engine,
    # ErrorObject,
    # File,
    # FineTune,
    # Model,
    # Search,
)
from zhipuai.error import APIError, InvalidRequestError, ZhipuAIError

api_key = os.environ.get("ZHIPUAI_API_KEY")
# Path of a file with an API key, whose contents can change. Supercedes
# `api_key` if set.  The main use case is volume-mounted Kubernetes secrets,
# which are updated automatically.
api_key_path: Optional[str] = os.environ.get("ZHIPUAI_API_KEY_PATH")

organization = os.environ.get("ZHIPUAI_ORGANIZATION")
api_base = os.environ.get("ZHIPUAI_API_BASE", "https://wudao.aminer.cn/os/api")
api_version = os.environ.get("ZHIPUAI_API_VERSION", "v2")
api_type = os.environ.get("ZHIPU_API_TYPE", "zhipu_ai")
# api_version = '2022-2-22-preview' if api_type == "azure" else None
verify_ssl_certs = False  # No effect. Certificates are always verified.
proxy = None
app_info = None
enable_telemetry = False  # Ignored; the telemetry feature was removed.
ca_bundle_path = None  # No longer used, feature was removed
debug = False
log = None  # Set to either 'debug' or 'info', controls console logging

__all__ = [
    "APIError",
    "Answer",
    "Classification",
    "Completion",
    "Embedding",
    "Engine",
    "ErrorObject",
    "File",
    "FineTune",
    "InvalidRequestError",
    "Model",
    "zhipuaiError",
    "Search",
    "api_base",
    "api_key",
    "api_type",
    "api_key_path",
    "api_version",
    "app_info",
    "ca_bundle_path",
    "debug",
    "enable_elemetry",
    "log",
    "organization",
    "proxy",
    "verify_ssl_certs",
]
