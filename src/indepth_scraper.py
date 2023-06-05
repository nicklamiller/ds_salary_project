import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

url = ''.join([
    'https://www.glassdoor.com/Job/',
    'new-york-python-jobs-SRCH_IL.0,8_IC1132348_KO9,15.htm',
    '?clickSource=searchBox',
])

number_of_jobs = 60
sleep_seconds = 5


def main():
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(url)

    try:
        time.sleep(10)
        all_job_data = iterate_through_jobs(driver, number_of_jobs)

    finally:
        driver.quit()

    return all_job_data


def iterate_through_jobs(driver, number_of_jobs: int):

    current_job_number = 0
    while current_job_number < number_of_jobs:
        try:
            all_jobs_container = driver.find_element(By.CSS_SELECTOR, '.hover')
            all_job_elements = all_jobs_container.find_elements(
                By.TAG_NAME, 'li',
            )
            all_job_data = []
            for job_element in all_job_elements:
                driver.execute_script('arguments[0].click();', job_element)
                job_data = _get_job_data(driver)
                all_job_data.append(job_data)
                current_job_number += 1
            _go_next_page(driver)
            time.sleep(sleep_seconds)
        except NoSuchElementException:
            _close_signup_popup(driver)
    return all_job_data


def _get_job_data(driver):
    return _get_common_job_data(driver)


def _get_common_job_data(driver):
    job_dict = {}
    job_dict['company_name'] = driver.find_element(By.CSS_SELECTOR, '.css-87uc0g').text
    job_dict['location'] = driver.find_element(By.CSS_SELECTOR, '.css-56kyx5').text
    job_dict['job_title'] = driver.find_element(By.CSS_SELECTOR, '.css-1vg6q84').text
    job_dict['job_description'] = driver.find_element(By.CSS_SELECTOR, '.jobDescriptionContent').text
    return job_dict


def _close_signup_popup(driver):
    driver.find_element(
        By.CSS_SELECTOR,
        '.modal_closeIcon',
    ).click()


def _go_next_page(driver):
    next_page_button = driver.find_element(
        By.CSS_SELECTOR,
        '.nextButton',
    )
    driver.execute_script('arguments[0].click();', next_page_button)


if __name__ == '__main__':
    all_job_data = main()
    print(all_job_data)
