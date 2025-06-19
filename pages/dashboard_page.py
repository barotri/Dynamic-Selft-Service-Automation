from playwright.sync_api import Page

class DashboardPage:
    # Locators as class attributes
    MENU_LOCATORS = {
        "home": "#c_AvayaMainScreenHome",
        "help": "#c_AvayaMainScreenHelp",
        "logoff": "#c_AvayaMainScreenLogoff",
        "call_flow_management": "#c_AvayaDefaultFormContainerMenuItemCallFlowManagement",
        "call_flows": "#c_AvayaDefaultFormContainerMenuItemCallFlow",
        "prompts": "#c_AvayaDefaultFormContainerMenuItemPrompt",
        "call_center_management": "#c_AvayaDefaultFormContainerMenuItemCallCenterManagement",
        "scheduling_table": "#c_AvayaDefaultFormContainerMenuItemSchedule",
        "schedule_groups": "#c_AvayaDefaultFormContainerMenuItemHoliday",
        "services": "#c_AvayaDefaultFormContainerMenuItemService",
        "products": "#c_AvayaDefaultFormContainerMenuItemProduct",
        "sites": "#c_AvayaDefaultFormContainerMenuItemSite",
        "ani_groups": "#c_AvayaDefaultFormContainerMenuItemTestAni",
        "icr_skills": "#c_AvayaDefaultFormContainerMenuItemIcrSkill",
        "user_management": "#c_AvayaDefaultFormContainerMenuItemUserManagement",
        "audit_log": "#c_AvayaDefaultFormContainerMenuItemAudit",
        "users": "#c_AvayaDefaultFormContainerMenuItemUser",
        "access_levels": "#c_AvayaDefaultFormContainerMenuItemRole",
        "system_management": "#c_AvayaDefaultFormContainerMenuItemSystemManagement",
        "flow_engine_servers": "#c_AvayaDefaultFormContainerMenuItemFlowEngineServer",
        "audio_cache": "#c_AvayaDefaultFormContainerMenuItemAudioCache",
        "call_flow_cache": "#c_AvayaDefaultFormContainerMenuItemCallFlowCache",
    }
    INFO_LOCATORS = {
        "welcome": "#c_27",
        "last_logon": "#c_28",
        "main_title": "#c_47",
        "description": "#c_48",
        "legal_notice": "#c_50",
    }

    def __init__(self, page: Page):
        self.page = page

    # Menu accessors
    def menu(self, name):
        return self.page.locator(self.MENU_LOCATORS[name])

    # Info accessors
    def info(self, name):
        return self.page.locator(self.INFO_LOCATORS[name])

    # Convenience for all menu names
    @property
    def all_menu_names(self):
        return list(self.MENU_LOCATORS.keys())

    @property
    def all_info_names(self):
        return list(self.INFO_LOCATORS.keys())

    def get_main_heading(self):
        # Tìm thẻ heading chính (h1)
        return self.page.locator("h1")

    def get_form_fields_with_labels(self):
        # Trả về danh sách tuple (label, input) cho các trường form
        labels = self.page.locator("label")
        fields = []
        for i in range(labels.count()):
            label = labels.nth(i)
            # Lấy thuộc tính 'for' của label để tìm input tương ứng
            for_attr = label.get_attribute("for")
            if for_attr:
                input_elem = self.page.locator(f'#{for_attr}')
                fields.append((label, input_elem))
        return fields 