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
#NLP Prompt for login check
LOGIN_CHECK_PROMPT = "Message saying Sorry, your password was incorrect"
#NLP Prompt for backend check
BACK_END_CHECK_PROMPT = "Red colored Message saying Please wait a few minutes"
#NLP Prompt for login button
LOGIN_PROMPT = "Button to Log in"
#NLP Prompt for two-step verify box
TWO_STEP_PROMPT = "Textbox for two-step verify code input "
#NLP Prompt for two-step verify button
TWO_STEP_BUTTON_PROMPT = "Button to continue "
#NLP Prompt for two-step reload
TWO_STEP_RELOAD_BUTTON_PROMPT = "Button to reload "
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


class QL:
    def __init__(self):
        self.playwright = sync_playwright().start()#Start the playwirght api
        self.browser = self.playwright.chromium.launch(headless=False)#Launch the chromium browser
        self.context = self.browser.new_context(locale="en-US")#Set the default language
        self.page = agentql.wrap(self.context.new_page())#Get the page for agentQL
    def login(self, user_name: str, password: str):
        """ Attempt to login with given username and password

        Args:
            user_name (str): The username of user
            password (str): The password of user

        Returns:
            login_attempt (bool): True if login successfully False if not
            error_code (str): code showing why the login was not sucessful 
        """
        self.page.goto("https://www.instagram.com/")
        self._input_login_data(user_name, password)
        login_attempt, error_code = self._login()
        if login_attempt:

            return login_attempt, "Login successful"
        else:

            return login_attempt, error_code

    def send_message(self, recipient: str, message: str):
        """ Attempt to send message with given recipient and message

        Args:
            recipient (str): The username of recipient
            message (str): The message need to be sent to the recipient

        Returns:
            login_attempt (bool): True if login successfully False if not
            error_code (str): code showing why the login was not sucessful 
        """
        if self.page:
            self._find_message_section()
            self._find_message_button()
            found = self._send_message(recipient,message)
            if found:
                return "Message sent successfully"
            else:
                return "recipient does not exist"
        else:
            return "Error: Not logged in or session has expired"
    def close(self):
        self.browser.close()
        self.playwright.stop()
    def _check_two_step(self,code: int):
        """Check if there is a two-step verfication that user need to solve

        Args:
            page (Page): The Playwright page object to interact with the browser.
        """
        self.page.wait_for_timeout(5000)#Sleep 5 seconds
        two_step_reload_butt = self.page.get_by_prompt(TWO_STEP_RELOAD_BUTTON_PROMPT)#Check if the page crashed
        if two_step_reload_butt:#if crashed, reload the page
            two_step_reload_butt.click()
            self.page.wait_for_timeout(1500)
        two_step_box = self.page.get_by_prompt(TWO_STEP_PROMPT)#Locate the code input box

        # Interact with the element using Playwright API
        # API Doc: https://playwright.dev/python/docs/api/class-locator#locator-click
        if two_step_box:
            two_step_box.type(code)#input the user given code
        two_step_button = self.page.get_by_prompt(TWO_STEP_BUTTON_PROMPT)#Locate the next button
        if two_step_button:#Click the next button
            two_step_button.click()
    def _input_login_data(self, user_name: str, password: str) -> dict:
        """ Input login data

        Args:
            page (Page): The Playwright page object to interact with the browser.
            user_name (str): The username of user
            password (str): The password of user

        Returns:
            None
        """
        # Find DOM element using AgentQL API's query_elements() method
        response = self.page.query_elements(USER_NAME_BOX_QUERY)#Locate the username inputbox

        # Interact with the element using Playwright API
        # API Doc: https://playwright.dev/python/docs/input#text-input
        response.user_name_input.type(user_name, delay=200)#Type in the username
        response = self.page.query_elements(USER_PASS_BOX_QUERY)#Locate the password inputbox
        response.password_input.type(password, delay=200)#Type in the password


        return 
    
    def _login(self):
        """Locate and Click the login button on the login page.

        Args:
            page (Page): The Playwright page object to interact with the browser.
        """
        # Find login button element using AgentQL API's get_by_prompt() method
        login_btn = self.page.get_by_prompt(LOGIN_PROMPT)#This is actually a Playwright Locator

        # Interact with the element using Playwright API
        # API Doc: https://playwright.dev/python/docs/api/class-locator#locator-click
        if login_btn:
            login_btn.click()

        # Wait for 3 seconds to see the browser action
        self.page.wait_for_timeout(5000)
        url = self.page.url
        print(url)
        if "auth_platform" in url:
            return False,"Error Code 99: Two-step Verify code needed"
        else:

            wrong_password = self.page.get_by_prompt(LOGIN_CHECK_PROMPT)#Check if instagram says wrong password
            if wrong_password:
                return False,"Error Code 100: Please double check your password"
            bakcend_error = self.page.get_by_prompt(BACK_END_CHECK_PROMPT)#Check if instagram says please wait few minuts
            if bakcend_error:
                
                return False,"Error Code 101: Your Instagram Account may be banned Or there was too many login attempt"
        return True,"Login Sucessfully"
        
    def _find_message_section(self):
        """Locate and Click the message button to direct to message section.

        Args:
            page (Page): The Playwright page object to interact with the browser.
        """
        # Find Message button element using AgentQL API's get_by_prompt() method
        Message_section_btn = self.page.get_by_prompt(MESSAGE_SECTION_PROMPT)
        # Interact with the element using Playwright API
        # API Doc: https://playwright.dev/python/docs/api/class-locator#locator-click
        if Message_section_btn:
            Message_section_btn.click()

        # Wait for 3 seconds to see the browser action
        self.page.wait_for_timeout(3000)
        # Use query_elements() method to fetch the close popup button from the page
        response = self.page.query_elements(POP_UP_QUERY)
        # Click the close button to close the popup
        response.popup_form.close_btn.click()
        # Wait for 3 seconds to see the browser action
        self.page.wait_for_timeout(3000)
    def _find_message_button(self):
        '''
        Locate and Click the new message button to direct to reciptions section.
        Note: AgentQL can only locate the svg on the new message button due to Instagram's encryption,
        by using the bounding_box and playwright api we can bypass it.
        # Interact with the element using Playwright API
        # API Doc: https://playwright.dev/python/docs/input#text-input
        response.new_message_btn.click()
        '''
        new_message_svg = self.page.get_by_prompt(MESSAGE_BUTTON_PROMPT)#locate the svg of new message button
        new_message_svg.click(force=True)
        #box = new_message_svg.bounding_box()#locate the cords of bounding box of that svg, which is the button itself
        #page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)#click on that cords
    def _send_message(self, user_name: str, message: str):
        """Locate and send the message to given reciption in the new message pop-up window.

        Args:
            page (Page): The Playwright page object to interact with the browser.
            user_name (str): The reciption's username
            message (str): The message to be sent to reciption
        """
        #locate the search box
        response = self.page.query_elements(USER_NAME_BOX_QUERY)
        #type in the username
        response.user_name_input.type(user_name, delay=200)
        # Wait for 3 seconds to see the browser action
        self.page.wait_for_timeout(3000)
        user_but = self.page.get_by_prompt(USER_PROMPT)#Locate the user checkbox
        if user_but:
            user_but.click()#Click on the check box to add user to reciption
            chat_but = self.page.get_by_prompt(CHAT_PROMPT)#Locate the start chat button
            chat_but.click()#Click on the start chat button
            response = self.page.query_elements(CHAT_BOX_QUERY)#Locate the message box
            response.message_input.type(message, delay=200)#Type in the message
            send_but = self.page.get_by_prompt(SEND_PROMPT)#Locate the send button
            send_but.click()#Click on the send message button
            # Wait for 3 seconds to see the browser action
            self.page.wait_for_timeout(3000)
            return True
        else:
            return False


