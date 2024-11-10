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

# The AgentQL query to locate the username box element
USER_NAME_BOX_QUERY = """
{
    user_name_input
}
"""
#The AgentQL query to locate the password box element
USER_PASS_BOX_QUERY = """
{
    password_input
}
"""
#The AgentQL query to locate the pop up window element
POP_UP_QUERY = """
{
    popup_form {
        close_btn
    }
}
"""
CHAT_BOX_QUERY = """
{
    message_input
}
"""
#NLP Prompt for login button
LOGIN_PROMPT = "Button to Log in"
#NLP Prompt for goto message section
MESSAGE_SECTION_PROMPT = "Button to send message"
#NLP Prompt for start new message button
MESSAGE_BUTTON_PROMPT = "Button with aria-label 'New Message'"
#NLP Prompt for user's checkbox
USER_PROMPT = "ContactSearchResultCheckbox "
#NLP Prompt for start chat button
CHAT_PROMPT = "Chat Button "
#NLP Prompt for send message button
SEND_PROMPT = "Send Button "
def main():
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        # Create a new page in the browser and wrap it get access to the AgentQL's querying API
        context = browser.new_context(locale="en-US")#Force the chromium browser language to be english https://playwright.dev/docs/api/class-browser
        new_page = context.new_page()
        page = agentql.wrap(new_page)#Get page

        page.goto(URL)#Direct to instagram
        _input_login_data(page,user_name="yigexiaohao49@gmail.com",password="824682465Asd!")#Fill in the login info
        _login(page)#Click the login button
        _find_message_section(page)#Direct to the message section
        _find_message_button(page)#Click on the new message button to direct to reciption page
        _send_message(page,user_name="jayjay199822",message="Hi")#Locate the reciption and send the message to it

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
def _login(page: Page):
    """Locate and Click the login button on the login page.

    Args:
        page (Page): The Playwright page object to interact with the browser.
    """
    # Find login button element using AgentQL API's get_by_prompt() method
    login_btn = page.get_by_prompt(LOGIN_PROMPT)#This is actually a Playwright Locator

    # Interact with the element using Playwright API
    # API Doc: https://playwright.dev/python/docs/api/class-locator#locator-click
    if login_btn:
        login_btn.click()

    # Wait for 10 seconds to see the browser action
    page.wait_for_timeout(10000)        

def _find_message_section(page: Page):
    """Locate and Click the message button to direct to message section.

    Args:
        page (Page): The Playwright page object to interact with the browser.
    """
    # Find Message button element using AgentQL API's get_by_prompt() method
    Message_section_btn = page.get_by_prompt(MESSAGE_SECTION_PROMPT)
    # Interact with the element using Playwright API
    # API Doc: https://playwright.dev/python/docs/api/class-locator#locator-click
    if Message_section_btn:
        Message_section_btn.click()

    # Wait for 3 seconds to see the browser action
    page.wait_for_timeout(3000)
    # Use query_elements() method to fetch the close popup button from the page
    response = page.query_elements(POP_UP_QUERY)
    # Click the close button to close the popup
    response.popup_form.close_btn.click()
    # Wait for 3 seconds to see the browser action
    page.wait_for_timeout(3000)
def _find_message_button(page: Page):
    '''
    Locate and Click the new message button to direct to reciptions section.
    Note: AgentQL can only locate the svg on the new message button due to Instagram's encryption,
      by using the bounding_box and playwright api we can bypass it.
    # Interact with the element using Playwright API
    # API Doc: https://playwright.dev/python/docs/input#text-input
    response.new_message_btn.click()
    '''
    new_message_svg = page.get_by_prompt(MESSAGE_BUTTON_PROMPT)#locate the svg of new message button
    new_message_svg.click(force=True)
    #box = new_message_svg.bounding_box()#locate the cords of bounding box of that svg, which is the button itself
    #page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)#click on that cords
def _send_message(page: Page, user_name: str, message: str):
    """Locate and send the message to given reciption in the new message pop-up window.

    Args:
        page (Page): The Playwright page object to interact with the browser.
        user_name (str): The reciption's username
        message (str): The message to be sent to reciption
    """
    #locate the search box
    response = page.query_elements(USER_NAME_BOX_QUERY)
    #type in the username
    response.user_name_input.type(user_name, delay=200)
    # Wait for 3 seconds to see the browser action
    page.wait_for_timeout(3000)
    user_but = page.get_by_prompt(USER_PROMPT)#Locate the user checkbox
    user_but.click()#Click on the check box to add user to reciption
    chat_but = page.get_by_prompt(CHAT_PROMPT)#Locate the start chat button
    chat_but.click()#Click on the start chat button
    response = page.query_elements(CHAT_BOX_QUERY)#Locate the message box
    response.message_input.type(message, delay=200)#Type in the message
    send_but = page.get_by_prompt(SEND_PROMPT)#Locate the send button
    send_but.click()#Click on the send message button
    # Wait for 3 seconds to see the browser action
    page.wait_for_timeout(3000)
if __name__ == "__main__":
    main()
