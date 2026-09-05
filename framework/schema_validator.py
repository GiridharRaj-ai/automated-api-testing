import json

from jsonschema import validate


def validate_json_schema(response_data, schema_file):
    with open(schema_file, "r") as file:
        schema = json.load(file)

    validate(
        instance=response_data,
        schema=schema
    )