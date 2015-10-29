import json
import unittest

import falcon
from falcon import testing
import mock
import pytest

from falcon_json import hooks


class DummyResource(object):

    def __init__(self):
        self.received = None

    @falcon.before(hooks.process_json_request)
    def on_post(self, request, response):
        self.received = request.context['json']


class TestHooksProcessJsonRequest(unittest.TestCase):

    def setUp(self):
        super(TestHooksProcessJsonRequest, self).setUp()
        self.app = falcon.API()
        self.resource = DummyResource()
        self.app.add_route('/dummy_route', self.resource)
        self.response_mock = falcon.testing.StartResponseMock()

    def test_loads_request_body_into_request_context(self):
        self._simulate_request(
            '/dummy_route', method='POST', body='[{"foo": "bar"}]')
        assert self.resource.received == [{'foo': 'bar'}]

    def test_raises_400_error_on_empty_body_request(self):
        response = self._simulate_request(
            '/dummy_route', method='POST', body='')
        self._assert_404_response(response, 'Empty request body')

    def test_raises_400_error_on_incorrect_json_structure(self):
        response = self._simulate_request(
            '/dummy_route', method='POST', body='{"foo": "bar')
        self._assert_404_response(response, 'Malformed JSON')

    def _simulate_request(self, path, *args, **kwargs):
        env = falcon.testing.create_environ(path=path, **kwargs)
        return self.app(env, self.response_mock)

    def _assert_404_response(self, response, error_title):
        assert self.resource.received is None
        assert self.response_mock.status == '400 Bad Request'
        assert json.loads(response[0].decode('utf-8'))['title'] == error_title


class TestHooksValidateJsonSchema(object):

    schema = {
        'type': 'object',
        'required': ['first_name'],
        'properties': {
            'first_name': {
                'type' : 'string',
            },
        },
    }

    def test_ok(self):
        request = mock.Mock(context={'json': {"first_name": "John"}})
        hooks.validate_json_schema(self.schema)(request, None, None, None)

    def test_raises_404_error_on_invalid_schema(self):
        request = mock.Mock(context={'json': {"name": "John"}})
        with pytest.raises(falcon.HTTPBadRequest):
            hooks.validate_json_schema(self.schema)(request, None, None, None)
