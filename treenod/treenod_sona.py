# -*- coding: utf-8 -*-
import logging
import time
#import re
import sys
from base import BaseTestCase
#from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common import exceptions
from util import language_check
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
#from selenium.webdriver.support.ui import WebDriverWait

LOGGER = logging.getLogger()
LANG_LIST = ['ko', 'en', 'ja']
BASE_URL = 'https://www.treenod.com/'

class TestTreenodcom(BaseTestCase):

    #scroll
    def scroll(self, lang=None):
        count = 0

        for i in range(100):
            element = self.selenium.wait('css_selector', '#scroll_marker a.scroll_bottom.sm_bounce', timeout=3)

            if element:
                try:
                    element.click()
                    element = self.selenium.wait('css_selector', '#scroll_marker a.scroll_bottom.sm_fadeOut', timeout=2)
                    if element:
                        count = i + 1
                        break
                except exceptions.ElementNotInteractableException as e:
                    LOGGER.warning("Scroll not available")
                    return False

        LOGGER.info("{} time(s) scroll.".format(count))

        scroll_top = self.selenium.wait('css_selector', '.scroll_top > img')
        self.assertTrue(scroll_top, msg= 'Top scroll not found.')
        scroll_top.click()
        time.sleep(1)

        return True

    #open browser
    def open_url(self, url):
        result = self.selenium.open_url(url)
        time.sleep(3)
        self.assertTrue(result, msg='URL ({}) open failed'.format(url))
        LOGGER.info("Current check page -> {}".format(self.driver.current_url))


    #change language
    def check_language(self, lang):
        #find lang list(pc)
        lang_list = self.selenium.wait('css_selector', 'nav.gnb > .lang > ul > li', find_multiple=True)
        lang_set = {
            'ko': {'nav': lambda: lang_list[0], 'menu_css': '#menu-header-ko > li', 'menu': ['About', 'Careers', 'Games', 'Brand']},
            'en': {'nav': lambda: lang_list[1], 'menu_css': '#menu-header-en > li', 'menu': ['About', 'Games', 'Brand']},
            'ja': {'nav': lambda: lang_list[2], 'menu_css': '#menu-header-ja > li', 'menu': ['About', 'Games', 'Brand']},
        }
        self.assertTrue(lang in lang_set.keys(), msg='Language not permitted')

        #click lang button
        cls_name = lang_set[lang]['nav']().get_attribute('class')
        if ('current-lang' in cls_name):
            pass
        else:
            self.selenium.wait('class_name', 'lang').click()
            time.sleep(1)

        #select lang
        try:
            lang_set[lang]['nav']().click()
        except:
            pass

        #compare class name
        lang_list = self.selenium.wait('css_selector', 'nav.gnb > .lang > ul > li', find_multiple=True)
        cls_name = lang_set[lang]['nav']().get_attribute('class')
        self.assertTrue('current-lang' in cls_name, msg='Lang Change Fail')

        #get menu_header elements
        menu_header = self.selenium.wait('css_selector', lang_set[lang]['menu_css'], find_multiple=True)
        self.assertIsNotNone(menu_header, msg='menu_header {} not found'.format(lang_set[lang]['menu_css']))

        #compares innertext with menu
        if (len(menu_header) == len(lang_set[lang]['menu'])):
            for i, j in zip(menu_header, lang_set[lang]['menu']):
                self.assertTrue((i.get_attribute('innerText')) == j, msg= 'Not correct')
        else:
            LOGGER.warning('Header menu count not correct.')

        time.sleep(3)
        text = self.selenium.get_text('xpath', '//*[@id="container"]')
        return lang in language_check.check(text)

    #video load
    def check_video(self, lang=None):
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

        return False

    #locaton
    def no_test_js(self):
        #javascript 코드 내의 변수에서 위치정보 가져오기
        location = self.driver.execute_script('return coordinateBusan')
        LOGGER.info(location['lat'])
        LOGGER.info(location['lng'])
        map_location = {}
        map_location['lat'] = 37.51624
        map_location['lng'] = 127.0391247

        if (location == map_location):
            LOGGER.info("Location Test Pass")
        else:
            LOGGER.warning("Location Test Fail")

    #check js fade in effect
    def check_effect(self, lang=None):
        #find elements applied javascript effect
        element = self.selenium.wait('class_name', 'wow', find_multiple=True)

        #scroll 수행 후 effect 적용 확인
        self.scroll()
        time.sleep(1)
        #animation effects used on treenod.com
        ani_list = ['fadeIn', 'fadeInUp', 'fadeInRight', 'fadeInLeft']

        count = 0
        for i in element:
            visibility = i.value_of_css_property('visibility')
            animation = i.value_of_css_property('animation-name')
            #visibility=='visible' && animation name != none 일 경우 effect 적용된 상태
            self.assertTrue(visibility=='visible', msg = "visibility("+ str(count) +") is not yet applied.")
            self.assertTrue(animation in ani_list, msg = "animation("+ str(count) +")is not yet applied.")
            count += 1

        return (len(element) == count)

    #link click & check url
    def check_link(self, element):
        #element가 없을 경우
        if element == None: return False

        #get element's url
        url = element.get_attribute('href')

        #h1 <a>tag 예외처리
        if (url == 'https://www.treenod.com'):
            url = url + '/'
        elif (url == 'https://www.treenod.com/en'):
            url = url + '/'
        elif (url == 'https://www.treenod.com/ja'):
            url = url + '/'
        elif (url == 'https://www.treenod.com/blog#'):
            url = url.rstrip('#')

        time.sleep(5)
        #print(url)

        referrer = self.driver.current_url
        #link click
        try:
            element.click()
        #about's child menu는 즉시 클릭이 불가하여 예외처리
        except:
            about = self.selenium.wait('xpath', '//*[@id="header"]/div[@class="header_in"]/nav[@class="gnb"]/div[2]/ul/li[1]')
            ActionChains(self.driver).move_to_element(about).click(element).perform()

        current_url = self.go_previous_page(referrer)

        time.sleep(5)
        return (url == current_url)

    #Click header menu
    def check_header(self, lang):
        el_h1 = self.selenium.wait('css_selector', '#header .header_in h1 a')
        self.assertTrue(self.check_link(el_h1), msg='Url not match')
        time.sleep(5)

        if (lang in LANG_LIST):
            el_li = self.selenium.wait('css_selector', '#menu-header-'+ str(lang) +' a', find_multiple=True)
        else:
            raise ValueError('Language not permitted')

        for i in range(len(el_li)):
            el_li = self.selenium.wait('css_selector', '#menu-header-'+ str(lang) +' a', find_multiple=True)
            self.assertTrue(self.check_link(el_li[i]), msg='Url not match')

        #a = self.selenium.wait('xpath', '/html/body').get_attribute('class')
        #print(a)

        return True

    #Click footer menu
    def check_footer(self, lang):
        #board exist only korean
        if (lang == 'ko'):
            el = self.selenium.wait('css_selector', '#menu-footer-ko a', find_multiple=True)

            for i in range(len(el)):
                el = self.selenium.wait('css_selector', '#menu-footer-ko a', find_multiple=True)
                self.assertTrue(self.check_link(el[i]), msg='Link error')
        
        urls = ['mailto:contact@treenod.com', 'https://www.facebook.com/treenod/', 'https://blog.naver.com/treenod_story']
        els = self.selenium.wait('css_selector', '.footer_area02 > a', find_multiple=True)

        #mail, Facebook link와 실제 url 비교
        for i, j in zip(els, urls):
            result = i.get_attribute('href')
            self.assertTrue(result == j, msg='Link error')

        return True

    #Click container menu
    def check_container(self, lang=None):

        #en, ja는 홈페이지 리뉴얼 후에 정상동작 가능(불필요한 태그 제거해야함 by. aster)
        el = self.selenium.wait('css_selector', '#container a', find_multiple=True)
        if el == None: return False

        length = len(el)
        for i in range(length):
            el = self.selenium.wait('css_selector', '#container a', find_multiple=True)
            result = self.check_link(el[i])
            self.assertTrue(result, msg='Link error')

        return True

    #image swipe
    def check_swiper(self, lang=None):
        location = []
        count = 7
        for i in range(0, count):
            el = self.selenium.wait('css_selector', '#careers02 > div.swiper-container.swiper-container-initialized.swiper-container-horizontal > div.swiper-wrapper')
            #changes slide location
            transform = el.value_of_css_property('transform')
            location.append(transform)
            #duration:300ms
            time.sleep(4)

        return (len(location) == len(set(location)))

    #search job
    def search_job(self, lang=None):
        input_box = self.selenium.wait('css_selector', '#keyword')
        input_box.click()
        time.sleep(1)
        input_box.send_keys('QO')
        input_box.send_keys(Keys.RETURN)
        result = self.selenium.wait('css_selector', '#jobList > div.jobList_info > div:nth-child(1) > a')
        time.sleep(2)

        if result:
            result.click()
            time.sleep(1)
            return True
        else:
            #1회차에서 검색 결과 없을 시 재시도
            try:
                ActionChains(self.driver).double_click(input_box).perform()
                time.sleep(1)
                input_box.send_keys('QA')
                input_box.send_keys(Keys.RETURN)
                time.sleep(2)
                self.selenium.wait('css_selector', '#jobList > div.jobList_info > div:nth-child(1) > a').click()
                time.sleep(1)
                return True
            #2회차에서 검색 결과 없을 시 종료
            except AttributeError as e:
                LOGGER.info("Job list not found")
        return True

    #href값이 현재 페이지 일 경우의 링크 검증
    def check_link_careers(self, lang=None):     
        a_tags = self.selenium.wait('css_selector', '#container a', find_multiple=True)
        time.sleep(2)

        #Link click (Until job list)
        for i in a_tags:
            try:
                self.driver.execute_script("arguments[0].click();", i)
                time.sleep(1)
            except exceptions.StaleElementReferenceException as e:
                return True

            time.sleep(1)
            url = self.driver.current_url
            self.assertTrue('careers' in url, msg='Url not match')

        return True

    #check_link_container() 사용이 불가하여 별도로 만든 함수.
    def check_link_games(self, lang=None):
        el = self.selenium.wait('css_selector', '#container a', find_multiple=True)

        for i in range(len(el)):
            el = self.selenium.wait('css_selector', '#container a', find_multiple=True)
            el[i].click()
            self.switch_to_window()

        self.driver.execute_script('history.go(-1);')
        time.sleep(2)
        return True

    #이전 페이지 이동
    def go_previous_page(self, referrer):
        time.sleep(5)
        current_url = self.driver.current_url
        #print(current_url)
        #go to forward page
        #referrer = self.driver.execute_script('return document.referrer;')

        #current page == forward page일 경우 수행하지 않음
        if (referrer == current_url):
            pass
        else :
            #self.driver.execute_script('history.go(-1);')
            self.driver.get(referrer)
            time.sleep(5)

        return current_url

    #새 창 열기/닫기
    def switch_to_window(self):
        #if new tab
        try:
            time.sleep(3)
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            time.sleep(3)
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(3)
        #if popup
        except IndexError as e:
            #refresh
            self.driver.execute_script('location.href = location.href;')
            time.sleep(3)

        return None

#----------------------- TC기반 function -----------------

    #이미지 출력
    '''
    def image(self, lang=None):
        image_check = self.selenium.is_image_loaded()
        return image_check
    '''


    def is_image_loaded(self, timeout=5, visibility_of=False, lang=None):
        length = self.driver.execute_script('return document.images.length')
        LOGGER.info('image count: {}'.format(length))

        count = 0
        for i in range(0, int(length)):            
            try:
                wait = WebDriverWait(self.driver, timeout)
                result = self.driver.execute_script('return document.images[{0}].complete;'.format(i))
                if visibility_of:
                    wait.until(expected_conditions.visibility_of(result))
                return True if result else None
                
            except (NoSuchElementException, TimeoutException) as e:
                LOGGER.warning('{} image load fail'.format(count + 1))
                break
            if result:
                count += 1
        return (length == count)


#----------------------- 함수 실행 ------------------------
    #Main
    def test_main(self):
        self.open_url(BASE_URL)
        self.execute_fn(['is_image_loaded'])
        #self.execute_fn(['image', 'check_video', 'check_effect', 'scroll', 'check_header', 'check_container', 'check_footer'])

    #about
    def no_test_about(self):
        self.open_url(BASE_URL + 'about')
        self.execute_fn(['image', 'check_video', 'check_effect', 'scroll', 'check_header', 'check_footer'])

    #history
    def no_test_history(self):
        self.open_url(BASE_URL + 'history')
        self.execute_fn(['image', 'scroll', 'check_header','check_footer'])

    #location
    def no_test_location(self):
        self.open_url(BASE_URL + 'location')
        self.execute_fn(['image', 'scroll', 'check_header', 'check_footer'])

    #blog
    def no_test_blog(self):
        self.open_url(BASE_URL + 'blog')
        self.execute_fn(['image', 'scroll', 'check_header', 'check_container', 'check_footer'])

    #careers
    def no_test_careers(self):
        self.open_url(BASE_URL + 'careers')
        self.execute_fn(['image', 'check_video','check_swiper' ,'scroll', 'check_header', 'check_link_careers', 'search_job', 'check_footer'])

    #Games
    def no_test_games(self):
        self.open_url(BASE_URL + 'games')
        self.execute_fn(['image', 'check_video', 'check_effect', 'scroll', 'check_header', 'check_container', 'check_footer'])

    #Games > pokopang town
    def no_test_pokopangtown(self):
        self.open_url(BASE_URL + 'pokopangtown')
        self.execute_fn(['image', 'scroll', 'check_header', 'check_link_games', 'check_footer'])

    #Games > pokopoko
    def no_test_pokopoko(self):
        self.open_url(BASE_URL + 'pokopoko')
        self.execute_fn(['image', 'scroll', 'check_header', 'check_link_games', 'check_footer'])

    #Games > pokopang
    def no_test_pokopang(self):
        self.open_url(BASE_URL + 'pokopang')
        self.execute_fn(['image', 'scroll', 'check_header', 'check_link_games', 'check_footer'])

    #brand
    def no_test_brand(self):
        self.open_url(BASE_URL + 'brand')
        self.execute_fn(['image', 'check_video', 'scroll', 'check_header', 'check_footer'])

    '''
    #url별 fn list 실행
    def execute_fn(self, func_list):
        #calling fn name
        call_fn = sys._getframe(1).f_code.co_name

        #페이지 별 LANG_LIST 셋팅
        LANG = [LANG_LIST[0]] if call_fn in ['test_blog', 'test_careers'] else LANG_LIST

        for i in LANG:
            self.check_language(i)
            #a = self.selenium.wait('xpath', '/html/body').get_attribute('class')
            #print(a)
            #파라미터 존재 여부에 맞춰 코드 실행
            for f in func_list:
                try:
                    result = getattr(self, f)()
                except:
                    result = getattr(self, f)(i)
                    
                self.assertTrue(result, msg="{0}({1}): Fail".format(f, i))
                LOGGER.info("{0}({1}): Pass".format(f, i))
    '''

    def execute_fn(self, func_list):
        #calling fn name
        call_fn = sys._getframe(1).f_code.co_name

        #페이지 별 LANG_LIST 셋팅
        LANG = [LANG_LIST[0]] if call_fn in ['test_blog', 'test_careers'] else LANG_LIST

        for i in LANG:
            self.check_language(i)
            for f in func_list:
                result = getattr(self, f)(i)
                self.assertTrue(result, msg="{0}({1}): Fail".format(f, i))
                LOGGER.info("{0}({1}): Pass".format(f, i))