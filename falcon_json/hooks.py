import json

import falcon
import jsonschema


def process_json_request(request, response, resource, params):
    body = request.stream.read()
    if not body:
        raise falcon.HTTPBadRequest(
            'Empty request body',
            'A valid JSON document is required',
        )

    try:
        request.context['json'] = json.loads(body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        raise falcon.HTTPBadRequest(
            'Malformed JSON',
            'Could not decode the request body. '
            'The JSON was incorrect or not encoded as UTF-8'
        )


def validate_json_schema(schema):
    def wrapper(request, response, resource, params):
        try:
            jsonschema.validate(request.context['json'], schema)
        except jsonschema.exceptions.ValidationError as e:
            raise falcon.HTTPBadRequest(
                'Invalid request body',
                str(e),
            )
    return wrapper
