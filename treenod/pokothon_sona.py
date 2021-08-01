import logging
import time
import re
import requests
from base import BaseTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common import exceptions

LOGGER = logging.getLogger()
BASE_URL = 'https://pokothon.treenod.com/'

class TestPokothoncom(BaseTestCase):

    def open_url(self, url):
        result = self.selenium.open_url(url)
        self.assertTrue(result, msg='URL {} open failed'.format(url))
        time.sleep(3)
        LOGGER.info("Current check page -> {}".format(self.driver.current_url))


    #video load
    def is_video_loaded(self):
        time.sleep(5)
        length = self.driver.execute_script('return document.getElementsByTagName("video").length')

        if length:
            count = 0

            for i in range(0, length):
                self.driver.implicitly_wait(10)
                result = self.driver.execute_script('return document.getElementsByTagName("video")['+ str(i) +'].readyState;')
                if result == 4:
                    pass
                else:
                    try:
                        self.driver.implicitly_wait(10)
                        result = self.driver.execute_script('return document.getElementsByTagName("video")['+ str(i) +'].readyState;')
                        if result == 4:
                            pass
                    except:
                        count += 1
                        break

            return (count == 0)

        return True


    #main img slide
    def slideshow(self):
        img = self.selenium.wait('css_selector', '.slideshow-container img', find_multiple=True)
        slide = []

        for i in range(len(img)):
            for j in img:
                slide.append(j.value_of_css_property('display'))
            #duration:300ms
            time.sleep(4)

        return slide.count('block') == len(img)


    #2017 apk download
    def check_download(self):
        apk = self.selenium.wait('css_selector', '.container  a', find_multiple=True)
        result = 0

        for i in apk:
            r = requests.get(i.get_attribute('href'))
            if r.status_code == 200:
                result += 1

        return len(apk) == result


    #link click & check url
    def check_link(self, element):
        if (element == None):
            return None

        url = element.get_attribute('href')

        try:
            element.click()
        except:
            LOGGER.warning('Element is not clickable.')

        current_url = self.go_previous_page()

        time.sleep(3)
        return (url == current_url)


    def go_previous_page(self):
        current_url = self.driver.current_url
        time.sleep(5)

        referrer = self.driver.execute_script('return document.referrer;')

        if (referrer == current_url) or (referrer == None):
            pass
        else :
            self.driver.execute_script('history.go(-1);')
            time.sleep(5)

        return current_url


    #Click header menu
    def check_link_header(self):
        header = self.selenium.wait('css_selector', '.w3-display-container a', find_multiple=True)

        for i in range(len(header)):
            header = self.selenium.wait('css_selector', '.w3-display-container a', find_multiple=True)
            self.assertTrue(self.check_link(header[i]), msg='Url not match')

        return True


    #Scroll
    def page_scroll(self):
        #페이지 전체 높이 구하기
        total_height = self.driver.execute_script("return document.body.scrollHeight;")
        #스크롤 길이 구하기
        scroll_height = self.driver.execute_script("return window.innerHeight;")

        if (scroll_height + 100) > total_height:
            LOGGER.info("Scroll not required")
        else:
            count = 0
            for i in range(100):
                #500px 스크롤 다운
                self.driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(1)
                current = self.driver.execute_script("return window.pageYOffset;")

                if (current + scroll_height) >= total_height:
                    #페이지 최상단으로 이동
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    count = i + 1
                    break
            LOGGER.info("{} time(s) scroll.".format(count))

        return True

#------------------------------------ func 실행 결과 검증 --------------------------------------

    #image check
    def image(self):
        image_check = self.selenium.is_image_loaded()
        self.assertTrue(image_check, msg="image check: FAIL")
        LOGGER.info('Image check: PASS')

    #video check
    def video(self):
        video_check = self.is_video_loaded()
        self.assertTrue(video_check, msg="video check: FAIL")
        LOGGER.info('Video check: PASS')

    #img slide
    def slide(self):
        slide = self.slideshow()
        self.assertTrue(slide, msg='Image slide check: FAIL')
        LOGGER.info('Image slide check: PASS')

    #apk download
    def download(self):
        apk = self.check_download()
        self.assertTrue(apk, msg='APK download check: FAIL')
        LOGGER.info('APK download check: PASS')

    #header link
    def header_link(self):
        header = self.check_link_header()
        self.assertTrue(header, msg='Header link check: FAIL')
        LOGGER.info('Header link check: PASS')

    def scroll(self):
        scroll = self.page_scroll()
        self.assertTrue(scroll, msg='scroll check: FAIL')
        LOGGER.info('scroll check: PASS')


#-------------------------------- 페이지 별 func 실행 ---------------------------------------

    def test_main(self):
        self.open_url(BASE_URL)

        func_list = [self.image(), self.video(), self.slide() ,self.header_link(), self.scroll()]
        

    def no_test_prologue(self):
        self.open_url(BASE_URL + 'pokothon')

        func_list = [self.image(), self.header_link(), self.scroll()]


    def no_test_2019(self):
        self.open_url(BASE_URL + '2019')

        func_list = [self.image(), self.video(), self.header_link(), self.scroll()]


    def no_test_2018(self):
        self.open_url(BASE_URL + '2018')

        func_list = [self.image(), self.video(), self.header_link(), self.scroll()]


    def no_test_2017(self):
        self.open_url(BASE_URL + '2017')

        func_list = [self.image(), self.video(), self.header_link(), self.scroll(), self.download()]

    
    def no_test_2015(self):
        self.open_url(BASE_URL + '2015')

        func_list = [self.image(), self.video(), self.header_link(), self.scroll()]

    
    def no_test_2014(self):
        self.open_url(BASE_URL + '2014')

        func_list = [self.image(), self.video(), self.header_link(), self.scroll()]


