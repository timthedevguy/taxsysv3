import json
import requests
from time import sleep
from django.conf import settings

BASE_URL = 'https://esi.evetech.net'


def get_markets_region_orders(region_id, **kwargs):
    return _request('/v1/markets/{region_id}/orders/', 'GET', region_id=region_id, success_status_code=200, **kwargs)


def _build_url(url, **kwargs):
    # This method builds the URL using any Query Params present in the kwargs dict

    # Build our query string
    query = ''
    for key, value in kwargs.items():
        key_str = '{' + key + '}'
        if key != 'all' and key != 'success_status_code' and key != 'Etag' and key_str not in url:
            query = str.format('{query}&{key}={value}', query=query, key=key, value=value)

    # Replace default query parameters in the url with ones in kwargs
    url = str.format(url, **kwargs)

    # Build our url
    if query:
        # Remove first &
        query = query[1:]
        url = str.format('{url}?{query}', url=url[:-1], query=query)

    # Return the full URL
    return str.format('{root}{url}', root=BASE_URL, url=url)


def _request(url, method, **kwargs):
    # Get the url
    full_url = _build_url(url, **kwargs)

    # Get our data
    data = ''
    if 'data' in kwargs:
        data = kwargs['data']
        # Check if our data is not a json str yet
        if type(data) is not str:
            data = json.dumps(data)

    # Make the call
    retries = 0
    while retries < 6:
        try:
            response = requests.request(method, full_url, headers=_get_headers(), data=data, timeout=(6, 10))
            break
        except requests.exceptions.Timeout:
            sleep(10)
            retries += 1
    else:
        return False

    if response.status_code == kwargs['success_status_code']:
        # Build result object
        result = {}
        if 'page' in kwargs:
            result['page'] = kwargs['page']
        else:
            result['page'] = 1

        result['pages'] = int(response.headers['x-pages'])
        result['etag'] = response.headers['etag']

        response_data = json.loads(response.text)

        # Check if we should get all results
        if 'all' in kwargs:
            for x in range(result['page'], result['pages']):
                kwargs['page'] = x
                full_url = _build_url(url, **kwargs)

                retries = 0
                while retries < 6:
                    try:
                        response = requests.request(method, full_url, headers=_get_headers(), data=data,
                                                    timeout=(6, 10))
                        break
                    except requests.exceptions.Timeout:
                        sleep(10)
                        retries += 1
                else:
                    return False

                if response.status_code == kwargs['success_status_code']:
                    response_data += json.loads(response.text)
                else:
                    return False

            result['page'] = 1
            result['pages'] = 1

        result['data'] = response_data

        return result
    else:
        return False


def _get_headers(**kwargs):
    headers = {
        'Accept': 'application/json',
        'Content-Type': "application/json",
    }

    if 'Etag' in kwargs:
        headers['If-None-Match'] = kwargs['Etag']

    return headers


def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i + n]
