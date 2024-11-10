#!/usr/bin/env python3

"""This is an example of collecting pricing data from e-commerce website using AgentQL."""

# Import the Page class from the AgentQL Playwright extension
# This enables the use of the AgentQL Smart Locator and Data Query API
import agentql
from agentql.ext.playwright.sync_api import Page

# Import the synchronous playwright library
# This library is used to launch the browser and interact with the web page
from playwright.sync_api import sync_playwright

URL = "https://www.instagram.com/"#Url to instagram

# The AgentQL query to locate the search box element
USER_NAME_BOX_QUERY = """
{
    user_name_input
}
"""
USER_PASS_BOX_QUERY = """
{
    password_input
}
"""
#NLP Prompt for login button
LOGIN_PROMPT = "Button to Log in"


def main():
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        # Create a new page in the browser and wrap it get access to the AgentQL's querying API
        page = agentql.wrap(browser.new_page())#Get page

        page.goto(URL)#Direct to instagram
        _input_login_data(page,user_name="71103huz@gmail.com",password="824682465Asd!")#Fill in the login info

def _input_login_data(page: Page, user_name: str, password: str) -> dict:
    """ Input login data

    Args:
        page (Page): The Playwright page object to interact with the browser.
        user_name (str): The username of user
        password (str): The password of user

    Returns:
        None
    """
    # Find DOM element using AgentQL API's query_elements() method
    response = page.query_elements(USER_NAME_BOX_QUERY)#Locate the username inputbox

    # Interact with the element using Playwright API
    # API Doc: https://playwright.dev/python/docs/input#text-input
    response.user_name_input.type(user_name, delay=200)#Type in the username
    response = page.query_elements(USER_PASS_BOX_QUERY)#Locate the password inputbox
    response.password_input.type(password, delay=200)#Type in the password


    return 
        




if __name__ == "__main__":
    main()
