import requests
from time import sleep


class ESI(object):
    BASE_URL = 'https://esi.evetech.net'

    @staticmethod
    def get_market_region_orders(region, page=1, etag=None):

        headers = None
        failures = 0

        if etag is not None:
            headers = {'If-None-Match': etag}

        while failures < 5:
            r = requests.get(ESI.BASE_URL + '/v1/markets/{region}/orders/?page={page}'.format(region=region, page=page),
                             headers=headers)

            if r.status_code == 200:
                return r.json(), int(r.headers['X-Pages']), r.headers['Etag']
            else:
                failures += 1
                sleep(10)

        return None


def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i + n]
