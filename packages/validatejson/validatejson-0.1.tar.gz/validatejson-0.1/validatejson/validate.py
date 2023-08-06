import json
import jsonschema
import typer
from jsonschema import validate

app = typer.Typer()


def get_schema(schema_location):
    with open(schema_location, 'r') as schema_file:
        schema = json.load(schema_file)
    return schema


def get_data(json_data_location):
    with open(json_data_location, 'r') as data_file:
        schema = json.load(data_file)
    return schema


@app.command()
def validate_json(json_data_location, schema_location):
    json_schema = get_schema(schema_location)
    json_data = get_data(json_data_location)
    try:
        validate(instance=json_data, schema=json_schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        err = "Invalid JSON"
        return False, err

    message = "Valid JSON"
    print(message)


def run_app():
    app()