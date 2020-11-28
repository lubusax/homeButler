# downloaded chrome driver build for ubuntu (arm)
# installed with "sudo dpkg -I chromedriver_blah_blah.deb"
# moved to /usr/local/share/driver (previously made symlinks with /usr/)
# included it in PATH (modifying .bashrc of user pi)

# run chromium-browser --headless
# you need to run this script as "sudo" if you want to save screenshots
# but if you run this script as sudo, then you have to --no-sandbox (as an option)
#https://medium.com/@pyzzled/running-headless-chrome-with-selenium-in-python-3f42d1f5ff1d
#https://chromedriver.chromium.org/getting-started ## headless option missing?
# get chromedriver # https://stackoverflow.com/questions/42492646/error-using-selenium-with-chromedriver-on-raspberry-pi-3-raspbian-jessie


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
  options = Options()
  options.add_argument("--headless")
  options.add_argument("--window-size=1920x1080")
  options.add_argument("--no-sandbox")

  driver = webdriver.Chrome(options=options, executable_path='/usr/local/share/chromedriver')

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

def appendMeasurement(filePath,timestamp, up, down):
  pass

measurementPeriod = 60 # seconds
minUp = 10000
maxUp = 0
up=10.0
timeMin = "0204"
webSite = "https://www.speedtest.net/"
fileBandwidthMeasurements = "fileBandwidthMeasurements"

Disp = Display.Display()
Disp.displayMsgRaw([(0,0), 16, "Hello"])

driver = getDriver()
# getWebSite(driver, webSite)

# clickAcceptGDPRpopup(driver)

while True:
  try:
    Disp.displayMsgRaw([(0,1), 16, "LAST: "+str(up)+ "\nMIN: "+str(minUp)+"\ntime MIN: "+ str(timeMin)+ "\nMAX: "+str(maxUp)])
    getWebSite(driver, webSite)
    try:
      clickAcceptGDPRpopup(driver)
    except Exception as e:
      print ("there was an exception while trying to click GDPR Pop Up: ",e)
    [timestamp,up,down] = measurementUpDownBandwidth(driver, measurementPeriod)
    appendMeasurement(fileBandwidthMeasurements,timestamp, up, down)
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




