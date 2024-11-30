from abc import ABC, abstractmethod
from re import A

from constants import LINKEDIN
from src.ai_hawk.authenticator import AIHawkAuthenticator
from src.job import Job
from src.jobContext import JobContext

from selenium.webdriver.remote.webelement import WebElement
from typing import List


class WebPage(ABC):

    def __init__(self, driver):
        self.driver = driver


class BaseJobsPage(WebPage):

    def __init__(self, driver, parameters):
        super().__init__(driver)
        self.parameters = parameters

    @abstractmethod
    def next_job_page(self, position, location, page_number):
        pass

    @abstractmethod
    def job_tile_to_job(self, job_tile: WebElement) -> Job:
        pass

    @abstractmethod
    def get_jobs_from_page(self, scroll=False) -> List[WebElement]:
        pass


class BaseJobPage(WebPage):

    def __init__(self, driver):
        super().__init__(driver)

    @abstractmethod
    def goto_job_page(self, job: Job):
        pass

    @abstractmethod
    def get_apply_button(self, job_context: JobContext) -> WebElement:
        pass

    @abstractmethod
    def get_job_description(self, job: Job) -> str:
        pass

    @abstractmethod
    def get_recruiter_link(self) -> str:
        pass

    @abstractmethod
    def click_apply_button(self, job_context: JobContext) -> None:
        pass


class BaseApplicationPage(WebPage):

    def __init__(self, driver):
        super().__init__(driver)

    @abstractmethod
    def has_next_button(self) -> bool:
        pass

    @abstractmethod
    def click_next_button(self) -> None:
        pass

    @abstractmethod
    def has_submit_button(self) -> bool:
        pass

    @abstractmethod
    def click_submit_button(self) -> None:
        pass

    @abstractmethod
    def has_errors(self) -> None:
        pass

    @abstractmethod
    def handle_errors(self) -> None:
        """this methos is also called as fix errors"""
        pass
    
    @abstractmethod
    def check_for_errors(self) -> None:
        """As the current impl needs this, later when we add retry mechanism, we will be moving to has errors and handle errors"""
        pass

    @abstractmethod
    def get_input_elements(self) -> List[WebElement]:
        """ this method will update to Enum / other easy way (in future) instead of webList """
        pass

    @abstractmethod
    def is_upload_field(self, element: WebElement) -> bool:
        pass
    
    


class BaseJobPortal(ABC):

    def __init__(self, driver):
        self.driver = driver

    @property
    @abstractmethod
    def jobs_page(self) -> BaseJobsPage:
        pass

    @property
    @abstractmethod
    def job_page(self) -> BaseJobPage:
        pass

    @property
    @abstractmethod
    def authenticator(self) -> AIHawkAuthenticator:
        pass

    @property
    @abstractmethod
    def application_page(self) -> BaseApplicationPage:
        pass


def get_job_portal(portal_name, driver, parameters):
    from src.job_portals.linkedIn.linkedin import LinkedIn

    if portal_name == LINKEDIN:
        return LinkedIn(driver, parameters)
    else:
        raise ValueError(f"Unknown job portal: {portal_name}")


def get_authenticator(driver, platform):
    from src.job_portals.linkedIn.authenticator import LinkedInAuthenticator

    if platform == LINKEDIN:
        return LinkedInAuthenticator(driver)
    else:
        raise NotImplementedError(f"Platform {platform} not implemented yet.")
