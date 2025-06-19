import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.fixture(scope="function")
def login_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=200)
        page = browser.new_page()
        # Clear all cookies trước khi login
        page.context.clear_cookies()
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        # Truy cập trang login và đăng nhập
        login_page.goto("http://10.255.245.202")
        login_page.login("admin","A123456a")
        yield page, dashboard_page
        browser.close()

def pytest_configure(config):
    if not hasattr(config.option, "htmlpath") or not config.option.htmlpath:
        config.option.htmlpath = "report.html"
        config.option.self_contained_html = True

