#!/usr/bin/env python3
"""
Description: This file uses selenium to access the ITA training program google form, and fill in values within the form.
             It uses a class to control either to run it in headless mode, or any other mode available.
"""
from __future__ import annotations

from enum import Enum
from typing import Callable, List, Optional, Tuple, Union


class SeleniumBotWebdriverType(Enum):
    """
    Controls what type of driver we are setting out webdriver to
    """
    BRAVE = 0
    CHROME = 1,
    CHROMIUM = 2,
    EDGE = 3,
    FIREFOX = 4,
    INTERNET_EXPLORER = 5,
    OPERA = 6


def find_webdriver(headless: bool):
    """
    Finds the webdriver, which will be used for automation purposes

    :param headless: Whether to run the browser in headless mode or not
    :return: The found browser instantiated into a selenium webdriver class instance
    """
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chromium.service import ChromiumService
    from selenium.webdriver.edge.service import Service as EdgeService
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from selenium.webdriver.ie.service import Service as IEService

    def get_driver(service: Callable[[str], Optional[Union[
        ChromeService, ChromiumService, EdgeService, FirefoxService, IEService]]],
                   spec: SeleniumBotWebdriverType) -> WebDriver:
        """
        Gets the  driver specified by the specification `spec` passed in. Fetches the driver using the helpful
        library `webdriver_manager`, which handles downloading the driver to be used, dependent on the specification
        supplied.

        :param service: The service instance lined up with the specification passed in
        :param spec: The
        specification, which controls which driver is instantiated (which loader is imported from webdriver_manager
        library)
        :return: The instantiated webdriver instance
        """
        from selenium import webdriver
        if spec == SeleniumBotWebdriverType.CHROME:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.options import Options
            options = Options()
            if headless:
                options.add_argument('--headless')
            return webdriver.Chrome(service=service(ChromeDriverManager().install()), options=options)
        elif spec == SeleniumBotWebdriverType.CHROMIUM:
            from selenium.webdriver.chrome.options import Options
            options = Options()
            if headless:
                options.add_argument('--headless')
            from webdriver_manager.chrome import ChromeDriverManager
            from webdriver_manager.core.utils import ChromeType
            return webdriver.Chrome(service=service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                                    options=options)
        elif spec == SeleniumBotWebdriverType.BRAVE:
            from selenium.webdriver.chrome.options import Options
            options = Options()
            if headless:
                options.add_argument('--headless')
            from webdriver_manager.chrome import ChromeDriverManager
            from webdriver_manager.core.utils import ChromeType
            return webdriver.Chrome(service=service(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()),
                                    options=options)
        elif spec == SeleniumBotWebdriverType.EDGE:
            from selenium.webdriver.edge.options import Options
            options = Options()
            if headless:
                options.add_argument('--headless')
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            return webdriver.Edge(service=service(EdgeChromiumDriverManager().install()), options=options)
        elif spec == SeleniumBotWebdriverType.INTERNET_EXPLORER:
            from selenium.webdriver.ie.options import Options
            options = Options()
            if headless:
                options.add_argument('--headless')
            from webdriver_manager.microsoft import IEDriverManager
            return webdriver.Ie(service=service(IEDriverManager().install()), options=options)
        elif spec == SeleniumBotWebdriverType.OPERA:
            from webdriver_manager.opera import OperaDriverManager
            from selenium.webdriver.chrome import service
            webdriver_service = service.Service(OperaDriverManager().install())
            webdriver_service.start()
            options = webdriver.ChromeOptions()
            options.add_experimental_option('w3c', True)
            if headless:
                options.add_argument('--headless')
            return webdriver.Remote(webdriver_service.service_url, options=options)

    def try_drivers() -> WebDriver:
        """
        Tries loading in all drivers realistically possible to be used with selenium. With the help of webdriver_manager
        library, we can try each driver in a loop, and we are guaranteed at least one because it downloads the drivers
        from a source if the driver is not found.

        :return: The instantiated webdriver found on the client's computer
        """
        specs: List[Tuple[SeleniumBotWebdriverType, Callable[[str], Union[
            ChromeService, ChromiumService, EdgeService, FirefoxService, IEService]]]] = [
            (SeleniumBotWebdriverType.BRAVE, ChromeService),
            (SeleniumBotWebdriverType.CHROME, ChromeService),
            (SeleniumBotWebdriverType.CHROMIUM, ChromiumService),
            (SeleniumBotWebdriverType.EDGE, EdgeService),
            (SeleniumBotWebdriverType.FIREFOX, FirefoxService),
            (SeleniumBotWebdriverType.INTERNET_EXPLORER, IEService),
            (SeleniumBotWebdriverType.OPERA, None)]
        for each_spec in specs:
            try:
                selected_driver = each_spec[1]
                driver_enum = each_spec[0]
                return get_driver(selected_driver, driver_enum)
            except Exception as exception:
                print(str(exception))
                pass

    return try_drivers()


class SeleniumBot:
    """
        ITA Training automator. Accesses the url specified below. Has options for all actions allowed, can even
        override the internal url if need be.
        https://docs.google.com/a/udel.edu/forms/d/e/1FAIpQLSeCnzQ7Kax9u6_uZQDbHiJrPP76iMUg3eJvZMmV3f2xZU8vsQ/viewform
    """

    def __init__(self,
                 headless: bool = False, timeout: float = 60_000.0) -> None:
        """
        Initializes an instance of the ITATraining Automator class

        :param headless: Whether to instantiate the automator in headless mode
        :param timeout: The page load timeout, waits x amount of seconds for page to load, or automatically closes
        """
        from selenium.webdriver.remote.webdriver import WebDriver
        self.driver: WebDriver = find_webdriver(headless)
        self.driver.set_page_load_timeout(timeout)
        from urllib.parse import urlsplit, SplitResult
        self.base_url: SplitResult = urlsplit(self.driver.current_url)

    def navigate(self, url: str) -> bool:
        """
        Navigates to the URL specified in the argument to the method

        :param url: The url to navigate to
        :return: Whether it was navigated to successfully
        """
        try:
            self.driver.get(url)
            from urllib.parse import urlsplit
            self.base_url = urlsplit(self.driver.current_url)
            return True
        except Exception as exception:
            print(str(exception))
            return False


    def log_in(self, email_or_phone: str, password: str) -> None:
        """
        Logs the user into google services using their email or phone, and their password

        :param email_or_phone: The email or phone number used to sign in
        :param password: The password used to sign in
        :return: Whether the login was successful or not
        """
        email_or_


if __name__ == '__main__':
    try:
        from pip import main as pipmain
    except ImportError:
        from pip._internal import main as pipmain
    try:
        import selenium
    except ImportError:
        pipmain(['install', 'selenium'])
    try:
        import webdriver_manager
    except ImportError:
        pipmain(['install', 'webdriver-manager'])

    selenium_bot = SeleniumBot()
    selenium_bot.navigate(
        'https://docs.google.com/forms/d/e/1FAIpQLSeCnzQ7Kax9u6_uZQDbHiJrPP76iMUg3eJvZMmV3f2xZU8vsQ/viewform')
    if selenium_bot.base_url.netloc == 'accounts.google.com':
        ## Logging in
