#!/usr/bin/env python3
"""
Description: This file uses selenium to access the ITA training program google form, and fill in values within the form.
             It uses a class to control either to run it in headless mode, or any other mode available.
"""
from __future__ import annotations

from enum import Enum
from typing import Callable, List, Optional, Tuple, Union


class ITATrainingAutomatorDriverEnum(Enum):
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
                   spec: ITATrainingAutomatorDriverEnum) -> WebDriver:
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
        if spec == ITATrainingAutomatorDriverEnum.CHROME:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.options import Options
            options = Options()
            options.headless = headless
            return webdriver.Chrome(service=service(ChromeDriverManager().install()), options=options)
        elif spec == ITATrainingAutomatorDriverEnum.CHROMIUM:
            from selenium.webdriver.chrome.options import Options
            options = Options()
            options.headless = headless
            from webdriver_manager.chrome import ChromeDriverManager
            from webdriver_manager.core.utils import ChromeType
            return webdriver.Chrome(service=service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                                    options=options)
        elif spec == ITATrainingAutomatorDriverEnum.BRAVE:
            from selenium.webdriver.chrome.options import Options
            options = Options()
            options.headless = headless
            from webdriver_manager.chrome import ChromeDriverManager
            from webdriver_manager.core.utils import ChromeType
            return webdriver.Chrome(service=service(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()),
                                    options=options)
        elif spec == ITATrainingAutomatorDriverEnum.EDGE:
            from selenium.webdriver.edge.options import Options
            options = Options()
            options.headless = headless
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            return webdriver.Edge(service=service(EdgeChromiumDriverManager().install()), options=options)
        elif spec == ITATrainingAutomatorDriverEnum.INTERNET_EXPLORER:
            from selenium.webdriver.ie.options import Options
            options = Options()
            options.headless = headless
            from webdriver_manager.microsoft import IEDriverManager
            return webdriver.Ie(service=service(IEDriverManager().install()), options=options)
        elif spec == ITATrainingAutomatorDriverEnum.OPERA:
            from webdriver_manager.opera import OperaDriverManager
            from selenium.webdriver.chrome import service
            webdriver_service = service.Service(OperaDriverManager().install())
            webdriver_service.start()
            options = webdriver.ChromeOptions()
            options.add_experimental_option('w3c', True)
            options.headless = headless
            return webdriver.Remote(webdriver_service.service_url, options=options)

    def try_drivers() -> WebDriver:
        """
        Tries loading in all drivers realistically possible to be used with selenium. With the help of webdriver_manager
        library, we can try each driver in a loop, and we are guaranteed at least one because it downloads the drivers
        from a source if the driver is not found.

        :return: The instantiated webdriver found on the client's computer
        """
        specs: List[Tuple[ITATrainingAutomatorDriverEnum, Callable[[str], Union[
            ChromeService, ChromiumService, EdgeService, FirefoxService, IEService]]]] = [
            (ITATrainingAutomatorDriverEnum.BRAVE, ChromeService),
            (ITATrainingAutomatorDriverEnum.CHROME, ChromeService),
            (ITATrainingAutomatorDriverEnum.CHROMIUM, ChromiumService),
            (ITATrainingAutomatorDriverEnum.EDGE, EdgeService),
            (ITATrainingAutomatorDriverEnum.FIREFOX, FirefoxService),
            (ITATrainingAutomatorDriverEnum.INTERNET_EXPLORER, IEService),
            (ITATrainingAutomatorDriverEnum.OPERA, None)]
        for each_spec in specs:
            try:
                selected_driver = each_spec[1]
                driver_enum = each_spec[0]
                return get_driver(selected_driver, driver_enum)
            except Exception as exception:
                print(str(exception))
                pass

    return try_drivers()


class ITATrainingAutomator:
    """
        ITA Training automator. Accesses the url specified below. Has options for all actions allowed, can even
        override the internal url if need be.
        https://docs.google.com/a/udel.edu/forms/d/e/1FAIpQLSeCnzQ7Kax9u6_uZQDbHiJrPP76iMUg3eJvZMmV3f2xZU8vsQ/viewform
    """

    def __init__(self,
                 url: str = 'https://docs.google.com/a/udel.edu/forms/d/e'
                            '/1FAIpQLSeCnzQ7Kax9u6_uZQDbHiJrPP76iMUg3eJvZMmV3f2xZU8vsQ/viewform',
                 headless: bool = False, timeout: float = 60_000.0) -> None:
        self.url = url  # The url to use when instantiating the webdriver
        self.headless = headless  # Whether to start the webdriver in headless mode
        from selenium.webdriver.remote.webdriver import WebDriver
        self.driver: WebDriver = find_webdriver()
        self.driver.set_page_load_timeout(timeout)


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

    print(find_webdriver())
