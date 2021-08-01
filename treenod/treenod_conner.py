# -*- coding: utf-8 -*-
from base import BaseTestCase
import logging
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from util import language_check
LOGGER = logging.getLogger(__name__)
COMMON_URL = 'https://rc-www.treenod.com/'
ABOUT_URL = 'https://rc-www.treenod.com/about'
HISTORY_URL = 'https://rc-www.treenod.com/history'
LOCATION_URL = 'https://rc-www.treenod.com/location'
BLOG_URL = 'https://rc-www.treenod.com/blog'
CAREERS_URL = 'https://rc-www.treenod.com/careers'
GAMES_URL = 'https://rc-www.treenod.com/games'
BRAND_URL = 'https://rc-www.treenod.com/brand'
#****************************************2020-08-05 수정 내역**********************************************
# 1. check_menu_link 함수 추가 (매 페이지마다 메뉴쪽 링크 검증이 이루어지기 때문에 함수화)
# 2. 잔존하던 page 변수 삭제
# 3. TC012 코드 압축
# 4. TC014 ~ TC017 추가 (TC016은 패스)
#*********************************************************************************************************

class test_treenod(BaseTestCase):
    def check_scroll(self):
        self.selenium.wait('tag_name','body').send_keys(Keys.CONTROL + Keys.HOME) #control+home 키를 입력시켜 페이지 최상단으로 이동시킨다.
        self.selenium.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        scroll_result = self.selenium.driver.execute_script("return window.scrollY")
        
        if scroll_result <= 0:
            result = None
            self.assertIsNotNone(result,msg=" 스크롤이 움직이지 않았습니다!!!")
        LOGGER.info(" 스크롤 테스트 완료. Y축의 값 : " + str(scroll_result))
    
    def check_video(self):
        video_element = self.selenium.wait('css_selector','#container > div > div.main_banner_bg > video.video_pc > source')
        self.assertIsNotNone(video_element,msg= ' 동영상을 찾지 못했습니다!!!')
        LOGGER.info(' 동영상 로드 확인')

    # about의 숨은 메뉴 함수. 자주 쓰이는 것 같아서 함수화.
    def about_hide_menu_element(self):
        about_hide_menu_element = self.selenium.wait('xpath', '/html/body/div/header/div/nav/div[2]/ul/li[1]/ul')
        self.selenium.driver.execute_script('arguments[0].setAttribute("style", "display: block");',about_hide_menu_element)
        time.sleep(0.1)

    def check_url(self,full_url): 
        url = self.selenium.driver.current_url 
        if 'location' in url : full_url = LOCATION_URL
        elif 'history' in url : full_url = HISTORY_URL
        elif 'games' in url : full_url = GAMES_URL
        elif 'careers' in url : full_url = CAREERS_URL
        elif 'brand' in url : full_url = BRAND_URL
        elif 'blog' in url : full_url = BLOG_URL
        if url != full_url: 
            result = None 
            self.assertIsNotNone(result, msg = url + " 페이지 이동 실패!!!!!!") 
        LOGGER.info(" " + url + " 페이지 이동 확인") 

    def check_menu_text(self):
        real_menu_text = [self.selenium.get_text('xpath', '/html/body/div/header')]
        time.sleep(0.5)
        menu_text_kor = ['KOR\nAbout\nTreenod\nHistory\nLocation\nBlog\nCareers\nGames\nBrand']
        if menu_text_kor != real_menu_text:
            result = None
            self.assertIsNotNone(result,msg=" 메뉴 텍스트 검증 실패!!!!!!!!!!")
        LOGGER.info(" 메뉴 텍스트 검증 완료")

    def check_menu_link(self,full_url):
        self.about_hide_menu_element() 
        self.selenium.wait('xpath', '//*[@id="menu-item-717"]/a').click() #Treenod부터 진입시킴 
        url = self.selenium.driver.current_url
        if url != full_url: #만약 Treenod 매뉴를 클릭할 수 없다면 이 부분에서 모든 테스트가 종료 
            result = None 
            self.assertIsNotNone(result,msg = " Treenod 페이지 이동 실패!!!") 
        self.selenium.wait('xpath', '//*[@id="menu-item-715"]/a').click() #Treenod 매뉴를 클릭해서 주소 검증이 끝나면 about을 검증 
        LOGGER.info(' Treenod 페이지 이동 확인') #위에서 이미 Treenod 주소 검증이 끝났으므로 로그만 출력함 

        # 2. history ~ brand . 메뉴에 보이는 순서에는 어긋나나, menu-item-의 숫자에 맞춰서 클릭하게 함.
        for i in range(4):
            self.about_hide_menu_element()
            self.selenium.wait('xpath', '//*[@id="menu-item-71{0}"]/a'.format(i)).click() 
            self.check_url(full_url)

        # 5. 상단 treenod 로고
        self.selenium.wait('xpath','//*[@id="header"]/div/h1/a/img[1]').click()
        url = self.selenium.driver.current_url
        if url != COMMON_URL:
            result = None
            self.assertIsNotNone(result,msg=" 트리노드 로고 클릭 실패!!!!!")
        LOGGER.info(' 트리노드 로고 작동 확인')

    #---------------------------테스트 시작---------------------------
    def test_OpenUrl(self):
        result = self.selenium.open_url(COMMON_URL)
        self.assertTrue(result, msg='{0} 접속 실패'.format(COMMON_URL))
        LOGGER.info('{0} 접속 성공'.format(COMMON_URL))
        self.selenium.driver.maximize_window()
    
    #main
    def test_main_page(self):
        #TC001 모든 이미지가 정상적으로 출력된다.
        self.selenium.is_image_loaded(ignore_hidden=False)


        #TC002 배경 영상이 정상적으로 출력된다.
        self.check_video()


        #TC003 메뉴의 텍스트가 정상적으로 출력된다.
        self.about_hide_menu_element()
        self.check_menu_text()

        
        #TC004 내용의 텍스트가 정상적으로 출력된다.
        main_page_text = ['make\nalive\n\n좋은 사람들이\n만들어가는\n트리노드이야기',
                        '이야기를 만드는 사람들\n\n올바른 일에 대해 주도적인 사람, 팀과 동료에게 긍정적인 영향을 주는 사람,\n사람에 대한 존중과 배려, 전문성과 책임감이 있는 사람, 자신의 창의성을 자유롭게\n표현할 수 있는 사람.\n우리는 트리티브이고, 트리티브가 모여 트리노드를 만들어 나갑니다.\n\n더보기',
                        'Careers\n다음 이야기를 함께할\n트리티브를 기다립니다.\n\n사람에 대한 믿음을 바탕으로, 개인에 대한 규제보다는 자율성을 중시하는 회사 트리노드. 열정이 가득한 당신에게 트리노드의 문은 언제나 열려 있습니다.\n\n더보기',
                        'Game\n포코팡과 포코포코 그리고...\n\n9,000만 다운로드를 기록하며 전 세계적으로 사랑받고 있는 게임 포코팡과\n포코포코 이후 포코숲 동물 친구들과 즐길 수 있는 다양한 장르의 게임을\n선보이고자 합니다.\n\n더보기',
                        'Character Business\n게임 밖으로 나온 포코팡\n\n포코팡 캐릭터는 모바일 게임 뿐만 아니라 애니메이션, 웹툰, 일러스트레이션 등\n다양한 장르의 콘텐츠를 통해 소개되고 있습니다.\n\n포코팡은 전세계 약 9,000만 다운로드의 게임 포코팡 시리즈에서 탄생한\n캐릭터 브랜드 입니다. 심심한 것은 참을 수 없는 분홍색 토끼 ‘포코타’와\n숲 속 동물들의 이야기가 펼쳐 집니다.\n\n더보기',
                        'Treenod Office\nLocation\n\nBusan - HQ\n부산 해운대구 센텀2로 25, 15F\n15F, 25, Centum2-ro,\nHaeundae-gu, Busan, Korea\n\nSeoul Office\n서울 강남구 선릉로 667, 8F\n8F, 667, Seolleung-ro,\nGangnam-gu, Seoul, Korea',
                        '공지사항\n이용약관\n개인정보처리방침\n이메일 무단수집 거부\ncontact@treenod.com facebook blog\n\nⓒTreenod Inc., All rights reserved.']

        # main_banner의 slogan 
        main_banner_slogan = self.selenium.get_text('xpath', '/html/body/div/div[1]/div/div[2]')
        if main_banner_slogan not in main_page_text:
            result = None
            self.assertIsNotNone(result,msg=" 메인 슬로건 텍스트 검증 실패!!!")
        LOGGER.info(" 메인 슬로건 텍스트 검증 완료")

        # sector01 ~ sector05
        for i in range(5):
            self.selenium.driver.execute_script("arguments[0].scrollIntoView();", self.selenium.wait('xpath', '/html/body/div/div[1]/section[{0}]'.format(i+1)))
            time.sleep(0.1)
            sector_text = self.selenium.get_text('xpath', '/html/body/div/div[1]/section[{0}]'.format(i+1))
            if sector_text not in main_page_text:
                result = None
                self.assertIsNotNone(result,msg=" 섹터" + str(i+1) +  "텍스트 검증 실패!!!")
            LOGGER.info(" 섹터" + str(i+1) +  " 텍스트 검증 완료")

        # 푸터 텍스트
        fotter_text = self.selenium.get_text('xpath', '/html/body/div/footer')
        if fotter_text not in main_page_text:
            result = None
            self.assertIsNotNone(result,msg=" 푸터 텍스트 검증 실패!!!")
        LOGGER.info(" 푸터 텍스트 검증 완료")


        # TC006 스크롤 방향에 따라 화면이 이동된다.
        self.check_scroll()


        # TC007 선택한 메뉴 페이지로 연결된다.
        full_url = ABOUT_URL
        self.check_menu_link(full_url)


        # TC008 내용의 선택한 메뉴 페이지로 이동된다.
        # 각 섹션의 [더보기] 버튼을 검증.
        for i in range(4):
            self.selenium.driver.execute_script("arguments[0].scrollIntoView();", self.selenium.wait('xpath', '//*[@id="sector0{0}"]'.format(i+1)))
            time.sleep(0.1)
            self.selenium.wait('xpath','//*[@id="sector0{0}"]/div/div/a'.format(i+1)).click()
            self.check_url(full_url)
            self.selenium.wait('xpath','//*[@id="header"]/div/h1/a/img[1]').click() #<- 메인으로 돌아가야하기 때문에 treenod 로고를 클릭하게 함


        #TC009 선택한 언어로 웹페이지의 텍스트가 변경된다.
        # 1. 기본 한국어 먼저 검증
        time.sleep(0.1)
        main_page_text = self.selenium.get_text('xpath', '/html/body')
        language_check.check(main_page_text)
        
        # 2,3 영어와 일본어 검수 후 다시 한국어 전환
        for i in range(2):
            self.selenium.wait('xpath','/html/body/div/header/div/nav/div[1]/a').click()
            time.sleep(0.1)
            self.selenium.wait('xpath','//*[@id="header"]/div/nav/div[1]/ul/li[{0}]/a'.format(i+2)).click()
            self.selenium.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            main_page_text = self.selenium.get_text('xpath', '/html/body')
            language_check.check(main_page_text)
        self.selenium.wait('xpath','/html/body/div/header/div/nav/div[1]/a').click()
        self.selenium.wait('xpath','//*[@id="header"]/div/nav/div[1]/ul/li[1]/a').click()

    # ABOUT 페이지 검증
    def test_about_page(self):
        self.selenium.wait('xpath', '//*[@id="menu-item-715"]/a').click()

        #TC010 모든 이미지가 정상적으로 출력된다.
        self.selenium.is_image_loaded(ignore_hidden=False)

        #TC011 메뉴의 텍스트가 정상적으로 출력된다.
        self.about_hide_menu_element()
        self.check_menu_text()

        #TC012 내용의 텍스트가 정상적으로 출력된다.
        about_page_text = ['About Treenod\n이야기를 만드는\n사람들\n\n트리노드는 글로벌 누적 다운로드 9,000만 이상을 기록한\n모바일 게임 포코팡 시리즈를 개발했습니다.\n이제는 게임 속의 이야기가 게임 안팎에서 사람들의 삶에\n함께할 수 있도록 사업 영역을 넓혀 나가고 있습니다.',
                            'Our Vision\nNarrative creation 매력적인 이야기로 사람들의 참여를 이끌어내고\n그들 자신의 이야기로 만들어 주는 기업\n\n매력적인 이야기는 시대를 뛰어넘어 사람의 마음을 움직입니다.\n우리가 만드는 콘텐츠 안에 담겨있는\n매력적인 이야기로 사람들의 참여를\n이끌어내고 그들 자신의 서사로\n만들어 주는 것이 트리노드가 꿈꾸는\n비전입니다.',
                            'Our Mission\nRediscover diversified emotions\n다채로운 감정은 사람들의 삶을\n더 건강하고 행복하게 만듭니다.\n\n우리는 사람들이 우리가 만드는 콘텐츠를 통해\n스스로의 이야기를 만들며 다양한 감정을\n다시 발견하며 삶이 더 행복해지길 바랍니다.',
                            "Our Value / Spirit\nMake alive\n트리노드는 '더 나음'을 추구합니다.\n\n'더 나음'은 현재에 머무르지 않고 내일의 변화에 대응하며\n'정해져 있지 않은 것, 즉 살아있는 것을 만들어 내는 것'입니다.\nmake alive는 트리노드가 하는 모든 일의 기준입니다.\n\n제대로 된 결과물을 만들어내기 위해 끊임없이 '왜?'라고 질문합니다.\n\n이런 과정에서 일어나는 갈등으로부터 우리만의 의미 있는 변화를 만들어냅니다.\n우리는 이러한 가치들이 더 나음을 만들어갈 수 있다고 믿습니다.",
                            '공지사항\n이용약관\n개인정보처리방침\n이메일 무단수집 거부\ncontact@treenod.com facebook blog\n\nⓒTreenod Inc., All rights reserved.']

        about_banner_text = self.selenium.get_text('xpath','//*[@id="container"]/div')
        if about_banner_text not in about_page_text:
            result = None
            self.assertIsNotNone(result,msg=" about 배너 텍스트 검증 실패!!!!")
        LOGGER.info(" about 배너 텍스트 검증 완료")

        for i in range(3):
            self.selenium.driver.execute_script("arguments[0].scrollIntoView();", self.selenium.wait('xpath', '//*[@id="about0{0}"]'.format(i+1)))
            time.sleep(0.1)
            about_sector_text = self.selenium.get_text('css_selector', '#about0{0} > div'.format(i+1))
            if about_sector_text not in about_page_text:
                result = None
                self.assertIsNotNone(result,msg=" about 섹터" +str(i+1)+ " 텍스트 검증 실패!!!!")    
            LOGGER.info("about 섹터" + str(i+1) + " 텍스트 검증 완료")

        about_fotter_text = self.selenium.get_text('xpath', '//*[@id="footer"]')
        if about_fotter_text not in about_page_text:
            result = None
            self.assertIsNotNone(result,msg=" about 푸터 텍스트 검증 실패!!!!")
        LOGGER.info(" about 푸터 텍스트 검증 완료")

        #TC014 스크롤 방향에 따라 화면이 이동된다.
        self.check_scroll()

        #TC015 선택한 메뉴 페이지로 연결된다.
        full_url = ABOUT_URL
        self.check_menu_link(full_url)
        self.selenium.wait('xpath','//*[@id="menu-item-715"]/a').click()
        
        #TC017 선택한 언어로 웹 페이지의 텍스트 변경된다.
        time.sleep(0.1)
        about_page_text = self.selenium.get_text('xpath', '/html/body')
        language_check.check(about_page_text)
        
        for i in range(2):
            self.selenium.wait('xpath','/html/body/div/header/div/nav/div[1]/a').click()
            time.sleep(0.1)
            self.selenium.wait('xpath','//*[@id="header"]/div/nav/div[1]/ul/li[{0}]/a'.format(i+2)).click()
            self.selenium.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(1)
            about_page_text = self.selenium.get_text('xpath', '/html/body')
            language_check.check(about_page_text)
        self.selenium.wait('xpath','/html/body/div/header/div/nav/div[1]/a').click()
        self.selenium.wait('xpath','//*[@id="header"]/div/nav/div[1]/ul/li[1]/a').click()