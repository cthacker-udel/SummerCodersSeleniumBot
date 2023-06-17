#!/usr/bin/env python3
"""
Description: This file uses selenium to access the ITA training program google form, and fill in values within the form.
             It uses a class to control either to run it in headless mode, or any other mode available.
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Callable, List, Optional, Tuple, Union


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


class GoogleFormBotFieldType(Enum):
    """
    Represents the different types of inputs present within the Google form
    """
    DATE = 0,
    MULTI_CHECKBOX = 1,
    MULTI_SELECT = 2,
    SINGLE_CHECKBOX = 3,
    TEXT = 4,


def find_webdriver(headless: bool) -> Any:
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


def press_enter_key(element: Any) -> None:
    """
    Presses the enter key in the element passed in

    :param element: The element to press the enter key in
    :return: None, mutates the element passed in
    """
    from selenium.webdriver.remote.webdriver import WebElement
    from selenium.webdriver.common.keys import Keys
    converted_element: WebElement = element
    converted_element.send_keys(Keys.ENTER)


def simulate_typing(element: Any, content: str | int, random_interval_start=.15, random_interval_stop=1) -> None:
    """
    Simulates typing into the element passed into the function. Types in a random interval, letter by letter,
    in the interval **[random_interval_start, random_interval_stop)**

    :param element: The element to simulate typing into
    :param content: The content to type into the element
    :param random_interval_start: The start of the random interval
    :param random_interval_stop: The end of the random interval
    :return: None, mutates the element internally
    """
    from selenium.webdriver.remote.webdriver import WebElement
    from time import sleep
    from random import uniform

    converted_element: WebElement = element

    converted_content = content if isinstance(content, str) else str(content)
    for each_letter in converted_content:
        converted_element.send_keys(each_letter)
        sleep(uniform(random_interval_start, random_interval_stop))


class SeleniumBot:
    """
        Selenium bot, capable of logging into google accounts as well as logging into University of Delaware accounts.
    """

    def __init__(self,
                 headless: bool = False, timeout: float = 60000.0) -> None:
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

    def enter_email_google_account(self, email_or_phone: str) -> Any:
        """
        Finds the email input for the Google form, used when accessing any Google resource

        :param email_or_phone: The email to enter into the email or phone input
        :return: The found email input
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.remote.webdriver import WebElement
        home_page_inputs = self.driver.find_elements(by=By.TAG_NAME, value='input')

        def is_email_input(web_element: WebElement):
            """
            Determines if the web element passed in is the input where the user enters in their email or phone number

            :param web_element: The web element to verify
            :return: Whether the web element is the email or phone input
            """
            return web_element.get_attribute('type') == 'email'

        email_or_phone_login: List[WebElement] = list(filter(is_email_input, home_page_inputs))
        if len(email_or_phone_login) == 0:
            raise Exception("Failed to find email or phone login element for google form")

        email_element = email_or_phone_login[-1]
        simulate_typing(email_element, email_or_phone)
        press_enter_key(email_element)

    def enter_password_google_account(self, password: str) -> None:
        """
        Enters the password into the password text box

        :param password: The password to enter
        :return: None, enters/interacts with the browser internally
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.remote.webdriver import WebElement

        password_form_inputs = self.driver.find_elements(by=By.TAG_NAME, value='input')

        def is_password_input(web_element: WebElement):
            """
            Determines if the web element passed in is the input where the user enters in their password

            :param web_element: The web element to verify
            :return: Whether the web element is the password input
            """
            return web_element.get_attribute('type') == 'password'

        password_inputs: List[WebElement] = list(filter(is_password_input, password_form_inputs))
        if len(password_inputs) == 0:
            raise Exception("Failed to find password element for google form")

        password_element = password_inputs[-1]
        simulate_typing(password_element, password)
        press_enter_key(password_element)

    def log_in_google_account(self, email_or_phone: str, password: str) -> None:
        """
        Logs the user into their Google account

        :param email_or_phone: The email or phone number to log into the account
        :param password: The password to log into the account
        :return: None, logs in internally
        """
        self.enter_email_google_account(email_or_phone)
        self.enter_password_google_account(password)

    def enter_username_udel_account(self, username: str) -> None:
        """
        Enters the username into the username input in the university of delaware login page

        :param username: The username to enter into the input element
        :return: None, mutates the browser internally
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.remote.webdriver import WebElement
        input_elements = self.driver.find_elements(by=By.TAG_NAME, value='input')

        if len(input_elements) == 0:
            raise Exception("Unable to find any input elements in the udel credentials page, please try again")

        found_username_inputs: List[WebElement] = list(
            filter(lambda x: x.get_attribute('id') == 'username', input_elements))

        if len(found_username_inputs) == 0:
            raise Exception("Unable to find username input")

        found_username_input: WebElement = found_username_inputs[-1]
        simulate_typing(found_username_input, username)

    def enter_password_udel_account(self, password: str) -> None:
        """
        Enters the password into the password input in the university of delaware login page

        :param password: The password to enter into the password input element
        :return: None, mutates the browser internally
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.remote.webdriver import WebElement
        input_elements = self.driver.find_elements(by=By.TAG_NAME, value='input')

        if len(input_elements) == 0:
            raise Exception("Unable to find any input elements in the udel credentials page, please try again")

        found_password_inputs: List[WebElement] = list(
            filter(lambda x: x.get_attribute('id') == 'password', input_elements))

        if len(found_password_inputs) == 0:
            raise Exception("Unable to find password input")

        found_password_input: WebElement = found_password_inputs[-1]
        simulate_typing(found_password_input, password)
        press_enter_key(found_password_input)

    def enter_otp_udel_account(self, otp_code: str) -> None:
        """
        Enters the OTP (One-Time-Password) code into the 2FA code input

        :param otp_code: The OTP code to enter into the 2FA code input
        :return: None, mutates the browser internally
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.remote.webdriver import WebElement
        input_elements = self.driver.find_elements(by=By.TAG_NAME, value='input')

        if len(input_elements) == 0:
            raise Exception("Unable to find any input elements in the 2FA page, please try again")

        found_token_inputs: List[WebElement] = list(filter(lambda x: x.get_attribute('id') == 'token', input_elements))

        if len(found_token_inputs) == 0:
            raise Exception("Unable to find token input")

        found_token_input: WebElement = found_token_inputs[-1]
        simulate_typing(found_token_input, otp_code)
        press_enter_key(found_token_input)

    def log_in_udel_account(self, username: str, password: str, otp_code) -> None:
        """
        Logs into an udel (University of Delaware) account if required for form sign in

        :param username: The username to log in with
        :param password: The password to log in with
        :param otp_code: The OTP code to log in with
        :return: None, mutates the browser internally
        """
        self.enter_username_udel_account(username)
        self.enter_password_udel_account(password)
        self.enter_otp_udel_account(otp_code)


def select_random_multiselect_option(mutliselect_element: Any) -> None:
    """
    Selects a random element from the mutliselect options

    :param mutliselect_element: The multiselect element
    :return: None, mutates the dom internally
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.remote.webdriver import WebElement
    from random import choice
    converted_multiselect: WebElement = mutliselect_element
    all_divs: List[WebElement] = converted_multiselect.find_elements(by=By.TAG_NAME, value='div')
    all_options: List[WebElement] = list(
        filter(lambda x: x.get_attribute('role') == 'option' and x.get_attribute('data-value') is not None,
               all_divs))
    if len(all_options) > 0:
        random_option: WebElement = choice(all_options)
        random_option.click()


def generate_random_string(length: int = 20) -> str:
    """
    Generates a random string from the ascii_lowercase constant within the string module

    :param length: The length of the randomized string
    :return: The randomized string
    """
    from random import choices
    from string import ascii_lowercase
    return ''.join(choices(ascii_lowercase, k=length))


class GoogleFormBot(SeleniumBot):
    """
        ITA Training automator. Accesses the url specified below. Has options for all actions allowed, can even
        override the internal url if need be.
        https://docs.google.com/a/udel.edu/forms/d/e/1FAIpQLSeCnzQ7Kax9u6_uZQDbHiJrPP76iMUg3eJvZMmV3f2xZU8vsQ/viewform
    """

    def __init__(self):
        """
        Just calls the super class, class will contain methods relating specifically to the ITA training google form
        """
        super().__init__()

    def get_input_by_label(self, label: str) -> Any:
        """
        Gets an input from the label

        :param label: The label to find the input element by
        :return: The found input element
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.remote.webdriver import WebElement
        all_divs = self.driver.find_elements(by=By.TAG_NAME, value='span')

        found_elements = list(filter(lambda x: x.get_attribute("innerHTML") is not None and x.get_attribute(
            "innerHTML").strip().lower() == label.lower(), all_divs))

        if len(found_elements) > 0:
            found_element: WebElement = found_elements[-1]
            fourth_parent = found_element.find_element('../../../../')
            input_element = fourth_parent.find_element(By.TAG_NAME, value='input')
            return input_element

        return None

    def get_mutliselect_by_label(self, label: str) -> Any:
        """
        Gets an input from the label

        :param label: The label to find the input element by
        :return: The found input element
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.remote.webdriver import WebElement
        all_divs = self.driver.find_elements(by=By.TAG_NAME, value='span')

        found_elements = list(filter(lambda x: x.get_attribute("innerHTML") is not None and x.get_attribute(
            "innerHTML").strip().lower() == label.lower(), all_divs))

        if len(found_elements) > 0:
            found_element: WebElement = found_elements[-1]
            fourth_parent = found_element.find_element('../../../../')
            all_divs_of_parent = fourth_parent.find_elements(By.TAG_NAME, value='div')
            if len(all_divs_of_parent) > 0:
                multiselect_elements = list(filter(lambda x: x.get_attribute('role') == 'listbox', all_divs_of_parent))
                if len(multiselect_elements) > 0:
                    return multiselect_elements[-1]
        return None

    def select_multiselect_option(self, label: str) -> None:
        """
        Selects a mutliselect option at random

        :param label: The label to find the multiselect by
        :return: None, mutates the dom internally
        """
        found_multiselect = self.get_mutliselect_by_label(label)
        select_random_multiselect_option(found_multiselect)

    def enter_text_in_text_input(self, label: str, content: Optional[str] = None) -> None:
        """
        Enters text into the text input in the Google form

        :param label: The label to find the text input by
        :param content: The content to input into the form
        :return: None, mutates the dom internally
        """
        found_input = self.get_input_by_label(label)
        simulate_typing(found_input, generate_random_string() if content is None else content)

    def check_singular_textbox(self, label: str, checked: bool = True) -> None:
        """
        Checks a singular textbox in the Google form

        :param label: The label to access the checkbox from
        :param checked: Whether to check the checkbox
        :return: None, mutates the DOM internally
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.remote.webdriver import WebElement

        all_spans = self.driver.find_elements(By.TAG_NAME, value='span')

        if len(all_spans) > 0:
            found_label_span = list(filter(lambda x: x.get_attribute("innerHTML") is not None and x.get_attribute(
                "innerHTML").strip().lower() == label.lower(), all_spans))
            if len(found_label_span) > 0:
                found_label = found_label_span[-1]
                third_parent: WebElement = found_label.find_element(By.XPATH, value='../../../')
                parent_divs = third_parent.find_elements(By.TAG_NAME, value='div')
                if len(parent_divs) > 0:
                    found_checkboxes = list(filter(lambda x: x.get_attribute("role") == "checkbox", parent_divs))
                    if len(found_checkboxes) > 0:
                        found_checkbox: WebElement = found_checkboxes[-1]
                        if checked:
                            found_checkbox.click()

    def enter_date(self, label: str, month: str, day: str, year: str) -> None:
        """
        Enters a date into the date input with the corresponding label

        :param label: The label used to access the date input
        :param month: The month of the date
        :param day: The day of the date
        :param year: The year of the date
        :return: None, mutates the DOM internally
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.remote.webdriver import WebElement

        all_spans: List[WebElement] = self.driver.find_elements(By.TAG_NAME, value='span')

        if len(all_spans) > 0:
            found_label_spans = list(filter(lambda x: x.get_attribute("innerHTML") is not None and x.get_attribute(
                "innerHTML").strip().lower() == label.lower(), all_spans))
            if len(found_label_spans) > 0:
                found_label_span: WebElement = found_label_spans[-1]
                fourth_parent = found_label_span.find_element(By.XPATH, value='../../../../')
                fourth_parent_inputs = fourth_parent.find_elements(By.TAG_NAME, value='input')
                if len(fourth_parent_inputs) > 0:
                    found_month_inputs = list(filter(lambda x: x.get_attribute("role") is not None and x.get_attribute(
                        "aria-label") is not None and x.get_attribute(
                        "role").strip().lower() == "combobox" and x.get_attribute(
                        "aria-label").strip().lower() == "month", fourth_parent_inputs))
                    found_day_inputs = list(filter(lambda x: x.get_attribute("role") is not None and x.get_attribute(
                        "aria-label") is not None and x.get_attribute(
                        "role").strip().lower() == "combobox" and x.get_attribute(
                        "aria-label").strip().lower() == "day of the month", fourth_parent_inputs))
                    found_year_inputs = list(filter(lambda x: x.get_attribute("role") is not None and x.get_attribute(
                        "aria-label") is not None and x.get_attribute(
                        "role").strip().lower() == "combobox" and x.get_attribute(
                        "aria-label").strip().lower() == "year", fourth_parent_inputs))
                    if len(found_month_inputs) > 0 and len(found_day_inputs) > 0 and len(found_year_inputs) > 0:
                        found_month_input = found_month_inputs[-1]
                        found_day_input = found_day_inputs[-1]
                        found_year_input = found_year_inputs[-1]
                        simulate_typing(found_month_input, month)
                        simulate_typing(found_day_input, day)
                        simulate_typing(found_year_input, year)

    def select_multiple_checkboxes(self, label: str, choose_amount: int = 1, other_text: Optional[str] = None) -> None:
        """
        Selects multiple checkboxes from a multi-checkbox input

        :param label: The label to search for the multi-checkbox input
        :param choose_amount: The number of checkboxes to select
        :param other_text: The text to input if the `Other` category is present within the checkbox
        :return: None, mutates the DOM internally
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.remote.webdriver import WebElement
        from random import choice

        all_spans: List[WebElement] = self.driver.find_elements(By.TAG_NAME, value='span')

        if len(all_spans) > 0:
            found_label_spans = list(filter(lambda x: x.get_attribute("innerHTML") is not None and x.get_attribute(
                "innerHTML").strip().lower() == label.lower(), all_spans))
            if len(found_label_spans) > 0:
                found_label: WebElement = found_label_spans[-1]
                fourth_parent: WebElement = found_label.find_element(By.XPATH, "../../../../")
                fourth_parent_divs = fourth_parent.find_elements(By.TAG_NAME, value='div')
                if len(fourth_parent_divs) > 0:
                    found_list_divs = list(filter(lambda x: x.get_attribute("role") is not None and x.get_attribute(
                        "role").strip().lower() == "list", fourth_parent_divs))
                    if len(found_list_divs) > 0:
                        found_list: WebElement = found_list_divs[-1]
                        found_list_divs = found_list.find_elements(By.TAG_NAME, value='div')
                        if len(found_list_divs) > 0:
                            found_list_options: List[WebElement] = list(filter(
                                lambda x: x.get_attribute("role") is not None and x.get_attribute("role") == "listitem",
                                found_list_divs))
                            for i in range(choose_amount):
                                random_option: WebElement = choice(found_list_options)
                                random_option.click()
                                # If we click on the other option.
                                # It automatically focuses onto the text input to describe the other option
                                focused_element = self.driver.switch_to.active_element
                                if focused_element.tag_name == 'input':
                                    if other_text is None:
                                        from string import ascii_lowercase
                                        simulate_typing(focused_element, generate_random_string())
                                    else:
                                        simulate_typing(focused_element, other_text)


class ITATrainingBot(GoogleFormBot):
    """
    Bot specifically designed for the ITA training bot
    """

    def __init__(self):
        """
        Just calls the super class, which instantiates the bot
        """
        super().__init__()
        # [Type of input, value, label]
        self.fields: List[List[GoogleFormBotFieldType, str | int | bool | List[str] | None, str]] = [
            [GoogleFormBotFieldType.SINGLE_CHECKBOX, True, "email"],
            [GoogleFormBotFieldType.TEXT, "Thacker", "Last Name"],
            [GoogleFormBotFieldType.TEXT, "Cameron", "First Name"],
            [GoogleFormBotFieldType.TEXT, "Z", "Middle Initial"],
            [GoogleFormBotFieldType.TEXT, 312931, "Student ID #"],
            [GoogleFormBotFieldType.MULTI_SELECT, None, "Country of Citizenship"],
            [GoogleFormBotFieldType.MULTI_SELECT, None, "Term for ELI ITA Attendance"],
            [GoogleFormBotFieldType.MULTI_SELECT, None, "ELI ITA Session"],
            [GoogleFormBotFieldType.TEXT, 99, "IBT TOEFL Score (Speaking)"],
            [GoogleFormBotFieldType.TEXT, 99, "IBT TOEFL Score (Total)"],
            [GoogleFormBotFieldType.DATE, [12, 20, 1990], "Begin Date of TA Contract"],
            [GoogleFormBotFieldType.DATE, [12, 20, 1991], "End Date of TA Contract"],
            [GoogleFormBotFieldType.TEXT, 20000, "Amount of Stipend"],
            [GoogleFormBotFieldType.TEXT, 100, "Percentage of Tuition"],
            [GoogleFormBotFieldType.MULTI_CHECKBOX, None, "Name of Student's Program"],
            [GoogleFormBotFieldType.TEXT, "Thacker Department", "Department Contact Name"],
            [GoogleFormBotFieldType.TEXT, "20 Thacker Lane", "Department Contact Campus Address"],
            [GoogleFormBotFieldType.TEXT, "123-401-9958", "Department Contact Person's Telephone Number"]
        ]

        ## lookup table of labels, to indexes within the fields, if the user wants to mutate any of the values
        self.lookup: dict[str, int] = {}

        for ind, element in enumerate(self.fields):
            self.lookup[element[-1]] = ind

    def change_field(self, field_label: str, value: str | int | bool | List[str]) -> ITATrainingBot:
        """
        Mutates the field value within the training bot

        :param field_label: The label to mutate
        :param value: The value to update the field with
        :return: The mutated class instance
        """
        if field_label in self.lookup:
            self.fields[self.lookup[field_label]] = value
        return self

    def process_fields(self) -> None:
        """
        Processes all the internal `fields` array, which contains commands the bot processes

        :return: None, processes the fields array internally
        """
        for each_field in self.fields:
            [field_type, value, label] = each_field
            if field_type == GoogleFormBotFieldType.TEXT:
                self.enter_text_in_text_input(label, value)
            elif field_type == GoogleFormBotFieldType.MULTI_CHECKBOX:
                self.select_multiple_checkboxes(label)
            elif field_type == GoogleFormBotFieldType.MULTI_SELECT:
                self.select_multiselect_option(label)
            elif field_type == GoogleFormBotFieldType.SINGLE_CHECKBOX:
                self.check_singular_textbox(label, value)
            elif field_type == GoogleFormBotFieldType.DATE:
                [month, day, year] = value
                self.enter_date(label, month, day, year)


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
    try:
        import pyotp
    except ImportError:
        pipmain(['install', 'pyotp'])

    ita_bot = GoogleFormBot()
    ita_bot.navigate(
        'https://docs.google.com/forms/d/e/1FAIpQLSeCnzQ7Kax9u6_uZQDbHiJrPP76iMUg3eJvZMmV3f2xZU8vsQ/viewform')
    import re

    google_email = ''
    while len(google_email) == 0 or not re.match(r'[^@]+@[^@]+\.[^@]+', google_email):
        google_email = input("Enter google email address >\t")
    ita_bot.enter_email_google_account(google_email)
    if ita_bot.base_url.netloc == 'accounts.google.com':
        #########################
        ## GOOGLE AUTHENTICATION
        #########################
        google_password = ''
        while len(google_password) == 0:
            google_password = input("Enter google account password >\t")
        ita_bot.log_in_google_account(google_email, google_password)
    elif ita_bot.base_url.netloc == 'cas.nss.udel.edu':
        ########################
        ## UDEL AUTHENTICATION
        ########################
        udel_username = ''
        while len(udel_username) == 0:
            udel_username = input("Enter University of Delaware username >\t")
        udel_password = ''
        while len(udel_password) == 0:
            udel_password = input("Enter University of Delaware password >\t")
        otp_secret = ''
        while len(otp_secret) == 0:
            otp_secret = input("Enter your OTP secret >\t")
        ita_bot.log_in_udel_account(udel_username, udel_password, otp_secret)
