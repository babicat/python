from base import BaseTestCase
import logging
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
LOGGER = logging.getLogger(__name__)

class Test_video_check(BaseTestCase):
    def test_OpenUrl(self): 
        url = 'https://pokothon.treenod.com/2019'
        result = self.selenium.open_url(url)
        self.assertTrue(result, msg='{0} 접속 실패'.format(url))
        LOGGER.info('{0} 접속 성공'.format(url))

        self.HTML5_video_check()
        
        url = 'https://youtu.be/1L0l5CzFs-4'
        result = self.selenium.open_url(url)
        time.sleep(5)
    
    def HTML5_video_check(self):
         time.sleep(5)
         video_element = self.selenium.wait('css_selector','body > div:nth-child(3) > div > video')
         video_element.click()
         self.assertIsNotNone(video_element, "동영상을 찾지 못했습니다!!!")
         LOGGER.info("페이지 동영상 로드 확인")
         time.sleep(5)

    def Youtube_video_check(self):
         el = self.selenium.driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[26]/div[2]/div[1]/button")
         self.selenium.driver.switch_to.frame(0)
         time.sleep(5)
         el.send_keys(Keys.RETURN)
         time.sleep(5)