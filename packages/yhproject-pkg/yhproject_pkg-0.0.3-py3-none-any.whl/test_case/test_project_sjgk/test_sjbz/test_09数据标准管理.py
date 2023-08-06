import pytest
import pyautogui
from yhproject_pkg.framework.data_driver.yaml_driver import load_yaml
from yhproject_pkg.framework.page.login_page.login_page import LoginPage
from yhproject_pkg.framework.page.login_page.menu_page import MenuPage
from yhproject_pkg.framework.page.sjgk_page.sjbzgl_page import SjbzglPage
import allure
import logging

logger = logging.getLogger(__name__)


@allure.feature('数据标准管理')
@allure.title('登录')
@pytest.mark.parametrize('data', load_yaml('../../../data/login/login1.yaml'))
def test_login_zlgzgl(browser, data):
    page = LoginPage(browser)
    page.driver.maximize_window()
    page.open(data["url"])
    page.input_user(data["user"])
    page.input_password(data["password"])
    page.button_remember()
    page.button_login()
    # 登录跳转
    page.switch_window(-1)
    page.assert_att("赢和数据")
    logger.info('------------进入数据标准管理模块-------------')


@allure.feature('数据标准管理')
@pytest.mark.parametrize('data', load_yaml('../../../data/login/menu.yaml'))
@allure.title('打开菜单_质量规则管理')
def test_menu_zlgzgl(browser, data):
    page = MenuPage(browser)
    page.table_manage()
    page.menu_icon()
    page.menu_sjgk()
    page.sjgk_sjbz_sjbzgl()
    # 切换iframe
    page.sjgk_sjbzgl_iframe()
    page.assert_att("基础数据标准")
    logger.info('01进入菜单成功')


@allure.feature('数据标准管理')
@pytest.mark.parametrize('data', load_yaml('../../../data/sjgk/sjbzgl.yaml'))
@allure.title('新增_标准主题')
def test_add_theme(browser, data):
    page = SjbzglPage(browser)
    page.button_addtheme()
    page.input_themename(data['theme'])
    page.input_themetype()
    page.button_themecomfirm()
    page.assert_att("操作成功")
    logger.info('02新增标准主题成功')


@allure.feature('数据标准管理')
@pytest.mark.parametrize('data', load_yaml('../../../data/sjgk/sjbzgl.yaml'))
@allure.title('搜索_标准分类')
def test_search_theme(browser, data):
    page = SjbzglPage(browser)
    page.input_treesearch(data['theme'])
    page.icon_addClass()
    page.input_classname(data['theme']+'class')
    page.input_treesearch(data['theme']+'class')
    page.icon_addsmclass()
    page.input_classname(data['theme']+'smclass')
    page.input_treesearch(data['theme']+'smclass')
    page.assert_att(data['theme']+'smclass')
    logger.info('03搜索标准主题成功')


@allure.feature('数据标准管理')
@pytest.mark.parametrize('data', load_yaml('../../../data/sjgk/sjbzgl.yaml'))
@allure.title('编辑_标准分类')
def test_edit_theme(browser, data):
    page = SjbzglPage(browser)
    page.icon_classrename()
    page.input_classname('ess')
    page.input_treesearch(data['theme']+'smclass'+'ess')
    page.assert_att(data['theme']+'smclass'+'ess')
    logger.info('04编辑标准主题成功')


@allure.feature('数据标准管理')
@pytest.mark.parametrize('data', load_yaml('../../../data/sjgk/sjbzgl.yaml'))
@allure.title('新增_标准管理')
def test_addstandard(browser, data):
    page = SjbzglPage(browser)
    page.button_addstandard()
    page.input_standardcode(data['code'])
    page.input_standardChname(data['nameChinese1'])
    page.input_standardthemeId(data['theme'])
    page.input_standardsuperId(data['theme']+'class')
    page.input_standardsonId(data['theme']+'smclassess')
    page.input_standardversDate('2022-02-01')
    page.input_standardDefin(data['defin'])
    page.input_standardRule(data['rule'])
    page.input_standardcodingRule(data['coderule'])
    page.input_standarddemoRule(data['demorule'])
    page.input_standardClssName(data['classname'])
    page.input_standardClssLevel(data['classlevel'])
    page.down_mouse()
    page.input_standardEnglish(data['nameEnglish'])
    page.input_standardCategory()
    page.input_standardFormat()
    page.input_standardDepart(data['depart'])
    page.input_standardapprovalDepart(data['depart'])
    page.button_standardcomfirm()
    page.assert_att('操作成功')
    logger.info('05新增标准成功')


@allure.feature('数据标准管理')
@pytest.mark.parametrize('data', load_yaml('../../../data/sjgk/sjbzgl.yaml'))
@allure.title('查看_标准管理')
def test_viewstandard(browser, data):
    page = SjbzglPage(browser)
    page.button_reset()
    page.input_search(data['code'])
    page.button_view()
    page.assert_att("查看标准")
    page.button_standardcomfirm()
    logger.info('06查看标准成功')


@allure.feature('数据标准管理')
@pytest.mark.parametrize('data', load_yaml('../../../data/sjgk/sjbzgl.yaml'))
@allure.title('启停_标准管理')
def test_switchtandard(browser, data):
    page = SjbzglPage(browser)
    page.button_switch()
    page.assert_att("启用")
    page.button_switch1()
    page.assert_att("禁用")
    logger.info('07启停标准成功')


@allure.feature('数据标准管理')
@pytest.mark.parametrize('data', load_yaml('../../../data/sjgk/sjbzgl.yaml'))
@allure.title('编辑_标准管理')
def test_editstandard(browser, data):
    page = SjbzglPage(browser)
    page.button_switch()
    page.button_edit()
    page.assert_att("编辑标准")
    page.input_standardChname(data['nameChinese2'])
    page.button_standardcomfirm()
    page.assert_att("操作成功")
    logger.info('08编辑标准成功')


@allure.feature('数据标准管理')
@pytest.mark.parametrize('data', load_yaml('../../../data/sjgk/sjbzgl.yaml'))
@allure.title('查找_标准管理')
def test_searchstandard(browser, data):
    page = SjbzglPage(browser)
    page.button_reset()
    page.input_search('error')
    page.assert_att("暂无数据")
    page.button_reset()
    page.input_search(data['nameChinese2'])
    page.assert_att(data['nameChinese2'])
    logger.info('09搜索标准成功')


@allure.feature('数据标准管理')
@pytest.mark.parametrize('data', load_yaml('../../../data/sjgk/sjbzgl.yaml'))
@allure.title('查看_变更记录管理')
def test_searchbgstandard(browser, data):
    page = SjbzglPage(browser)
    page.button_bgjlgl()
    page.input_bgsearch('error')
    page.assert_att("暂无数据")
    page.input_bgreset()
    page.input_bgsearch(data['code'])
    page.assert_att(data["nameChinese2"])
    logger.info('10查看变更标准成功')


@allure.feature('数据标准管理')
@pytest.mark.parametrize('data', load_yaml('../../../data/sjgk/sjbzgl.yaml'))
@allure.title('溯源_变更记录管理')
def test_sybgstandard(browser, data):
    page = SjbzglPage(browser)
    page.button_bgsy()
    page.assert_att(data['nameChinese1'])
    page.button_bgcomfirm()
    logger.info('11溯源变更标准成功')


@allure.feature('数据标准管理')
@pytest.mark.parametrize('data', load_yaml('../../../data/sjgk/sjbzgl.yaml'))
@allure.title('编辑_变更记录管理')
def test_editbgstandard(browser, data):
    page = SjbzglPage(browser)
    page.button_bgedit()
    page.input_bgreason(data['bgreason'])
    page.button_bgcomfirm()
    page.assert_att(data['bgreason'])
    logger.info('12变更标准成功')


@allure.feature('数据标准管理')
@allure.title('删除_变更记录管理')
def test_removebgstandard(browser):
    page = SjbzglPage(browser)
    page.button_remove()
    page.enter_keys()
    page.assert_att("操作成功")
    logger.info('13删除标准成功')


@allure.feature('数据标准管理')
@pytest.mark.parametrize('data', load_yaml('../../../data/sjgk/sjbzgl.yaml'))
@allure.title('新增_变更记录管理')
def test_addbgstandard(browser, data):
    page = SjbzglPage(browser)
    page.button_addbgstandard()
    page.input_bgversion(data['version'])
    page.input_bgcodestandard(data['code'])
    page.input_bgremark(data['remark'])
    page.button_bgcomfirm()
    page.assert_att(data['code'])
    page.button_remove()
    page.enter_keys()
    page.assert_att("操作成功")
    logger.info('14新增标准成功')


@allure.feature('数据标准管理')
@pytest.mark.parametrize('data', load_yaml('../../../data/sjgk/sjbzgl.yaml'))
@allure.title('删除_标准分类')
def test_remove_theme(browser, data):
    page = SjbzglPage(browser)
    page.input_treesearch(data['theme'])
    page.icon_classremove()
    page.button_bzgl()
    page.button_reset()
    page.input_search(data['code'])
    page.assert_att("暂无数据")
    logger.info('15删除标准成功')


@allure.feature('数据标准管理')
@allure.title('退出登录')
def test_zlgzgl_logout(browser):
    page = LoginPage(browser)
    page.reback_iframe()
    page.button_user()
    pyautogui.click(2428, 391)
    page.wait(2)
    page.assert_att("赢和数据")
    logger.info('.....退出登录.....')
















