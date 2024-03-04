import csv

import urllib.parse
import urllib.request

from os import getenv

ENTRYPOINT = getenv('ENDPOINT')  # https://event-www-dev-01.kidsnote.com/v1/coupang/post-back
HTTP_PROXY = getenv('HTTP_PROXY')  # http://proxy.onkakao.net:3128
HTTPS_PROXY = getenv('HTTP_PROXY', HTTP_PROXY)


def listen(contents):
    for row in csv.reader(contents.splitlines()):
        print(row)

        timestamp, auth_key, post_body, *etc = row

        req = urllib.request.Request(
            ENTRYPOINT,
            data=post_body.encode(),
            headers={
                'Content-Type': 'application/json'
            },
        )
        req.set_proxy(HTTP_PROXY, 'http')
        req.set_proxy(HTTP_PROXY, 'https')

        with urllib.request.urlopen(req, timeout=10) as response:
            result = response.read()
            print(result.decode())
