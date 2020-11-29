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

def getTimestamp():
  return time.strftime('%y%m%d%H%M%S',time.localtime())

def getDay():
  return time.strftime('%y%m%d',time.localtime())

def appendLineToFile(pathFile,lineToAppend):
  with open(pathFile, 'a') as f: 
    f.write(str(lineToAppend+"\n"))

def getPathFile(fileType):
  directory = "/home/pi/homeButler/tests/measurementsBandwidth"
  if not os.path.exists(directory):
    os.mkdir(directory)
  pathFile = directory + "/" + fileType + getDay()
  print("filetype "+fileType+ " : "+pathFile)
  if not os.path.exists(pathFile):
    with open(pathFile, 'w') as f: 
      pass
  return pathFile

def getDriver():
  options = Options()
  options.add_argument("--headless")
  options.add_argument("--window-size=1920x1080")
  options.add_argument("--no-sandbox")

  driver = webdriver.Chrome(options=options, executable_path='/usr/local/share/chromedriver')
  appendLineToFile(fileLog, "got the driver at "+ getTimestamp())
  return driver

def getWebSite(driver, webSite):
  driver.get(webSite)
  time.sleep(5)
  appendLineToFile(fileLog, "got the website at "+ getTimestamp())

def clickAcceptGDPRpopup(driver):
  accept_button = driver.find_element_by_id("_evidon-banner-acceptbutton")
  accept_button.click()
  appendLineToFile(fileLog, "after click GDPR pop-up at "+ getTimestamp())
  time.sleep(3)

def measurementUpDownBandwidth(driver, measurementWaitPeriod):
  go_button = driver.find_element_by_css_selector(".start-button a")
  go_button.click()
  timestamp = getTimestamp()
  appendLineToFile(fileLog, "in method measurementUpDownBandwidth " + timestamp)
  #driver.save_screenshot("screenBefore.png")
  time.sleep(measurementWaitPeriod)
  #driver.save_screenshot("screenAfter.png")  
  up = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text
  down = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span').text
  return [timestamp,float(up),float(down)]

measurementWaitPeriod = 60 # seconds

webSite = "https://www.speedtest.net"

fileMeasurementsData  = getPathFile("data")

fileLog               = getPathFile("log")

appendLineToFile(fileLog, "_"*100)
appendLineToFile(fileLog, "starting measureBandwidthOnce at "+ getTimestamp() )

driver                = getDriver()

getWebSite( driver, webSite)

try:
  clickAcceptGDPRpopup( driver)
except Exception as e:
  appendLineToFile(fileLog, "there was an exception while trying to click GDPR Pop Up: "+ str(e) )

try:
  [timestamp,up,down] = measurementUpDownBandwidth( driver, measurementWaitPeriod)
  appendLineToFile(fileMeasurementsData, str(timestamp)+", "+str(up)+", "+str(down))
  appendLineToFile(fileLog, "after measurements "+timestamp+"- UP: "+str(up)+"- DOWN: "+str(down))
  print("after measurements "+timestamp+"- UP: "+str(up)+"- DOWN: "+str(down) )
except Exception as e:
  print("there was an exception while trying to measure the bandwidth: " + e)
  appendLineToFile(fileLog, "there was an exception while trying to measure the bandwidth: " + e)
  appendLineToFile(fileLog, "_"*100)