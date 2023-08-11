from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium import webdriver


def set_chrome_options() -> Options:
    chromedriver_autoinstaller.install()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--disable-dev-shm-usage")
    return chrome_options


def get_properties(names: list, urls: list):
    temp = []
    for name, url in zip(names, urls):
        temp.append([name.text, url.get_attribute("src")])
    return temp


def scrape(url: str) -> list[str]:
    # Declare variables
    force_next_page = False
    skip_reading = False
    runs = 0
    data_complete = []
    driver = webdriver.Chrome(options=set_chrome_options())
    print("Started scraping:")
    driver.get(url)
    while len(data_complete) < 500 and runs < 32:
        flag_data_read = False
        runs += 1
        try:
            if not skip_reading:
                name_temp = driver.find_elements(By.CSS_SELECTOR, ".name.ng-binding")
                url_temp = driver.find_elements(By.XPATH, "//preact/div/div/a[1]/img")
        except NoSuchElementException:
            print("Failed to scrape data on page")
            if not force_next_page:
                force_next_page = True
                continue
            else:
                force_next_page = False
        else:
            if not skip_reading:
                data_complete += get_properties(name_temp, url_temp)
                flag_data_read = True
        try:
            element_present = ec.presence_of_element_located((By.CSS_SELECTOR, ".paging-next"))
            WebDriverWait(driver, 15).until(element_present)
            next_url = driver.find_element(By.CSS_SELECTOR, ".paging-next").get_attribute("href")
        except (TimeoutException, NoSuchElementException):
            print("Page was not loaded in time!")
            if not flag_data_read:
                continue
            else:
                skip_reading = True
        else:
            if next_url:
                skip_reading = False
                driver.get(next_url)
            else:
                break
        print("Run:", runs, "/32 (max), Collected rows:", len(data_complete))
    driver.close()
    rows = len(data_complete)
    if rows != 500:
        print("Parsing finished, wrong number of rows: ", rows)
        exit()
    return data_complete
