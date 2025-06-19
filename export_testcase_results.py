import xml.etree.ElementTree as ET
from openpyxl import Workbook

# Mapping area theo prefix tên testcase
AREA_MAP = {
    'test_main_': 'Main Info/UI Header',
    'test_welcome_': 'Main Info/UI Header',
    'test_last_': 'Main Info/UI Header',
    'test_legal_': 'Main Info/UI Header',
    'test_description_': 'Main Info/UI Header',
    'test_all_menu_': 'Menu/Menu Buttons',
    'test_logoff_': 'Menu/Menu Buttons',
    'test_menu_': 'Menu/Menu Buttons',
    'test_no_': 'Accessibility',
    'test_all_images_': 'Accessibility',
    'test_aria_': 'Accessibility',
    'test_keyboard_': 'Accessibility',
    'test_buttons_': 'Button Response/UI Feedback',
}

def get_area(testname):
    for prefix, area in AREA_MAP.items():
        if testname.startswith(prefix):
            return area
    return 'Other'

def parse_pytest_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    results = []
    for testcase in root.iter('testcase'):
        name = testcase.attrib.get('name')
        classname = testcase.attrib.get('classname')
        area = get_area(name)
        status = 'PASSED'
        message = ''
        if testcase.find('failure') is not None:
            status = 'FAILED'
            message = testcase.find('failure').attrib.get('message', '')
        elif testcase.find('error') is not None:
            status = 'ERROR'
            message = testcase.find('error').attrib.get('message', '')
        elif testcase.find('skipped') is not None:
            status = 'SKIPPED'
            message = testcase.find('skipped').attrib.get('message', '')
        results.append({
            'area': area,
            'name': name,
            'status': status,
            'message': message,
        })
    return results

def export_to_excel(results, out_path):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Testcase Results'
    ws.append(['Area', 'Testcase Name', 'Status', 'Message'])
    for r in results:
        ws.append([r['area'], r['name'], r['status'], r['message']])
    wb.save(out_path)

if __name__ == '__main__':
    results = parse_pytest_xml('dashboard_test_result.xml')
    export_to_excel(results, 'testcase_results.xlsx')
    print('Exported testcase_results.xlsx') 