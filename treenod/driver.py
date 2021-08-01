# -*- coding: utf-8 -*-
import logging
import os
import sys
import stat
import re
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
from . import command

LOGGER =logging.getLogger(__name__)
OS = {'linux64': 'linux', 'mac64': 'darwin', 'win32': 'win'}


def chromedriver():
    driver = 'chromedriver'
    bin_path = os.path.join(os.getcwd(), 'bin')
    if os.environ.get('AWS_EXECUTION_ENV'):
        return os.path.join(bin_path, driver)
    os_prefix = next((k for k in OS.keys() if sys.platform.lower().find(OS[k].lower()) != -1), '')
    file_ext = '.exe' if sys.platform.lower() in 'win' else ''

    try:
        if os_prefix == 'win32':
            r, o, e = command.run(['reg', 'query', 'HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon', '/v', 'version'])
            matched = re.findall(r'.* ([0-9]+)\.[0-9]+.*', o)
            chrome_major_version = matched[0]
        else:
            if os_prefix == 'mac64':
                r, o, e = command.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'])
            else:
                r, o, e = command.run('google-chrome --version')
            matched = re.match(r'.* ([0-9]+)\.[0-9]+.*', o)
            chrome_major_version = matched.groups()[0]
    except FileNotFoundError:
        LOGGER.error('Google Chrome required')
        sys.exit(-1)
    except Exception as e:
        LOGGER.warning(e)
        return os.path.join(bin_path, driver)

    chrome_driver_version = urlopen('https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{}'.format(chrome_major_version)).read().decode('utf-8')
    driver += '-{0}-{1}{2}'.format(os_prefix, chrome_driver_version, file_ext)

    chrome_bin = os.path.join(bin_path, driver)
    # chromedriver 가 없을 경우 다운로드
    if not os.path.isfile(chrome_bin):
        with urlopen('https://chromedriver.storage.googleapis.com/{0}/chromedriver_{1}.zip'.format(chrome_driver_version, os_prefix)) as zipresp:
            with ZipFile(BytesIO(zipresp.read())) as zipdata:
                zipinfo = zipdata.infolist()[0]
                zipinfo.filename = os.path.join('bin', driver)
                zipdata.extract(zipinfo)
        st = os.stat(chrome_bin)
        os.chmod(chrome_bin, st.st_mode | stat.S_IEXEC)
    return chrome_bin
