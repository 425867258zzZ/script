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
    def get_similarity(str1: str, str2: str) -> float:
        """
        获取两组字符的相似度,使用jacquard算法,用于获取正确选项
        :return: 相似值,∈[0,1],越高说明越相似
        """
        set1 = set(str1)
        set2 = set(str2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union

    @staticmethod
    def get_origin_word(word_get: str, word_dic: dict) -> str:
        """
        获取当前单词的词根
        :param word_dic: 词典
        :param word_get: 当前题中的单词
        :return: 当前单词的词根
        """
        word_res = word_get
        word_len = len(word_get)
        max_similarity = 0
        for word in word_dic.keys():
            max_len = max(len(word), word_len)
            min_len = min(len(word), word_len)
            same = 0
            for i in range(min_len):
                if word_get[i] == word[i]:
                    same += 1
            if (similarity := same / max_len) > max_similarity:
                max_similarity = similarity
                word_res = word
        return word_res

    @staticmethod
    def get_lines() -> int:
        """
        获取当前页面行数
        由于英文字段的行数会导致按钮和英文区域的位置改变,
        所以获取当前行数用于动态创建const文件中的类获取当前页面下的正确区域
        :return:行数
        """
        pyautogui.screenshot(SCREENSHOT_PATH, region=SCREENSHOT_REGION)
        img = cv2.imread(SCREENSHOT_PATH)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        lines = pytesseract.image_to_string(
            gray_img, lang="eng", config="--psm 6"
        ).splitlines()
        result = [line for line in lines if line != ""]
        return len(result)

    @staticmethod
    def is_red(rgb: tuple) -> bool:
        """
        一个题做错时,所点击的选项会变成红色,以此判断是否做错
        判断 RGB 值是否为红色
        """
        r, g, b = rgb
        return b < 10 or (r - g > 150 and r - b > 150)

    @staticmethod
    def is_green(rgb: tuple) -> bool:
        """
        两次都做错,会进入释义界面,在固定位置会有一个绿点,以此判断
        判断给定的 RGB 值是否属于绿色。
        """
        r, g, b = rgb
        return g > r and g > b

    @staticmethod
    def get_options(translations: list, options: list) -> list:
        """
        获取当前单词对应的可能选项
        :param translations:某一单词的字典翻译list
        :param options: 当前选项的list
        :return: 一个存有4个选项代号的list,记录了当前单词最可能的选项list
        """
        print("单词释义为" + str(translations))
        options_dict = {}
        for j in range(4):
            # 每个选项内容对应一个按钮编号1-4
            options_dict[options[j]] = j
        options_result = []
        # 只会有两次点击机会
        for t in range(len(translations)):
            sim = {}
            for option in options:
                sim[option] = Answer.get_similarity(translations[t], option)
            sim = sorted(sim.items(), key=lambda item: item[1], reverse=True)
            if t == 0:
                options_result = [options_dict[option_tuple[0]] for option_tuple in sim]
                options.remove(sim[0][0])
            else:
                options_result[t] = options_dict[sim[0][0]]
        print(options_result)
        return options_result

    def answer_and_check(self, option_region: tuple, options: list) -> None:
        pyautogui.click(option_region[options[0]][0], option_region[options[0]][1])
        time.sleep(0.3)
        screenshot1 = ImageGrab.grab()
        # 获取指定点的 RGB 值
        rgb_color1 = screenshot1.getpixel(
            (option_region[options[0]][0], option_region[options[0]][1])
        )
        if self.is_red(rgb_color1):
            print("第一次答案错误")
            time.sleep(2.0)
            pyautogui.click(option_region[options[1]][0], option_region[options[1]][1])
            time.sleep(1.0)
        screenshot2 = ImageGrab.grab()
        rgb_color2 = screenshot2.getpixel((98, 651))
        if self.is_green(rgb_color2) or self.get_lines() > 7:
            print("第二次答案错误")
            self.wrong_answer += 1
            pyautogui.click(NEXT_BUTTON_REGION[0], NEXT_BUTTON_REGION[1])
            time.sleep(1.0)

    def show_result(self) -> None:
        print("正确率为" + str(100 * (1 - self.wrong_answer / self.question_num)) + "%")

    def get_word_in_listen_part(self, options_get: list, word_dic: dict) -> list:
        """
        获取听力部分每一个选项对应的单词
        :param options_get: 选项内容list
        :param word_dic: 词典
        :return: 4个选项对应的单词list
        """
        res = None
        word_res = []
        for option in options_get:
            max_similarity = 0
            for word in word_dic:
                similarity = max(
                    [
                        self.get_similarity(option, translation)
                        for translation in word_dic[word]
                    ]
                )
                if similarity > max_similarity:
                    max_similarity = similarity
                    res = word
            word_res.append(res)
        return word_res

    def answer_routine(self, word_dic: dict) -> None:
        """
        答题流程
        :param word_dic: 词典
        """
        # 依据当前行数动态获取信息
        line_name = eval("Line" + str(self.get_lines()))
        line = line_name()
        word_in_question_region = line.get_question_region()
        pyautogui.screenshot(WORD_IN_QUESTION_PATH, region=word_in_question_region)
        word_get = Word.get_word_in_question(WORD_IN_QUESTION_PATH)
        print("当前单词识别为" + word_get)

        # 若当前单词不在字典中(过去式,复数等),则尝试获取最相似的单词,即词根
        word_get = self.get_origin_word(word_get, word_dic)
        print("当前词/词根为" + word_get)
        try:
            translations_get = word_dic[word_get]
            # 获取当前单词的选项内容
            translation_in_question_region = line.get_translation_region()
            pyautogui.screenshot(
                TRANSLATION_IN_QUESTION_PATH, region=translation_in_question_region
            )
            # 上 options_get :list['...']
            options_get = Word.get_translation_in_dic(TRANSLATION_IN_QUESTION_PATH)[:4]
            # options_result: list[0,1,2,3]
            options_result = self.get_options(translations_get, options_get)
            self.answer_and_check(line.get_option_zone(), options_result)
        except KeyError:
            print("单词识别错误")
            raise KeyError
        except IndexError:
            print("选项识别错误")
            raise IndexError
        self.question_num += 1
