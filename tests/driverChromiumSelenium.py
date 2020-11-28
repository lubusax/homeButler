import sys

# sys.path.append("/home/pi/ras/lib")
# sys.path.append("/home/pi/ras/dicts")
sys.path.append("/home/pi/ras")

from lib import Display
from lib import Utils

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

#@Utils.timer
def measurementUpDownBandwidth(driver, measurementPeriod):
  go_button = driver.find_element_by_css_selector(".start-button a")
  go_button.click()
  print("after click go measure")
  #timestamp = time.strftime('%y%m%d%H%M%S',time.localtime())
  timestamp = time.strftime('%H%M',time.localtime())
  time.sleep(measurementPeriod)
  #driver.get_screenshot_as_file("capture.png") # works fine
  driver.save_screenshot("capture.png")
  up = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text
  down = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span').text
  return [timestamp,float(up),float(down)]

@Utils.timer
def getDriver():
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--window-size=1920x1080")
  chrome_options.add_argument("--no-sandbox")

  driver = webdriver.Chrome(options=chrome_options, executable_path='/usr/local/share/chromedriver')  # Optional argument, if not specified will search path.
  return driver

@Utils.timer
def getWebSite(driver, webSite):
  driver.get(webSite)
  time.sleep(5)

@Utils.timer
def clickAcceptGDPRpopup(driver):
  # Depending on your location, you might need to accept the GDPR pop-up.
  accept_button = driver.find_element_by_id("_evidon-banner-acceptbutton")
  accept_button.click()
  print("after click GDPR pop-up")
  time.sleep(3)

measurementPeriod = 60 # seconds
minUp = 10000
maxUp = 0
up=10.0
timeMin = "0204"
webSite = "https://www.speedtest.net/"

Disp = Display.Display()
Disp.displayMsgRaw([(0,0), 16, "Hello"])

driver = getDriver()
# getWebSite(driver, webSite)

# clickAcceptGDPRpopup(driver)

while True:
  try:
    Disp.displayMsgRaw([(0,5), 16, "LAST: "+str(up)+ "\nMIN: "+str(minUp)+"\ntime MIN: "+ str(timeMin)+ "\nMAX: "+str(maxUp)])
    getWebSite(driver, webSite)
    try:
      clickAcceptGDPRpopup(driver)
    except Exception as e:
      print ("there was an exception while trying to click GDPR Pop Up: ",e)
    [timestamp,up,down] = measurementUpDownBandwidth(driver, measurementPeriod)
    print("after measurements")
    print("TIMESTAMP: ", timestamp)
    print("UP: ", up)
    print("DOWN: ", down)
    if up>maxUp:
      maxUp =(up)

    if up<minUp:
      minUp=up
      timeMin = timestamp

    Disp.displayMsgRaw([(0,5), 16, "LAST: "+str(up)+ "/nMIN: "+str(minUp)+"/ntime MIN: "+ str(timeMin)+ "/nMAX: "+str(maxUp)])
  except Exception as e:
    print ("there was an exception while trying to measure the bandwidth: ",e)




