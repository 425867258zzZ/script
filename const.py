"""
仅支持2K分辨率显示屏下运行
"""

WORD_IMAGE_PATH = "image/word_image.png"
TRANSLATION_IMAGE_PATH = "image/translation_image.png"
TRANSLATION_IN_QUESTION_PATH = "image/translation_image.png"
WORD_IN_QUESTION_PATH = "image/word_in_question.png"
SCREENSHOT_PATH = "image/screenshot.png"
# 全屏区域
SCREENSHOT_REGION = (67, 238, 1199, 1138)
# 跳过单词所在区域
WORD_REGION = (400, 370, 500, 90)
# 跳过部分单词的释义所在区域
TRANSLATION_REGION = (142, 840, 550, 284)
# 继续按钮坐标
GOON_BUTTON_REGION = (971, 1314)
# 下一题按钮坐标
NEXT_BUTTON_REGION = (966, 1335)
# 听力部分选项区域
LISTEN_OPTION_REGION = (198, 546, 943, 686)
# 识图config
ENGLISH_CONFIG = r'--oem 3 --psm 6 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz.'


class Line:
    translation_in_question_region = word_in_question_region = option1 = option2 = option3 = option4 = ()

    def get_option_zone(self):
        """
        :return: 4个选项按钮坐标
        """
        return [self.option1, self.option2, self.option3, self.option4]

    def get_question_region(self):
        """
        :return: 题干所在区域
        """
        return self.word_in_question_region

    def get_translation_region(self):
        """
        :return: 选项所在区域
        """
        return self.translation_in_question_region


class Line5(Line):
    # 包含绿色单词的题干区域
    word_in_question_region = (60, 311, 1150, 105)
    # 题干选项区域
    translation_in_question_region = (320, 473, 700, 712)
    # 四个选项区域
    option1 = (1108, 551)
    option2 = (1108, 742)
    option3 = (1108, 921)
    option4 = (1108, 1110)


class Line6(Line):
    # 包含绿色单词的题干区域
    word_in_question_region = (60, 324, 1164, 191)
    # 题干选项区域
    translation_in_question_region = (322, 567, 700, 805)
    # 四个选项区域
    option1 = (1108, 641)
    option2 = (1108, 826)
    option3 = (1108, 1012)
    option4 = (1108, 1200)


class Line7(Line):
    # 包含绿色单词的题干区域
    word_in_question_region = (60, 329, 1115, 266)
    # 题干选项区域
    translation_in_question_region = (315, 660, 814, 676)
    # 四个选项区域
    option1 = (1108, 732)
    option2 = (1108, 917)
    option3 = (1108, 1111)
    option4 = (1108, 1274)
