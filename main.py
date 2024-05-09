from answer import Answer
from word import Word

if __name__ == '__main__':
    word = Word()
    answer = Answer()

    n = int(input("输入单词个数"))
    for i in range(n):
        word.routine()

    word_dic = word.get_dic()

    m = int(input("输入测试个数"))
    for k in range(m):
        try:
            answer.routine(word_dic)
        except IndexError:
            # 这里用来处理意外
            input("识别个数错误,请自行做题并点击继续后按任意键继续运行")

    answer.show_result()
