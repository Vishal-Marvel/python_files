from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time, pywhatkit, pyttsx3
from datetime import datetime

speaker = pyttsx3.init()

WINDOW_SIZE = "1920,1080"
options = webdriver.ChromeOptions()
options.add_argument("--headless")

options.add_argument("--window-size=%s" % WINDOW_SIZE)
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)


#specify the path to chromedriver.exe (download and save on your computer)
driver = webdriver.Chrome('F:/vishal/installer raw file/chromedriver.exe', chrome_options=options)

#open the webpage
driver.get("http://main.velammallive.in/")

def attain():
    time.sleep(5)
    anchors = driver.find_elements_by_tag_name('a')
    anchors = [a.get_attribute('href') for a in anchors]
    anchors = [a for a in anchors if 'https://main.velammallive.in/mod/bigbluebuttonbn/view.php' in str(a)]
    message = '\nTotal number of classes = {}'.format(len(anchors))
    conform_list = []
    conform_class_list = []
    for link in anchors:
        driver.get(link)
        time.sleep(1)
        try:
            conform = driver.find_element_by_tag_name('input')
            conform_list = [c.get_attribute('value') for c in conform]
            conform_class_list.append(link)
        except TypeError:
            pass

    message += '\n\n' + 'Number of running classes = {}'.format(len(conform_list))
    print(message, conform_class_list, sep='\n')
    # pywhatkit.sendwhatmsg('+919791077398', message, now_h, now_m+1, wait_time=30)


while True:
    try:
        #target username
        username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

        #enter username and password
        username.clear()
        username.send_keys("H30525")
        password.clear()
        password.send_keys("alpha123@#2020")

        #target the login button and click it
        button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

        time.sleep(5)
        while True:
            now_h, now_m = int(datetime.now().strftime('%H')), int(datetime.now().strftime('%M'))
            attain()
            if 8<=now_h<=15:
                driver.refresh()
                attain()
            elif now_h>15:
                break
            time.sleep(1500)

    except Exception:
        driver.refresh()

