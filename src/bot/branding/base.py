# src/bot/branding/base.py

from dataclasses import dataclass

@dataclass
class BrandConfig:
    PRODUCT_NAME: str
    BOT_TITLE: str

    PRIMARY_COLOR: str
    ACCENT_COLOR: str

    LABEL_AGENT: str
    LABEL_SECURITY: str
    LABEL_STATUS: str

    EMOJI_AGENT: str
    EMOJI_SECURITY: str
