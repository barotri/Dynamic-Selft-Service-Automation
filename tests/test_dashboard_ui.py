import pytest
from playwright.sync_api import sync_playwright
from pages.dashboard_page import DashboardPage

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        debug_logs = getattr(item, 'debug_logs', [])
        if debug_logs:
            report.longrepr.addsection("Debug logs", "\n".join(debug_logs))

def log_debug(msg):
    """Helper function to log debug messages only when test fails"""
    try:
        item = pytest.test_item  # Get current test item
        item.debug_logs = getattr(item, 'debug_logs', [])
        item.debug_logs.append(msg)
    except:
        pass  # Ignore if not in test context

# =====================
# AREA: MAIN INFO/UI HEADER
# =====================
def test_main_title_and_info(login_session):
    page, d = login_session
    assert d.info("main_title").is_visible(), "Main title should be visible"
    assert "Dynamic Self Service Admin Tool" in d.info("main_title").inner_text()
    assert d.info("welcome").is_visible(), "Welcome info should be visible"
    assert d.info("last_logon").is_visible(), "Last logon info should be visible"
    assert d.info("description").is_visible(), "Description should be visible"
    assert d.info("legal_notice").is_visible(), "Legal notice should be visible"

def test_welcome_message_content(login_session):
    page, d = login_session
    welcome_text = d.info("welcome").inner_text()
    assert "Welcome" in welcome_text and "Administrator" in welcome_text, "Welcome message should greet Administrator"

def test_last_logon_format(login_session):
    page, d = login_session
    last_logon = d.info("last_logon").inner_text()
    assert "Last logon:" in last_logon, "Last logon info should be present"
    # Có thể kiểm tra định dạng ngày giờ nếu cần

def test_legal_notice_present(login_session):
    page, d = login_session
    # Cách 1: sibling sau tiêu đề
    legal_sibling = d.info("legal_notice").evaluate("el => el.parentElement.nextElementSibling ? el.parentElement.nextElementSibling.innerText : ''")
    log_debug(f"Legal notice sibling text: {legal_sibling!r}")
    # Cách 2: toàn bộ table cha
    legal_table = d.info("legal_notice").evaluate("el => el.closest('table') ? el.closest('table').innerText : ''")
    log_debug(f"Legal notice table text: {legal_table!r}")
    # Cách 3: toàn bộ innerHTML vùng legal_notice
    legal_html = d.info("legal_notice").evaluate("el => el.innerHTML")
    log_debug(f"Legal notice innerHTML: {legal_html!r}")
    # Ưu tiên kiểm tra sibling, nếu không có thì kiểm tra table
    legal = legal_sibling if legal_sibling.strip() else legal_table
    assert "Avaya" in legal or "All Rights Reserved" in legal, "Legal notice should mention Avaya or rights reserved"

def test_main_title_tag_is_span(login_session):
    page, d = login_session
    tag = d.info("main_title").evaluate("el => el.tagName")
    assert tag == "SPAN", "Main title should be a <span> tag"

def test_main_title_font_size(login_session):
    page, d = login_session
    size = d.info("main_title").evaluate("el => getComputedStyle(el).fontSize")
    assert size.endswith("px") and int(size.replace("px", "")) >= 16, "Main title font size should be at least 16px"

def test_main_title_font_weight(login_session):
    page, d = login_session
    weight = d.info("main_title").evaluate("el => getComputedStyle(el).fontWeight")
    assert int(weight) >= 600, "Main title should be bold or semi-bold"

def test_description_not_empty(login_session):
    page, d = login_session
    desc = d.info("description").inner_text().strip()
    assert desc != "", "Description should not be empty"

def test_legal_notice_link_present(login_session):
    page, d = login_session
    # Tìm tất cả link <a> trong ancestor table của legal_notice
    links = d.info("legal_notice").locator("xpath=ancestor::table//a")
    link_count = links.count()
    log_debug(f"Legal notice link count: {link_count}")
    for i in range(link_count):
        log_debug(f"Legal notice link {i}: {links.nth(i).get_attribute('href')}")
    assert link_count > 0, "Legal notice should contain at least one link"

def test_main_title_alignment(login_session):
    page, d = login_session
    align = d.info("main_title").evaluate("el => getComputedStyle(el).textAlign")
    log_debug(f"Main title text-align: {align!r}")
    assert align in ("center", "left", "start"), "Main title should be left, center, or start aligned"

def test_welcome_message_case(login_session):
    page, d = login_session
    text = d.info("welcome").inner_text()
    assert text[0].isupper(), "Welcome message should start with uppercase letter"

# =====================
# AREA: MENU/MENU BUTTONS
# =====================
def test_all_menu_items_visible(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        assert d.menu(name).is_visible(), f"Menu '{name}' should be visible"

def test_logoff_button_clickable(login_session):
    page, d = login_session
    logoff = d.menu("logoff")
    assert logoff.is_visible(), "Logoff button should be visible"
    logoff.click()
    # Có thể kiểm tra chuyển về trang login hoặc popup xác nhận
    # assert d.page.locator('#c_nameFieldId').is_visible(), "Should return to login page after logoff"

def test_menu_navigation(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        menu = d.menu(name)
        assert menu.is_visible(), f"Menu '{name}' should be visible"
        menu.click()
        d.page.wait_for_timeout(500)

def test_menu_text_not_empty(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        text = d.menu(name).inner_text().strip()
        assert text != "", f"Menu '{name}' should have non-empty text"

def test_menu_tabindex_unique(login_session):
    page, d = login_session
    tabindexes = [d.menu(name).get_attribute("tabindex") for name in d.all_menu_names]
    log_debug(f"Menu tabindexes: {tabindexes}")
    assert len(set(tabindexes)) == len(tabindexes), "Each menu should have unique tabindex"

def test_menu_icon_present_if_any(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        icon_count = d.menu(name).locator("img").count()
        assert icon_count >= 0, f"Menu '{name}' should have 0 or more icons"

def test_menu_is_focusable(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        el = d.menu(name)
        el.focus()
        assert el.evaluate("el => document.activeElement === el"), f"Menu '{name}' should be focusable"

def test_menu_is_not_disabled(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        el = d.menu(name)
        assert not el.get_attribute("disabled"), f"Menu '{name}' should not be disabled"

def test_menu_aria_label_if_any(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        aria = d.menu(name).get_attribute("aria-label")
        # Không bắt buộc, chỉ kiểm tra nếu có thì không rỗng
        if aria is not None:
            assert aria.strip() != "", f"Menu '{name}' aria-label should not be empty if present"

def test_menu_keyboard_navigation_order(login_session):
    page, d = login_session
    tabindexes = [int(d.menu(name).get_attribute("tabindex") or 0) for name in d.all_menu_names]
    assert tabindexes == sorted(tabindexes), "Menu tabindex should be in order"

# =====================
# AREA: ACCESSIBILITY
# =====================
def test_menu_items_have_tabindex(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        el = d.menu(name)
        assert el.get_attribute("tabindex") is not None, f"Menu '{name}' should be focusable by keyboard (tabindex)"

def test_main_title_has_contrast(login_session):
    page, d = login_session
    color = d.info("main_title").evaluate("el => getComputedStyle(el).color")
    bg = d.info("main_title").evaluate("el => getComputedStyle(el).backgroundColor")
    assert color != bg, "Main title text color and background should have contrast"

def test_menu_items_accessible_by_keyboard(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        el = d.menu(name)
        el.focus()
        assert el.evaluate("el => document.activeElement === el"), f"Menu '{name}' should be focusable by keyboard"

def test_no_elements_with_title_empty(login_session):
    page, d = login_session
    empty_titles = d.page.evaluate("Array.from(document.querySelectorAll('[title]')).filter(e => e.title.trim() === '').length")
    assert empty_titles == 0, "No element should have empty title attribute"

def test_all_images_have_alt(login_session):
    page, d = login_session
    imgs = page.query_selector_all('img')
    missing = []
    for img in imgs:
        alt = img.get_attribute('alt')
        role = img.get_attribute('role')
        if not alt and (not role or role != 'presentation'):
            missing.append(img.get_attribute('id'))
    log_debug(f"Images missing alt: {missing}")
    assert not missing, "All images should have alt attribute or role='presentation'"

def test_main_title_has_aria_label(login_session):
    page, d = login_session
    aria = d.info("main_title").get_attribute("aria-label")
    assert aria is None or aria.strip() != "", "Main title aria-label should not be empty if present"

def test_legal_notice_links_accessible(login_session):
    page, d = login_session
    links = d.info("legal_notice").locator("a")
    for i in range(links.count()):
        href = links.nth(i).get_attribute("href")
        assert href and href.startswith("http"), "Legal notice link should be valid URL"

def test_menu_items_have_role_button(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        role = d.menu(name).get_attribute("role")
        assert role in (None, "button"), f"Menu '{name}' should have role='button' or no role"

def test_no_duplicate_ids(login_session):
    page, d = login_session
    ids = d.page.evaluate("Array.from(document.querySelectorAll('[id]')).map(e => e.id)")
    assert len(ids) == len(set(ids)), "No duplicate id attributes in DOM"

def test_no_tabindex_minus_one(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        tabindex = d.menu(name).get_attribute("tabindex")
        assert tabindex != "-1", f"Menu '{name}' should not have tabindex='-1'"

def test_no_hidden_elements(login_session):
    page, d = login_session
    hidden = d.page.evaluate("Array.from(document.querySelectorAll('[hidden]')).length")
    assert hidden == 0, "No element should have the 'hidden' attribute"

# =====================
# AREA: BUTTON RESPONSE/UI FEEDBACK
# =====================
def test_menu_buttons_focus_response(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        btn = d.menu(name)
        btn.focus()
        outline = btn.evaluate("el => getComputedStyle(el).outlineStyle")
        assert outline != "none", f"Menu '{name}' should have visible outline when focused"

def test_menu_buttons_text_and_icon(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        btn = d.menu(name)
        text = btn.inner_text().strip()
        assert text != "", f"Menu '{name}' should have visible text"
        icon_count = btn.locator("img").count()
        assert icon_count >= 0, f"Menu '{name}' should have 0 hoặc nhiều icon (img)"

def test_menu_buttons_enabled_state(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        btn = d.menu(name)
        disabled = btn.get_attribute("disabled")
        aria_disabled = btn.get_attribute("aria-disabled")
        assert not disabled, f"Menu '{name}' should not be disabled"
        assert aria_disabled in (None, "false"), f"Menu '{name}' should not be aria-disabled"

def test_menu_buttons_visible_and_clickable(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        btn = d.menu(name)
        assert btn.is_visible(), f"Menu '{name}' should be visible"
        btn.click()

def test_menu_buttons_cursor_pointer(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        btn = d.menu(name)
        cursor = btn.evaluate("el => getComputedStyle(el).cursor")
        assert cursor == "pointer", f"Menu '{name}' should have cursor:pointer on hover"

def test_menu_buttons_text_align(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        btn = d.menu(name)
        align = btn.evaluate("el => getComputedStyle(el).textAlign")
        log_debug(f"Menu '{name}' text-align: {align}")
        assert align in ("center", "left", "start"), f"Menu '{name}' text should be left, center, or start aligned"

def test_menu_buttons_no_text_overflow(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        btn = d.menu(name)
        overflow = btn.evaluate("el => getComputedStyle(el).textOverflow")
        assert overflow != "ellipsis", f"Menu '{name}' should not have text-overflow: ellipsis by default"

def test_menu_buttons_no_outline_on_mouse(login_session):
    page, d = login_session
    for name in d.all_menu_names:
        btn = d.menu(name)
        btn.hover()
        outline = btn.evaluate("el => getComputedStyle(el).outlineStyle")
        assert outline in ("none", "hidden"), f"Menu '{name}' should not have outline on mouse hover"