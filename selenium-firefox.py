import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


krx_url = "http://marketdata.krx.co.kr/mdi#document=040601"

input_id_kospi = "market_gubun1a87ff679a2f3e71d9181a67b7542122c"
btn_id_search = "btnidc81e728d9d4c2f636f067f89cc14862c"
span_id_download = "6f4922f45568161a8cdf4ad2299f6d23"
selector_for_test_loaded = "td[data-name='isu_cd']"

ff_driver = webdriver.Firefox()
ff_driver.get(krx_url)


def enable_download_headless(browser, download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)


try:
    WebDriverWait(ff_driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector_for_test_loaded)),"asdfasdf"
    )

    element_kospi = ff_driver.find_element_by_id(input_id_kospi)
    element_kospi.click()

    element_btn_search = ff_driver.find_element_by_id(btn_id_search)
    element_btn_search.click()

    downloads = ff_driver.find_element_by_id(span_id_download).find_elements_by_css_selector('button')
    # test = downloads[2]
    # test.click()

    ff_driver.implicitly_wait(3000)
    ff_driver.execute_async_script("$.down(this,'csv','form8e296a067a37563370ded05f5a3bf3ec');")
    # ff_driver.implicitly_wait(50)



finally:
    ff_driver.quit()

