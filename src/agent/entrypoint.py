"""Secrets file settings source."""

from __future__ import annotations as _annotations

import os
import warnings
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
)

from pydantic.fields import FieldInfo

from pydantic_settings.utils import path_type_label

from ...exceptions import SettingsError
from ..base import PydanticBaseEnvSettingsSource
from ..types import PathType

if TYPE_CHECKING:
    from pydantic_settings.main import BaseSettings


class SecretsSettingsSource(PydanticBaseEnvSettingsSource):
    """
    Source class for loading settings values from secret files.
    """

    def __init__(
        self,
        settings_cls: type[BaseSettings],
        secrets_dir: PathType | None = None,
        case_sensitive: bool | None = None,
        env_prefix: str | None = None,
        env_ignore_empty: bool | None = None,
        env_parse_none_str: str | None = None,
        env_