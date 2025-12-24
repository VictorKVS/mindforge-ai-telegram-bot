import os
import warnings
from functools import reduce
from glob import iglob
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Optional

from ...exceptions import SettingsError
from ...utils import path_type_label
from ..base import PydanticBaseSettingsSource
from ..utils import parse_env_vars
from .env import EnvSettingsSource
from .secrets import SecretsSettingsSource

if TYPE_CHECKING:
    from ...main import BaseSettings
    from ...sources import PathType


SECRETS_DIR_MAX_SIZE = 16 * 2**20  # 16 MiB seems to be a reasonable default


class NestedSecretsSettingsSource(EnvSettingsSource):
    def __init__(
        self,
        file_secret_settings: PydanticBaseSettingsSource | SecretsSettingsSource,
        secrets_dir: Optional['PathType'] = None,
        secrets_dir_missing: Literal['ok', 'warn', 'error'] | None = None,
        secrets_dir_max_size: int | None = None,
        secrets_case_sensitive: bool | None = None,
        secrets_prefix: str | None = None,
        secrets_nested_delimiter: str | None = None,
        secrets_nested_subdir: bool | None = None,
        # args for compatibility with 