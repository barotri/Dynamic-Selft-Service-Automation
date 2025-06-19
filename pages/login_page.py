from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.frame = None

    def goto(self, url: str):
        self.page.goto(url)
        # Đợi frame xuất hiện và lấy frame thực sự chứa form login
        self.page.wait_for_selector('frame')
        frame_element = self.page.query_selector('frame')
        self.frame = frame_element.content_frame()

    def login(self, username , password):
        # Đảm bảo frame đã được lấy
        if self.frame is None:
            self.page.wait_for_selector('frame')
            frame_element = self.page.query_selector('frame')
            self.frame = frame_element.content_frame()
        # Chụp screenshot trước khi login
        self.page.screenshot(path="before_login.png")
        # Thao tác với các trường input trong frame (dùng type thay vì fill)
        username_input = self.frame.locator('#c_nameFieldId')
        password_input = self.frame.locator('#c_passwordFieldId')
        login_button = self.frame.locator('#c_loginSubmitButtonId')
        username_input.click()
        username_input.type(username, delay=100)
        password_input.click()
        password_input.type(password, delay=100)
        login_button.click()
        # Chờ chuyển trang hoặc xác nhận login thành công
        self.frame.wait_for_timeout(2000)
        # Chụp screenshot sau khi login
        self.page.screenshot(path="after_login.png")
        # In ra HTML sau khi login
        print("\n========== PAGE HTML AFTER LOGIN ==========")
        print(self.frame.inner_html('body'))
        print("========== END PAGE HTML ==========") 