# -*- coding: utf-8 -*-
import logging
# import coloredlogs
import time
import json
import re
from enum import Flag, auto
from base import BaseTestCase, unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from util import language_check

LOGGER = logging.getLogger()
# coloredlogs.install(level='INFO') # LOGGER.info 내용이 많아 WARNING 과 구분하기 위하여 추가

BASE_URL = 'https://www.pokopang.com/' # 테스트할 페이지의 기본 URL

MAIN = {'ko' : {'url' : 'ko', 'search' : '포코포코'},
        'jp' : {'url' : 'home', 'search' : 'ポコポコ'},
        'en' : {'url' : 'en', 'search' : 'Pokopoko'}} # MAIN 페이지 언어(ko, jp, en)별 필요 추가 url 스트링과 언어에 따라 사용할 검색어를 딕셔너리 형태로 저장

ABOUT = {'ko' : {'url' : 'ko/about', 'search' : '포코'},
         'jp' : {'url' : 'about', 'search' : 'ポコ'},
         'en' : {'url' : 'en/about', 'search' : 'Poko'}} # ABOUT 페이지 언어(ko, jp, en)별 필요 추가 url 스트링과 언어에 따라 사용할 검색어를 딕셔너리 형태로 저장

NEWS = {'ko' : {'url' : 'ko/news', 'search' : '포코'},
        'jp' : {'url' : 'news', 'search' : 'ポコ'},
        'en' : {'url' : 'en/news', 'search' : 'Poko'}} # NEWS 페이지 언어(ko, jp, en)별 필요 추가 url 스트링과 언어에 따라 사용할 검색어를 딕셔너리 형태로 저장

CONTENTS = {'ko' : {'url' : 'ko/contents', 'search' : '포코'},
            'jp' : {'url' : 'contents', 'search' : 'ポコ'},
            'en' : {'url' : 'en/contents', 'search' : 'Poko'}} # CONTENTS 페이지 언어(ko, jp, en)별 필요 추가 url 스트링과 언어에 따라 사용할 검색어를 딕셔너리 형태로 저장

CONTACT = {'ko' : {'url' : 'ko/contact', 'search' : '라이선스'},
           'jp' : {'url' : 'contact', 'search' : 'ライセンス'},
           'en' : {'url' : 'en/contact', 'search' : 'license'}} # CONTACT 페이지 언어(ko, jp, en)별 필요 추가 url 스트링과 언어에 따라 사용할 검색어를 딕셔너리 형태로 저장

class TestPokopangcomko(BaseTestCase):

    def wait_for_window(self, timeout=3): # 창 전환 관련 selenium ide 에서 생성된 부분
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def check_by_lang(self, func): # MAIN 페이지 언어별 Tc test 함수
        """동일 테스트 KO, JP, EN 언어별로 반복"""
        for key, value in MAIN.items():
            LANG = key
            SEARCH_KEYWORD = value['search'] # 언어별 search 값 매칭
            current_url = BASE_URL + value['url'] # 언어별 url 값 매칭
            self.selenium.open_url(current_url)
            result = self.selenium.open_url(current_url)
            func(LANG, search_keyword = SEARCH_KEYWORD, result = result)

    def about_check_by_lang(self, func): # ABOUT 페이지 언어별 Tc test 함수
        """동일 테스트 KO, JP, EN 언어별로 반복"""
        for key, value in ABOUT.items():
            LANG = key
            SEARCH_KEYWORD = value['search'] # 언어별 search 값 매칭
            current_url = BASE_URL + value['url'] # 언어별 url 값 매칭
            self.selenium.open_url(current_url)
            result = self.selenium.open_url(current_url)
            func(LANG, search_keyword = SEARCH_KEYWORD, result = result)
            
    def news_check_by_lang(self, func): # NEWS 페이지 언어별 Tc test 함수
        """동일 테스트 KO, JP, EN 언어별로 반복"""
        for key, value in NEWS.items():
            LANG = key
            SEARCH_KEYWORD = value['search'] # 언어별 search 값 매칭
            current_url = BASE_URL + value['url'] # 언어별 url 값 매칭
            self.selenium.open_url(current_url)
            result = self.selenium.open_url(current_url)
            func(LANG, search_keyword = SEARCH_KEYWORD, result = result)
    
    def contents_check_by_lang(self, func): # CONTENTS 페이지 언어별 Tc test 함수
        """동일 테스트 KO, JP, EN 언어별로 반복"""
        for key, value in CONTENTS.items():
            LANG = key
            SEARCH_KEYWORD = value['search'] # 언어별 search 값 매칭
            current_url = BASE_URL + value['url'] # 언어별 url 값 매칭
            self.selenium.open_url(current_url)
            result = self.selenium.open_url(current_url)
            func(LANG, search_keyword = SEARCH_KEYWORD, result = result)

    def contact_check_by_lang(self, func): # CONTACT 페이지 언어별 Tc test 함수
        """동일 테스트 KO, JP, EN 언어별로 반복"""
        for key, value in CONTACT.items():
            LANG = key
            SEARCH_KEYWORD = value['search'] # 언어별 search 값 매칭
            current_url = BASE_URL + value['url'] # 언어별 url 값 매칭
            self.selenium.open_url(current_url)
            result = self.selenium.open_url(current_url)
            func(LANG, search_keyword = SEARCH_KEYWORD, result = result)

    def check_menu_list(self, menu_list, menu_type, language): # 공통 사용되는 menu_list 검증 함수
        # menu_list = ['ABOUT', 'NEWS', 'CONTENTS', 'CONTACT']
        # menu_type : "top", "hamburger", "footer"

        count = 0
        for index, expected_value in enumerate(menu_list): # for + enumerate 사용
            if menu_type == 'top':
                menu_xpath = f'/html/body/header/div[1]/div/nav/ul/li[{index+1}]/a'
            elif menu_type == 'hamburger':
                menu_xpath = f'/html/body/header/div[3]/div/ul/li[{index+2}]/a'
                self.selenium.wait('xpath', '/html/body/header/div[1]/div/ul/li[2]').click() # 햄버거 버튼 클릭
            elif menu_type == 'footer':
                menu_xpath = f'/html/body/footer/div[1]/div/div[1]/div/ul[{index+1}]/li/a'

            expected_xpath = '/html/body/main/div[1]/ul/li[2]' # 버튼 선택하여 이동한 페이지에서 고정값으로 기대되는 페이지 트리 xpath 기대값으로 설정

            if expected_value == 'CONTACT': # CONTACT US 메뉴만 xpath 값이 달라 if 로 분기 처리
                expected_xpath = '/html/body/main/div/ul/li[2]'

            self.selenium.wait('xpath', menu_xpath).click() # 각 메뉴 클릭 실행
            time.sleep(1)

            menu = self.selenium.wait('xpath', expected_xpath)
            result = menu.text.split(' ')[0] # 가져온 menu text 중, contact의 경우 'CONTACT US' 이기 때문에 공백 기준으로 문자열 자름

            if expected_value == result:
                count += 1

            LOGGER.info("TC_menu_check: (%s) %s menu '%s' - test is pass", language, menu_type, result)
        return len(menu_list) == count

    def check_page_main_title(self, page_name, language): # 공통 사용되는 page main title text 검증 함수
        main_title_xpath = "/html/body/main/div[2]/h1" # about 페이지 상단 타이틀 xpath  
        result_text = self.selenium.get_text('xpath', main_title_xpath)
        
        if page_name == 'ABOUT':
            expected_text = 'ABOUT'
        elif page_name == 'NEWS':
            expected_text = 'NEWS'
        elif page_name == 'CONTENTS':
            expected_text = 'CONTENTS'

        self.assertEqual(expected_text, result_text, msg=("Tc_pages's main title: expected_title = {expected_text}, result = {result_text}")) # 검증
        LOGGER.info("TC_page's main title: (%s) '%s page's title text: '%s' - test is pass", language, page_name, result_text)
    
    def test_Tc001(self): # 포코팡닷컴 MAIN 페이지 오픈
        """웹 브라우저 > 포코팡닷컴 접속"""
        print("=================================================== MAIN PAGE ===================================================")
        def Tc001(LANG, **kwargs):
            result = kwargs['result']
            self.assertTrue(result, msg='Tc001: open url - test is fail')
            LOGGER.info("Tc001: (%s) open url '%s'- test is pass", LANG, result)

        self.check_by_lang(Tc001)

    def test_Tc002(self): # 현재 페이지 언어 감지 - 뉴스 헤드라인 부분으로 검증
        """language_check 모듈로 현재 웹페이지 언어 감지"""
        def Tc002(LANG, **kwargs):
            main_contents_xpath = "//div[@class='clearfix']" # 페이지 중단 컨텐츠 xpath
            main_contents_text = self.selenium.get_text('xpath', main_contents_xpath) # 컨텐츠에 있는 텍스트 모두 저장
            result_list = language_check.check(main_contents_text) # language_check 모듈 > 함수 사용하여 컨텐츠 텍스트 언어 감지

            if len(result_list) >= 2: # 2가지 이상 언어가 섞여 있을 경우의 처리
                LOGGER.warning("Tc002: (%s) 이 페이지 언어는 %s가 동일 비율로 섞여 있어 추가 확인이 필요합니다.", LANG, result_list)

            elif len(result_list) == 0: # 언어 판단 불가능할 경우의 처리
                LOGGER.warning("Tc002: (%s) 이 페이지 언어는 판단 가능한 언어가 포함되지 않아 %s 추가 확인이 필요합니다.", LANG, result_list)

            elif 'ko' in result_list: # 한국어 비율이 높을 경우의 처리
                LOGGER.info("Tc002: (%s) 이 페이지는 한국어%s 페이지일 가능성이 높습니다.", LANG, result_list)

            elif 'en' in result_list: # 영어 비율이 높을 경우의 처리
                LOGGER.info("Tc002: (%s) 이 페이지는 English%s 페이지일 가능성이 높습니다.", LANG, result_list)

            elif 'ja' in result_list: # 일본어 비율이 높을 경우의 처리
                LOGGER.info("Tc002: (%s) 이 페이지는 日本語%s 페이지일 가능성이 높습니다.", LANG, result_list)

            self.assertIsNotNone(result_list, msg='Tc002: language_check - test is fail')
            LOGGER.info("Tc002: (%s) language_check = %s - test is pass", LANG, result_list)

        self.check_by_lang(Tc002)

    def test_Tc003(self): # 메인 > 탑 메뉴 'POKOPANG!' 선택 > 탭 타이틀 텍스트 비교
        """탑 메뉴 > POKOPANG! 클릭 후, 탭 타이틀 비교"""
        def Tc003(LANG, **kwargs):
            pokopang_xpath = "//a[@class='over']//img" # 좌측 상단 POKOPANG! xpath
            pokopang = self.selenium.wait('xpath', pokopang_xpath)
            pokopang.click() # 'POKOPANG!' 버튼 클릭
            title_xpath = "//title[contains(text(),'POKOPANG!')]" # title xpath
            title = self.selenium.wait('xpath', title_xpath)

            result_title = title.get_attribute('innerText') # title text 가져옴(innerText or textContent)
            expected_title = 'POKOPANG!' # 타이틀 기대값

            self.assertIn(expected_title, result_title, msg=(f'Tc003: expected title = {expected_title}, result = {result_title}')) # 검증
            LOGGER.info("Tc003: (%s) 'POKOPANG!' link page's title: '%s' - test is pass", LANG, result_title)

        self.check_by_lang(Tc003)

    def test_Tc004_Tc007(self): # 탑 메뉴 xpath로 찾아 클릭하여 해당 페이지 이동, menu path 검증
        """탑 메뉴 > ABOUT, NEWS, CONTENTS, CONTACT xpath 로 가져와서 text 비교"""
        def Tc004_Tc007(LANG, **kwargs):
            expected_top_list = ['ABOUT', 'NEWS', 'CONTENTS', 'CONTACT'] # 탑 메뉴 list

            result = self.check_menu_list(expected_top_list, 'top', LANG)
            self.assertTrue(result, msg='TC_menu_check - test is fail')
            LOGGER.info("Tc004~007: (%s) top menu '%s' - test is pass", LANG, result)

        self.check_by_lang(Tc004_Tc007)

    def test_Tc008_Tc009(self): # 탑 메뉴 > 돋보기 아이콘 클릭 > 검색창에 특정 단어 입력하여 검색 버튼으로 검색/검증
        """탑 메뉴 > 돋보기 검색 기능 검증(search 버튼)"""
        def Tc008_Tc009(LANG, **kwargs):
            SEARCH_KEYWORD = kwargs['search_keyword']
            magnify_xpath = "//li[@id='js-searchBtn']" # 돋보기 아이콘 xpath
            magnify = self.selenium.wait('xpath', magnify_xpath)
            magnify.click() # 돋보기 아이콘 클릭
            time.sleep(1)

            search_box_xpath = "//input[@name='s']" # 검색 창 xpath
            search_box = self.selenium.wait('xpath', search_box_xpath)
            search_box.send_keys(SEARCH_KEYWORD) # 검색 창에 검색어 입력
            time.sleep(1)

            search_button_xpath = "//button[@class='header_search_btn']" # 검색 창 옆 'search' 버튼 xpath
            search_button = self.selenium.wait('xpath', search_button_xpath)
            search_button.click() # search 버튼 클릭
            time.sleep(1)

            expected_keyword = SEARCH_KEYWORD # 기대값 = 입력 검색어
            search_head = self.selenium.wait('xpath', "//div[@class='search_head']") # '/html/body/main/div[2]/div[1]' # 검색 결과창 xpath로 속성 가져옴
            span_list = search_head.find_elements_by_tag_name('span') # search_head 안에 결과 값 2개가 span 태그 안에 있어 가져옴
            span_one = span_list[0] # span 안에 2개가 있어 분리, 첫번째 ("검색어" text)
            span_two = span_list[1] # span 두번째 (검색 결과 카운트 text)
            result_keyword = span_one.text.strip('“”') # 키워드 앞뒤로 큰따옴표(“”) 제거
            expected_count = int(span_two.text) # 검색 결과 카운트 문자 → 숫자 변환
            ul_element = self.selenium.wait('xpath', "//ul[@class='col3_block_list']") # 하단 검색 결과 집합

            item_class_list = ul_element.find_elements_by_class_name('col3_block_list_item') # 하단 전체 집합에서 특정 클래스 네임이 들어간 부분 list

            result_count = len(item_class_list) # item_class_list 갯수

            self.assertEqual(expected_keyword, result_keyword, msg=(f'Tc008: expected keyword = {expected_keyword}, result = {result_keyword}')) # 검증
            LOGGER.info("Tc008: (%s) search keyword '%s' - test is pass", LANG, result_keyword)
            self.assertEqual(expected_count, result_count, msg=(f'Tc009: expected count = {expected_count}, result = {result_count}')) # 검증
            LOGGER.info("Tc009: (%s) search count '%d' - test is pass", LANG, result_count)
            time.sleep(1)

        self.check_by_lang(Tc008_Tc009)

    def test_Tc010_Tc011(self): # 탑 메뉴 > 돋보기 아이콘 클릭하여 검색창에 특정 단어 입력하여 엔터키로 검색/검증
        """탑 메뉴 > 돋보기 검색 기능 검증(엔터키 입력)"""
        def Tc010_Tc011(LANG, **kwargs):
            SEARCH_KEYWORD = kwargs['search_keyword']
            magnify = "//li[@id='js-searchBtn']" # 돋보기 아이콘 xpath
            self.selenium.wait('xpath', magnify).click() # 돋보기 아이콘 클릭
            time.sleep(1)
          
            search_box = "//input[@name='s']" # 검색 창 xpath
            self.selenium.wait('xpath', search_box).send_keys(SEARCH_KEYWORD, Keys.RETURN) # 검색 창 검색어 입력 + ENTER
            time.sleep(1)

            expected_keyword = SEARCH_KEYWORD

            search_head = self.selenium.wait('xpath', '/html/body/main/div[2]/div[1]')
            span_list = search_head.find_elements_by_tag_name('span')
            span_one = span_list[0] # span 에서 첫번째 값, 두번째 값 분리
            span_two = span_list[1]

            result_keyword = span_one.text.strip('“”') # 검색결과 키워드에서 앞뒤 큰따옴표 제거
            expected_count = int(span_two.text) # 문자 → 숫자 변환

            self.assertEqual(expected_keyword, result_keyword, msg=(f'Tc010: expected keyword = {expected_keyword}, result = {result_keyword}')) # 검증
            LOGGER.info("Tc010: (%s) search keyword '%s' - test is pass", LANG, result_keyword)

            """검색어를 입력해서 나온 결과 페이지에 실제 해당 검색어가 들어 있는지 검증"""
            # 검색어가 타이틀(헤드라인)에 있는지, 실제 본문에 있는지 확인
            # 만약 해당 컨텐츠에 실제 검색어가 있으면 카운트를 +1
            # 타이틀에 검색어가 있으면, 본문 검색 불필요
            # 타이틀에 검색어가 없으면, 본문에 있는지 검색
            # 타이틀, 본문 둘 다 검색어가 없다면 잘못된 부분으로 에러 처리

            item_list = self.selenium.wait('class_name', 'col3_block_list_item', find_multiple=True) # tag_name 으로 찾으면 실제 결과값 안맞아서 class_name으로 변경
            real_count = 0 # 실제 검색어 여부에 따라 카운트를 저장해줄 변수 지정

            if not item_list: # 검색 결과가 없을 때의 처리
                LOGGER.warning("Tc011: (%s) search_keyword '%s' - No results were found for your search", LANG, SEARCH_KEYWORD)
                return

            # 기존 코드는 뒤돌아가기로 페이지 돌아올 경우, element를 못찾음
            # 되돌아가기로 돌아오더라도 아이템 리스트를 기억할 수 있게 변경
            for index in range(len(item_list)):
                item_list = self.selenium.wait('class_name', 'col3_block_list_item', find_multiple=True) # 페이지 되돌아 왔을 때, 이전 element 속성값 찾지 못해 리스트 저장
                li = item_list[index]
                try:
                    li_div = li.find_element_by_class_name('col3_block_text')
                except Exception as e:
                    LOGGER.warning("Tc011: (%s) real count test is fail. '%s'", LANG, e)
                    continue # 에러 무시하고 다시 for문 진행
                li_div_p = li_div.find_element_by_tag_name('p')
                title_contents = li_div_p.text # 컨텐츠 헤드라인 텍스트

                if SEARCH_KEYWORD in title_contents: # 검색어가 헤드라인에 들어 있으면 카운트 +1 증가
                    real_count += 1
                    LOGGER.info("Tc011: (%s) '%s'(제목): real count '%d'", LANG, title_contents, real_count)
                else:
                    li.click() # 검색 결과 클릭하여 해당 연결 사이트로 이동
                    body_contents = self.selenium.wait('xpath', '/html/body/main/article/div/div[2]/div[3]') # 연결된 페이지
                    body_contents_p_list = body_contents.find_elements_by_tag_name('p') # 연결된 페이지 'p' 태그 확인
                    for p in body_contents_p_list: # p 태그 안 텍스트에 검색어가 있으면 카운트 +1 증가
                        if SEARCH_KEYWORD in p.text:
                            real_count += 1
                            LOGGER.info("Tc011: (%s) '%s'(본문): real count '%d'", LANG, p.text, real_count)
                            break # 검색어가 확인되면 추가 검증없이 바로 나감
                    time.sleep(2)
                    self.driver.back() # 이전 화면 되돌아가기
                    time.sleep(2)
            self.assertEqual(expected_count, real_count, msg=(f'Tc011: expected_count = {expected_count}, real_count = {real_count}'))
            LOGGER.info("Tc011: (%s) real count '%d' - test is pass", LANG, real_count)

        self.check_by_lang(Tc010_Tc011)

    def test_Tc012(self): # 탑 메뉴 > 햄버거 선택 후, 추가 노출되는 메뉴 중 HOME 검증
        """햄버거 버튼 하위 메뉴 HOME을 타이틀명으로 검증"""
        def Tc012(LANG, **kwargs):
            hamburger = "//li[@id='js-sitemenuBtn']" # 햄버거 xpath
            self.selenium.wait('xpath', hamburger).click() # 햄버거 버튼 클릭
            home = '/html/body/header/div[3]/div/ul/li[1]/a' # HOME xpath
            self.selenium.wait('xpath', home).click() # HOME 메뉴 클릭

            title_xpath = "//title[contains(text(),'POKOPANG!')]"
            title = self.selenium.wait('xpath', title_xpath) # 타이틀 속성 지정

            result_title = title.get_attribute('innerText') # title의 text 가져옴, innerText 대신 textContent 도 결과 동일
            expected_title = 'POKOPANG!' # 타이틀 스트링 기대값

            self.assertIn(expected_title, result_title, msg=(f'Tc012: expected title = {expected_title}, result = {result_title}')) # 검증
            LOGGER.info("Tc012: (%s) hamburger menu 'HOME(%s)' - test is pass", LANG, result_title)
        
        self.check_by_lang(Tc012)

    def test_Tc013_Tc016(self): # 탑 메뉴 > 햄버거 선택 후, 추가 노출되는 메뉴 중 HOME을 제외한 나머지 검증
        """햄버거 버튼 하위 메뉴 ABOUT, NEWS, CONTENTS, CONTACT를 xpath로 검증"""
        def Tc013_Tc016(LANG, **kwargs):
            expected_hamburger_list = ['ABOUT', 'NEWS', 'CONTENTS', 'CONTACT']

            result = self.check_menu_list(expected_hamburger_list, 'hamburger', LANG)
            self.assertTrue(result, msg='TC_menu_check - test is fail')
            LOGGER.info("Tc013~016: (%s) hamburger menu '%s' - test is pass", LANG, result) # 검증

        self.check_by_lang(Tc013_Tc016)

    def test_Tc017_Tc019(self): # 탑 메뉴 > 햄버거 선택 후, 추가 노출되는 메뉴 중 언어 변경 검증
        """햄버거 버튼 하위 메뉴 English, 日本語, 한국어 html tag_name lang 으로 검증"""
        def Tc017_Tc019(LANG, **kwargs):
            expected_language_list = ['en-US', 'ja', 'ko-KR']

            for index, expected_lang in enumerate(expected_language_list):
                self.selenium.wait('xpath', '/html/body/header/div[1]/div/ul/li[2]').click() # 햄버거 버튼 클릭
                xpath = f'/html/body/header/div[3]/div/div/ul/li[{index+1}]' # 각 메뉴 xpath

                self.selenium.wait('xpath', xpath).click() # 각 메뉴 클릭 실행
                time.sleep(1)

                result_lang = self.selenium.wait('tag_name', 'html').get_attribute('lang') # 각 언어 페이지마다 html lang 값 가져옴

                if result_lang == 'en-US': # 영어 검증
                    self.assertEqual(expected_lang, result_lang, msg=(f'Tc017: expected title = {expected_lang}, result = {result_lang}'))
                    LOGGER.info("Tc017: (%s) hamburger menu 'English(%s)' - test is pass", LANG, result_lang)
                    time.sleep(1)

                elif result_lang == 'ja': # 일본어 검증
                    self.assertEqual(expected_lang, result_lang, msg=(f'Tc017: expected title = {expected_lang}, result = {result_lang}'))
                    LOGGER.info("Tc018: (%s) hamburger menu '日本語(%s)' - test is pass", LANG, result_lang)
                    time.sleep(1)

                elif result_lang == 'ko-KR': # 한국어 검증
                    self.assertEqual(expected_lang, result_lang, msg=(f'Tc017: expected title = {expected_lang}, result = {result_lang}'))
                    LOGGER.info("Tc019: (%s) hamburger menu '한국어(%s)' - test is pass", LANG, result_lang)
                    time.sleep(1)

        self.check_by_lang(Tc017_Tc019)

    def test_Tc020(self): # 메인 페이지 > 이미지 검증
        """페이지 전체 이미지 로드 되는지 확인"""
        def Tc020(LANG, **kwargs):
            image_load = self.selenium.is_image_loaded()
            self.assertTrue(image_load, msg='Tc020: image_load - test is fail')
            LOGGER.info("Tc020: (%s) page's image load '%s' - test is pass", LANG, image_load)
        
        self.check_by_lang(Tc020)

    def test_Tc021(self): # 상단 슬라이드 배너 > 슬라이드 버튼 검증
        """이미지 노출 확인, 이동 버튼 클릭하여 배너 이미지 바뀌는지 확인"""
        def Tc021(LANG, **kwargs):
            # 단순 버튼 클릭 검증 or 버튼 선택 후, 이동 결과 값 검증
            # 두번째 슬라이드 배너의 경우, 클릭하면 라인 스티커 구매 페이지 연결
            # 목적: 슬라이드 버튼 존재 확인
            def is_button_exist():
                button_tag = self.selenium.wait('xpath', "//button[@class='slick-prev slick-arrow']")
                # 슬라이드 배너 이동 버튼
                # /html/body/main/div[1]/div/button[1], /html/body/main/div[1]/div/button[2]
                if button_tag:
                    return True
                return False

            def stop_moving_slide_banner(): # 슬라이드 배너가 자동 이동 되지 않도록 정지
                action = ActionChains(self.driver)
                el = self.selenium.wait('class_name', 'main_visual_list')
                action.move_to_element(el)
                action.perform()

            def get_current_banner_image_name(slide): # 현재 배너 이미지 주소를 가져오는 함수
                current_banner = slide.find_element_by_class_name('slick-current')
                current_url = current_banner.value_of_css_property('background-image')
                current_url = current_url.split('url(')[1].split(')')[0].strip('""')
                banner_image_name = current_url.split("/")[-1]
                return banner_image_name

            def get_current_slide_banner_url_after_click(): # 버튼 클릭 후에 슬라이드 배너 url 가져오는 함수
                self.selenium.wait('xpath', "//button[@class='slick-prev slick-arrow']").click() # click이 제대로 되는지 확인
                img_src_xpath = '/html/body/main/div[1]/div/div/div'
                slide = self.selenium.wait('xpath', img_src_xpath)
                stop_moving_slide_banner()
                return get_current_banner_image_name(slide), slide

            is_url_click_dict = {}

            def check_elements_clickable(slide_url, element): # elements가 클릭이 가능하면 True 아니면 False
                if is_url_click_dict.get(slide_url, False): # key error 방지 위해 기본값 설정
                    return
                is_url_click_dict[slide_url] = False
                try:
                    element.click()
                    res = self.driver.execute_script("return document.readyState;")
                    is_url_click_dict[slide_url] = True
                    self.assertEqual(res, 'complete', msg="Tc021: 페이지 로드 실패")
                    self.driver.back()
                except Exception as e:
                    LOGGER.warning(e)

            if not is_button_exist():
                LOGGER.info("Tc021: 여러 개의 슬라이드 배너가 존재하지 않음")
                return

            stop_moving_slide_banner()

            current_url, slide_elements = get_current_slide_banner_url_after_click()
            default_url = current_url # default_url은 고정된 기본값

            # check_elements_clickable(slide_url, element)

            expected = True

            while True:
                after_url, slide_elements = get_current_slide_banner_url_after_click()
                check_elements_clickable(after_url, slide_elements) # 클릭이 가능하면 클릭 후, 페이지 확인

                if current_url == after_url:
                    LOGGER.info("Tc021: (%s) 같은 슬라이드 배너 존재하여 재클릭! url: %s", LANG, after_url)
                    after_url, slide_elements = get_current_slide_banner_url_after_click()
                    if current_url == after_url:
                        click_count = 3
                        is_changed = False
                        LOGGER.info("Tc021: (%s) 알 수 없는 오류가 의심되어 최대 %d회 다음 슬라이드 버튼 클릭 진행", LANG, click_count)
                        for _ in range(click_count):
                            after_url, slide_elements = get_current_slide_banner_url_after_click()

                            if current_url != after_url:
                                is_changed = True
                                break

                        if not is_changed:
                            LOGGER.warning("Tc021: (%s) 다른 슬라이드 배너가 존재하지 않음! url: %s", LANG, after_url)
                            expected = False
                            break # 실패일때 멈추는 부분

                    elif current_url != after_url:
                        LOGGER.info("Tc021: (%s) 현재 url / 클릭 후 url 비교: 다름", LANG)
                        current_url = after_url

                elif current_url != after_url:
                    current_url = after_url

                if default_url == current_url:
                    LOGGER.info("Tc021: (%s) 기본 url / 현재 url 비교: 동일", LANG)
                    break # 성공일때 멈추는 부분

            self.assertTrue(expected, msg='Tc021: slide banner - test is fail')
            LOGGER.info("Tc021: (%s) main slide banner '%s' - test is pass", LANG, expected)
        
        self.check_by_lang(Tc021)

    def test_Tc022_Tc027(self): # 메인페이지 뉴스 노출 확인
        """뉴스 기사가 노출되는지 확인하고, 클릭시 해당 기사 페이지로 이동 되는지 확인"""
        def Tc022_Tc027(LANG, **kwargs):
            first_news_image_xpath = "//div[@class='main_block01']//div[1]//a[1]//div[1]//img[1]" # /html/body/main/div[2]/div[1]/div[1]/div[1]/a/div[1]/img
            first_news_image = self.selenium.wait('xpath', first_news_image_xpath)
            first_news_image_src = first_news_image.get_attribute('src')
            first_news_image.click()

            linkpage_news_image_xpath = "//img[@class='attachment-eye-catch size-eye-catch wp-post-image']" # /html/body/main/article/div/div[1]/img
            linkpage_news_image = self.selenium.wait('xpath', linkpage_news_image_xpath)
            linkpage_news_src = linkpage_news_image.get_attribute('src')

            self.assertEqual(first_news_image_src, linkpage_news_src, msg=(f'Tc022: expected value = {first_news_image_src}, result = {linkpage_news_src}')) # 검증
            LOGGER.info("Tc022: (%s) main page first_news_image url '%s' - test is pass", LANG, first_news_image_src)
            self.selenium.driver.back()

            first_news_date_xpath = '/html/body/main/div[2]/div[1]/div[1]/div[1]/a/div[2]/div[1]' # "//div[contains(text(),'2018.08.08')]"
            first_news_date = self.selenium.wait('xpath', first_news_date_xpath)
            first_news_date_text = first_news_date.text
            first_news_date.click()

            linkpage_news_date_xpath = "//div[@class='article_outline_date']"
            linkpage_news_date = self.selenium.wait('xpath', linkpage_news_date_xpath)
            linkpage_news_date_text = linkpage_news_date.text

            self.assertEqual(first_news_date_text, linkpage_news_date_text, msg=(f'Tc023: expected value = {first_news_date_text}, result = {linkpage_news_date_text}')) # 검증
            LOGGER.info("Tc023: (%s) main page first_news_date '%s' - test is pass", LANG, first_news_date_text)
            self.selenium.driver.back()

            first_news_headline_xpath = '/html/body/main/div[2]/div[1]/div[1]/div[1]/a/div[2]/div[3]/p' # "//p[contains(text(),'2')]"
            first_news_headline = self.selenium.wait('xpath', first_news_headline_xpath)
            first_news_headline_text = first_news_headline.text
            first_news_headline.click()

            linkpage_news_headline_xpath = '/html/body/main/article/div/div[2]/div[1]/div/div[3]/p' # "//div[@class='article_outline_text']//p[contains(text(),'2')]"
            linkpage_news_headline = self.selenium.wait('xpath', linkpage_news_headline_xpath)
            linkpage_news_headline_text = linkpage_news_headline.text

            self.assertEqual(first_news_headline_text, linkpage_news_headline_text, msg=(f'Tc024: expected value = {first_news_headline_text}, result = {linkpage_news_headline_text}')) # 검증
            LOGGER.info("Tc024: (%s) main page first_news_headline_text '%s' - test is pass", LANG, first_news_headline_text)
            self.selenium.driver.back()

            second_news_image_xpath = "//div[@class='clearfix']//div[2]//a[1]//div[1]//img[1]"    # /html/body/main/div[2]/div[1]/div[1]/div[2]/a/div[1]/img
            second_news_image = self.selenium.wait('xpath', second_news_image_xpath)
            second_news_image_src = second_news_image.get_attribute('src')
            second_news_image.click()

            linkpage_news_image_xpath = "//img[@class='attachment-eye-catch size-eye-catch wp-post-image']" # /html/body/main/article/div/div[1]/img
            linkpage_news_image = self.selenium.wait('xpath', linkpage_news_image_xpath)
            linkpage_news_src = linkpage_news_image.get_attribute('src')

            self.assertEqual(second_news_image_src, linkpage_news_src, msg=(f'Tc025: expected value = {second_news_image_src}, result = {linkpage_news_src}')) # 검증
            LOGGER.info("Tc025: (%s) main page second_news_image url '%s' - test is pass", LANG, second_news_image_src)
            self.selenium.driver.back()

            second_news_date_xpath = '/html/body/main/div[2]/div[1]/div[1]/div[2]/a/div[2]/div[1]' # "//div[contains(text(),'2017.12.22')]"
            second_news_date = self.selenium.wait('xpath', second_news_date_xpath)
            second_news_date_text = second_news_date.text
            second_news_date.click()

            linkpage_news_date_xpath = "//div[@class='article_outline_date']"
            linkpage_news_date = self.selenium.wait('xpath', linkpage_news_date_xpath)
            linkpage_news_date_text = linkpage_news_date.text

            self.assertEqual(second_news_date_text, linkpage_news_date_text, msg=(f'Tc026: expected value = {second_news_date_text}, result = {linkpage_news_date_text}'))
            LOGGER.info("Tc026: (%s) main page second_news_date '%s' - test is pass", LANG, second_news_date_text)
            self.selenium.driver.back()

            second_news_headline_xpath = '/html/body/main/div[2]/div[1]/div[1]/div[2]/a/div[2]/div[3]/p' # "//p[contains(text(),'35')]"
            second_news_headline = self.selenium.wait('xpath', second_news_headline_xpath)
            second_news_headline_text = second_news_headline.text
            second_news_headline.click()

            linkpage_news_headline_xpath = '/html/body/main/article/div/div[2]/div[1]/div/div[3]/p' # / "/p[contains(text(),'35')]"
            linkpage_news_headline = self.selenium.wait('xpath', linkpage_news_headline_xpath)
            linkpage_news_headline_text = linkpage_news_headline.text

            self.assertEqual(second_news_headline_text, linkpage_news_headline_text, msg=(f'Tc027: expected value = {second_news_headline_text}, result = {linkpage_news_headline_text}')) # 검증
            LOGGER.info("Tc027: (%s) main page second_news_headline '%s' - test is pass", LANG, second_news_headline_text)

        self.check_by_lang(Tc022_Tc027)

    def test_Tc028(self): # SNS 배너 확인
        """SNS 이미지가 노출되는지 확인, 해당 부분 클릭시 관련 SNS 사이트 새창 띄우는지 확인"""
        def Tc028(LANG, **kwargs):
            facebook_benner_xpath = "//li[@class='main_block02_list_item slick-slide slick-current slick-active']//a//img"

            # 전체를 다 가지고 온 다음 -> for문으로 돌린다.

            self.selenium.wait('xpath', facebook_benner_xpath).click() # 페이스북 배너 클릭

            expected_xpath = "//a[@class='_2wmb']" # facebook 경로
            self.selenium.driver.switch_to.window(self.selenium.driver.window_handles[-1])

            el = self.selenium.wait('xpath', expected_xpath)

            # expected_xpath_by_domain_dict = {'facebook' : "//a[@class='_2wmb']", "instagram" : "//h2[contains(@class,'')]", "twitter" : " "}

            if not el:
                LOGGER.warning("존재하지 않는 경로, 다른 SNS 사이트 접속")
                expected_xpath = "//h2[contains(@class,'')]" # instagram 경로, JP 한정
                el = self.selenium.wait('xpath', expected_xpath)

            result_title = el.text # facebook 페이지 특정 text 가져옴
            expected_title = 'pokopang.info'
            self.assertIn(expected_title, result_title, msg=(f'Tc028: expected title = {expected_title}, result = {result_title}')) # 검증
            LOGGER.info("Tc028: (%s) SNS benner link '%s' - test is pass", LANG, result_title)
            self.selenium.driver.close()
            self.selenium.driver.switch_to.window(self.selenium.driver.window_handles[0])
            time.sleep(1)
        
        self.check_by_lang(Tc028)

    def test_Tc029_Tc031(self): # Tc021: Artwork, Video, Webcomic 부분
        """Artwork, video, webcomic 노출 여부 확인, 컨텐츠별 각각 클릭시 페이지 이동 가능한지 확인"""
        def Tc029_Tc031(LANG, **kwargs):
            contents_list = ['Artwork', 'Video', 'Webcomic'] # contents 리스트
            for index, expected_value in enumerate(contents_list):
                contents = f'/html/body/main/div[2]/div[2]/ul/li[{index+1}]/a/div/img'
                self.selenium.wait('xpath', contents).click()
                time.sleep(1)
                if expected_value == 'Artwork':
                    expected_xpath = '/html/body/div[3]/div[1]/div[2]/div[2]/div[1]/div/div[2]/span'
                    artwork_result = self.selenium.wait('xpath', expected_xpath).text
                    self.assertEqual(expected_value, artwork_result, msg=(f'Tc029: expected value = {expected_value}, result = {artwork_result}')) # 검증
                    LOGGER.info("Tc029: (%s) contents menu '%s' - test is pass", LANG, artwork_result)
                    self.selenium.wait('xpath', '/html/body/div[3]/div[1]/div[2]/div[2]/button[4]').click()

                elif expected_value == 'Video':
                    # self.selenium.driver.switch_to.frame('1595226670711')
                    expected_xpath = '/html/body/div[3]/div[1]/div[2]/div[2]/div[1]/iframe'
                    el = self.selenium.wait('xpath', expected_xpath)
                    self.assertIsNotNone(el, msg='Tc030: video is not exist')
                    LOGGER.info("Tc030: (%s) contents menu '%s' - test is pass", LANG, expected_value)
                    self.selenium.wait('xpath', '/html/body/div[3]/div[1]/div[2]/div[2]/button[4]').click()

                elif expected_value == 'Webcomic':
                    self.selenium.driver.switch_to.window(self.selenium.driver.window_handles[-1])
                    expected_xpath = '/html/body/div/nav/div/div/div[2]/h6'
                    webcomic_result = self.selenium.wait('xpath', expected_xpath).text[:7]
                    self.assertEqual('Episode', webcomic_result, msg=(f'Tc031: expected value = Episode, result = {webcomic_result}')) # 검증
                    LOGGER.info("Tc031: (%s) contents menu '%s(%s)' - test is pass", LANG, expected_value, webcomic_result)
                    self.selenium.driver.back()
                time.sleep(1)

        self.check_by_lang(Tc029_Tc031)

    def test_Tc032(self): # See more 버튼 검증
        """See more 버튼 노출 여부 확인, 클릭시 컨텐츠 페이지로 이동하는지 확인"""
        def Tc032(LANG, **kwargs):
            see_more_xpath = "//a[@class='btn']" # /html/body/main/div[2]/div[2]/div/a
            self.selenium.wait('xpath', see_more_xpath).click()
            expected_xpath = "//li[contains(text(),'CONTENTS')]" # '/html/body/main/div[1]/ul/li[2]'
            menu = self.selenium.wait('xpath', expected_xpath)
            result = menu.text
            expected_value = 'CONTENTS'

            self.assertEqual(expected_value, result, msg=(f'Tc032: expected value = {expected_value}, result = {result}')) # 검증
            LOGGER.info("Tc032: (%s) 'See more' button link: '%s' - test is pass", LANG, result) # 검증

        self.check_by_lang(Tc032)

    def test_Tc033_Tc036(self): # 푸터 부분 검증
        """푸터 메뉴 ABOUT, NEWS, CONTENTS, CONTACT xpath로 각각 검증"""
        def Tc033_Tc036(LANG, **kwargs):
            expected_footer_list = ['ABOUT', 'NEWS', 'CONTACT']

            contents_xpath = '/html/body/footer/div[1]/div/div[1]/div/ul[2]/li[2]/a' # //li[@id='menu-item-587']//a[contains(text(),'CONTENTS')]

            result = self.check_menu_list(expected_footer_list, 'footer', LANG)
            self.assertTrue(result, msg='TC_menu_check - test is fail')
            LOGGER.info("Tc033~035: (%s) footer menu '%s' - test is pass", LANG, result) # 검증

            expected_xpath = '/html/body/main/div[1]/ul/li[2]'
            contents = self.selenium.wait('xpath', contents_xpath)
            expected_value = contents.text
            contents.click()
            menu = self.selenium.wait('xpath', expected_xpath)
            result = menu.text.split(' ')[0]
            self.assertEqual(expected_value, result, msg=(f'Tc036: expected value = {expected_value}, result = {result}'))
            LOGGER.info("Tc036: (%s) footer menu '%s' - test is pass", LANG, result)
        
        self.check_by_lang(Tc033_Tc036)

    def test_Tc037(self): # 하단 treenod 로고 버튼 검증
        """최하단 treenod 로고 노출 여부 확인, 클릭시 트리노드 홈페이지 이동 확인"""
        def Tc037(LANG, **kwargs):
            treenod_xpath = "//p[@class='copyright']//a//img" # '/html/body/footer/div[2]/div/p/a/img' # 하단 treenod 로고 버튼 xpath
            self.selenium.wait('xpath', treenod_xpath).click() # 버튼 click

            self.selenium.driver.switch_to.window(self.selenium.driver.window_handles[-1]) # 새로 띄운 창으로 전환
            time.sleep(1)

            title_xpath = '/html/head/title' # 새로 열린 창의 타이틀 xpath
            el = self.selenium.wait('xpath', title_xpath)
            result_title = el.get_attribute('innerText') # 타이틀 속성 중, 텍스트 가져옴
            expected_title = 'Treenod | 트리노드' # 타이틀 스트링 기대값
            self.assertEqual(expected_title, result_title, msg=(f'Tc037: expected title = {expected_title}, result = {result_title}')) # 검증
            LOGGER.info("Tc037: (%s) 'treenod' link page's title: '%s' - test is pass", LANG, result_title)
        
        self.check_by_lang(Tc037)

    def test_Tc038_Tc039(self): # 스크롤 다운 후, top 버튼 노출 확인 및 검증하고 클릭하여 Top으로 이동
        """스크롤 이동하여 페이지 최하단 이동, 스크롤 바닥에서 top 버튼 검증"""
        def Tc038_Tc039(LANG, **kwargs):
            # https://sometimes-n.tistory.com/22 참고사이트
            y_offset = int(self.driver.execute_script("return window.pageYOffset;")) # 현재 보여지는 페이지 최상단 location 의 Y offset 값
            if y_offset != 0: # y_offset 값이 0 이 아닌 경우, 테스트 불가능 상황 처리
                LOGGER.warning("Tc038~039: (%s) test is impossible", LANG)
                self.assertTrue(False)

            self.selenium.scroll_down() # selenium.scroll_down 함수 이용, 페이지 최하단 이동

            total_height = int(self.driver.execute_script("return document.body.scrollHeight;")) # 현재 페이지 전체 크기
            scroll_height = int(self.driver.execute_script("return window.innerHeight;")) # 현재 보이는 화면 크기

            y_offset = int(self.driver.execute_script("return window.pageYOffset;")) # 스크롤 최하단 이동 후, 현재 페이지 Y offset 값 다시 가져옴
            if y_offset != (total_height - scroll_height): # 현재 y offset 값이 전체 높이에서 스크롤 높이를 뺀 수치와 같지 않다면, 스크롤에 문제가 되는 상황
                LOGGER.warning("Tc038~039: (%s) test is impossible", LANG)
                self.assertTrue(False)

            top_button_xpath = "//a[@id='js-pagetop-link']" # 탑버튼(∧) xpath
            top_button = self.selenium.wait('xpath', top_button_xpath)
            top_button.click() # 버튼 클릭하여 최상단 이동
            self.assertTrue(top_button, msg="top_botton is not exist")
            time.sleep(1)
            y_offset = int(self.driver.execute_script("return window.pageYOffset;"))
            if y_offset == 0:
                self.assertTrue(True, msg="y_offset != 0")
                LOGGER.info("Tc038~039: (%s) 'scroll_down + top_button' - test is pass", LANG)

        self.check_by_lang(Tc038_Tc039)

    def test_Tc040(self): # 포코팡닷컴 한국어 페이지 오픈
        """웹 브라우저 > 포코팡닷컴 접속"""
        print("=================================================== ABOUT PAGE ===================================================")
        def Tc040(LANG, **kwargs):
            result = kwargs['result']
            self.assertTrue(result, msg='Tc040: open url - test is fail')
            LOGGER.info("Tc040: (%s) open url '%s'- test is pass", LANG, result)

        self.about_check_by_lang(Tc040)

    def test_Tc041(self): # 현재 페이지 언어 감지 - 뉴스 헤드라인 부분으로 검증
        """language_check 모듈로 현재 웹페이지 언어 감지"""
        def Tc041(LANG, **kwargs):
            body_main_xpath = "/html/body/main" # 페이지 text xpath 
            body_main_text = self.selenium.get_text('xpath', body_main_xpath) # 컨텐츠에 있는 텍스트 모두 저장
            result_list = language_check.check(body_main_text) # language_check 모듈 > 함수 사용하여 컨텐츠 텍스트 언어 감지

            if len(result_list) >= 2: # 2가지 이상 언어가 섞여 있을 경우의 처리
                LOGGER.warning("Tc041: (%s) 이 페이지 언어는 %s가 동일 비율로 섞여 있어 추가 확인이 필요합니다.", LANG, result_list)

            elif len(result_list) == 0: # 언어 판단 불가능할 경우의 처리
                LOGGER.warning("Tc041: (%s) 이 페이지 언어는 판단 가능한 언어가 포함되지 않아 %s 추가 확인이 필요합니다.", LANG, result_list)

            elif 'ko' in result_list: # 한국어 비율이 높을 경우의 처리
                LOGGER.info("Tc041: (%s) 이 페이지는 한국어%s 페이지일 가능성이 높습니다.", LANG, result_list)

            elif 'en' in result_list: # 영어 비율이 높을 경우의 처리
                LOGGER.info("Tc041: (%s) 이 페이지는 English%s 페이지일 가능성이 높습니다.", LANG, result_list)

            elif 'ja' in result_list: # 일본어 비율이 높을 경우의 처리
                LOGGER.info("Tc041: (%s) 이 페이지는 日本語%s 페이지일 가능성이 높습니다.", LANG, result_list)

            self.assertIsNotNone(result_list, msg='Tc002: language_check - test is fail')
            LOGGER.info("Tc041: (%s) language_check = %s - test is pass", LANG, result_list)

        self.about_check_by_lang(Tc041)

    def test_Tc042(self): # 메인페이지 > 탑 메뉴 'POKOPANG!' 선택 > 탭 타이틀 텍스트 비교
        """탑 메뉴 > POKOPANG! 클릭 후, 탭 타이틀 비교"""
        def Tc042(LANG, **kwargs):
            pokopang_xpath = "//a[@class='over']//img" # 좌측 상단 POKOPANG! xpath
            pokopang = self.selenium.wait('xpath', pokopang_xpath)
            pokopang.click() # 'POKOPANG!' 버튼 클릭
            title_xpath = "//title[contains(text(),'POKOPANG!')]" # title xpath
            title = self.selenium.wait('xpath', title_xpath)

            result_title = title.get_attribute('innerText') # title text 가져옴(innerText or textContent)
            expected_title = 'POKOPANG!' # 타이틀 기대값

            self.assertIn(expected_title, result_title, msg=(f'Tc042: expected title = {expected_title}, result = {result_title}')) # 검증
            LOGGER.info("Tc042: (%s) 'POKOPANG!' link page's title: '%s' - test is pass", LANG, result_title)

        self.about_check_by_lang(Tc042)

    def test_Tc043_Tc046(self): # 탑 메뉴 xpath로 찾아 클릭하여 해당 페이지 이동, menu path 검증
        """탑 메뉴 > ABOUT, NEWS, CONTENTS, CONTACT xpath 로 가져와서 text 비교"""
        def Tc043_Tc046(LANG, **kwargs):
            expected_top_list = ['ABOUT', 'NEWS', 'CONTENTS', 'CONTACT'] # 탑 메뉴 list

            result = self.check_menu_list(expected_top_list, 'top', LANG)
            self.assertTrue(result, msg='TC_menu_check - test is fail')
            LOGGER.info("Tc043~046: (%s) top menu '%s' - test is pass", LANG, result)

        self.about_check_by_lang(Tc043_Tc046)

    def test_Tc047(self): # 탑 메뉴 > 햄버거 선택 후, 추가 노출되는 메뉴 중 HOME 검증
        """햄버거 버튼 하위 메뉴 HOME을 타이틀명으로 검증"""
        def Tc047(LANG, **kwargs):
            hamburger = "//li[@id='js-sitemenuBtn']" # 햄버거 xpath
            self.selenium.wait('xpath', hamburger).click() # 햄버거 버튼 클릭
            home = '/html/body/header/div[3]/div/ul/li[1]/a' # HOME xpath
            self.selenium.wait('xpath', home).click() # HOME 메뉴 클릭

            title_xpath = "//title[contains(text(),'POKOPANG!')]"
            title = self.selenium.wait('xpath', title_xpath) # 타이틀 속성 지정

            result_title = title.get_attribute('innerText') # title의 text 가져옴, innerText 대신 textContent 도 결과 동일
            expected_title = 'POKOPANG!' # 타이틀 스트링 기대값

            self.assertIn(expected_title, result_title, msg=(f'Tc047: expected title = {expected_title}, result = {result_title}')) # 검증
            LOGGER.info("Tc047: (%s) hamburger menu 'HOME(%s)' - test is pass", LANG, result_title)
        
        self.about_check_by_lang(Tc047)

    def test_Tc048_Tc051(self): # 탑 메뉴 > 햄버거 선택 후, 추가 노출되는 메뉴 중 HOME을 제외한 나머지 검증
        """햄버거 버튼 하위 메뉴 ABOUT, NEWS, CONTENTS, CONTACT를 xpath로 검증"""
        def Tc048_Tc051(LANG, **kwargs):
            expected_hamburger_list = ['ABOUT', 'NEWS', 'CONTENTS', 'CONTACT']

            result = self.check_menu_list(expected_hamburger_list, 'hamburger', LANG)
            self.assertTrue(result, msg='TC_menu_check - test is fail')
            LOGGER.info("Tc048~051: (%s) hamburger menu '%s' - test is pass", LANG, result) # 검증

        self.about_check_by_lang(Tc048_Tc051)

    def test_Tc052_Tc054(self): # 탑 메뉴 > 햄버거 선택 후, 추가 노출되는 메뉴 중 언어 변경 검증
        """햄버거 버튼 하위 메뉴 English, 日本語, 한국어 html tag_name lang 으로 검증"""
        def Tc052_Tc054(LANG, **kwargs):
            expected_language_list = ['en-US', 'ja', 'ko-KR']

            for index, expected_lang in enumerate(expected_language_list):
                self.selenium.wait('xpath', '/html/body/header/div[1]/div/ul/li[2]').click() # 햄버거 버튼 클릭
                xpath = f'/html/body/header/div[3]/div/div/ul/li[{index+1}]' # 각 메뉴 xpath

                self.selenium.wait('xpath', xpath).click() # 각 메뉴 클릭 실행
                time.sleep(1)

                result_lang = self.selenium.wait('tag_name', 'html').get_attribute('lang') # 각 언어 페이지마다 html lang 값 가져옴

                if result_lang == 'en-US': # 영어 검증
                    self.assertEqual(expected_lang, result_lang, msg=(f'Tc052: expected title = {expected_lang}, result = {result_lang}'))
                    LOGGER.info("Tc052: (%s) hamburger menu 'English(%s)' - test is pass", LANG, result_lang)
                    time.sleep(1)

                elif result_lang == 'ja': # 일본어 검증
                    self.assertEqual(expected_lang, result_lang, msg=(f'Tc053: expected title = {expected_lang}, result = {result_lang}'))
                    LOGGER.info("Tc053: (%s) hamburger menu '日本語(%s)' - test is pass", LANG, result_lang)
                    time.sleep(1)

                elif result_lang == 'ko-KR': # 한국어 검증
                    self.assertEqual(expected_lang, result_lang, msg=(f'Tc054: expected title = {expected_lang}, result = {result_lang}'))
                    LOGGER.info("Tc054: (%s) hamburger menu '한국어(%s)' - test is pass", LANG, result_lang)
                    time.sleep(1)

        self.about_check_by_lang(Tc052_Tc054)

    def test_Tc055(self): # 메인 페이지 > 이미지 검증
        """페이지 전체 이미지 로드 되는지 확인"""
        def Tc055(LANG, **kwargs):
            image_load = self.selenium.is_image_loaded()
            self.assertTrue(image_load, msg='Tc055: image_load - test is fail')
            LOGGER.info("Tc055: (%s) page's image load '%s' - test is pass", LANG, image_load)
        
        self.about_check_by_lang(Tc055)

    def test_Tc056_Tc059(self): # 푸터 부분 검증
        """푸터 메뉴 ABOUT, NEWS, CONTENTS, CONTACT xpath로 각각 검증"""
        def Tc056_Tc059(LANG, **kwargs):
            expected_footer_list = ['ABOUT', 'NEWS', 'CONTACT']

            contents_xpath = '/html/body/footer/div[1]/div/div[1]/div/ul[2]/li[2]/a' # //li[@id='menu-item-587']//a[contains(text(),'CONTENTS')]

            result = self.check_menu_list(expected_footer_list, 'footer', LANG)
            self.assertTrue(result, msg='TC_menu_check - test is fail')
            LOGGER.info("Tc056~058: (%s) footer menu '%s' - test is pass", LANG, result) # 검증

            expected_xpath = '/html/body/main/div[1]/ul/li[2]'
            contents = self.selenium.wait('xpath', contents_xpath)
            expected_value = contents.text
            contents.click()
            menu = self.selenium.wait('xpath', expected_xpath)
            result = menu.text.split(' ')[0]
            self.assertEqual(expected_value, result, msg=(f'Tc059: expected value = {expected_value}, result = {result}'))
            LOGGER.info("Tc059: (%s) footer menu '%s' - test is pass", LANG, result)
        
        self.about_check_by_lang(Tc056_Tc059)

    def test_Tc060(self): # 하단 treenod 로고 버튼 검증
        """최하단 treenod 로고 노출 여부 확인, 클릭시 트리노드 홈페이지 이동 확인"""
        def Tc060(LANG, **kwargs):
            treenod_xpath = "//p[@class='copyright']//a//img" # '/html/body/footer/div[2]/div/p/a/img' # 하단 treenod 로고 버튼 xpath
            self.selenium.wait('xpath', treenod_xpath).click() # 버튼 click

            self.selenium.driver.switch_to.window(self.selenium.driver.window_handles[-1]) # 새로 띄운 창으로 전환
            time.sleep(1)

            title_xpath = '/html/head/title' # 새로 열린 창의 타이틀 xpath
            el = self.selenium.wait('xpath', title_xpath)
            result_title = el.get_attribute('innerText') # 타이틀 속성 중, 텍스트 가져옴
            expected_title = 'Treenod | 트리노드' # 타이틀 스트링 기대값
            self.assertEqual(expected_title, result_title, msg=(f'Tc060: expected title = {expected_title}, result = {result_title}')) # 검증
            LOGGER.info("Tc060: (%s) 'treenod' link page's title: '%s' - test is pass", LANG, result_title)
        
        self.about_check_by_lang(Tc060)

    def test_Tc061_Tc062(self): # 스크롤 다운 후, top 버튼 노출 확인 및 검증하고 클릭하여 Top으로 이동
        """스크롤 이동하여 페이지 최하단 이동, 스크롤 바닥에서 top 버튼 검증"""
        def Tc061_Tc062(LANG, **kwargs):
            y_offset = int(self.driver.execute_script("return window.pageYOffset;")) # 현재 보여지는 페이지 최상단 location 의 Y offset 값
            if y_offset != 0: # y_offset 값이 0 이 아닌 경우, 테스트 불가능 상황 처리
                LOGGER.warning("Tc061~062: (%s) test is impossible", LANG)
                self.assertTrue(False)

            self.selenium.scroll_down() # selenium.scroll_down 함수 이용, 페이지 최하단 이동

            total_height = int(self.driver.execute_script("return document.body.scrollHeight;")) # 현재 페이지 전체 크기
            scroll_height = int(self.driver.execute_script("return window.innerHeight;")) # 현재 보이는 화면 크기

            y_offset = int(self.driver.execute_script("return window.pageYOffset;")) # 스크롤 최하단 이동 후, 현재 페이지 Y offset 값 다시 가져옴
            if y_offset != (total_height - scroll_height): # 현재 y offset 값이 전체 높이에서 스크롤 높이를 뺀 수치와 같지 않다면, 스크롤에 문제가 되는 상황
                LOGGER.warning("Tc061~062: (%s) test is impossible", LANG)
                self.assertTrue(False)

            top_button_xpath = "//a[@id='js-pagetop-link']" # 탑버튼(∧) xpath
            top_button = self.selenium.wait('xpath', top_button_xpath)
            top_button.click() # 버튼 클릭하여 최상단 이동
            self.assertTrue(top_button, msg="top_botton is not exist")
            time.sleep(1)
            y_offset = int(self.driver.execute_script("return window.pageYOffset;"))
            if y_offset == 0:
                self.assertTrue(True, msg="y_offset != 0")
                LOGGER.info("Tc061~062: (%s) 'scroll_down + top_button' - test is pass", LANG)

        self.about_check_by_lang(Tc061_Tc062)

    def test_Tc063(self):
        def Tc063(LANG, **kwargs):
            self.check_page_main_title('ABOUT', LANG)

        self.about_check_by_lang(Tc063)
    
    def test_Tc064(self):
        def Tc064(LANG, **kwargs):
            body_xpath = "/html/body/main" # 페이지 body text
            result_text = self.selenium.get_text('xpath', body_xpath)
                
            SEARCH_KEYWORD = kwargs['search_keyword']

            self.assertIn(SEARCH_KEYWORD, result_text, msg=(f'Tc064: search_keyword = {SEARCH_KEYWORD}, result = {result_text}')) # 검증
            LOGGER.info("TC064: (%s) page keyword text: '%s' - test is pass", LANG, SEARCH_KEYWORD)

        self.about_check_by_lang(Tc064)

    def test_Tc0065(self): # 포코팡닷컴 한국어 페이지 오픈
        """웹 브라우저 > 포코팡닷컴 접속"""
        print("=================================================== NEWS PAGE ===================================================")
        def Tc065(LANG, **kwargs):
            result = kwargs['result']
            self.assertTrue(result, msg='Tc065: open url - test is fail')
            LOGGER.info("Tc065: (%s) open url '%s'- test is pass", LANG, result)

        self.news_check_by_lang(Tc065)

    def test_Tc066(self): # 현재 페이지 언어 감지 - 뉴스 헤드라인 부분으로 검증
        """language_check 모듈로 현재 웹페이지 언어 감지"""
        def Tc066(LANG, **kwargs):
            body_main_xpath = "/html/body/main" # 페이지 text xpath 
            body_main_text = self.selenium.get_text('xpath', body_main_xpath) # 컨텐츠에 있는 텍스트 모두 저장
            result_list = language_check.check(body_main_text) # language_check 모듈 > 함수 사용하여 컨텐츠 텍스트 언어 감지

            if len(result_list) >= 2: # 2가지 이상 언어가 섞여 있을 경우의 처리
                LOGGER.warning("Tc066: (%s) 이 페이지 언어는 %s가 동일 비율로 섞여 있어 추가 확인이 필요합니다.", LANG, result_list)

            elif len(result_list) == 0: # 언어 판단 불가능할 경우의 처리
                LOGGER.warning("Tc066: (%s) 이 페이지 언어는 판단 가능한 언어가 포함되지 않아 %s 추가 확인이 필요합니다.", LANG, result_list)

            elif 'ko' in result_list: # 한국어 비율이 높을 경우의 처리
                LOGGER.info("Tc066: (%s) 이 페이지는 한국어%s 페이지일 가능성이 높습니다.", LANG, result_list)

            elif 'en' in result_list: # 영어 비율이 높을 경우의 처리
                LOGGER.info("Tc066: (%s) 이 페이지는 English%s 페이지일 가능성이 높습니다.", LANG, result_list)

            elif 'ja' in result_list: # 일본어 비율이 높을 경우의 처리
                LOGGER.info("Tc066: (%s) 이 페이지는 日本語%s 페이지일 가능성이 높습니다.", LANG, result_list)

            self.assertIsNotNone(result_list, msg='Tc066: language_check - test is fail')
            LOGGER.info("Tc066: (%s) language_check = %s - test is pass", LANG, result_list)

        self.news_check_by_lang(Tc066)

    def test_Tc067(self): # 메인페이지 > 탑 메뉴 'POKOPANG!' 선택 > 탭 타이틀 텍스트 비교
        """탑 메뉴 > POKOPANG! 클릭 후, 탭 타이틀 비교"""
        def Tc067(LANG, **kwargs):
            pokopang_xpath = "//a[@class='over']//img" # 좌측 상단 POKOPANG! xpath
            pokopang = self.selenium.wait('xpath', pokopang_xpath)
            pokopang.click() # 'POKOPANG!' 버튼 클릭
            title_xpath = "//title[contains(text(),'POKOPANG!')]" # title xpath
            title = self.selenium.wait('xpath', title_xpath)

            result_title = title.get_attribute('innerText') # title text 가져옴(innerText or textContent)
            expected_title = 'POKOPANG!' # 타이틀 기대값

            self.assertIn(expected_title, result_title, msg=(f'Tc067: expected title = {expected_title}, result = {result_title}')) # 검증
            LOGGER.info("Tc067: (%s) 'POKOPANG!' link page's title: '%s' - test is pass", LANG, result_title)

        self.news_check_by_lang(Tc067)

    def test_Tc068_Tc071(self): # 탑 메뉴 xpath로 찾아 클릭하여 해당 페이지 이동, menu path 검증
        """탑 메뉴 > ABOUT, NEWS, CONTENTS, CONTACT xpath 로 가져와서 text 비교"""
        def Tc068_Tc071(LANG, **kwargs):
            expected_top_list = ['ABOUT', 'NEWS', 'CONTENTS', 'CONTACT'] # 탑 메뉴 list

            result = self.check_menu_list(expected_top_list, 'top', LANG)
            self.assertTrue(result, msg='TC_menu_check - test is fail')
            LOGGER.info("Tc068~071: (%s) top menu '%s' - test is pass", LANG, result)

        self.news_check_by_lang(Tc068_Tc071)

    def test_Tc072(self): # 탑 메뉴 > 햄버거 선택 후, 추가 노출되는 메뉴 중 HOME 검증
        """햄버거 버튼 하위 메뉴 HOME을 타이틀명으로 검증"""
        def Tc072(LANG, **kwargs):
            hamburger = "//li[@id='js-sitemenuBtn']" # 햄버거 xpath
            self.selenium.wait('xpath', hamburger).click() # 햄버거 버튼 클릭
            home = '/html/body/header/div[3]/div/ul/li[1]/a' # HOME xpath
            self.selenium.wait('xpath', home).click() # HOME 메뉴 클릭

            title_xpath = "//title[contains(text(),'POKOPANG!')]"
            title = self.selenium.wait('xpath', title_xpath) # 타이틀 속성 지정

            result_title = title.get_attribute('innerText') # title의 text 가져옴, innerText 대신 textContent 도 결과 동일
            expected_title = 'POKOPANG!' # 타이틀 스트링 기대값

            self.assertIn(expected_title, result_title, msg=(f'Tc072: expected title = {expected_title}, result = {result_title}')) # 검증
            LOGGER.info("Tc072: (%s) hamburger menu 'HOME(%s)' - test is pass", LANG, result_title)
        
        self.news_check_by_lang(Tc072)

    def test_Tc073_Tc076(self): # 탑 메뉴 > 햄버거 선택 후, 추가 노출되는 메뉴 중 HOME을 제외한 나머지 검증
        """햄버거 버튼 하위 메뉴 ABOUT, NEWS, CONTENTS, CONTACT를 xpath로 검증"""
        def Tc073_Tc076(LANG, **kwargs):
            expected_hamburger_list = ['ABOUT', 'NEWS', 'CONTENTS', 'CONTACT']

            result = self.check_menu_list(expected_hamburger_list, 'hamburger', LANG)
            self.assertTrue(result, msg='TC_menu_check - test is fail')
            LOGGER.info("Tc073~076: (%s) hamburger menu '%s' - test is pass", LANG, result) # 검증

        self.news_check_by_lang(Tc073_Tc076)

    def test_Tc077_Tc079(self): # 탑 메뉴 > 햄버거 선택 후, 추가 노출되는 메뉴 중 언어 변경 검증
        """햄버거 버튼 하위 메뉴 English, 日本語, 한국어 html tag_name lang 으로 검증"""
        def Tc077_Tc079(LANG, **kwargs):
            expected_language_list = ['en-US', 'ja', 'ko-KR']

            for index, expected_lang in enumerate(expected_language_list):
                self.selenium.wait('xpath', '/html/body/header/div[1]/div/ul/li[2]').click() # 햄버거 버튼 클릭
                xpath = f'/html/body/header/div[3]/div/div/ul/li[{index+1}]' # 각 메뉴 xpath

                self.selenium.wait('xpath', xpath).click() # 각 메뉴 클릭 실행
                time.sleep(1)

                result_lang = self.selenium.wait('tag_name', 'html').get_attribute('lang') # 각 언어 페이지마다 html lang 값 가져옴

                if result_lang == 'en-US': # 영어 검증
                    self.assertEqual(expected_lang, result_lang, msg=(f'Tc077: expected title = {expected_lang}, result = {result_lang}'))
                    LOGGER.info("Tc077: (%s) hamburger menu 'English(%s)' - test is pass", LANG, result_lang)
                    time.sleep(1)

                elif result_lang == 'ja': # 일본어 검증
                    self.assertEqual(expected_lang, result_lang, msg=(f'Tc078: expected title = {expected_lang}, result = {result_lang}'))
                    LOGGER.info("Tc078: (%s) hamburger menu '日本語(%s)' - test is pass", LANG, result_lang)
                    time.sleep(1)

                elif result_lang == 'ko-KR': # 한국어 검증
                    self.assertEqual(expected_lang, result_lang, msg=(f'Tc079: expected title = {expected_lang}, result = {result_lang}'))
                    LOGGER.info("Tc079: (%s) hamburger menu '한국어(%s)' - test is pass", LANG, result_lang)
                    time.sleep(1)

        self.news_check_by_lang(Tc077_Tc079)

    def test_Tc080(self): # 메인 페이지 > 이미지 검증
        """페이지 전체 이미지 로드 되는지 확인"""
        def Tc080(LANG, **kwargs):
            image_load = self.selenium.is_image_loaded()
            self.assertTrue(image_load, msg='Tc080: image_load - test is fail')
            LOGGER.info("Tc080: (%s) page's image load '%s' - test is pass", LANG, image_load)
        
        self.news_check_by_lang(Tc080)

    def test_Tc081_Tc084(self): # 푸터 부분 검증
        """푸터 메뉴 ABOUT, NEWS, CONTENTS, CONTACT xpath로 각각 검증"""
        def Tc081_Tc084(LANG, **kwargs):
            expected_footer_list = ['ABOUT', 'NEWS', 'CONTACT']

            contents_xpath = '/html/body/footer/div[1]/div/div[1]/div/ul[2]/li[2]/a' # //li[@id='menu-item-587']//a[contains(text(),'CONTENTS')]

            result = self.check_menu_list(expected_footer_list, 'footer', LANG)
            self.assertTrue(result, msg='TC_menu_check - test is fail')
            LOGGER.info("Tc081~083: (%s) footer menu '%s' - test is pass", LANG, result) # 검증

            expected_xpath = '/html/body/main/div[1]/ul/li[2]'
            contents = self.selenium.wait('xpath', contents_xpath)
            expected_value = contents.text
            contents.click()
            menu = self.selenium.wait('xpath', expected_xpath)
            result = menu.text.split(' ')[0]
            self.assertEqual(expected_value, result, msg=(f'Tc084: expected value = {expected_value}, result = {result}'))
            LOGGER.info("Tc084: (%s) footer menu '%s' - test is pass", LANG, result)
        
        self.news_check_by_lang(Tc081_Tc084)

    def test_Tc085(self): # 하단 treenod 로고 버튼 검증
        """최하단 treenod 로고 노출 여부 확인, 클릭시 트리노드 홈페이지 이동 확인"""
        def Tc085(LANG, **kwargs):
            treenod_xpath = "//p[@class='copyright']//a//img" # '/html/body/footer/div[2]/div/p/a/img' # 하단 treenod 로고 버튼 xpath
            self.selenium.wait('xpath', treenod_xpath).click() # 버튼 click

            self.selenium.driver.switch_to.window(self.selenium.driver.window_handles[-1]) # 새로 띄운 창으로 전환
            time.sleep(1)

            title_xpath = '/html/head/title' # 새로 열린 창의 타이틀 xpath
            el = self.selenium.wait('xpath', title_xpath)
            result_title = el.get_attribute('innerText') # 타이틀 속성 중, 텍스트 가져옴
            expected_title = 'Treenod | 트리노드' # 타이틀 스트링 기대값
            self.assertEqual(expected_title, result_title, msg=(f'Tc085: expected title = {expected_title}, result = {result_title}')) # 검증
            LOGGER.info("Tc085: (%s) 'treenod' link page's title: '%s' - test is pass", LANG, result_title)
        
        self.news_check_by_lang(Tc085)

    def test_Tc086_Tc087(self): # 스크롤 다운 후, top 버튼 노출 확인 및 검증하고 클릭하여 Top으로 이동
        """스크롤 이동하여 페이지 최하단 이동, 스크롤 바닥에서 top 버튼 검증"""
        def Tc086_Tc087(LANG, **kwargs):
            y_offset = int(self.driver.execute_script("return window.pageYOffset;")) # 현재 보여지는 페이지 최상단 location 의 Y offset 값
            if y_offset != 0: # y_offset 값이 0 이 아닌 경우, 테스트 불가능 상황 처리
                LOGGER.warning("Tc086~087: (%s) test is impossible", LANG)
                self.assertTrue(False)

            self.selenium.scroll_down() # selenium.scroll_down 함수 이용, 페이지 최하단 이동

            total_height = int(self.driver.execute_script("return document.body.scrollHeight;")) # 현재 페이지 전체 크기
            scroll_height = int(self.driver.execute_script("return window.innerHeight;")) # 현재 보이는 화면 크기

            y_offset = int(self.driver.execute_script("return window.pageYOffset;")) # 스크롤 최하단 이동 후, 현재 페이지 Y offset 값 다시 가져옴
            if y_offset != (total_height - scroll_height): # 현재 y offset 값이 전체 높이에서 스크롤 높이를 뺀 수치와 같지 않다면, 스크롤에 문제가 되는 상황
                LOGGER.warning("Tc086~087: (%s) test is impossible", LANG)
                self.assertTrue(False)

            top_button_xpath = "//a[@id='js-pagetop-link']" # 탑버튼(∧) xpath
            top_button = self.selenium.wait('xpath', top_button_xpath)
            top_button.click() # 버튼 클릭하여 최상단 이동
            self.assertTrue(top_button, msg="top_botton is not exist")
            time.sleep(1)
            y_offset = int(self.driver.execute_script("return window.pageYOffset;"))
            if y_offset == 0:
                self.assertTrue(True, msg="y_offset != 0")
                LOGGER.info("Tc086~087: (%s) 'scroll_down + top_button' - test is pass", LANG)

        self.news_check_by_lang(Tc086_Tc087)

    def test_Tc088(self):
        def Tc088(LANG, **kwargs):
            self.check_page_main_title('NEWS', LANG)

        self.news_check_by_lang(Tc088)
    
    def test_Tc089(self):
        def Tc089(LANG, **kwargs):
            body_xpath = "/html/body/main" # 페이지 body text
            result_text = self.selenium.get_text('xpath', body_xpath)
                
            SEARCH_KEYWORD = kwargs['search_keyword']

            self.assertIn(SEARCH_KEYWORD, result_text, msg=(f'Tc089: search_keyword = {SEARCH_KEYWORD}, result = {result_text}')) # 검증
            LOGGER.info("TC089: (%s) page keyword text: '%s' - test is pass", LANG, SEARCH_KEYWORD)

        self.news_check_by_lang(Tc089)

    def test_Tc090(self): # 포코팡닷컴 한국어 페이지 오픈
        """웹 브라우저 > 포코팡닷컴 접속"""
        print("=================================================== CONTENTS PAGE ===================================================")
        def Tc090(LANG, **kwargs):
            result = kwargs['result']
            self.assertTrue(result, msg='Tc090: open url - test is fail')
            LOGGER.info("Tc090: (%s) open url '%s'- test is pass", LANG, result)

        self.contents_check_by_lang(Tc090)

    def test_Tc091(self): # 현재 페이지 언어 감지 - 뉴스 헤드라인 부분으로 검증
        """language_check 모듈로 현재 웹페이지 언어 감지"""
        def Tc091(LANG, **kwargs):
            body_main_xpath = "/html/body/main" # 페이지 text xpath 
            body_main_text = self.selenium.get_text('xpath', body_main_xpath) # 컨텐츠에 있는 텍스트 모두 저장
            result_list = language_check.check(body_main_text) # language_check 모듈 > 함수 사용하여 컨텐츠 텍스트 언어 감지

            if len(result_list) >= 2: # 2가지 이상 언어가 섞여 있을 경우의 처리
                LOGGER.warning("Tc091: (%s) 이 페이지 언어는 %s가 동일 비율로 섞여 있어 추가 확인이 필요합니다.", LANG, result_list)

            elif len(result_list) == 0: # 언어 판단 불가능할 경우의 처리
                LOGGER.warning("Tc091: (%s) 이 페이지 언어는 판단 가능한 언어가 포함되지 않아 %s 추가 확인이 필요합니다.", LANG, result_list)

            elif 'ko' in result_list: # 한국어 비율이 높을 경우의 처리
                LOGGER.info("Tc091: (%s) 이 페이지는 한국어%s 페이지일 가능성이 높습니다.", LANG, result_list)

            elif 'en' in result_list: # 영어 비율이 높을 경우의 처리
                LOGGER.info("Tc091: (%s) 이 페이지는 English%s 페이지일 가능성이 높습니다.", LANG, result_list)

            elif 'ja' in result_list: # 일본어 비율이 높을 경우의 처리
                LOGGER.info("Tc091: (%s) 이 페이지는 日本語%s 페이지일 가능성이 높습니다.", LANG, result_list)

            self.assertIsNotNone(result_list, msg='Tc002: language_check - test is fail')
            LOGGER.info("Tc091: (%s) language_check = %s - test is pass", LANG, result_list)

        self.contents_check_by_lang(Tc091)

    def test_Tc092(self): # 메인페이지 > 탑 메뉴 'POKOPANG!' 선택 > 탭 타이틀 텍스트 비교
        """탑 메뉴 > POKOPANG! 클릭 후, 탭 타이틀 비교"""
        def Tc092(LANG, **kwargs):
            pokopang_xpath = "//a[@class='over']//img" # 좌측 상단 POKOPANG! xpath
            pokopang = self.selenium.wait('xpath', pokopang_xpath)
            pokopang.click() # 'POKOPANG!' 버튼 클릭
            title_xpath = "//title[contains(text(),'POKOPANG!')]" # title xpath
            title = self.selenium.wait('xpath', title_xpath)

            result_title = title.get_attribute('innerText') # title text 가져옴(innerText or textContent)
            expected_title = 'POKOPANG!' # 타이틀 기대값

            self.assertIn(expected_title, result_title, msg=(f'Tc092: expected title = {expected_title}, result = {result_title}')) # 검증
            LOGGER.info("Tc092: (%s) 'POKOPANG!' link page's title: '%s' - test is pass", LANG, result_title)

        self.contents_check_by_lang(Tc092)

    def test_Tc093_Tc096(self): # 탑 메뉴 xpath로 찾아 클릭하여 해당 페이지 이동, menu path 검증
        """탑 메뉴 > ABOUT, NEWS, CONTENTS, CONTACT xpath 로 가져와서 text 비교"""
        def Tc093_Tc096(LANG, **kwargs):
            expected_top_list = ['ABOUT', 'NEWS', 'CONTENTS', 'CONTACT'] # 탑 메뉴 list

            result = self.check_menu_list(expected_top_list, 'top', LANG)
            self.assertTrue(result, msg='TC_menu_check - test is fail')
            LOGGER.info("Tc093~096: (%s) top menu '%s' - test is pass", LANG, result)

        self.contents_check_by_lang(Tc093_Tc096)

    def test_Tc097(self): # 탑 메뉴 > 햄버거 선택 후, 추가 노출되는 메뉴 중 HOME 검증
        """햄버거 버튼 하위 메뉴 HOME을 타이틀명으로 검증"""
        def Tc097(LANG, **kwargs):
            hamburger = "//li[@id='js-sitemenuBtn']" # 햄버거 xpath
            self.selenium.wait('xpath', hamburger).click() # 햄버거 버튼 클릭
            home = '/html/body/header/div[3]/div/ul/li[1]/a' # HOME xpath
            self.selenium.wait('xpath', home).click() # HOME 메뉴 클릭

            title_xpath = "//title[contains(text(),'POKOPANG!')]"
            title = self.selenium.wait('xpath', title_xpath) # 타이틀 속성 지정

            result_title = title.get_attribute('innerText') # title의 text 가져옴, innerText 대신 textContent 도 결과 동일
            expected_title = 'POKOPANG!' # 타이틀 스트링 기대값

            self.assertIn(expected_title, result_title, msg=(f'Tc097: expected title = {expected_title}, result = {result_title}')) # 검증
            LOGGER.info("Tc097: (%s) hamburger menu 'HOME(%s)' - test is pass", LANG, result_title)
        
        self.contents_check_by_lang(Tc097)

    def test_Tc098_Tc101(self): # 탑 메뉴 > 햄버거 선택 후, 추가 노출되는 메뉴 중 HOME을 제외한 나머지 검증
        """햄버거 버튼 하위 메뉴 ABOUT, NEWS, CONTENTS, CONTACT를 xpath로 검증"""
        def Tc098_Tc101(LANG, **kwargs):
            expected_hamburger_list = ['ABOUT', 'NEWS', 'CONTENTS', 'CONTACT']

            result = self.check_menu_list(expected_hamburger_list, 'hamburger', LANG)
            self.assertTrue(result, msg='TC_menu_check - test is fail')
            LOGGER.info("Tc098~101: (%s) hamburger menu '%s' - test is pass", LANG, result) # 검증

        self.contents_check_by_lang(Tc098_Tc101)

    def test_Tc102_Tc104(self): # 탑 메뉴 > 햄버거 선택 후, 추가 노출되는 메뉴 중 언어 변경 검증
        """햄버거 버튼 하위 메뉴 English, 日本語, 한국어 html tag_name lang 으로 검증"""
        def Tc102_Tc104(LANG, **kwargs):
            expected_language_list = ['en-US', 'ja', 'ko-KR']

            for index, expected_lang in enumerate(expected_language_list):
                self.selenium.wait('xpath', '/html/body/header/div[1]/div/ul/li[2]').click() # 햄버거 버튼 클릭
                xpath = f'/html/body/header/div[3]/div/div/ul/li[{index+1}]' # 각 메뉴 xpath

                self.selenium.wait('xpath', xpath).click() # 각 메뉴 클릭 실행
                time.sleep(1)

                result_lang = self.selenium.wait('tag_name', 'html').get_attribute('lang') # 각 언어 페이지마다 html lang 값 가져옴

                if result_lang == 'en-US': # 영어 검증
                    self.assertEqual(expected_lang, result_lang, msg=(f'Tc102: expected title = {expected_lang}, result = {result_lang}'))
                    LOGGER.info("Tc102: (%s) hamburger menu 'English(%s)' - test is pass", LANG, result_lang)
                    time.sleep(1)

                elif result_lang == 'ja': # 일본어 검증
                    self.assertEqual(expected_lang, result_lang, msg=(f'Tc103: expected title = {expected_lang}, result = {result_lang}'))
                    LOGGER.info("Tc103: (%s) hamburger menu '日本語(%s)' - test is pass", LANG, result_lang)
                    time.sleep(1)

                elif result_lang == 'ko-KR': # 한국어 검증
                    self.assertEqual(expected_lang, result_lang, msg=(f'Tc104: expected title = {expected_lang}, result = {result_lang}'))
                    LOGGER.info("Tc104: (%s) hamburger menu '한국어(%s)' - test is pass", LANG, result_lang)
                    time.sleep(1)

        self.contents_check_by_lang(Tc102_Tc104)

    def test_Tc105(self): # 메인 페이지 > 이미지 검증
        """페이지 전체 이미지 로드 되는지 확인"""
        def Tc105(LANG, **kwargs):
            image_load = self.selenium.is_image_loaded()
            self.assertTrue(image_load, msg='Tc105: image_load - test is fail')
            LOGGER.info("Tc105: (%s) page's image load '%s' - test is pass", LANG, image_load)
        
        self.contents_check_by_lang(Tc105)

    def test_Tc106_Tc109(self): # 푸터 부분 검증
        """푸터 메뉴 ABOUT, NEWS, CONTENTS, CONTACT xpath로 각각 검증"""
        def Tc106_Tc109(LANG, **kwargs):
            expected_footer_list = ['ABOUT', 'NEWS', 'CONTACT']

            contents_xpath = '/html/body/footer/div[1]/div/div[1]/div/ul[2]/li[2]/a' # //li[@id='menu-item-587']//a[contains(text(),'CONTENTS')]

            result = self.check_menu_list(expected_footer_list, 'footer', LANG)
            self.assertTrue(result, msg='TC_menu_check - test is fail')
            LOGGER.info("Tc106~108: (%s) footer menu '%s' - test is pass", LANG, result) # 검증

            expected_xpath = '/html/body/main/div[1]/ul/li[2]'
            contents = self.selenium.wait('xpath', contents_xpath)
            expected_value = contents.text
            contents.click()
            menu = self.selenium.wait('xpath', expected_xpath)
            result = menu.text.split(' ')[0]
            self.assertEqual(expected_value, result, msg=(f'Tc109: expected value = {expected_value}, result = {result}'))
            LOGGER.info("Tc109: (%s) footer menu '%s' - test is pass", LANG, result)
        
        self.contents_check_by_lang(Tc106_Tc109)

    def test_Tc110(self): # 하단 treenod 로고 버튼 검증
        """최하단 treenod 로고 노출 여부 확인, 클릭시 트리노드 홈페이지 이동 확인"""
        def Tc110(LANG, **kwargs):
            treenod_xpath = "//p[@class='copyright']//a//img" # '/html/body/footer/div[2]/div/p/a/img' # 하단 treenod 로고 버튼 xpath
            self.selenium.wait('xpath', treenod_xpath).click() # 버튼 click

            self.selenium.driver.switch_to.window(self.selenium.driver.window_handles[-1]) # 새로 띄운 창으로 전환
            time.sleep(1)

            title_xpath = '/html/head/title' # 새로 열린 창의 타이틀 xpath
            el = self.selenium.wait('xpath', title_xpath)
            result_title = el.get_attribute('innerText') # 타이틀 속성 중, 텍스트 가져옴
            expected_title = 'Treenod | 트리노드' # 타이틀 스트링 기대값
            self.assertEqual(expected_title, result_title, msg=(f'Tc110: expected title = {expected_title}, result = {result_title}')) # 검증
            LOGGER.info("Tc110: (%s) 'treenod' link page's title: '%s' - test is pass", LANG, result_title)
        
        self.contents_check_by_lang(Tc110)

    def test_Tc111_Tc112(self): # 스크롤 다운 후, top 버튼 노출 확인 및 검증하고 클릭하여 Top으로 이동
        """스크롤 이동하여 페이지 최하단 이동, 스크롤 바닥에서 top 버튼 검증"""
        def Tc111_Tc112(LANG, **kwargs):
            y_offset = int(self.driver.execute_script("return window.pageYOffset;")) # 현재 보여지는 페이지 최상단 location 의 Y offset 값
            if y_offset != 0: # y_offset 값이 0 이 아닌 경우, 테스트 불가능 상황 처리
                LOGGER.warning("Tc111~112: (%s) test is impossible", LANG)
                self.assertTrue(False)

            self.selenium.scroll_down() # selenium.scroll_down 함수 이용, 페이지 최하단 이동

            total_height = int(self.driver.execute_script("return document.body.scrollHeight;")) # 현재 페이지 전체 크기
            scroll_height = int(self.driver.execute_script("return window.innerHeight;")) # 현재 보이는 화면 크기

            y_offset = int(self.driver.execute_script("return window.pageYOffset;")) # 스크롤 최하단 이동 후, 현재 페이지 Y offset 값 다시 가져옴
            if y_offset != (total_height - scroll_height): # 현재 y offset 값이 전체 높이에서 스크롤 높이를 뺀 수치와 같지 않다면, 스크롤에 문제가 되는 상황
                LOGGER.warning("Tc111~112: (%s) test is impossible", LANG)
                self.assertTrue(False)

            top_button_xpath = "//a[@id='js-pagetop-link']" # 탑버튼(∧) xpath
            top_button = self.selenium.wait('xpath', top_button_xpath)
            top_button.click() # 버튼 클릭하여 최상단 이동
            self.assertTrue(top_button, msg="top_botton is not exist")
            time.sleep(1)
            y_offset = int(self.driver.execute_script("return window.pageYOffset;"))
            if y_offset == 0:
                self.assertTrue(True, msg="y_offset != 0")
                LOGGER.info("Tc111~112: (%s) 'scroll_down + top_button' - test is pass", LANG)

        self.contents_check_by_lang(Tc111_Tc112)

    def test_Tc113(self):
        def Tc113(LANG, **kwargs):
            self.check_page_main_title('CONTENTS', LANG)

        self.contents_check_by_lang(Tc113)
    
    def test_Tc114(self):
        def Tc114(LANG, **kwargs):
            body_xpath = "/html/body/main" # 페이지 body text
            result_text = self.selenium.get_text('xpath', body_xpath)
                
            SEARCH_KEYWORD = kwargs['search_keyword']

            self.assertIn(SEARCH_KEYWORD, result_text, msg=(f'Tc114: search_keyword = {SEARCH_KEYWORD}, result = {result_text}')) # 검증
            LOGGER.info("Tc114: (%s) page keyword text: '%s' - test is pass", LANG, SEARCH_KEYWORD)

        self.contents_check_by_lang(Tc114)

    def test_Tc115(self): # 포코팡닷컴 페이지 오픈
        """웹 브라우저 > 포코팡닷컴 접속"""
        print("=================================================== CONTACT PAGE ===================================================")
        def Tc115(LANG, **kwargs):
            result = kwargs['result']
            self.assertTrue(result, msg='Tc115: open url - test is fail')
            LOGGER.info("Tc115: (%s) open url '%s'- test is pass", LANG, result)

        self.contact_check_by_lang(Tc115)

    def test_Tc116(self): # 현재 페이지 언어 감지 - 뉴스 헤드라인 부분으로 검증
        """language_check 모듈로 현재 웹페이지 언어 감지"""
        def Tc116(LANG, **kwargs):
            body_main_xpath = "/html/body/main" # 페이지 text xpath 
            body_main_text = self.selenium.get_text('xpath', body_main_xpath) # 컨텐츠에 있는 텍스트 모두 저장
            result_list = language_check.check(body_main_text) # language_check 모듈 > 함수 사용하여 컨텐츠 텍스트 언어 감지

            if len(result_list) >= 2: # 2가지 이상 언어가 섞여 있을 경우의 처리
                LOGGER.warning("Tc116: (%s) 이 페이지 언어는 %s가 동일 비율로 섞여 있어 추가 확인이 필요합니다.", LANG, result_list)

            elif len(result_list) == 0: # 언어 판단 불가능할 경우의 처리
                LOGGER.warning("Tc116: (%s) 이 페이지 언어는 판단 가능한 언어가 포함되지 않아 %s 추가 확인이 필요합니다.", LANG, result_list)

            elif 'ko' in result_list: # 한국어 비율이 높을 경우의 처리
                LOGGER.info("Tc116: (%s) 이 페이지는 한국어%s 페이지일 가능성이 높습니다.", LANG, result_list)

            elif 'en' in result_list: # 영어 비율이 높을 경우의 처리
                LOGGER.info("Tc116: (%s) 이 페이지는 English%s 페이지일 가능성이 높습니다.", LANG, result_list)

            elif 'ja' in result_list: # 일본어 비율이 높을 경우의 처리
                LOGGER.info("Tc116: (%s) 이 페이지는 日本語%s 페이지일 가능성이 높습니다.", LANG, result_list)

            self.assertIsNotNone(result_list, msg='Tc116: language_check - test is fail')
            LOGGER.info("Tc116: (%s) language_check = %s - test is pass", LANG, result_list)

        self.contact_check_by_lang(Tc116)

    def test_Tc117(self): # 메인페이지 > 탑 메뉴 'POKOPANG!' 선택 > 탭 타이틀 텍스트 비교
        """탑 메뉴 > POKOPANG! 클릭 후, 탭 타이틀 비교"""
        def Tc117(LANG, **kwargs):
            pokopang_xpath = "//a[@class='over']//img" # 좌측 상단 POKOPANG! xpath
            pokopang = self.selenium.wait('xpath', pokopang_xpath)
            pokopang.click() # 'POKOPANG!' 버튼 클릭
            title_xpath = "//title[contains(text(),'POKOPANG!')]" # title xpath
            title = self.selenium.wait('xpath', title_xpath)

            result_title = title.get_attribute('innerText') # title text 가져옴(innerText or textContent)
            expected_title = 'POKOPANG!' # 타이틀 기대값

            self.assertIn(expected_title, result_title, msg=(f'Tc117: expected title = {expected_title}, result = {result_title}')) # 검증
            LOGGER.info("Tc117: (%s) 'POKOPANG!' link page's title: '%s' - test is pass", LANG, result_title)

        self.contact_check_by_lang(Tc117)

    def test_Tc118_Tc121(self): # 탑 메뉴 xpath로 찾아 클릭하여 해당 페이지 이동, menu path 검증
        """탑 메뉴 > ABOUT, NEWS, CONTENTS, CONTACT xpath 로 가져와서 text 비교"""
        def Tc118_Tc121(LANG, **kwargs):
            expected_top_list = ['ABOUT', 'NEWS', 'CONTENTS', 'CONTACT'] # 탑 메뉴 list

            result = self.check_menu_list(expected_top_list, 'top', LANG)
            self.assertTrue(result, msg='TC_menu_check - test is fail')
            LOGGER.info("Tc118~121: (%s) top menu '%s' - test is pass", LANG, result)

        self.contact_check_by_lang(Tc118_Tc121)

    def test_Tc122(self): # 탑 메뉴 > 햄버거 선택 후, 추가 노출되는 메뉴 중 HOME 검증
        """햄버거 버튼 하위 메뉴 HOME을 타이틀명으로 검증"""
        def Tc122(LANG, **kwargs):
            hamburger = "//li[@id='js-sitemenuBtn']" # 햄버거 xpath
            self.selenium.wait('xpath', hamburger).click() # 햄버거 버튼 클릭
            home = '/html/body/header/div[3]/div/ul/li[1]/a' # HOME xpath
            self.selenium.wait('xpath', home).click() # HOME 메뉴 클릭

            title_xpath = "//title[contains(text(),'POKOPANG!')]"
            title = self.selenium.wait('xpath', title_xpath) # 타이틀 속성 지정

            result_title = title.get_attribute('innerText') # title의 text 가져옴, innerText 대신 textContent 도 결과 동일
            expected_title = 'POKOPANG!' # 타이틀 스트링 기대값

            self.assertIn(expected_title, result_title, msg=(f'Tc122: expected title = {expected_title}, result = {result_title}')) # 검증
            LOGGER.info("Tc122: (%s) hamburger menu 'HOME(%s)' - test is pass", LANG, result_title)
        
        self.contact_check_by_lang(Tc122)

    def test_Tc123_Tc126(self): # 탑 메뉴 > 햄버거 선택 후, 추가 노출되는 메뉴 중 HOME을 제외한 나머지 검증
        """햄버거 버튼 하위 메뉴 ABOUT, NEWS, CONTENTS, CONTACT를 xpath로 검증"""
        def Tc123_Tc126(LANG, **kwargs):
            expected_hamburger_list = ['ABOUT', 'NEWS', 'CONTENTS', 'CONTACT']

            result = self.check_menu_list(expected_hamburger_list, 'hamburger', LANG)
            self.assertTrue(result, msg='TC_menu_check - test is fail')
            LOGGER.info("Tc123~126: (%s) hamburger menu '%s' - test is pass", LANG, result) # 검증

        self.contact_check_by_lang(Tc123_Tc126)

    def test_Tc127_Tc129(self): # 탑 메뉴 > 햄버거 선택 후, 추가 노출되는 메뉴 중 언어 변경 검증
        """햄버거 버튼 하위 메뉴 English, 日本語, 한국어 html tag_name lang 으로 검증"""
        def Tc127_Tc129(LANG, **kwargs):
            expected_language_list = ['en-US', 'ja', 'ko-KR']

            for index, expected_lang in enumerate(expected_language_list):
                self.selenium.wait('xpath', '/html/body/header/div[1]/div/ul/li[2]').click() # 햄버거 버튼 클릭
                xpath = f'/html/body/header/div[3]/div/div/ul/li[{index+1}]' # 각 메뉴 xpath

                self.selenium.wait('xpath', xpath).click() # 각 메뉴 클릭 실행
                time.sleep(1)

                result_lang = self.selenium.wait('tag_name', 'html').get_attribute('lang') # 각 언어 페이지마다 html lang 값 가져옴

                if result_lang == 'en-US': # 영어 검증
                    self.assertEqual(expected_lang, result_lang, msg=(f'Tc127: expected title = {expected_lang}, result = {result_lang}'))
                    LOGGER.info("Tc127: (%s) hamburger menu 'English(%s)' - test is pass", LANG, result_lang)
                    time.sleep(1)

                elif result_lang == 'ja': # 일본어 검증
                    self.assertEqual(expected_lang, result_lang, msg=(f'Tc128: expected title = {expected_lang}, result = {result_lang}'))
                    LOGGER.info("Tc128: (%s) hamburger menu '日本語(%s)' - test is pass", LANG, result_lang)
                    time.sleep(1)

                elif result_lang == 'ko-KR': # 한국어 검증
                    self.assertEqual(expected_lang, result_lang, msg=(f'Tc129: expected title = {expected_lang}, result = {result_lang}'))
                    LOGGER.info("T129: (%s) hamburger menu '한국어(%s)' - test is pass", LANG, result_lang)
                    time.sleep(1)

        self.contact_check_by_lang(Tc127_Tc129)

    def test_Tc130(self): # 메인 페이지 > 이미지 검증
        """페이지 전체 이미지 로드 되는지 확인"""
        def Tc130(LANG, **kwargs):
            image_load = self.selenium.is_image_loaded()
            self.assertTrue(image_load, msg='Tc130: image_load - test is fail')
            LOGGER.info("Tc130: (%s) page's image load '%s' - test is pass", LANG, image_load)
        
        self.contact_check_by_lang(Tc130)

    def test_Tc131_Tc134(self): # 푸터 부분 검증
        """푸터 메뉴 ABOUT, NEWS, CONTENTS, CONTACT xpath로 각각 검증"""
        def Tc131_Tc134(LANG, **kwargs):
            expected_footer_list = ['ABOUT', 'NEWS', 'CONTACT']

            contents_xpath = '/html/body/footer/div[1]/div/div[1]/div/ul[2]/li[2]/a' # //li[@id='menu-item-587']//a[contains(text(),'CONTENTS')]

            result = self.check_menu_list(expected_footer_list, 'footer', LANG)
            self.assertTrue(result, msg='TC_menu_check - test is fail')
            LOGGER.info("Tc131~133: (%s) footer menu '%s' - test is pass", LANG, result) # 검증

            expected_xpath = '/html/body/main/div[1]/ul/li[2]'
            contents = self.selenium.wait('xpath', contents_xpath)
            expected_value = contents.text
            contents.click()
            menu = self.selenium.wait('xpath', expected_xpath)
            result = menu.text.split(' ')[0]
            self.assertEqual(expected_value, result, msg=(f'Tc134: expected value = {expected_value}, result = {result}'))
            LOGGER.info("Tc134: (%s) footer menu '%s' - test is pass", LANG, result)
        
        self.contact_check_by_lang(Tc131_Tc134)

    def test_Tc135(self): # 하단 treenod 로고 버튼 검증
        """최하단 treenod 로고 노출 여부 확인, 클릭시 트리노드 홈페이지 이동 확인"""
        def Tc135(LANG, **kwargs):
            treenod_xpath = "//p[@class='copyright']//a//img" # '/html/body/footer/div[2]/div/p/a/img' # 하단 treenod 로고 버튼 xpath
            self.selenium.wait('xpath', treenod_xpath).click() # 버튼 click

            self.selenium.driver.switch_to.window(self.selenium.driver.window_handles[-1]) # 새로 띄운 창으로 전환
            time.sleep(1)

            title_xpath = '/html/head/title' # 새로 열린 창의 타이틀 xpath
            el = self.selenium.wait('xpath', title_xpath)
            result_title = el.get_attribute('innerText') # 타이틀 속성 중, 텍스트 가져옴
            expected_title = 'Treenod | 트리노드' # 타이틀 스트링 기대값
            self.assertEqual(expected_title, result_title, msg=(f'Tc135: expected title = {expected_title}, result = {result_title}')) # 검증
            LOGGER.info("Tc135: (%s) 'treenod' link page's title: '%s' - test is pass", LANG, result_title)
        
        self.contact_check_by_lang(Tc135)

    def test_Tc136_Tc137(self): # 스크롤 다운 후, top 버튼 노출 확인 및 검증하고 클릭하여 Top으로 이동
        """스크롤 이동하여 페이지 최하단 이동, 스크롤 바닥에서 top 버튼 검증"""
        def Tc136_Tc137(LANG, **kwargs):
            y_offset = int(self.driver.execute_script("return window.pageYOffset;")) # 현재 보여지는 페이지 최상단 location 의 Y offset 값
            if y_offset != 0: # y_offset 값이 0 이 아닌 경우, 테스트 불가능 상황 처리
                LOGGER.warning("Tc136~137: (%s) test is impossible", LANG)
                self.assertTrue(False)

            self.selenium.scroll_down() # selenium.scroll_down 함수 이용, 페이지 최하단 이동

            total_height = int(self.driver.execute_script("return document.body.scrollHeight;")) # 현재 페이지 전체 크기
            scroll_height = int(self.driver.execute_script("return window.innerHeight;")) # 현재 보이는 화면 크기

            y_offset = int(self.driver.execute_script("return window.pageYOffset;")) # 스크롤 최하단 이동 후, 현재 페이지 Y offset 값 다시 가져옴
            if y_offset != (total_height - scroll_height): # 현재 y offset 값이 전체 높이에서 스크롤 높이를 뺀 수치와 같지 않다면, 스크롤에 문제가 되는 상황
                LOGGER.warning("Tc136~137: (%s) test is impossible", LANG)
                self.assertTrue(False)

            top_button_xpath = "//a[@id='js-pagetop-link']" # 탑버튼(∧) xpath
            top_button = self.selenium.wait('xpath', top_button_xpath)
            top_button.click() # 버튼 클릭하여 최상단 이동
            self.assertTrue(top_button, msg="top_botton is not exist")
            time.sleep(1)
            y_offset = int(self.driver.execute_script("return window.pageYOffset;"))
            if y_offset == 0:
                self.assertTrue(True, msg="y_offset != 0")
                LOGGER.info("Tc136~137: (%s) 'scroll_down + top_button' - test is pass", LANG)

        self.contact_check_by_lang(Tc136_Tc137)

    def test_Tc138(self):
        def Tc138(LANG, **kwargs):
            main_title_xpath = "/html/body/main/section/div/div/h2"
            result_text = self.selenium.get_text('xpath', main_title_xpath)
            expected_text = 'CONTACT US'
            self.assertIn(expected_text, result_text, msg=("Tc_pages's main title: expected_title = {expected_text}, result = {result_text}")) # 검증
            LOGGER.info("Tc138: (%s) 'CONTACT page's title text: '%s' - test is pass", LANG, expected_text)

        self.contact_check_by_lang(Tc138)
    
    def test_Tc139(self):
        def Tc139(LANG, **kwargs):
            body_xpath = "/html/body/main" # 페이지 body text
            result_text = self.selenium.get_text('xpath', body_xpath)
                
            SEARCH_KEYWORD = kwargs['search_keyword']

            self.assertIn(SEARCH_KEYWORD, result_text, msg=(f'Tc139: search_keyword = {SEARCH_KEYWORD}, result = {result_text}')) # 검증
            LOGGER.info("Tc139: (%s) page keyword text: '%s' - test is pass", LANG, SEARCH_KEYWORD)

        self.contact_check_by_lang(Tc139)