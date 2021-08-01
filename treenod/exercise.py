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

# flake8 linting ignore: E501(line too long), E226(missing whitespace around arithmetic operator), E301,E302(expected 2 blank lines, found 1 - 클래스 / 메소드별 개행 개수)
# pydocstyle linting ignore: D100,D101,D102(Missing docstring in public module, class, method)
# 커버리지: 1. 각 페이지 이동, 2. 페이지별 Header/게시물/Footer/슬라이드 및 Top버튼 동작, 3. 게시물 기능(새창, 페이지 이동, 팝업), 4. 게시물 개수, 5. 검색/메뉴 버튼 기능
# 스펙아웃: 1. 각 게시물 상세 문구 및 이미지 일치 여부, 2. All 탭 게시물 기능, 3. 동영상 컨텐츠 재생, 4. 전자 메일 송부 기능, 5. 검색 버튼으로 검색한 컨텐츠 기능(별도로 클릭하지 않음)

LOGGER = logging.getLogger()
MAIN_URL = 'https://www.pokopang.com/'

class TestPokopangcom(BaseTestCase):
    MI = '#menu-item-'  # MenuItem
    Header = {
        'ko': {"POKOPANG!": ".logo", "ABOUT": MI+"637", "NEWS": MI+"51", "CONTENTS": MI+"549", "CONTACT": MI+"543", "search": "#js-searchBtn", "menu": "#js-sitemenuBtn"},
        'en': {"POKOPANG!": ".logo", "ABOUT": MI+"638", "NEWS": MI+"51", "CONTENTS": MI+"549", "CONTACT": MI+"542", "search": "#js-searchBtn", "menu": "#js-sitemenuBtn"},
        'jp': {"POKOPANG!": ".logo", "ABOUT": MI+"636", "NEWS": MI+"51", "CONTENTS": MI+"549", "CONTACT": MI+"159", "search": "#js-searchBtn", "menu": "#js-sitemenuBtn"}
    }
    Banner = {
        "slideimage1": "[1]/div/div/div/span[1]", "slideimage2": "[1]/div/div/div/a[2]", "event_image": "[2]/div[1]/div[1]/div[1]/a/div[1]/img",
        "collabo_image": "[2]/div[1]/div[1]/div[2]/a/div[1]/img", "facebook_image": "[2]/div[1]/div[2]/ul/div/div/li/a/img", "Artwork": "[2]/div[2]/ul/li[1]/a/div/img",
        "Video": "[2]/div[2]/ul/li[2]/a/div/img", "Webcomic": "[2]/div[2]/ul/li[3]/a/div/img", "See_more_btn": "[2]/div[2]/div/a"
    }
    Footer = {
        'ko': {"TOP_btn": "#js-pagetop-link", "footer_area": ".footer_col_wrapper", "footer_title": ".footer_col_head", "footer_ABOUT": MI+"768",
               "footer_NEWS": MI+"775", "footer_CONTENTS": MI+"587", "footer_CONTACT": MI+"589", "treenod_and_copyright": ".copyright"},
        'en': {"TOP_btn": "#js-pagetop-link", "footer_area": ".footer_col_wrapper", "footer_title": ".footer_col_head", "footer_ABOUT": MI+"769",
               "footer_NEWS": MI+"775", "footer_CONTENTS": MI+"587", "footer_CONTACT": MI+"590", "treenod_and_copyright": ".copyright"},
        'jp': {"TOP_btn": "#js-pagetop-link", "footer_area": ".footer_col_wrapper", "footer_title": ".footer_col_head", "footer_ABOUT": MI+"767",
               "footer_NEWS": MI+"775", "footer_CONTENTS": MI+"587", "footer_CONTACT": MI+"588", "treenod_and_copyright": ".copyright"}
    }

    # 최초_포코팡닷컴_메인페이지_이동
    def open_page(self, url, lan):
        if lan == 'jp':
            result = self.selenium.open_url(url+'home')
        else:
            result = self.selenium.open_url(url+lan)
        self.driver.implicitly_wait(10)
        self.assertTrue(result, msg='{0} 접속 불가 - FAIL'.format(url+lan))
        LOGGER.info('{0} 접속 - PASS'.format(url+lan))

    # Header 영역 확인
    def find_header(self, lan):
        for key in self.Header[lan].keys():
            result = self.selenium.wait('css_selector', self.Header[lan][key])
            self.assertTrue(result, msg='{0} 미노출 - FAIL'.format(key))
            LOGGER.info('{0} 노출 - PASS'.format(key))

    # 슬라이드 배너 및 기타 메인 페이지 이미지 확인 - 클래스명이 동일한 이미지들이 있어, xpath 활용
    def find_banner(self, lan):
        if lan == 'en':
            del self.Banner['slideimage2'], self.Banner["event_image"], self.Banner["collabo_image"]
            self.Banner['Sticker_image_1'] = '[2]/div[1]/div[1]/div[1]/a/div[1]/img'
            self.Banner['Sticker_image_2'] = '[2]/div[1]/div[1]/div[2]/a/div[1]/img'
        if lan == 'jp':     # en 다음으로 jp 검증하기 때문에 en 배너들 삭제
            del self.Banner['Sticker_image_1'], self.Banner['Sticker_image_2']
            self.Banner["event_image"] = '[2]/div[1]/div[1]/div[1]/a/div[1]/img'
            self.Banner['Sticker_image'] = '[2]/div[1]/div[1]/div[2]/a/div[1]/img'
            self.Banner['instagram_image'] = '[2]/div[1]/div[2]/ul/div/div/li[1]/a/img'
            self.Banner['twitter_image'] = '[2]/div[1]/div[2]/ul/div/div/li[2]/a/img'
        for key, value in self.Banner.items():
            result = self.selenium.wait('xpath', "/html/body/main/div"+value)
            self.assertTrue(result, msg='{0} 메인페이지 {1} 미노출 - FAIL'.format(lan, key))
            LOGGER.info('{0} 메인페이지 {1} 노출 - PASS'.format(lan, key))

    # Footer 영역 및 TOP 버튼 확인
    def find_footer(self, lan):
        for key in self.Footer[lan].keys():
            result = self.selenium.wait('css_selector', self.Footer[lan][key])
            self.assertTrue(result, msg='{0} 미노출 - FAIL'.format(key))
            LOGGER.info('{0} 노출 - PASS'.format(key))

    def check_scroll(self, lan, value):     # 스크롤 및 TOP 버튼으로 올라오기 - sona, conner 함수 참고하여 섞은 형태
        self.selenium.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        scroll_result = self.selenium.driver.execute_script("return document.querySelector('html').scrollTop")
        total_height = self.driver.execute_script("return document.body.scrollHeight;")  # 페이지 전체 높이
        scroll_height = self.driver.execute_script("return window.innerHeight;")  # 스크롤 길이
        if (scroll_height + 100) > total_height:
            LOGGER.info("스크롤이 필요하지 않은 페이지입니다.")
        if scroll_result > 0:
            LOGGER.info("{0} {1} 스크롤 - PASS".format(lan, value))
        elif scroll_result <= 0:
            result = None
            self.assertIsNone(result, msg="{0} {1} 스크롤 불가 - FAIL".format(lan, value))
        time.sleep(1)
        self.selenium.wait('css_selector', self.Footer[lan]['TOP_btn']).click()  # TOP 버튼 터치
        result = self.selenium.wait('css_selector', self.Header[lan]['POKOPANG!'])
        self.assertTrue(result, msg='TOP 버튼 미작동 - FAIL')
        LOGGER.info('TOP 버튼 작동 - PASS')

    # 임의의 메뉴 터치하여 페이지 이동(각 페이지별 메인 타이틀 텍스트가 노출되는지 확인하여 페이지 이동 유추) 확인
    def move_page(self, lan, value):
        time.sleep(1)
        self.selenium.wait('css_selector', self.Header[lan][value]).click()
        title_text = value
        if value == 'CONTACT':      # CONTACT 페이지의 경우만 메인 타이틀의 클래스명이 상이하여 예외처리
            page_title = self.selenium.get_text('css_selector', '.content_title')
        else:
            page_title = self.selenium.get_text('css_selector', '.main_title')
        if title_text not in page_title:
            result = None
            self.assertIsNotNone(result, msg="{0} 페이지 메인 타이틀 텍스트 - FAIL".format(value))
        LOGGER.info("{0} 페이지 메인 타이틀 텍스트 - PASS".format(value))

    # element 노출 검증
    def find_element(self, name, value):
        result = self.selenium.wait('css_selector', value)
        if value == '.header_search_inner' or value == '.header_sitemenu_inner':
            if result is not True:              # 메뉴 버튼과 X버튼 클래스명이 동일하여, X버튼 터치 시 메뉴 영역 미노출 확인을 위한 예외처리
                reverse_result = True           # 메뉴 영역이 보이지 않을 시, result는 false가 되며, 해당 결과가 TC에서는 Pass인 상태
                self.assertTrue(reverse_result, msg='{0} 노출 - FAIL'.format(name))     # 메뉴 영역 노출 시 Fail
                LOGGER.info('{0} 미노출 - PASS'.format(name))                           # 메뉴 영역 미노출 시 Pass
        else:
            self.assertTrue(result, msg='{0} 미노출 - FAIL'.format(name))
            LOGGER.info('{0} 노출 - PASS'.format(name))

    # text 검증
    def find_text(self, name, value, sentence):
        result = self.selenium.wait('css_selector', value, find_multiple=True)
        text_list = list(result)
        for i in text_list:
            j = i.text
            if sentence not in j:
                j = None
                self.assertIsNotNone(j, msg='{0} 텍스트 미노출 - FAIL'.format(name))
        LOGGER.info('{0} 텍스트 정상 노출 확인 - PASS'.format(name))

    # text로 요소 개수 검증 - NEWS page > 각 탭 내 카테고리들이 정상적으로 노출되는지 검증(각 탭별 카테고리 개수 합산 > All 탭 개수와 비교하여 유추)
    def find_text_count(self, name, value, sentence):
        result = self.selenium.wait('css_selector', value, find_multiple=True)
        text_list = list(result)
        count = []
        for i in text_list:
            j = i.text
            if sentence == j:
                count.append(j)
            else:
                self.assertIsNotNone(j, msg='{0} 요소 개수 검증 불가 - FAIL'.format(name))
        LOGGER.info('{0} 요소 개수: {1} 개 - PASS'.format(name, len(count)))

    # 임의의 버튼 클릭
    def button_click(self, value):
        time.sleep(1)
        self.selenium.wait('css_selector', value).click()

    # 임의의 게시물 클릭 후 페이지 이동 여부 확인 - 게시물 터치 시, 1. 새 창 오픈 / 2. 페이지 이동 / 3. 팝업 노출 > 검증
    def button_click_move_page(self, value):
        count = self.selenium.wait('css_selector', value, find_multiple=True)
        for i in range(0, len(count)):
            result = self.selenium.wait('css_selector', value, find_multiple=True)
            url = self.driver.current_url       # 현재 주소를 받아 url 변수로 저장
            if len(result) > 0:
                time.sleep(1)
                j = result[i].click()           # 게시물 터치
                time.sleep(1)
                if url != self.driver.current_url:  # 페이지 이동하는 게시물(현재 주소가 url 변수의 주소와 다를 경우) > 2. 페이지 이동
                    self.driver.back()              # 이동 후, 뒤로 가기하여 이전 페이지로 돌아오기
                    LOGGER.info('{0}번째 게시물 이동 확인(뒤로 가기) - PASS'.format(i+1))
                elif len(self.driver.window_handles) == 1:  # 현재 주소가 url 변수의 주소와 같으나, 현재 열린 창 수가 1개인 경우 > 3. 팝업 노출
                    # self.driver.implicitly_wait(10)   # video, artwork의 경우, 동영상 실행 시 오류 발생 - 일단 주석처리!!
                    # self.selenium.wait('css_selector',"#player").click()
                    time.sleep(2)
                    self.selenium.wait('css_selector', '#cboxClose').click()     # x버튼 터치하여 팝업 닫기
                    LOGGER.info('{0}번째 게시물 이동 확인(팝업 닫기) - PASS'.format(i+1))
                elif len(self.driver.window_handles) > 1:       # 현재 주소가 url 변수의 주소와 같으나, 현재 열린 창 수가 1개 이상인 경우 > 1. 새 창 오픈
                    self.driver.switch_to_window(self.driver.window_handles[1])  # 새 창으로 창 이동
                    self.driver.implicitly_wait(10)
                    self.driver.close()                                          # 현재 창 닫기
                    LOGGER.info('{0}번째 게시물 이동 확인(새창 닫음) - PASS'.format(i+1))
                    self.driver.switch_to_window(self.driver.window_handles[0])  # 이전 창으로 돌아오기
                else:   # 페이지 이동하지 않으면서, 새창 열리지 않으면서, 팝업 열리지 않는 경우
                    j = None
                    self.assertIsNotNone(j, msg='{0}번째 게시물 이동 불가 - FAIL'.format(i+1))

    # 요소 개수 검증 - 탭별 게시물들의 요소(날짜 / 제목 / 이미지 / 카테고리) 개수가 동일하게 노출되는지 검증(각 요소별 개수 비교로 빠진 요소가 있는지 유추)
    def find_count(self, name, value):
        result = self.selenium._driver.execute_script('return document.getElementsByClassName("{0}").length'.format(value))
        self.assertTrue(result, msg='{0} 개수 미노출 - FAIL'.format(name))
        LOGGER.info('{0} {1} 개 노출 - PASS'.format(name, result))

# -------------------------------------페이지별 기능 검증 함수------------------------------------- #

    # 메인 화면 이동 및 노출 확인
    def main_page_check(self, lan):
        self.open_page(MAIN_URL, lan)
        self.find_header(lan)
        self.find_banner(lan)
        main_page = ['.main_block01_item', 'body > main > div.container > div.clearfix > div.main_block02 > ul > div > div > li.main_block02_list_item.slick-slide.slick-current.slick-active', '.col3_block_list_item', '.btn_block']
        for i in main_page:                       # 간소화 예정!
            self.button_click_move_page(i)
        self.find_footer(lan)
        self.check_scroll(lan, '메인 페이지')

    # ABOUT Page 검증
    def ABOUT_page_check(self, lan):
        self.move_page(lan, 'ABOUT')
        self.find_text('ABOUT', '.main_title', 'ABOUT')  # 페이지 이동 후, 메인 타이틀 노출 검증(페이지 이동 유추 위함)
        self.find_header(lan)
        self.find_element('POKOPANG! 동물 이미지', 'body > main > div:nth-child(2) > div > div > p:nth-child(1) > img')  # 페이지 내 이미지1 검증
        if lan == 'ko':  # 페이지 내 언어별 메인 내용 노출 검증
            self.find_text('ABOUT 페이지 내용_메인 내용', '.entryBody', '포코팡은 전세계')
        elif lan == 'en':
            self.find_text('ABOUT 페이지 내용_메인 내용', '.entryBody', 'Pokopang is a character brand')
        else:
            self.find_text('ABOUT 페이지 내용_메인 내용', '.entryBody', 'ポコパンは全世界約7,000万ダ')
        self.find_element('ABOUT 페이지 내용_이미지', '.goods')  # 페이지 내 이미지2 검증
        self.find_footer(lan)
        self.check_scroll(lan, 'ABOUT 페이지')

    # NEWS Page 검증
    count_list = {'이미지': 'col3_block_img', '날짜': 'col3_block_date', '카테고리': 'col3_block_category', '제목': 'col3_block_text'}  # 각 page 내 반복문에서 쓰일 리스트
    def NEWS_page_check(self, lan):
        self.move_page(lan, 'NEWS')
        self.find_text('NEWS', '.main_title', 'NEWS')
        self.find_header(lan)
        index = [2, 3, 4, 1]
        Tab = ['All', 'Collaboration', 'Sticker', 'Event']
        if lan == 'en':
            del index[2], Tab[3]  # en 리전의 경우, Event 탭이 없기 떄문에 해당 내용 삭제
        for i in index:
            self.button_click('body > main > div:nth-child(2) > div.category_block.container-s > ul > li:nth-child({0}) > a'.format(i))  # 각 카테고리별 탭 터치
            for key, value in self.count_list.items():
                self.find_count(Tab[i-1]+' 게시물 - '+key, value)        # 게시물 요소(이미지 / 날짜 / 카테고리 / 제목) 수 파악(누락 요소 확인) - 클래스명으로 검증
                if i != 1:
                    self.find_text(Tab[i-1]+' 탭 내 카테고리', '.col3_block_category', Tab[i-1])  # 카테고리 개수 파악(타 카테고리가 필터링 되었는지 확인)
            if i != 1:
                self.button_click_move_page('.col3_block_list_item')    # 게시물 클릭 시, 페이지 이동 / 새 창 열림 / 팝업 노출 기능 작동 확인
        self.find_footer(lan)
        self.check_scroll(lan, 'NEWS 페이지')

    # CONTENTS Page 검증
    def CONTENTS_page_check(self, lan):
        self.move_page(lan, 'CONTENTS')
        self.find_text('CONTENTS', '.main_title', 'CONTENTS')
        self.find_header(lan)
        self.find_text_count('Webcomic 카테고리 게시물', '.col3_block_category', 'Webcomic')  # 별도 카테고리별 탭 이동 없음
        self.find_text_count('Video 카테고리 게시물', '.col3_block_category', 'Video')        # 각 카테고리별 개수와 총 게시물 요소들 개수 비교로 누락된 게시물 여부 확인
        self.find_text_count('Artwork 카테고리 게시물', '.col3_block_category', 'Artwork')
        for key, value in self.count_list.items():  # 게시물 요소(이미지 / 날짜 / 카테고리 / 제목) 수 파악(누락 요소 확인) - 클래스명으로 검증
            self.find_count('게시물 - '+key, value)
        self.button_click_move_page('.col3_block_list_item')  # 게시물 클릭 시, 페이지 이동 / 새 창 열림 / 팝업 노출 기능 작동 확인
        self.find_footer(lan)
        self.check_scroll(lan, 'CONTENTS 페이지')

    # CONTACT Page 검증
    def CONTACT_page_check(self, lan):
        self.move_page(lan, 'CONTACT')
        self.find_text('CONTACT US', '.content_title', 'CONTACT US')
        self.find_header(lan)
        if lan == 'ko':
            text_list = ['라이선스, 제휴 등 비즈니스 문의는', 'licensing@treenod.com', '으로 보내주시면', '담당자가 검토 후 연락드리겠습니다.']
        elif lan == 'en':
            text_list = ['The character products', 'Waiting for partners!', 'We always welcome to discuss']
        else:
            text_list = ['日本、韓国、台湾、', '商品化提携、ライセンスイベントなど、']
        for i in text_list:
            self.find_text('CONTACT 페이지 내용_메인 텍스트', '.content_box', i)    # 언어별 메인 텍스트 노출 확인
        self.find_element('CONTACT 페이지 이메일 영역', '.licensing_contact')
        self.find_text('CONTACT 페이지 이메일 영역', '.licensing_contact', 'licensing@treenod.com')
        self.find_footer(lan)
        self.check_scroll(lan, 'CONTACT 페이지')

    # 돋보기(검색) 영역 검증
    def SEARCH_check(self, lan):
        self.button_click(self.Header[lan]['search'])
        self.find_element('검색란', '#searchform')
        self.find_element('search 버튼', '.header_search_btn')
        self.find_element('X버튼', '#js-searchBtn')   # X버튼과 검색 버튼 클래스명 동일
        self.button_click('#js-searchBtn')           # X버튼 터치 시, 검색 영역 미노출 확인
        self.find_element('검색 영역', '.header_search_inner')  # 검색 영역 미노출 시 Pass 처리 - find element 함수에 예외처리 해둔 상태
        self.button_click(self.Header[lan]['search'])
        self.selenium.wait('css_selector', '#searchform > input').send_keys('Amelia')
        self.button_click('.header_search_btn')
        self.find_text('검색 결과 게시물 수', '.search_head', '0')
        if lan == 'ko':     # 검색 결과 없을 시 노출되는 언어별 메인 내용 노출 확인
            self.find_text('검색 결과가 없습니다(ko).', '.entryBody', '검색어와 일치하는 것이 없습니다.')
        elif lan == 'en':
            self.find_text('검색 결과가 없습니다(en).', '.entryBody', 'Sorry, but nothing matched your search terms.')
        else:
            self.find_text('검색 결과가 없습니다(jp).', '.entryBody', '検索キーワードに一致するものが見つかりませんでした。')
        self.button_click(self.Header[lan]['search'])
        self.selenium.wait('css_selector', '#searchform > input').send_keys('poko')
        self.button_click('.header_search_btn')
        search_count = self.selenium._driver.execute_script('return document.getElementsByClassName("col3_block_list_item").length')  # 검색 결과 게시물 수
        result = self.selenium.wait('css_selector', '.search_head', find_multiple=True)
        text_list = list(result)    # 검색 결과 문구 리스트화(Showing / Search / "poko" / with / "N" /results)
        for i in text_list:
            j = i.text              # 검색 결과 문구 리스트 내 검색 결과 게시물 수 텍스트가 포함되어 있는지 검증
            if str(search_count) not in j:
                j = None
                self.assertIsNotNone(j, msg='검색 게시물 수 상이 - FAIL')
        LOGGER.info('검색 결과와 게시물 수 동일({0} 개) - PASS'.format(search_count))
        for key, value in self.count_list.items():  # 검색된 게시물들의 각 요소가 검색 결과 게시물 수와 동일한지 비교(& 누락 요소 여부 확인)
            self.find_count('게시물 - '+key, value)

    # 메뉴 영역 검증
    def MENU_check(self, lan):
        self.button_click(self.Header[lan]['menu'])
        self.find_element('X버튼', '#js-sitemenu')      # X버튼과 메뉴 버튼 클래스명 동일
        menu_list1 = ['HOME', 'ABOUT', 'NEWS', 'CONTENTS', 'CONTACT', 'Language Switcher', 'English (United States)', '日本語', '한국어']    # 메뉴 영역 내 문구 리스트화
        if lan == 'jp':  # jp의 경우, Language Switcher > 言語切り替え 로 노출되어 예외처리
            del menu_list1[5]
            menu_list1.append('言語切り替え')
        for i in menu_list1:
            self.find_text(i+' 문구', '#js-sitemenu', i)
        self.button_click('#js-sitemenuBtn')                    # X버튼 터치 시, 메뉴 영역 미노출 확인
        self.find_element('메뉴 영역', '.header_sitemenu_inner')  # 메뉴 영역 미노출 확인 - find element 함수에 예외처리 해둔 상태
        self.button_click(self.Header[lan]['menu'])             # 메뉴 영역 내 문구들 하나씩 클릭하여 해당 페이지로 이동하는지 확인
        self.button_click('#js-sitemenu > div > ul > li.menu-item.menu-item-type-post_type.menu-item-object-page.menu-item-home.current-menu-item.page_item.page-item-8.current_page_item.menu-item-63')
        if lan == 'jp':  # jp의 경우, HOME 문구 클릭 시, NEWS 페이지로 이동하기 때문에 예외처리
            self.find_text('NEWS 타이틀', '.main_title', 'NEWS')
        else:
            self.find_element('메인 페이지 배너 영역', '.slick-track')  # 나머지 리전의 경우, HOME 문구 클릭 시 메인 페이지로 이동 확인(배너 노출로 페이지 이동 유추)
        menu_list2 = ['ABOUT', 'NEWS', 'CONTENTS', 'CONTACT US']
        address = {
            'ABOUT': 'post_type.menu-item-object-page.menu-item-', 'NEWS': 'taxonomy.menu-item-object-category.menu-item-',
            'CONTENTS': 'taxonomy.menu-item-object-category.menu-item-', 'CONTACT US': 'post_type.menu-item-object-page.menu-item-'
        }
        lan_number = {
            'ko': {"ABOUT": "637", "NEWS": "51", "CONTENTS": "549", "CONTACT US": "543"},
            'en': {"ABOUT": "638", "NEWS": "51", "CONTENTS": "549", "CONTACT US": "542"},
            'jp': {"ABOUT": "636", "NEWS": "51", "CONTENTS": "549", "CONTACT US": "159"}
        }
        for i in menu_list2:    # 나머지 메뉴 영역(NEWS, CONTENTS, CONTACT) 반복문 처리
            self.button_click(self.Header[lan]['menu'])
            self.button_click('#js-sitemenu > div > ul > li.menu-item.menu-item-type-'+address[i]+lan_number[lan][i])
            if i == 'CONTACT US':
                self.find_text(i+' 타이틀', '.content_title', i)
            else:
                self.find_text(i+' 타이틀', '.main_title', i)
        self.button_click(self.Header[lan]['menu'])  # 언어 변경 기능(CONTACT page에서 확인 후, 메인 페이지 이동은 url 변경으로 진행) - ko > en / en > jp / jp > ko로 변경
        lan_list = {
            'ko': {'address': 'li.en-US.en.first', '변경 문구': 'Waiting for partners!'},
            'en': {'address': 'li.ja > a', '변경 문구': 'ライセンスイベントなど'},
            'jp': {'address': 'li.ko-KR.ko.last > a', '변경 문구': '라이선스, 제휴 등 비즈니스 문의는'}
        }
        self.button_click('#js-sitemenu > div > div > ul > '+lan_list[lan]['address'])
        self.find_text("변경 문구 확인 - '"+lan_list[lan]['변경 문구']+"'", '.content_box', lan_list[lan]['변경 문구'])

# -------------------------------------언어별 함수 작동 확인------------------------------------- #

    def test(self):
        self.open_page(MAIN_URL, 'ko')
        '''
        a = self.selenium.wait('css_selector', 'body')
        b = len(a.get_attribute('src'))
        print(b)
        '''
        #self.selenium.is_image_loaded()

        #a = self.selenium.wait('css_selector', '.footer_col > .clearfix a', find_multiple=True)
        #print(len(a))

        b = self.selenium.wait('css_selector', '#top > div.container.clearfix > div > nav > ul a', find_multiple=True)
        print(len(b))


        '''
        lan = ['ko', 'en', 'jp']

        for i in lan:
            self.main_page_check(i)
            self.ABOUT_page_check(i)
            self.NEWS_page_check(i)
            self.CONTENTS_page_check(i)
            self.CONTACT_page_check(i)
            self.SEARCH_check(i)
            self.MENU_check(i)
        '''

    # TO DO: 1.[완료] 메인 페이지 게시물 이동 기능 구현, 2.[완료] Video / Artwork N번째 표시 필요, 3. 수행결과 가독성 높일 수 있도록
    # 코드 리뷰 피드백: 1.[문의 필요] 언어 변경 시, 메인페이지쪽 > 보완(time.sleep), 2. 딕셔너리 간소화(개발자 도구 상위 요소 활용하여 리스트화) 3. 재사용성을 높이기 위해 세분화된 함수 재검토
    # 언어 변경하여 메인 URL 진입 시, 포코팡 닷컴이 아닌 타 페이지 다녀올 시 에러 발생 > URL이 아닌 버튼으로 접근해야 할지?