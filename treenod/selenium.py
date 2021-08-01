# -*- coding: utf-8 -*-
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException

LOGGER = logging.getLogger(__name__)


class SeleniumException(Exception):
    pass


class Selenium(object):
    def __init__(self, driver=None, host=None, browser=None):
        self._driver = None
        
        if driver:
            self._driver = driver
            self.capabilities = None
        elif host:
            if browser == 'firefox':
                self.capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
            elif browser == 'ie':
                self.capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
            elif browser == 'edge':
                self.capabilities = webdriver.DesiredCapabilities.EDGE.copy()
            elif browser == 'safari':
                self.capabilities = webdriver.DesiredCapabilities.SAFARI.copy()
            elif browser == 'chrome':
                self.capabilities = webdriver.DesiredCapabilities.CHROME.copy()
            elif browser == 'ipad':
                options = webdriver.ChromeOptions()
                # https://chromium.googlesource.com/chromium/src/+/master/chrome/test/chromedriver/chrome/mobile_device_list.cc
                #mobile_emulation = {
                #    'deviceMetrics': { 'width': 360, 'height': 640, 'pixelRatio': 3.0 },
                #    'userAgent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'
                #}
                #options.add_experimental_option("mobileEmulation", mobile_emulation)
                #options.add_experimental_option("mobileEmulation", {'deviceName': 'Nexus 5'})
                options.add_experimental_option("mobileEmulation", {'deviceName': 'iPad Mini'})
                self.capabilities = options.to_capabilities()

                # height = int(driver.execute_script('return window.screen.height'))
                # width = int(driver.execute_script('return window.screen.width'))
                # driver.set_window_size(width, height * 1.2)
            else:
                self.capabilities = {
                    'browserName': 'chrome',
                    'chromeOptions': {
                        'args': [
                            '--disable-gpu',
                            '--headless',
                            '--disable-impl-side-painting',
                            '--disable-gpu-sandbox',
                            '--disable-accelerated-2d-canvas',
                            '--disable-accelerated-jpeg-decoding',
                            '--no-sandbox',
                            '--test-type=ui',
                        ],
                    },
                }
            self._driver = webdriver.Remote(command_executor=host, desired_capabilities=self.capabilities)
        else:
            raise ValueError('host or driver parameter required')

        LOGGER.debug('selenium session_id {0}'.format(self._driver.session_id))

    def __del__(self):
        self.close()

    def close(self):
        if self._driver:
            if self.capabilities:
                self.capabilities.clear()

            try:
                self._driver.close()
            except Exception as ex:
                #LOGGER.exception(ex)
                pass
            try:
                self._driver.quit()
            except Exception as ex:
                #LOGGER.exception(ex)
                pass
        self._driver = None

    @property
    def driver(self):
        return self._driver

    def browser_log(self, disable_warning=False):
        try:
            logs = self._driver.get_log('browser')
        except:
            return None

        if logs:
            if disable_warning and isinstance(logs, list):
                logs = [v for v in logs if v.get('level', '') != 'WARNING']
            if logs:
                LOGGER.warning(logs)
        return logs

    def open_url(self, url, disable_warning=False):
        try:
            self._driver.get(url)
        except Exception as e:
            LOGGER.warning('open_url({0}) error - {1}'.format(url, e))
            return False

        return False if self.browser_log(disable_warning=disable_warning) else True

    def wait(self, by_type, by_value, timeout=5, visibility_of=False, find_multiple=False):
        by_types = ['id', 'name', 'xpath', 'link_text', 'partial_link_text', 'tag_name', 'class_name', 'css_selector']
        #by_types 리스트에 없는 타입 전달 시 에러메시지 출력
        if by_type not in by_types:
            raise ValueError('elements not permitted')

        try:
            #find elements일 경우에만 m='s'를 붙여준다.
            m = 's' if find_multiple else ''

            #el = WebDriverWait(self._driver, timeout).until(lambda _: getattr(self._driver, 'find_element_by_' + by_type)(by_value))
            #timeout 5초로 셋팅한다.
            wait = WebDriverWait(self._driver, timeout)
            #5초동안 by_value에 해당하는 element를 찾은 후 el에 저장한다. 
            el = wait.until(lambda _: getattr(self._driver, 'find_element' + m + '_by_' + by_type)(by_value))

            #element가 보이는 상태일 경우(visibility_of=True로 전달한 경우)
            if visibility_of:
                #el이 화면에 보일때까지 기다린다.(5초)
                wait.until(expected_conditions.visibility_of(el))
            #el이 있으면 리턴하고, 없으면 아무것도 리턴하지 않는다.
            return el if el else None
        #element를 못 찾거나, 5초 경과 시 pass
        except (NoSuchElementException, TimeoutException) as e:
            # LOGGER.warning('wait_by_{0}({1}) error - {2}'.format(by_type, by_value, e))
            pass
        
        return None


    def scroll_down(self, by_id='viewport', timeout=3):
        element = self.wait('id', by_id)

        if element:
            try:
                wait = WebDriverWait(self._driver, timeout)
                # element = wait.until(expected_conditions.presence_of_element_located((By.ID, by_id)))
                element = wait.until(expected_conditions.visibility_of(element))
            except TimeoutException as e:
                LOGGER.warning('scroll_down() timeout - {0}'.format(e))
                return False

            try:
                actions = webdriver.ActionChains(self._driver)
                actions.move_to_element(element)
                actions.click()
                actions.send_keys(Keys.END)
                actions.perform()
                time.sleep(3)
            except WebDriverException as e:
                LOGGER.warning('scroll_down() error - {0}'.format(e))
        else:
            try:
                self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            except WebDriverException as e:
                LOGGER.warning('scroll_down() error - {0}'.format(e))
            time.sleep(timeout)

        return False if self.browser_log(disable_warning=True) else True


    def get_text(self, *args, **kwargs):
        el = self.wait(*args, **kwargs)
        if isinstance(el, list):
            text = [e.get_attribute('innerText') for e in el]
        else:
            text = el.get_attribute('innerText')
        return text


    def is_image_loaded(self, ignore_hidden=False):
        length = self._driver.execute_script('return document.images.length')
        LOGGER.debug('image count: {}'.format(length))

        count = 0
        for i in range(0, int(length)):            
            result = self._driver.execute_script('return document.images[{0}].complete;'.format(i))
            #firefox에서 style.visibility, width, height 값 못가져와서 사용불가
            #visible = self._driver.execute_script('return document.images[{0}].style.visibility;'.format(i))
            #width = self._driver.execute_script('return document.images[{0}].width;'.format(i))
            #height = self._driver.execute_script('return document.images[{0}].height;'.format(i))

            # ignore_hidden option 이 켜지면 visible 이 아닌경우 check count 증가
            # 이미지가 로드되었고 가로,세로 크기가 합이 1보다 큰 경우 check count 증가
            #if (ignore_hidden and visible != 'visible') or (result and (width + height > 1)):
            if result:
                count += 1

        # 전에 이미지 갯수와 check count 비교
        print(count)
        return (length == count)

