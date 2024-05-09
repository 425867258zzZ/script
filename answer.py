import time

import cv2
import pyautogui
import pytesseract
from PIL import ImageGrab

from const import *
from word import Word


class Answer:
    def __init__(self):
        self.question_num = 0
        self.wrong_answer = 0

    @staticmethod
    def get_similarity(str1, str2):
        """
        获取两组字符的相似度,使用jacquard算法,用于获取词根
        :return: 相似值,∈[0,1],越高说明越相似
        """
        set1 = set(str1)
        set2 = set(str2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union

    @staticmethod
    def get_lines():
        """
        获取当前页面行数
        由于英文字段的行数会导致按钮和英文区域的位置改变,
        所以获取当前行数用于动态创建const文件中的类获取当前页面下的正确区域
        :return:行数
        """
        pyautogui.screenshot(screenshot_path, region=screenshot_region)
        img = cv2.imread(screenshot_path)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        lines = pytesseract.image_to_string(gray_img, lang="eng", config='--psm 6').splitlines()
        print(len(lines))
        return len(lines)

    @staticmethod
    def is_red(rgb):
        """
        一个题做错时,所点击的选项会变成红色,以此判断是否做错
        判断 RGB 值是否为红色
        """
        r, g, b = rgb
        return b < 10 or (r - g > 150 and r - b > 150)

    @staticmethod
    def get_options(translations, options):
        """
        获取当前单词对应的可能选项
        :param translations:某一单词的字典翻译list
        :param options: 当前选项的list
        :return: 一个存有4个选项代号的list,记录了当前单词最可能的选项list
        """
        options_dict = {}
        for j in range(4):
            # 每个选项内容对应一个按钮编号1-4
            options_dict[options[j]] = j
        result = []
        for t in range(len(translations)):
            sim = {}
            for option in options:
                sim[option] = Answer.get_similarity(translations[t], option)
            sim = sorted(sim.items(), key=lambda item: item[1], reverse=True)
            if t == 0:
                result = [options_dict[option_tuple[0]] for option_tuple in sim]
                options.remove(sim[0][0])
            else:
                result[t] = options_dict[sim[0][0]]
        print(result)
        return result

    def answer_and_check(self, option_region, options):
        pyautogui.click(option_region[options[0]][0], option_region[options[0]][1])
        time.sleep(0.2)
        screenshot = ImageGrab.grab()
        # 获取指定点的 RGB 值
        rgb_color1 = screenshot.getpixel((option_region[options[0]][0], option_region[options[0]][1]))
        if self.is_red(rgb_color1):
            print("第一次答案错误")
            time.sleep(2.0)
            pyautogui.click(option_region[options[1]][0], option_region[options[1]][1])
            time.sleep(0.5)
        # 若两次答案都是错的,会出现一个释义界面,必然有大于7行文字,以此判断是否两次都做错了
        if self.get_lines() > 7:
            print("第二次答案错误")
            self.wrong_answer += 1
            time.sleep(0.5)
            pyautogui.click(NEXT_BUTTON_REGION[0], NEXT_BUTTON_REGION[1])

    def routine(self, word_dic):
        # 依据当前行数动态获取信息
        line_name = eval("Line" + str(self.get_lines()))
        line = line_name()
        word_in_question_region = line.get_question_region()
        pyautogui.screenshot(word_in_question_path, region=word_in_question_region)
        word_get = Word.get_word_in_question(word_in_question_path)

        # 若当前单词不在字典中(过去式,复数等),则尝试获取最相似的单词,即词根
        max_similarity = 0
        if word_get not in word_dic:
            for word_in_dic in list(word_dic.keys()):
                if n := self.get_similarity(word_in_dic, word_get) > max_similarity:
                    word_get = word_in_dic
                    max_similarity = n
        print("当前词/词根为" + word_get)

        # 获取当前单词的选项内容
        print(word_get in word_dic)
        translations_get = word_dic[word_get]
        translation_in_question_region = line.get_translation_region()
        pyautogui.screenshot(translation_in_question_path, region=translation_in_question_region)
        options_get = Word.get_translation_in_dic(translation_in_question_path)[:4]
        try:
            options_result = self.get_options(translations_get, options_get)
            self.answer_and_check(line.get_option_zone(), options_result)
        except IndexError:
            print("选项识别错误")
            print(translations_get)
            raise IndexError
        self.question_num += 1
        time.sleep(1.0)

    def show_result(self):
        print("正确率为" + str(1 - self.wrong_answer / self.question_num))
