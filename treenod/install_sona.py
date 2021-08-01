# -*- coding: utf-8 -*-
import logging
import time
import re
import sys
import requests
import os.path
from base import BaseTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common import exceptions
from util import setup_sona as setup
from util import slack


LOGGER = logging.getLogger()
BASE_URL = 'https://gadmin.treenod.com/'

ID = ''
PW = ''
PATH = ''

class DownloadFile(BaseTestCase):

    def open_url(self, url):
        result = self.selenium.open_url(url)
        time.sleep(3)
        self.assertTrue(result, msg='URL ({}) open failed'.format(url))
        LOGGER.info("Current check page -> {}".format(self.driver.current_url))


    def login(self, url):
        self.open_url(url)
        time.sleep(5)

        #signin click
        self.selenium.wait('xpath', '//*[@id="my-signin2"]/div').click()
        time.sleep(5)

        self.driver.switch_to.window(self.driver.window_handles[1])

        #input id
        self.selenium.wait('xpath', '//*[@id="identifierId"]').send_keys(ID)
        time.sleep(3)

        #next
        self.selenium.wait('xpath', '//*[@id="identifierNext"]').click()
        time.sleep(10)
        
        #input password
        self.selenium.wait('css_selector', '#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input').send_keys(PW)
        time.sleep(3)
        
        #next
        self.selenium.wait('xpath', '//*[@id="passwordNext"]').click()
        time.sleep(5)

        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(10)


    def download(self, div):
        build = self.selenium.wait('css_selector', 'tbody > tr > td:nth-child(1)').text
        version = self.selenium.wait('css_selector', 'tbody > tr > td:nth-child(2) > a').text.rstrip('cloud_download')

        #기본 다운로드 경로 + 최신 apk명
        file_name = build + '_' + version + div +'.apk'
        app = os.path.join(PATH, file_name)
        print(app)
        
        if os.path.isfile(app): #최신파일 이미 보유
            LOGGER.info("Latest file already have")
            return None
        else: #최신파일 미보유
            self.slack(self.driver.current_url) #slack 알림
            apk = self.selenium.wait('css_selector', 'tbody > tr > td:nth-child(2) > a')
            apk.click() #download
            time.sleep(60) #추후 다운로드 완료시까지 대기하는 코드로..변경하면 좋겠다.
            LOGGER.info('Download complete.')
            return file_name

    
    def install(self, f):
        setup.TableSearchTest.test_setUp(self, PATH, f)

    
    def div_blossom(self):
        #select division list
        division = self.selenium.wait('xpath', '//*[@id="searchForm"]/div/div[1]/div/input')
        division.click()
        time.sleep(5)

        #select dev
        dev = self.selenium.wait('css_selector', '.select-wrapper > ul > li', find_multiple=True)
        dev[1].click() #1 == dev, 2 == QA
        time.sleep(3)


    def div_pokopoko(self):
        #select division list
        division = self.selenium.wait('xpath', '//*[@id="searchForm"]/div/div[1]/div/input')
        division.click()
        time.sleep(5)

        #select dev
        dev = self.selenium.wait('css_selector', '.select-wrapper > ul > li', find_multiple=True)
        dev[5].click() #5 == qa
        time.sleep(3)


    def div_blast(self):
        #select division list
        division = self.selenium.wait('xpath', '//*[@id="searchForm"]/div/div[1]/div/input')
        division.click()
        time.sleep(5)

        #select dev
        dev = self.selenium.wait('css_selector', '.select-wrapper > ul > li', find_multiple=True)
        dev[8].click() #5 == qa
        time.sleep(3)

#----------------------------------------------------------------

    #coin blossom_dev
    def test_blossom(self):
        url = BASE_URL + 'TAPCOING/appBuild'
        self.login(url)
        f = self.download('_dev')
        if f:
            self.install(f) #설치

    #pokopoko_alpha
    def no_test_pokopoko(self):
        url = BASE_URL + 'PKPKGLOBAL/appbuild'
        self.login(url)
        self.div_pokopoko()
        self.download('_alpha')


    #pokopang tap blast_alpha
    def no_test_blast(self):
        url = BASE_URL + 'PKPTGLOBAL/appbuild'
        self.login(url)
        self.div_blast()
        self.download('_alpha')
       
    def slack(self, url):
        WEBHOOK_URL= 'https://hooks.slack.com/services/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'
        text = "New build release: " + url
        slack.Slack.notify(WEBHOOK_URL, text=text)

        #text = 'Test'
        #update_check.Slack.notify(Config.SLACK.SONA.WEBHOOK_URL, text=text)
