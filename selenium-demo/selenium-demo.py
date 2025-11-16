"""
# For Mac / Linux
docker run -it -d \
  --platform linux/amd64 \
  --name selenium-dev \
  --shm-size=2g \
  -p 14444:4444 \
  -p 15900:5900 \
  -p 17900:7900 \
  -e SE_NODE_OVERRIDE_MAX_SESSIONS=true \
  -e SE_NODE_MAX_SESSIONS=5 \
  -e JAVA_OPTS=-XX:ActiveProcessorCount=5 \
  selenium/standalone-chrome:142.0-20251101

# For Windows
docker run -it -d `
  --platform linux/amd64 `
  --name selenium-dev `
  --shm-size=2g `
  -p 14444:4444 `
  -p 15900:5900 `
  -p 17900:7900 `
  -e SE_NODE_OVERRIDE_MAX_SESSIONS=true `
  -e SE_NODE_MAX_SESSIONS=5 `
  -e JAVA_OPTS="-XX:ActiveProcessorCount=5" `
  selenium/standalone-chrome:142.0-20251101
"""

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def wait_for_page_ready(driver: webdriver.Remote, timeout=15):
    """Wait until the document ready state is complete."""
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")  # required for some containerized runs
chrome_options.add_argument("--disable-extensions")  # keep Chrome lightweight for automation
chrome_options.add_argument("--disable-gpu")  # avoid GPU issues on headless servers
chrome_options.add_argument("--window-size=1080,720")  # ensure consistent viewport
chrome_options.add_argument("--ignore-certificate-errors")  # skip TLS warnings on demo sites
chrome_options.add_argument("--allow-insecure-localhost")  # permit self-signed localhost certs
# chrome_options.add_argument("--headless=new")  # uncomment if you don't need a visible browser

driver = webdriver.Remote(
    command_executor="http://127.0.0.1:14444/wd/hub",
    options=chrome_options,
)

url = "https://www.ptt.cc/bbs/index.html"

driver.get(url)


wait_for_page_ready(driver)
time.sleep(10)

driver.find_element(by=By.PARTIAL_LINK_TEXT, value="Gossiping").click()
wait_for_page_ready(driver)
time.sleep(10)

driver.find_element(by=By.CLASS_NAME, value="btn-big").click()
wait_for_page_ready(driver)
time.sleep(10)

html = driver.page_source
# print(driver.find_element(by=By.TAG_NAME, value="html").text)
print(html)
print("===")

cookie = driver.get_cookies()
print(cookie)

driver.quit()