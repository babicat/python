# -*- coding: utf-8 -*-
import logging
import time
import json
import re

from base import BaseTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

LOGGER = logging.getLogger()

# 에피소드 전역 변수(dictionary list) 분리
EPISODE = {        
    'ja' : [
        {'num': 'EP11', 'title': 'クルグVSタイゴ', 'sub_num': 'Episode 11'},
        {'num': 'EP10', 'title': "ベリーのベリーベリー特訓", 'sub_num': 'Episode 10'},
        {'num': 'EP09', 'title': 'ミドリのおかしな歌', 'sub_num': 'Episode 9'},
        {'num': 'EP08', 'title': '新しい友達ができた！ パート2', 'sub_num': 'Episode 8-2'},
        {'num': 'EP08', 'title': '新しい友達ができた！ パート1', 'sub_num': 'Episode 8-1'},
        {'num': 'EP07', 'title': 'ニンジンがない！ パート2', 'sub_num': 'Episode 7-2'},
        {'num': 'EP07', 'title': 'ニンジンがない！ パート１', 'sub_num': 'Episode 7-1'},
        {'num': 'EP06', 'title': 'ポコ森ソリ大会 パート2', 'sub_num': 'Episode 6-2'},
        {'num': 'EP06', 'title': 'ポコ森ソリ大会 パート１', 'sub_num': 'Episode 6-1'},
        {"num": "EP05", "title": "ティミーの忘れ物 パート2", 'sub_num': 'Episode 5-2'},
        {"num": "EP05", "title": "ティミーの忘れ物 パート1", 'sub_num': 'Episode 5-1'}, 
        {'num': 'EP04', 'title': 'ポコ森のホラ吹き王「クルグ」', 'sub_num': 'Episode 4'},
        {'num': 'EP03', 'title': 'ポコ森行方不明の謎', 'sub_num': 'Episode 3'},
        {'num': 'EP02', 'title': '母をたずねて三センチ', 'sub_num': 'Episode 2'},
        {'num': 'EP01', 'title': 'ミドリの歌', 'sub_num': 'Episode 1'},
    ],
    'en' : [
        {'num': 'EP11', 'title': 'Kroog VS Tygo'},
        {'num': 'EP10', 'title': "Berrie's Berry Very Special Training"},
        {'num': 'EP09', 'title': 'The Bizarre Song of Midori'},
        {'num': 'EP08', 'title': 'I Have a New Friend! Part 2'},
        {'num': 'EP08', 'title': 'I Have a New Friend! Part 1'},
        {'num': 'EP07', 'title': 'No Carrots!! Part 2'},
        {'num': 'EP07', 'title': 'No Carrots!! Part 1'},
        {'num': 'EP06', 'title': 'The Poko Forest Sled Race Part 2'},
        {'num': 'EP06', 'title': 'The Poko Forest Sled Race Part 1'},
        {"num": "EP05", "title": "Timmy's Autumn Part 2"},
        {"num": "EP05", "title": "Timmy's Autumn Part 1"}, 
        {'num': 'EP04', 'title': 'The biggest liar in all of Poko Forest'},
        {'num': 'EP03', 'title': 'The Mysterious Case of Poko Forest'},
        {'num': 'EP02', 'title': '3CM in Search of Mother'},
        {'num': 'EP01', 'title': 'The Song of Midori'},
    ],
    'ko' : [
        {'num': '11화', 'title': '크루그VS타이고'},
        {'num': '10화', 'title': '베리의 베리베리 특훈'},
        {'num': '9화', 'title': '미도리의 이상한 노래'},
        {'num': '8화', 'title': '새로운 친구가 생겼어! 2부'},
        {'num': '8화', 'title': '새로운 친구가 생겼어! 1부'},
        {'num': '7화', 'title': '당근이 없어졌어! 2부'},
        {'num': '7화', 'title': '당근이 없어졌어! 1부'},
        {'num': '6화', 'title': '포코숲의 썰매타기 대회 2부'},
        {'num': '6화', 'title': '포코숲의 썰매타기 대회 1부'},
        {'num': '5화', 'title': '티미의 가을나기 2부'},
        {'num': '5화', 'title': '티미의 가을나기 1부'},
        {'num': '4화', 'title': '포코숲 허세왕 크루그'},
        {'num': '3화', 'title': '포코숲 실종사건의 비밀'},
        {'num': '2화', 'title': '엄마 찾아 3CM'},
        {'num': '1화', 'title': '미도리의 노래'},
    ]
}

COMMON = {
    'length' : [
        {'window_minimal': 483, 'window_maximum': 2543, 'moving_bar_length': 469, 'latest_episode': 11},
    ],
    'text' : [
        {'language': '日本語', 'main_title': 'ポコパンのエピソード', 'latest_episode': '最新エピソード', 'other_episode': '他のエピソード', 'sns': 'ポコタと仲間の最新ニュース', '©copyright': '©Treenod Inc., All rights reserved.'},
        {'language': 'English', 'main_title': 'POKOPANG Episodes', 'latest_episode': 'The Latest Episode', 'other_episode': 'Other Episodes', 'sns': 'The latest news of Pokota and Friends!', '©copyright': '©Treenod Inc., All rights reserved.'},
        {'language': '한국어', 'main_title': '포코팡 에피소드', 'latest_episode': '최신 에피소드', 'other_episode': '다른 에피소드 보기', 'sns': '포코타와 친구들 최근 소식', '©copyright': '©Treenod Inc., All rights reserved.'},
    ],
    'SNS' : [
        {'facebook': 'ポコタ', 'instagram': 'pokopang.info', 'twitter': 'POKOTA【公式】'},
    ]
}

class TestEpisode(BaseTestCase):
    
    def wait_for_window(self, timeout = 3):
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def scroll_down(self): # 스크롤 > 하
        scroll_height = self.selenium.driver.execute_script("return document.body.scrollHeight") # 웹페이지 높이 측정
        scroll_dn_div = scroll_height / 10 # 웹페이지 길이를 10등분
        scroll_dn_divs = scroll_dn_div # 웹페이지 길이를 10등분된 값을 별도로 저장
        for i in range(10): # 10등분에 따라 10회 반복
            self.selenium.driver.execute_script("window.scrollTo(0, " + str(scroll_dn_div) + ")") # 웹페이지 길이의 1/10씩 스크롤 다운
            scroll_dn_div = scroll_dn_div + scroll_dn_divs
            if scroll_dn_div >= scroll_height: # 스크롤을 한 값이 웹페이지 길이와 같거나 크면 스크롤 비정상 동작으로 에러 처리
                self.assertTrue(scroll_dn_div, msg="Main Page Scroll Down Error")
            time.sleep(1)
    # for문으로 동작 시 에피소드 3~1(상하 스크롤 방식)에서 Error가 발생
    
    def scroll_up(self): # 스크롤 > 상
        self.selenium.driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);") # 웹페이지 시작점으로 바로 스크롤 업
        scroll_result = self.selenium.driver.execute_script("return window.scrollY") # 웹페이지 시작점의 값(scrollY)을 scroll_result에 저장
        if scroll_result > 0: # 시작점의 값은 0이니 스크롤 업해서 값이 0이 아니면 에러 처리
            self.assertTrue(scroll_result, msg="Main Page Scroll Up Error")
        time.sleep(1)

    def check_window_minimal(self): # 웹페이지 크기 최소화 (크롬(window) 기준)
        self.driver.set_window_size(500, 1280) # 최소화
        minimal = self.selenium.driver.execute_script("return document.body.scrollWidth") # 웹페이지 넓이 측정
        self.assertTrue(minimal==COMMON['length'][0]['window_minimal'], msg="Window Minimization Error") # 최소화 시 넓이값(483)과 비교
        time.sleep(1)

    def check_window_maximize(self): # 웹페이지 크기 최대화 (크롬(window) 기준)
        self.driver.maximize_window() # 최대화
        maximum = self.selenium.driver.execute_script("return document.body.scrollWidth") # 웹페이지 넓이 측정
        self.assertTrue(maximum==COMMON['length'][0]['window_maximum'], msg="Window Maximization Error") # 최대화 시 넓이값(2543)과 비교
        time.sleep(1)

    def check_main_thumbnail(self): # 메인 에피소드 영역 > 썸네일 이미지 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        main_thumbnail = self.selenium.wait('xpath', '//div[@class="img-shadow"]//img')
        if language == 'ja' :
            self.assertIsNotNone(main_thumbnail, msg="Main Episode - Thumbnail Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :
            self.assertIsNotNone(main_thumbnail, msg="Main Episode - Thumbnail Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertIsNotNone(main_thumbnail, msg="Main Episode - Thumbnail Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("Main Episode - Thumbnail Error (Language is empty.)")
        else:
            LOGGER.warning("Main Episode - Thumbnail Error (Unsupported language)")

    def check_dropdown_button_text(self): # 언어변경 > 드랍다운 텍스트 검증        
        japanese = self.selenium.get_text('css_selector', '#changeLanguage > option:nth-child(1)')
        self.assertTrue(japanese==COMMON['text'][0]['language'], msg="Dropdown Menu Text Error ({})".format(COMMON['text'][0]['language']))
        english = self.selenium.get_text('css_selector', '#changeLanguage > option:nth-child(2)')            
        self.assertTrue(english==COMMON['text'][1]['language'], msg="Dropdown Menu Text Error ({})".format(COMMON['text'][1]['language']))
        korean = self.selenium.get_text('css_selector', '#changeLanguage > option:nth-child(3)')            
        self.assertTrue(korean==COMMON['text'][2]['language'], msg="Dropdown Menu Text Error ({})".format(COMMON['text'][2]['language']))
    
    def check_main_title(self): # 메인 에피소드 영역 > 텍스트 언어 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        main_title = self.selenium.get_text('xpath', '//div[@class="header-shadow-main"]//h1')
        if language == 'ja' :            
            self.assertTrue(main_title==COMMON['text'][0]['main_title'], msg="Main Title Text Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :            
            self.assertTrue(main_title==COMMON['text'][1]['main_title'], msg="Main Title Text Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertTrue(main_title==COMMON['text'][2]['main_title'], msg="Main Title Text Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("Main Title Text Error (Language is empty.)")
        else:
            LOGGER.warning("Main Title Text Error (Unsupported language)")

    def check_latest_episode_text(self): # 최신 에피소드 영역 > 텍스트 언어 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        latest_episode_text = self.selenium.get_text('xpath', '//div[@class="main-title-1"]')
        if language == 'ja' :            
            self.assertTrue(latest_episode_text==COMMON['text'][0]['latest_episode'], msg="The Latest Episode - Text Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :            
            self.assertTrue(latest_episode_text==COMMON['text'][1]['latest_episode'], msg="The Latest Episode - Text Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertTrue(latest_episode_text==COMMON['text'][2]['latest_episode'], msg="The Latest Episode - Text Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("The Latest Episode - Text Error (Language is empty.)")
        else:
            LOGGER.warning("The Latest Episode - Text Error (Unsupported language)")
    
    def check_latest_episode_image(self): # 최신 에피소드 영역 > 이미지 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        latest_episode_image = self.selenium.wait('xpath', '//div[@class="responsive-image"]//img') # 최신 에피소드 이미지
        if language == 'ja' :            
            self.assertIsNotNone(latest_episode_image, msg="The Latest Episode - Image Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :            
            self.assertIsNotNone(latest_episode_image, msg="The Latest Episode - Image Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertIsNotNone(latest_episode_image, msg="The Latest Episode - Image Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("The Latest Episode - Image Error (Language is empty.)")
        else:
            LOGGER.warning("The Latest Episode - Image Error (Unsupported language)")
    
    def check_latest_episode_number(self): # 최신 에피소드 영역 > 회차 > 번호 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        latest_episode_number = self.selenium.get_text('xpath', '//p[@class="left-text"]') # 최신 에피소드 회차
        if language == 'ja' :            
            self.assertTrue(latest_episode_number==EPISODE['ja'][0]['num'], msg="The Latest Episode - Number Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :            
            self.assertTrue(latest_episode_number==EPISODE['en'][0]['num'], msg="The Latest Episode - Number Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertTrue(latest_episode_number==EPISODE['ko'][0]['num'], msg="The Latest Episode - Number Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("The Latest Episode - Number Error (Language is empty.)")
        else:
            LOGGER.warning("The Latest Episode - Number Error (Unsupported language)")

    def check_latest_episode_title(self): # 최신 에피소드 영역 > 제목 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        latest_episode_title = self.selenium.get_text('xpath', '//h1[@class="left-text"]') # 최신 에피소드 제목
        if language == 'ja' :            
            self.assertTrue(latest_episode_title==EPISODE['ja'][0]['title'], msg="The Latest Episode - Title Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :            
            self.assertTrue(latest_episode_title==EPISODE['en'][0]['title'], msg="The Latest Episode - Title Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertTrue(latest_episode_title==EPISODE['ko'][0]['title'], msg="The The Latest Episode - Title Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("The Latest Episode - Title Error (Language is empty.)")
        else:
            LOGGER.warning("The Latest Episode - Title Error (Unsupported language)")

    def check_other_episode_text(self): # 다른 에피소드 영역 > 텍스트 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        other_episode_text = self.selenium.get_text('xpath', '//div[@class="main-title-2"]') # 다른 에피소드 텍스트
        if language == 'ja' :            
            self.assertTrue(other_episode_text==COMMON['text'][0]['other_episode'], msg="Other Episode - Text Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :            
            self.assertTrue(other_episode_text==COMMON['text'][1]['other_episode'], msg="Other Episode - Text Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertTrue(other_episode_text==COMMON['text'][2]['other_episode'], msg="Other Episode - Text Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("Other Episode - Text Error (Language is empty.)")
        else:
            LOGGER.warning("Other Episode - Text Error (Unsupported language)")

    def check_other_episode_image(self): # 다른 에피소드 영역 > 이미지 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        for i in range((len(EPISODE['ko']))-1): # EPISODE 변수를 추가만 하면 관리 가능 (-1은 최신 에피소드를 제외)
            other_episode_image = self.selenium.wait('xpath', '//*[@id="__next"]/div[4]/div/div/div[2]/div[{}]/a/img'.format(i+1))
            if language == 'ja' :            
                self.assertIsNotNone(other_episode_image, msg="Other Episode - Image Error ({})".format(COMMON['text'][0]['language']))
            elif language == 'en' :            
                self.assertIsNotNone(other_episode_image, msg="Other Episode - Image Error ({})".format(COMMON['text'][1]['language']))
            elif language == 'ko' :                    
                self.assertIsNotNone(other_episode_image, msg="Other Episode - Image Error ({})".format(COMMON['text'][2]['language']))
            elif language == 'none' :
                LOGGER.warning("Other Episode - Image Error (Language is empty.)")
            else :
                LOGGER.warning("Other Episode - Image Error (Unsupported language)")
    
    def check_other_episode_number(self): # 다른 에피소드 영역 > 회차 > 번호 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        for i in range(1, (len(EPISODE['ko']))): # EPISODE 변수를 추가만 하면 관리 가능 (-1은 최신 에피소드를 제외)
            other_episode_number = self.selenium.wait('css_selector', '#__next > div:nth-child(4) > div > div > div.main-container > div:nth-child({}) > div > div.episode-subtitle'.format(i))
            if language == 'ja' :            
                self.assertIsNotNone(other_episode_number, msg="Other Episode - Number Error ({})".format(COMMON['text'][0]['language']))
            elif language == 'en' :            
                self.assertIsNotNone(other_episode_number, msg="Other Episode - Number Error ({})".format(COMMON['text'][1]['language']))
            elif language == 'ko' :                    
                self.assertIsNotNone(other_episode_number, msg="Other Episode - Number Error ({})".format(COMMON['text'][2]['language']))
            elif language == 'none' :
                LOGGER.warning("Other Episode - Number Error (Language is empty.)")
            else :
                LOGGER.warning("Other Episode - Number Error (Unsupported language)")

    def check_other_episode_title(self): # 다른 에피소드 영역 > 제목 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        for i in range(1, (len(EPISODE['ko']))): # EPISODE 변수를 추가만 하면 관리 가능 (-1은 최신 에피소드를 제외)
            other_episode_title = self.selenium.get_text('css_selector', '#__next > div:nth-child(4) > div > div > div.main-container > div:nth-child({}) > div > div.episode-title'.format(i))
            if language == 'ja' :            
                self.assertTrue(other_episode_title==EPISODE['ja'][i]['title'], msg="Other Episode - Title Error ({})".format(COMMON['text'][0]['language']))
            elif language == 'en' :            
                self.assertTrue(other_episode_title==EPISODE['en'][i]['title'], msg="Other Episode - Title Error ({})".format(COMMON['text'][1]['language']))
            elif language == 'ko' :                
                self.assertTrue(other_episode_title==EPISODE['ko'][i]['title'], msg="Other Episode - Title Error ({})".format(COMMON['text'][2]['language']))
            elif language == 'none' :
                LOGGER.warning("Other Episode - Title Error (Language is empty.)")
            else :
                LOGGER.warning("Other Episode - Title Error (Unsupported language)")

    def check_sns_title(self): # SNS 영역 > 텍스트 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        sns_title = self.selenium.get_text('xpath', '//div[@class="main-title-3"]')
        if language == 'ja' :            
            self.assertTrue(sns_title==COMMON['text'][0]['sns'], msg="SNS Title Text Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :            
            self.assertTrue(sns_title==COMMON['text'][1]['sns'], msg="SNS Title Text Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertTrue(sns_title==COMMON['text'][2]['sns'], msg="SNS Title Text Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("SNS Title Text Error (Language is empty.)")
        else:
            LOGGER.warning("SNS Title Text Error (Unsupported language)")
    
    def check_facebook_image(self): # SNS 영역 > 페이스북 > 이미지 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        facebook_image = self.selenium.wait('xpath', '//*[@id="__next"]/div[5]/div/div[2]/div[1]/a/img') # 페이스북 이미지
        if language == 'ja' :            
            self.assertIsNotNone(facebook_image, msg="Facebook Image Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :            
            self.assertIsNotNone(facebook_image, msg="Facebook Image Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertIsNotNone(facebook_image, msg="Facebook Image Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("Facebook Image Error (Language is empty.)")
        else:
            LOGGER.warning("Facebook Image Error (Unsupported language)")

    def check_instagram_image(self): # SNS 영역 > 인스타그램 > 이미지 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        instagram_image = self.selenium.wait('xpath', '//*[@id="__next"]/div[5]/div/div[2]/div[2]/a/img') # 인스타그램 이미지
        if language == 'ja' :
            self.assertIsNotNone(instagram_image, msg="Instagram Image Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :
            self.assertIsNotNone(instagram_image, msg="Instagram Image Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertIsNotNone(instagram_image, msg="Instagram Image Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("Instagram Image Error (Language is empty.)")
        else:
            LOGGER.warning("Instagram Image Error (Unsupported language)")

    def check_twitter_image(self): # SNS 영역 > 트위터 > 이미지 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        twitter_image = self.selenium.wait('xpath', '//*[@id="__next"]/div[5]/div/div[2]/div[3]/a/img') # 트위터 이미지
        if language == 'ja' :
            self.assertIsNotNone(twitter_image, msg="Twitter Image Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :
            self.assertIsNotNone(twitter_image, msg="Twitter Image Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertIsNotNone(twitter_image, msg="Twitter Image Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("Twitter Image Error (Language is empty.)")
        else:
            LOGGER.warning("Twitter Image Error (Unsupported language)")

    def check_copyright_text(self): # ⓒcopyright 영역 텍스트 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        copyright = self.selenium.get_text('xpath', "//p[@class='copyright center-text no-bottom']") # copyright 텍스트
        if language == 'ja' :            
            self.assertTrue(copyright==COMMON['text'][0]['©copyright'], msg="©copyright Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :            
            self.assertTrue(copyright==COMMON['text'][1]['©copyright'], msg="©copyright Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertTrue(copyright==COMMON['text'][2]['©copyright'], msg="©copyright Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("SNS Title Text Error (Language is empty.)")
        else:
            LOGGER.warning("SNS Title Text Error (Unsupported language)")

    def check_latest_episode_image_click(self): # 최신 에피소드 클릭 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")        
        self.selenium.wait('xpath', "//div[@class='responsive-image']//img").click() # 최신 에피소드 페이지로 이동
        latest_episode_click_image = self.selenium.wait('xpath', '//div[@class="swiper-slide swiper-slide-active"]//img')
        if language == 'ja' :            
            self.assertIsNotNone(latest_episode_click_image, msg="The Latest Episode - Click Error ({})".format(COMMON['text'][0]['language']))
            time.sleep(3)
            self.selenium.driver.back()
            current_page = self.selenium.wait('class_name', 'text-area', timeout=5)
            self.assertIsNotNone(current_page, msg="The Latest Episode - Back Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :            
            self.assertIsNotNone(latest_episode_click_image, msg="The Latest Episode - Click Error ({})".format(COMMON['text'][1]['language']))
            time.sleep(3)
            self.selenium.driver.back()
            current_page = self.selenium.wait('class_name', 'text-area', timeout=5)
            self.assertIsNotNone(current_page, msg="The Latest Episode - Back Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertIsNotNone(latest_episode_click_image, msg="The Latest Episode - Click Error ({})".format(COMMON['text'][2]['language']))
            time.sleep(3)
            self.selenium.driver.back()
            current_page = self.selenium.wait('class_name', 'text-area', timeout=5)
            self.assertIsNotNone(current_page, msg="The Latest Episode - Back Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("The Latest Episode - Back Error (Language is empty.)")
        else:
            LOGGER.warning("The Latest Episode - Back Error (Unsupported language)")

    def check_other_episode_image_click_2(self): # 다른 에피소드(10~4화) 클릭 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        if language == 'ja' :
            for i in range((len(EPISODE['ko']))-1-3): # EPISODE 변수를 추가만 하면 관리 가능 (-1은 최신 에피소드를 제외, -3은 상하 스크롤 방식 에피소드를 제외)
                self.selenium.wait('xpath', "/html[1]/body[1]/div[1]/div[4]/div[1]/div[1]/div[2]/div[{}]/a[1]/img[1]".format(i+1)).click() # 다른 에피소드 페이지로 이동
                other_episode_click_image = self.selenium.wait('xpath', '//div[@class="swiper-slide swiper-slide-active"]//img')            
                self.assertIsNotNone(other_episode_click_image, msg="Other Episode - Click Error ({})".format(COMMON['text'][0]['language']))
                time.sleep(3) # 페이지 로딩이 될 떄까지 대기
                self.selenium.driver.back() # 이전 페이지로 돌아가기
                current_page = self.selenium.wait('class_name', 'text-area', timeout=5) # 이전 페이지에서 'class_name'과 'text-area'를 찾기
                self.assertIsNotNone(current_page, msg="Other Episodes - {} Back Error (ja)".format(EPISODE['ja'][i+1]['num'])) # 최신 에피소드를 제외하고 표시
        elif language == 'en' :
            for i in range((len(EPISODE['ko']))-1-3):
                self.selenium.wait('xpath', "/html[1]/body[1]/div[1]/div[4]/div[1]/div[1]/div[2]/div[{}]/a[1]/img[1]".format(i+1)).click()
                other_episode_click_image = self.selenium.wait('xpath', '//div[@class="swiper-slide swiper-slide-active"]//img')            
                self.assertIsNotNone(other_episode_click_image, msg="Other Episode - Click Error ({})".format(COMMON['text'][1]['language']))
                time.sleep(3)
                self.selenium.driver.back()
                current_page = self.selenium.wait('class_name', 'text-area', timeout=5)
                self.assertIsNotNone(current_page, msg="Other Episodes - {} Back Error (en)".format(EPISODE['en'][i+1]['num']))
        elif language == 'ko' :
            for i in range((len(EPISODE['ko']))-1-3):
                self.selenium.wait('xpath', "/html[1]/body[1]/div[1]/div[4]/div[1]/div[1]/div[2]/div[{}]/a[1]/img[1]".format(i+1)).click()
                other_episode_click_image = self.selenium.wait('xpath', '//div[@class="swiper-slide swiper-slide-active"]//img')            
                self.assertIsNotNone(other_episode_click_image, msg="Other Episode - Click Error ({})".format(COMMON['text'][2]['language']))
                time.sleep(3)
                self.selenium.driver.back()
                current_page = self.selenium.wait('class_name', 'text-area', timeout=5)                
                self.assertIsNotNone(current_page, msg="Other Episodes - {} Back Error (ko)".format(EPISODE['ko'][(i+1)]['num']))
        elif language == 'none' :
            LOGGER.warning("Other Episodes Page Move Error (Language is empty.)")
        else:
            LOGGER.warning("Other Episodes Page Move (Unsupported language)")

    def check_other_episode_image_click_1(self): # 다른 에피소드(3~1화) 클릭 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        if language == 'ja' :
            for i in range(1,4): # 상하 스크롤 방식 에피소드 개수만큼 반복
                self.selenium.wait('xpath', "/html[1]/body[1]/div[1]/div[4]/div[1]/div[1]/div[2]/div[{}]/a[1]/img[1]".format(i+COMMON['length'][0]['latest_episode'])).click() # 반복 횟수 + 최신 에피소드 번호가 해당 에피소드 경로 번호
                other_image = self.selenium.wait('xpath', '//*[@id="toon_content"]/div[1]/div/img[1]')            
                self.assertIsNotNone(other_image, msg="Other Episode - Click Error ({})".format(COMMON['text'][0]['language']))
                time.sleep(3) # 페이지 로딩이 될 떄까지 대기
                self.selenium.driver.back() # 이전 페이지로 돌아가기
                current_page = self.selenium.wait('class_name', 'text-area', timeout=5) # 이전 페이지에서 'class_name'과 'text-area'를 찾기                
                self.assertIsNotNone(current_page, msg="Other Episodes {} Back Error (ja)".format(EPISODE['ja'][i+10+1]['num'])) # 최신 에피소드 + 다른 에피소드 1~3화를 제외하고 표시
        elif language == 'en' :
            for i in range(1,4):                
                self.selenium.wait('xpath', "/html[1]/body[1]/div[1]/div[4]/div[1]/div[1]/div[2]/div[{}]/a[1]/img[1]".format(i+COMMON['length'][0]['latest_episode'])).click()
                other_image = self.selenium.wait('xpath', '//*[@id="toon_content"]/div[1]/div/img[1]')            
                self.assertIsNotNone(other_image, msg="Other Episode - Click Error ({})".format(COMMON['text'][1]['language']))
                time.sleep(3)
                self.selenium.driver.back()
                current_page = self.selenium.wait('class_name', 'text-area', timeout=5)                
                self.assertIsNotNone(current_page, msg="Other Episodes {} Back Error (en)".format(EPISODE['en'][i+10+1]['num']))
        elif language == 'ko' :
            for i in range(1,4):
                self.selenium.wait('xpath', "/html[1]/body[1]/div[1]/div[4]/div[1]/div[1]/div[2]/div[{}]/a[1]/img[1]".format(i+COMMON['length'][0]['latest_episode'])).click()
                other_image = self.selenium.wait('xpath', '//*[@id="toon_content"]/div[1]/div/img[1]')            
                self.assertIsNotNone(other_image, msg="Other Episode - Click Error ({})".format(COMMON['text'][2]['language']))
                time.sleep(3)
                self.selenium.driver.back()
                current_page = self.selenium.wait('class_name', 'text-area', timeout=5)                
                self.assertIsNotNone(current_page, msg="Other Episodes {} Back Error (ko)".format(EPISODE['ko'][i+10+1]['num']))
        elif language == 'none' :
            LOGGER.warning("Other Episodes Page Move Error (Language is empty.)")
        else:
            LOGGER.warning("Other Episodes Page Move (Unsupported language)")

    def check_facebook_click(self): # 페이스북 클릭 검증
        self.vars["window_handles"] = self.selenium.driver.window_handles
        self.selenium.wait('css_selector', "#__next > div.main-body-2 > div > div.no-bottom > div:nth-child(1) > a > img").click()
        self.vars["win1000"] = self.wait_for_window(2000)
        self.vars["root"] = self.selenium.driver.current_window_handle
        self.selenium.driver.switch_to.window(self.vars["win1000"])
        time.sleep(3)
        facebook_title = self.selenium.get_text('xpath', '//*[@id="seo_h1_tag"]/a/span') # Pokopang 페이스북인지 확인
        self.assertTrue(facebook_title==COMMON['SNS'][0]['facebook'], msg="This page not pokopang facebook.")
        self.selenium.driver.switch_to.window(self.vars["root"]) # 이전 창(메인 에피소드 페이지)로 이동
        time.sleep(1)

    def check_instagram_click(self): # 인스타그램 클릭 검증
        self.vars["window_handles"] = self.selenium.driver.window_handles
        self.selenium.wait('css_selector', "#__next > div.main-body-2 > div > div.no-bottom > div:nth-child(2) > a > img").click()
        self.vars["win1001"] = self.wait_for_window(2000)
        self.vars["root"] = self.selenium.driver.current_window_handle
        self.selenium.driver.switch_to.window(self.vars["win1001"])
        time.sleep(3)
        instagram_title = self.selenium.get_text('xpath', '//*[@id="react-root"]/section/main/div/header/section/div[1]/h2') # Pokopang 인스타그램인지 확인
        self.assertTrue(instagram_title==COMMON['SNS'][0]['instagram'], msg="This page not pokopang instagram.")
        self.selenium.driver.switch_to.window(self.vars["root"]) # 이전 창(메인 에피소드 페이지)로 이동
        time.sleep(1)

    def check_twitter_click(self): # 트위터 클릭 검증
        self.vars["window_handles"] = self.selenium.driver.window_handles
        self.selenium.wait('css_selector', "#__next > div.main-body-2 > div > div.no-bottom > div:nth-child(3) > a > img").click()
        self.vars["win1002"] = self.wait_for_window(2000)
        self.vars["root"] = self.selenium.driver.current_window_handle
        self.selenium.driver.switch_to.window(self.vars["win1002"])
        time.sleep(3)
        twitter_title = self.selenium.get_text('xpath', '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/span[1]/span') # Pokopang 트위터인지 확인
        self.assertTrue(twitter_title==COMMON['SNS'][0]['twitter'], msg="This page not pokopang twitter.")        
        self.selenium.driver.switch_to.window(self.vars["root"]) # 이전 창(메인 에피소드 페이지)로 이동
        time.sleep(1)

    def check_move_to_latest_episode(self): # 메인 에피소드 > 최신 에피소드 페이지 이동 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        self.selenium.wait('xpath', "//div[@class='responsive-image']//img").click() # 최신 에피소드 페이지로 이동
        latest_episode = self.selenium.wait('xpath', "//div[@class='swiper-slide swiper-slide-active']//img") # 최신 에피소드 첫 웹툰 이미지
        if language == 'ja' :
            self.assertIsNotNone(latest_episode, msg="The Latest Episode - Move Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :
            self.assertIsNotNone(latest_episode, msg="The Latest Episode - Move Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertIsNotNone(latest_episode, msg="The Latest Episode - Move Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("The Latest Episode - Move Error (Language is empty.)")
        else:
            LOGGER.warning("The Latest Episode - Move Error (Unsupported language)")

    def check_upper_number(self): # 최신 에피소드 > 상단 영역 > 회차 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        upper_number = self.selenium.get_text('xpath', "//*[@id='cbp-spmenu-s3']/div/div/div[2]/h6")
        if language == 'ja' :            
            self.assertTrue(upper_number==EPISODE['ja'][0]['sub_num'], msg="The Latest Episode - Upper Number Error ({})".format(COMMON['text'][0]['language'])) # 회차(sub_num)는 'ja'에서 모두 가져옴
        elif language == 'en' :            
            self.assertTrue(upper_number==EPISODE['ja'][0]['sub_num'], msg="The Latest Episode - Upper Number Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :            
            self.assertTrue(upper_number==EPISODE['ja'][0]['sub_num'], msg="The Latest Episode - Upper Number Error  ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("The Latest Episode - Upper Number Error (Language is empty.)")
        else:
            LOGGER.warning("The Latest Episode - Upper Number Error (Unsupported language)")

    def check_upper_title(self): # 최신 에피소드 > 상단 영역 > 제목 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        upper_title = self.selenium.get_text('xpath', "//*[@id='cbp-spmenu-s3']/div/div/div[2]/h2")
        if language == 'ja' :            
            self.assertTrue(upper_title==EPISODE['ja'][0]['title'], msg="The Latest Episode - Upper Title Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :            
            self.assertTrue(upper_title==EPISODE['en'][0]['title'], msg="The Latest Episode - Upper Title Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertTrue(upper_title==EPISODE['ko'][0]['title'], msg="The Latest Episode - Upper Title Error  ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("The Latest Episode - Upper Title Error (Language is empty.)")
        else:
            LOGGER.warning("The Latest Episode - Upper Title Error (Unsupported language)")

    def check_upper_image(self): # 최신 에피소드 > 상단 영역 > 이미지 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        upper_image = self.selenium.wait('xpath', '//*[@id="cbp-spmenu-s3"]/div/div/div[1]/img')
        if language == 'ja' :
            self.assertIsNotNone(upper_image, msg="The Latest Episode - Upper Image Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :
            self.assertIsNotNone(upper_image, msg="The Latest Episode - Upper Image Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertIsNotNone(upper_image, msg="The Latest Episode - Upper Image Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("The Latest Episode - Upper Image Error (Language is empty.)")
        else:
            LOGGER.warning("The Latest Episode - Upper Image Error (Unsupported language)")

    def check_menu_icon(self): # 최신 에피소드 > 상단 영역 > 메뉴 아이콘 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        menu_icon = self.selenium.wait('xpath', '//*[@id="cbp-spmenu-s3"]/div/div/div[3]/a/img')
        if language == 'ja' :
            self.assertIsNotNone(menu_icon, msg="The Latest Episode - Menu Icon Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :
            self.assertIsNotNone(menu_icon, msg="The Latest Episode - Menu Icon Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertIsNotNone(menu_icon, msg="The Latest Episode - Menu Icon Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("The Latest Episode - Menu Icon Error (Language is empty.)")
        else:
            LOGGER.warning("The Latest Episode - Menu Icon Error (Unsupported language)")

    def check_click_image_to_next(self): # 중단 영역 > 이미지 > 다음 페이지 넘기기 & 마지막 페이지 넘기기 불가 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")        
        page_num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div') # 변경된 페이지에서 페이지 수(xx/xx)의 값을 찾음
        page_all = page_num.split('/')[1] # 페이지 수(xx/xx)의 값에서 앞 부분 현재 페이지 부분을 삭제하여 전체 페이지 수의 값만 남김
        episode = self.selenium.get_text('xpath', '//*[@id="cbp-spmenu-s3"]/div/div/div[2]/h6') # 해당 에피소드 'Episode XX'를 찾음
        episode_num = episode.split(' ')[1] # 해당 에피소드 'Episode XX'에서 'Episode' 부분을 삭제하여 에피소드 번호만 남김        
        time.sleep(2)
        if language == 'ja' :
            for i in range(1,int(page_all)+1): # 전체 페이지 수의 값만큼 반복                
                page_num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div') # 변경된 페이지에서 페이지 수(xx/xx)의 값을 다시 찾음           
                page_current = page_num.split('/')[0] # 페이지 수(xx/xx)의 값에서 뒷 부분 전체 페이지 부분을 삭제하여 현재 페이지 수의 값만 남김            
                webtoon_image = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))            
                self.assertTrue(i == int(page_current), msg="This page not {} page. (日本語)".format(i)) # 페이지 번호가 맞지 않으면 페이지 번호를 알려줌            
                if int(page_current) < int(page_all): # 현재 페이지가 전체 페이지보다 작을 때
                    self.assertIsNotNone(webtoon_image, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i)) # 웹툰 이미지가 나오지 않으면 안나온 페이지 번호를 알려줌
                if int(page_current) == int(page_all): # 현재 페이지가 전체 페이지보다 같을 때 (마지막 페이지 도달)
                    self.assertIsNone(webtoon_image, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i)) # 마지막 페이지로 웹툰 이미지가 나오지 않아야 함
                    last_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[3]') # 마지막 페이지에 'class="swiper-button-next swiper-button-disabled"'가 없으면 Fail
                    self.assertIsNotNone(last_page, msg="This page not last page. (日本語)")                                
                    break
                self.selenium.wait('xpath', '//div[@class="swiper-button-next"]').click()
        if language == 'en' :
            for i in range(1,int(page_all)+1):                
                page_num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                page_current = page_num.split('/')[0]
                webtoon_image = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))            
                self.assertTrue(i == int(page_current), msg="This page not {} page. (English)".format(i))
                if int(page_current) < int(page_all):
                    self.assertIsNotNone(webtoon_image, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                if int(page_current) == int(page_all):
                    self.assertIsNone(webtoon_image, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                    last_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[3]')
                    self.assertIsNotNone(last_page, msg="This page not last page. (English)")                                
                    break
                self.selenium.wait('xpath', '//div[@class="swiper-button-next"]').click()
        if language == 'ko' :
            for i in range(1,int(page_all)+1):
                page_num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                page_current = page_num.split('/')[0]
                webtoon_image = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))            
                self.assertTrue(i == int(page_current), msg="This page not {} page. (한국어)".format(i))
                if int(page_current) < int(page_all):
                    self.assertIsNotNone(webtoon_image, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                if int(page_current) == int(page_all):
                    self.assertIsNone(webtoon_image, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                    last_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[3]')
                    self.assertIsNotNone(last_page, msg="This page not last page. (한국어)")                                
                    break
                self.selenium.wait('xpath', '//div[@class="swiper-button-next"]').click()
        elif language == 'none' :
            LOGGER.warning("Image Click Next Error (Language is empty.)")
        else:
            LOGGER.warning("Image Click Next Error (Unsupported language)")

    def check_click_image_to_previous(self): # 중단 영역 > 이미지 > 이전 페이지 돌아가기 & 마지막 이전 페이지 넘기기 불가 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")        
        page_num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
        page_all = page_num.split('/')[1]        
        episode = self.selenium.get_text('xpath', '//*[@id="cbp-spmenu-s3"]/div/div/div[2]/h6')
        episode_num = episode.split(' ')[1]        
        time.sleep(2)
        if language == 'ja' :
            for i in reversed(range(1,int(page_all)+1)): # 카운트 순서를 역순으로 전환              
                webtoon_image = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                page_num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div') # 변경된 페이지에서 페이지 수(xx/xx)의 값을 다시 찾음           
                page_current = page_num.split('/')[0] # 페이지 수(xx/xx)의 값에서 뒷 부분 전체 페이지 부분을 삭제하여 현재 페이지 수의 값만 남김                
                self.assertTrue(i == int(page_current), msg="This page not {} page. (日本語)".format(i)) # 페이지 번호가 맞지 않으면 페이지 번호를 알려줌            
                if int(page_current) < int(page_all): # 현재 페이지가 전체 페이지보다 작을 때
                    self.assertIsNotNone(webtoon_image, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i)) # 웹툰 이미지가 나오지 않으면 안나온 페이지 번호를 알려줌                    
                if int(page_current) == int(page_all): # 현재 페이지가 전체 페이지보다 같을 때
                    self.assertIsNone(webtoon_image, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i)) # 마지막 페이지로 웹툰 이미지가 나오지 않아야 함
                if int(page_current) == 1: # 현재 페이지가 첫 페이지(1)일 때
                    first_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[4]') # 첫 페이지에 'swiper-button-prev swiper-button-disabled"'가 없으면 Fail
                    self.assertIsNotNone(first_page, msg="This page not first page. (日本語)")                    
                self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[4]').click()
        if language == 'en' :
            for i in reversed(range(1,int(page_all)+1)):
                webtoon_image = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))            
                page_num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                page_current = page_num.split('/')[0]                
                self.assertTrue(i == int(page_current), msg="This page not {} page. (English)".format(i))
                if int(page_current) < int(page_all): # 현재 페이지가 전체 페이지보다 작을 때
                    self.assertIsNotNone(webtoon_image, msg="Episode {} - {} Page Error (English)".format(episode_num, i)) # 웹툰 이미지가 나오지 않으면 안나온 페이지 번호를 알려줌                    
                if int(page_current) == int(page_all): # 현재 페이지가 전체 페이지보다 같을 때
                    self.assertIsNone(webtoon_image, msg="Episode {} - {} Page Error (English)".format(episode_num, i)) # 마지막 페이지로 웹툰 이미지가 나오지 않아야 함
                if int(page_current) == 1: # 현재 페이지가 첫 페이지(1)일 때
                    first_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[4]') # 첫 페이지에 'swiper-button-prev swiper-button-disabled"'가 없으면 Fail
                    self.assertIsNotNone(first_page, msg="This page not first page. (日本語)")                    
                self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[4]').click()
        if language == 'ko' :
            for i in reversed(range(1,int(page_all)+1)):                
                webtoon_image = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))            
                page_num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                page_current = page_num.split('/')[0]                
                self.assertTrue(i == int(page_current), msg="This page not {} page. (한국어)".format(i))
                if int(page_current) < int(page_all): # 현재 페이지가 전체 페이지보다 작을 때
                    self.assertIsNotNone(webtoon_image, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i)) # 웹툰 이미지가 나오지 않으면 안나온 페이지 번호를 알려줌                    
                if int(page_current) == int(page_all): # 현재 페이지가 전체 페이지보다 같을 때
                    self.assertIsNone(webtoon_image, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i)) # 마지막 페이지로 웹툰 이미지가 나오지 않아야 함
                if int(page_current) == 1: # 현재 페이지가 첫 페이지(1)일 때
                    first_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[4]') # 첫 페이지에 'swiper-button-prev swiper-button-disabled"'가 없으면 Fail
                    self.assertIsNotNone(first_page, msg="This page not first page. (한국어)")                    
                self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[4]').click()
        elif language == 'none' :
            LOGGER.warning("Image Click Previous Error (Language is empty.)")
        else:
            LOGGER.warning("Image Click Previous Error (Unsupported language)")
    
    def check_drag_and_drop_to_next(self): # 중단 영역 > 이미지 > 다음 페이지 넘기기 & 마지막 페이지 넘기기 불가 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")        
        repeat = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
        repeat_all = repeat.split('/')[1]        
        length = int(COMMON['length'][0]['moving_bar_length']) / (int(repeat_all)-1) # 1~21까지 20번을 이동
        episode = self.selenium.get_text('xpath', '//*[@id="cbp-spmenu-s3"]/div/div/div[2]/h6') # 해당 에피소드 'Episode XX'를 찾음
        episode_num = episode.split(' ')[1] # 해당 에피소드 'Episode XX'에서 'Episode' 부분을 삭제하여 에피소드 번호만 남김        
        time.sleep(2)
        if language == 'ja' :
            for i in range(1,int(repeat_all)+1):
                if i == 1: # 카운트가 1일 때는 드래그&드롭을 하지 않음
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (日本語)".format(i))
                if i > 1: # 카운트 2부터 드래그&드롭을 시작
                    moving_cursor = self.selenium.wait('xpath', '//*[@id="footer"]/div[1]/div/div[2]/div/span/span[1]/div') # 이동커서                    
                    actions = ActionChains(self.driver)
                    actions.drag_and_drop_by_offset(moving_cursor, int(-length), 0).perform() # 페이지 이동바를 드래그&드롭으로 이동 (전체에서 0으로)
                    time.sleep(1) # 클릭이 될 수 있도록 대기
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (日本語)".format(i))        
            last_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[3]')
            self.assertIsNotNone(last_page, msg="This page not last page. (日本語)") # 마지막 페이지에 웹툰 이미지가 나오면 마지막 페이지가 아니기 때문에
        if language == 'en' :
            for i in range(1,int(repeat_all)+1):
                if i == 1: # 카운트가 1일 때는 드래그&드롭을 하지 않음
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (English)".format(i))
                if i > 1: # 카운트 2부터 드래그&드롭을 시작
                    moving_cursor = self.selenium.wait('xpath', '//*[@id="footer"]/div[1]/div/div[2]/div/span/span[1]/div') # 이동커서                    
                    actions = ActionChains(self.driver)
                    actions.drag_and_drop_by_offset(moving_cursor, int(-length), 0).perform() # 페이지 이동바를 드래그&드롭으로 이동 (전체에서 0으로)
                    time.sleep(1) # 클릭이 될 수 있도록 대기
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (English)".format(i))        
            last_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[3]')
            self.assertIsNotNone(last_page, msg="This page not last page. (English)") # 마지막 페이지에 웹툰 이미지가 나오면 마지막 페이지가 아니기 때문에
        if language == 'ko' :
            for i in range(1,int(repeat_all)+1):
                if i == 1: # 카운트가 1일 때는 드래그&드롭을 하지 않음
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (한국어)".format(i))
                if i > 1: # 카운트 2부터 드래그&드롭을 시작
                    moving_cursor = self.selenium.wait('xpath', '//*[@id="footer"]/div[1]/div/div[2]/div/span/span[1]/div') # 이동커서                    
                    actions = ActionChains(self.driver)
                    actions.drag_and_drop_by_offset(moving_cursor, int(-length), 0).perform() # 페이지 이동바를 드래그&드롭으로 이동 (전체에서 0으로)
                    time.sleep(1) # 클릭이 될 수 있도록 대기
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (한국어)".format(i))        
            last_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[3]')
            self.assertIsNotNone(last_page, msg="This page not last page. (한국어)") # 마지막 페이지에 웹툰 이미지가 나오면 마지막 페이지가 아니기 때문에
        elif language == 'none' :
            LOGGER.warning("Moving Bar Drag & Drop Next Error (Language is empty.)")
        else:
            LOGGER.warning("Moving Bar Drag & Drop Next Error (Unsupported language)")

    def check_drag_and_drop_to_previous(self): # 하단 영역 > 페이지 이동바 > 드래그&드롭 > 이전 페이지 돌아가기 & 마지막 이전 페이지 돌아가기 불가 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")        
        repeat = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
        repeat_all = repeat.split('/')[1]        
        length = int(COMMON['length'][0]['moving_bar_length']) / (int(repeat_all)-1) # 1~21까지 20번을 이동
        episode = self.selenium.get_text('xpath', '//*[@id="cbp-spmenu-s3"]/div/div/div[2]/h6') # 해당 에피소드 'Episode XX'를 찾음
        episode_num = episode.split(' ')[1] # 해당 에피소드 'Episode XX'에서 'Episode' 부분을 삭제하여 에피소드 번호만 남김        
        time.sleep(2)
        if language == 'ja' :
            for i in reversed(range(1,int(repeat_all)+1)): # 카운트 순서를 역순으로 전환
                if i == int(repeat_all): # 마지막 페이지일 때는 마우스 이동을 하지 않음
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (日本語)".format(i))
                if i < int(repeat_all):                
                    moving_cursor = self.selenium.wait('xpath', '//*[@id="footer"]/div[1]/div/div[2]/div/span/span[1]/div') # 이동커서
                    actions = ActionChains(self.driver)
                    actions.drag_and_drop_by_offset(moving_cursor, int(length), 0).perform() # 페이지 이동바를 드래그&드롭으로 이동 (전체에서 0으로)
                    time.sleep(1) # 클릭이 될 수 있도록 대기                
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (日本語)".format(i))        
            first_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[4]')
            self.assertIsNotNone(first_page, msg="This page not first page. (日本語)") # 첫 페이지로 돌아가는 버튼이 나오면 첫 페이지가 아니기 때문에
        if language == 'en' :
            for i in reversed(range(1,int(repeat_all)+1)): # 카운트 순서를 역순으로 전환
                if i == int(repeat_all): # 마지막 페이지일 때는 마우스 이동을 하지 않음
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (English)".format(i))
                if i < int(repeat_all):                
                    moving_cursor = self.selenium.wait('xpath', '//*[@id="footer"]/div[1]/div/div[2]/div/span/span[1]/div') # 이동커서
                    actions = ActionChains(self.driver)
                    actions.drag_and_drop_by_offset(moving_cursor, int(length), 0).perform() # 페이지 이동바를 드래그&드롭으로 이동 (전체에서 0으로)
                    time.sleep(1) # 클릭이 될 수 있도록 대기                
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (English)".format(i))        
            first_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[4]')
            self.assertIsNotNone(first_page, msg="This page not first page. (English)") # 첫 페이지로 돌아가는 버튼이 나오면 첫 페이지가 아니기 때문에
        if language == 'ko' :
            for i in reversed(range(1,int(repeat_all)+1)): # 카운트 순서를 역순으로 전환
                if i == int(repeat_all): # 마지막 페이지일 때는 마우스 이동을 하지 않음
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (한국어)".format(i))
                if i < int(repeat_all):                
                    moving_cursor = self.selenium.wait('xpath', '//*[@id="footer"]/div[1]/div/div[2]/div/span/span[1]/div') # 이동커서
                    actions = ActionChains(self.driver)
                    actions.drag_and_drop_by_offset(moving_cursor, int(length), 0).perform() # 페이지 이동바를 드래그&드롭으로 이동 (전체에서 0으로)
                    time.sleep(1) # 클릭이 될 수 있도록 대기                
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (ko)".format(i))        
            first_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[4]')
            self.assertIsNotNone(first_page, msg="This page not first page. (한국어)") # 첫 페이지로 돌아가는 버튼이 나오면 첫 페이지가 아니기 때문에
        elif language == 'none' :
            LOGGER.warning("Moving Bar Drag & Drop Previous Error (Language is empty.)")
        else:
            LOGGER.warning("Moving Bar Drag & Drop Previous Error (Unsupported language)")

    def check_movingbar_click_to_next(self): # 하단 영역 > 페이지 이동바 > 클릭 > 다음 페이지 넘기기 & 다음 페이지 넘기기 불가 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        repeat = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
        repeat_all = repeat.split('/')[1]
        length = int(COMMON['length'][0]['moving_bar_length']) / (int(repeat_all)-1)
        episode = self.selenium.get_text('xpath', '//*[@id="cbp-spmenu-s3"]/div/div/div[2]/h6')
        episode_num = episode.split(' ')[1]
        time.sleep(2)        
        if language == 'ja' :
            for i in range(1,int(repeat_all)+1):
                if i == 1: # 카운트가 1일 때는 마우스 이동을 하지 않음
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (日本語)".format(i))
                if i > 1: # 카운트 2부터 마우스 이동을 시작
                    length_distance = (length * i) - length # 마우스가 움직여야 하는 거리값
                    moving_bar = self.selenium.wait('xpath', '//*[@id="footer"]/div[1]/div/div[2]/div') # 이동바
                    actions = ActionChains(self.driver)
                    actions.move_to_element_with_offset(moving_bar, int(COMMON['length'][0]['moving_bar_length']) - length_distance, 0).click().perform() # 이동바에서 클릭해서 한 페이지씩 넘기기
                    time.sleep(1) # 클릭이 될 수 있도록 대기                
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (日本語)".format(i))        
            last_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[3]')
            self.assertIsNotNone(last_page, msg="This page not last page. (日本語)")                     
        if language == 'en' :
            for i in range(1,int(repeat_all)+1):
                if i == 1: # 카운트가 1일 때는 마우스 이동을 하지 않음
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (English)".format(i))
                if i > 1: # 카운트 2부터 마우스 이동을 시작
                    length_distance = (length * i) - length # 마우스가 움직여야 하는 거리값
                    moving_bar = self.selenium.wait('xpath', '//*[@id="footer"]/div[1]/div/div[2]/div') # 이동바
                    actions = ActionChains(self.driver)
                    actions.move_to_element_with_offset(moving_bar, int(COMMON['length'][0]['moving_bar_length']) - length_distance, 0).click().perform() # 이동바에서 클릭해서 한 페이지씩 넘기기
                    time.sleep(1) # 클릭이 될 수 있도록 대기                
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (English)".format(i))        
            last_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[3]')
            self.assertIsNotNone(last_page, msg="This page not last page. (English)")                
        if language == 'ko' :
            for i in range(1,int(repeat_all)+1):
                if i == 1: # 카운트가 1일 때는 마우스 이동을 하지 않음
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (한국어)".format(i))
                if i > 1: # 카운트 2부터 마우스 이동을 시작
                    length_distance = (length * i) - length # 마우스가 움직여야 하는 거리값
                    moving_bar = self.selenium.wait('xpath', '//*[@id="footer"]/div[1]/div/div[2]/div') # 이동바
                    actions = ActionChains(self.driver)
                    actions.move_to_element_with_offset(moving_bar, int(COMMON['length'][0]['moving_bar_length']) - length_distance, 0).click().perform() # 이동바에서 클릭해서 한 페이지씩 넘기기
                    time.sleep(1) # 클릭이 될 수 있도록 대기                
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (한국어)".format(i))        
            last_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[3]')
            self.assertIsNotNone(last_page, msg="This page not last page. (한국어)")
        elif language == 'none' :
            LOGGER.warning("Moving Bar Click Next Error (Language is empty.)")
        else:
            LOGGER.warning("Moving Bar Click Next Error (Unsupported language)")

    def check_movingbar_click_to_previous(self): # 하단 영역 > 페이지 이동바 > 클릭 > 이전 페이지 넘기기 & 이전 페이지 넘기기 불가 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        repeat = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
        repeat_all = repeat.split('/')[1]
        length = int(COMMON['length'][0]['moving_bar_length']) / (int(repeat_all)-1)
        episode = self.selenium.get_text('xpath', '//*[@id="cbp-spmenu-s3"]/div/div/div[2]/h6')
        episode_num = episode.split(' ')[1]
        time.sleep(2)        
        
        if language == 'ja' :
            for i in reversed(range(1,int(repeat_all)+1)): # 카운트 순서를 역순으로 전환
                if i == int(repeat_all): # 마지막 페이지일 때는 마우스 이동을 하지 않음
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (日本語)".format(i))
                if i < int(repeat_all): # 마지막 페이지 이전부터 마우스 이동을 시작
                    length_distance = (length * i) - length # 마우스가 움직여야 하는 거리값

                    moving_bar = self.selenium.wait('xpath', '//*[@id="footer"]/div[1]/div/div[2]/div') # 이동바

                    actions = ActionChains(self.driver)
                    actions.move_to_element_with_offset(moving_bar, int(COMMON['length'][0]['moving_bar_length']) - length_distance, 0).click().perform() # 이동바에서 클릭해서 한 페이지씩 넘기기
                    time.sleep(1) # 클릭이 될 수 있도록 대기
                
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (日本語)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (日本語)".format(i))
        
            first_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[4]')
            self.assertIsNotNone(first_page, msg="This page not first page. (日本語)")
                     
        if language == 'en' :
            for i in reversed(range(1,int(repeat_all)+1)): # 카운트 순서를 역순으로 전환
                if i == int(repeat_all): # 마지막 페이지일 때는 마우스 이동을 하지 않음
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (English)".format(i))
                if i < int(repeat_all): # 마지막 페이지 이전부터 마우스 이동을 시작
                    length_distance = (length * i) - length # 마우스가 움직여야 하는 거리값

                    moving_bar = self.selenium.wait('xpath', '//*[@id="footer"]/div[1]/div/div[2]/div') # 이동바

                    actions = ActionChains(self.driver)
                    actions.move_to_element_with_offset(moving_bar, int(COMMON['length'][0]['moving_bar_length']) - length_distance, 0).click().perform() # 이동바에서 클릭해서 한 페이지씩 넘기기
                    time.sleep(1) # 클릭이 될 수 있도록 대기
                
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (English)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (English)".format(i))
        
            first_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[4]')
            self.assertIsNotNone(first_page, msg="This page not first page. (English)")
                
        if language == 'ko' :
            for i in reversed(range(1,int(repeat_all)+1)): # 카운트 순서를 역순으로 전환
                if i == int(repeat_all): # 마지막 페이지일 때는 마우스 이동을 하지 않음
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (한국어)".format(i))
                if i < int(repeat_all): # 마지막 페이지 이전부터 마우스 이동을 시작
                    length_distance = (length * i) - length # 마우스가 움직여야 하는 거리값

                    moving_bar = self.selenium.wait('xpath', '//*[@id="footer"]/div[1]/div/div[2]/div') # 이동바

                    actions = ActionChains(self.driver)
                    actions.move_to_element_with_offset(moving_bar, int(COMMON['length'][0]['moving_bar_length']) - length_distance, 0).click().perform() # 이동바에서 클릭해서 한 페이지씩 넘기기
                    time.sleep(1) # 클릭이 될 수 있도록 대기
                
                    el = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[{}]/div/img'.format(i))
                    num = self.selenium.get_text('xpath', '//*[@id="num-area"]/div')
                    current_num = num.split('/')[0]
                    if int(current_num) < int(repeat_all):
                        self.assertIsNotNone(el, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                    if int(current_num) == int(repeat_all):
                        self.assertIsNone(el, msg="Episode {} - {} Page Error (한국어)".format(episode_num, i))
                    self.assertTrue(i == int(current_num), msg="This page not {} page. (한국어)".format(i))
        
            first_page = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[4]')
            self.assertIsNotNone(first_page, msg="This page not first page. (한국어)")
        elif language == 'none' :
            LOGGER.warning("Moving Bar Click Previous Error (Language is empty.)")
        else:
            LOGGER.warning("Moving Bar Click Previous Error (Unsupported language)")

    def check_last_page_title_ep11(self): # 에피소드 마지막 페이지 > 텍스트(제목) > 11화 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        last_text_1 = self.selenium.get_text('xpath', "//div[@class='last-text']//span[1]")
        last_text_2 = self.selenium.get_text('xpath', "//div[@class='last-text']//span[2]")
        game_1 = self.selenium.get_text('xpath', "//div[@class='last-sub-text']//span[1]")
        game_2 = self.selenium.get_text('xpath', "//div[@class='last-sub-text']//span[2]")
        pokopoko = self.selenium.get_text('xpath', "//span[@class='title']")        
        if language == 'ja' :
            self.assertTrue(last_text_1=='クルグVSタイゴの感想を', msg="Episode Last Page - EP11 Text 1 Error ({})".format(COMMON['text'][0]['language']))
            self.assertTrue(last_text_2=='！ぜひ感想をコメントしてください', msg="Episode Last Page - EP11 Text 2 Error ({})".format(COMMON['text'][0]['language']))
            self.assertTrue(game_1=='ゲームでもポコタと仲間たちに', msg="Episode Last Page - EP11 Text Error ({})".format(COMMON['text'][0]['language']))
            self.assertTrue(game_2=='！会いに行きましょう', msg="Episode Last Page - EP11 Text Error ({})".format(COMMON['text'][0]['language']))
            self.assertTrue(pokopoko=='ポコポコ', msg="Episode Last Page - EP11 Pokopoko Text Error ({})".format(COMMON['text'][0]['language']))
        elif language == 'en' :
            self.assertTrue(last_text_1=='?How was Kroog VS Tygo story', msg="Episode Last Page - EP11 Text 1 Error ({})".format(COMMON['text'][1]['language']))
            self.assertTrue(last_text_2=='!Leave a comment', msg="Episode Last Page - EP11 Text 2 Error ({})".format(COMMON['text'][1]['language']))
            self.assertTrue(game_1=='You can meet Pokota and Friends', msg="Episode Last Page - EP11 Text Error ({})".format(COMMON['text'][1]['language']))
            self.assertTrue(game_2=='!Join them', msg="Episode Last Page - EP11 Text Error ({})".format(COMMON['text'][1]['language']))
            self.assertTrue(pokopoko=='POKOPOKO', msg="Episode Last Page - EP11 Pokopoko Text Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertTrue(last_text_1=='크루그VS타이고 이야기의', msg="Episode Last Page - EP11 Text 1 Error ({})".format(COMMON['text'][1]['language']))
            self.assertTrue(last_text_2=='!감상평을 남겨 주세요', msg="Episode Last Page - EP11 Text 2 Error ({})".format(COMMON['text'][1]['language']))
            self.assertTrue(game_1=='게임에서 포코타와 친구들을', msg="Episode Last Page - EP11 Text Error ({})".format(COMMON['text'][1]['language']))
            self.assertTrue(game_2=='!만날 수 있어요', msg="Episode Last Page - EP11 Text Error ({})".format(COMMON['text'][1]['language']))
            self.assertTrue(pokopoko=='포코포코', msg="Episode Last Page - EP11 Pokopoko Text Error ({})".format(COMMON['text'][1]['language']))                
        elif language == 'none' :
            LOGGER.warning("Episode Last Page - EP11 Text Error (Language is empty.)")
        else :
            LOGGER.warning("Episode Last Page - EP11 Text Error (Unsupported language)")

    def check_star_1(self): # 별점 제출 > 별점 1개 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")        
        if language == 'ja' :
            empty_star_1 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[1]/img')
            self.assertIsNotNone(empty_star_1, msg="Episode Last Page - Empty Star 1 Error ({})".format(COMMON['text'][0]['language'])) # 빈 별점이 나오는지 확인
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_1).perform() # 빈 별점이 위에 마우스 오버하는 동작
            full_star_1 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[1]/span/img')
            self.assertIsNotNone(full_star_1, msg="Episode Last Page - Full Star 1 Error ({})".format(COMMON['text'][0]['language'])) # 빈 별점이 위에 마우스 오버 시 풀 별점이 나오는지 확인
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[1]').click() # 풀 별점을 클릭
            pop_up_open_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm.on') # 클래스 이름이 'feedbackConfirm.on'이면 별점 팝업이 열림
            self.assertIsNotNone(pop_up_open_star, msg="Episode Last Page - Star 1 Pop-up Open Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업이 열리는지 확인
            text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/p')
            self.assertTrue(text=='?このまま登録しますか', msg="Episode Last Page - Star 1 Pop-up Text Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업 텍스트 확인
            yes_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertIsNotNone(yes_button, msg="Episode Last Page - Star 1 Pop-up [Yes] Button Error ({})".format(COMMON['text'][0]['language'])) # [네] 버튼이 나오는지 확인
            yes_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertTrue(yes_but_text=='はい', msg="Episode Last Page - Star 1 Pop-up [Yes] Button Text Error ({})".format(COMMON['text'][0]['language'])) # [네] 버튼에서 텍스트가 나오는지 확인
            no_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertIsNotNone(no_button, msg="Episode Last Page - Star 1 Pop-up [No] Button Error ({})".format(COMMON['text'][0]['language'])) # [아니오] 버튼이 나오는지 확인
            no_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertTrue(no_but_text=='いいえ', msg="Episode Last Page - Star 1 Pop-up [No] Button Text Error ({})".format(COMMON['text'][0]['language'])) # [아니오] 버튼에서 텍스트가 나오는지 확인
            time.sleep(1) # 클릭이 될 수 있도록 딜레이
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]').click() # [아니오] 버튼을 클릭
            pop_up_close_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm') # 클래스 이름이 'feedbackConfirm'이면 별점 팝업이 닫힘
            self.assertIsNotNone(pop_up_close_star, msg="Episode Last Page - Star 1 Pop-up Close Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업이 닫히지는 확인
        elif language == 'en' :
            empty_star_1 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[1]/img')
            self.assertIsNotNone(empty_star_1, msg="Episode Last Page - Empty Star 1 Error ({})".format(COMMON['text'][1]['language']))
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_1).perform()
            full_star_1 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[1]/span/img')
            self.assertIsNotNone(full_star_1, msg="Episode Last Page - Full Star 1 Error ({})".format(COMMON['text'][1]['language']))
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[1]').click()
            pop_up_open_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm.on')
            self.assertIsNotNone(pop_up_open_star, msg="Episode Last Page - Star 1 Pop-up Open Error ({})".format(COMMON['text'][1]['language']))
            text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/p')
            self.assertTrue(text=='?Do you want to submit this rating', msg="Episode Last Page - Star 1 Pop-up Text Error ({})".format(COMMON['text'][1]['language']))
            yes_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertIsNotNone(yes_button, msg="Episode Last Page - Star 1 Pop-up [Yes] Button Error ({})".format(COMMON['text'][1]['language']))
            yes_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertTrue(yes_but_text=='Yes', msg="Episode Last Page - Star 1 Pop-up [Yes] Button Text Error ({})".format(COMMON['text'][1]['language']))
            no_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertIsNotNone(no_button, msg="Episode Last Page - Star 1 Pop-up [No] Button Error ({})".format(COMMON['text'][1]['language']))
            no_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertTrue(no_but_text=='No', msg="Episode Last Page - Star 1 Pop-up [No] Button Text Error ({})".format(COMMON['text'][1]['language']))
            time.sleep(1)
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]').click()
            pop_up_close_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm')
            self.assertIsNotNone(pop_up_close_star, msg="Episode Last Page - Star 1 Pop-up Close Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            empty_star_1 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[1]/img')
            self.assertIsNotNone(empty_star_1, msg="Episode Last Page - Empty Star 1 Error ({})".format(COMMON['text'][2]['language']))
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_1).perform()
            full_star_1 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[1]/span/img')
            self.assertIsNotNone(full_star_1, msg="Episode Last Page - Full Star 1 Error ({})".format(COMMON['text'][2]['language']))
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[1]').click()
            pop_up_open_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm.on')
            self.assertIsNotNone(pop_up_open_star, msg="Episode Last Page - Star 1 Pop-up Open Error ({})".format(COMMON['text'][2]['language']))
            text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/p')
            self.assertTrue(text=='?이대로 제출하시겠습니까', msg="Episode Last Page - Star 1 Pop-up Text Error ({})".format(COMMON['text'][2]['language']))
            yes_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertIsNotNone(yes_button, msg="Episode Last Page - Star 1 Pop-up [Yes] Button Error ({})".format(COMMON['text'][2]['language']))
            yes_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertTrue(yes_but_text=='네', msg="Episode Last Page - Star 1 Pop-up [Yes] Button Text Error ({})".format(COMMON['text'][2]['language']))
            no_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertIsNotNone(no_button, msg="Episode Last Page - Star 1 Pop-up [No] Button Error ({})".format(COMMON['text'][2]['language']))
            no_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertTrue(no_but_text=='아니오', msg="Episode Last Page - Star 1 Pop-up [No] Button Text Error ({})".format(COMMON['text'][2]['language']))
            time.sleep(1)
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]').click()
            pop_up_close_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm')
            self.assertIsNotNone(pop_up_close_star, msg="Episode Last Page - Star 1 Pop-up Close Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("Episode Last Page - Star 1 Error (Language is empty.)")
        else :
            LOGGER.warning("Episode Last Page - Star 1 Error (Unsupported language)")

    def check_star_2(self): # 별점 제출 > 별점 2개 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")        
        if language == 'ja' :
            empty_star_2 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[2]/img')
            self.assertIsNotNone(empty_star_2, msg="Episode Last Page - Empty Star 2 Error ({})".format(COMMON['text'][0]['language'])) # 빈 별점이 나오는지 확인
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_2).perform() # 빈 별점이 위에 마우스 오버하는 동작
            full_star_2 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[2]/span/img')
            self.assertIsNotNone(full_star_2, msg="Episode Last Page - Full Star 2 Error ({})".format(COMMON['text'][0]['language'])) # 빈 별점이 위에 마우스 오버 시 풀 별점이 나오는지 확인
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[2]').click() # 풀 별점을 클릭
            pop_up_open_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm.on') # 클래스 이름이 'feedbackConfirm.on'이면 별점 팝업이 열림
            self.assertIsNotNone(pop_up_open_star, msg="Episode Last Page - Star 2 Pop-up Open Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업이 열리는지 확인
            text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/p')
            self.assertTrue(text=='?このまま登録しますか', msg="Episode Last Page - Star 2 Pop-up Text Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업 텍스트 확인
            yes_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertIsNotNone(yes_button, msg="Episode Last Page - Star 2 Pop-up [Yes] Button Error ({})".format(COMMON['text'][0]['language'])) # [네] 버튼이 나오는지 확인
            yes_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertTrue(yes_but_text=='はい', msg="Episode Last Page - Star 2 Pop-up [Yes] Button Text Error ({})".format(COMMON['text'][0]['language'])) # [네] 버튼에서 텍스트가 나오는지 확인
            no_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertIsNotNone(no_button, msg="Episode Last Page - Star 2 Pop-up [No] Button Error ({})".format(COMMON['text'][0]['language'])) # [아니오] 버튼이 나오는지 확인
            no_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertTrue(no_but_text=='いいえ', msg="Episode Last Page - Star 2 Pop-up [No] Button Text Error ({})".format(COMMON['text'][0]['language'])) # [아니오] 버튼에서 텍스트가 나오는지 확인
            time.sleep(1) # 클릭이 될 수 있도록 딜레이
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]').click() # [아니오] 버튼을 클릭
            pop_up_close_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm') # 클래스 이름이 'feedbackConfirm'이면 별점 팝업이 닫힘
            self.assertIsNotNone(pop_up_close_star, msg="Episode Last Page - Star 2 Pop-up Close Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업이 닫히지는 확인
        elif language == 'en' :
            empty_star_2 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[2]/img')
            self.assertIsNotNone(empty_star_2, msg="Episode Last Page - Empty Star 2 Error ({})".format(COMMON['text'][1]['language']))
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_2).perform()
            full_star_2 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[2]/span/img')
            self.assertIsNotNone(full_star_2, msg="Episode Last Page - Full Star 2 Error ({})".format(COMMON['text'][1]['language']))
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[2]').click()
            pop_up_open_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm.on')
            self.assertIsNotNone(pop_up_open_star, msg="Episode Last Page - Star 2 Pop-up Open Error ({})".format(COMMON['text'][1]['language']))
            text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/p')
            self.assertTrue(text=='?Do you want to submit this rating', msg="Episode Last Page - Star 2 Pop-up Text Error ({})".format(COMMON['text'][1]['language']))
            yes_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertIsNotNone(yes_button, msg="Episode Last Page - Star 2 Pop-up [Yes] Button Error ({})".format(COMMON['text'][1]['language']))
            yes_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertTrue(yes_but_text=='Yes', msg="Episode Last Page - Star 2 Pop-up [Yes] Button Text Error ({})".format(COMMON['text'][1]['language']))
            no_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertIsNotNone(no_button, msg="Episode Last Page - Star 2 Pop-up [No] Button Error ({})".format(COMMON['text'][1]['language']))
            no_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertTrue(no_but_text=='No', msg="Episode Last Page - Star 2 Pop-up [No] Button Text Error ({})".format(COMMON['text'][1]['language']))
            time.sleep(1)
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]').click()
            pop_up_close_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm')
            self.assertIsNotNone(pop_up_close_star, msg="Episode Last Page - Star 2 Pop-up Close Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            empty_star_2 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[2]/img')
            self.assertIsNotNone(empty_star_2, msg="Episode Last Page - Empty Star 2 Error ({})".format(COMMON['text'][2]['language']))
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_2).perform()
            full_star_2 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[2]/span/img')
            self.assertIsNotNone(full_star_2, msg="Episode Last Page - Full Star 2 Error ({})".format(COMMON['text'][2]['language']))
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[2]').click()
            pop_up_open_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm.on')
            self.assertIsNotNone(pop_up_open_star, msg="Episode Last Page - Star 2 Pop-up Open Error ({})".format(COMMON['text'][2]['language']))
            text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/p')
            self.assertTrue(text=='?이대로 제출하시겠습니까', msg="Episode Last Page - Star 2 Pop-up Text Error ({})".format(COMMON['text'][2]['language']))
            yes_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertIsNotNone(yes_button, msg="Episode Last Page - Star 2 Pop-up [Yes] Button Error ({})".format(COMMON['text'][2]['language']))
            yes_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertTrue(yes_but_text=='네', msg="Episode Last Page - Star 2 Pop-up [Yes] Button Text Error ({})".format(COMMON['text'][2]['language']))
            no_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertIsNotNone(no_button, msg="Episode Last Page - Star 2 Pop-up [No] Button Error ({})".format(COMMON['text'][2]['language']))
            no_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertTrue(no_but_text=='아니오', msg="Episode Last Page - Star 2 Pop-up [No] Button Text Error ({})".format(COMMON['text'][2]['language']))
            time.sleep(1)
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]').click()
            pop_up_close_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm')
            self.assertIsNotNone(pop_up_close_star, msg="Episode Last Page - Star 2 Pop-up Close Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("Episode Last Page - Star 2 Error (Language is empty.)")
        else :
            LOGGER.warning("Episode Last Page - Star 2 Error (Unsupported language)")

    def check_star_3(self): # 별점 제출 > 별점 3개 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")        
        if language == 'ja' :
            empty_star_3 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[3]/img')
            self.assertIsNotNone(empty_star_3, msg="Episode Last Page - Empty Star 3 Error ({})".format(COMMON['text'][0]['language'])) # 빈 별점이 나오는지 확인
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_3).perform() # 빈 별점이 위에 마우스 오버하는 동작
            full_star_3 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[3]/span/img')
            self.assertIsNotNone(full_star_3, msg="Episode Last Page - Full Star 3 Error ({})".format(COMMON['text'][0]['language'])) # 빈 별점이 위에 마우스 오버 시 풀 별점이 나오는지 확인
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[3]').click() # 풀 별점을 클릭
            pop_up_open_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm.on') # 클래스 이름이 'feedbackConfirm.on'이면 별점 팝업이 열림
            self.assertIsNotNone(pop_up_open_star, msg="Episode Last Page - Star 3 Pop-up Open Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업이 열리는지 확인
            text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/p')
            self.assertTrue(text=='?このまま登録しますか', msg="Episode Last Page - Star 3 Pop-up Text Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업 텍스트 확인
            yes_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertIsNotNone(yes_button, msg="Episode Last Page - Star 3 Pop-up [Yes] Button Error ({})".format(COMMON['text'][0]['language'])) # [네] 버튼이 나오는지 확인
            yes_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertTrue(yes_but_text=='はい', msg="Episode Last Page - Star 3 Pop-up [Yes] Button Text Error ({})".format(COMMON['text'][0]['language'])) # [네] 버튼에서 텍스트가 나오는지 확인
            no_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertIsNotNone(no_button, msg="Episode Last Page - Star 3 Pop-up [No] Button Error ({})".format(COMMON['text'][0]['language'])) # [아니오] 버튼이 나오는지 확인
            no_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertTrue(no_but_text=='いいえ', msg="Episode Last Page - Star 3 Pop-up [No] Button Text Error ({})".format(COMMON['text'][0]['language'])) # [아니오] 버튼에서 텍스트가 나오는지 확인
            time.sleep(1) # 클릭이 될 수 있도록 딜레이
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]').click() # [아니오] 버튼을 클릭
            pop_up_close_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm') # 클래스 이름이 'feedbackConfirm'이면 별점 팝업이 닫힘
            self.assertIsNotNone(pop_up_close_star, msg="Episode Last Page - Star 3 Pop-up Close Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업이 닫히지는 확인
        elif language == 'en' :
            empty_star_3 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[3]/img')
            self.assertIsNotNone(empty_star_3, msg="Episode Last Page - Empty Star 3 Error ({})".format(COMMON['text'][1]['language']))
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_3).perform()
            full_star_3 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[3]/span/img')
            self.assertIsNotNone(full_star_3, msg="Episode Last Page - Full Star 3 Error ({})".format(COMMON['text'][1]['language']))
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[3]').click()
            pop_up_open_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm.on')
            self.assertIsNotNone(pop_up_open_star, msg="Episode Last Page - Star 3 Pop-up Open Error ({})".format(COMMON['text'][1]['language']))
            text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/p')
            self.assertTrue(text=='?Do you want to submit this rating', msg="Episode Last Page - Star 3 Pop-up Text Error ({})".format(COMMON['text'][1]['language']))
            yes_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertIsNotNone(yes_button, msg="Episode Last Page - Star 3 Pop-up [Yes] Button Error ({})".format(COMMON['text'][1]['language']))
            yes_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertTrue(yes_but_text=='Yes', msg="Episode Last Page - Star 3 Pop-up [Yes] Button Text Error ({})".format(COMMON['text'][1]['language']))
            no_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertIsNotNone(no_button, msg="Episode Last Page - Star 3 Pop-up [No] Button Error ({})".format(COMMON['text'][1]['language']))
            no_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertTrue(no_but_text=='No', msg="Episode Last Page - Star 3 Pop-up [No] Button Text Error ({})".format(COMMON['text'][1]['language']))
            time.sleep(1)
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]').click()
            pop_up_close_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm')
            self.assertIsNotNone(pop_up_close_star, msg="Episode Last Page - Star 3 Pop-up Close Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            empty_star_3 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[3]/img')
            self.assertIsNotNone(empty_star_3, msg="Episode Last Page - Empty Star 3 Error ({})".format(COMMON['text'][2]['language']))
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_3).perform()
            full_star_3 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[3]/span/img')
            self.assertIsNotNone(full_star_3, msg="Episode Last Page - Full Star 3 Error ({})".format(COMMON['text'][2]['language']))
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[3]').click()
            pop_up_open_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm.on')
            self.assertIsNotNone(pop_up_open_star, msg="Episode Last Page - Star 3 Pop-up Open Error ({})".format(COMMON['text'][2]['language']))
            text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/p')
            self.assertTrue(text=='?이대로 제출하시겠습니까', msg="Episode Last Page - Star 3 Pop-up Text Error ({})".format(COMMON['text'][2]['language']))
            yes_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertIsNotNone(yes_button, msg="Episode Last Page - Star 3 Pop-up [Yes] Button Error ({})".format(COMMON['text'][2]['language']))
            yes_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertTrue(yes_but_text=='네', msg="Episode Last Page - Star 3 Pop-up [Yes] Button Text Error ({})".format(COMMON['text'][2]['language']))
            no_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertIsNotNone(no_button, msg="Episode Last Page - Star 3 Pop-up [No] Button Error ({})".format(COMMON['text'][2]['language']))
            no_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertTrue(no_but_text=='아니오', msg="Episode Last Page - Star 3 Pop-up [No] Button Text Error ({})".format(COMMON['text'][2]['language']))
            time.sleep(1)
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]').click()
            pop_up_close_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm')
            self.assertIsNotNone(pop_up_close_star, msg="Episode Last Page - Star 3 Pop-up Close Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("Episode Last Page - Star 3 Error (Language is empty.)")
        else :
            LOGGER.warning("Episode Last Page - Star 3 Error (Unsupported language)")

    def check_star_4(self): # 별점 제출 > 별점 4개 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")        
        if language == 'ja' :
            empty_star_4 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[4]/img')
            self.assertIsNotNone(empty_star_4, msg="Episode Last Page - Empty Star 4 Error ({})".format(COMMON['text'][0]['language'])) # 빈 별점이 나오는지 확인
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_4).perform() # 빈 별점이 위에 마우스 오버하는 동작
            full_star_4 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[4]/span/img')
            self.assertIsNotNone(full_star_4, msg="Episode Last Page - Full Star 4 Error ({})".format(COMMON['text'][0]['language'])) # 빈 별점이 위에 마우스 오버 시 풀 별점이 나오는지 확인
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[4]').click() # 풀 별점을 클릭
            pop_up_open_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm.on') # 클래스 이름이 'feedbackConfirm.on'이면 별점 팝업이 열림
            self.assertIsNotNone(pop_up_open_star, msg="Episode Last Page - Star 4 Pop-up Open Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업이 열리는지 확인
            text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/p')
            self.assertTrue(text=='?このまま登録しますか', msg="Episode Last Page - Star 4 Pop-up Text Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업 텍스트 확인
            yes_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertIsNotNone(yes_button, msg="Episode Last Page - Star 4 Pop-up [Yes] Button Error ({})".format(COMMON['text'][0]['language'])) # [네] 버튼이 나오는지 확인
            yes_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertTrue(yes_but_text=='はい', msg="Episode Last Page - Star 4 Pop-up [Yes] Button Text Error ({})".format(COMMON['text'][0]['language'])) # [네] 버튼에서 텍스트가 나오는지 확인
            no_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertIsNotNone(no_button, msg="Episode Last Page - Star 4 Pop-up [No] Button Error ({})".format(COMMON['text'][0]['language'])) # [아니오] 버튼이 나오는지 확인
            no_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertTrue(no_but_text=='いいえ', msg="Episode Last Page - Star 4 Pop-up [No] Button Text Error ({})".format(COMMON['text'][0]['language'])) # [아니오] 버튼에서 텍스트가 나오는지 확인
            time.sleep(1) # 클릭이 될 수 있도록 딜레이
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]').click() # [아니오] 버튼을 클릭
            pop_up_close_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm') # 클래스 이름이 'feedbackConfirm'이면 별점 팝업이 닫힘
            self.assertIsNotNone(pop_up_close_star, msg="Episode Last Page - Star 4 Pop-up Close Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업이 닫히지는 확인
        elif language == 'en' :
            empty_star_4 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[4]/img')
            self.assertIsNotNone(empty_star_4, msg="Episode Last Page - Empty Star 4 Error ({})".format(COMMON['text'][1]['language']))
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_4).perform()
            full_star_4 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[4]/span/img')
            self.assertIsNotNone(full_star_4, msg="Episode Last Page - Full Star 4 Error ({})".format(COMMON['text'][1]['language']))
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[4]').click()
            pop_up_open_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm.on')
            self.assertIsNotNone(pop_up_open_star, msg="Episode Last Page - Star 4 Pop-up Open Error ({})".format(COMMON['text'][1]['language']))
            text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/p')
            self.assertTrue(text=='?Do you want to submit this rating', msg="Episode Last Page - Star 4 Pop-up Text Error ({})".format(COMMON['text'][1]['language']))
            yes_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertIsNotNone(yes_button, msg="Episode Last Page - Star 4 Pop-up [Yes] Button Error ({})".format(COMMON['text'][1]['language']))
            yes_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertTrue(yes_but_text=='Yes', msg="Episode Last Page - Star 4 Pop-up [Yes] Button Text Error ({})".format(COMMON['text'][1]['language']))
            no_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertIsNotNone(no_button, msg="Episode Last Page - Star 4 Pop-up [No] Button Error ({})".format(COMMON['text'][1]['language']))
            no_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertTrue(no_but_text=='No', msg="Episode Last Page - Star 4 Pop-up [No] Button Text Error ({})".format(COMMON['text'][1]['language']))
            time.sleep(1)
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]').click()
            pop_up_close_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm')
            self.assertIsNotNone(pop_up_close_star, msg="Episode Last Page - Star 4 Pop-up Close Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            empty_star_4 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[4]/img')
            self.assertIsNotNone(empty_star_4, msg="Episode Last Page - Empty Star 4 Error ({})".format(COMMON['text'][2]['language']))
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_4).perform()
            full_star_4 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[4]/span/img')
            self.assertIsNotNone(full_star_4, msg="Episode Last Page - Full Star 4 Error ({})".format(COMMON['text'][2]['language']))
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[4]').click()
            pop_up_open_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm.on')
            self.assertIsNotNone(pop_up_open_star, msg="Episode Last Page - Star 4 Pop-up Open Error ({})".format(COMMON['text'][2]['language']))
            text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/p')
            self.assertTrue(text=='?이대로 제출하시겠습니까', msg="Episode Last Page - Star 4 Pop-up Text Error ({})".format(COMMON['text'][2]['language']))
            yes_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertIsNotNone(yes_button, msg="Episode Last Page - Star 4 Pop-up [Yes] Button Error ({})".format(COMMON['text'][2]['language']))
            yes_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertTrue(yes_but_text=='네', msg="Episode Last Page - Star 4 Pop-up [Yes] Button Text Error ({})".format(COMMON['text'][2]['language']))
            no_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertIsNotNone(no_button, msg="Episode Last Page - Star 4 Pop-up [No] Button Error ({})".format(COMMON['text'][2]['language']))
            no_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertTrue(no_but_text=='아니오', msg="Episode Last Page - Star 4 Pop-up [No] Button Text Error ({})".format(COMMON['text'][2]['language']))
            time.sleep(1)
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]').click()
            pop_up_close_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm')
            self.assertIsNotNone(pop_up_close_star, msg="Episode Last Page - Star 4 Pop-up Close Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("Episode Last Page - Star 4 Error (Language is empty.)")
        else :
            LOGGER.warning("Episode Last Page - Star 4 Error (Unsupported language)")

    def check_star_5(self): # 별점 제출 > 별점 5개 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")        
        if language == 'ja' :
            empty_star_5 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[5]/img')
            self.assertIsNotNone(empty_star_5, msg="Episode Last Page - Empty Star 5 Error ({})".format(COMMON['text'][0]['language'])) # 빈 별점이 나오는지 확인
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_5).perform() # 빈 별점이 위에 마우스 오버하는 동작
            full_star_5 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[5]/span/img')
            self.assertIsNotNone(full_star_5, msg="Episode Last Page - Full Star 5 Error ({})".format(COMMON['text'][0]['language'])) # 빈 별점이 위에 마우스 오버 시 풀 별점이 나오는지 확인
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[5]').click() # 풀 별점을 클릭
            pop_up_open_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm.on') # 클래스 이름이 'feedbackConfirm.on'이면 별점 팝업이 열림
            self.assertIsNotNone(pop_up_open_star, msg="Episode Last Page - Star 5 Pop-up Open Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업이 열리는지 확인
            text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/p')
            self.assertTrue(text=='?このまま登録しますか', msg="Episode Last Page - Star 5 Pop-up Text Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업 텍스트 확인
            yes_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertIsNotNone(yes_button, msg="Episode Last Page - Star 5 Pop-up [Yes] Button Error ({})".format(COMMON['text'][0]['language'])) # [네] 버튼이 나오는지 확인
            yes_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertTrue(yes_but_text=='はい', msg="Episode Last Page - Star 5 Pop-up [Yes] Button Text Error ({})".format(COMMON['text'][0]['language'])) # [네] 버튼에서 텍스트가 나오는지 확인
            no_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertIsNotNone(no_button, msg="Episode Last Page - Star 5 Pop-up [No] Button Error ({})".format(COMMON['text'][0]['language'])) # [아니오] 버튼이 나오는지 확인
            no_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertTrue(no_but_text=='いいえ', msg="Episode Last Page - Star 5 Pop-up [No] Button Text Error ({})".format(COMMON['text'][0]['language'])) # [아니오] 버튼에서 텍스트가 나오는지 확인
            time.sleep(1) # 클릭이 될 수 있도록 딜레이
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]').click() # [아니오] 버튼을 클릭
            pop_up_close_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm') # 클래스 이름이 'feedbackConfirm'이면 별점 팝업이 닫힘
            self.assertIsNotNone(pop_up_close_star, msg="Episode Last Page - Star 5 Pop-up Close Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업이 닫히지는 확인
        elif language == 'en' :
            empty_star_5 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[5]/img')
            self.assertIsNotNone(empty_star_5, msg="Episode Last Page - Empty Star 5 Error ({})".format(COMMON['text'][1]['language']))
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_5).perform()
            full_star_5 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[5]/span/img')
            self.assertIsNotNone(full_star_5, msg="Episode Last Page - Full Star 5 Error ({})".format(COMMON['text'][1]['language']))
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[5]').click()
            pop_up_open_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm.on')
            self.assertIsNotNone(pop_up_open_star, msg="Episode Last Page - Star 5 Pop-up Open Error ({})".format(COMMON['text'][1]['language']))
            text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/p')
            self.assertTrue(text=='?Do you want to submit this rating', msg="Episode Last Page - Star 5 Pop-up Text Error ({})".format(COMMON['text'][1]['language']))
            yes_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertIsNotNone(yes_button, msg="Episode Last Page - Star 5 Pop-up [Yes] Button Error ({})".format(COMMON['text'][1]['language']))
            yes_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertTrue(yes_but_text=='Yes', msg="Episode Last Page - Star 5 Pop-up [Yes] Button Text Error ({})".format(COMMON['text'][1]['language']))
            no_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertIsNotNone(no_button, msg="Episode Last Page - Star 5 Pop-up [No] Button Error ({})".format(COMMON['text'][1]['language']))
            no_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertTrue(no_but_text=='No', msg="Episode Last Page - Star 5 Pop-up [No] Button Text Error ({})".format(COMMON['text'][1]['language']))
            time.sleep(1)
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]').click()
            pop_up_close_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm')
            self.assertIsNotNone(pop_up_close_star, msg="Episode Last Page - Star 5 Pop-up Close Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            empty_star_5 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[5]/img')
            self.assertIsNotNone(empty_star_5, msg="Episode Last Page - Empty Star 5 Error ({})".format(COMMON['text'][2]['language']))
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_5).perform()
            full_star_5 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[5]/span/img')
            self.assertIsNotNone(full_star_5, msg="Episode Last Page - Full Star 5 Error ({})".format(COMMON['text'][2]['language']))
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[5]').click()
            pop_up_open_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm.on')
            self.assertIsNotNone(pop_up_open_star, msg="Episode Last Page - Star 5 Pop-up Open Error ({})".format(COMMON['text'][2]['language']))
            text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/p')
            self.assertTrue(text=='?이대로 제출하시겠습니까', msg="Episode Last Page - Star 5 Pop-up Text Error ({})".format(COMMON['text'][2]['language']))
            yes_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertIsNotNone(yes_button, msg="Episode Last Page - Star 5 Pop-up [Yes] Button Error ({})".format(COMMON['text'][2]['language']))
            yes_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]')
            self.assertTrue(yes_but_text=='네', msg="Episode Last Page - Star 5 Pop-up [Yes] Button Text Error ({})".format(COMMON['text'][2]['language']))
            no_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertIsNotNone(no_button, msg="Episode Last Page - Star 5 Pop-up [No] Button Error ({})".format(COMMON['text'][2]['language']))
            no_but_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]')
            self.assertTrue(no_but_text=='아니오', msg="Episode Last Page - Star 5 Pop-up [No] Button Text Error ({})".format(COMMON['text'][2]['language']))
            time.sleep(1)
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[1]').click()
            pop_up_close_star = self.selenium.driver.find_element_by_class_name('feedbackConfirm')
            self.assertIsNotNone(pop_up_close_star, msg="Episode Last Page - Star 5 Pop-up Close Error ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("Episode Last Page - Star 5 Error (Language is empty.)")
        else :
            LOGGER.warning("Episode Last Page - Star 5 Error (Unsupported language)")

    def check_star_yes_1(self): # 별점 제출 > 별점 1개 > 네 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")        
        if language == 'ja' :
            empty_star_1 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[1]/img')
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_1).perform() # 별점 1개에 마우스 오버
            time.sleep(1) # 마우스 오버 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[1]').click() # 별점 1개 클릭
            time.sleep(1) # 클릭 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]').click() # 별점 팝업에서 '네'를 선택
            disappear_star = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[32]/div/div/div[2]/div')        
            self.assertIsNone(disappear_star, msg="Episode Last Page - Star 1 Assign Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업이 사라지는지 확인
        elif language == 'en' :
            empty_star_1 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[1]/img')
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_1).perform()
            time.sleep(1) # 마우스 오버 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[1]').click() # 별점 1개 클릭
            time.sleep(1) # 클릭 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]').click() # 별점 팝업에서 '네'를 선택
            disappear_star = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[32]/div/div/div[2]/div')        
            self.assertIsNone(disappear_star, msg="Episode Last Page - Star 1 Assign Error ({})".format(COMMON['text'][1]['language'])) # 별점 팝업이 사라지는지 확인
        elif language == 'ko' :
            empty_star_1 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[1]/img')
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_1).perform()
            time.sleep(1) # 마우스 오버 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[1]').click() # 별점 1개 클릭
            time.sleep(1) # 클릭 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]').click() # 별점 팝업에서 '네'를 선택
            disappear_star = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[32]/div/div/div[2]/div')        
            self.assertIsNone(disappear_star, msg="Episode Last Page - Star 1 Assign Error ({})".format(COMMON['text'][2]['language'])) # 별점 팝업이 사라지는지 확인
        elif language == 'none' :
            LOGGER.warning("Episode Last Page - Star 1 Assign Error (Language is empty.)")
        else :
            LOGGER.warning("Episode Last Page - Star 1 Assign Error (Unsupported language)")

    def check_star_yes_2(self): # 별점 제출 > 별점 2개 > 네 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")        
        if language == 'ja' :
            empty_star_2 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[2]/img')
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_2).perform() # 별점 2개에 마우스 오버
            time.sleep(1) # 마우스 오버 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[2]').click() # 별점 2개 클릭
            time.sleep(1) # 클릭 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]').click() # 별점 팝업에서 '네'를 선택
            disappear_star = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[32]/div/div/div[2]/div')        
            self.assertIsNone(disappear_star, msg="Episode Last Page - Star 2 Assign Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업이 사라지는지 확인
        elif language == 'en' :
            empty_star_2 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[2]/img')
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_2).perform() # 별점 2개에 마우스 오버
            time.sleep(1) # 마우스 오버 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[2]').click() # 별점 2개 클릭
            time.sleep(1) # 클릭 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]').click() # 별점 팝업에서 '네'를 선택
            disappear_star = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[32]/div/div/div[2]/div')        
            self.assertIsNone(disappear_star, msg="Episode Last Page - Star 2 Assign Error ({})".format(COMMON['text'][1]['language'])) # 별점 팝업이 사라지는지 확인
        elif language == 'ko' :
            empty_star_2 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[2]/img')
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_2).perform() # 별점 2개에 마우스 오버
            time.sleep(1) # 마우스 오버 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[2]').click() # 별점 2개 클릭
            time.sleep(1) # 클릭 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]').click() # 별점 팝업에서 '네'를 선택
            disappear_star = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[32]/div/div/div[2]/div')        
            self.assertIsNone(disappear_star, msg="Episode Last Page - Star 2 Assign Error ({})".format(COMMON['text'][2]['language'])) # 별점 팝업이 사라지는지 확인
        elif language == 'none' :
            LOGGER.warning("Episode Last Page - Star 2 Assign Error (Language is empty.)")
        else :
            LOGGER.warning("Episode Last Page - Star 2 Assign Error (Unsupported language)")

    def check_star_yes_3(self): # 별점 제출 > 별점 3개 > 네 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")        
        if language == 'ja' :
            empty_star_3 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[3]/img')
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_3).perform() # 별점 3개에 마우스 오버
            time.sleep(1) # 마우스 오버 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[3]').click() # 별점 3개 클릭
            time.sleep(1) # 클릭 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]').click() # 별점 팝업에서 '네'를 선택
            disappear_star = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[32]/div/div/div[2]/div')        
            self.assertIsNone(disappear_star, msg="Episode Last Page - Star 3 Assign Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업이 사라지는지 확인
        elif language == 'en' :
            empty_star_3 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[3]/img')
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_3).perform() # 별점 3개에 마우스 오버
            time.sleep(1) # 마우스 오버 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[3]').click() # 별점 3개 클릭
            time.sleep(1) # 클릭 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]').click() # 별점 팝업에서 '네'를 선택
            disappear_star = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[32]/div/div/div[2]/div')        
            self.assertIsNone(disappear_star, msg="Episode Last Page - Star 3 Assign Error ({})".format(COMMON['text'][1]['language'])) # 별점 팝업이 사라지는지 확인
        elif language == 'ko' :
            empty_star_3 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[3]/img')
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_3).perform() # 별점 3개에 마우스 오버
            time.sleep(1) # 마우스 오버 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[3]').click() # 별점 3개 클릭
            time.sleep(1) # 클릭 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]').click() # 별점 팝업에서 '네'를 선택
            disappear_star = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[32]/div/div/div[2]/div')        
            self.assertIsNone(disappear_star, msg="Episode Last Page - Star 3 Assign Error ({})".format(COMMON['text'][2]['language'])) # 별점 팝업이 사라지는지 확인
        elif language == 'none' :
            LOGGER.warning("Episode Last Page - Star 3 Assign Error (Language is empty.)")
        else :
            LOGGER.warning("Episode Last Page - Star 3 Assign Error (Unsupported language)")

    def check_star_yes_4(self): # 별점 제출 > 별점 4개 > 네 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")        
        if language == 'ja' :
            empty_star_4 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[4]/img')
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_4).perform() # 별점 4개에 마우스 오버
            time.sleep(1) # 마우스 오버 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[4]').click() # 별점 4개 클릭
            time.sleep(1) # 클릭 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]').click() # 별점 팝업에서 '네'를 선택
            disappear_star = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[32]/div/div/div[2]/div')        
            self.assertIsNone(disappear_star, msg="Episode Last Page - Star 4 Assign Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업이 사라지는지 확인
        elif language == 'en' :
            empty_star_4 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[4]/img')
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_4).perform() # 별점 4개에 마우스 오버
            time.sleep(1) # 마우스 오버 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[4]').click() # 별점 4개 클릭
            time.sleep(1) # 클릭 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]').click() # 별점 팝업에서 '네'를 선택
            disappear_star = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[32]/div/div/div[2]/div')        
            self.assertIsNone(disappear_star, msg="Episode Last Page - Star 4 Assign Error ({})".format(COMMON['text'][1]['language'])) # 별점 팝업이 사라지는지 확인
        elif language == 'ko' :
            empty_star_4 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[4]/img')
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_4).perform() # 별점 4개에 마우스 오버
            time.sleep(1) # 마우스 오버 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[4]').click() # 별점 4개 클릭
            time.sleep(1) # 클릭 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]').click() # 별점 팝업에서 '네'를 선택
            disappear_star = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[32]/div/div/div[2]/div')        
            self.assertIsNone(disappear_star, msg="Episode Last Page - Star 4 Assign Error ({})".format(COMMON['text'][2]['language'])) # 별점 팝업이 사라지는지 확인
        elif language == 'none' :
            LOGGER.warning("Episode Last Page - Star 4 Assign Error (Language is empty.)")
        else :
            LOGGER.warning("Episode Last Page - Star 4 Assign Error (Unsupported language)")

    def check_star_yes_5(self): # 별점 제출 > 별점 5개 > 네 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")        
        if language == 'ja' :
            empty_star_5 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[5]/img')
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_5).perform() # 별점 5개에 마우스 오버
            time.sleep(1) # 마우스 오버 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[5]').click() # 별점 5개 클릭
            time.sleep(1) # 클릭 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]').click() # 별점 팝업에서 '네'를 선택
            disappear_star = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[32]/div/div/div[2]/div')        
            self.assertIsNone(disappear_star, msg="Episode Last Page - Star 5 Assign Error ({})".format(COMMON['text'][0]['language'])) # 별점 팝업이 사라지는지 확인
        elif language == 'en' :
            empty_star_5 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[5]/img')
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_5).perform() # 별점 5개에 마우스 오버
            time.sleep(1) # 마우스 오버 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[5]').click() # 별점 5개 클릭
            time.sleep(1) # 클릭 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]').click() # 별점 팝업에서 '네'를 선택
            disappear_star = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[32]/div/div/div[2]/div')        
            self.assertIsNone(disappear_star, msg="Episode Last Page - Star 5 Assign Error ({})".format(COMMON['text'][1]['language'])) # 별점 팝업이 사라지는지 확인
        elif language == 'ko' :
            empty_star_5 = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[5]/img')
            actions = ActionChains(self.driver)
            actions.move_to_element(empty_star_5).perform() # 별점 5개에 마우스 오버
            time.sleep(1) # 마우스 오버 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[2]/div/span/span[5]').click() # 별점 5개 클릭
            time.sleep(1) # 클릭 후 잠시 대기
            self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/div[3]/div/button[2]').click() # 별점 팝업에서 '네'를 선택
            disappear_star = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[32]/div/div/div[2]/div')        
            self.assertIsNone(disappear_star, msg="Episode Last Page - Star 5 Assign Error ({})".format(COMMON['text'][2]['language'])) # 별점 팝업이 사라지는지 확인
        elif language == 'none' :
            LOGGER.warning("Episode Last Page - Star 5 Assign Error (Language is empty.)")
        else :
            LOGGER.warning("Episode Last Page - Star 5 Assign Error (Unsupported language)")

    def check_review_button(self): # 감상평 남기기 > 버튼 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        review_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/a/div')
        review_text = self.selenium.get_text('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/a/div')
        if language == 'ja' :
            self.assertIsNotNone(review_button, msg="Episode Last Page - Review Button Error ({})".format(COMMON['text'][0]['language'])) # '감상평 남기기' 버튼이 나오는지 확인
            self.assertTrue(review_text=='感想をコメント', msg="Episode Last Page - Review Button Text Error ({})".format(COMMON['text'][0]['language'])) # '감상평 남기기' 영역에서 텍스트가 나오는지 확인            
        elif language == 'en' :
            self.assertIsNotNone(review_button, msg="Episode Last Page - Review Button Error ({})".format(COMMON['text'][1]['language']))
            self.assertTrue(review_text=='Leave a comment', msg="Episode Last Page - Review Button Text Error ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertIsNotNone(review_button, msg="Episode Last Page - Review Button Error ({})".format(COMMON['text'][2]['language']))
            self.assertTrue(review_text=='감상평 남기기', msg="Episode Last Page - Review Button Text Error ({})".format(COMMON['text'][2]['language']))        
        elif language == 'none' :
            LOGGER.warning("Episode Last Page - Review Button Error (Language is empty.)")
        else :
            LOGGER.warning("Episode Last Page - Review Button Error (Unsupported language)")

    def check_review_mouse_movement(self): # 감상평 남기기 > 마우스 아웃 / 오버 검증
        review_button = self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/a/div')
        re_before = self.driver.execute_script('const el = document.querySelector(".reply-btn");return getComputedStyle(el).background') # '감상평 남기기'에 마우스 오버가 되지 않았을 때의 색상값을 구하는 부분
        re_before_rgb = re_before.rsplit(' none')[0] # RGB값만 남기는 부분
        self.assertTrue(re_before_rgb=='rgb(255, 131, 71)', msg="Episode Last Page - Reply Mouse-Out Color Error") # RGB값을 비교하여 확인
        time.sleep(1)
        actions = ActionChains(self.driver)
        actions.move_to_element(review_button).perform() # 감상평 남기기 버튼에 마우스 이동
        time.sleep(1)
        re_after = self.driver.execute_script('const el = document.querySelector(".reply-btn");return getComputedStyle(el).background') # '감상평 남기기'에 마우스 오버가 되었을 때의 색상값을 구하는 부분
        re_after_rgb = re_after.rsplit(' none')[0] # RGB값만 남기는 부분        
        self.assertTrue(re_after_rgb=='rgb(136, 42, 0)', msg="Episode Last Page - Reply Mouse-Over Color Error") # RGB값을 비교하여 확인

    def check_review_open_close(self): # 감상평 남기기 > 열기 / 닫기 검증
        self.selenium.wait('xpath', '//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[21]/div/div/a/div').click() # '감상평 남기기' 버튼 클릭
        reply_facebook_open = self.selenium.wait('xpath', '//*[@id="comment"]/div')
        self.assertIsNotNone(reply_facebook_open, msg="Episode Last Page - Reply Facebook Error") # '감상평 남기기' 페이스북 페이지가 열리는지 확인
        time.sleep(1)
        reply_facebook_close = self.selenium.wait('xpath', '//*[@id="__next"]/div[4]/div/div[1]/a/img')
        self.assertIsNotNone(reply_facebook_close, msg="Episode Last Page - Reply Facebook Close Error") # '감상평 남기기' 페이스북 닫기 버튼이 나오는지 확인        
        self.selenium.wait('xpath', '//*[@id="__next"]/div[4]/div/div[1]/a/img').click() # '감상평 남기기' 닫기[X] 버튼 클릭

    def check_game_icon(self): # 마켓 바로가기 > 게임 아이콘 검증
        game_icon = self.selenium.wait('xpath', '//*[@id="game_content"]/div/ul/li[1]/img')
        self.assertIsNotNone(game_icon, msg="Episode Last Page - Game Icon Image Error")

    def check_market_icon(self): # 마켓 바로가기 > 마켓 아이콘 검증
        apple_store = self.selenium.wait('xpath', '//*[@id="game_content"]/div/ul/li[2]/a[1]')
        self.assertIsNotNone(apple_store, msg="Episode Last Page - App Store Image Error")
        google_store = self.selenium.wait('xpath', '//*[@id="game_content"]/div/ul/li[2]/a[2]')
        self.assertIsNotNone(google_store, msg="Episode Last Page - Google Play Image Error")
    
    def check_market_appstore(self): # 마켓 바로가기 > 마켓 이동 > 앱 스토어 검증
        time.sleep(1)
        self.vars["window_handles"] = self.selenium.driver.window_handles
        self.selenium.wait('xpath', '//*[@id="game_content"]/div/ul/li[2]/a[1]').click()
        self.vars["win1500"] = self.wait_for_window(2000)
        self.vars["root"] = self.selenium.driver.current_window_handle
        self.selenium.driver.switch_to.window(self.vars["win1500"])
        time.sleep(1)
        title = self.selenium.get_text('css_selector', '#localnav > div > div.localnav-content.we-localnav__content > div.localnav-title.we-localnav__title > a > span') # App Store가 맞는지 확인
        self.assertTrue(title=='App Store', msg="This page not App Store.")
        # title_pokopoko = self.selenium.get_text('xpath', '/html/body/div[4]/div/main/div/div/div[2]/div[2]/section[1]/div/div[2]/header/h1/text()') # POKOPOKO The Match 3 Puzzle가 맞는지 확인        
        # self.assertTrue(title_pokopoko=='POKOPOKO The Match 3 Puzzle', msg="This page not POKOPOKO The Match 3 Puzzle.")
        # 검증이 안되는 부분 수정 필요
        self.selenium.driver.switch_to.window(self.vars["root"]) # 이전 창(최신 에피소드 마지막 페이지)으로 이동

    def check_market_googleplay(self): # 마켓 바로가기 > 마켓 이동 > 구글 플레이 검증
        time.sleep(1)
        self.vars["window_handles"] = self.selenium.driver.window_handles
        self.selenium.wait('xpath', '//*[@id="game_content"]/div/ul/li[2]/a[2]').click()
        self.vars["win2500"] = self.wait_for_window(2000)
        self.vars["root"] = self.selenium.driver.current_window_handle
        self.selenium.driver.switch_to.window(self.vars["win2500"])
        time.sleep(1)
        title = self.selenium.get_text('xpath', '//*[@id="ZCHFDb"]/c-wiz/div/div[2]/div[1]/span[1]') # Google Play가 맞는지 확인
        self.assertTrue(title=='©2020 Google', msg="This page not Google Play.")
        title_pokopoko = self.selenium.get_text('xpath', '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[1]/c-wiz[1]/h1/span') # 포코포코가 맞는지 확인        
        self.assertTrue(title_pokopoko=='포코포코', msg="This page not 포코포코")
        self.selenium.driver.switch_to.window(self.vars["root"]) # 이전 창(최신 에피소드 마지막 페이지)으로 이동

    def check_review_facebook_button(self): # 하단 영역 > 말풍선 (감상평) > 페이스북 버튼 검증
        language = self.selenium.driver.execute_script("return document.querySelector('html').getAttribute('lang')")
        speech_bubble = self.selenium.wait('xpath', '//*[@id="footer"]/div[2]/div/div[1]/img')
        if language == 'ja' :
            self.assertIsNotNone(speech_bubble, msg="Review(Facebook) Icon is not exist. ({})".format(COMMON['text'][0]['language'])) # 감상평(페이스북) 버튼(아이콘)이 나오는지 확인
        elif language == 'en' :
            self.assertIsNotNone(speech_bubble, msg="Review(Facebook) Icon is not exist. ({})".format(COMMON['text'][1]['language']))
        elif language == 'ko' :
            self.assertIsNotNone(speech_bubble, msg="Review(Facebook) Icon is not exist. ({})".format(COMMON['text'][2]['language']))
        elif language == 'none' :
            LOGGER.warning("Review Facebook Button Error (Language is empty.)")
        else :
            LOGGER.warning("Review Facebook Button Error (Unsupported language)")
    
    def check_review_facebook_open(self): # 하단 영역 > 말풍선 (감상평) > 페이스북 열기 검증
        self.selenium.wait('xpath', '//*[@id="footer"]/div[2]/div/div[1]/img').click()
        time.sleep(2)
        self.selenium.driver.switch_to.frame(0) # 감상평(페이스북) 페이지로 변경        
        facebook_certification = self.selenium.get_text('xpath', '//*[@id="facebook"]/body/div/div/div/div/div/div[4]/div/div[2]/div/a')
        self.assertTrue(facebook_certification=='Facebook 댓글 플러그인', msg="This page not Review(Facebook) page.") # 감상평(페이스북) 페이지인지 확인
    
    def check_review_facebook_reply(self): # TC192_하단 영역 > 말풍선 (감상평) > 페이스북 댓글 남기기 검증
        text_area = self.selenium.wait('xpath', '//*[@id="facebook"]/body/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/textarea')
        self.assertIsNotNone(text_area, msg="Review(Facebook) Text Area is not exist.") # 페이스북 댓글창이 나오는지 확인
        self.selenium.wait('xpath', '//*[@id="facebook"]/body/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/textarea').click() # 댓글창을 선택
        self.selenium.wait('xpath', '//*[@id="facebook"]/body/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/textarea').send_keys("QA2 Test") # 활성화를 위해 댓글창에 임의의 내용을 입력
        self.vars["window_handles"] = self.selenium.driver.window_handles
        self.selenium.wait('xpath', '//*[@id="facebook"]/body/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div/div[2]/span/button').click() # '게시하려면 로그인하세요' 버튼을 선택
        self.vars["win7777"] = self.wait_for_window(2000)
        self.vars["root"] = self.selenium.driver.current_window_handle
        self.selenium.driver.switch_to.window(self.vars["win7777"]) # 페이스북 로그인창으로 전환
        self.selenium.wait('xpath', '//*[@id="email"]').send_keys("xejex@nate.com") # ID 입력
        self.selenium.wait('xpath', '//*[@id="pass"]').send_keys("Jwjdwlsdn7410") # Password 입력
        self.selenium.wait('xpath', '//*[@id="u_0_0"]').click() # [로그인] 버튼 선택
        self.selenium.driver.switch_to.window(self.vars["root"]) # 에피소드 윈도우로 변경
        self.selenium.driver.switch_to.frame(0) # 감상평(페이스북) 프레임으로 변경
        time.sleep(1) # 창이 전환되고 클릭할 수 있을 때까지 잠시 대기
        self.selenium.wait('xpath', '//*[@id="facebook"]/body/div[1]/div/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div[2]/div/div/div/div').click() # 댓글창을 선택
        self.selenium.wait('xpath', '//*[@id="facebook"]/body/div[1]/div/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div[2]/div/div/div/div').send_keys("This episode is so fun. The best!!!") # 댓글창에 고유한 내용을 입력
        self.selenium.wait('xpath', '//*[@id="facebook"]/body/div[1]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div/div[2]/span/button').click() # [게시] 버튼 선택
        comment = self.selenium.get_text('xpath', '//*[@id="facebook"]/body/div[1]/div/div/div/div/div[3]/div[1]/div[2]/div/div[2]/div/div[1]/div/span[1]/span/span')
        self.assertTrue(comment=='This episode is so fun. The best!!!', msg="Review(Facebook) Comment Error") # 입력한 댓글이 맞게 게시되었는지 확인
    
    def check_review_facebook_close(self): # 하단 영역 > 말풍선 (감상평) > 페이스북 닫기 검증
        self.driver.switch_to.default_content() # 감상평(기본) 프레임으로 변경
        time.sleep(2)
        close_button = self.selenium.wait('xpath', '//*[@id="__next"]/div/div[3]/div/div[1]/a/img')
        self.assertIsNotNone(close_button, msg="Review(Facebook) Close Button is not exist.") # 감상평(페이스북) 닫기 버튼이 나오는지 확인
        self.selenium.wait('xpath', '//*[@id="__next"]/div/div[3]/div/div[1]/a/img').click() # 감상평(페이스북) 닫기
        facebook = self.selenium.wait('xpath', '//*[@id="facebook"]/body/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/textarea')
        self.assertIsNone(facebook, msg="Review(Facebook) is not clsoed.") # 페이스북 댓글창이 닫혔는지 확인
    
    def check_review_facebook_logout(self): # TC193_sub_하단 영역 > 말풍선 (감상평) > 페이스북 로그아웃 (미사용 - 임시)
        self.vars["window_handles"] = self.selenium.driver.window_handles
        self.selenium.driver.execute_script('window.open("https://facebook.com/");') # 페이스북 새 탭에서 열기
        self.vars["win2424"] = self.wait_for_window(2000)
        self.vars["root"] = self.selenium.driver.current_window_handle
        self.selenium.driver.switch_to.window(self.vars["win2424"]) # 페이스북 탭으로 전환
        self.selenium.wait('xpath', '//*[@id="mount_0_0"]/div/div/div[1]/div[2]/div[4]/div[1]/span/div/div[1]/img').click() # 계정 드랍다운 메뉴 선택
        time.sleep(1) # 계정 드랍다운 메뉴가 열릴 때까지 잠시 대기
        self.selenium.wait('xpath', '//*[@id="mount_0_0"]/div/div/div[1]/div[2]/div[4]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div[1]/div[3]/div/div[5]').click() # 페이스북 로그아웃
        self.selenium.driver.close() # 페이스북 탭 닫기
        self.selenium.driver.switch_to.window(self.vars["root"]) # 에피소드 윈도우로 전환
    
    def check_review_twitter_button(self): # TC194_하단 영역 > SNS 공유 > 트위터 > 트위터 버튼 확인
        twitter_button = self.selenium.wait('xpath', '//*[@id="twitter_a"]/img')
        self.assertIsNotNone(twitter_button, msg="Twitter Icon is not exist.") # 트위터 버튼(아이콘)이 나오는지 확인

###############################################################################################################################################################################################################
# 트위터 
###############################################################################################################################################################################################################

    def check_share_facebook_button(self): # TC196_하단 영역 > SNS 공유 > 페이스북 > 페이스북 버튼 확인
        facebook_button = self.selenium.wait('xpath', '//*[@id="footer"]/div[2]/div/div[2]/div[2]/a/img')
        self.assertIsNotNone(facebook_button, msg="Facebook Icon is not exist.") # 페이스북 버튼(아이콘)이 나오는지 확인

    def check_share_facebook(self): # TC197_200_하단 영역 > SNS 공유 > 페이스북 > 페이스북 공유하기
        self.vars["window_handles"] = self.selenium.driver.window_handles
        self.selenium.wait('xpath', '//a[@class="btn-facebook ga-event"]//img').click() # 페이스북 버튼을 선택
        self.vars["win9999"] = self.wait_for_window(2000)
        self.vars["root"] = self.selenium.driver.current_window_handle
        self.selenium.driver.switch_to.window(self.vars["win9999"]) # 페이스북창으로 전환        
        # 페이스북 페이지의 ID값이 가변이라 절대 xpath 사용
        self.selenium.wait('xpath', '//*[@id="u_0_t"]').click() # 내용 입력창 클릭
        self.selenium.wait('xpath', '//*[@id="u_0_t"]').send_keys("Facebook sharing sample comment") # 임의의 내용 입력
        self.selenium.wait('xpath', '//*[@id="u_0_27"]').click() # [Facebook에 게시] 버튼 선택
        time.sleep(1) # 게시물이 등록될 때까지 대기
        self.selenium.driver.switch_to.window(self.vars["root"]) # 에피소드 윈도우로 전환

    def check_share_facebook_result(self): # TC197_sub_하단 영역 > SNS 공유 > 페이스북 > 페이스북 공유 확인
        self.vars["window_handles"] = self.selenium.driver.window_handles
        self.selenium.driver.execute_script('window.open("https://www.facebook.com/profile.php?id=100028841417025");') # 페이스북 새 탭에서 열기
        self.vars["win5454"] = self.wait_for_window(2000)
        self.vars["root"] = self.selenium.driver.current_window_handle
        self.selenium.driver.switch_to.window(self.vars["win5454"]) # 페이스북 탭으로 전환
        time.sleep(1) # 입력한 임의의 내용 검증을 위한 딜레이
        facebook_comment = self.selenium.get_text('xpath', '/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/span[1]/div[1]/div[1]')
        self.assertTrue(facebook_comment=="Facebook sharing sample comment", msg="Facebook sharing Error") # 입력한 임의의 내용 검증
        self.selenium.driver.close() # 페이스북 탭 닫기
        self.selenium.driver.switch_to.window(self.vars["root"]) # 에피소드 윈도우로 전환

    def check_share_mail(self): # TC201_205_하단 영역 > SNS 공유 > 메일 > 메일 버튼 확인
        # 메일 공유는 메일 동작 방식이 환경마다 다르기에 메일 버튼이 나오는 것만 검증
        mail_button = self.selenium.wait('xpath', '//a[@class="btn-email ga-event"]//img')
        self.assertIsNotNone(mail_button, msg="Mail Icon is not exist.") # 메일 버튼(아이콘)이 나오는지 확인

###############################################################################################################################################################################################################

    def test_TC001(self): # TC001_웹페이지 불러오기
        url = 'https://rc-www.pokopang.com/episode/' # 테스트 할 웹페이지 경로
        self.selenium.open_url(url) # 테스트 할 웹페이지를 로딩
        el = self.selenium.wait('class_name', 'text-area', timeout=5) # 'class_name'에 'text-area'가 나올 때까지 5초간 대기
        self.assertIsNotNone(el, msg="URL Error") # 클래스 이름 중 'text-area'가 없을 시 에러 출력
        LOGGER.info("Current Page : {0}".format(self.driver.current_url)) # 테스트 할 웹페이지를 출력

    def test_TC002_003(self):
        self.check_window_minimal() # TC002_웹페이지 크기 최소화 (크롬(window) 기준)
        self.check_window_maximize() # TC003_웹페이지 크기 최대화 (크롬(window) 기준)

    def test_TC004_057(self):
        self.check_main_thumbnail() # TC004_메인 에피소드 영역 > 썸네일 이미지
        self.check_main_title() # TC005_메인 에피소드 영역 > 텍스트
        self.check_dropdown_button_text() # TC006_언어변경 > 드랍다운 텍스트
        self.check_latest_episode_text() # TC007_최신 에피소드 영역 > 텍스트
        self.check_latest_episode_image() # TC008_최신 에피소드 영역 > 이미지
        self.check_latest_episode_number() # TC009_최신 에피소드 영역 > 회차
        self.check_latest_episode_title() # TC010_최신 에피소드 영역 > 제목
        self.check_other_episode_text() # TC011_다른 에피소드 영역 > 텍스트
        self.check_other_episode_image() # TC012_다른 에피소드 영역 > 이미지
        self.check_other_episode_number() # TC013_다른 에피소드 영역 > 회차
        self.check_other_episode_title() # TC014_다른 에피소드 영역 > 제목
        self.check_sns_title() # TC015_SNS 영역 > 텍스트
        self.check_facebook_image() # TC016_SNS 영역 > 페이스북
        self.check_instagram_image() # TC017_SNS 영역 > 인스타그램
        self.check_twitter_image() # TC018_SNS 영역 > 트위터
        self.check_copyright_text() # TC019_ⓒcopyright 영역
        self.scroll_down() # TC020_스크롤 > 하
        self.scroll_up() # TC021_스크롤 > 상
        self.check_latest_episode_image_click() # TC022_23_클릭 > 최신 에피소드
        self.check_other_episode_image_click_2() # TC024_45_클릭 > 다른 에피소드(10~4화) 보기
        self.check_other_episode_image_click_1() # TC046_51_클릭 > 다른 에피소드(3~1화) 보기
        self.check_facebook_click() # TC052_53_클릭 > 페이스북
        self.check_instagram_click() # TC054_55_클릭 > 인스타그램
        self.check_twitter_click() # TC056_57_클릭 > 트위터

    def test_TC058_59(self): # TC058_59_언어 변경 > 영어
        self.selenium.wait(By.ID, "changeLanguage").click()
        dropdown = self.selenium.wait(By.ID, "changeLanguage")
        dropdown.find_element(By.XPATH, "//option[. = 'English']").click()
        dropdown_en = self.selenium.wait(By.XPATH, "//option[. = 'English']")
        self.assertIsNotNone(dropdown_en, msg="English Change Error")
        time.sleep(1)

    def test_TC060_111(self): # TC060_111_메인 페이지 > 영어
        self.check_main_title()                
        self.check_latest_episode_text()        
        self.check_latest_episode_image()
        self.check_latest_episode_number()        
        self.check_latest_episode_title()        
        self.check_other_episode_text()        
        self.check_other_episode_image()        
        self.check_other_episode_number()        
        self.check_other_episode_title()        
        self.check_sns_title()        
        self.check_facebook_image()        
        self.check_instagram_image()        
        self.check_twitter_image()        
        self.check_copyright_text()

    def test_TC112_113(self): # TC112_언어 변경 > 일본어
        self.selenium.wait(By.ID, "changeLanguage").click()
        dropdown = self.selenium.wait(By.ID, "changeLanguage")
        dropdown.find_element(By.XPATH, "//option[. = '日本語']").click()
        dropdown_ja = self.selenium.wait(By.XPATH, "//option[. = '日本語']")
        self.assertIsNotNone(dropdown_ja, msg="日本語 Change Error")
        time.sleep(1)

    def test_TC114_165(self): # TC114_165_메인 페이지 > 일본어
        self.check_main_title()                
        self.check_latest_episode_text()        
        self.check_latest_episode_image()
        self.check_latest_episode_number()        
        self.check_latest_episode_title()        
        self.check_other_episode_text()        
        self.check_other_episode_image()        
        self.check_other_episode_number()        
        self.check_other_episode_title()        
        self.check_sns_title()        
        self.check_facebook_image()        
        self.check_instagram_image()        
        self.check_twitter_image()        
        self.check_copyright_text()
        self.scroll_down()
        self.scroll_up()
        self.check_latest_episode_image_click()
        self.check_other_episode_image_click_2()
        self.check_other_episode_image_click_1()
        self.check_facebook_click()
        self.check_instagram_click()
        self.check_twitter_click()        

    def test_TC167(self): # TC167_언어변경 > 드랍다운 > 한국어 (일본어 → 한국어)
        self.selenium.wait(By.ID, "changeLanguage").click()
        dropdown = self.selenium.wait(By.ID, "changeLanguage")
        dropdown.find_element(By.XPATH, "//option[. = '한국어']").click()
        dropdown_ja = self.selenium.wait(By.XPATH, "//option[. = '한국어']")
        self.assertIsNotNone(dropdown_ja, msg="한국어 Change Error")
        time.sleep(1)

    def test_TC168(self):
        self.check_move_to_latest_episode() # TC0168_메인 에피소드 > 최신 에피소드 페이지 이동
        self.check_upper_number() # TC169_최신 에피소드 > 상단 영역 > 회차
        self.check_upper_title() # TC170_상단 영역 > 제목
        self.check_upper_image() # TC171_상단 영역 > 이미지
        self.check_menu_icon() # TC172_상단 영역 > 메뉴
        self.check_click_image_to_next() # TC173_177_중단 영역 > 이미지 > 다음 페이지 넘기기 & 마지막 페이지 넘기기 불가
        self.check_last_page_title_ep11() # TC206_208_에피소드 마지막 페이지 > 텍스트 (제목) > 11화
        self.check_star_1() # TC212_215_별점 제출 > 별점 1개 > 아니오
        self.check_star_2() # TC218_221_별점 제출 > 별점 2개 > 아니오
        self.check_star_3() # TC224_227_별점 제출 > 별점 3개 > 아니오
        self.check_star_4() # TC230_233_별점 제출 > 별점 4개 > 아니오
        self.check_star_5() # TC236_239_별점 제출 > 별점 5개 > 아니오
        self.check_review_button() # TC242_감상평 남기기 > 버튼
        self.check_review_mouse_movement() # TC243_244_감상평 남기기 > 마우스 아웃 / 오버
        self.check_review_open_close() # TC245_246_감상평 남기기 > 열기 / 닫기
        self.check_game_icon() # TC247_마켓 바로가기 > 게임 아이콘
        self.check_market_icon() # TC248_249_마켓 바로가기 > 마켓 아이콘
        self.check_market_appstore() # TC250_마켓 바로가기 > 마켓 이동 > 앱 스토어
        self.check_market_googleplay() # TC251_마켓 바로가기 > 마켓 이동 > 구글 플레이
        self.check_click_image_to_previous() # TC176_177_중단 영역 > 이미지 > 이전 페이지 돌아가기 & 마지막 이전 페이지 넘기기 불가
        self.check_drag_and_drop_to_next() # TC178_180_하단 영역 > 페이지 이동바 > 드래그&드롭 > 다음 페이지 넘기기 & 마지막 페이지 넘기기 불가
        self.check_drag_and_drop_to_previous() # TC181_183_하단 영역 > 페이지 이동바 > 드래그&드롭 > 이전 페이지 돌아가기 & 마지막 이전 페이지 돌아가기 불가
        self.check_movingbar_click_to_next() # TC184_186_하단 영역 > 페이지 이동바 > 클릭 > 다음 페이지 넘기기 & 다음 페이지 넘기기 불가
        self.check_movingbar_click_to_previous() # TC187_189_하단 영역 > 페이지 이동바 > 클릭 > 이전 페이지 돌아가기
        self.check_review_facebook_button() # TC190_하단 영역 > 말풍선 (감상평) > 페이스북 버튼 확인
        self.check_review_facebook_open() # TC191_하단 영역 > 말풍선 (감상평) > 페이스북 열기
        self.check_review_facebook_reply() # TC192_하단 영역 > 말풍선 (감상평) > 페이스북 댓글 남기기
        self.check_review_facebook_close() # TC193_하단 영역 > 말풍선 (감상평) > 페이스북 닫기
        # self.check_review_facebook_logout() # TC193_sub_하단 영역 > 말풍선 (감상평) > 페이스북 로그아웃 (미사용 - 임시)
        self.check_review_twitter_button() # TC194_하단 영역 > SNS 공유 > 트위터 > 트위터 버튼 확인        
        self.check_share_facebook_button() # TC196_하단 영역 > SNS 공유 > 페이스북 > 페이스북 버튼 확인
        self.check_share_facebook() # TC197_200_하단 영역 > SNS 공유 > 페이스북 > 페이스북 공유하기        
        self.check_share_facebook_result() # TC197_sub_하단 영역 > SNS 공유 > 페이스북 > 페이스북 공유 확인
        self.check_share_mail() # TC201_205_하단 영역 > SNS 공유 > 메일 > 메일 버튼 확인
        
    def test_TC195(self): # TC195_하단 영역 > SNS 공유 > 트위터 > 트위터 공유하기
        number = self.selenium.get_text('css_selector', '#cbp-spmenu-s3 > div > div > div.head-title > h6')
        episode_number = number.split(' ')[1] # 현재 에피소드의 '숫자'만 가져오도록 함        
        self.vars["window_handles"] = self.selenium.driver.window_handles
        self.selenium.wait('xpath', '//*[@id="twitter_a"]/img').click() # 트위터 버튼을 선택
        self.vars["win8888"] = self.wait_for_window(2000)
        self.vars["root"] = self.selenium.driver.current_window_handle        
        self.selenium.driver.switch_to.window(self.vars["win8888"]) # 트위터 로그인창으로 전환
        self.selenium.wait('css_selector', '#react-root > div > div > div.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-184en5c > div:nth-child(2) > div > div > div > div > div > div.css-1dbjc4n.r-1awozwy.r-1kihuf0.r-18u37iz.r-1pi2tsx.r-1777fci.r-1pjcn9w.r-fxte16.r-1xcajam.r-ipm5af.r-g6jmlv > div.css-1dbjc4n.r-t23y2h.r-1jgb5lz.r-pm9dpa.r-1ye8kvj.r-1rnoaur.r-13qz1uu > div > div.css-1dbjc4n.r-1pcd2l5 > form > div > div:nth-child(6) > label > div > div.css-1dbjc4n.r-18u37iz.r-16y2uox.r-1wbh5a2.r-1udh08x > div > input').send_keys("xejex@naver.com") # ID 입력
        self.selenium.wait('css_selector', '#react-root > div > div > div.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-184en5c > div:nth-child(2) > div > div > div > div > div > div.css-1dbjc4n.r-1awozwy.r-1kihuf0.r-18u37iz.r-1pi2tsx.r-1777fci.r-1pjcn9w.r-fxte16.r-1xcajam.r-ipm5af.r-g6jmlv > div.css-1dbjc4n.r-t23y2h.r-1jgb5lz.r-pm9dpa.r-1ye8kvj.r-1rnoaur.r-13qz1uu > div > div.css-1dbjc4n.r-1pcd2l5 > form > div > div:nth-child(7) > label > div > div.css-1dbjc4n.r-18u37iz.r-16y2uox.r-1wbh5a2.r-1udh08x > div > input').send_keys("Jwjdwlsdn7410") # Password 입력
        self.selenium.wait('css_selector', '#react-root > div > div > div.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-184en5c > div:nth-child(2) > div > div > div > div > div > div.css-1dbjc4n.r-1awozwy.r-1kihuf0.r-18u37iz.r-1pi2tsx.r-1777fci.r-1pjcn9w.r-fxte16.r-1xcajam.r-ipm5af.r-g6jmlv > div.css-1dbjc4n.r-t23y2h.r-1jgb5lz.r-pm9dpa.r-1ye8kvj.r-1rnoaur.r-13qz1uu > div > div.css-1dbjc4n.r-1gkumvb.r-1efd50x.r-5kkj8d.r-18u37iz.r-1wtj0ep.r-d9fdf6.r-9qu9m4 > div.css-18t94o4.css-1dbjc4n.r-urgr8i.r-42olwf.r-sdzlij.r-1phboty.r-rs99b7.r-1w2pmg.r-1vuscfd.r-1dhvaqw.r-1ny4l3l.r-1fneopy.r-o7ynqc.r-6416eg.r-lrvibr > div > span > span > span').click() # [로그인] 버튼 선택
        twitter = self.selenium.get_text('xpath', '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/div/div/div/div[3]/div/div/span/span')
        self.assertTrue(twitter=='Tweet', msg="This page not Twitter page. (ko)") # 트위터가 맞는지 확인
        comment = self.selenium.get_text('xpath', '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[3]/div/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div/div/div/div/div/span[7]/span/span')
        self.assertTrue(comment=='https://rc-www.pokopang.com/episode/{}?utm_source=twitter&utm_medium=share_post&utm_campaign={}&lang=ko'.format(episode_number,episode_number), msg="Twittter sharing comment Error (ko)") # 공유 내용이 맞는지 확인        
        tweet_button = self.selenium.wait('xpath', '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/div/div/div/div[3]/div')
        self.assertIsNotNone(tweet_button, msg="Tweet Icon is not exist. (ko)") # 등록[Tweet] 버튼이 나오는지 확인
        self.selenium.wait('xpath', '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/div/div/div/div[3]/div/div/span/span').click() # 등록[Tweet] 버튼을 선택     
        
    # 트위터에 등록 후 등록된 내용을 확인하는 과정이 필요