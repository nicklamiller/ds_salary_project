"""Configuration for data science project."""
from typing import List

from src.base_models import StrictBaseModel

dict_keyword = 'dict_keyword'
div_class_pattern = 'div_class_pattern'


class ScrapingConfig(StrictBaseModel):
    """Configuration for web scraper."""

    url: str = ''.join([
        'https://www.glassdoor.com/Job/',
        'new-york-python-jobs-SRCH_IL.0,8_IC1132348_KO9,15.htm',
        '?clickSource=searchBox',
    ])
    sleep_time_seconds: int = 2


class JobInfoField(StrictBaseModel):
    """Configuration for each job field extracted from scraped job info."""

    dict_keyword: str
    div_class_pattern: str


class JobInfoFields(StrictBaseModel):
    """Configuration for all desired job info fields to extract."""

    fields: List[JobInfoField] = [
        JobInfoField(**{
            dict_keyword: 'name_of_company',
            div_class_pattern: 'd-flex align-items-center',
        }),
        JobInfoField(**{
            dict_keyword: 'name_of_job',
            div_class_pattern: 'job-title mt-xsm',
        }),
        JobInfoField(**{
            dict_keyword: 'location',
            div_class_pattern: 'location mt-xxsm',
        }),
        JobInfoField(**{
            dict_keyword: 'salary',
            div_class_pattern: 'salary-estimate',
        }),
    ]
