'''
Android Native Script
'''
import unittest
import os
import cv2
import numpy as np
import time, datetime
from appium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

#*******************************2020.12.04 변경사항**********************************
# 1. 테스트 단계 추가 (앱 설치 ~ 상점(클로버~다이아) 진입)
# 2. 단계 추가에 따른 이미지 작업
# 3. 스테이지 입장을 후 순위로 조정
# 4. 기간 한정 이벤트(야채 스테이지 등) 출입을 판별하는 코드 작성중 (try 문으로 시도중)
#***********************************************************************************

class TS():
    def makeTS(self):
        return str(int(datetime.datetime.now().timestamp())) 

class pkpkg_login_test(unittest.TestCase):
    
    def check_cv(self,FILE_NAME):
        ts = TS()
        driver = self.driver
        directory = '%s/' % os.getcwd()
        screenshot = '%s-screenshot.png' % ts.makeTS()
        detectshot = '%s-detect.png' % ts.makeTS()

        driver.save_screenshot(directory + screenshot)

        driver.save_screenshot(directory + screenshot)
        sourceimage = cv2.imread(screenshot, 0)
        template = cv2.imread('searchimages\\'+FILE_NAME+'.png', 0)
        w, h = template.shape[::-1]
        method = eval('cv2.TM_CCOEFF')
        res = cv2.matchTemplate(sourceimage, template, method)
        
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        center = (top_left[0] + int(w/2), top_left[1] + int(h/2))

        color = (0, 0, 255)

        cv2.rectangle(sourceimage, top_left, bottom_right, color, thickness=8)
        cv2.imwrite(detectshot, sourceimage)

        driver.tap([center])

    def setUp(self):
        
        # POKOPOKO 경로
        app = os.path.join(os.path.dirname(__file__), 'C:\\appium_test\\pkpkg', '7_1.13.0_alpha.apk')
        app = os.path.abspath(app)

        # Set up appium
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities={
                'app': app,
                'platformName': 'Android',
                'platformVersion': '9.0',
                'deviceName': 'Pixel_2_xl',
                'automationName': 'Appium',
                'appPackage': 'com.nhnent.SKPOKOPOKO',
                'appActivity': 'seoul.treenod.com.launchscreen.LaunchScreenActivity',
                'udid': '712KPYR1019450'
            })

        # ---------테스트 시작 지점---------
    def test_search_field(self):
        
        # ----------앱 실행 후 권한 허용 안내 팝업의 OK 버튼 터치----------
        driver = self.driver
        wait = WebDriverWait(driver, 20)
        FILE_NAME = '001first_start'

        sleep(10)
        self.check_cv(FILE_NAME)
        sleep(5)

        # ----------저장소 권한 묻는 팝업의 허용 버튼 터치----------
        FILE_NAME = '002first_start'
        self.check_cv(FILE_NAME)
        sleep(5)

        # ----------이용약관 일괄 동의 체크박스를 체크함----------
        FILE_NAME = '003check_box'
        self.check_cv(FILE_NAME)
        sleep(5)

        # ----------GUEST LOGIN 터치----------
        FILE_NAME = '004guest_login'
        self.check_cv(FILE_NAME)
        sleep(5)

        # ----------GUEST LOGIN 후 OK버튼 터치----------
        FILE_NAME = '005guest_ok_button'
        self.check_cv(FILE_NAME)
        sleep(10)

        # ----------홍보성 알림 수신 동의 버튼 터치----------
        FILE_NAME = '006agree_button'
        self.check_cv(FILE_NAME)
        sleep(13)

        # ----------클로버 터치----------
        FILE_NAME = '007clover'
        self.check_cv(FILE_NAME)
        sleep(3)

        # ----------클로버 팝업 X 버튼 터치----------
        FILE_NAME = '008clover_x_button'
        self.check_cv(FILE_NAME)
        sleep(3)

        # ----------코인 상점 터치----------
        FILE_NAME = '009coin_shop'
        self.check_cv(FILE_NAME)
        sleep(3)

        # ----------코인 상점 더보기 버튼 터치----------
        FILE_NAME = '010shop_more_button'
        self.check_cv(FILE_NAME)
        sleep(2)

        # ----------코인 상점 x 버튼 터치----------
        FILE_NAME = '011shop_x_button'
        self.check_cv(FILE_NAME)
        sleep(2)

        # ----------다이아 상점 터치----------
        FILE_NAME = '012diamond_shop'
        self.check_cv(FILE_NAME)
        sleep(3)

        # ----------다이아 상점 더보기 버튼 터치----------
        FILE_NAME = '010shop_more_button'
        self.check_cv(FILE_NAME)
        sleep(2)

        # ----------코인 상점 x 버튼 터치----------
        FILE_NAME = '011shop_x_button'
        self.check_cv(FILE_NAME)
        sleep(2)

        # ----------코인 상점 터치----------
        FILE_NAME = '009coin_shop'
        self.check_cv(FILE_NAME)
        sleep(3)

        # ----------상점 전환 버튼 터치(코인->다이아)----------
        FILE_NAME = '013change_shop01'
        self.check_cv(FILE_NAME)
        sleep(2)

        # ----------상점 전환 버튼 터치(다이아->코인)----------
        FILE_NAME = '014change_shop01'
        self.check_cv(FILE_NAME)
        sleep(2)

        # ----------x 버튼 터치----------
        FILE_NAME = '011shop_x_button'
        self.check_cv(FILE_NAME)
        sleep(2)

        # ----------다이아 상점 터치----------
        FILE_NAME = '012diamond_shop'
        self.check_cv(FILE_NAME)
        sleep(3)

        # ----------상점 전환 버튼 터치(다이아->코인)----------
        FILE_NAME = '014change_shop01'
        self.check_cv(FILE_NAME)
        sleep(2)

        # ----------상점 전환 버튼 터치(코인->다이아)----------
        FILE_NAME = '013change_shop01'
        self.check_cv(FILE_NAME)
        sleep(2)

        # ----------x 버튼 터치----------
        FILE_NAME = '011shop_x_button'
        self.check_cv(FILE_NAME)
        sleep(2)

        '''
        try:    
            FILE_NAME = '990vege_stage_button'
            self.check_cv(FILE_NAME)
            sleep(2)
        execpt:
            pass
        try:    
            FILE_NAME = '991vege_stage_ok_button'
            self.check_cv(FILE_NAME)
            sleep(2)
        execpt:
            pass
        try:    
            FILE_NAME = '992vege_stage_x_button'
            self.check_cv(FILE_NAME)
            sleep(2)
        execpt:
            pass

        # ----------1스테이지 터치----------
        FILE_NAME = '014stage1'
        self.check_cv(FILE_NAME)
        sleep(3)

        # ----------준비화면의 시작 버튼 터치----------
        FILE_NAME = '015stage1_start'
        self.check_cv(FILE_NAME)
        sleep(5)
        '''

# 앱을 종료시킵니다
def tearDown(self):
        self.driver.quit()

# 테스트가 시작되는 부분
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(pkpkg_login_test)
    unittest.TextTestRunner(verbosity=2).run(suite)