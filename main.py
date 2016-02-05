#!/usr/bin/env python 

from datetime import datetime
import json
import time
import random
import socket
import urllib2



URLS = [
    'http://ss-aws-fr.spindelanalytics.com/index.html',
    'http://ss-gcs-eu.spindelanalytics.com/index.html',
    'http://ss-gcs-us.spindelanalytics.com/index.html',
    'http://ss-gcs-cl.spindelanalytics.com/index.html',
    'http://ss-gae-cf.spindelanalytics.com/index.html',
    'http://ss-aws-cf.spindelanalytics.com/index.html',
    'http://ss-aws-au.spindelanalytics.com/index.html',
    'http://ss-aws-eu.spindelanalytics.com/index.html',
    'http://ss-aws-us.spindelanalytics.com/index.html',
    'http://ss-gae-eu.spindelanalytics.com/index.html',
    'http://ss-gae-us.spindelanalytics.com/index.html',
    'http://ss-ghp-gh.spindelanalytics.com/index.html',
]

HEADERS = {
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
}


def speed_test(url):
    status_code = None
    ttfb = None
    ttlb = None
    exception = None
    headers = None


    try:
        opener = urllib2.build_opener()
        request = urllib2.Request(url, headers=HEADERS)

        now = datetime.utcnow().isoformat()
        start = time.time()
        response = opener.open(request, timeout=60)

        response.read(1)  # Read one byte
        ttfb = time.time() - start

        response.read()
        ttlb = time.time() - start

        status_code  = response.code

        headers = json.dumps(dict(response.info()))
    except urllib2.HTTPError as e:
        exception = e
        status_code = e.code
    except Exception as e:
        exception = e
    finally:
        data = (now, socket.gethostname(), url, status_code, ttfb, ttlb, exception, headers)

    with open('results.txt', 'a') as outfile:
        outfile.write('|'.join(str(x) for x in data) + '\n') 


def shuffled(x):
    temp = list(x)
    random.shuffle(temp)
    return temp



if __name__ == '__main__':
    while True:
        for url in shuffled(URLS):
            speed_test(url)
            time.sleep(10)
