# def test_main_heading_present(login_session):
#     page, dashboard = login_session
#     # Kiểm tra có thẻ h1 sau khi login
#     heading = dashboard.get_main_heading()
#     assert heading.is_visible(), "Main heading <h1> should be visible after login"
#     assert heading.inner_text().strip() != "", "Main heading <h1> should not be empty"

# def test_form_fields_have_labels(login_session):
#     page, dashboard = login_session
#     # Kiểm tra mỗi trường form có label tương ứng
#     fields = dashboard.get_form_fields_with_labels()
#     assert fields, "No form fields with labels found"
#     for label, input_elem in fields:
#         label_text = label.inner_text().strip()
#         assert label_text, "Label should not be empty"
#         assert input_elem.count() > 0, f"Input for label '{label_text}' not found"

def test_admin_tool_text_displayed(login_session):
    page, dashboard = login_session
    # Lấy frame chứa nội dung sau login
    frame = page.query_selector('frame').content_frame()
    assert frame.inner_text('body').find('Dynamic Self Service Admin Tool') != -1, \
        "Text 'Dynamic Self Service Admin Tool' should be displayed after login" 