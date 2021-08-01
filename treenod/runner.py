# -*- coding: utf-8 -*-
import logging
import os
import sys
import argparse
import tempfile
import shutil
import requests
from util import test

logging.basicConfig()
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

for _ in ('boto', 'boto3', 'botocore', 'urllib3'):
    logging.getLogger(_).setLevel(logging.ERROR)


def lambda_handler(event, context):
    results = dict(result='failed')
    filename = event.get('testfile', None)

    if event.get('selenium_hub'):
        os.environ['SELENIUM_HUB'] = event.get('selenium_hub')
    elif os.environ.get('SELENIUM_HUB'):
        del os.environ['SELENIUM_HUB']

    if event.get('browser'):
        os.environ['BROWSER'] = event.get('browser')
    elif os.environ.get('BROWSER'):
        del os.environ['BROWSER']

    if not filename:
        return results

    testfile = tempfile.mktemp(suffix='.py')

    session = requests.session()
    if filename.startswith('file://'):
        from util.requests_adapter import LocalFileAdapter
        session.mount('file://', LocalFileAdapter())

    r = session.get(filename, stream=True)
    if r.status_code == 200:
        with open(testfile, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    LOGGER.info('test %s', filename)

    result = test.unittest(testfile)
    os.unlink(testfile)

    LOGGER.info(result)
    if result.wasSuccessful():
        return dict(result='success')

    if result.failures:
        results['failures'] = result.failures
    if result.errors:
        results['errors'] = result.errors
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='selenium test runner')
    parser.add_argument('--server', type=str, required=False, help='selenium hub url', default=None)
    parser.add_argument('--browser', type=str, required=False, help='browser name', default=None)
    parser.add_argument('testfile', type=str, help='testfile')
    args = parser.parse_args()

    if not os.path.isfile(args.testfile):
        sys.exit(1)
    event = {'testfile': 'file://' + os.path.abspath(args.testfile).replace('\\', '/')}

    if args.server:
        event['selenium_hub'] = args.server

    if args.browser:
        event['browser'] = args.browser

    LOGGER.info('selenium test %s', args.testfile)
    print(lambda_handler(event, None))

