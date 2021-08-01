import unittest
import os
from appium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
 
class TableSearchTest(unittest.TestCase):

    def test_setUp(self, path, file_name):
        
        #Test App 경로
        app = os.path.join(os.path.dirname(__file__), path, file_name)
        app = os.path.abspath(app)

        # Set up appium
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

    def no_test_field(self):
        #driver = self.driver
        #wait = WebDriverWait(driver, 20)
        pass

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TableSearchTest)
    unittest.TextTestRunner(verbosity=2).run(suite)