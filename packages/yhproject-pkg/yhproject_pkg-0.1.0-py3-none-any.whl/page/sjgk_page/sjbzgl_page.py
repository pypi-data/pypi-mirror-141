# 从关键字文件导入基类
from pynput.keyboard import Controller
import pyautogui

from yhproject_pkg.framework.key_word.keyword_web import WebKeys


class SjbzglPage(WebKeys):
    def button_addtheme(self):
        self.locator("xpath", "//*[@id='app']/section/div/div/div/div[1]/div/div/div[1]/button").click()
        self.wait(2)

    def input_themename(self, word_keys):
        self.locator("xpath", "/html/body/div[3]/div/div[2]/div/form/div[1]/div/div[1]/input").send_keys(word_keys)
        self.wait(1)

    def input_themetype(self):
        self.locator("xpath", '/html/body/div[3]/div/div[2]/div/form/div[2]/div/div/div/input').click()
        self.down_keys()
        self.enter_keys()
        self.wait(2)

    def button_themecomfirm(self):
        self.locator("xpath", "/html/body/div[3]/div/div[3]/span/span/button[1]").click()
        self.wait(1)

    def input_treesearch(self, search_key):
        self.locator("xpath", "//*[@id='pane-tree1']/div[1]/input").clear()
        self.wait(1)
        self.locator("xpath", "//*[@id='pane-tree1']/div[1]/input").send_keys(search_key)
        self.wait(2)

    def icon_addClass(self):
        pyautogui.click(690, 620)
        self.wait(1)
        pyautogui.click(710, 690)
        self.wait(2)

    def input_classname(self, word_keys):
        self.locator("xpath", "/html/body/div[3]/div/div[2]/div/form/div[1]/div/div[1]/input").send_keys(word_keys)
        self.wait(2)
        self.locator("xpath", "/html/body/div[3]/div/div[3]/span/span/button[1]").click()
        self.wait(2)

    def icon_addsmclass(self):
        pyautogui.click(693, 672)
        self.wait(1)
        pyautogui.click(711, 741)
        self.wait(2)

    def icon_classrename(self):
        pyautogui.click(735, 720)
        self.wait(1)
        pyautogui.click(750, 780)
        self.wait(2)

    def icon_classremove(self):
        pyautogui.click(735, 628)
        self.wait(1)
        pyautogui.click(745, 745)
        self.wait(2)
        self.enter_keys()
        self.wait(3)

    def button_addstandard(self):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[1]/div/div[1]/button[1]").click()
        self.wait(3)

    def input_standardcode(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[2]/div[1]/div/div/div[1]/input").send_keys(word_keys)

    def input_standardChname(self, word_keys):
        el = self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[2]/div[2]/div/div/div[1]/input")
        el.clear()
        el.send_keys(word_keys)

    def input_standardthemeId(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[3]/div[1]/div/div/span/div/div/input").send_keys(word_keys)
        self.down_keys()
        self.enter_keys()

    def input_standardsuperId(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[3]/div[2]/div/div/span/div/div/input").send_keys(word_keys)
        self.down_keys()
        self.enter_keys()

    def input_standardsonId(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[4]/div[1]/div/div/span/div/div/input").send_keys(word_keys)
        self.down_keys()
        self.enter_keys()

    def input_standardversDate(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[4]/div[2]/div/div/div/input").click()
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[4]/div[2]/div/div/div/input").send_keys(word_keys)
        self.wait(3)

    def input_standardDefin(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[6]/div[1]/div/div/div[1]/input").send_keys(word_keys)

    def input_standardRule(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[6]/div[2]/div/div/div/input").send_keys(word_keys)
        self.enter_keys()

    def input_standardcodingRule(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[7]/div[1]/div/div/div/input").send_keys(word_keys)

    def input_standarddemoRule(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[7]/div[2]/div/div/div/input").send_keys(word_keys)

    def input_standardClssName(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[8]/div[1]/div/div/div/input").send_keys(word_keys)

    def input_standardClssLevel(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[8]/div[2]/div/div/div/input").send_keys(word_keys)

    def input_standardEnglish(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[11]/div/div/div/div/input").send_keys(word_keys)

    def input_standardCategory(self):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[12]/div[1]/div/div/div/div/input").click()
        self.down_keys()
        self.enter_keys()

    def input_standardFormat(self):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[12]/div[2]/div/div/div/div[1]/input").click()
        self.down_keys()
        self.enter_keys()

    def input_standardDepart(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[15]/div/div/div/div[1]/input").send_keys(word_keys)

    def input_standardapprovalDepart(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[2]/form/div[16]/div[1]/div/div/div[1]/input").send_keys(word_keys)

    def button_standardcomfirm(self):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div[2]/div/div[3]/span/span/button[1]").click()
        self.wait(3)

    def button_view(self):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div/div/div[1]/div/div[4]/div[2]/table/tbody/tr/td[10]/div/button[1]").click()
        self.wait(2)

    def button_edit(self):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div/div/div[1]/div/div[4]/div[2]/table/tbody/tr/td[10]/div/button[2]").click()
        self.wait(2)

    def button_switch(self):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div/div/div[1]/div/div[4]/div[2]/table/tbody/tr/td[10]/div/button[4]").click()
        self.wait(3)

    def button_switch1(self):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[2]/div/div/div[1]/div/div[4]/div[2]/table/tbody/tr/td[10]/div/button[3]").click()
        self.wait(3)

    def input_search(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[1]/div/div[2]/div/input").send_keys(word_keys)
        self.wait(1)
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[1]/div/div[2]/button[1]").click()
        self.wait(2)

    def button_reset(self):
        self.locator("xpath", "//*[@id='pane-tab1']/div/div[1]/div/div[2]/button[2]").click()
        self.wait(1)

    def button_bzgl(self):
        self.locator("xpath", "//*[@id='tab-tab1']").click()

    def button_bgjlgl(self):
        self.locator("xpath", "//*[@id='tab-tab2']").click()
        self.wait(2)

    def input_bgsearch(self, search_key):
        self.locator("xpath", "//*[@id='pane-tab2']/div/div[1]/div/div[2]/div/input").send_keys(search_key)
        self.wait(1)
        self.locator("xpath", "//*[@id='pane-tab2']/div/div[1]/div/div[2]/button[1]").click()
        self.wait(2)

    def input_bgreset(self):
        self.locator("xpath", "//*[@id='pane-tab2']/div/div[1]/div/div[2]/button[2]").click()

    def button_bgsy(self):
        self.locator("xpath", "//*[@id='pane-tab2']/div/div[2]/div/div/div[1]/div/div[4]/div[2]/table/tbody/tr/td[10]/div/button[1]").click()
        self.wait(2)

    def button_bgedit(self):
        self.locator("xpath", "//*[@id='pane-tab2']/div/div[2]/div/div/div[1]/div/div[4]/div[2]/table/tbody/tr[1]/td[10]/div/button[2]").click()
        self.wait(2)

    def button_remove(self):
        self.locator("xpath", "//*[@id='pane-tab2']/div/div[2]/div/div/div[1]/div/div[4]/div[2]/table/tbody/tr[1]/td[10]/div/button[3]").click()

    def input_bgreason(self, word_key):
        self.locator("xpath", "//*[@id='pane-tab2']/div/div[2]/div[2]/div/div[2]/form/div[2]/div[2]/div/div/div/input").send_keys(word_key)

    def button_bgcomfirm(self):
        self.locator("xpath", "//*[@id='pane-tab2']/div/div[2]/div[2]/div/div[3]/span/span/button[1]").click()
        self.wait(3)

    def button_addbgstandard(self):
        self.locator("xpath", "//*[@id='pane-tab2']/div/div[1]/div/div[1]/button").click()
        self.wait(2)

    def input_bgversion(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab2']/div/div[2]/div[2]/div/div[2]/form/div[1]/div[1]/div/div/div/input").send_keys(word_keys)

    def input_bgcodestandard(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab2']/div/div[2]/div[2]/div/div[2]/form/div[1]/div[2]/div/div/div/div/input").send_keys(word_keys)
        self.wait(2)
        self.down_keys()
        self.enter_keys()

    def input_bgremark(self, word_keys):
        self.locator("xpath", "//*[@id='pane-tab2']/div/div[2]/div[2]/div/div[2]/form/div[3]/div[1]/div/div/div/input").send_keys(word_keys)
















