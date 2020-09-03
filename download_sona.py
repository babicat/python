import unittest
import os
from appium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.common.touch_action import TouchAction


# opencv를 사용하기 위해 아래 모듈을 import합니다.
import cv2
import numpy as np
import time, datetime


class TS():
    def makeTS(self):
        return str(int(datetime.datetime.now().timestamp()))

class GrandchaseLoginOutTest(unittest.TestCase):

    def setUp(self):
        
        #Test App 경로
        app = os.path.join(os.path.dirname(__file__), 'C:\\workspace\\apk', '026_coinblossom.apk')
        app = os.path.abspath(app)

                # Set up appium
        # Appium 서버의 포트는 4001로 지정합니다.
        # 그리고 desired_capabilities에 연결하려는 디바이스(V10)의 정보를 넣습니다.
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities={
                'app': app,
                'platformName': 'Android',
                'platformVersion': '10',
                'deviceName': 'zflip',
                'automationName': 'Appium',
                'appPackage': 'com.treenod.tapcoin.android.Google.global.normal',
                'appActivity': 'com.unity3d.player.UnityPlayerActivity',
                'udid': 'R39N200603T'
            })

    def test_search_field(self):

        ts = TS()

        # appiun의 webdriver를 초기화 합니다.
        driver = self.driver

        # selenium의 WebDriverWait을 사용합니다. element가 나올때 까지 최고 20초까지 기다립니다.
        wait = WebDriverWait(driver, 10)

        # 게임 실행 후 Asset을 다운로드할때까지 기다립니다.
        sleep(20)

        # python 파일이 실행된 현재 경로를 확인합니다.
        directory = '%s/' % os.getcwd()

        # appium에서 screenshot을 찍고 저장할 파일 이름을 생성합니다.
        screenshot = '%s-screenshot.png' % ts.makeTS()
        detectshot = '%s-detect.png' % ts.makeTS()
        # appium으로 스크린샷을 찍고 현제 경로에 저장합니다.
        driver.save_screenshot(directory + screenshot)

        # opencv로 스크린샵을 흑백으로 읽어들입니다.
        sourceimage = cv2.imread(screenshot, 0)

        # 찾으려는 이미지도 opencv로 읽어들입니다. (흑백: grayscale)
        template = cv2.imread('C:\\workspace\\img\\coin_2.png', 0)

        # 찾으려는 이미지의 폭과 높이를 확인합니다.
        w, h = template.shape[::-1]

        # opencv에서 이미지 매칭할 방법을 선택합니다. TM_CCOEFF으로 이미지를 찾겠습니다.
        method = eval('cv2.TM_CCOEFF')

        # opencv의 matchTemplate() 함수를 사용해 스크린샷 이미지에서 찾으려는 이미즈를 확인합니다.
        res = cv2.matchTemplate(sourceimage, template, method)

        '''
        matchTemplate() 함수의 결과값을 minMaxLoc() 함수에 넣습니다.
        이미지 매칭에 대한 최소값(min_val: 가장 비슷하지 가중치 값)과 
        최대값(max_val: 가장 비슷한 가중치 값)을 확인합니다.
        가중치가 낮은 곳의 정사각형의 왼쪽 위 모서리 좌표(min_loc)과 
        가중치가 큰 곳의 정사각형의 왼쪽 위 모서리 좌표(max_loc)를 확인할 수 있습니다.
        '''
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # max_loc을 이용해 찾으려는 이미지의 외쪽 위 모서리 좌표와 오른쪽 아래 모서리 좌표를 확인합니다.
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # 중앙 좌표도 확인합니다. 중앙 좌표는 x, y이므로 튜플로 확인합니다.
        center = (top_left[0] + int(w/2), top_left[1] + int(h/2))

        # 찾으려는 이미지가 맞는지 원본인 스크린샷 이미지에 사각형으로 표시해 봅니다.
        color = (0, 0, 255)
        cv2.rectangle(sourceimage, top_left, bottom_right, color, thickness=8)
        cv2.imwrite(detectshot, sourceimage)
        # appium(driver)의 tap 명령으로 중안 좌표를 클릭(탭)합니다.
        driver.tap([center])

        # 30초 동안 기다립니다.
        sleep(10)


#---------------------------------------------------
        
        screenshot = '%s-screenshot.png' % ts.makeTS()
        detectshot = '%s-detect.png' % ts.makeTS()
        driver.save_screenshot(directory + screenshot)

        sourceimage = cv2.imread(screenshot, 0)

        template = cv2.imread('C:\\workspace\\img\\coin_3.png', 0)

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
        sleep(10)
        
#-----------------------------------------------------------------
        screenshot = '%s-screenshot.png' % ts.makeTS()
        detectshot = '%s-detect.png' % ts.makeTS()
        driver.save_screenshot(directory + screenshot)

        sourceimage = cv2.imread(screenshot, 0)

        template = cv2.imread('C:\\workspace\\img\\coin_4.png', 0)

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
        sleep(200)



    def tearDown(self):
        self.driver.quit()



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(GrandchaseLoginOutTest)
    unittest.TextTestRunner(verbosity=2).run(suite)