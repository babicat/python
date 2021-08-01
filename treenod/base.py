# -*- coding: utf-8 -*-
import unittest
import logging
import os
import sys
import shutil
import tempfile
from selenium import webdriver
from util.selenium import Selenium
from util.driver import chromedriver

LOGGER =logging.getLogger(__name__)


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.environ.get('AWS_EXECUTION_ENV'):
            os.environ['HOME'] = os.getcwd()
        os.environ['TZ'] = 'Asia/Seoul'

        bin_path = os.path.join(os.getcwd(), 'bin')
        cls.temp_path = tempfile.mkdtemp()

        if os.environ.get('SELENIUM_HUB'):
            cls._selenium = Selenium(host=os.environ['SELENIUM_HUB'], browser=os.environ.get('BROWSER', None))
        else:
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-application-cache')
            options.add_argument('--start-maximized')
            options.add_argument('--lang=ko')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-extensions')
            options.add_argument('--homedir={0}'.format(cls.temp_path))
            options.add_argument('--user-data-dir={0}'.format(os.path.join(cls.temp_path, 'user-data')))
            options.add_argument('--data-path={0}'.format(os.path.join(cls.temp_path, 'data-path')))
            options.add_argument('--disk-cache-dir={0}'.format(os.path.join(cls.temp_path, 'cache-dir')))

            if os.environ.get('AWS_EXECUTION_ENV'):
                options.binary_location = os.path.join(bin_path, 'headless-shell')
                options.add_argument('--single-process')
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                options.add_argument('--no-sandbox')
                options.add_argument('--no-zygote')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-impl-side-painting')
                options.add_argument('--disable-gpu-sandbox')
                options.add_argument('--disable-accelerated-2d-canvas')
                options.add_argument('--disable-accelerated-jpeg-decoding')
            elif os.environ.get('APP_ENV') in ['production']:
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')

            driver = webdriver.Chrome(chromedriver(), chrome_options=options)

            cls._selenium = Selenium(driver=driver)
        cls._selenium.driver.delete_all_cookies()

        if cls is not BaseTestCase and cls.setUp is not BaseTestCase.setUp:
            origin_setUp = cls.setUp
            def setUpOverride(self, *args, **kwargs):
                BaseTestCase.setUp(self)
                return origin_setUp(self, *args, **kwargs)
            cls.setUp = setUpOverride


    @classmethod
    def tearDownClass(cls):
        if cls._selenium.driver:
            cls._selenium.close()

        shutil.rmtree(cls.temp_path, ignore_errors=True)


    def setUp(self):
        self.selenium = self.__class__._selenium
        self.driver = self.__class__._selenium.driver
        self.vars = {}
