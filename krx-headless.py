import os

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import datetime

download_dir = "/Users/kyle.sgjung/temp"


def enable_download_headless(browser,_download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': _download_dir}}
    browser.execute("send_command", params)


chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
})
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')

krx_url = "http://marketdata.krx.co.kr/mdi#document=040601"

input_id_kospi = "market_gubun1a87ff679a2f3e71d9181a67b7542122c"
input_id_kosdaq = "market_gubun298dce83da57b0395e163467c9dae521b"

btn_id_search = "btnidc81e728d9d4c2f636f067f89cc14862c"
span_id_download = "6f4922f45568161a8cdf4ad2299f6d23"
selector_for_test_loaded = "td[data-name='isu_cd']"

browser = webdriver.Chrome(options=chrome_options)
enable_download_headless(browser, download_dir)
browser.get(krx_url)

try:
    element_kospi = browser.find_element_by_id(input_id_kospi)
    element_kospi.click()

    element_btn_search = browser.find_element_by_id(btn_id_search)
    element_btn_search.click()

    # browser.execute_script("$.down(this,'csv','form8e296a067a37563370ded05f5a3bf3ec');")

    WebDriverWait(browser, 50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector_for_test_loaded)), "asdfasdf"
    )

    downloads = browser.find_element_by_id(span_id_download).find_elements_by_css_selector('button')
    csv = downloads[2]

    csv.click()
    time.sleep(60)

    sep = "/"
    date_now = datetime.datetime.now()
    str_date = date_now.strftime('%Y_%m')

    downloaded_file = download_dir + sep + "data.csv"
    replace_filename = download_dir + sep + str_date + "_" + "_KOSPI_LIST.csv"

    os.rename(downloaded_file, replace_filename)

finally:
    browser.quit()
