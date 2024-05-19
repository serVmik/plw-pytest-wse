import os
import re
from urllib.parse import urljoin

from dotenv import load_dotenv
from playwright.sync_api import BrowserContext, APIRequestContext, Page, expect

load_dotenv()

HOST = 'http://localhost:8000/'
LOGIN_PATH = 'users/login/'
TEST_USERNAME = os.getenv('TEST_USERNAME')
TEST_USER_PASSWORD = os.getenv('TEST_USER_PASSWORD')


def test_user_authentication_api(page: Page, context: BrowserContext) -> None:
    """Test user authentication api."""
    # get csrf_token
    page.goto(urljoin(HOST, LOGIN_PATH))
    csrf_token = page.locator('[name="csrfmiddlewaretoken"]').input_value()

    # set post request parameters
    params = {
        'headers': {
            'Referer': HOST,
            'X-CSRFToken': csrf_token,
        },
        'fail_on_status_code': True,
        'ignore_https_errors': True,
    }
    form_data = {
        'username': TEST_USERNAME,
        'password': TEST_USER_PASSWORD,
    }

    # send post request
    api_request_context: APIRequestContext = context.request
    api_request_context.post(page.url, **params, form=form_data)

    page.goto(HOST)
    expect(page.locator('id=user-nav')).to_have_text(
        re.compile(f'.*{TEST_USERNAME}')
    )
