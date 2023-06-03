import time
from typing import List

import bs4
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from src.base_models import StrictBaseModel
from src.configuration import JobInfoField, JobInfoFields, ScrapingConfig

# scraping tutorial: https://www.scrapingdog.com/blog/scrape-glassdoor/


class WebScraper(StrictBaseModel):
    config: ScrapingConfig = ScrapingConfig()

    def scrape_data(self) -> pd.DataFrame:
        response = self.fetch_url_data()
        all_jobs = self.find_all_jobs(response)
        extracted_jobs = self.extract_all_jobs_info(all_jobs)
        return pd.DataFrame(extracted_jobs)

    def fetch_url_data(self) -> str:
        driver = webdriver.Firefox()
        driver.get(self.config.url)
        time.sleep(self.config.sleep_time_seconds)
        response = driver.page_source
        driver.close()
        return response

    def find_all_jobs(
        self,
        response: str,
    ) -> bs4.element.ResultSet:
        soup = bs4.BeautifulSoup(response, 'html.parser')
        all_jobs_container = soup.find('ul', {'class': 'css-7ry9k1'})
        return all_jobs_container.find_all('li')

    def extract_all_jobs_info(
        self,
        found_jobs: bs4.element.ResultSet,
    ) -> List[dict]:
        all_jobs_info = []
        for job in found_jobs:
            single_job_info = _extract_job_all_info_fields(job)
            all_jobs_info.append(single_job_info)
        return all_jobs_info


def _extract_job_all_info_fields(
    single_job_info: bs4.element.Tag,
) -> dict:
    job_info_fields = JobInfoFields().fields
    opening = {}
    for job_info_field in job_info_fields:
        opening = _extract_job_info_field(
            opening,
            single_job_info,
            job_info_field,
        )
    return opening


def _extract_job_info_field(
    opening: dict,
    single_job_info: bs4.element.Tag,
    job_info_field: JobInfoField,
) -> dict:
    try:
        opening[job_info_field.dict_keyword] = single_job_info.find(
            'div',
            {'class': job_info_field.div_class_pattern},
        ).text
    except NoSuchElementException:
        opening[job_info_field.dict_keyword] = None
    return opening


if __name__ == '__main__':
    web_scraper = WebScraper()
    scraped_data = web_scraper.scrape_data()
    scraped_data.head()
