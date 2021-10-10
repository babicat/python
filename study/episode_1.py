import pyautogui
import webbrowser
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select

from selenium import webdriver
driver=webdriver.Chrome("C:\work\chromedriver.exe")
driver.get("https://rc-www.pokopang.com/episode/10")

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

# storing the current window handle to get back to dashbord 
main_page = driver.current_window_handle 

#epi_num= driver.find_element_by_xpath('//*[@id="cbp-spmenu-s3"]/div/div/div[2]/h6').text
#title= driver.find_element_by_xpath('//*[@id="cbp-spmenu-s3"]/div/div/div[2]/h2').text
#print("에피소드 no: ",epi_num)
#print("제목 :",title)

# full screen
pyautogui.press('f11')

#######################################################################페이지 넘기기

# lang = en
select = Select(driver.find_element_by_id('changeLanguage'))

time.sleep(1)

# select by visible text
select.select_by_visible_text('日本語')

# select by value 
select.select_by_value('ja')
time.sleep(1)

# mouse movement
width, height = pyautogui.size()
pyautogui.moveTo(width / 8, height / 2,0.3) 
time.sleep(1)

# turn page
for page in range(0, 32):
    pyautogui.click(clicks=1, interval=0.5)

# lang=ko
select = Select(driver.find_element_by_id('changeLanguage'))
time.sleep(1)
select.select_by_visible_text('English')
select.select_by_value('en')
time.sleep(1)

# turn page reverse
for page in range(0, 32):
    pyautogui.hscroll(10, width / 8, height / 2)
    time.sleep(0.5)

# lang=ja
select = Select(driver.find_element_by_id('changeLanguage'))
time.sleep(1)
select.select_by_visible_text('한국어')
select.select_by_value('ko')
time.sleep(1)

# turn page 
for page in range(0, 32):
    pyautogui.click(clicks=1, interval=0.5)

time.sleep(2)

######################################################################별점 등록

# keep score
driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[3]/div/div[1]/div[32]/div/div/div[2]/div/span/span[3]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[3]/div/div[1]/div[32]/div/div/div[3]/div/button[2]').click()

# reply_btn
time.sleep(3)
driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[3]/div/div[1]/div[32]/div/div/a/div').click()
time.sleep(3)
driver.find_element_by_xpath('//*[@id="__next"]/div[3]/div/div[1]/a/img').click()


####################################################################페이스북 댓글등록

# fb_reply_btn
time.sleep(2)
driver.find_element_by_xpath('//*[@id="footer"]/div[2]/div/div[1]/img').click()
time.sleep(2)


im1 = pyautogui.screenshot('C:\\work\\a.png')   #screenshot
write_area = pyautogui.locateOnScreen('C:\\work\\write.png')    #find 'write area' 

#이미지 가운데 위치 얻기
center_a = pyautogui.center(write_area)

#클릭하기
center_b= pyautogui.locateCenterOnScreen('C:\\work\\write.png')
pyautogui.click(center_a)

# ok
time.sleep(1)  
pyautogui.typewrite('Login', interval=0.25)
time.sleep(1)

im1 = pyautogui.screenshot('C:\\work\\b.png')   #screenshot
fb_login = pyautogui.locateOnScreen('C:\\work\\fb_login.png')   #find 'fb login btn'

#이미지 가운데 위치 얻기
center_b = pyautogui.center(fb_login)

#클릭하기
center_b= pyautogui.locateCenterOnScreen('C:\\work\\fb_login.png')
pyautogui.click(center_b)



# changing the handles to access login page 
for handle in driver.window_handles: 
    if handle != main_page: 
        login_page = handle 

# change the control to signin page         
driver.switch_to.window(login_page) 

## facebook login
time.sleep(3)
email = driver.find_element_by_xpath("//input[@name='email']")
password = driver.find_element_by_xpath("//input[@name='pass']")
btn = driver.find_element_by_xpath("//input[@value='로그인']")

time.sleep(1)

email.send_keys("sona@treenod.com")
password.send_keys("password")
btn.click()

time.sleep(3)

# change control to main page 
driver.switch_to.window(main_page)

time.sleep(1)


im1 = pyautogui.screenshot('C:\\work\\c.png')   #screenshot
write_area= pyautogui.locateOnScreen('C:\\work\\write_b.png')    #find 'write area'

#이미지 가운데 위치 얻기
center_c = pyautogui.center(write_area)

#클릭하기
center_c= pyautogui.locateCenterOnScreen('C:\\work\\write_b.png')
pyautogui.click(center_c)


# input text
time.sleep(1)  
pyautogui.typewrite('python auto test:)_20191209', interval=0.1)

time.sleep(1)

im1 = pyautogui.screenshot('C:\\work\\d.png')   #screenshot
register = pyautogui.locateOnScreen('C:\\work\\register.png')   #find 'register btn'

#이미지 가운데 위치 얻기
center_d = pyautogui.center(register)

#클릭하기
center_d= pyautogui.locateCenterOnScreen('C:\\work\\register.png')
pyautogui.click(center_d)

#페북로그인 버튼 ("//button[@data-testid='post-comment-button']")
#댓글 더보기 버튼 ("//button[@class='_1gl3 _4jy0 _4jy3 _517h _51sy _42ft']")


# fb [x]
time.sleep(2)
driver.find_element_by_xpath('//*[@id="__next"]/div[3]/div/div[1]/a/img').click()


######################################################################트위터 공유
# twitter
driver.find_element_by_xpath('//*[@id="twitter_a"]/img').click()

# changing the handles to access login page 
for handle in driver.window_handles: 
    if handle != main_page: 
        login_page = handle 

# change the control to signin page         
driver.switch_to.window(login_page) 

time.sleep(3)
email = driver.find_element_by_xpath("//input[@type='text']")
password = driver.find_element_by_xpath("//input[@type='password']")
btn = driver.find_element_by_xpath("//input[@type='submit']")

time.sleep(1)

email.send_keys("seong2ya@naver.com")
password.send_keys("password")
btn.click()

time.sleep(3)
driver.find_element_by_xpath('//*[@id="update-form"]/div[3]/fieldset/input').click()

# change control to main page 
driver.switch_to.window(main_page) 


#####################################################################페이스북 공유

##페이스북 버튼 클릭
#화면 스크린 샷
im1 = pyautogui.screenshot('C:\\work\\z.png')

#화면에서 fb_share.png와 동일한 이미지 위치 찾기
fb_share_btn = pyautogui.locateOnScreen('C:\\work\\fb_share.png')

#이미지 가운데 위치 얻기
center_z = pyautogui.center(fb_share_btn)
#클릭하기
center_z= pyautogui.locateCenterOnScreen('C:\\work\\fb_share.png')
pyautogui.click(center_z)

##공유
#화면 스크린 샷
time.sleep(3)  
im1 = pyautogui.screenshot('C:\\work\\y.png')

#화면에서 tweeter.png와 동일한 이미지 위치 찾기
fb_share_ok_btn = pyautogui.locateOnScreen('C:\\work\\fb_share_ok.png')

#이미지 가운데 위치 얻기
center_y = pyautogui.center(fb_share_ok_btn)

#클릭하기
center_y= pyautogui.locateCenterOnScreen('C:\\work\\fb_share_ok.png')
pyautogui.click(center_y)



###################################################################이메일 전송
#이메일 아이콘 클릭
#화면 스크린 샷
time.sleep(10)  
im1 = pyautogui.screenshot('C:\\work\\f.png')

#화면에서 email.png와 동일한 이미지 위치 찾기
email_btn = pyautogui.locateOnScreen('C:\\work\\email.png')

#이미지 가운데 위치 얻기
center_f = pyautogui.center(email_btn)

#클릭하기
center_f= pyautogui.locateCenterOnScreen('C:\\work\\email.png')
pyautogui.click(center_f)


##주소입력창에 커서 옮기기
#화면 스크린 샷
time.sleep(3)  
im1 = pyautogui.screenshot('C:\\work\\g.png')

#화면에서 email.png와 동일한 이미지 위치 찾기
email_ad_btn = pyautogui.locateOnScreen('C:\\work\\email_ad.png')

#이미지 가운데 위치 얻기
center_g = pyautogui.center(email_ad_btn)

#클릭하기
center_g= pyautogui.locateCenterOnScreen('C:\\work\\email_ad.png')
pyautogui.click(center_g)


####이메일 입력
time.sleep(3)  
pyautogui.typewrite('seoyeong@treenod.com', interval=0.25)


####이메일 발신
#화면 스크린 샷
im1 = pyautogui.screenshot('C:\\work\\h.png')

#화면에서 register.png와 동일한 이미지 위치 찾기
email_send_btn = pyautogui.locateOnScreen('C:\\work\\email_send.png')

#이미지 가운데 위치 얻기
center_h = pyautogui.center(email_send_btn)

#클릭하기
center_h= pyautogui.locateCenterOnScreen('C:\\work\\email_send.png')
pyautogui.click(center_h)
