# Falcon JSON
Small set of JSON utilities for Python Falcon framework.

Falcon doesn't currently provide JSON deserialization and most of the 
time you need one.  

Example code:

    import falcon

    schema = {
        'type': 'object',
        'required': ['first_name', 'last_name'],
        'properties': {
            'first_name': {
                'type' : 'string',
            },
            'last_name': {
                'type' : 'string',
            },
        },
    }


    class People(object):
    
        @falcon.before(hooks.process_json_request)
        @falcon.before(hooks.validate_json_schema(schema))
        def on_post(self, request, response):
            # Validated JSON request body goes here:
            data = resp.context['json']
