from base import BaseTestCase
import logging
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
LOGGER = logging.getLogger(__name__)
#********************************************2020.07.24********************************************
# 1. check_scroll 코드 수정 ( IE 등의 다른 브라우저에서도 동작하도록 수정 )
#**************************************************************************************************
class Test_pokothon_com(BaseTestCase):
    def check_scroll(self, page):
        self.selenium.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        #scroll_result = self.selenium.driver.execute_script("return window.scrollY")   <- IE에서는 이 코드가 작동하지 않음.
        scroll_result=self.selenium.driver.execute_script("return document.querySelector('html').scrollTop")
        
        if scroll_result > 0:
            LOGGER.info("_" + page + " 페이지 스크롤 테스트 완료. Y축의 값 : " + str(scroll_result))
        elif scroll_result <= 0:
            result = None
            self.assertIsNone(result,msg="_"+page+" 페이지의 스크롤이 움직이지 않았습니다!!!")

    def check_video(self, page):                
        if page in ["2019", "2018", "2017", "2015", "2014"]:
            video_element = self.selenium.wait('css_selector','body > div:nth-child(3) > div > video')
            self.assertIsNotNone(video_element, msg= page + " 에서 동영상을 찾지 못했습니다!!!")
            LOGGER.info("_" + page + " 페이지 동영상 로드 확인")

    def check_url(self, page):
        common_url = 'https://pokothon.treenod.com/'
        page_name = ['pokothon', '2019', '2018', '2017', '2015', '2014']
        for i in range(0,6):
            if page_name[i] == page :
                self.selenium.wait('css_selector','body > header > div.w3-bar.w3-light-grey.w3-round.w3-display-bottommiddle.w3-hide-small.w3-hide-medium.w3-padding-medium.w3-card > a:nth-child({0})'.format(i+1)).click()
                full_url = common_url + page
                url = self.selenium.driver.current_url
                
                if full_url != url:
                    result = None
                    self.assertIsNone(result,msg = "_"+page+" 페이지 접속 실패!!!!!!")
                else:
                    LOGGER.info("_" + page + ' 페이지 접속 성공')

    def check_text(self, page) : #<!--- 2020.06.22 을 기준으로 텍스트 내용을 복사하였음 ---!>
        text_pokothon_page ='포코톤은 POKO IP를 통해 24시간 동안 컨'
        text_2017_page = '요리포코 조'
        page_text = [self.selenium.get_text('xpath', '/html/body')]
        
        if page == 'pokothon':
            if text_pokothon_page not in str(page_text):
                result = None
                self.assertIsNone(result,msg="_"+page+" 페이지 텍스트 검증 실패!!!!")
            else:
                LOGGER.info('_'+page+' 페이지 텍스트 검증 완료\n')

        if page == '2017' :
            if text_2017_page not in str(page_text):
                result = None
                self.assertIsNone("_"+page+" 페이지 텍스트 검증 실패!!!")
            else:
                LOGGER.info('_'+page+' 페이지 텍스트 검증 완료\n')

    
    def check_apk(self):
        LOGGER.info("_________2017 페이지의 apk 파일 체크 시작_________")
        apk_count = 0
        for link in self.selenium.wait('xpath', '//div[@class="card h-100"]/a', find_multiple=True):
            apk_url = link.get_attribute('href')
            status_code = requests.get(apk_url).status_code
            apk_count += 1
            if status_code == 200:
                self.assertTrue(status_code == 200, msg='_2017 페이지 APK 확인 실패')
        
        if apk_count == 11:
            LOGGER.info("_2017 페이지의 APK 확인 완료")

    def image_check(self, page):
        el = self.selenium.driver.execute_script('return document.images.length')
        count = 0

        for i in range(0, int(el)):
            count += 1

        if count == 0:
            LOGGER.warning('_'+page+'페이지에서 이미지를 찾을 수 없습니다.')

        elif count > 0:
            LOGGER.info('_'+page+' 페이지의 이미지 개수 : '+str(count)+'개')


#----------------------------- 테스트 시작 -----------------------------
    def test_OpenUrl(self): #TC0 : 포코톤 메인으로 이동
        url = 'https://pokothon.treenod.com/'
        result = self.selenium.open_url(url)
        self.assertTrue(result, msg='{0} 접속 실패'.format(url))
        LOGGER.info('{0} 접속 성공'.format(url))


    def test_POKOTHON_COM(self): #TC001 ~ TC004
        page = "POKOTHON_COM"

        #TC1 : POKOTHON.COM 스크롤 테스트
        self.check_scroll(page)
   
        #TC2 : POKOTHON.COM 이미지 검증
        self.image_check(page)


    def test_POKOTHON_PAGE(self): #TC005 ~ TC009
        page = 'pokothon'
        
        #TC3 : POKOTHON 페이지 이동
        self.check_url(page)
        
        #TC4 : POKOTHON 페이지 스크롤 테스트
        self.check_scroll(page)

        #TC5 : POKOTHON 페이지 이미지 검증
        self.image_check(page)
        
        #TC6 : POKOTHON 페이지 텍스트 검증
        self.check_text(page)


    def test_2019(self): #TC010 ~ TC014
        page = "2019"

        #TC7 : 2019 페이지로 이동
        self.check_url(page)

        #TC8 : 2019 페이지 스크롤 테스트
        self.check_scroll(page)
        
        #TC9 : 2019 페이지 동영상 검증
        self.check_video(page)
        
        #TC10 : 2019 페이지 이미지 검증
        self.image_check(page)


    def test_2018(self): #TC015 ~ TC019
        page = "2018"

        #TC11 : 2018 페이지로 이동
        self.check_url(page)

        #TC12 : 2018 페이지 스크롤 테스트
        self.check_scroll(page)

        #TC13 : 2018 페이지 동영상 검증
        self.check_video(page)

        #TC14 : 2018 페이지 이미지 검증
        self.image_check(page)


    def test_2017(self): #TC020 ~ TC025
        page = "2017"

        #TC15 : 2017 페이지로 이동
        self.check_url(page)

        #TC16 : 2017 페이지 스크롤 테스트
        self.check_scroll(page)
    
        #TC17 : 2017 페이지 동영상 검증
        self.check_video(page)

        #TC18 : 2017 페이지 이미지 검증
        self.image_check(page)
    
        #TC19 : 2017 페이지의 apk 파일을 다운로드
        self.check_apk()

        #TC20 : 2017 페이지 텍스트 검증
        self.check_text(page)


    def test_2015(self): #TC026 ~ TC030
        page = "2015"

        #TC21 : 2015 페이지 이동
        self.check_url(page)

        #TC22 : 2015 페이지 스크롤 테스트
        self.check_scroll(page)
    
        #TC23 : 2015 페이지 동영상 검증
        self.check_video(page)

        #TC24 : 2015 페이지 이미지 검증
        self.image_check(page)


    def test_2014(self): #TC031 ~ TC035
        page = "2014"
        
        #TC25 : 2014 페이지 이동
        self.check_url(page)

        #TC26 : 2014 페이지 스크롤 테스트
        self.check_scroll(page)

        #TC27 : 2014 페이지 동영상 검증
        self.check_video(page)

        #TC28 : 2014 페이지 이미지 검증
        self.image_check(page)