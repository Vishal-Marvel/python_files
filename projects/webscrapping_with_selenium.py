from selenium import webdriver
import selenium
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException, NoSuchFrameException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time, pywhatkit, pyttsx3
from datetime import datetime
from tkinter import messagebox
from datetime import datetime
import winsound
duration = 1000  # milliseconds
freq = 440  # Hz


WINDOW_SIZE = "1080,800"
options = webdriver.ChromeOptions()
# options.add_argument("--headless")

# options.add_argument("--window-size=%s" % WINDOW_SIZE)
options.add_argument("user-data-dir=F:/codings/user_data")
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)


#specify the path to chromedriver.exe (download and save on your computer)
driver = webdriver.Chrome('D:/downloads/chromedriver.exe', chrome_options=options)
# driver = webdriver.

#open the webpage
# driver.get("https://courses.edx.org/login?next=https%3A%2F%2Fenterprise.edx.org%2Fsairam-institutions&enterprise_customer=cfcb8e6c-0e56-49f4-8c61-e11d83e85865&proxy_login=True")
# time.sleep(3)

#target username
# username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
# # enter username
# username.clear()
# username.send_keys("narayanan.pvn@gmail.com")
# # enter password
# password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
# password.clear()
# password.send_keys("edx@200104")

# WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
# time.sleep(4)


driver.get("https://learning.edx.org/course/course-v1:IBM+DS0101EN+2T2021/block-v1:IBM+DS0101EN+2T2021+type@sequential+block@170bd95e77ea436e8c7b1e5c6b9b1867/block-v1:IBM+DS0101EN+2T2021+type@vertical+block@0a5125d5d33e44e7bb471886a903e29d")
url_count = 0
# driver.switch_to.frame('unit-iframe')

# iframe = driver.find_elements_by_tag_name('iframe')
# print(iframe)
while True:
    winsound.Beep(freq, duration)
    url_count += 1
    print(driver.current_url, datetime.now(), url_count, sep='\n')
    time.sleep(7)
    tot_time = ''
    try:
        driver.switch_to.frame('unit-iframe')
        tot_time = str(driver.find_element_by_class_name('vidtime').text).split('/')[1].replace(' ','')
    except NoSuchElementException as e:
        if 'vidtime' in str(e):
            tot_time = ''
        elif 'unit-iframe' in str(e):
            messagebox.showerror('error', str(e))
        else:
            messagebox.showerror('error', str(e))
    except NoSuchFrameException as e:
        messagebox.showerror('error', str(e))
        pass
    except IndexError:
        pass     

    if not tot_time == '0:00':
        iframe = driver.find_elements_by_tag_name('iframe')

        # print(iframe)
        # break
        for frame in iframe:
            try:
                driver.switch_to.frame(frame)
                driver.find_element_by_xpath("//*[@id=\"movie_player\"]/div[4]/button").click()
                # butt = driver.find_element_by_id('movie_player')
                # driver.execute_script('arguments[0].click()', butt)
                time.sleep(7)
                break
            except NoSuchElementException as e:
                # messagebox.showerror('error', str(e))
                continue
            except StaleElementReferenceException as e:
                # messagebox.showerror('error', str(e))
                continue
            except Exception as e:
                messagebox.showerror('error', str(e))
                pass
    elif tot_time == '0:00':
        try:
            driver.find_element_by_xpath('/html/body/div[4]/div/section/main/div/div/div[2]/div/div/div[2]/div[1]/div[5]/div[2]/div[1]/button').click()
            # but = driver.find_element_by_xpath('/html/body/div[4]/div/section/main/div/div/div[2]/div/div/div[2]/div[1]/div[5]/div[2]/div[1]/button')

            # driver.execute_script('arguments[0].click()', but)
            time.sleep(5)
        except NoSuchElementException:
            pass

    driver.switch_to.default_content()
    driver.switch_to.frame('unit-iframe')
    try:
        li=False
        try:
            li=driver.find_elements_by_xpath('//ol[@class="subtitles-menu"]/li')
            count = len(li) - 10
        except NoSuchElementException:
            pass
        except Exception as e:
            messagebox.showerror('error', str(e))
        while True:
            try:
                tot_time = str(driver.find_element_by_class_name('vidtime').text).split('/')[1].replace(' ','')
                present_time = str(driver.find_element_by_class_name('vidtime').text).split('/')[0].replace(' ','')
                # print(present_time, tot_time, present_time == tot_time)
                if present_time == tot_time != '0:00':
                    break
                else:
                    if li and not present_time == '0:00':
                        driver.find_element_by_xpath('//ol[@class="subtitles-menu"]/li[{}]/span'.format(count)).click()
                        
                        time.sleep(5)
                        li = False
                    time.sleep(2)
            except IndexError:
                pass
            except NoSuchElementException as e:
                if 'vidtime' in str(e):
                    break
                elif 'subtitles-menu' in str(e):
                    continue
                else:
                    messagebox.showerror('error', str(e))
                    
                    pass                    

    except NoSuchElementException as e:
        messagebox.showerror('error', str(e))
        pass
    except KeyboardInterrupt:
        driver.close()
    except Exception as e:
        messagebox.showerror('error', str(e))
    driver.switch_to.default_content()
    button = driver.find_element_by_xpath('//*[@id="main-content"]/div[2]/div[2]/div[1]/div/div/div/div[2]/button[2]')
    driver.execute_script('arguments[0].click()', button)
    
    