import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

from const import *


class Word:
    """
    用于获取词典和读取英文字段/单词,翻译/选项文字
    """

    def __init__(self):
        self.dic = {}

    @staticmethod
    def get_word_in_dic(word_image_path: str) -> str:
        img = cv2.imread(word_image_path)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        word = pytesseract.image_to_string(gray_img, lang="eng", config=ENGLISH_CONFIG)
        return word.replace("\n", "")

    @staticmethod
    def get_translation_in_dic(translation_image_path: str) -> list:
        """
        获取中文字段,同时可用于读取前30个词的翻译,和题干中的选项中文
        :param translation_image_path:
        :return:
        """
        image = Image.open(translation_image_path)
        image = image.convert('L')  # 转换为灰度图
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)  # 提高对比度
        image = image.filter(ImageFilter.MedianFilter())  # 应用中值滤波去噪
        image = image.point(lambda x: 0 if x < 140 else 255)
        result = pytesseract.image_to_string(
            image, lang="chi_sim", config=r"--oem 3 --psm 6"
        ).splitlines()
        # 去除可能的空行,同时去除可能出现的多识别的非中文字符
        result = [
            line.replace(" ", "")
            for line in result
            if (line != "" and (line.isalnum() == False))
        ]
        print(result)
        return result

    def creat_dic(self, word_image_path: str, translation_image_path: str) -> None:
        word = self.get_word_in_dic(word_image_path)
        translation = self.get_translation_in_dic(translation_image_path)
        self.dic[word] = translation

    def get_dic(self) -> dict:
        return self.dic

    @staticmethod
    def get_word_in_question(question_image_path: str) -> str:
        """
        获取题干中标记为绿色的单词,先使用掩码将非绿色部分标记为白色,之后读取转化后的图片获取单词
        :param question_image_path: 题干的图片路径
        :return:
        """
        image = Image.open(question_image_path)
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # 定义绿色的 HSV 范围
        lower_green = np.array([60, 60, 60])
        upper_green = np.array([90, 255, 255])
        anpy=1
        # 将图片转换为 HSV 格式，并根据绿色范围创建掩码,把绿色部分标记为黑色,其余部分为白色
        hsv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_green, upper_green)
        result = cv2.bitwise_and(image_cv, image_cv, mask=mask)
        result[mask == 0] = [255, 255, 255]

        text = pytesseract.image_to_string(result, lang="eng", config=ENGLISH_CONFIG)
        return text.strip().lower().replace(" ", "")

    def routine(self):
        """
        获取词典,读取英文字段/单词,翻译/选项文字,并点击继续按钮
        """
        pyautogui.screenshot(WORD_IMAGE_PATH, region=WORD_REGION)
        pyautogui.screenshot(TRANSLATION_IMAGE_PATH, region=TRANSLATION_REGION)

        self.creat_dic(WORD_IMAGE_PATH, TRANSLATION_IMAGE_PATH)
        print(self.get_dic())
        pyautogui.click(GOON_BUTTON_REGION[0], GOON_BUTTON_REGION[1])
