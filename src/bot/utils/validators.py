def is_valid_input(text: str) -> bool:
    """
    Basic validator to satisfy unit tests.
    """
    return isinstance(text, str) and len(text.strip()) > 0
