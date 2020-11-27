from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait

if __name__ == "__main__":
    options = Options()
    options.add_argument('-headless')
    driver = Firefox(executable_path='/usr/local/bin/geckodriver', options=options)
    wait = WebDriverWait(driver, timeout=10)
    driver.get('http://www.google.com')
    wait.until(expected.visibility_of_element_located((By.NAME, 'q'))).send_keys('headless firefox' + Keys.ENTER)
    wait.until(expected.visibility_of_element_located((By.CSS_SELECTOR, '#ires a'))).click()
    print(driver.page_source)
    driver.quit()


# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# browser = webdriver.Firefox(executable_path="/usr/lib/geckodriver")
# browser.get('https://www.linuxhint.com')
# print('Title: %s' % browser.title)
# browser.quit()



# from selenium import webdriver
# # from selenium.webdriver.chrome.options import Options

# # chromium_path = "/usr/lib/chromium-browser"

# #chromedriver_path = "/usr/bin/chromedriver"

# # opts = Options()
# # opts.binary_location = chromium_path
# opts.add_argument("headless")
# # driver = webdriver.Chrome(chrome_options=opts)

# #driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')  # Optional argument, if not specified will search path.

# driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")

# driver.get('http://www.google.com/xhtml');
# time.sleep(5) # Let the user actually see something!
# someText = driver.find_element_by_name('SIvCob').text
# print("SIvCob :", someText)
# driver.quit()
