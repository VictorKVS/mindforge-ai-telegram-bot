import json
from jsonschema import validate, ValidationError
from pathlib import Path

SCHEMA_PATH = Path("contracts/uag/uag_request_schema.json")


class UAGValidationError(Exception):
    pass


def validate_request(payload: dict):
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)

    try:
        validate(instance=payload, schema=schema)
    except ValidationError as e:
        raise UAGValidationError(str(e))
