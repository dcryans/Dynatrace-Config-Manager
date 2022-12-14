import requests
import json
from urllib.parse import urlencode
from exception import TokenNotAuthorized, SettingsValidationError


# Methods
method_get = "GET"
method_put = "PUT"
method_post = "POST"
method_delete = "DELETE"

# Settings v2
settings_schemas = 'api/v2/settings/schemas'
settings_objects = 'api/v2/settings/objects'

entities = 'api/v2/entities'
entity_types = 'api/v2/entityTypes'

# Map of required API Token scopes
api_token_map = {
    settings_schemas: {
        "prefix": "settings."
    },
    settings_objects: {
        "prefix": "settings."
    },
    entities: {
        "prefix": "entities."
    },
    entity_types: {
        "prefix": "entities."
    },
}

method_token_map = {
    method_get: "read",
    method_put: "write",
    method_post: "write",
    method_delete: "write",

}

def get(config, api, url_trail, query_dict={}):

    method = method_get

    url_trail = _append_query_string(url_trail, query_dict)
    call_url = config['url'] + api + url_trail

    response = requests.request(
        method, call_url, headers=config['headers'], verify=config['verifySSL'], proxies=config['proxies'])
    _handle_response(response, method, api)

    return response


def delete(config, api, url_trail):
    method = method_delete

    call_url = config['url'] + api + url_trail

    response = requests.request(
        method, call_url, headers=config['headers'], verify=config['verifySSL'], proxies=config['proxies'])
    _handle_response(response, method, api)

    return response


def post(config, api, url_trail, payload):
    return _call_method(method_post, config, api, url_trail, payload)


def put(config, api, url_trail, payload):
    return _call_method(method_put, config, api, url_trail, payload)


def _call_method(method, config, api, url_trail, payload):

    call_url = config['url'] + api + url_trail

    response = requests.request(
        method, call_url, headers=config['headers'], data=payload, verify=config['verifySSL'], proxies=config['proxies'])
    _handle_response(response, method, api)

    return response


def _handle_response(response, method, api):

    if (response.status_code >= 400):
        print("Error", response.status_code, ": ", response.text)

    if (response.status_code == 401):
        requiredTokenScope = api_token_map[api]["prefix"]
        requiredTokenScope += method_token_map[method]
        raise TokenNotAuthorized(
            "Token not authorized for required scope: " + requiredTokenScope)
    elif (response.status_code == 404):
        pass
    elif (response.status_code == 400):
        raise SettingsValidationError(
            "Settings 2.0 Validation error: ", response.text)
    elif (response.status_code == 403):
        raise SettingsValidationError(
            "Token missing the required scope for Settings 2.0 object: ", response.text)
    else:
        response.raise_for_status()


def _append_query_string(url_trail, query_dict):

    if (len(query_dict) > 0):
        url_trail += '?'
        url_trail += urlencode(query_dict)

    return url_trail


def get_json(config, api, url_trail, query_dict={}):

    response = get(config, api, url_trail, query_dict)
    result = response.text

    try:
        response_object = json.loads(result)
    except json.JSONDecodeError as err:
        print("Call Result is an invalid JSON: ",
              "\n", err)
        print("Response: ", response,
            "\n", "Response Headers: ", response.headers,
            "\n", "Response Content: ", response.content)
        raise err

    return response_object


def post_json(config, api, url_trail, payload):

    response = post(config, api, url_trail, payload)
    response_object = json.loads(response.text)

    return response_object
