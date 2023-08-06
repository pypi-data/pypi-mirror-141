# 从关键字文件导入基类
import pyautogui
from pynput.keyboard import Controller
from yhproject_pkg.framework.key_word.keyword_web import WebKeys


class LbjkPage(WebKeys):
    def input_search(self, search_key):
        self.locator("xpath", "//*[@id='app']/section/div/div[1]/div/div/div/div[1]/div/input").send_keys(search_key)
        self.wait(3)

    def local_table(self):
        pyautogui.click(520, 645)
        self.wait(2)

