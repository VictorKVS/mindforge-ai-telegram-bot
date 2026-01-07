# src/bot/branding/__init__.py

from src.bot.config import settings
from importlib import import_module

_brand = import_module(f"src.bot.branding.{settings.BRAND_PROFILE}")
BRAND = _brand.BRAND
